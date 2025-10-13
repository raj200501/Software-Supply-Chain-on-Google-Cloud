#!/usr/bin/env bash
set -euo pipefail

KIND_CLUSTER_NAME="slsa-ref"
REGISTRY_NAME="kind-registry"

kind delete cluster --name "${KIND_CLUSTER_NAME}" || true

docker rm -f "${REGISTRY_NAME}" >/dev/null 2>&1 || true
