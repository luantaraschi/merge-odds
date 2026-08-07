import json
from pathlib import Path

import pytest
import requests

from merge_odds.github import MAX_ATTEMPTS, GitHub, GitHubUnavailable, RepoNotFound

FIXTURES = Path(__file__).parent / "fixtures"


class FakeResponse:
    def __init__(self, status_code, payload=None, text="", headers=None):
        self.status_code = status_code
        self._payload = payload
        self.text = text
        self.headers = headers or {}

    def json(self):
        return self._payload


class FakeSession:
    """Replays canned responses in order and records the URLs asked for."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.urls = []

    def get(self, url, **kwargs):
        self.urls.append(url)
        return self._responses.pop(0)


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


HEAD = FakeResponse(200, {"sha": "a" * 40})
"""GitHub.repo() makes two calls: repository metadata, then the head commit."""


def test_repo_reads_metadata():
    session = FakeSession([FakeResponse(200, load("repo_payload.json")), HEAD])

    meta = GitHub(session=session).repo("payloadcms/payload")

    assert meta.full_name == "payloadcms/payload"
    assert meta.archived is False
    assert meta.default_branch
    assert meta.head_sha == "a" * 40


def test_repo_follows_a_rename():
    payload = dict(load("repo_payload.json"), full_name="calcom/cal.diy")
    session = FakeSession([FakeResponse(200, payload), HEAD])

    meta = GitHub(session=session).repo("calcom/cal.com")

    assert meta.full_name == "calcom/cal.diy"
    assert "/repos/calcom/cal.diy/commits/" in session.urls[1]


def test_missing_repo_raises():
    session = FakeSession([FakeResponse(404, {"message": "Not Found"})])

    with pytest.raises(RepoNotFound):
        GitHub(session=session).repo("nobody/nothing")


def test_closed_pulls_maps_bots_and_timestamps():
    session = FakeSession([FakeResponse(200, load("pulls_payload.json"))])

    pulls = GitHub(session=session).closed_pulls("payloadcms/payload")

    assert pulls
    assert all(pull.closed_at is not None for pull in pulls)
    assert any(pull.merged_at is not None for pull in pulls)


def test_raw_file_returns_none_on_404():
    session = FakeSession([FakeResponse(404, text="")])

    assert GitHub(session=session).raw_file("a/b", "0" * 40, "AGENTS.md") is None


def test_raw_file_raises_on_persistent_server_error():
    session = FakeSession([FakeResponse(500, text="boom") for _ in range(MAX_ATTEMPTS)])

    with pytest.raises(GitHubUnavailable):
        GitHub(session=session, sleep=lambda _: None).raw_file(
            "a/b", "0" * 40, "AGENTS.md"
        )


def test_repo_raises_on_forbidden_first_response():
    # A 403 with no rate-limit headers is not retried by _get; it must still
    # surface as GitHubUnavailable instead of falling through to response.json().
    session = FakeSession([FakeResponse(403, {"message": "Forbidden"})])

    with pytest.raises(GitHubUnavailable):
        GitHub(session=session).repo("payloadcms/payload")


def test_repo_raises_when_head_commit_fails():
    session = FakeSession(
        [FakeResponse(200, load("repo_payload.json")), FakeResponse(422, text="no such ref")]
    )

    with pytest.raises(GitHubUnavailable):
        GitHub(session=session).repo("payloadcms/payload")


def test_server_error_is_retried_then_succeeds():
    session = FakeSession(
        [
            FakeResponse(502, text="bad gateway"),
            FakeResponse(200, load("repo_payload.json")),
            HEAD,
        ]
    )

    meta = GitHub(session=session, sleep=lambda _: None).repo("payloadcms/payload")

    assert meta.full_name == "payloadcms/payload"
    assert len(session.urls) == 3


def test_exhausted_rate_limit_waits_for_the_reset(monkeypatch):
    waited = []
    session = FakeSession(
        [
            FakeResponse(
                403,
                {"message": "rate limit"},
                headers={"x-ratelimit-remaining": "0", "x-ratelimit-reset": "1000"},
            ),
            FakeResponse(200, load("repo_payload.json")),
            HEAD,
        ]
    )
    monkeypatch.setattr("merge_odds.github.time.time", lambda: 940.0)

    GitHub(session=session, sleep=waited.append).repo("payloadcms/payload")

    assert waited and 55 <= waited[0] <= 70


def test_exhausted_rate_limit_never_sleeps_on_the_final_attempt():
    waited = []
    session = FakeSession(
        [
            FakeResponse(
                403,
                {"message": "rate limit"},
                headers={"x-ratelimit-remaining": "0", "x-ratelimit-reset": "1000"},
            )
            for _ in range(MAX_ATTEMPTS)
        ]
    )

    with pytest.raises(GitHubUnavailable):
        GitHub(session=session, sleep=waited.append).raw_file(
            "a/b", "0" * 40, "AGENTS.md"
        )

    assert len(waited) == MAX_ATTEMPTS - 1


def test_secondary_rate_limit_retries_after_retry_after_header():
    waited = []
    session = FakeSession(
        [
            FakeResponse(
                403,
                {"message": "secondary rate limit"},
                headers={"x-ratelimit-remaining": "50", "Retry-After": "3"},
            ),
            FakeResponse(200, load("repo_payload.json")),
            HEAD,
        ]
    )

    meta = GitHub(session=session, sleep=waited.append).repo("payloadcms/payload")

    assert meta.full_name == "payloadcms/payload"
    assert waited == [3.0]
