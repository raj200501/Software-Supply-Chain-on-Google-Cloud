resource "google_kms_key_ring" "attest" {
  name     = "slsa-ref-keyring"
  project  = var.project_id
  location = var.location
}

resource "google_kms_crypto_key" "container" {
  name            = "container-signing"
  key_ring        = google_kms_key_ring.attest.id
  purpose         = "ASYMMETRIC_SIGN"
  version_template {
    algorithm = "EC_SIGN_P256_SHA256"
  }
}

resource "google_kms_crypto_key" "attestor" {
  name            = "binauthz-attestor"
  key_ring        = google_kms_key_ring.attest.id
  purpose         = "ASYMMETRIC_SIGN"
  version_template {
    algorithm = "EC_SIGN_P256_SHA256"
  }
}

resource "google_kms_crypto_key_version" "attestor_primary" {
  crypto_key = google_kms_crypto_key.attestor.id
}

data "google_kms_crypto_key_version" "attestor_primary" {
  name = google_kms_crypto_key_version.attestor_primary.name
}

resource "google_kms_crypto_key_iam_binding" "container_signers" {
  crypto_key_id = google_kms_crypto_key.container.id
  role          = "roles/cloudkms.signerVerifier"
  members       = [for m in var.attestor_members : "serviceAccount:${m}"]
}

output "container_key_id" {
  value = google_kms_crypto_key.container.id
}

output "attestor_key_id" {
  value = google_kms_crypto_key.attestor.id
}

output "attestor_public_key" {
  value = data.google_kms_crypto_key_version.attestor_primary.public_key[0].pem
}
