import json
from pathlib import Path

import pytest
from validate_module import pairing_errors, schema_errors

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = sorted((ROOT / "data" / "repos").glob("*.json"))


@pytest.mark.parametrize("path", ENTRIES, ids=lambda p: p.stem)
def test_entry_matches_the_schema(path):
    assert schema_errors(json.loads(path.read_text(encoding="utf-8"))) == []


@pytest.mark.parametrize("path", ENTRIES, ids=lambda p: p.stem)
def test_entry_pairs_every_stance_with_a_quote(path):
    assert pairing_errors(json.loads(path.read_text(encoding="utf-8"))) == []


@pytest.mark.parametrize("path", ENTRIES, ids=lambda p: p.stem)
def test_filename_matches_the_repo_field(path):
    entry = json.loads(path.read_text(encoding="utf-8"))
    assert path.name == entry["repo"].replace("/", "__") + ".json"


# The verbatim-quote check is deliberately absent from this file: it needs
# network access to fetch the pinned file from GitHub, so it lives in
# scripts/validate_data.py and is invoked by CI, not by the offline test suite.
