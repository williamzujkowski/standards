---
name: monitoring-observability
category: devops
difficulty: intermediate
tags: [monitoring, observability, prometheus, grafana, elk, opentelemetry, metrics, logging, tracing]
description: Master monitoring and observability for distributed systems
prerequisites: [docker, kubernetes-basics, ci-cd-pipelines]
estimated_time: 8-10 hours
---

# Monitoring & Observability

## Level 1: Quick Reference

### Three Pillars of Observability

**Metrics** - Numerical measurements over time

- Counter (only increases): request_total, errors_total
- Gauge (can go up/down): cpu_usage, memory_bytes
- Histogram (distribution): request_duration_seconds
- Summary (quantiles): response_time_summary

**Logs** - Timestamped event records

- Structured (JSON): `{"level":"error","msg":"connection failed","user_id":123}`
- Unstructured (text): `2025-01-15 ERROR: Connection timeout`
- Log levels: DEBUG, INFO, WARN, ERROR, FATAL

**Traces** - Request flow through distributed systems

- Span: Single operation (HTTP request, DB query)
- Trace: Collection of spans showing full request path
- Context propagation: Trace ID passed between services

### Golden Signals (Google SRE)

```
Latency    - How long requests take
Traffic    - How many requests (RPS, QPS)
Errors     - Rate of failed requests
Saturation - How "full" your service is (CPU, memory, disk, network)
```

### Essential Checklist

- [ ] **SLIs defined**: Key user-facing metrics (availability, latency)
- [ ] **SLOs set**: Service Level Objectives (99.9% availability)
- [ ] **Error budgets**: 0.1% downtime = 43 minutes/month
- [ ] **Alerting configured**: On-call rotation, escalation policies
- [ ] **Dashboards created**: Service overview, system health
- [ ] **Log aggregation**: Centralized logging with retention policies
- [ ] **Distributed tracing**: Request path visualization
- [ ] **Runbooks written**: Step-by-step incident response guides

### Quick Commands

```bash
# Prometheus - Query metrics
curl 'http://localhost:9090/api/v1/query?query=up'

# Check alerting rules
promtool check rules alert-rules.yml

# Grafana - Create API key
curl -X POST http://admin:admin@localhost:3000/api/auth/keys \
  -H "Content-Type: application/json" \
  -d '{"name":"deploy-key","role":"Admin"}'

# Elasticsearch - Check cluster health
curl -X GET "localhost:9200/_cluster/health?pretty"

# Jaeger - Query traces
curl "http://localhost:16686/api/traces?service=frontend&limit=10"
```

---

## Level 2: Implementation Guide

### 1. Metrics with Prometheus

#### Architecture Overview

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ Application │────▶│  Prometheus  │────▶│   Grafana   │
│  /metrics   │     │   (scrape)   │     │ (visualize) │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Alertmanager │
                    │  (alerting)  │
                    └──────────────┘
```

#### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    env: 'prod'

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

# Load rules
rule_files:
  - 'recording-rules.yml'
  - 'alert-rules.yml'

# Scrape configurations
scrape_configs:
  # Prometheus itself
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Node Exporter (system metrics)
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
        labels:
          env: 'production'

  # Application metrics
  - job_name: 'api-service'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
```

#### Instrumenting Applications

**Go Example**:

```go
package main

import (
    "net/http"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
    httpRequestsTotal = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests",
        },
        []string{"method", "endpoint", "status"},
    )

    httpRequestDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request latency",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "endpoint"},
    )
)

func instrumentHandler(handler http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        timer := prometheus.NewTimer(httpRequestDuration.WithLabelValues(r.Method, r.URL.Path))
        defer timer.ObserveDuration()

        handler(w, r)

        httpRequestsTotal.WithLabelValues(r.Method, r.URL.Path, "200").Inc()
    }
}

func main() {
    http.Handle("/metrics", promhttp.Handler())
    http.HandleFunc("/api/users", instrumentHandler(usersHandler))
    http.ListenAndServe(":8080", nil)
}
```

