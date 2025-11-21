import json
from pathlib import Path
import typer
import yaml

from .event_minimum_set_suggester import suggest_minimum_events
from .playbook_suggester import generate_playbook
from .product_profile import ProductProfile


app = typer.Typer(help="AI helper stubs for ru-fin-monitoring-helper.")


def _load_profile(path: Path) -> ProductProfile:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return ProductProfile(
        product_type=data["product_type"],
        channels=data.get("channels", []),
        geography=data.get("geography", "RU"),
        features=data.get("features", []),
        description=data.get("description"),
    )


@app.command("suggest-events")
def cli_suggest_events(profile: Path):
    prof = _load_profile(profile)
    events = sorted(suggest_minimum_events(prof))
    typer.echo(json.dumps({"events": events}, ensure_ascii=False, indent=2))


@app.command("playbook")
def cli_playbook(profile: Path, risk_level: str = "medium"):
    prof = _load_profile(profile)
    events = suggest_minimum_events(prof)
    typer.echo(generate_playbook(prof, events, risk_level))


if __name__ == "__main__":
    app()
