from pathlib import Path

import yaml
from typer.testing import CliRunner

from cli.main import app


def test_suggest_events_command(tmp_path):
    runner = CliRunner()
    product_path = Path(__file__).resolve().parents[2] / "examples" / "products" / "simple_psp_ru.yaml"
    output = tmp_path / "events.yaml"
    result = runner.invoke(
        app,
        [
            "suggest-events",
            "--product",
            str(product_path),
            "--out",
            str(output),
        ],
    )
    assert result.exit_code == 0, result.output
    assert output.exists()
    data = yaml.safe_load(output.read_text())
    assert "events" in data
    assert "transaction_core" in data["events"]
