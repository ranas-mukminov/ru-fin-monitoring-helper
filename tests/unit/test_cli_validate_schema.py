from pathlib import Path

from typer.testing import CliRunner

from cli.main import app


def test_validate_schema_succeeds():
    runner = CliRunner()
    schema_path = Path(__file__).resolve().parents[2] / "schemas" / "events" / "transaction_core.yaml"
    result = runner.invoke(app, ["validate-schema", "--file", str(schema_path)])
    assert result.exit_code == 0, result.output
    assert "valid" in result.output.lower()
