#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

printf "Checking shell scripts...\n"
find "${ROOT_DIR}/scripts" -type f -name "*.sh" -print0 | xargs -0 bash -n

printf "Checking Python syntax...\n"
python -m compileall "${ROOT_DIR}/src/app/lib/packages" > /dev/null
