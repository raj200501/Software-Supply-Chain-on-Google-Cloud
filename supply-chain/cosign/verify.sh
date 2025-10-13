#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <image> <kms-key>" >&2
  exit 1
fi

IMAGE="$1"
KMS_KEY="$2"

cosign verify "${IMAGE}" \
  --key "gcpkms://${KMS_KEY}" \
  --certificate-identity-regex "https://cloudbuild.googleapis.com/.*" \
  --certificate-oidc-issuer "https://accounts.google.com"

cosign verify-attestation "${IMAGE}" \
  --type slsaprovenance \
  --key "gcpkms://${KMS_KEY}"
