# slsa-bazel-gke-reference

This repository demonstrates a polyglot supply-chain aware microservice platform targeting Google Cloud and local development workflows. The implementation delivered here brings up the full microservice topology called out in `slsa_bazel_gke_reference_codex_prompt.txt` (users, orders, inventory, payments, notifications, and the Go gateway) together with a React web experience, Bazel builds, containerization, and docker-compose orchestration for local validation.

## Repository layout

- `apps/web`: React + TypeScript single page app that consumes the gateway REST API.
- `services/users`: Go gRPC/REST service with request validation and tests.
- `services/orders`: Python FastAPI service packaged with Bazel and Docker.
- `services/inventory`: Java Spring Boot service exposing stock reservation APIs.
- `services/payments`: Node.js service handling capture flows and posting to notifications.
- `services/notifications`: Rust Actix-web service emitting notification events.
- `api/proto`: Protocol Buffer definitions for cross-service communication.
- `api/gateway`: Go gRPC-Gateway translating REST requests into gRPC calls.
- `infra`: Kubernetes manifests and configuration baselines for dev/prod.
- `ci`: Cloud Build and GitHub Actions workflows for builds, tests, and security attestations.
- `supply-chain`: Cosign, SLSA, in-toto, and SBOM helper material.
- `docs`: Operational and architectural documentation.
- `Makefile`: Common developer operations.

## Getting started

### Prerequisites

- Docker
- Bazelisk (`brew install bazelisk` or download from GitHub)
- Node.js 18+
- Go 1.21+
- Python 3.11+

### Quick start

```bash
make deps          # install language-specific toolchains via asdf or local shims
make generate      # run bazel to generate protobufs and install web UI deps
make compose-up    # launch docker-compose stack with Postgres and all services
```

Visit http://localhost:3000 to access the web UI.

### Tests

```bash
bazel test //...
```

### Next steps

- Complete Terraform GCP infrastructure provisioning under `infra/terraform`.
- Add Binary Authorization constraints and GUAC ingestion once Cloud Build is wired up.
- Expand unit/e2e test suites to cover all services.

Refer to the documentation in `docs/` for deeper guidance.