**Python Example**:

```python
from prometheus_client import Counter, Histogram, start_http_server
import time

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

@REQUEST_LATENCY.labels(method='GET', endpoint='/users').time()
def get_users():
    # Simulate work
    time.sleep(0.1)
    REQUEST_COUNT.labels(method='GET', endpoint='/users', status='200').inc()
    return {"users": []}

if __name__ == '__main__':
    start_http_server(8000)  # Expose metrics on :8000/metrics
```

#### PromQL Query Examples

```promql
# Request rate (requests per second)
rate(http_requests_total[5m])

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# CPU usage by pod
sum(rate(container_cpu_usage_seconds_total[5m])) by (pod)

# Memory usage percentage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100

# Disk space remaining
(node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100

# Aggregation examples
sum(rate(http_requests_total[5m])) by (status)          # By status code
avg(http_request_duration_seconds) by (endpoint)        # By endpoint
topk(5, rate(http_requests_total[5m]))                  # Top 5 services
```

#### Recording Rules

```yaml
# recording-rules.yml
groups:
  - name: api_rules
    interval: 30s
    rules:
      # Pre-compute expensive queries
      - record: job:http_requests:rate5m
        expr: sum(rate(http_requests_total[5m])) by (job)

      - record: job:http_request_duration:p95
        expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))

      - record: job:http_errors:rate5m
        expr: sum(rate(http_requests_total{status=~"5.."}[5m])) by (job)

      - record: instance:cpu:usage
        expr: 100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

### 2. Logging with ELK/Loki

#### Structured Logging Best Practices

**Good - Structured JSON**:

```json
{
  "timestamp": "2025-01-15T10:30:45Z",
  "level": "error",
  "service": "api-gateway",
  "trace_id": "abc123",
  "user_id": 12345,
  "message": "Database connection failed",
  "error": "connection timeout after 5s",
  "db_host": "db-primary.internal",
  "retry_count": 3
}
```

**Bad - Unstructured**:

```
[ERROR] 2025-01-15 10:30:45 - User 12345 got error: Database connection failed (timeout 5s) from db-primary.internal, retried 3 times
```

#### Log Levels Strategy

```
FATAL  - System unusable, immediate action required
ERROR  - Error occurred, but system continues
WARN   - Potential issue, degraded functionality
INFO   - Important business events
DEBUG  - Detailed diagnostic information (disabled in prod)
TRACE  - Very detailed, function-level tracing (dev only)
```

#### Loki Configuration (Lightweight Alternative to ELK)

```yaml
# loki-config.yaml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
  chunk_idle_period: 5m
  chunk_retain_period: 30s

schema_config:
  configs:
    - from: 2024-01-01
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/boltdb-cache
    shared_store: filesystem
  filesystem:
    directory: /loki/chunks

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h  # 7 days
  ingestion_rate_mb: 10
  ingestion_burst_size_mb: 20

chunk_store_config:
  max_look_back_period: 720h  # 30 days
