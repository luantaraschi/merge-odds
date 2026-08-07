import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schema" / "repo.schema.json").read_text(encoding="utf-8"))
VALID = json.loads((ROOT / "tests" / "fixtures" / "entry_valid.json").read_text(encoding="utf-8"))


def errors(entry):
    return list(Draft202012Validator(SCHEMA).iter_errors(entry))


def test_valid_entry_passes():
    assert errors(VALID) == []


def test_review_field_is_rejected():
    entry = dict(VALID, _review=["candidate quote"])
    assert errors(entry), "_review must never reach data/repos/"


def test_policy_claim_without_evidence_is_allowed_only_when_not_stated():
    entry = json.loads(json.dumps(VALID))
    entry["policy"]["evidence"] = []
    assert errors(entry) == []  # schema permits; scripts/validate_data.py enforces the pairing


def test_url_must_pin_a_full_sha():
    entry = json.loads(json.dumps(VALID))
    entry["policy"]["evidence"][0]["url"] = (
        "https://github.com/payloadcms/payload/blob/main/CONTRIBUTING.md#L118"
    )
    assert errors(entry), "branch-pinned URLs rot; only full SHAs are accepted"


def test_stats_require_a_window():
    entry = json.loads(json.dumps(VALID))
    del entry["merge_stats"]["window_days"]
    assert errors(entry), "acceptance without a window is meaningless"


def test_insufficient_sample_forbids_percentages():
    entry = json.loads(json.dumps(VALID))
    entry["insufficient_sample"] = True
    assert errors(entry)

    entry["merge_stats"] = {"sample_size": 8, "window_days": 12.0, "bots_excluded": True}
    assert errors(entry) == []


def test_archived_entry_has_no_stats():
    entry = json.loads(json.dumps(VALID))
    entry["archived"] = True
    assert errors(entry)

    del entry["merge_stats"]
    assert errors(entry) == []
