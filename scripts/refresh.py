#!/usr/bin/env python3
"""Re-measure every entry weekly. Never rewrites a quote.

Usage:
    python scripts/refresh.py
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from merge_odds.entry import dump  # noqa: E402
from merge_odds.github import (  # noqa: E402
    GitHub,
    GitHubUnavailable,
    RepoMeta,
    RepoNotFound,
)
from merge_odds.prs import PullRequest, merge_stats  # noqa: E402


def refresh_entry(
    entry: dict,
    meta: RepoMeta,
    pulls: list[PullRequest],
    fetch,
    today: str,
) -> tuple[dict, list[str]]:
    """Update statistics in place. Policy and evidence are read-only here.

    ``fetch`` may raise ``GitHubUnavailable`` when a source file could not
    be checked (as opposed to returning ``None``, which means the file is
    genuinely gone). That is not evidence of drift -- it is deliberately
    left uncaught here so it propagates to the caller, which knows how to
    tell "GitHub had a bad minute" apart from "the policy text changed".
    """
    updated = json.loads(json.dumps(entry))
    updated["measured_at"] = today

    updated.pop("archived", None)
    updated.pop("insufficient_sample", None)
    updated.pop("merge_stats", None)

    if meta.archived:
        updated["archived"] = True
    else:
        computed = merge_stats(pulls)
        if computed["insufficient_sample"]:
            updated["insufficient_sample"] = True
        updated["merge_stats"] = computed["merge_stats"]

    stale = []
    for item in updated["policy"]["evidence"]:
        body = fetch(updated["repo"], meta.head_sha, item["source"])
        if body is None or item["quote"].replace("\r\n", "\n") not in body.replace(
            "\r\n", "\n"
        ):
            stale.append(f"{item['source']}: {item['claim']}")

    if stale:
        updated["policy_stale"] = True
    else:
        updated.pop("policy_stale", None)

    return updated, stale


def main() -> int:
    client = GitHub()
    today = date.today().isoformat()
    report: list[str] = []

    for path in sorted((ROOT / "data" / "repos").glob("*.json")):
        entry = json.loads(path.read_text(encoding="utf-8"))
        try:
            meta = client.repo(entry["repo"])
        except RepoNotFound:
            report.append(f"- `{entry['repo']}` is gone or private")
            continue
        except GitHubUnavailable as error:
            # We could not even confirm the repository is still there.
            # This is not drift -- it is a failed check -- so it must not
            # be conflated with a stale quote. Record it and move on to
            # the rest of the entries instead of aborting the whole run.
            report.append(f"- `{entry['repo']}` could not be re-measured: {error}")
            continue

        try:
            pulls = [] if meta.archived else client.closed_pulls(meta.full_name)
            updated, stale = refresh_entry(
                entry, meta, pulls, client.raw_file, today
            )
        except RepoNotFound:
            # A narrow race: the repository existed when client.repo() ran
            # above but was deleted or made private before closed_pulls()
            # got to it. Same handling as the first-stage check.
            report.append(f"- `{entry['repo']}` is gone or private")
            continue
        except GitHubUnavailable as error:
            # Same reasoning as above: a fetch failure while recomputing
            # statistics or checking evidence quotes is a transient problem,
            # not a signal that the policy text changed. Skip writing this
            # entry this week rather than guessing, and keep going.
            report.append(f"- `{entry['repo']}` could not be re-measured: {error}")
            continue

        path.write_text(dump(updated), encoding="utf-8", newline="\n")

        for problem in stale:
            report.append(f"- `{entry['repo']}` — {problem}")

    Path(ROOT / "refresh-report.md").write_text(
        "\n".join(report) or "No policy drift.", encoding="utf-8", newline="\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
