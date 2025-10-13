# Supply Chain Assets

This directory collects helper scripts, policies, and sample outputs for the secure supply chain pipeline.

- `cosign/`: Cosign policy configuration and verification helpers.
- `slsa/`: Example SLSA provenance predicate and verifier instructions.
- `intoto/`: in-toto layout describing build, test, scan, and sign steps.
- `sbom/`: Syft configuration, sample SBOMs, and ingestion manifest templates.

These assets are consumed by Cloud Build (`ci/cloudbuild/build-all.yaml`) and by pre-deployment checks (`scripts/verify-attestations.sh`).
