from pathlib import Path

import typer
import yaml

from ru_fin_ai_helper.event_minimum_set_suggester import suggest_minimum_events
from ru_fin_ai_helper.product_profile import ProductProfile


def _load_product_profile(path: Path) -> ProductProfile:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return ProductProfile(
        product_type=data["product_type"],
        channels=data.get("channels", []),
        geography=data.get("geography", "RU"),
        features=data.get("features", []),
        description=data.get("description"),
    )


def suggest_events(product: Path, out: Path) -> None:
    profile = _load_product_profile(product)
    events = sorted(suggest_minimum_events(profile))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump({"events": events}, allow_unicode=True), encoding="utf-8")
    typer.echo(f"Suggested {len(events)} events into {out}")
