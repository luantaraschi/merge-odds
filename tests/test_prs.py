from datetime import datetime, timedelta, timezone

from merge_odds.prs import MIN_HUMAN_SAMPLE, PullRequest, is_bot, merge_stats

BASE = datetime(2026, 6, 1, tzinfo=timezone.utc)


def pr(author, *, bot=False, opened_day=0, closed_day=1, merged=True):
    created = BASE + timedelta(days=opened_day)
    closed = BASE + timedelta(days=closed_day)
    return PullRequest(
        author=author,
        is_bot=bot,
        created_at=created,
        closed_at=closed,
        merged_at=closed if merged else None,
    )


def test_bot_detection_covers_suffix_type_and_denylist():
    assert is_bot("dependabot[bot]", "User")
    assert is_bot("someone", "Bot")
    assert is_bot("renovate", "User")
    assert not is_bot("luantaraschi", "User")


def test_bots_are_excluded_before_any_statistic():
    """Dependabot merges in minutes and drags every median to zero."""
    bots = [
        pr(f"dependabot[bot]", bot=True, opened_day=d, closed_day=d)
        for d in range(30)
    ]
    humans = [
        pr(f"person{i}", opened_day=0, closed_day=10, merged=True)
        for i in range(MIN_HUMAN_SAMPLE)
    ]

    result = merge_stats(bots + humans)

    assert result["merge_stats"]["sample_size"] == MIN_HUMAN_SAMPLE
    assert result["merge_stats"]["median_days_to_merge"] == 10.0
    assert result["merge_stats"]["bots_excluded"] is True


def test_high_traffic_insider_does_not_inflate_acceptance():
    """A paid contributor shows up as CONTRIBUTOR; only appearance count filters them."""
    insider = [pr("staff", opened_day=0, closed_day=1, merged=True) for _ in range(40)]
    casual = [
        pr(f"outsider{i}", opened_day=0, closed_day=5, merged=(i == 0))
        for i in range(20)
    ]

    result = merge_stats(insider + casual)

    assert result["merge_stats"]["casual_author_acceptance"] == 0.05
    assert result["merge_stats"]["distinct_casual_authors"] == 1


def test_window_days_spans_the_whole_sample():
    sample = [
        pr(f"person{i}", opened_day=0, closed_day=i, merged=True)
        for i in range(MIN_HUMAN_SAMPLE)
    ]

    result = merge_stats(sample)

    assert result["merge_stats"]["window_days"] == float(MIN_HUMAN_SAMPLE - 1)


def test_small_sample_reports_insufficient_and_omits_percentages():
    sample = [pr(f"person{i}", closed_day=i) for i in range(5)]

    result = merge_stats(sample)

    assert result["insufficient_sample"] is True
    assert result["merge_stats"] == {
        "sample_size": 5,
        "window_days": 4.0,
        "bots_excluded": True,
    }


def test_p90_interpolates_between_ordered_values():
    sample = [
        pr(f"person{i}", opened_day=0, closed_day=i + 1, merged=True)
        for i in range(MIN_HUMAN_SAMPLE)
    ]

    result = merge_stats(sample)

    assert result["merge_stats"]["p90_days_to_merge"] == 18.1


def test_deleted_account_is_dropped():
    sample = [pr("", closed_day=2) for _ in range(3)] + [
        pr(f"person{i}", closed_day=2) for i in range(MIN_HUMAN_SAMPLE)
    ]

    result = merge_stats(sample)

    assert result["merge_stats"]["sample_size"] == MIN_HUMAN_SAMPLE
