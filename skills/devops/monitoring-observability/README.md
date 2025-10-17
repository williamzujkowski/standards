# Monitoring & Observability Skill

## Overview

Comprehensive skill module covering monitoring and observability for distributed systems with the three pillars: metrics, logs, and traces.

## Structure

```
monitoring-observability/
├── SKILL.md                          # Main skill content (959 lines)
├── config/
│   └── prometheus.yml                # Production Prometheus config (194 lines)
├── templates/
│   ├── recording-rules.yml           # PromQL recording rules (226 lines)
│   ├── alert-rules.yml               # Alerting rules (394 lines)
│   ├── grafana-dashboard.json        # Complete dashboard (361 lines)
│   └── otel-collector.yaml           # OpenTelemetry config (276 lines)
└── scripts/
    └── setup-monitoring-stack.sh     # Docker Compose stack (432 lines)

Total: ~2,842 lines of production-ready configuration
```

## Skill Content

### Level 1: Quick Reference (~800 tokens)

- Three pillars of observability
- Golden signals (latency, traffic, errors, saturation)
- Essential checklist
- Quick commands

### Level 2: Implementation Guide (~4,500 tokens)

1. **Metrics with Prometheus**
   - Architecture and configuration
   - Application instrumentation (Go, Python)
   - PromQL queries and recording rules

2. **Logging with ELK/Loki**
   - Structured logging best practices
   - Loki and Promtail configuration
   - LogQL queries

3. **Distributed Tracing**
   - OpenTelemetry instrumentation
   - Trace collection and storage
   - Context propagation

4. **Grafana Dashboards**
   - Dashboard JSON structure
   - Template variables
   - Panels and visualizations

5. **Alerting Strategies**
   - Alert rules and severity levels
   - Alertmanager configuration
   - Alert fatigue prevention

6. **SLIs, SLOs, and Error Budgets**
   - Service level indicators
   - SLO definitions
   - Error budget calculations

7. **Incident Response**
   - Runbook templates
   - Triage steps
   - Communication protocols

8. **Cost Optimization**
   - Cardinality management
   - Retention policies
   - Sampling strategies

### Level 3: Deep Dive Resources

- Official documentation links
- Recommended books
- Advanced topics
- Community resources

## Bundled Resources

### 1. Prometheus Configuration (`config/prometheus.yml`)

- Global settings and alerting
- Kubernetes service discovery
- Static targets
- Database exporters
- Blackbox probing
- Remote write configuration

### 2. Recording Rules (`templates/recording-rules.yml`)

- API performance metrics
- Infrastructure resource usage
- Database performance
- Kubernetes pod metrics
- SLI calculations
- Business metrics
- Cluster aggregates

### 3. Alert Rules (`templates/alert-rules.yml`)

- Infrastructure alerts (CPU, memory, disk)
- API service alerts (errors, latency, traffic)
- SLO and error budget alerts
- Database alerts (PostgreSQL, Redis)
- Kubernetes alerts
- Certificate expiration
- Business metric alerts
- Self-monitoring alerts

### 4. Grafana Dashboard (`templates/grafana-dashboard.json`)

- Request rate visualization
- Error rate with thresholds
- Latency percentiles
- Resource usage (CPU, memory)
- Network I/O
- Stats panels (uptime, response time)
- Top endpoints table
- Template variables for filtering

### 5. OpenTelemetry Collector (`templates/otel-collector.yaml`)

- Multiple receivers (OTLP, Jaeger, Zipkin, Prometheus)
- Processors (batch, sampling, filtering, resource detection)
- Multiple exporters (Jaeger, Tempo, Loki, Prometheus)
- Extensions (health check, profiler, zpages)
- Complete pipelines for traces, metrics, logs

### 6. Monitoring Stack Setup (`scripts/setup-monitoring-stack.sh`)

- Docker Compose orchestration
- Services included:
  - Prometheus + Node Exporter + cAdvisor
  - Grafana with pre-configured dashboard
  - Loki + Promtail
  - Jaeger
  - OpenTelemetry Collector
  - Alertmanager
  - Blackbox Exporter
- Health checks for all services
- Easy start/stop/restart commands

## Quick Start

```bash
# Setup and start the monitoring stack
cd skills/devops/monitoring-observability
./scripts/setup-monitoring-stack.sh start

# Access the services:
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)
# - Jaeger: http://localhost:16686
# - Alertmanager: http://localhost:9093

# View logs
./scripts/setup-monitoring-stack.sh logs [service]

# Stop the stack
./scripts/setup-monitoring-stack.sh stop

# Cleanup (removes all data)
./scripts/setup-monitoring-stack.sh cleanup
```

## Prerequisites

- Docker and Docker Compose installed
- Basic understanding of containerization
- Familiarity with CI/CD concepts (from ci-cd-pipelines skill)
- Kubernetes basics (optional, for Kubernetes examples)

## Learning Path

1. **Read SKILL.md Level 1** - Understand the fundamentals
2. **Explore configurations** - Study the provided templates
3. **Run the stack** - Deploy using setup script
4. **Instrument an app** - Add metrics/traces to your service
5. **Create dashboards** - Build custom visualizations
6. **Set up alerts** - Configure meaningful alerts
7. **Implement SLOs** - Define service level objectives

## Integration with Other Skills

- **CI/CD Pipelines**: Integrate monitoring into deployment pipelines
- **Kubernetes Basics**: Monitor Kubernetes clusters
- **Infrastructure as Code**: Automate monitoring deployment

## Production Considerations

- **Security**: Enable TLS, authentication, and authorization
- **High Availability**: Run multiple replicas of critical services
- **Scalability**: Use Thanos for Prometheus, Tempo for traces
- **Retention**: Configure appropriate data retention policies
- **Cost**: Monitor cardinality and storage usage

## Advanced Topics

- Multi-cluster monitoring with Thanos
- Long-term metrics storage
- Custom Prometheus exporters
- Advanced PromQL and LogQL
- Continuous profiling
- Real User Monitoring (RUM)
- AIOps and anomaly detection

## Support

For issues or questions:

- Review the SKILL.md documentation
- Check official documentation linked in Level 3
- Consult the SPARC methodology for systematic troubleshooting

---

**Estimated Time**: 8-10 hours to complete all levels
**Difficulty**: Intermediate
**Category**: DevOps
