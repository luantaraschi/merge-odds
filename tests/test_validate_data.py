import json
import sys
from pathlib import Path

from validate_module import GitHubUnavailable, pairing_errors, quote_errors, schema_errors

FIXTURES = Path(__file__).parent / "fixtures"


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_valid_fixture_has_no_schema_error():
    assert schema_errors(load("entry_valid.json")) == []


def test_review_field_is_reported_clearly():
    # build_entry() emits _review as an object with candidates/unmatched_claims/
    # files_read, not a bare list -- but any shape must be rejected, since the
    # root schema forbids the key outright.
    entry = dict(
        load("entry_valid.json"),
        _review={
            "candidates": [],
            "unmatched_claims": ["ai_assisted_code"],
            "files_read": [],
        },
    )

    problems = schema_errors(entry)

    assert problems and any("_review" in problem for problem in problems)


def test_non_default_stance_without_evidence_is_rejected():
    entry = load("entry_valid.json")
    entry["policy"]["evidence"] = []

    problems = pairing_errors(entry)

    assert any("ai_assisted_code" in problem for problem in problems)


def test_default_stance_needs_no_evidence():
    entry = load("entry_valid.json")
    entry["policy"]["ai_assisted_code"] = "not_stated"
    entry["policy"]["evidence"] = []

    assert pairing_errors(entry) == []


def test_quote_must_appear_verbatim_in_the_pinned_file():
    entry = load("entry_valid.json")

    def fetch(repo, sha, path):
        return "intro\nClaude Code is supported.\noutro\n"

    assert quote_errors(entry, fetch) == []


def test_rewritten_quote_is_caught():
    entry = load("entry_valid.json")

    def fetch(repo, sha, path):
        return "intro\nClaude Code works well here.\noutro\n"

    problems = quote_errors(entry, fetch)

    assert problems and "not found verbatim" in problems[0]


def test_missing_file_is_caught():
    entry = load("entry_valid.json")

    assert quote_errors(entry, lambda repo, sha, path: None)


def test_main_reports_a_clear_error_and_nonzero_exit_when_github_is_unavailable(
    tmp_path, monkeypatch, capsys
):
    import validate_module

    entry_path = tmp_path / "payloadcms__payload.json"
    entry_path.write_text(json.dumps(load("entry_valid.json")), encoding="utf-8")

    class FlakyGitHub:
        def __init__(self, *args, **kwargs):
            pass

        def raw_file(self, repo, sha, path):
            raise GitHubUnavailable(f"could not fetch {path} for {repo}@{sha}: status 503")

    monkeypatch.setattr(validate_module, "GitHub", FlakyGitHub)
    monkeypatch.setattr(sys, "argv", ["validate_data.py", str(entry_path)])

    exit_code = validate_module.main()

    captured = capsys.readouterr()
    assert exit_code != 0
    assert "payloadcms/payload" in captured.err
    assert "503" in captured.err
