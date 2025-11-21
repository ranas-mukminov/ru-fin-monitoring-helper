#!/usr/bin/env bash
set -euo pipefail

echo "[lint] Running ruff"
if command -v ruff >/dev/null 2>&1; then
  ruff .
else
  echo "ruff not installed, skipping"
fi

echo "[lint] Running mypy"
if command -v mypy >/dev/null 2>&1; then
  mypy ai/src sanctions/ cli/ || true
else
  echo "mypy not installed, skipping"
fi

echo "[lint] Running yamllint"
if command -v yamllint >/dev/null 2>&1; then
  yamllint schemas pipelines examples
else
  echo "yamllint not installed, skipping"
fi
