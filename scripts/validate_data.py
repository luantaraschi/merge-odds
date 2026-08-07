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
        body = fetch(entry["repo"], sha, item["source"])
        if body is None:
            problems.append(f"{item['source']}: file not readable at {sha[:8]}")
            continue
        if item["quote"].replace("\r\n", "\n") not in body.replace("\r\n", "\n"):
            problems.append(
                f"{item['source']}: quote not found verbatim at {sha[:8]}"
            )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    arguments = parser.parse_args()

    paths = arguments.paths or sorted((ROOT / "data" / "repos").glob("*.json"))
    paths = [path for path in paths if path.suffix == ".json" and path.exists()]

    client = GitHub()
    failed = False

    for path in paths:
        entry = json.loads(path.read_text(encoding="utf-8"))
        problems = schema_errors(entry)
        if not problems:
            problems = pairing_errors(entry)
            try:
                problems += quote_errors(entry, client.raw_file)
            except GitHubUnavailable as error:
                # A transient failure (persistent 5xx, exhausted rate-limit
                # retries, ...) means the quotes for this entry could not be
                # checked at all. That must never be silently treated as a
                # pass, so it becomes its own clear, non-zero-exit failure.
                problems.append(f"could not verify quotes: {error}")
        if problems:
            failed = True
            print(f"{path}:", file=sys.stderr)
            for problem in problems:
                print(f"  {problem}", file=sys.stderr)

    if not failed:
        print(f"{len(paths)} entries valid")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
