variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "attestor_members" {
  type = list(string)
}

variable "attestation_project" {
  type = string
}

variable "artifact_registry_projects" {
  type = list(string)
}

variable "attestor_public_key" {
  type = string
}
