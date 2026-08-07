"""Assembles and serialises a data/repos entry."""

from __future__ import annotations

import json

from .github import RepoMeta
from .policy import Candidate
from .prs import PullRequest, merge_stats


def evidence_url(repo: str, sha: str, path: str, start: int, end: int) -> str:
    anchor = f"#L{start}" if start == end else f"#L{start}-L{end}"
    return f"https://github.com/{repo}/blob/{sha}/{path}{anchor}"


def build_entry(
    meta: RepoMeta,
    pulls: list[PullRequest],
    candidates: list[Candidate],
    measured_at: str,
) -> dict:
    entry: dict = {
        "repo": meta.full_name,
        "measured_at": measured_at,
        "default_branch_sha": meta.head_sha,
        "policy": {
            "accepts_external_prs": True,
            "requires_issue_first": False,
            "ai_assisted_code": "not_stated",
            "ai_authored_pr_text": "not_stated",
            "evidence": [],
        },
    }

    if meta.archived:
        entry["archived"] = True
    else:
        computed = merge_stats(pulls)
        if computed["insufficient_sample"]:
            entry["insufficient_sample"] = True
        entry["merge_stats"] = computed["merge_stats"]

    if candidates:
        entry["_review"] = [
            {
                "claim": candidate.claim,
                "source": candidate.source,
                "url": evidence_url(
                    meta.full_name,
                    meta.head_sha,
                    candidate.source,
                    candidate.line_start,
                    candidate.line_end,
                ),
                "quote": candidate.quote,
            }
            for candidate in candidates
        ]

    return entry


def entry_path(repo: str) -> str:
    owner, name = repo.split("/", 1)
    return f"data/repos/{owner}__{name}.json"


def dump(entry: dict) -> str:
    return json.dumps(entry, indent=2, ensure_ascii=False) + "\n"
