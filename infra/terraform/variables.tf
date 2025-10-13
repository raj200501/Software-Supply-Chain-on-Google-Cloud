variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
}

variable "region" {
  description = "Default region for resources"
  type        = string
  default     = "us-central1"
}

variable "artifact_registry_repo" {
  description = "Name of the Artifact Registry repository"
  type        = string
  default     = "slsa-reference"
}

variable "attestation_bucket" {
  description = "Cloud Storage bucket for SBOMs and attestations"
  type        = string
}

variable "guac_bucket_prefix" {
  description = "Prefix inside the attestation bucket for GUAC ingestion"
  type        = string
  default     = "env/dev"
}

variable "gke_release_channel" {
  description = "GKE release channel"
  type        = string
  default     = "REGULAR"
}

variable "db_password" {
  description = "Initial database password"
  type        = string
  sensitive   = true
}

variable "notifications_token" {
  description = "Token used by notifications service"
  type        = string
  sensitive   = true
}
