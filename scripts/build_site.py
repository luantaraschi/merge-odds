#!/usr/bin/env python3
"""Build the static site data and its no-script dataset table."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "repos"
SITE_DIR = ROOT / "site"
TEMPLATE_PATH = SITE_DIR / "index.template.html"
INDEX_PATH = SITE_DIR / "index.html"
DATA_PATH = SITE_DIR / "repos.json"
ROWS_MARKER = "<!-- merge-odds:dataset-rows -->"
OPTIONS_MARKER = "<!-- merge-odds:repo-options -->"

STANCE_LABELS = {
    "allowed": "allowed",
    "allowed_with_conditions": "conditional",
    "not_stated": "not stated",
    "disallowed": "disallowed",
}


def load_entries() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(DATA_DIR.glob("*.json"))
    ]


def evidence_for(policy: dict, claim: str) -> dict | None:
    found = None
    for item in policy["evidence"]:
        if item["claim"] == claim:
            found = {"source": item["source"], "url": item["url"]}
    return found


def public_entry(entry: dict) -> dict:
    policy = entry["policy"]
    stats = entry.get("merge_stats", {})
    return {
        "repo": entry["repo"],
        "measured_at": entry["measured_at"],
        "sha": entry["default_branch_sha"],
        "archived": entry.get("archived", False),
        "insufficient_sample": entry.get("insufficient_sample", False),
        "policy": {
            "accepts_external_prs": policy["accepts_external_prs"],
            "requires_issue_first": policy["requires_issue_first"],
            "ai_assisted_code": policy["ai_assisted_code"],
            "ai_authored_pr_text": policy["ai_authored_pr_text"],
        },
        "evidence": {
            claim: evidence_for(policy, claim)
            for claim in (
                "accepts_external_prs",
                "requires_issue_first",
                "ai_assisted_code",
                "ai_authored_pr_text",
            )
        },
        "stats": {
            key: round(value, 2)
            for key, value in stats.items()
            if key
            in {
                "sample_size",
                "casual_sample_size",
                "casual_author_acceptance",
                "median_days_to_merge",
                "p90_days_to_merge",
                "median_close_age_days",
            }
        },
    }


def cell(value: str, label: str) -> str:
    return f'<td data-label="{html.escape(label)}">{html.escape(value)}</td>'


def dataset_row(entry: dict) -> str:
    policy = entry["policy"]
    stats = entry["stats"]
    acceptance = stats.get("casual_author_acceptance")
    median = stats.get("median_days_to_merge")
    evidence_count = sum(item is not None for item in entry["evidence"].values())
    values = (
        entry["repo"],
        "yes" if policy["accepts_external_prs"] else "no",
        "yes" if policy["requires_issue_first"] else "not required",
        STANCE_LABELS[policy["ai_assisted_code"]],
        STANCE_LABELS[policy["ai_authored_pr_text"]],
        "not available" if acceptance is None else f"{round(acceptance * 100)}%",
        "not available" if median is None else f"{median} days",
        str(evidence_count),
        entry["measured_at"],
    )
    labels = (
        "Project",
        "External PRs",
        "Issue first",
        "AI code",
        "AI PR text",
        "Casual acceptance",
        "Median to merge",
        "Sources",
        "Measured",
    )
    project_url = f"https://github.com/{html.escape(entry['repo'])}"
    project = (
        '<td data-label="Project">'
        f'<a href="{project_url}">{html.escape(entry["repo"])}</a>'
        "</td>"
    )
    other_cells = "".join(cell(value, label) for value, label in zip(values[1:], labels[1:]))
    return f'<tr data-repo="{html.escape(entry["repo"].lower())}">{project}{other_cells}</tr>'


def replace_once(source: str, marker: str, value: str) -> str:
    if source.count(marker) != 1:
        raise ValueError(f"expected exactly one {marker!r}")
    return source.replace(marker, value)


def build(entries: list[dict]) -> tuple[str, str]:
    public_entries = [public_entry(entry) for entry in entries]
    public_entries.sort(key=lambda entry: entry["repo"].lower())
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    rows = "\n".join(dataset_row(entry) for entry in public_entries)
    options = "\n".join(
        f'<option value="{html.escape(entry["repo"])}">{html.escape(entry["repo"])}</option>'
        for entry in public_entries
    )
    page = replace_once(template, ROWS_MARKER, rows)
    page = replace_once(page, OPTIONS_MARKER, options)
    data = json.dumps(public_entries, indent=2, ensure_ascii=False) + "\n"
    return page, data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    page, data = build(load_entries())

    if arguments.check:
        stale = []
        if not INDEX_PATH.exists() or INDEX_PATH.read_text(encoding="utf-8") != page:
            stale.append(INDEX_PATH.relative_to(ROOT))
        if not DATA_PATH.exists() or DATA_PATH.read_text(encoding="utf-8") != data:
            stale.append(DATA_PATH.relative_to(ROOT))
        if stale:
            print(f"site output is stale: {', '.join(map(str, stale))}", file=sys.stderr)
            return 1
        return 0

    INDEX_PATH.write_text(page, encoding="utf-8", newline="\n")
    DATA_PATH.write_text(data, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
