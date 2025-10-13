# GCP Deployment Outline

- Configure a Google Cloud project and enable GKE, Artifact Registry, Cloud Build, and Binary Authorization APIs.
- Use Terraform modules under `infra/terraform` (to be expanded) to provision infrastructure.
- Configure Cloud Build triggers to run Bazel builds and push images to Artifact Registry.
- Deploy workloads to GKE using the manifests in `infra/k8s/overlays/prod`.
