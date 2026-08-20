#!/usr/bin/env python3
"""Reject punctuation patterns prohibited in public copy: README, site, and skills."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = (
    (re.compile(r"[—–]"), "em dash or en dash"),
    (re.compile(r"[\t ]--?[\t ]"), "ASCII hyphen used as sentence punctuation"),
    (re.compile(r"[\t ]--?[\t ]*$", re.MULTILINE), "trailing ASCII hyphen punctuation"),
)


def public_files() -> list[Path]:
    files = [ROOT / "README.md"]
    files.extend(
        path
        for path in (ROOT / "site").rglob("*")
        if path.is_file() and path.suffix in {".html", ".js", ".md", ".svg"}
    )
    # Skills ship inside the plugin and are read by whoever installs it,
    # which makes them public copy under the same rules as the site.
    files.extend(
        path for path in (ROOT / "skills").rglob("*.md") if path.is_file()
    )
    return sorted(files)


def problems_in(text: str) -> list[tuple[int, str]]:
    problems = []
    for pattern, description in FORBIDDEN:
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            problems.append((line, description))
    return problems


def main() -> int:
    problems = []
    for path in public_files():
        text = path.read_text(encoding="utf-8")
        for line, description in problems_in(text):
            problems.append(f"{path.relative_to(ROOT)}:{line}: {description}")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print(f"checked {len(public_files())} public content files; 0 problems")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
