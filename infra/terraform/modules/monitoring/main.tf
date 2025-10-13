resource "google_monitoring_dashboard" "service_overview" {
  project     = var.project_id
  dashboard_json = jsonencode({
    displayName = "SLSA Reference Overview"
    mosaicLayout = {
      columns = 6
      tiles = [
        {
          xPos  = 0
          yPos  = 0
          width = 3
          height = 2
          widget = {
            title = "Request latency"
            xyChart = {
              dataSets = [{
                timeSeriesQuery = {
                  unitOverride = "ms"
                  timeSeriesFilter = {
                    filter = "metric.type=\"custom.googleapis.com/http/server/latency\""
                  }
                }
              }]
            }
          }
        },
        {
          xPos  = 3
          yPos  = 0
          width = 3
          height = 2
          widget = {
            title = "Binary Authorization denials"
            xyChart = {
              dataSets = [{
                timeSeriesQuery = {
                  timeSeriesFilter = {
                    filter = "metric.type=\"logging.googleapis.com/user/binauthz_denials\""
                  }
                }
              }]
            }
          }
        }
      ]
    }
  })
}

output "dashboard_id" {
  value = google_monitoring_dashboard.service_overview.id
}
