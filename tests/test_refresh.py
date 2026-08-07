import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import refresh_module
from merge_odds.github import RepoMeta, RepoNotFound
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


def _write_minimal_entry(path: Path, repo: str) -> None:
    path.write_text(
        json.dumps(
            {
                "repo": repo,
                "measured_at": "2026-01-01",
                "default_branch_sha": "a" * 40,
                "policy": {
                    "accepts_external_prs": True,
                    "requires_issue_first": False,
                    "ai_assisted_code": "not_stated",
                    "ai_authored_pr_text": "not_stated",
                    "evidence": [],
                },
            }
        ),
        encoding="utf-8",
    )


def test_main_continues_past_a_repo_that_vanishes_between_repo_and_pulls_calls(
    tmp_path, monkeypatch
):
    """A narrow race: client.repo() succeeds, but the repository is gone or
    private by the time client.closed_pulls() runs. RepoNotFound raised from
    the second call must be handled the same way as from the first, not
    escape main() and abort the rest of the run.
    """
    repos_dir = tmp_path / "data" / "repos"
    repos_dir.mkdir(parents=True)
    _write_minimal_entry(repos_dir / "a__ok.json", "a/ok")
    _write_minimal_entry(repos_dir / "b__vanished.json", "b/vanished")

    class FakeClient:
        def repo(self, name):
            return RepoMeta(
                full_name=name, archived=False, default_branch="main", head_sha="c" * 40
            )

        def closed_pulls(self, name):
            if name == "b/vanished":
                raise RepoNotFound(name)
            return []

        def raw_file(self, name, sha, path):
            return None

    monkeypatch.setattr(refresh_module, "ROOT", tmp_path)
    monkeypatch.setattr(refresh_module, "GitHub", lambda: FakeClient())

    rc = refresh_module.main()

    assert rc == 0
    report = (tmp_path / "refresh-report.md").read_text(encoding="utf-8")
    assert "b/vanished" in report
    assert "is gone or private" in report

    updated = json.loads((repos_dir / "a__ok.json").read_text(encoding="utf-8"))
    assert updated["measured_at"] != "2026-01-01"

    untouched = json.loads((repos_dir / "b__vanished.json").read_text(encoding="utf-8"))
    assert untouched["measured_at"] == "2026-01-01"
