"""Analysis of a closed pull request sample. Pure functions, no network."""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from statistics import median

CASUAL_MAX_APPEARANCES = 2
"""An author appearing more often than this is not an outsider passing through."""

MIN_HUMAN_SAMPLE = 20
"""Below this many human pull requests, percentages are noise."""

MIN_CASUAL_SAMPLE = 20
"""Below this many casual pull requests, the acceptance denominator is noise."""

BOT_LOGINS = frozenset(
    {
        "allcontributors",
        "codecov",
        "crowdin-bot",
        "dependabot",
        "dependabot-preview",
        "github-actions",
        "greenkeeper",
        "imgbot",
        "mergify",
        "pre-commit-ci",
        "renovate",
        "renovate-bot",
        "restyled-io",
        "snyk-bot",
        "sonarcloud",
        "step-security-bot",
        "whitesource-bourbon",
    }
)


@dataclass(frozen=True)
class PullRequest:
    author: str
    is_bot: bool
    created_at: datetime
    closed_at: datetime
    merged_at: datetime | None


def is_bot(login: str, account_type: str) -> bool:
    if account_type == "Bot":
        return True
    login = (login or "").lower()
    return login.endswith("[bot]") or login in BOT_LOGINS


def _percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    low, high = math.floor(position), math.ceil(position)
    if low == high:
        return round(ordered[low], 4)
    interpolated = ordered[low] * (high - position) + ordered[high] * (position - low)
    return round(interpolated, 4)


def _days(pull: PullRequest) -> float:
    return (pull.merged_at - pull.created_at).total_seconds() / 86400


def merge_stats(sample: list[PullRequest]) -> dict:
    humans = [pull for pull in sample if not pull.is_bot and pull.author]
    stats: dict[str, object] = {
        "sample_size": len(humans),
        "window_days": 0.0,
        "bots_excluded": True,
    }

    if humans:
        closed = [pull.closed_at for pull in humans]
        stats["window_days"] = round((max(closed) - min(closed)).total_seconds() / 86400, 4)

    appearances = Counter(pull.author for pull in humans)
    casual = [
        pull for pull in humans if appearances[pull.author] <= CASUAL_MAX_APPEARANCES
    ]
    stats["casual_sample_size"] = len(casual)

    if len(humans) < MIN_HUMAN_SAMPLE or len(casual) < MIN_CASUAL_SAMPLE:
        return {"merge_stats": stats, "insufficient_sample": True}

    merged = [pull for pull in casual if pull.merged_at is not None]

    stats["casual_author_acceptance"] = (
        round(len(merged) / len(casual), 4) if casual else 0.0
    )
    stats["distinct_merged_casual_authors"] = len({pull.author for pull in merged})

    latencies = [_days(pull) for pull in merged]
    stats["median_days_to_merge"] = round(median(latencies), 4) if latencies else 0.0
    stats["p90_days_to_merge"] = _percentile(latencies, 0.9) if latencies else 0.0

    return {"merge_stats": stats, "insufficient_sample": False}
