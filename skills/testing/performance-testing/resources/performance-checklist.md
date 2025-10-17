# Performance Testing Checklist: SLI/SLO/SLA Guide

## Service Level Indicators (SLIs)

SLIs are **quantitative measurements** of service behavior that matter to users.

### Common SLIs

**Availability:**
- Definition: Percentage of successful requests
- Measurement: `successful_requests / total_requests`
- Example: 99.9% of requests return 2xx or 3xx status codes

**Latency:**
- Definition: Time to complete a request
- Measurement: Response time at specific percentiles (p50, p95, p99)
- Example: 95% of requests complete in < 500ms

**Throughput:**
- Definition: Number of requests processed per unit time
- Measurement: Requests per second (RPS)
- Example: System processes 1000 RPS at peak load

**Error Rate:**
- Definition: Percentage of failed requests
- Measurement: `failed_requests / total_requests`
- Example: < 0.1% of requests result in 5xx errors

**Durability:**
- Definition: Data integrity and persistence
- Measurement: Successful data writes / Total data writes
- Example: 99.999% of writes are durably stored

### SLI Selection Criteria

- **User-Centric**: Measure what users actually experience
- **Measurable**: Can be reliably quantified from logs/metrics
- **Actionable**: Changes in SLI should trigger specific actions
- **Relevant**: Directly impacts user satisfaction

---

## Service Level Objectives (SLOs)

SLOs are **target values or ranges** for SLIs over a specific time window.

### SLO Components

**Target Value:**
```yaml
slo:
  sli: latency_p95
  target: 500
  unit: milliseconds
  comparison: less_than
```

**Time Window:**
```yaml
slo:
  sli: availability
  target: 99.9
  unit: percent
  window: 30 days  # Rolling 30-day window
```

**Measurement Interval:**
```yaml
slo:
  sli: error_rate
  target: 0.1
  unit: percent
  measurement_interval: 5 minutes
  aggregation: average
```

### SLO Examples by Service Type

**API Service:**
- Availability: 99.9% (43.2 min downtime/month)
- Latency p95: < 500ms
- Latency p99: < 1000ms
- Error rate: < 0.1%

**Web Application:**
- Page load time p95: < 2s
- Time to interactive p95: < 3s
- Availability: 99.95%
- Error rate: < 0.05%

**Data Pipeline:**
- Job completion rate: 99.5%
- Processing latency p95: < 5 minutes
- Data accuracy: 99.99%
- Freshness: < 15 minutes lag

**Machine Learning Service:**
- Inference latency p95: < 100ms
- Model accuracy: > 95%
- Availability: 99.5%
- Prediction throughput: > 500 RPS

### SLO Best Practices

- **Set Realistic Targets**: Based on historical data and user needs
- **Don't Over-Promise**: 100% uptime is impossible and wasteful
- **Include Error Budget**: Allow room for innovation and deployment
- **Review Regularly**: Adjust based on business needs and capabilities
- **Align with Stakeholders**: Ensure agreement across teams

---

## Service Level Agreements (SLAs)

SLAs are **contractual commitments** that define consequences when SLOs are not met.

### SLA Components

**Performance Guarantees:**
```yaml
sla:
  tier: gold
  availability: 99.95%
  latency_p95: 300ms
  support_response: 1 hour
  incident_resolution: 4 hours
```

**Financial Remedies:**
```yaml
sla:
  credits:
    - threshold: 99.95%
      credit: 0%
    - threshold: 99.9%
      credit: 10%  # 10% monthly fee credit
    - threshold: 99.0%
      credit: 25%
    - threshold: below_99%
      credit: 50%
```

**Service Tiers:**
```yaml
service_tiers:
  - name: Enterprise
    availability: 99.99%
    latency_p95: 200ms
    support: 24/7 phone + slack
    price: premium

  - name: Professional
    availability: 99.95%
    latency_p95: 300ms
    support: 24/7 email
    price: standard

  - name: Starter
    availability: 99.9%
    latency_p95: 500ms
    support: business hours
    price: basic
```

### SLA Calculation Example

**Monthly Uptime Calculation:**

```
SLA: 99.9% uptime per month
Total minutes in month: 43,200 (30 days)
Allowed downtime: 43,200 * 0.001 = 43.2 minutes

Actual uptime: 43,180 minutes
Actual downtime: 20 minutes
Actual availability: 43,180 / 43,200 = 99.95%

Result: SLA MET (downtime < 43.2 minutes)
```

**Credit Calculation:**

