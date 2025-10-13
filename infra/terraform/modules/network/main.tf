resource "google_compute_network" "main" {
  name                    = "slsa-ref-network"
  project                 = var.project_id
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "main" {
  name          = "slsa-ref-subnet"
  project       = var.project_id
  region        = var.region
  network       = google_compute_network.main.id
  ip_cidr_range = "10.20.0.0/20"
  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.21.0.0/20"
  }
  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.22.0.0/24"
  }
}

output "network_self_link" {
  value = google_compute_network.main.self_link
}

output "subnetwork_self_link" {
  value = google_compute_subnetwork.main.self_link
}
