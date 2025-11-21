from pathlib import Path

import pytest
import yaml


SCHEMA_DIR = Path(__file__).resolve().parents[2] / "schemas" / "events"
ALLOWED_CATEGORIES = {"auth", "transaction", "kyc", "aml", "ops", "sanctions"}
MANDATORY_FIELDS = {"event_type", "ts"}


def _load_schema(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_schema_directory_exists():
    assert SCHEMA_DIR.exists(), "schemas/events directory must exist"


def test_schema_files_present():
    files = list(SCHEMA_DIR.glob("*.yaml"))
    assert files, "at least one event schema must be defined"


@pytest.mark.parametrize("schema_path", sorted(SCHEMA_DIR.glob("*.yaml")))
def test_schema_has_required_structure(schema_path: Path):
    data = _load_schema(schema_path)
    for key in ("event_name", "description_ru", "category", "use_cases", "fields"):
        assert key in data, f"{schema_path.name} missing {key}"
    assert data["category"] in ALLOWED_CATEGORIES
    assert isinstance(data["use_cases"], list) and data["use_cases"], "use_cases must be non-empty list"
    fields = data["fields"]
    assert isinstance(fields, list) and fields, f"{schema_path.name} must define fields"
    field_names = {f.get("name") for f in fields}
    assert None not in field_names, "every field must have a name"
    for field in fields:
        assert "description" in field, f"{schema_path.name} has a field without description"
    assert MANDATORY_FIELDS.issubset(field_names), f"{schema_path.name} missing mandatory fields"
