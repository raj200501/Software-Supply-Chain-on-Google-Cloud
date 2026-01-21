#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${ROOT_DIR}/src/app/lib/packages:${PYTHONPATH:-}"

python - <<'PY'
from supply_chain_demo.doctor import as_text, run_diagnostics
print(as_text(run_diagnostics()))
PY
