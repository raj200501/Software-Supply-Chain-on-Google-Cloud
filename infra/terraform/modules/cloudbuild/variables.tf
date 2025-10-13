variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "cloud_build_sa" {
  type = string
}

variable "artifact_registry_repo" {
  type = string
}

variable "kms_key_name" {
  type = string
}

variable "attestation_bucket" {
  type = string
}

variable "guac_bucket_prefix" {
  type = string
}

variable "github_owner" {
  type    = string
  default = "your-github-org"
}

variable "github_repo" {
  type    = string
  default = "slsa-bazel-gke-reference"
}
