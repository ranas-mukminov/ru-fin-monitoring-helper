#!/usr/bin/env bash
set -euo pipefail

echo "[security] Running pip-audit"
if command -v pip-audit >/dev/null 2>&1; then
  pip-audit || true
else
  echo "pip-audit not installed, skipping"
fi

echo "[security] Running bandit"
if command -v bandit >/dev/null 2>&1; then
  bandit -r ai sanctions cli || true
else
  echo "bandit not installed, skipping"
fi
