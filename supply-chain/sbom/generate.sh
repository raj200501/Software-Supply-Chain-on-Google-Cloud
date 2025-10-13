#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <image> <output-dir>" >&2
  exit 1
fi

IMAGE="$1"
OUT="$2"
mkdir -p "${OUT}"

syft "${IMAGE}" -o cyclonedx-json >"${OUT}/cyclonedx.json"
syft "${IMAGE}" -o spdx-json >"${OUT}/spdx.json"

echo "generated SBOMs for ${IMAGE} in ${OUT}"
