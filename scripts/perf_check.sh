#!/usr/bin/env bash
set -euo pipefail

echo "[perf] Generating synthetic dataset..."
tmpfile=$(mktemp)
python - <<'PY'
import json, random, sys
for i in range(1000):
    doc = {
        "event_type": "transaction_core",
        "ts": "2024-01-01T00:00:00Z",
        "transaction_id": f"txn-{i}",
        "user_id": f"u{i%100}",
        "amount": random.random() * 1000,
        "currency": "RUB",
    }
    sys.stdout.write(json.dumps(doc) + "\n")
PY
echo "[perf] Synthetic dataset ready (1000 lines). Expand as needed for baseline measurements."
