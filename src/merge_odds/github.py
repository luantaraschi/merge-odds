"""The only module that talks to the network."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from datetime import datetime

import requests

from .prs import PullRequest, is_bot

API = "https://api.github.com"
RAW = "https://raw.githubusercontent.com"
MAX_ATTEMPTS = 4
RATE_LIMIT_CEILING_SECONDS = 900


class RepoNotFound(Exception):
    pass


@dataclass(frozen=True)
class RepoMeta:
    full_name: str
    archived: bool
    default_branch: str
    head_sha: str


def _moment(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


class GitHub:
    def __init__(self, token=None, session=None, sleep=time.sleep):
        self._token = token or os.environ.get("GITHUB_TOKEN")
        self._session = session or requests.Session()
        self._sleep = sleep

    def _headers(self):
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "merge-odds"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    def _get(self, url):
        for attempt in range(MAX_ATTEMPTS):
            response = self._session.get(url, headers=self._headers(), timeout=30)

            if response.status_code in (403, 429):
                remaining = response.headers.get("x-ratelimit-remaining")
                reset = response.headers.get("x-ratelimit-reset")
                if remaining == "0" and reset:
                    wait = min(float(reset) - time.time() + 5, RATE_LIMIT_CEILING_SECONDS)
                    self._sleep(max(wait, 0))
                    continue

            if response.status_code >= 500 and attempt < MAX_ATTEMPTS - 1:
                self._sleep(2**attempt)
                continue

            return response

        return response

    def repo(self, name: str) -> RepoMeta:
        response = self._get(f"{API}/repos/{name}")
        if response.status_code == 404:
            raise RepoNotFound(name)
        response_body = response.json()
        full_name = response_body["full_name"]

        head = self._get(
            f"{API}/repos/{full_name}/commits/{response_body['default_branch']}"
        )
        return RepoMeta(
            full_name=full_name,
            archived=bool(response_body.get("archived")),
            default_branch=response_body["default_branch"],
            head_sha=head.json()["sha"] if head.status_code == 200 else "",
        )

    def closed_pulls(self, name: str, limit: int = 100) -> list[PullRequest]:
        url = (
            f"{API}/repos/{name}/pulls"
            f"?state=closed&sort=updated&direction=desc&per_page={limit}"
        )
        response = self._get(url)
        if response.status_code == 404:
            raise RepoNotFound(name)

        pulls = []
        for item in response.json():
            user = item.get("user") or {}
            login = user.get("login") or ""
            closed_at = _moment(item.get("closed_at"))
            if closed_at is None:
                continue
            pulls.append(
                PullRequest(
                    author=login,
                    is_bot=is_bot(login, user.get("type", "User")),
                    created_at=_moment(item["created_at"]),
                    closed_at=closed_at,
                    merged_at=_moment(item.get("merged_at")),
                )
            )
        return pulls

    def raw_file(self, name: str, sha: str, path: str) -> str | None:
        response = self._get(f"{RAW}/{name}/{sha}/{path}")
        if response.status_code != 200:
            return None
        return response.text.replace("\r\n", "\n")
