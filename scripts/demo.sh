#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${ROOT_DIR}/src/app/lib/packages:${PYTHONPATH:-}"

printf "Running recruiter demo...\n"
if python -m supply_chain_demo.demo; then
  printf "DEMO PASS\n"
else
  printf "DEMO FAIL\n"
  exit 1
fi
