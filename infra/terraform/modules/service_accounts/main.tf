resource "google_service_account" "cloud_build" {
  account_id   = "cloud-build"
  display_name = "Cloud Build"
}

resource "google_service_account" "workload_identity" {
  account_id   = "workload-identity"
  display_name = "Workload Identity"
}

resource "google_service_account" "binary_authorization" {
  account_id   = "binauthz-enforcer"
  display_name = "Binary Authorization Enforcer"
}

resource "google_iam_workload_identity_pool" "pool" {
  workload_identity_pool_id = "slsa-ref-pool"
  display_name              = "SLSA Reference Workload Identity"
}

resource "google_project_iam_member" "cloud_build_roles" {
  for_each = toset([
    "roles/cloudbuild.builds.editor",
    "roles/artifactregistry.writer",
    "roles/cloudkms.signerVerifier",
    "roles/storage.admin"
  ])
  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.cloud_build.email}"
}

output "cloud_build_sa" {
  value = google_service_account.cloud_build.email
}

output "workload_identity_pool" {
  value = google_iam_workload_identity_pool.pool.name
}

output "workload_identity_sa" {
  value = google_service_account.workload_identity.email
}

output "binary_authorization_sa" {
  value = google_service_account.binary_authorization.email
}