```

#### Promtail (Log Shipper for Loki)

```yaml
# promtail-config.yaml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: containers
    static_configs:
      - targets:
          - localhost
        labels:
          job: containerlogs
          __path__: /var/lib/docker/containers/*/*.log
    pipeline_stages:
      # Parse JSON logs
      - json:
          expressions:
            level: level
            message: message
            trace_id: trace_id
      # Extract labels
      - labels:
          level:
          trace_id:
      # Drop debug logs in production
      - match:
          selector: '{level="debug"}'
          action: drop
```

#### LogQL Query Examples

```logql
# Search for errors in api-service
{service="api-service"} |= "error"

# Count errors per minute
sum(rate({service="api-service"} |= "error" [1m]))

# Extract JSON field
{service="api-service"} | json | user_id="12345"

# Pattern matching
{service="api-service"} |~ "timeout|connection refused"

# Aggregate by status code
sum(count_over_time({service="api-service"} | json | __error__="" [5m])) by (status)
```

### 3. Distributed Tracing with OpenTelemetry

#### OpenTelemetry Architecture

```
┌──────────────┐     ┌─────────────────┐     ┌─────────────┐
│ Application  │────▶│ OTel Collector  │────▶│   Jaeger    │
│ (SDK/Agent)  │     │  (aggregate)    │     │ (storage)   │
└──────────────┘     └─────────────────┘     └─────────────┘
                              │
                              ├───────▶ Prometheus (metrics)
                              └───────▶ Loki (logs)
```

#### Instrumenting with OpenTelemetry

**Go Example**:

```go
package main

import (
    "context"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/jaeger"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.4.0"
    "go.opentelemetry.io/otel/trace"
)

func initTracer() (*sdktrace.TracerProvider, error) {
    exporter, err := jaeger.New(jaeger.WithCollectorEndpoint(
        jaeger.WithEndpoint("http://jaeger:14268/api/traces"),
    ))
    if err != nil {
        return nil, err
    }

    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceNameKey.String("api-service"),
            semconv.ServiceVersionKey.String("1.0.0"),
        )),
    )
    otel.SetTracerProvider(tp)
    return tp, nil
}

func handleRequest(ctx context.Context) {
    tracer := otel.Tracer("api-service")
    ctx, span := tracer.Start(ctx, "handle_request")
    defer span.End()

    // Add attributes
    span.SetAttributes(
        attribute.String("user.id", "12345"),
        attribute.String("http.method", "GET"),
    )

    // Call downstream service
    callDatabase(ctx)
}

func callDatabase(ctx context.Context) {
    tracer := otel.Tracer("api-service")
    ctx, span := tracer.Start(ctx, "database_query")
    defer span.End()

    span.SetAttributes(
        attribute.String("db.system", "postgresql"),
        attribute.String("db.statement", "SELECT * FROM users"),
    )

    // Simulate DB call
    time.Sleep(50 * time.Millisecond)
}
```

**Python Example**:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# Setup tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Use tracer
with tracer.start_as_current_span("handle_request") as span:
    span.set_attribute("user.id", "12345")
    span.set_attribute("http.method", "GET")

    with tracer.start_as_current_span("database_query") as db_span:
        db_span.set_attribute("db.system", "postgresql")
        # Perform database operation
```

### 4. Grafana Dashboards

#### Dashboard JSON Structure

```json
{
  "dashboard": {
    "title": "API Service Overview",
    "tags": ["api", "production"],
    "timezone": "browser",
    "refresh": "30s",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (status)",
            "legendFormat": "{{status}}"
          }
        ],
        "yaxes": [
          {"format": "reqps", "label": "Requests/sec"}
        ]
      },
      {
        "id": 2,
        "title": "Latency (p95)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "p95"
          }
        ]
      }
    ]
  }
}
```

#### Template Variables

```json
{
  "templating": {
    "list": [
      {
        "name": "env",
        "type": "query",
        "query": "label_values(up, env)",
        "multi": false,
        "includeAll": false
      },
      {
        "name": "service",
        "type": "query",
        "query": "label_values(up{env=\"$env\"}, job)",
        "multi": true,
        "includeAll": true
      }
    ]
  }
}
```

### 5. Alerting Strategies

#### Alert Rules

```yaml
# alert-rules.yml
groups:
  - name: api_alerts
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (job)
          /
          sum(rate(http_requests_total[5m])) by (job)
          > 0.05
        for: 5m
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "High error rate on {{ $labels.job }}"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 5%)"
          runbook_url: "https://wiki.company.com/runbooks/high-error-rate"

      # High latency
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le)
          ) > 1.0
        for: 10m
        labels:
          severity: warning
          team: backend
        annotations:
          summary: "High latency on {{ $labels.job }}"
          description: "p95 latency is {{ $value }}s (threshold: 1s)"

      # Service down
      - alert: ServiceDown
        expr: up == 0
        for: 2m
        labels:
          severity: critical
          team: sre
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "Instance {{ $labels.instance }} has been down for 2 minutes"

      # Disk space low
      - alert: DiskSpaceLow
        expr: |
          (node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 < 10
        for: 5m
        labels:
          severity: warning
          team: infrastructure
        annotations:
          summary: "Disk space low on {{ $labels.instance }}"
          description: "Only {{ $value }}% disk space remaining"
```

#### Alertmanager Configuration

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
  pagerduty_url: 'https://events.pagerduty.com/v2/enqueue'

route:
  receiver: 'default'
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h

  routes:
    # Critical alerts to PagerDuty
    - match:
        severity: critical
      receiver: 'pagerduty'
      continue: true

    # Warning alerts to Slack
    - match:
        severity: warning
      receiver: 'slack-warnings'

    # Team-specific routing
    - match:
        team: backend
      receiver: 'slack-backend'

receivers:
  - name: 'default'
    slack_configs:
      - channel: '#alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: 'YOUR_PAGERDUTY_KEY'
        description: '{{ .GroupLabels.alertname }}'

  - name: 'slack-warnings'
    slack_configs:
      - channel: '#warnings'
        color: 'warning'

  - name: 'slack-backend'
    slack_configs:
      - channel: '#team-backend'

inhibit_rules:
  # Inhibit warnings if critical alert is firing
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'instance']
```

#### Alert Fatigue Prevention

**Best Practices**:

1. **Actionable alerts only**: Every alert should require human action
2. **Meaningful thresholds**: Based on actual user impact, not arbitrary numbers
3. **Proper severity levels**: Critical = wake someone up, Warning = investigate during business hours
4. **Group related alerts**: Don't send 100 alerts for same issue
5. **Runbooks required**: Every alert must link to troubleshooting steps
6. **Review regularly**: Delete alerts that never fire or always ignored

### 6. SLIs, SLOs, and Error Budgets

#### Service Level Indicators (SLIs)

```
SLI = Good Events / Total Events

Availability SLI = Successful Requests / Total Requests
Latency SLI = Requests < 100ms / Total Requests
Throughput SLI = Requests Processed / Expected Requests
```

#### Service Level Objectives (SLOs)

```yaml
# slo-definitions.yml
slos:
  - name: api_availability
    description: "API should be available 99.9% of the time"
    target: 0.999
    window: 30d
    sli_query: |
      sum(rate(http_requests_total{status!~"5.."}[30d]))
      /
      sum(rate(http_requests_total[30d]))

  - name: api_latency
    description: "95% of requests should complete in < 200ms"
    target: 0.95
    window: 30d
    sli_query: |
      histogram_quantile(0.95,
        sum(rate(http_request_duration_seconds_bucket[30d])) by (le)
      ) < 0.2

  - name: api_error_rate
    description: "Error rate should be < 1%"
    target: 0.99
    window: 30d
    sli_query: |
      1 - (
        sum(rate(http_requests_total{status=~"5.."}[30d]))
        /
        sum(rate(http_requests_total[30d]))
      )
```

#### Error Budget Calculation

```
SLO = 99.9% uptime
Allowed downtime = 100% - 99.9% = 0.1%

Over 30 days:
30 days * 24 hours * 60 minutes = 43,200 minutes
Error budget = 43,200 * 0.001 = 43.2 minutes

If you've used 30 minutes of downtime this month:
Remaining budget = 43.2 - 30 = 13.2 minutes
Budget consumption = 30 / 43.2 = 69.4%
```

**Error Budget Policy**:

```
Budget remaining > 50%: Deploy freely
Budget remaining 20-50%: Require approval for risky changes
Budget remaining < 20%: Freeze deployments, focus on reliability
Budget exhausted: Incident declared, all hands on deck
```

### 7. Incident Response

#### Runbook Template

```markdown
# Runbook: High API Error Rate

## Severity: P1 (Critical)

## Symptoms
- Error rate > 5% for 5+ minutes
- Alert: `HighErrorRate` firing
- User reports of 500 errors

## Impact
- Users cannot complete transactions
- Revenue loss: ~$1000/minute

## Triage Steps

1. **Check service health**
   ```bash
   kubectl get pods -n production
   kubectl logs -n production -l app=api-service --tail=100
   ```

2. **Check dependencies**
   - Database: http://grafana/d/database
   - Cache: http://grafana/d/redis
   - External APIs: http://grafana/d/external

3. **Check recent changes**

   ```bash
   git log --since="1 hour ago" --pretty=format:"%h %an %s"
   ```

## Resolution Steps

### If database is down:

1. Check DB master health: `kubectl get pods -n database`
2. Failover to replica if needed: `./scripts/db-failover.sh`
3. Verify connection restored: `curl http://api/health/db`

### If recent deployment caused issue:

1. Rollback: `kubectl rollout undo deployment/api-service`
2. Verify: `kubectl rollout status deployment/api-service`
3. Monitor error rate: http://grafana/d/api-overview

### If external API is down:

1. Enable circuit breaker: `kubectl patch configmap api-config --patch '{"data":{"circuit_breaker":"true"}}'`
2. Restart pods: `kubectl rollout restart deployment/api-service`

## Communication

- Update status page: https://status.company.com
- Post to #incidents Slack channel
- Notify on-call manager if issue persists > 15 min

## Post-Incident

- [ ] Write postmortem within 48 hours
- [ ] Add action items to backlog
- [ ] Update runbook with learnings

```

### 8. Cost Optimization

#### Cardinality Management

**High cardinality problem**:
```promql
# BAD: user_id creates millions of unique time series
http_requests_total{user_id="12345", endpoint="/api/users"}

# GOOD: Aggregate by service and endpoint only
http_requests_total{service="api", endpoint="/api/users"}

# If you need user-level data, use logs or traces instead
```

**Cardinality analysis**:

```promql
# Find metrics with highest cardinality
topk(10, count by (__name__)({__name__=~".+"}))

# Count unique label combinations
count({__name__="http_requests_total"})
```

#### Retention Policies

```yaml
# prometheus.yml
storage:
  tsdb:
    retention.time: 15d  # Keep raw metrics for 15 days
    retention.size: 50GB # Or until 50GB limit

# Use recording rules for long-term data
# Keep pre-aggregated data in cheaper storage (e.g., Thanos)
```

#### Sampling Strategies

```yaml
# For high-traffic services, sample traces
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-collector-config
data:
  config.yaml: |
    processors:
      probabilistic_sampler:
        sampling_percentage: 10  # Sample 10% of traces

      tail_sampling:
        policies:
          # Always keep error traces
          - name: errors
            type: status_code
            status_code: {status_codes: [ERROR]}
          # Sample 5% of successful traces
          - name: success
            type: probabilistic
            probabilistic: {sampling_percentage: 5}
```

---

## Level 3: Deep Dive Resources

### Official Documentation

- [Prometheus Docs](https://prometheus.io/docs/)
- [Grafana Docs](https://grafana.com/docs/)
- [OpenTelemetry](https://opentelemetry.io/docs/)
- [Jaeger](https://www.jaegertracing.io/docs/)
- [Loki](https://grafana.com/docs/loki/latest/)

### Books

- **"Site Reliability Engineering"** - Google SRE team
- **"The Site Reliability Workbook"** - Practical SRE examples
- **"Distributed Tracing in Practice"** - Austin Parker et al.
- **"Observability Engineering"** - Charity Majors, Liz Fong-Jones

### Advanced Topics

- Multi-cluster monitoring with Thanos
- Long-term metrics storage
- Custom Prometheus exporters
- Advanced PromQL and LogQL
- Continuous profiling with Pyroscope
- Real User Monitoring (RUM)
- Synthetic monitoring
- AIOps and anomaly detection

### Community

- [CNCF Observability SIG](https://github.com/cncf/sig-observability)
- [Prometheus Community](https://prometheus.io/community/)
- [#observability on CNCF Slack](https://slack.cncf.io)
