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
    "Sample recency",
    "Measured",
)

STANCE_LABEL = {
    "allowed": "allowed",
    "allowed_with_conditions": "conditional",
    "not_stated": DASH,
    "disallowed": "disallowed",
}


def _number(stats: dict, key: str, suffix: str = "") -> str:
    # Rendering-layer precision only: the stored data keeps its full
    # figures, but four decimal places on a median of a few dozen values
    # is false precision on the page.
    if key not in stats:
        return DASH
    return f"{round(stats[key], 2)}{suffix}"


def _evidence_url(policy: dict, claim: str) -> str | None:
    for item in policy["evidence"]:
        if item["claim"] == claim:
            return item["url"]
    return None


def _cell(text: str, url: str | None) -> str:
    return f"[{text}]({url})" if url else text


def _row(entry: dict) -> str:
    policy = entry["policy"]
    stats = entry.get("merge_stats", {})
    name = entry["repo"]
    cells = [
        f"[{name}](https://github.com/{name})",
        _cell(
            "yes" if policy["accepts_external_prs"] else "**no**",
            _evidence_url(policy, "accepts_external_prs"),
        ),
        _cell(
            "yes" if policy["requires_issue_first"] else DASH,
            _evidence_url(policy, "requires_issue_first"),
        ),
        _cell(
            STANCE_LABEL[policy["ai_assisted_code"]],
            _evidence_url(policy, "ai_assisted_code"),
        ),
        _cell(
            STANCE_LABEL[policy["ai_authored_pr_text"]],
            _evidence_url(policy, "ai_authored_pr_text"),
        ),
        _number(stats, "casual_author_acceptance"),
        _number(stats, "median_days_to_merge", " d"),
        _number(stats, "p90_days_to_merge", " d"),
        _number(stats, "median_close_age_days", " d"),
        entry["measured_at"],
    ]
    return "| " + " | ".join(cells) + " |"


def render_table(entries: list[dict]) -> str:
    header = "| " + " | ".join(COLUMNS) + " |"
    divider = "|" + "---|" * len(COLUMNS)
    rows = [_row(entry) for entry in sorted(entries, key=lambda e: e["repo"].lower())]
    return "\n".join([header, divider, *rows])


def splice(readme: str, table: str) -> str:
    start_count = readme.count(START)
    end_count = readme.count(END)

    if start_count != 1:
        raise ValueError(f"expected exactly one {START!r} marker, found {start_count}")
    if end_count != 1:
        raise ValueError(f"expected exactly one {END!r} marker, found {end_count}")

    start_index = readme.index(START)
    end_index = readme.index(END)
    if start_index > end_index:
        raise ValueError(f"{START!r} marker must appear before {END!r} marker")

    before = readme[:start_index]
    after = readme[end_index + len(END) :]
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
