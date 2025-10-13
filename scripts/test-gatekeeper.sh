#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <kustomize-dir> <manifest>" >&2
  exit 1
fi

KUSTOMIZE_DIR="$1"
MANIFEST="$2"

kind create cluster --name gatekeeper-test >/dev/null 2>&1 || true
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/v3.13.0/deploy/gatekeeper.yaml

kustomize build "${KUSTOMIZE_DIR}" | kubectl apply -f -

if ! kubectl apply -f "${KUSTOMIZE_DIR}/${MANIFEST}" 2>&1 | tee /tmp/gatekeeper.log; then
  echo "Gatekeeper denied manifest (expected for violations). See /tmp/gatekeeper.log"
fi

kind delete cluster --name gatekeeper-test >/dev/null 2>&1 || true
