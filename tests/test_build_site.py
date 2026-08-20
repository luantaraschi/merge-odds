import json
from pathlib import Path

from build_site_module import build, dataset_row, public_entry

FIXTURES = Path(__file__).parent / "fixtures"


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_public_site_data_keeps_sources_but_drops_quotes():
    entry = public_entry(load("entry_valid.json"))

    evidence = entry["evidence"]["ai_assisted_code"]
    assert evidence["source"] == "CONTRIBUTING.md"
    assert evidence["url"].startswith("https://github.com/")
    assert "quote" not in evidence


def test_dataset_row_uses_explicit_labels_for_missing_values():
    entry = public_entry(load("entry_restricted.json"))

    row = dataset_row(entry)

    assert "not available" in row
    assert "data-label=\"Casual acceptance\"" in row


def test_build_includes_no_script_rows_and_machine_readable_data():
    page, data = build([load("entry_valid.json")])
    records = json.loads(data)

    assert "payloadcms/payload" in page
    assert '<option value="payloadcms/payload">' in page
    assert records[0]["repo"] == "payloadcms/payload"
    assert "quote" not in data
