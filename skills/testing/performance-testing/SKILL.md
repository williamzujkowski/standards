---
name: performance-testing-standards
category: testing
difficulty: intermediate
tags:
- performance
- load-testing
- stress-testing
- k6
- jmeter
- monitoring
prerequisites:
- api-testing-standards
- monitoring-observability-standards
related_skills:
- security-testing-standards
- ci-cd-pipeline-standards
estimated_time: 45 minutes
last_updated: '2025-10-17'
applies_to:
- backend
- frontend
- api
- microservices
- data-pipelines
description: 'Performance Test Types:'
---


# Performance Testing Standards

## 📋 Metadata

**Category:** Testing
**Difficulty:** Intermediate
**Prerequisites:** API testing basics, monitoring fundamentals
**Estimated Time:** 45 minutes
**Last Updated:** 2025-10-17

---

## 🎯 Level 1: Quick Reference

### Core Concepts

**Performance Test Types:**

1. **Load Testing**: Validate system behavior under expected load
2. **Stress Testing**: Find breaking point and failure modes
3. **Spike Testing**: Validate sudden traffic surge handling
4. **Soak Testing**: Verify stability under sustained load (memory leaks, resource exhaustion)
5. **Breakpoint Testing**: Incrementally increase load to find capacity limits

**Key Metrics:**

- **Latency Percentiles**: p50 (median), p95, p99, p99.9
- **Throughput**: Requests per second (RPS), transactions per second (TPS)
- **Error Rate**: Percentage of failed requests
- **Concurrent Users**: Virtual users (VUs) active simultaneously
- **Resource Utilization**: CPU, memory, disk I/O, network bandwidth

**Critical Success Indicators:**

- p95 latency < SLO threshold
- Error rate < 0.1%
- System stability during sustained load
- Graceful degradation under stress
- Recovery after traffic spikes

### Essential Checklist

**Before Testing:**

```
☐ Define SLIs/SLOs (Service Level Indicators/Objectives)
☐ Identify critical user journeys
☐ Set up monitoring (APM, metrics, logs)
☐ Establish baseline performance
☐ Configure realistic test scenarios
☐ Prepare production-like test environment
```

**During Testing:**

```
☐ Monitor system resources in real-time
☐ Track error logs and exceptions
☐ Validate data integrity
☐ Capture network traces for bottlenecks
☐ Document anomalies and failures
```

**After Testing:**

```
☐ Analyze latency distributions
☐ Identify performance bottlenecks
☐ Compare against SLOs
☐ Generate executive summary
☐ Create remediation plan
☐ Update capacity planning docs
```

### Quick Start: k6 Load Test

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Ramp-up
    { duration: '5m', target: 50 },   // Steady state
    { duration: '2m', target: 0 },    // Ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% < 500ms
    http_req_failed: ['rate<0.01'],   // Error rate < 1%
  },
};

