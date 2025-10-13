# Troubleshooting Guide

This document enumerates common issues encountered when working with the repository and how to resolve them.

## Docker Compose stack fails to start

- Ensure ports 3000, 8080-8085, and 5432 are free.
- Run `docker compose logs -f` to inspect failing services.
- Re-run `make generate` to ensure protobufs and frontend dependencies are up to date.

## Bazel build errors

- Clear the Bazel cache with `bazel clean --expunge` if dependency changes are not picked up.
- Install required toolchains (Go, Python, Java, Node, Rust) using `make deps`.
- Verify you are using Bazelisk (it automatically selects the correct Bazel version).

## Terraform authentication failures

- Run `gcloud auth application-default login`.
- Set the active project: `gcloud config set project <PROJECT_ID>`.
- Ensure the service account running Terraform has `roles/resourcemanager.projectIamAdmin`, `roles/container.admin`, `roles/cloudkms.admin`, `roles/cloudbuild.builds.editor`, and `roles/binaryauthorization.policyEditor`.

## Cloud Build provenance failures

- Confirm that the KMS key specified by `_KMS_KEY` exists and the Cloud Build service account has the `cloudkms.signerVerifier` role.
- Verify that cosign can access the key: `cosign sign --key ${KMS_KEY} --dry-run IMAGE`.
- Inspect Cloud Build logs for errors in `generate-provenance` or `generate-sbom` steps.

## Binary Authorization denials

- Retrieve the denial reason via `gcloud container binauthz verificationalert list`.
- Ensure the image digest matches the signed provenance (rerun `./scripts/verify-attestations.sh`).
- Confirm the Binary Authorization policy includes the attestor reference created by Terraform.

## GUAC ingestion delays

- Check the GUAC collector logs: `kubectl logs deployment/guac-collect -n supply-chain`.
- Validate the bucket prefix in `_GUAC_BUCKET_PREFIX` matches the deployment environment.
- Review OTEL metrics for ingestion lag (`guac_ingest_duration_seconds`).

## kind cluster issues

- `make kind-down` followed by `make kind-up` recreates the cluster.
- Ensure Docker has at least 6 CPUs and 8 GB RAM allocated.
- If image pushes fail, verify the local registry mirror is running (`docker ps | grep kind-registry`).

## Skaffold sync problems

- Run `skaffold delete --profile=dev` to clean up stale resources.
- Check `skaffold.yaml` sync rules for the service you are editing.
- Inspect Bazel build cache and ensure dependencies are properly declared.

## Helm deployment errors

- `helm dependency update infra/helm/umbrella` to refresh subchart references.
- `helm template` to render manifests and check for invalid values.
- Confirm the values file for the environment defines `image.registry`, `image.repository`, and `image.tag`.

## Contact

If you run into an issue not covered here, open an issue with reproduction steps or ask in the internal `#supply-chain-platform` Slack channel.
