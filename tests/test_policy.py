from merge_odds.policy import CANDIDATE_FILES, scan


def test_finds_a_restriction_hidden_in_an_html_comment():
    """documenso buried this inside PULL_REQUEST_TEMPLATE.md and it cost a fork."""
    files = {
        ".github/PULL_REQUEST_TEMPLATE.md": (
            "<!--\n"
            "We are no longer accepting external pull requests.\n"
            "Open an issue instead.\n"
            "-->\n"
            "## Description\n"
        )
    }

    found = scan(files)

    assert any(candidate.claim == "accepts_external_prs" for candidate in found)


def test_quote_is_verbatim_and_carries_line_numbers():
    body = "line one\n\nWe do not accept pull requests from outside.\n\nline five\n"
    files = {"CONTRIBUTING.md": body}

    candidate = next(c for c in scan(files) if c.claim == "accepts_external_prs")

    assert candidate.quote in body
    assert candidate.source == "CONTRIBUTING.md"
    assert candidate.line_start == 3
    assert candidate.line_end == 3


def test_finds_an_issue_first_requirement():
    files = {"CONTRIBUTING.md": "Ask before you start. Open an issue first.\n"}

    assert any(c.claim == "requires_issue_first" for c in scan(files))


def test_separates_ai_code_from_ai_written_text():
    files = {
        "ai_policy.md": (
            "We require a human in the loop at all times.\n"
            "\n"
            "Do not copy-paste or use entirely AI-generated text for issue "
            "descriptions, pull requests, comments, or replies.\n"
        )
    }

    claims = {candidate.claim for candidate in scan(files)}

    assert "ai_assisted_code" in claims
    assert "ai_authored_pr_text" in claims


def test_quote_is_capped():
    files = {"CONTRIBUTING.md": "x " * 2000 + "\nAI agents are welcome.\n"}

    for candidate in scan(files):
        assert len(candidate.quote) <= 600


def test_clean_project_yields_nothing():
    files = {"CONTRIBUTING.md": "Run the tests with pytest. Open a pull request.\n"}

    assert scan(files) == []


def test_candidate_files_cover_the_known_hiding_places():
    for path in ("ai_policy.md", "AGENTS.md", ".github/PULL_REQUEST_TEMPLATE.md"):
        assert path in CANDIDATE_FILES
