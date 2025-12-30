# Performance Testing Standards - Extended Reference

This document contains detailed examples, configurations, and templates that extend
the core SKILL.md content. Reference this for production-ready implementations.

## Table of Contents

- [JMeter Complete Test Plan](#jmeter-complete-test-plan)
- [k6 Prometheus Integration](#k6-prometheus-integration)
- [Performance Metrics Definitions](#performance-metrics-definitions)
- [SLI/SLO/SLA Framework](#slislosla-framework)
- [Performance Report Template](#performance-report-template)
- [Network Trace Analysis](#network-trace-analysis)
- [Database Profiling](#database-profiling)
- [Learning Path](#learning-path)
- [Competency Checklist](#competency-checklist)

---

## JMeter Complete Test Plan

```xml
<!-- jmeter-test-plan.jmx -->
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="API Load Test">
      <stringProp name="TestPlan.comments">Performance test for User API</stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>

      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments">
        <collectionProp name="Arguments.arguments">
          <elementProp name="BASE_URL" elementType="Argument">
            <stringProp name="Argument.name">BASE_URL</stringProp>
            <stringProp name="Argument.value">${__P(base_url,https://api.example.com)}</stringProp>
          </elementProp>
          <elementProp name="USERS" elementType="Argument">
            <stringProp name="Argument.name">USERS</stringProp>
            <stringProp name="Argument.value">${__P(users,100)}</stringProp>
          </elementProp>
        </collectionProp>
      </elementProp>
    </TestPlan>

    <hashTree>
      <!-- Thread Group -->
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="User Load">
        <stringProp name="ThreadGroup.num_threads">${USERS}</stringProp>
        <stringProp name="ThreadGroup.ramp_time">120</stringProp>
        <stringProp name="ThreadGroup.duration">600</stringProp>
        <boolProp name="ThreadGroup.scheduler">true</boolProp>
      </ThreadGroup>

      <hashTree>
        <!-- HTTP Request Defaults -->
        <ConfigTestElement guiclass="HttpDefaultsGui" testclass="ConfigTestElement">
          <stringProp name="HTTPSampler.domain">${BASE_URL}</stringProp>
          <stringProp name="HTTPSampler.protocol">https</stringProp>
          <stringProp name="HTTPSampler.connect_timeout">10000</stringProp>
          <stringProp name="HTTPSampler.response_timeout">30000</stringProp>
        </ConfigTestElement>

        <!-- HTTP Header Manager -->
        <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager">
          <collectionProp name="HeaderManager.headers">
            <elementProp name="" elementType="Header">
              <stringProp name="Header.name">Content-Type</stringProp>
              <stringProp name="Header.value">application/json</stringProp>
            </elementProp>
          </collectionProp>
        </HeaderManager>

        <!-- HTTP Requests -->
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="Get User Profile">
          <stringProp name="HTTPSampler.path">/api/user/profile</stringProp>
          <stringProp name="HTTPSampler.method">GET</stringProp>
        </HTTPSamplerProxy>

        <!-- Response Assertions -->
        <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion">
          <collectionProp name="Asserion.test_strings">
            <stringProp name="49586">200</stringProp>
          </collectionProp>
          <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
        </ResponseAssertion>

        <!-- Duration Assertion -->
        <DurationAssertion guiclass="DurationAssertionGui" testclass="DurationAssertion">
          <stringProp name="DurationAssertion.duration">500</stringProp>
        </DurationAssertion>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

---

## k6 Prometheus Integration

```javascript
// k6-prometheus.js
import http from 'k6/http';
import { check } from 'k6';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';

export const options = {
  stages: [
    { duration: '5m', target: 100 },
    { duration: '10m', target: 100 },
    { duration: '5m', target: 0 },
  ],
  ext: {
    loadimpact: {
      projectID: 123456,
      name: 'API Load Test',
    },
  },
};

export default function () {
  const res = http.get('https://api.example.com/endpoint');
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
}

export function handleSummary(data) {
  const prometheusMetrics = generatePrometheusMetrics(data);
  return {
    'stdout': textSummary(data, { indent: ' ', enableColors: true }),
    'prometheus.txt': prometheusMetrics,
  };
}

function generatePrometheusMetrics(data) {
  let output = '';

  // Request duration
  output += `# HELP http_req_duration HTTP request duration\n`;
  output += `# TYPE http_req_duration summary\n`;
  output += `http_req_duration{quantile="0.5"} ${data.metrics.http_req_duration.values['p(50)']}\n`;
  output += `http_req_duration{quantile="0.95"} ${data.metrics.http_req_duration.values['p(95)']}\n`;
  output += `http_req_duration{quantile="0.99"} ${data.metrics.http_req_duration.values['p(99)']}\n`;

  // Request rate
  output += `# HELP http_reqs_total Total HTTP requests\n`;
  output += `# TYPE http_reqs_total counter\n`;
  output += `http_reqs_total ${data.metrics.http_reqs.values.count}\n`;

  // Error rate
  output += `# HELP http_req_failed HTTP request failure rate\n`;
  output += `# TYPE http_req_failed gauge\n`;
  output += `http_req_failed ${data.metrics.http_req_failed.values.rate}\n`;

  return output;
}
```

---

## Performance Metrics Definitions

```javascript
// performance-metrics.js
export const PerformanceMetrics = {
  // Latency metrics (in milliseconds)
  latency: {
    p50: 'Median response time - 50% of requests',
    p90: '90th percentile - 90% of requests faster than this',
    p95: '95th percentile - SLO threshold',
    p99: '99th percentile - Worst-case for most users',
    p99_9: '99.9th percentile - Absolute worst-case',
  },

  // Throughput metrics
  throughput: {
    rps: 'Requests per second',
    tps: 'Transactions per second',
    data_transfer: 'MB/s transferred',
  },

  // Error metrics
  errors: {
    error_rate: 'Failed requests / Total requests',
    timeout_rate: 'Timed out requests / Total requests',
    error_types: 'Breakdown by HTTP status code',
  },

  // Resource utilization
  resources: {
    cpu_usage: 'Percentage of CPU capacity',
    memory_usage: 'Percentage of memory capacity',
    disk_io: 'Read/write operations per second',
    network_bandwidth: 'MB/s network throughput',
  },

  // Application-specific metrics
  application: {
    db_query_time: 'Database query duration',
    cache_hit_rate: 'Cache hits / Total cache requests',
    queue_depth: 'Number of items in processing queue',
    connection_pool: 'Active database connections',
  },
};
```

---

## SLI/SLO/SLA Framework

```yaml
# slo-definitions.yaml
service: user-api
version: 1.0.0

# Service Level Indicators (What we measure)
slis:
  - name: availability
    description: "Percentage of successful requests"
    query: "sum(rate(http_requests_total{status=~'2..'}[5m])) / sum(rate(http_requests_total[5m]))"

  - name: latency_p95
    description: "95th percentile response time"
    query: "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"

  - name: error_rate
    description: "Percentage of failed requests"
    query: "sum(rate(http_requests_total{status=~'5..'}[5m])) / sum(rate(http_requests_total[5m]))"

# Service Level Objectives (Targets we aim for)
slos:
  - sli: availability
    target: 99.9
    unit: percent
    window: 30d

  - sli: latency_p95
    target: 500
    unit: milliseconds
    window: 30d

  - sli: error_rate
    target: 0.1
    unit: percent
    window: 30d

# Service Level Agreements (Contractual commitments)
slas:
  - name: "Gold Tier SLA"
    availability: 99.95
    latency_p95: 300
    support_response: 1h
    credits: "10% monthly fee per 0.1% below SLA"

  - name: "Silver Tier SLA"
    availability: 99.9
    latency_p95: 500
    support_response: 4h
    credits: "5% monthly fee per 0.5% below SLA"

# Error Budget
error_budget:
  calculation: "(1 - SLO_target) * total_requests"
  availability_budget: 43.2m  # 99.9% uptime = 43.2 min downtime/month
  burn_rate_alert: 10x         # Alert if burning budget 10x faster
```

---

## Performance Report Template

```markdown
# Performance Test Report

**Test Date:** YYYY-MM-DD
**Environment:** Staging/Production
**Test Duration:** X minutes
**Peak Load:** X concurrent users

## Executive Summary

- [ ] System handled target load successfully
- [ ] p95 latency within SLO
- [ ] No memory leaks detected
- [ ] Error rate below threshold

## Test Results

### Load Test Results

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| p50 Latency | < 100ms | Xms | PASS/FAIL |
| p95 Latency | < 500ms | Xms | PASS/FAIL |
| p99 Latency | < 1000ms | Xms | PASS/FAIL |
| Throughput | > 1000 RPS | X RPS | PASS/FAIL |
| Error Rate | < 0.1% | X% | PASS/FAIL |
| CPU Usage | < 80% | X% | PASS/FAIL |
| Memory Usage | < 85% | X% | PASS/FAIL |

### Latency Distribution

```
p50:  Xms  ████████████████░░░░░░░░░░░░░░░░░░░░ (50%)
p75:  Xms  ████████████████████████░░░░░░░░░░░░ (75%)
p90:  Xms  ████████████████████████████████░░░░ (90%)
p95:  Xms  ████████████████████████████████████ (95%)
p99:  Xms  ████████████████████████████████████ (99%)
```

## Bottlenecks Identified

1. **Issue Name**
   - Symptom: Description of observed behavior
   - Root cause: Analysis of underlying problem
   - Recommendation: Suggested remediation

## Recommendations

### Immediate (P0)
- [ ] Critical fix 1
- [ ] Critical fix 2

### Short-term (P1)
- [ ] Optimization 1
- [ ] Optimization 2

### Long-term (P2)
- [ ] Strategic improvement 1
- [ ] Strategic improvement 2

## Appendices

- [Grafana Dashboard](link)
- [Raw k6 Results](./results/k6-results.json)
- [Flame Graph](./results/flamegraph.svg)
```

---

## Network Trace Analysis

```bash
# Capture network traces during load test
tcpdump -i any -w performance-test.pcap port 8080

# Analyze with tshark
tshark -r performance-test.pcap -Y "http" -T fields \
  -e frame.time_relative \
  -e ip.src \
  -e ip.dst \
  -e http.request.method \
  -e http.response.code \
  -e http.time

# Visualize with Wireshark
wireshark performance-test.pcap
```

---

## Database Profiling

### PostgreSQL

```sql
-- Enable query logging
ALTER DATABASE mydb SET log_min_duration_statement = 100; -- Log queries > 100ms

-- Identify slow queries
SELECT
  query,
  calls,
  total_time,
  mean_time,
  max_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 20;

-- Check for missing indexes
SELECT
  schemaname,
  tablename,
  attname,
  n_live_tup,
  idx_scan
FROM pg_stat_user_tables t
JOIN pg_stats s ON t.tablename = s.tablename
WHERE idx_scan = 0 AND n_live_tup > 10000;
```

### MySQL

```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 0.1; -- 100ms threshold

-- Analyze slow queries
SELECT * FROM mysql.slow_log
ORDER BY query_time DESC
LIMIT 20;

-- Check query execution plan
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

---

## CI/CD Integration - Extended

### PR Comment Integration

```yaml
- name: Comment on PR
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v6
  with:
    script: |
      const p95 = '${{ steps.results.outputs.p95_latency }}';
      const errorRate = '${{ steps.results.outputs.error_rate }}';
      const status = '${{ steps.results.outputs.threshold_status }}';

      const body = `## Performance Test Results

      **Status:** ${status === 'passed' ? 'PASSED' : 'FAILED'}

      | Metric | Value | Threshold | Status |
      |--------|-------|-----------|--------|
      | p95 Latency | ${p95}ms | < 500ms | ${p95 < 500 ? 'PASS' : 'FAIL'} |
      | Error Rate | ${(errorRate * 100).toFixed(2)}% | < 1% | ${errorRate < 0.01 ? 'PASS' : 'FAIL'} |
      `;

      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: body
      });
```

### Slack Notification

```yaml
- name: Send Slack Notification
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Performance test failed!",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Performance Test Failed*\n\nWorkflow: ${{ github.workflow }}\nRun: ${{ github.run_id }}"
            }
          }
        ]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## Learning Path

### Week 1-2: Fundamentals

- Study performance testing types and metrics
- Set up k6 and run basic load tests
- Learn to interpret latency percentiles

### Week 3-4: Implementation

- Create realistic test scenarios
- Implement custom metrics and thresholds
- Integrate with monitoring tools (Prometheus/Grafana)

### Week 5-6: Analysis & Optimization

- Profile application bottlenecks
- Optimize database queries
- Implement caching strategies

### Week 7-8: CI/CD & Production

- Automate performance testing in CI/CD
- Set up SLI/SLO monitoring
- Create alerting and incident response plans

---

## Competency Checklist

By completing this skill, you should be able to:

- [ ] Design performance test scenarios for different load patterns
- [ ] Implement load tests using k6 and JMeter
- [ ] Define and measure SLIs, SLOs, and SLAs
- [ ] Analyze latency distributions and identify outliers
- [ ] Integrate performance testing into CI/CD pipelines
- [ ] Profile applications to identify bottlenecks
- [ ] Optimize database queries and connection pools
- [ ] Set up APM monitoring and alerting
- [ ] Generate performance reports with actionable recommendations
- [ ] Implement graceful degradation and circuit breakers

---

## Common Pitfalls

### Pitfall 1: Testing in Unrealistic Environments

**Problem:** Test environment doesn't match production configuration

**Solution:**
- Use production-like data volumes
- Match hardware/resource allocation
- Simulate realistic network latency

### Pitfall 2: Ignoring Warm-up Period

**Problem:** Measuring performance before JIT compilation and cache warming

**Solution:**
- Include warm-up phase in test design
- Exclude warm-up metrics from analysis
- Allow connection pools to initialize

### Pitfall 3: Single-Metric Focus

**Problem:** Only looking at average latency, missing tail latency issues

**Solution:**
- Always measure p95, p99, p99.9 percentiles
- Track error rate alongside latency
- Monitor resource utilization during tests

### Pitfall 4: Not Testing Failure Modes

**Problem:** Only testing happy path, missing resilience issues

**Solution:**
- Include chaos engineering scenarios
- Test with partial service degradation
- Validate circuit breaker behavior

---

## Additional Resources

### Books

- "The Art of Application Performance Testing" by Ian Molyneaux
- "Web Performance in Action" by Jeremy Wagner
- "High Performance Browser Networking" by Ilya Grigorik

### Online Courses

- [Google's Web Performance Optimization Course](https://developers.google.com/web/fundamentals/performance)
- [k6 Learn](https://k6.io/docs/examples/)

### Community Resources

- [Performance Testing Guidance for Web Applications (Microsoft)](https://docs.microsoft.com/en-us/previous-versions/msp-n-p/bb924375(v=pandp.10))
- [Web Performance Working Group (W3C)](https://www.w3.org/webperf/)
- [k6 Community Forum](https://community.k6.io/)

---

**Last Updated:** 2025-10-17
**Version:** 2.0.0
**Maintainer:** Testing Standards Team
