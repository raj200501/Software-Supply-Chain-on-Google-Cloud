# SBOM Generation and GUAC Ingestion

This document covers how the repository produces Software Bills of Materials (SBOMs) and ingests them into GUAC (Graph for Understanding Artifact Composition) for downstream security analysis.

## SBOM production

SBOMs are generated during the Cloud Build pipeline via the `./scripts/generate-sbom.sh` helper. The script runs Syft in both CycloneDX JSON and SPDX JSON modes against each produced container image. Artifacts are uploaded to:

- `gs://${_ATTESTATION_BUCKET}/sbom/${SERVICE}/${TAG}/cyclonedx.json`
- `gs://${_ATTESTATION_BUCKET}/sbom/${SERVICE}/${TAG}/spdx.json`

The script also writes a manifest file that lists the generated SBOMs, their digests, and upload timestamps. This manifest is used by GUAC to discover new documents.

Locally you can generate SBOMs with:

```bash
./scripts/generate-sbom.sh \
  --image localhost:5001/gateway:dev \
  --output-dir supply-chain/sbom/out
```

## GUAC deployment

The GUAC stack is provisioned in Kubernetes via `infra/helm/umbrella`. The umbrella chart deploys:

- `guac-graph`: the GraphQL API and data store
- `guac-collect`: collectors that monitor the SBOM bucket and in-toto attestations
- `guac-ingest`: HTTP ingestion endpoint used by the build pipeline

The `infra/k8s/base/guac/` manifests provide a Kustomize alternative for environments where Helm is not available.

The OTEL Collector is configured to export traces to GUAC so that ingestion latency can be monitored.

## Feeding GUAC

During Cloud Build the `publish-guac.sh` script copies generated SBOM and attestation files to the bucket path watched by GUAC. The `GUAC_BUCKET_PREFIX` substitution allows isolating environments.

For manual ingestion:

```bash
./scripts/publish-guac.sh \
  --bucket ${ATTESTATION_BUCKET} \
  --prefix env/dev \
  --path supply-chain/sbom/out
```

## Querying GUAC

Once GUAC is running, port-forward the GraphQL endpoint:

```bash
kubectl port-forward svc/guac-graph 8088:8080 -n supply-chain
```

Example queries:

```graphql
query PackagesForService {
  artifacts(where: {name: {equals: "gateway"}}) {
    name
    sboms {
      digest
      createdAt
      documentType
    }
  }
}
```

```graphql
query VulnerableDependencies {
  packages(where: {licenses: {some: {name: {contains: "GPL"}}}}) {
    name
    version
    dependentArtifacts {
      name
    }
  }
}
```

## Alerting on issues

The OTEL Collector exports Prometheus metrics tracking GUAC ingestion status. The `docs/06-observability.md` guide explains how to configure alerting when ingestion falls behind or documents fail verification.
