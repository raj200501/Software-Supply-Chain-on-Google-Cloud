resource "google_binary_authorization_attestor" "main" {
  name        = "slsa-attestor"
  project     = var.project_id
  description = "Attestor verifying cosign signatures and SLSA provenance"

  attestation_authority_note {
    note_reference = google_container_analysis_note.attestor.id
    public_keys {
      pkix_public_key {
        public_key_pem      = var.attestor_public_key
        signature_algorithm = "ECDSA_P256_SHA256"
      }
    }
  }
}

resource "google_container_analysis_note" "attestor" {
  project = var.project_id
  note_id = "slsa-attestor-note"
}

resource "google_binary_authorization_policy" "policy" {
  project = var.project_id

  admission_whitelist_patterns {
    name_pattern = "gcr.io/google_containers/*"
  }

  default_admission_rule {
    evaluation_mode  = "REQUIRE_ATTESTATION"
    enforcement_mode = "ENFORCED_BLOCK_AND_AUDIT_LOG"
    require_attestations_by = [
      google_binary_authorization_attestor.main.name
    ]
  }

  cluster_admission_rules = {
    "*" = {
      evaluation_mode         = "REQUIRE_ATTESTATION"
      enforcement_mode        = "ENFORCED_BLOCK_AND_AUDIT_LOG"
      require_attestations_by = [google_binary_authorization_attestor.main.name]
    }
  }
}

resource "google_binary_authorization_continuous_validation_config" "cv" {
  project = var.project_id
  description = "Continuous validation for SLSA reference"
}

output "attestor_name" {
  value = google_binary_authorization_attestor.main.name
}
