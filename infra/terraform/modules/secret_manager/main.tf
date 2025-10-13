locals {
  formatted_secrets = [for key, value in var.secrets : {
    name  = key
    value = value
  }]
}

resource "google_secret_manager_secret" "secret" {
  for_each = { for secret in local.formatted_secrets : secret.name => secret }
  project  = var.project_id
  secret_id = each.value.name

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "secret" {
  for_each    = google_secret_manager_secret.secret
  secret      = each.value.id
  secret_data = var.secrets[each.key]
}
