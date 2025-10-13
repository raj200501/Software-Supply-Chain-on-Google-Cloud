resource "google_container_cluster" "main" {
  name               = "slsa-ref-cluster"
  location           = var.region
  project            = var.project_id
  network            = var.network
  subnetwork         = var.subnetwork
  release_channel {
    channel = var.release_channel
  }
  remove_default_node_pool = true
  initial_node_count       = 1
  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }
  workload_identity_config {
    workload_pool = var.workload_identity_pool
  }
  binary_authorization {
    evaluation_mode = "PROJECT_SINGLETON_POLICY_ENFORCE"
  }
  private_cluster_config {
    enable_private_endpoint = false
    enable_private_nodes    = true
    master_ipv4_cidr_block  = "172.16.0.16/28"
  }
}

resource "google_container_node_pool" "primary" {
  name       = "primary-pool"
  cluster    = google_container_cluster.main.name
  project    = var.project_id
  location   = var.region
  node_count = 3
  node_config {
    machine_type = "e2-standard-4"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
    workload_metadata_config {
      mode = "GKE_METADATA"
    }
  }
}

output "cluster_name" {
  value = google_container_cluster.main.name
}

output "cluster_location" {
  value = google_container_cluster.main.location
}
