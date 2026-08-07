import json
from pathlib import Path

import pytest

from render_module import render_table, splice  # see conftest note in Step 4

FIXTURES = Path(__file__).parent / "fixtures"


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_policy_columns_come_before_statistics():
    header = render_table([load("entry_valid.json")]).splitlines()[0]

    assert header.index("External PRs") < header.index("Casual acceptance")
    assert header.index("AI PR text") < header.index("Median")
    assert header.index("AI PR text") < header.index("Window")


def test_window_column_sits_between_p90_and_measured():
    header = render_table([load("entry_valid.json")]).splitlines()[0]

    assert header.index("p90") < header.index("Window") < header.index("Measured")


def test_window_column_shows_the_day_count():
    row = next(
        line
        for line in render_table([load("entry_valid.json")]).splitlines()
        if "payloadcms/payload" in line
    )

    assert "34.0 d" in row


def test_window_column_shows_a_dash_when_absent():
    archived = dict(load("entry_valid.json"), archived=True)
    del archived["merge_stats"]

    row = next(
        line
        for line in render_table([archived]).splitlines()
        if "payloadcms/payload" in line
    )

    assert "| — |" in row


def test_rows_are_sorted_by_name_not_by_any_score():
    table = render_table([load("entry_valid.json"), load("entry_restricted.json")])
    rows = [line for line in table.splitlines() if line.startswith("| [")]

    assert "aaa/restricted" in rows[0]
    assert "payloadcms/payload" in rows[1]


def test_insufficient_sample_shows_a_dash_not_a_number():
    table = render_table([load("entry_restricted.json")])
    header_cells = table.splitlines()[0].split(" | ")
    row = next(
        line
        for line in table.splitlines()
        if "aaa/restricted" in line
    )
    cells = row.split(" | ")

    assert "|  |" in row or "| — |" in row
    stat_columns = ("Casual acceptance", "Median", "p90")
    for column in stat_columns:
        assert cells[header_cells.index(column)] == "—"


def test_splice_replaces_only_between_the_markers():
    readme = "intro\n<!-- merge-odds:table:start -->\nold\n<!-- merge-odds:table:end -->\noutro\n"

    result = splice(readme, "NEW")

    assert "old" not in result
    assert result.startswith("intro")
    assert result.endswith("outro\n")
    assert "NEW" in result


def test_splice_round_trips_a_well_formed_readme_byte_for_byte_outside_the_markers():
    readme = "intro\n<!-- merge-odds:table:start -->\nold\n<!-- merge-odds:table:end -->\noutro\n"

    result = splice(readme, "NEW")

    before, _, rest = readme.partition("<!-- merge-odds:table:start -->")
    _, _, after = rest.partition("<!-- merge-odds:table:end -->")
    assert result.startswith(before)
    assert result.endswith(after)


def test_splice_raises_when_the_end_marker_is_missing():
    readme = "intro\n<!-- merge-odds:table:start -->\nold content\nno end marker here\noutro tail\n"

    with pytest.raises(ValueError):
        splice(readme, "NEW")


def test_splice_raises_when_the_start_marker_is_missing():
    readme = "intro\nold content\n<!-- merge-odds:table:end -->\noutro tail\n"

    with pytest.raises(ValueError):
        splice(readme, "NEW")


def test_splice_raises_when_the_markers_are_in_the_wrong_order():
    readme = "intro\n<!-- merge-odds:table:end -->\nold\n<!-- merge-odds:table:start -->\noutro\n"

    with pytest.raises(ValueError):
        splice(readme, "NEW")


def test_splice_raises_when_the_start_marker_appears_twice():
    readme = (
        "intro\n<!-- merge-odds:table:start -->\nold\n<!-- merge-odds:table:start -->\n"
        "<!-- merge-odds:table:end -->\noutro\n"
    )

    with pytest.raises(ValueError):
        splice(readme, "NEW")


def test_splice_raises_when_the_end_marker_appears_twice():
    readme = (
        "intro\n<!-- merge-odds:table:start -->\nold\n<!-- merge-odds:table:end -->\n"
        "<!-- merge-odds:table:end -->\noutro\n"
    )

    with pytest.raises(ValueError):
        splice(readme, "NEW")