export default function () {
  const res = http.get('https://api.example.com/health');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

**Run:**

```bash
k6 run load-test.js
```

### Quick Metrics Reference

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| p50 latency | < 100ms | 100-200ms | > 200ms |
| p95 latency | < 500ms | 500-1000ms | > 1000ms |
| p99 latency | < 1s | 1-2s | > 2s |
| Error rate | < 0.1% | 0.1-1% | > 1% |
| CPU usage | < 60% | 60-80% | > 80% |
| Memory usage | < 70% | 70-85% | > 85% |

---

## 🔧 Level 2: Implementation Guide

### 1. Test Strategy & Planning

#### Define Performance Requirements

**Service Level Indicators (SLIs):**

```yaml
# performance-requirements.yaml
service: user-api
environment: production

slis:
  availability:
    target: 99.9%
    measurement: successful_requests / total_requests

  latency:
    p50: 100ms
    p95: 500ms
    p99: 1000ms
    measurement: response time at percentile

  throughput:
    target: 1000 rps
    measurement: requests per second

  error_rate:
    target: 0.1%
    measurement: failed_requests / total_requests

critical_user_journeys:
  - name: user_login
    weight: 30%
    slo_p95: 300ms

  - name: fetch_dashboard
    weight: 40%
    slo_p95: 500ms

  - name: submit_transaction
    weight: 20%
    slo_p95: 1000ms

  - name: search_products
    weight: 10%
    slo_p95: 400ms
```

#### Test Scenario Design

**Load Profile Patterns:**

```javascript
// 1. Ramp-Up Pattern (Gradual Load Increase)
export const rampUpOptions = {
  stages: [
    { duration: '5m', target: 100 },   // Ramp to 100 users
    { duration: '10m', target: 100 },  // Hold at 100
    { duration: '5m', target: 200 },   // Ramp to 200
    { duration: '10m', target: 200 },  // Hold at 200
    { duration: '5m', target: 0 },     // Ramp down
  ],
};

// 2. Stress Test Pattern (Beyond Normal Capacity)
export const stressOptions = {
  stages: [
    { duration: '2m', target: 200 },   // Fast ramp-up
    { duration: '5m', target: 200 },   // Stay at 200
    { duration: '2m', target: 400 },   // Push to 400
    { duration: '5m', target: 400 },   // Hold at 400
    { duration: '10m', target: 0 },    // Long ramp-down
  ],
};

// 3. Spike Test Pattern (Sudden Traffic Surge)
export const spikeOptions = {
  stages: [
    { duration: '1m', target: 50 },    // Baseline
    { duration: '10s', target: 500 },  // Sudden spike
    { duration: '3m', target: 500 },   // Hold spike
    { duration: '10s', target: 50 },   // Drop back
    { duration: '3m', target: 50 },    // Recovery
    { duration: '10s', target: 0 },    // End
  ],
};

// 4. Soak Test Pattern (Sustained Load)
export const soakOptions = {
  stages: [
    { duration: '5m', target: 100 },   // Ramp-up
    { duration: '4h', target: 100 },   // Soak for 4 hours
    { duration: '5m', target: 0 },     // Ramp-down
  ],
};
```

### 2. k6 Implementation

#### Advanced k6 Test Structure

```javascript
// advanced-load-test.js
import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';
import { htmlReport } from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js';

// Custom metrics
const errorRate = new Rate('errors');
const customTrend = new Trend('custom_duration');
const requestCount = new Counter('request_count');

// Test configuration
export const options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 200 },
    { duration: '5m', target: 200 },
    { duration: '2m', target: 0 },
  ],

  thresholds: {
    // HTTP-specific thresholds
    'http_req_duration': ['p(95)<500', 'p(99)<1000'],
    'http_req_duration{type:api}': ['p(95)<300'],
    'http_req_duration{type:static}': ['p(95)<100'],
    'http_req_failed': ['rate<0.01'],

    // Custom metric thresholds
    'errors': ['rate<0.01'],
    'custom_duration': ['p(95)<400'],

    // Group-specific thresholds
    'group_duration{group:::Login Flow}': ['p(95)<800'],
    'group_duration{group:::Dashboard Load}': ['p(95)<600'],
  },

  // Graceful stop configuration
  gracefulStop: '30s',

  // Disable default summary
  summaryTrendStats: ['min', 'med', 'avg', 'p(90)', 'p(95)', 'p(99)', 'max'],
};

// Test data
const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';
const users = JSON.parse(open('./data/test-users.json'));

// Setup function (runs once)
export function setup() {
  // Authenticate and get token
  const loginRes = http.post(`${BASE_URL}/auth/login`, {
    username: 'test-user',
    password: 'test-password',
  });

  return {
    token: loginRes.json('token'),
    timestamp: new Date().toISOString(),
  };
}

// Main test scenario
export default function (data) {
  const params = {
    headers: {
      'Authorization': `Bearer ${data.token}`,
      'Content-Type': 'application/json',
    },
    tags: { type: 'api' },
  };

  // User login flow
  group('Login Flow', () => {
    const loginStart = new Date();
    const res = http.get(`${BASE_URL}/api/user/profile`, params);

    const success = check(res, {
      'login status is 200': (r) => r.status === 200,
      'response has user data': (r) => r.json('id') !== undefined,
    });

    errorRate.add(!success);
    customTrend.add(new Date() - loginStart);
    requestCount.add(1);
  });

  sleep(1);

  // Dashboard load flow
  group('Dashboard Load', () => {
    const responses = http.batch([
      ['GET', `${BASE_URL}/api/dashboard/summary`, null, params],
      ['GET', `${BASE_URL}/api/notifications`, null, params],
      ['GET', `${BASE_URL}/api/user/settings`, null, params],
    ]);

    responses.forEach((res) => {
      check(res, {
        'dashboard status is 200': (r) => r.status === 200,
      });
    });
  });

  sleep(2);

  // Transaction submission
  group('Submit Transaction', () => {
    const payload = JSON.stringify({
      amount: 100.00,
      currency: 'USD',
      description: `Test transaction ${__VU}-${__ITER}`,
    });

    const res = http.post(`${BASE_URL}/api/transactions`, payload, params);

    check(res, {
      'transaction created': (r) => r.status === 201,
      'transaction ID returned': (r) => r.json('transactionId') !== undefined,
    });
  });

  sleep(1);
}

// Teardown function (runs once)
export function teardown(data) {
  console.log(`Test completed at ${new Date().toISOString()}`);
  console.log(`Test started at ${data.timestamp}`);
}

// Custom HTML report generation
export function handleSummary(data) {
  return {
    'summary.html': htmlReport(data),
    'summary.json': JSON.stringify(data),
  };
}
```

#### k6 with Prometheus Integration

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

  // Send metrics to Prometheus via remote write
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
  // Export metrics for Prometheus
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

### 3. JMeter Implementation

#### JMeter Test Plan Structure

```xml
<!-- jmeter-test-plan.jmx (simplified) -->
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

**Run JMeter from CLI:**

```bash
# Run test plan
jmeter -n -t test-plan.jmx \
  -Jbase_url=https://api.example.com \
  -Jusers=200 \
  -l results.jtl \
  -e -o report/

# Generate HTML report from existing results
jmeter -g results.jtl -o report/
```

### 4. Metrics & Monitoring

#### Key Performance Indicators

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

#### SLI/SLO/SLA Framework

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

### 5. CI/CD Integration

#### GitHub Actions Performance Testing

```yaml
# .github/workflows/performance-test.yml
name: Performance Testing

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:
    inputs:
      duration:
        description: 'Test duration (minutes)'
        required: false
        default: '10'
      vus:
        description: 'Virtual users'
        required: false
        default: '100'

jobs:
  performance-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Install k6
        run: |
          sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
          echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
          sudo apt-get update
          sudo apt-get install k6

      - name: Run Load Test
        env:
          BASE_URL: ${{ secrets.PERF_TEST_URL }}
          DURATION: ${{ github.event.inputs.duration || '10' }}
          VUS: ${{ github.event.inputs.vus || '100' }}
        run: |
          k6 run \
            --out json=results.json \
            --summary-export=summary.json \
            tests/performance/load-test.js

      - name: Parse Results
        id: results
        run: |
          p95=$(jq -r '.metrics.http_req_duration.values["p(95)"]' summary.json)
          error_rate=$(jq -r '.metrics.http_req_failed.values.rate' summary.json)

          echo "p95_latency=$p95" >> $GITHUB_OUTPUT
          echo "error_rate=$error_rate" >> $GITHUB_OUTPUT

          # Check thresholds
          if (( $(echo "$p95 > 500" | bc -l) )); then
            echo "threshold_status=failed" >> $GITHUB_OUTPUT
            exit 1
          fi

          if (( $(echo "$error_rate > 0.01" | bc -l) )); then
            echo "threshold_status=failed" >> $GITHUB_OUTPUT
            exit 1
          fi

          echo "threshold_status=passed" >> $GITHUB_OUTPUT

      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: performance-results
          path: |
            results.json
            summary.json
            summary.html

      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const p95 = '${{ steps.results.outputs.p95_latency }}';
            const errorRate = '${{ steps.results.outputs.error_rate }}';
            const status = '${{ steps.results.outputs.threshold_status }}';

            const body = `## Performance Test Results

            **Status:** ${status === 'passed' ? '✅ PASSED' : '❌ FAILED'}

            | Metric | Value | Threshold | Status |
            |--------|-------|-----------|--------|
            | p95 Latency | ${p95}ms | < 500ms | ${p95 < 500 ? '✅' : '❌'} |
            | Error Rate | ${(errorRate * 100).toFixed(2)}% | < 1% | ${errorRate < 0.01 ? '✅' : '❌'} |
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });

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
                    "text": ":warning: *Performance Test Failed*\n\nWorkflow: ${{ github.workflow }}\nRun: ${{ github.run_id }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### 6. Profiling & Bottleneck Analysis

#### Application Profiling

```bash
# Node.js profiling with clinic.js
npm install -g clinic

# Flame graph (CPU profiling)
clinic flame -- node server.js
# Load test the app
clinic flame --visualize

# Bubbleprof (async operations)
clinic bubbleprof -- node server.js
# Load test the app
clinic bubbleprof --visualize

# Doctor (event loop monitoring)
clinic doctor -- node server.js
# Load test the app
clinic doctor --visualize
```

#### Database Query Profiling

```sql
-- PostgreSQL: Enable query logging
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

-- MySQL: Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 0.1; -- 100ms threshold

-- Analyze slow queries
SELECT * FROM mysql.slow_log
ORDER BY query_time DESC
LIMIT 20;
```

#### Network Trace Analysis

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

### 7. Results Analysis & Reporting

#### Performance Report Template

```markdown
# Performance Test Report

**Test Date:** 2025-10-17
**Environment:** Staging
**Test Duration:** 30 minutes
**Peak Load:** 500 concurrent users

## Executive Summary

- ✅ System handled target load successfully
- ⚠️  p95 latency exceeded SLO by 15% during peak
- ❌ Memory leak detected during soak test
- ✅ Error rate remained below 0.1%

## Test Results

### Load Test Results

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| p50 Latency | < 100ms | 87ms | ✅ PASS |
| p95 Latency | < 500ms | 574ms | ❌ FAIL |
| p99 Latency | < 1000ms | 1247ms | ❌ FAIL |
| Throughput | > 1000 RPS | 1342 RPS | ✅ PASS |
| Error Rate | < 0.1% | 0.08% | ✅ PASS |
| CPU Usage | < 80% | 72% | ✅ PASS |
| Memory Usage | < 85% | 91% | ❌ FAIL |

### Latency Distribution

```

p50:  87ms  ████████████████░░░░░░░░░░░░░░░░░░░░ (43%)
p75:  234ms ████████████████████████████░░░░░░░░ (70%)
p90:  412ms ████████████████████████████████████░ (90%)
p95:  574ms ████████████████████████████████████▓ (95%)
p99:  1247ms████████████████████████████████████▓ (99%)

```

## Bottlenecks Identified

1. **Database Connection Pool Exhaustion**
   - Symptom: p95 latency spike at 400+ concurrent users
   - Root cause: Connection pool size limited to 50
   - Recommendation: Increase to 200, implement connection pooling retry logic

2. **Memory Leak in User Session Handler**
   - Symptom: Memory usage grows 2% per hour during soak test
   - Root cause: Event listeners not properly cleaned up
   - Recommendation: Implement proper cleanup in session middleware

3. **N+1 Query Problem in Dashboard Endpoint**
   - Symptom: Dashboard load time > 1s at high load
   - Root cause: Fetching related data in loop vs. single query
   - Recommendation: Implement eager loading with JOIN queries

## Recommendations

### Immediate (P0)
- [ ] Fix memory leak in session handler
- [ ] Increase database connection pool size
- [ ] Add connection pool monitoring alerts

### Short-term (P1)
- [ ] Optimize dashboard N+1 queries
- [ ] Implement response caching for static data
- [ ] Add circuit breakers for external API calls

### Long-term (P2)
- [ ] Implement database read replicas
- [ ] Add CDN for static assets
- [ ] Consider horizontal scaling strategy

## Appendices

- [Grafana Dashboard](https://grafana.example.com/d/perf-test-2025-10-17)
- [Raw k6 Results](./results/k6-results.json)
- [Flame Graph](./results/flamegraph.svg)
- [Database Slow Query Log](./results/slow-queries.log)
```

---

## 📚 Level 3: Deep Dive Resources

### Official Documentation

**k6:**

- [k6 Documentation](https://k6.io/docs/)
- [k6 Examples](https://k6.io/docs/examples/)
- [k6 Extensions](https://k6.io/docs/extensions/)

**JMeter:**

- [Apache JMeter User Manual](https://jmeter.apache.org/usermanual/)
- [JMeter Best Practices](https://jmeter.apache.org/usermanual/best-practices.html)
- [JMeter Plugins](https://jmeter-plugins.org/)

**Gatling:**

- [Gatling Documentation](https://gatling.io/docs/)
- [Gatling Scenario DSL](https://gatling.io/docs/gatling/reference/current/core/scenario/)

### Books & Courses

- "The Art of Application Performance Testing" by Ian Molyneaux
- "Web Performance in Action" by Jeremy Wagner
- "High Performance Browser Networking" by Ilya Grigorik
- [Google's Web Performance Optimization Course](https://developers.google.com/web/fundamentals/performance)

### Tools & Services

**Load Testing:**

- [k6](https://k6.io/) - Modern load testing tool
- [Apache JMeter](https://jmeter.apache.org/) - Java-based load testing
- [Gatling](https://gatling.io/) - Scala-based load testing
- [Locust](https://locust.io/) - Python-based load testing
- [Artillery](https://artillery.io/) - Modern performance testing toolkit

**APM & Monitoring:**

- [Prometheus](https://prometheus.io/) + [Grafana](https://grafana.com/)
- [Datadog APM](https://www.datadoghq.com/product/apm/)
- [New Relic](https://newrelic.com/)
- [Dynatrace](https://www.dynatrace.com/)
- [Elastic APM](https://www.elastic.co/apm)

**Profiling:**

- [Clinic.js](https://clinicjs.org/) - Node.js profiling
- [py-spy](https://github.com/benfred/py-spy) - Python profiling
- [pprof](https://github.com/google/pprof) - Go profiling
- [Java Flight Recorder](https://docs.oracle.com/javacomponents/jmc-5-4/jfr-runtime-guide/about.htm)

### Community Resources

- [Performance Testing Guidance for Web Applications (Microsoft)](https://docs.microsoft.com/en-us/previous-versions/msp-n-p/bb924375(v=pandp.10))
- [Web Performance Working Group (W3C)](https://www.w3.org/webperf/)
- [r/webdev Performance Discussions](https://www.reddit.com/r/webdev/)
- [k6 Community Forum](https://community.k6.io/)

### Bundled Resources

This skill includes 6 ready-to-use resources in this directory:

1. **templates/k6-load-test.js** - Production-ready k6 load test script
2. **templates/k6-stress-test.js** - k6 stress testing script
3. **config/jmeter-test-plan.jmx** - JMeter test plan template
4. **templates/grafana-dashboard.json** - Performance monitoring dashboard
5. **scripts/run-perf-tests.sh** - Automated test execution script
6. **resources/performance-checklist.md** - Comprehensive SLI/SLO/SLA guide

---

## 🎓 Learning Path

**Week 1-2:** Fundamentals

- Study performance testing types and metrics
- Set up k6 and run basic load tests
- Learn to interpret latency percentiles

**Week 3-4:** Implementation

- Create realistic test scenarios
- Implement custom metrics and thresholds
- Integrate with monitoring tools (Prometheus/Grafana)

**Week 5-6:** Analysis & Optimization

- Profile application bottlenecks
- Optimize database queries
- Implement caching strategies

**Week 7-8:** CI/CD & Production

- Automate performance testing in CI/CD
- Set up SLI/SLO monitoring
- Create alerting and incident response plans

---

## ✅ Competency Checklist

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

## Examples

### Basic Usage

```python
// TODO: Add basic example for performance-testing
// This example demonstrates core functionality
```

### Advanced Usage

```python
// TODO: Add advanced example for performance-testing
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how performance-testing
// works with other systems and services
```

See `examples/performance-testing/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Common development tools and frameworks
- **Prerequisites**: Basic understanding of general concepts

### Downstream Consumers

- **Applications**: Production systems requiring performance-testing functionality
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

- Follow established patterns and conventions for performance-testing
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

**Last Updated:** 2025-10-17
**Version:** 1.0.0
**Maintainer:** Testing Standards Team
