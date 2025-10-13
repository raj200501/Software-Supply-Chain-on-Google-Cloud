# OPA Gatekeeper Policies

OPA Gatekeeper enforces cluster admission policies before workloads are scheduled. This repository ships with templates and constraints ensuring workloads comply with supply chain requirements.

## Deployed policies

The Kustomize overlays (`infra/k8s/overlays/*/gatekeeper`) and Helm chart configure the following `ConstraintTemplate`s:

- **K8sAllowedRegistry**: Limits images to approved Artifact Registry repositories.
- **K8sRequiredProvenance**: Requires cosign and in-toto annotations referencing SLSA provenance documents.
- **K8sRequiredLabels**: Enforces ownership labels (`app.kubernetes.io/owner`).
- **K8sResourceLimits**: Rejects pods without CPU/memory requests and limits.
- **K8sDisallowLatestTag**: Prevents usage of the `:latest` tag.

Each template is backed by Rego stored in `infra/k8s/policies/templates/`.

## Local testing

Use the `scripts/test-gatekeeper.sh` helper to evaluate manifests before applying:

```bash
./scripts/test-gatekeeper.sh infra/k8s/base gateway-deployment.yaml
```

The script renders the manifests, applies them to a throwaway kind cluster, and reports violations.

## Extending policies

1. Create a new template under `infra/k8s/policies/templates/<name>.yaml` with the Rego logic.
2. Add a constraint in `infra/k8s/policies/constraints/<name>.yaml` referencing the template.
3. Reference the constraint in the appropriate Kustomize overlay (`overlays/dev/kustomization.yaml`).
4. Re-run `./scripts/test-gatekeeper.sh`.

## Continuous validation

Binary Authorization continuous validation runs alongside Gatekeeper to monitor Artifact Registry for unverified images. Together they provide defense in depth: Gatekeeper catches policy violations at admission time, while Binary Authorization validates provenance and signatures as part of image promotion.
