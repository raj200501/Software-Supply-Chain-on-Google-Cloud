#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${ROOT_DIR}/src/app/lib/packages:${PYTHONPATH:-}"

printf "\n==> Shell lint\n"
"${ROOT_DIR}/scripts/lint.sh"

printf "\n==> Python compile check\n"
python -m compileall "${ROOT_DIR}/src/app/lib/packages"

printf "\n==> Unit and integration tests\n"
LOCAL_GATEWAY=1 python -m pytest "${ROOT_DIR}/tests"

printf "\n==> Demo smoke\n"
"${ROOT_DIR}/scripts/demo.sh"

printf "\nAll checks passed.\n"
