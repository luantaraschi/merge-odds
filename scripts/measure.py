#!/usr/bin/env python3
"""Measure one repository and print its data/repos entry.

Usage:
    python scripts/measure.py owner/repo [--write]
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from merge_odds.entry import build_entry, dump, entry_path  # noqa: E402
from merge_odds.github import GitHub, GitHubUnavailable, RepoNotFound  # noqa: E402
from merge_odds.policy import CANDIDATE_FILES, scan  # noqa: E402


def measure(repo: str, client: GitHub) -> dict:
    meta = client.repo(repo)
    pulls = [] if meta.archived else client.closed_pulls(meta.full_name)
    files = {
        path: body
        for path in CANDIDATE_FILES
        if (body := client.raw_file(meta.full_name, meta.head_sha, path))
    }
    return build_entry(meta, pulls, scan(files), date.today().isoformat())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", help="owner/name")
    parser.add_argument("--write", action="store_true", help="write into data/repos/")
    arguments = parser.parse_args()

    try:
        entry = measure(arguments.repo, GitHub())
    except RepoNotFound:
        print(f"repository not found: {arguments.repo}", file=sys.stderr)
        return 1
    except GitHubUnavailable as error:
        print(f"GitHub request failed: {error}", file=sys.stderr)
        return 1

    text = dump(entry)
    if arguments.write:
        target = Path(entry_path(entry["repo"]))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {target}", file=sys.stderr)
        if "_review" in entry:
            print(
                f"{len(entry['_review'])} quote(s) need review before this passes CI",
                file=sys.stderr,
            )
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
