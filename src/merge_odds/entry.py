"""Assembles and serialises a data/repos entry."""

from __future__ import annotations

import json

from .github import RepoMeta
from .policy import Candidate
from .prs import PullRequest, merge_stats

CLAIM_ORDER = (
    "accepts_external_prs",
    "requires_issue_first",
    "ai_assisted_code",
    "ai_authored_pr_text",
)
"""Matches the order of ``$defs.claim.enum`` in schema/repo.schema.json."""


def evidence_url(repo: str, sha: str, path: str, start: int, end: int) -> str:
    anchor = f"#L{start}" if start == end else f"#L{start}-L{end}"
    return f"https://github.com/{repo}/blob/{sha}/{path}{anchor}"


def build_entry(
    meta: RepoMeta,
    pulls: list[PullRequest],
    candidates: list[Candidate],
    measured_at: str,
    files_read: tuple[str, ...] = (),
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

    matched_claims = {candidate.claim for candidate in candidates}
    unmatched_claims = [claim for claim in CLAIM_ORDER if claim not in matched_claims]

    entry["_review"] = {
        "candidates": [
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
        ],
        "unmatched_claims": unmatched_claims,
        "files_read": list(files_read),
    }

    return entry


def entry_path(repo: str) -> str:
    owner, name = repo.split("/", 1)
    return f"data/repos/{owner}__{name}.json"


def dump(entry: dict) -> str:
    return json.dumps(entry, indent=2, ensure_ascii=False) + "\n"
