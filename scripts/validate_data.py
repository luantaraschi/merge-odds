#!/usr/bin/env python3
"""Validate data/repos entries: schema, evidence pairing, verbatim quotes.

Usage:
    python scripts/validate_data.py                 all entries
    python scripts/validate_data.py path [path...]  only these
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from merge_odds.github import GitHub, GitHubUnavailable  # noqa: E402

SCHEMA = json.loads((ROOT / "schema" / "repo.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)

DEFAULT_STANCE = {
    "accepts_external_prs": True,
    "requires_issue_first": False,
    "ai_assisted_code": "not_stated",
    "ai_authored_pr_text": "not_stated",
}


def schema_errors(entry: dict) -> list[str]:
    return [
        f"{'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in VALIDATOR.iter_errors(entry)
    ]


def pairing_errors(entry: dict) -> list[str]:
    policy = entry["policy"]
    claimed = {item["claim"] for item in policy["evidence"]}
    return [
        f"{claim}: stance differs from the default but no evidence quotes it"
        for claim, default in DEFAULT_STANCE.items()
        if policy[claim] != default and claim not in claimed
    ]


def quote_errors(entry: dict, fetch) -> list[str]:
    problems = []
    for item in entry["policy"]["evidence"]:
        sha = item["url"].split("/blob/")[1].split("/")[0]
        try:
            body = fetch(entry["repo"], sha, item["source"])
        except GitHubUnavailable as error:
            # A transient failure (persistent 5xx, exhausted rate-limit
            # retries, ...) means this particular quote could not be
            # checked. Record it and keep checking the rest of the
            # evidence for this entry instead of losing findings already
            # made for other items.
            problems.append(
                f"{item['source']}: could not verify quote at {sha[:8]}: {error}"
            )
            continue
        if body is None:
            problems.append(f"{item['source']}: file not readable at {sha[:8]}")
            continue
        if item["quote"].replace("\r\n", "\n") not in body.replace("\r\n", "\n"):
            problems.append(
                f"{item['source']}: quote not found verbatim at {sha[:8]}"
            )
    return problems


def _resolve_paths(raw_paths: list[Path]) -> tuple[list[Path], list[str]]:
    """Resolve explicit CLI path arguments.

    Every argument must exist, be a file and end in ``.json``. Unlike a
    directory glob, an explicit argument that quietly resolves to nothing
    is a bug, not an empty result -- it must never look like "there was
    nothing to check" when the user actually asked for something specific.
    """
    resolved = []
    bad_arguments = []
    for candidate in raw_paths:
        if candidate.is_file() and candidate.suffix == ".json":
            resolved.append(candidate)
        else:
            bad_arguments.append(f"{candidate}: not a readable .json file")
    return resolved, bad_arguments


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    arguments = parser.parse_args()

    failed = False

    if arguments.paths:
        paths, bad_arguments = _resolve_paths(arguments.paths)
        if bad_arguments:
            failed = True
            for problem in bad_arguments:
                print(problem, file=sys.stderr)
    else:
        # No arguments: validate everything under data/repos/. An empty
        # directory legitimately yields zero entries here.
        paths = sorted((ROOT / "data" / "repos").glob("*.json"))

    client = GitHub()

    for path in paths:
        try:
            entry = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            failed = True
            print(f"{path}:", file=sys.stderr)
            print(f"  invalid JSON: {error}", file=sys.stderr)
            continue

        problems = schema_errors(entry)
        if not problems:
            problems = pairing_errors(entry) + quote_errors(entry, client.raw_file)
        if problems:
            failed = True
            print(f"{path}:", file=sys.stderr)
            for problem in problems:
                print(f"  {problem}", file=sys.stderr)

    if not failed:
        # Only reachable when every requested path (or, with no arguments,
        # every entry under data/repos/) was actually checked -- so "0
        # entries valid" can only appear for a legitimately empty directory,
        # never for a run that silently checked nothing it was asked to.
        print(f"{len(paths)} entries valid")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
