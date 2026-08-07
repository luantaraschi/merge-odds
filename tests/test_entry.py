import json
from datetime import datetime, timedelta, timezone

from merge_odds.entry import build_entry, dump, entry_path
from merge_odds.github import RepoMeta
from merge_odds.policy import Candidate
from merge_odds.prs import MIN_HUMAN_SAMPLE, PullRequest

BASE = datetime(2026, 6, 1, tzinfo=timezone.utc)
META = RepoMeta(
    full_name="payloadcms/payload",
    archived=False,
    default_branch="main",
    head_sha="a" * 40,
)


def sample(count=MIN_HUMAN_SAMPLE):
    return [
        PullRequest(
            author=f"person{i}",
            is_bot=False,
            created_at=BASE,
            closed_at=BASE + timedelta(days=2),
            merged_at=BASE + timedelta(days=2),
        )
        for i in range(count)
    ]


def test_entry_starts_with_every_stance_unset():
    entry = build_entry(META, sample(), [], "2026-08-07")

    assert entry["policy"]["ai_assisted_code"] == "not_stated"
    assert entry["policy"]["accepts_external_prs"] is True
    assert entry["policy"]["evidence"] == []


def test_candidates_land_in_review_never_in_evidence():
    candidate = Candidate(
        claim="ai_assisted_code",
        source="CONTRIBUTING.md",
        line_start=10,
        line_end=12,
        quote="Claude Code is supported.",
    )

    entry = build_entry(META, sample(), [candidate], "2026-08-07")

    assert entry["policy"]["evidence"] == []
    assert len(entry["_review"]) == 1
    assert entry["_review"][0]["url"] == (
        "https://github.com/payloadcms/payload/blob/"
        + "a" * 40
        + "/CONTRIBUTING.md#L10-L12"
    )


def test_archived_repo_carries_no_stats():
    meta = RepoMeta(
        full_name="old/thing", archived=True, default_branch="main", head_sha="b" * 40
    )

    entry = build_entry(meta, [], [], "2026-08-07")

    assert entry["archived"] is True
    assert "merge_stats" not in entry


def test_small_sample_is_flagged():
    entry = build_entry(META, sample(4), [], "2026-08-07")

    assert entry["insufficient_sample"] is True
    assert "casual_author_acceptance" not in entry["merge_stats"]


def test_path_is_derived_from_the_repo_name():
    assert entry_path("payloadcms/payload") == "data/repos/payloadcms__payload.json"


def test_dump_is_stable_and_ends_with_a_newline():
    entry = build_entry(META, sample(), [], "2026-08-07")
    text = dump(entry)

    assert text.endswith("\n")
    assert json.loads(text) == entry
    assert dump(json.loads(text)) == text
