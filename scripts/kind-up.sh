#!/usr/bin/env bash
set -euo pipefail

KIND_CLUSTER_NAME="slsa-ref"
REGISTRY_NAME="kind-registry"
REGISTRY_PORT="5001"

if ! command -v kind >/dev/null; then
  echo "kind is required" >&2
  exit 1
fi

if ! docker ps --format '{{.Names}}' | grep -q "^${REGISTRY_NAME}$"; then
  docker run -d --restart=always -p "127.0.0.1:${REGISTRY_PORT}:5000" --name "${REGISTRY_NAME}" registry:2
fi

kind create cluster --name "${KIND_CLUSTER_NAME}" --config - <<EOF_KCFG
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
containerdConfigPatches:
- |-
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."localhost:${REGISTRY_PORT}"]
    endpoint = ["http://${REGISTRY_NAME}:5000"]
nodes:
  - role: control-plane
    extraPortMappings:
      - containerPort: 30000
        hostPort: 30000
EOF_KCFG

kubectl apply -f infra/k8s/base/namespace.yaml
