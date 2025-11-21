import json
import typer

from .client import OpenSanctionsClient


app = typer.Typer(help="OpenSanctions helper CLI (offline-friendly demos).")


@app.command("search")
def search(name: str):
    """Perform a simple search by name."""
    client = OpenSanctionsClient()
    result = client.search_name(name)
    typer.echo(json.dumps([e.__dict__ for e in result.results], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    app()
