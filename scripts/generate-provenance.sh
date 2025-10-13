#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 4 ]]; then
  echo "usage: $0 <image> <bucket> <prefix> <kms-key>" >&2
  exit 1
fi

IMAGE="$1"
BUCKET="$2"
PREFIX="$3"
KMS_KEY="$4"

PROVENANCE=$(mktemp)
cosign attest --predicate-type slsaprovenance --predicate supply-chain/slsa/provenance.json \
  --key "gcpkms://${KMS_KEY}" "${IMAGE}" --yes --output-file "${PROVENANCE}"

gsutil cp "${PROVENANCE}" "gs://${BUCKET}/${PREFIX}/provenance.json"
rm -f "${PROVENANCE}"
echo "uploaded provenance to gs://${BUCKET}/${PREFIX}/provenance.json"
