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
    body = "AI-assisted contributions are welcome. " + "x" * 700 + "\n"
    files = {"CONTRIBUTING.md": body}

    candidates = scan(files)

    assert candidates
    for candidate in candidates:
        assert len(candidate.quote) <= 600
    assert any(len(c.quote) == 600 and c.quote in body for c in candidates)


def test_clean_project_yields_nothing():
    files = {"CONTRIBUTING.md": "Run the tests with pytest. Open a pull request.\n"}

    assert scan(files) == []


def test_candidate_files_cover_the_known_hiding_places():
    for path in ("ai_policy.md", "AGENTS.md", ".github/PULL_REQUEST_TEMPLATE.md"):
        assert path in CANDIDATE_FILES


def test_catches_a_plain_not_accepting_pull_requests_phrasing():
    """The original pattern demanded external/outside/new right after "accepting";
    "we are not accepting pull requests" has none of those and slipped through."""
    files = {"CONTRIBUTING.md": "We are not accepting pull requests at this time.\n"}

    assert any(c.claim == "accepts_external_prs" for c in scan(files))


def test_catches_file_an_issue_before_submitting_a_pr():
    files = {"CONTRIBUTING.md": "Please file an issue before submitting a PR.\n"}

    assert any(c.claim == "requires_issue_first" for c in scan(files))


def test_catches_the_hono_ai_usage_policy_sentence():
    """hono/docs/CONTRIBUTING.md buries this in an "AI Usage Policy" section.
    Only a bare "AI" appears -- no compound like "AI-assisted" -- and the old
    patterns required a compound, so scan() returned nothing for this file."""
    files = {
        "docs/CONTRIBUTING.md": (
            "To enforce this, and regardless of whether AI was actually used, "
            "a maintainer may close your PR without notice and block your account.\n"
        )
    }

    candidate = next(c for c in scan(files) if c.claim == "ai_assisted_code")

    assert (
        "To enforce this, and regardless of whether AI was actually used, "
        "a maintainer may close your PR without notice and block your account."
        in candidate.quote
    )


def test_catches_ai_generated_comments_not_just_descriptions():
    files = {
        "ai_policy.md": (
            "Please avoid AI-generated comments; all replies must be written "
            "by a human.\n"
        )
    }

    assert any(c.claim == "ai_authored_pr_text" for c in scan(files))


def test_catches_raise_an_issue_before_core_changes():
    """codeceptjs writes its only gate as "raise an issue", under a Core Changes
    heading. Every issue-first pattern demanded open, file or ask, so the claim
    landed in unmatched_claims and that silence read as "no requirement"."""
    files = {
        ".github/CONTRIBUTING.md": (
            "## Core Changes\n"
            "\n"
            "Before applying any Core changes please raise an issue to discuss "
            "that change with core team.\n"
        )
    }

    assert any(c.claim == "requires_issue_first" for c in scan(files))


def test_catches_open_an_issue_to_discuss():
    """wundergraph/cosmo opens CONTRIBUTING.md with this sentence. "open an issue
    first" matched and "open an issue to discuss" did not, and the only difference
    is which word follows the noun."""
    files = {
        "CONTRIBUTING.md": (
            "Before contributing to the WunderGraph Cosmo repository, please open "
            "an issue to discuss the changes you would like to make.\n"
        )
    }

    assert any(c.claim == "requires_issue_first" for c in scan(files))


def test_catches_a_discussion_requirement_written_as_a_markdown_link():
    """supabase has been in the dataset with requires_issue_first true since the
    first release, and the scanner never found the sentence behind it: a human
    read the file. The claim covers a prior issue or discussion, no pattern
    mentioned discussions, and the noun is wrapped in a markdown link."""
    files = {
        "CONTRIBUTING.md": (
            "- If you're submitting a new feature, make sure you have opened a "
            "[Discussion](https://github.com/orgs/supabase/discussions/new/choose) "
            "to discuss the new feature before opening a PR.\n"
        )
    }

    assert any(c.claim == "requires_issue_first" for c in scan(files))


def test_catches_start_by_opening_an_issue_split_by_a_markdown_link():
    """orval states the requirement twice. "make sure you open an issue first"
    matched; the broader one under Prerequisites did not, because a markdown link
    splits the verb from the rest of the sentence."""
    files = {
        "CONTRIBUTING.md": (
            "In order to not waste your time implementing a change that has "
            "already been declined, start by [opening an issue]"
            "(https://github.com/orval-labs/orval/issues/new) describing the "
            "problem you would like to solve.\n"
        )
    }

    assert any(c.claim == "requires_issue_first" for c in scan(files))
