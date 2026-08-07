import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from merge_odds.github import RepoMeta
from merge_odds.prs import MIN_HUMAN_SAMPLE, PullRequest
from refresh_module import refresh_entry

FIXTURES = Path(__file__).parent / "fixtures"
BASE = datetime(2026, 7, 1, tzinfo=timezone.utc)
META = RepoMeta(
    full_name="payloadcms/payload",
    archived=False,
    default_branch="main",
    head_sha="c" * 40,
)


def load():
    return json.loads((FIXTURES / "entry_valid.json").read_text(encoding="utf-8"))


def sample():
    return [
        PullRequest(
            author=f"person{i}",
            is_bot=False,
            created_at=BASE,
            closed_at=BASE + timedelta(days=1),
            merged_at=BASE + timedelta(days=1),
        )
        for i in range(MIN_HUMAN_SAMPLE)
    ]


def intact(repo, sha, path):
    return "intro\nClaude Code is supported.\noutro\n"


def changed(repo, sha, path):
    return "intro\nWe removed that section.\noutro\n"


def test_statistics_are_recomputed():
    updated, stale = refresh_entry(load(), META, sample(), intact, "2026-09-01")

    assert updated["merge_stats"]["median_days_to_merge"] == 1.0
    assert updated["measured_at"] == "2026-09-01"
    assert stale == []


def test_policy_and_evidence_are_never_touched():
    original = load()

    updated, _ = refresh_entry(original, META, sample(), changed, "2026-09-01")

    assert updated["policy"] == original["policy"]
    assert updated["default_branch_sha"] == original["default_branch_sha"]


def test_a_quote_that_stopped_matching_marks_the_entry_stale():
    updated, stale = refresh_entry(load(), META, sample(), changed, "2026-09-01")

    assert updated["policy_stale"] is True
    assert stale and "CONTRIBUTING.md" in stale[0]


def test_a_repaired_quote_clears_the_flag():
    entry = dict(load(), policy_stale=True)

    updated, stale = refresh_entry(entry, META, sample(), intact, "2026-09-01")

    assert "policy_stale" not in updated
    assert stale == []
