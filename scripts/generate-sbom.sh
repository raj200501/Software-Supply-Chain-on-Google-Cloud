#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "usage: $0 <image> <bucket> <prefix>" >&2
  exit 1
fi

IMAGE="$1"
BUCKET="$2"
PREFIX="$3"
TMP_DIR=$(mktemp -d)

./supply-chain/sbom/generate.sh "${IMAGE}" "${TMP_DIR}"

SAFE_NAME=$(echo "${IMAGE}" | sed 's|[^a-zA-Z0-9._-]|_|g')
LOCAL_DIR="supply-chain/sbom/out/${SAFE_NAME}"
mkdir -p "${LOCAL_DIR}"

for file in cyclonedx.json spdx.json; do
  cp "${TMP_DIR}/${file}" "${LOCAL_DIR}/${file}"
  gsutil cp "${TMP_DIR}/${file}" "gs://${BUCKET}/${PREFIX}/${file}"
  echo "uploaded ${file} to gs://${BUCKET}/${PREFIX}/${file}"
done

rm -rf "${TMP_DIR}"
