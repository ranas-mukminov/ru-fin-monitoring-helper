from pathlib import Path
from typing import Optional, Set

import typer
import yaml

from ru_fin_ai_helper.event_minimum_set_suggester import suggest_minimum_events
from ru_fin_ai_helper.playbook_suggester import generate_playbook
from ru_fin_ai_helper.product_profile import ProductProfile


def _load_profile(path: Path) -> ProductProfile:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return ProductProfile(
        product_type=data["product_type"],
        channels=data.get("channels", []),
        geography=data.get("geography", "RU"),
        features=data.get("features", []),
        description=data.get("description"),
    )


def _load_events(path: Optional[Path]) -> Optional[Set[str]]:
    if not path:
        return None
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return set(data.get("events") or [])


def generate_playbooks(product: Path, events_file: Optional[Path], out: Path, risk_level: str = "medium") -> None:
    profile = _load_profile(product)
    events = _load_events(events_file) or suggest_minimum_events(profile)
    content = generate_playbook(profile, events, risk_level=risk_level)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    typer.echo(f"Wrote playbook to {out}")
