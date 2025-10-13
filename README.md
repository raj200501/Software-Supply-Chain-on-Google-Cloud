# slsa-bazel-gke-reference

This repository delivers an end-to-end secure software supply chain on Google Cloud underpinned by Bazel builds, polyglot microservices, and continuous verification. It fulfills the specification captured in `slsa_bazel_gke_reference_codex_prompt.txt` by wiring reproducible builds, SBOM generation, in-toto attestations, Binary Authorization enforcement, GUAC ingestion, and both local and cloud execution paths.

The implementation is intentionally verbose and self-documenting so that a fresh clone can be taken from zero to a fully deployed environment on either a developer workstation (`docker-compose`, `kind`, `skaffold`) or Google Cloud (`terraform`, `cloudbuild`).

## Repository layout

- `apps/web`: React + TypeScript web UI served via Bazel and containerized with multi-stage Docker builds. Unit tests and OpenTelemetry instrumentation are bundled with the code.
- `api/proto`: Protocol Buffer definitions describing the domain. Bazel rules generate language-specific stubs consumed by the services and gateway.
- `api/gateway`: Go-based gRPC-Gateway translating REST calls to gRPC. Includes health/readiness endpoints and OpenTelemetry exporters.
- `services/users`: Go microservice exposing CRUD operations, backed by Postgres, with gRPC, REST, and unit tests.
- `services/orders`: Python FastAPI service orchestrating order lifecycle. Includes async clients, tests, and integration hooks.
- `services/inventory`: Java Spring Boot service managing stock reservations. Includes Flyway migrations and unit tests.
- `services/payments`: Node.js Express service simulating payment capture and producing notification events.
- `services/notifications`: Rust Actix-web service emitting notification events and forwarding to GUAC ingestion.
- `infra/k8s`: Kustomize base and overlays (`dev`, `prod`) for deploying onto Kubernetes, including OTEL Collector, GUAC, and OPA Gatekeeper integration.
- `infra/helm`: Helm umbrella chart and per-service charts mirroring the Kustomize topology.
- `infra/terraform`: Terraform modules for creating Google Cloud infrastructure (GKE, Artifact Registry, Cloud Build, KMS, Binary Authorization, Secret Manager, Workload Identity).
- `supply-chain`: Cosign, SLSA, in-toto, and SBOM helper material plus verification scripts.
- `ci`: Cloud Build pipelines (SLSA L3 provenance, SBOM generation, cosign signing, in-toto links, Binary Authorization promotion) and GitHub Actions workflows for local CI.
- `docs`: Detailed operational and architectural documentation with diagrams, walkthroughs, and troubleshooting guidance.
- `scripts`: Helper automation for local dev, seeding data, verifying attestations, and managing clusters.
- `skaffold.yaml`: Inner-loop developer experience for syncing changes into kind or GKE clusters.
- `Makefile`: One-stop entry point for common flows.

## Getting started

### Prerequisites

- Docker / Docker Compose v2
- Bazelisk (`brew install bazelisk` or download the release binary)
- Terraform >= 1.6
- gcloud CLI (`brew install --cask google-cloud-sdk`)
- Node.js 18+, Go 1.21+, Python 3.11+, Java 17+, Rust toolchain
- Cosign (`go install sigs.k8s.io/release/cosign/cmd/cosign@latest`)
- Syft (`brew install syft` or `go install github.com/anchore/syft/cmd/syft@latest`)

### Quick start (local docker-compose)

```bash
make deps           # install language-specific toolchains and npm/pip deps
make generate       # compile protobufs and install UI dependencies
make compose-up     # launch Postgres, OTEL, services, gateway, and web UI locally
```

Navigate to http://localhost:3000 to exercise the UI. Health endpoints are exposed at `/healthz` and `/readyz` on each service container.

To tear down the stack run `make compose-down`.

### Local Kubernetes workflow (kind + skaffold)

```bash
make kind-up                    # create kind cluster + registry mirror
skaffold dev --profile=dev      # continuous build/deploy with Dockerfile-based images
```

The gateway will become available via the `gateway` service (NodePort 30080). The web UI is served through the `web` service (NodePort 30000).

### Google Cloud deployment

```bash
cd infra/terraform
terraform init
terraform apply -var-file=terraform.tfvars.example
```

Outputs include service account emails, Artifact Registry URIs, and kubeconfig instructions. Once infrastructure is ready trigger the secure Cloud Build pipeline:

```bash
gcloud builds submit --config=ci/cloudbuild/build-all.yaml . \
  --substitutions=_ENV=prod,_REGION=us-central1
```

The pipeline produces SLSA provenance, CycloneDX and SPDX SBOMs, cosign signatures, and in-toto link metadata, all of which are published to Artifact Registry and Binary Authorization.

To deploy into the newly created cluster:

```bash
skaffold run --profile=prod --default-repo="${ARTIFACT_REGISTRY_REPO}"
```

### Testing

```bash
bazel test //...
make test-e2e
```

The `test-e2e` target executes the top-level happy-path scenario across the running stack.

### Documentation

Every operational flow is captured in `docs/`:

- `00-architecture.md`: Application and supply chain architecture diagrams and narratives.
- `01-local-dev.md`: Detailed steps for docker-compose and kind+skaffold workflows.
- `02-gcp-deploy.md`: Terraform, Cloud Build, Binary Authorization, and cleanup instructions.
- `03-slsa-binary-auth.md`: Provenance model, cosign signing, and Binary Authorization policy.
- `04-sbom-and-guac.md`: SBOM generation, publishing, and GUAC queries.
- `05-opa-gatekeeper.md`: Policy enforcement for Kubernetes.
- `06-observability.md`: OpenTelemetry collector and dashboards.
- `07-testing-e2e.md`: Test strategy across unit/integration/e2e and how to extend.
- `08-troubleshooting.md`: Common failure modes and remediations.

### Support scripts

Key helper scripts live under `scripts/`:

- `dev-seed.sh`: Populates the stack with demo data via gateway APIs.
- `verify-attestations.sh`: Validates SLSA, SBOM, and cosign attestations prior to deployment.
- `kind-up.sh` / `kind-down.sh`: Manage the local kind environment and registry mirror.
- `otel-collector-config.yaml`: Centralized collector configuration for local deployments.

## Contributing

1. Fork the repo and create a feature branch.
2. Run `make lint fmt test` to ensure code quality.
3. Open a pull request and attach the generated provenance and SBOM artifacts (see `docs/04-sbom-and-guac.md`).

All contributions must include relevant tests and documentation updates.

## License

Apache License 2.0. See `LICENSE` and `NOTICE` for details.
