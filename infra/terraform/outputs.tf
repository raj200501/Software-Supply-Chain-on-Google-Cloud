output "cloud_build_service_account" {
  description = "Cloud Build service account email"
  value       = module.service_accounts.cloud_build_sa
}

output "gke_cluster_name" {
  description = "Name of the provisioned GKE cluster"
  value       = module.gke.cluster_name
}

output "gke_location" {
  description = "Location of the GKE cluster"
  value       = module.gke.cluster_location
}

output "artifact_registry_repository" {
  description = "Artifact Registry repository path"
  value       = module.artifact_registry.repository
}

output "binary_authorization_attestor" {
  description = "Binary Authorization attestor name"
  value       = module.binary_authorization.attestor_name
}

output "workload_identity_pool" {
  description = "Workload Identity pool"
  value       = module.service_accounts.workload_identity_pool
}
