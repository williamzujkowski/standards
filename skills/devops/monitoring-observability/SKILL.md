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

## Level 2:
>
> **📚 Full Examples**: See [REFERENCE.md](./REFERENCE.md) for complete code samples, detailed configurations, and production-ready implementations.

 Implementation Guide

### 1. Metrics with Prometheus

#### Architecture Overview


*See [REFERENCE.md](./REFERENCE.md#example-0) for complete implementation.*


#### Prometheus Configuration


*See [REFERENCE.md](./REFERENCE.md#example-1) for complete implementation.*


#### Instrumenting Applications

**Go Example**:


*See [REFERENCE.md](./REFERENCE.md#example-2) for complete implementation.*


**Python Example**:


*See [REFERENCE.md](./REFERENCE.md#example-3) for complete implementation.*


#### PromQL Query Examples


*See [REFERENCE.md](./REFERENCE.md#example-4) for complete implementation.*


#### Recording Rules


*See [REFERENCE.md](./REFERENCE.md#example-5) for complete implementation.*


### 2. Logging with ELK/Loki

#### Structured Logging Best Practices

**Good - Structured JSON**:


*See [REFERENCE.md](./REFERENCE.md#example-6) for complete implementation.*


**Bad - Unstructured**:

```
[ERROR] 2025-01-15 10:30:45 - User 12345 got error: Database connection failed (timeout 5s) from db-primary.internal, retried 3 times
```

#### Log Levels Strategy


*See [REFERENCE.md](./REFERENCE.md#example-8) for complete implementation.*


#### Loki Configuration (Lightweight Alternative to ELK)


*See [REFERENCE.md](./REFERENCE.md#example-9) for complete implementation.*


#### Promtail (Log Shipper for Loki)


*See [REFERENCE.md](./REFERENCE.md#example-10) for complete implementation.*


#### LogQL Query Examples


*See [REFERENCE.md](./REFERENCE.md#example-11) for complete implementation.*


### 3. Distributed Tracing with OpenTelemetry

#### OpenTelemetry Architecture


*See [REFERENCE.md](./REFERENCE.md#example-12) for complete implementation.*


#### Instrumenting with OpenTelemetry

**Go Example**:


*See [REFERENCE.md](./REFERENCE.md#example-13) for complete implementation.*


**Python Example**:


*See [REFERENCE.md](./REFERENCE.md#example-14) for complete implementation.*


### 4. Grafana Dashboards

#### Dashboard JSON Structure


*See [REFERENCE.md](./REFERENCE.md#example-15) for complete implementation.*


#### Template Variables


*See [REFERENCE.md](./REFERENCE.md#example-16) for complete implementation.*


### 5. Alerting Strategies

#### Alert Rules


*See [REFERENCE.md](./REFERENCE.md#example-17) for complete implementation.*


#### Alertmanager Configuration


*See [REFERENCE.md](./REFERENCE.md#example-18) for complete implementation.*


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


*See [REFERENCE.md](./REFERENCE.md#example-20) for complete implementation.*


#### Error Budget Calculation


*See [REFERENCE.md](./REFERENCE.md#example-21) for complete implementation.*


**Error Budget Policy**:


*See [REFERENCE.md](./REFERENCE.md#example-22) for complete implementation.*


### 7. Incident Response

#### Runbook Template


*See [REFERENCE.md](./REFERENCE.md#example-23) for complete implementation.*

bash
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


*See [REFERENCE.md](./REFERENCE.md#example-25) for complete implementation.*



### 8. Cost Optimization

#### Cardinality Management

**High cardinality problem**:


*See [REFERENCE.md](./REFERENCE.md#example-26) for complete implementation.*



**Cardinality analysis**:

```promql
# Find metrics with highest cardinality
topk(10, count by (__name__)({__name__=~".+"}))

# Count unique label combinations
count({__name__="http_requests_total"})
```

#### Retention Policies


*See [REFERENCE.md](./REFERENCE.md#example-28) for complete implementation.*


#### Sampling Strategies


*See [REFERENCE.md](./REFERENCE.md#example-29) for complete implementation.*


## Examples

### Basic Usage


*See [REFERENCE.md](./REFERENCE.md#example-30) for complete implementation.*


### Advanced Usage

```python
// TODO: Add advanced example for monitoring-observability
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how monitoring-observability
// works with other systems and services
```

See `examples/monitoring-observability/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Common development tools and frameworks
- **Prerequisites**: Basic understanding of general concepts

### Downstream Consumers

- **Applications**: Production systems requiring monitoring-observability functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- See other skills in this category

### Common Integration Patterns

1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points

## Common Pitfalls

### Pitfall 1: Insufficient Testing

**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:

- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration

**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:

- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices

**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:

- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**

- Follow established patterns and conventions for monitoring-observability
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

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
