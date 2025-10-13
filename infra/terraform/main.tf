module "network" {
  source     = "./modules/network"
  project_id = var.project_id
  region     = var.region
}

module "service_accounts" {
  source     = "./modules/service_accounts"
  project_id = var.project_id
}

module "kms" {
  source           = "./modules/kms"
  project_id       = var.project_id
  location         = var.region
  attestor_members = [module.service_accounts.cloud_build_sa]
}

module "artifact_registry" {
  source       = "./modules/artifact_registry"
  project_id   = var.project_id
  location     = var.region
  repository   = var.artifact_registry_repo
  kms_key_name = module.kms.container_key_id
}

module "cloudbuild" {
  source                 = "./modules/cloudbuild"
  project_id             = var.project_id
  region                 = var.region
  cloud_build_sa         = module.service_accounts.cloud_build_sa
  artifact_registry_repo = module.artifact_registry.repository
  kms_key_name           = module.kms.container_key_id
  attestation_bucket     = var.attestation_bucket
  guac_bucket_prefix     = var.guac_bucket_prefix
}

module "gke" {
  source                  = "./modules/gke"
  project_id              = var.project_id
  region                  = var.region
  network                 = module.network.network_self_link
  subnetwork              = module.network.subnetwork_self_link
  release_channel         = var.gke_release_channel
  workload_identity_pool = module.service_accounts.workload_identity_pool
}

module "binary_authorization" {
  source                     = "./modules/binary_authorization"
  project_id                 = var.project_id
  region                     = var.region
  attestor_members           = [module.service_accounts.cloud_build_sa]
  attestation_project        = var.project_id
  artifact_registry_projects = [var.project_id]
  attestor_public_key        = module.kms.attestor_public_key
}

module "monitoring" {
  source       = "./modules/monitoring"
  project_id   = var.project_id
  region       = var.region
  cluster_name = module.gke.cluster_name
  location     = module.gke.cluster_location
}

module "secret_manager" {
  source     = "./modules/secret_manager"
  project_id = var.project_id
  secrets = {
    db-password         = var.db_password
    notifications-token = var.notifications_token
  }
}
