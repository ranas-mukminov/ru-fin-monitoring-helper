from pathlib import Path

import typer

from cli.commands.generate_pipeline_stub import generate_pipeline_stub
from cli.commands.generate_playbooks import generate_playbooks
from cli.commands.suggest_events import suggest_events
from cli.commands.validate_schema import run_validation

app = typer.Typer(help="RU Fin Monitoring Helper CLI")


@app.command("validate-schema")
def validate_schema_cli(file: Path):
    """Validate schema YAML file."""
    run_validation(file)


@app.command("generate-pipeline-stub")
def generate_pipeline_stub_cli(schema: Path, target: str = typer.Option("elk"), out: Path = typer.Option(...)):
    generate_pipeline_stub(schema, target, out)


@app.command("suggest-events")
def suggest_events_cli(product: Path, out: Path):
    suggest_events(product, out)


@app.command("generate-playbooks")
def generate_playbooks_cli(
    product: Path,
    events: Path | None = typer.Option(None, help="Optional events yaml"),
    out: Path = typer.Option(...),
    risk_level: str = typer.Option("medium"),
):
    generate_playbooks(product, events, out, risk_level)


if __name__ == "__main__":
    app()
