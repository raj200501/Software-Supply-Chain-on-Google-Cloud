#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: $0 --image <image> --kms-key <kms-key> --attestor <attestor>
USAGE
}

IMAGE=""
KMS_KEY=""
ATTESTOR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --image)
      IMAGE="$2"
      shift 2
      ;;
    --kms-key)
      KMS_KEY="$2"
      shift 2
      ;;
    --attestor)
      ATTESTOR="$2"
      shift 2
      ;;
    *)
      usage
      exit 1
      ;;
  esac
done

if [[ -z "${IMAGE}" || -z "${KMS_KEY}" || -z "${ATTESTOR}" ]]; then
  usage
  exit 1
fi

echo "Verifying cosign signature for ${IMAGE}"
cosign verify "${IMAGE}" --key "gcpkms://${KMS_KEY}" \
  --certificate-identity-regex "https://cloudbuild.googleapis.com/.*" \
  --certificate-oidc-issuer "https://accounts.google.com"

echo "Verifying SLSA attestation"
cosign verify-attestation "${IMAGE}" --type slsaprovenance --key "gcpkms://${KMS_KEY}" > provenance.json
python supply-chain/slsa/verify.py provenance.json

echo "Checking Binary Authorization attestor"
gcloud container binauthz attestations list \
  --attestor="${ATTESTOR}" \
  --project="$(gcloud config get-value project)" \
  --filter="resourceUri~${IMAGE}"

echo "All checks passed"
