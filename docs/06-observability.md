# Observability Strategy

All services and supporting tooling are instrumented with OpenTelemetry (OTEL) to provide unified metrics, traces, and logs. This document explains the instrumentation and how to observe the system in local and cloud environments.

## Instrumentation overview

- Each microservice initializes OTEL SDKs using environment variables defined in `infra/k8s/base/config/otel-collector-config.yaml`.
- Traces include service-level span attributes (`service.name`, `deployment.environment`).
- Metrics cover request latency, database interactions, and queue depth.
- Logs are exported to stdout with OTEL context injected for correlation.

## Collector configuration

The OTEL Collector configuration is located at `infra/k8s/base/config/otel-collector-config.yaml`. Key pipelines:

- `traces`: Receives OTLP/gRPC from services and exports to stdout locally or Cloud Trace in GCP.
- `metrics`: Receives OTLP and exposes Prometheus scrape endpoints.
- `logs`: Routes structured logs to Cloud Logging via the `googlecloud` exporter when running in GCP.

The same configuration is reused in docker-compose via the `otel-collector` service and in Kubernetes via a DaemonSet.

## Local workflows

1. Start the stack via `make compose-up`.
2. Access traces at `http://localhost:55679/debug/tracez`.
3. Scrape Prometheus metrics from `http://localhost:9464/metrics`.
4. Use the provided Grafana dashboards located in `docs/dashboards/*.json` by importing them into a local Grafana instance.

## GCP workflows

- Cloud Trace: The Terraform stack creates a sink to export traces. View them under **Trace Explorer** filtered by `resource.label."service.name"`.
- Cloud Monitoring: Terraform provisions dashboards (see `infra/terraform/modules/monitoring`).
- Cloud Logging: Logs are shipped via the OTEL collector and tagged with `serviceContext.service`.

## Alerting

Prometheus-style alerts are defined under `infra/k8s/base/monitoring/alerting-rules.yaml`. They cover:

- High error rate per service.
- SBOM ingestion lag reported by GUAC.
- Binary Authorization denials.

In Google Cloud, Alert Policies are created via Terraform with similar thresholds and notifications routed to Cloud Pub/Sub or email groups.
