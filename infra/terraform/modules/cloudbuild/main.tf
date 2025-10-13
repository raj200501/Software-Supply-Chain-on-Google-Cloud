resource "google_cloudbuild_trigger" "main" {
  project = var.project_id
  name    = "slsa-reference-build"
  filename = "ci/cloudbuild/build-all.yaml"

  github {
    owner = var.github_owner
    name  = var.github_repo
    push {
      branch = "^main$"
    }
  }

  substitutions = {
    _REGION              = var.region
    _ENV                 = "prod"
    _ARTIFACT_REGISTRY   = var.artifact_registry_repo
    _ATTESTATION_BUCKET  = var.attestation_bucket
    _GUAC_BUCKET_PREFIX  = var.guac_bucket_prefix
    _KMS_KEY             = var.kms_key_name
  }
}

resource "google_project_iam_member" "cloudbuild_storage" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${var.cloud_build_sa}"
}

resource "google_project_iam_member" "cloudbuild_artifact" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${var.cloud_build_sa}"
}

output "trigger_id" {
  value = google_cloudbuild_trigger.main.id
}
