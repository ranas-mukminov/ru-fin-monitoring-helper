from pathlib import Path
from typing import Iterable

import typer
import yaml

ALLOWED_CATEGORIES = {"auth", "transaction", "kyc", "aml", "ops", "sanctions"}
REQUIRED_KEYS = ("event_name", "description_ru", "category", "use_cases", "fields")
MANDATORY_FIELDS = {"event_type", "ts"}


def _load_schema(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_schema_file(path: Path) -> Iterable[str]:
    errors = []
    if not path.exists():
        return [f"{path} does not exist"]
    data = _load_schema(path)
    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(f"{path.name}: missing {key}")
    category = data.get("category")
    if category and category not in ALLOWED_CATEGORIES:
        errors.append(f"{path.name}: unsupported category {category}")
    fields = data.get("fields") or []
    if not fields:
        errors.append(f"{path.name}: fields must be non-empty list")
    else:
        field_names = {f.get("name") for f in fields if isinstance(f, dict)}
        if not MANDATORY_FIELDS.issubset(field_names):
            errors.append(f"{path.name}: mandatory fields {MANDATORY_FIELDS} missing")
    return errors


def run_validation(file: Path) -> None:
    errors = list(validate_schema_file(file))
    if errors:
        for err in errors:
            typer.echo(err, err=True)
        raise typer.Exit(code=1)
    typer.echo(f"{file} is valid")
