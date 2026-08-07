#!/usr/bin/env python3
"""Render the README table from data/repos.

Usage:
    python scripts/render.py            rewrite README.md
    python scripts/render.py --check    exit 1 when README.md is out of date
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- merge-odds:table:start -->"
END = "<!-- merge-odds:table:end -->"
DASH = "—"

COLUMNS = (
    "Project",
    "External PRs",
    "Issue first",
    "AI code",
    "AI PR text",
    "Casual acceptance",
    "Median",
    "p90",
    "Measured",
)

STANCE_LABEL = {
    "allowed": "allowed",
    "allowed_with_conditions": "conditional",
    "not_stated": DASH,
    "disallowed": "disallowed",
}


def _number(stats: dict, key: str, suffix: str = "") -> str:
    if key not in stats:
        return DASH
    return f"{stats[key]}{suffix}"


def _row(entry: dict) -> str:
    policy = entry["policy"]
    stats = entry.get("merge_stats", {})
    name = entry["repo"]
    cells = [
        f"[{name}](https://github.com/{name})",
        "yes" if policy["accepts_external_prs"] else "**no**",
        "yes" if policy["requires_issue_first"] else DASH,
        STANCE_LABEL[policy["ai_assisted_code"]],
        STANCE_LABEL[policy["ai_authored_pr_text"]],
        _number(stats, "casual_author_acceptance"),
        _number(stats, "median_days_to_merge", " d"),
        _number(stats, "p90_days_to_merge", " d"),
        entry["measured_at"],
    ]
    return "| " + " | ".join(cells) + " |"


def render_table(entries: list[dict]) -> str:
    header = "| " + " | ".join(COLUMNS) + " |"
    divider = "|" + "---|" * len(COLUMNS)
    rows = [_row(entry) for entry in sorted(entries, key=lambda e: e["repo"].lower())]
    return "\n".join([header, divider, *rows])


def splice(readme: str, table: str) -> str:
    before, _, rest = readme.partition(START)
    _, _, after = rest.partition(END)
    return f"{before}{START}\n{table}\n{END}{after}"


def load_entries() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "data" / "repos").glob("*.json"))
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()

    readme_path = ROOT / "README.md"
    current = readme_path.read_text(encoding="utf-8")
    updated = splice(current, render_table(load_entries()))

    if arguments.check:
        if current != updated:
            print("README.md is out of date; run: python scripts/render.py", file=sys.stderr)
            return 1
        return 0

    readme_path.write_text(updated, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
