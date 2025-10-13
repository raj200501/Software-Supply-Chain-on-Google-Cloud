resource "google_artifact_registry_repository" "repo" {
  project       = var.project_id
  location      = var.location
  repository_id = var.repository
  description   = "Container images for SLSA reference"
  format        = "DOCKER"
  kms_key_name  = var.kms_key_name
}

output "repository" {
  value = google_artifact_registry_repository.repo.repository
}