```yaml
actual_availability: 99.85%
sla_target: 99.9%
monthly_fee: $10,000

credit_table:
  - range: [99.9%, 100%]
    credit: 0%
  - range: [99.5%, 99.9%)
    credit: 10%
  - range: [99.0%, 99.5%)
    credit: 25%
  - range: [0%, 99.0%)
    credit: 50%

# 99.85% falls in 10% credit range
credit_amount: $10,000 * 0.10 = $1,000
```

---

## Error Budget

Error budget is the **allowed amount of unreliability** derived from SLOs.

### Error Budget Calculation

**Formula:**
```
Error Budget = (1 - SLO) * Total Requests
```

**Example:**
```
SLO: 99.9% availability
Total requests per month: 100,000,000
Error budget: (1 - 0.999) * 100,000,000 = 100,000 failed requests

Per day: 100,000 / 30 = 3,333 failed requests
Per hour: 3,333 / 24 = 139 failed requests
```

### Error Budget Usage

**Burn Rate:**
```
Burn Rate = Actual Error Rate / SLO Error Rate

Example:
SLO error rate: 0.1% (99.9% availability)
Current error rate: 0.5%
Burn Rate: 0.5 / 0.1 = 5x

At 5x burn rate, error budget will be exhausted in:
30 days / 5 = 6 days
```

**Alerting Thresholds:**
```yaml
error_budget_alerts:
  - burn_rate: 10x
    window: 1 hour
    severity: critical
    action: page oncall engineer

  - burn_rate: 5x
    window: 6 hours
    severity: high
    action: notify team lead

  - burn_rate: 2x
    window: 24 hours
    severity: warning
    action: create ticket
```

**Error Budget Policy:**
```yaml
error_budget_policy:
  - budget_remaining: "> 50%"
    actions:
      - normal_deployment_cadence
      - feature_development
      - controlled_experiments

  - budget_remaining: "25-50%"
    actions:
      - cautious_deployments
      - increased_monitoring
      - prioritize_reliability

  - budget_remaining: "< 25%"
    actions:
      - freeze_non_critical_changes
      - focus_on_reliability_work
      - root_cause_analysis

  - budget_remaining: "< 0%"
    actions:
      - deployment_freeze
      - incident_postmortem
      - reliability_sprint
```

---

## Monitoring & Alerting

### SLI/SLO Monitoring Dashboard

**Key Metrics:**
- Current SLI values (real-time)
- SLO compliance status (% of time within SLO)
- Error budget remaining (% and absolute)
- Error budget burn rate (current vs. allowed)
- Historical trends (7d, 30d, 90d)

**Alert Rules:**
```yaml
alerts:
  - name: SLO Violation
    condition: sli < slo_target
    duration: 5m
    severity: high
    notify: [team-oncall]

  - name: Error Budget Exhausted
    condition: error_budget_remaining < 0
    severity: critical
    notify: [team-lead, engineering-manager]

  - name: High Burn Rate
    condition: burn_rate > 10
    duration: 1h
    severity: critical
    notify: [team-oncall]
```

### Reporting

**Weekly SLO Report:**
```markdown
## SLO Compliance Report - Week of 2025-10-17

### Summary
- Overall Compliance: 99.87% ✅
- Error Budget Remaining: 64% ✅
- Incidents: 2 (1 SLO violation)

### SLI Details
| SLI | Target | Actual | Status |
|-----|--------|--------|--------|
| Availability | 99.9% | 99.95% | ✅ |
| Latency p95 | < 500ms | 487ms | ✅ |
| Latency p99 | < 1000ms | 1234ms | ❌ |
| Error Rate | < 0.1% | 0.08% | ✅ |

### Incidents
1. Database connection pool exhaustion (2025-10-14)
   - Duration: 23 minutes
   - Impact: p99 latency spike to 3000ms
   - Error budget consumed: 15%

### Actions
- Increase DB connection pool size ✅
- Add connection pool monitoring
- Implement circuit breaker for DB calls
```

---

## Implementation Checklist

### Phase 1: Define (Week 1)
- [ ] Identify critical user journeys
- [ ] Select relevant SLIs
- [ ] Set realistic SLO targets
- [ ] Calculate error budgets
- [ ] Document SLA commitments

### Phase 2: Instrument (Week 2)
- [ ] Add metrics collection
- [ ] Implement SLI calculations
- [ ] Set up monitoring dashboards
- [ ] Configure alerting rules
- [ ] Test metric pipelines

### Phase 3: Operationalize (Week 3)
- [ ] Train team on SLO practices
- [ ] Establish incident response
- [ ] Create error budget policy
- [ ] Set up reporting cadence
- [ ] Define escalation paths

### Phase 4: Iterate (Ongoing)
- [ ] Review SLOs quarterly
- [ ] Analyze SLO violations
- [ ] Adjust targets as needed
- [ ] Optimize monitoring
- [ ] Improve reliability
