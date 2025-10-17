// k6-load-test.js - Production-ready k6 load testing script
import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Rate, Trend, Counter, Gauge } from 'k6/metrics';
import { htmlReport } from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';

// Custom metrics
const errorRate = new Rate('errors');
const successRate = new Rate('success');
const customDuration = new Trend('custom_request_duration');
const activeUsers = new Gauge('active_users');
const apiCallCount = new Counter('api_calls');

// Configuration
export const options = {
  // Load test stages
  stages: [
    { duration: '2m', target: 50 },    // Warm-up: ramp to 50 users
    { duration: '5m', target: 50 },    // Baseline: maintain 50 users
    { duration: '2m', target: 100 },   // Ramp-up: increase to 100 users
    { duration: '5m', target: 100 },   // Plateau: maintain 100 users
    { duration: '2m', target: 200 },   // Peak: increase to 200 users
    { duration: '5m', target: 200 },   // Peak hold: maintain 200 users
    { duration: '5m', target: 0 },     // Ramp-down: graceful shutdown
  ],

  // Thresholds - Define pass/fail criteria
  thresholds: {
    // Overall HTTP metrics
    'http_req_duration': [
      'p(50)<100',   // 50% of requests must complete below 100ms
      'p(95)<500',   // 95% of requests must complete below 500ms
      'p(99)<1000',  // 99% of requests must complete below 1000ms
    ],
    'http_req_failed': ['rate<0.01'], // Error rate must be less than 1%
    'http_reqs': ['rate>100'],         // Must achieve >100 RPS

    // Endpoint-specific thresholds using tags
    'http_req_duration{endpoint:health}': ['p(95)<50'],
    'http_req_duration{endpoint:api}': ['p(95)<500'],
    'http_req_duration{endpoint:dashboard}': ['p(95)<800'],

    // Custom metric thresholds
    'errors': ['rate<0.01'],
    'success': ['rate>0.99'],
    'custom_request_duration': ['p(95)<600'],

    // Group-specific thresholds
    'group_duration{group:::User Authentication}': ['p(95)<800'],
    'group_duration{group:::Dashboard Operations}': ['p(95)<1000'],
    'group_duration{group:::Data Processing}': ['p(95)<1500'],
  },

  // HTTP-specific options
  http: {
    timeout: '30s',
  },

  // Graceful shutdown
  gracefulStop: '30s',
  gracefulRampDown: '10s',

  // Detailed summary statistics
  summaryTrendStats: ['min', 'avg', 'med', 'p(90)', 'p(95)', 'p(99)', 'p(99.9)', 'max'],
  
  // Output results to multiple formats
  noConnectionReuse: false,
  userAgent: 'k6-load-test/1.0',
};

// Environment variables
const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';
const API_TOKEN = __ENV.API_TOKEN || '';
const TEST_DURATION = __ENV.TEST_DURATION || '26m';

// Test data
const testUsers = [
  { username: 'user1@example.com', password: 'password123' },
  { username: 'user2@example.com', password: 'password456' },
  { username: 'user3@example.com', password: 'password789' },
];

// Setup function - runs once before test
export function setup() {
  console.log(`Starting load test against ${BASE_URL}`);
  console.log(`Test duration: ${TEST_DURATION}`);
  console.log(`Virtual users: ${options.stages.map(s => s.target).join(' → ')}`);
  
  // Authenticate and get token (if needed)
  const loginRes = http.post(`${BASE_URL}/auth/login`, JSON.stringify({
    username: 'load-test-user',
    password: 'load-test-password',
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  let authToken = API_TOKEN;
  if (loginRes.status === 200) {
    authToken = loginRes.json('token') || API_TOKEN;
  }

  return {
    authToken: authToken,
    testStartTime: new Date().toISOString(),
    baseUrl: BASE_URL,
  };
}

// Main test scenario
export default function (data) {
  // Update active users gauge
  activeUsers.add(1);

  // Common request parameters
  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${data.authToken}`,
      'X-Test-Run-Id': `load-test-${__VU}-${__ITER}`,
    },
    tags: {
      test_type: 'load',
      environment: 'staging',
    },
  };

  // Scenario 1: Health check
  group('Health Check', () => {
    const res = http.get(`${data.baseUrl}/health`, {
      ...params,
      tags: { ...params.tags, endpoint: 'health' },
    });

    const success = check(res, {
      'health check status is 200': (r) => r.status === 200,
      'health check response time < 50ms': (r) => r.timings.duration < 50,
    });

    errorRate.add(!success);
    successRate.add(success);
    apiCallCount.add(1);
  });

  sleep(1);

  // Scenario 2: User authentication
  group('User Authentication', () => {
    const startTime = new Date();
    const user = testUsers[__VU % testUsers.length];

    const loginRes = http.post(
      `${data.baseUrl}/auth/login`,
      JSON.stringify(user),
      {
        ...params,
        tags: { ...params.tags, endpoint: 'api', operation: 'login' },
      }
    );

    const loginSuccess = check(loginRes, {
      'login status is 200': (r) => r.status === 200,
      'login has token': (r) => r.json('token') !== undefined,
      'login response time < 500ms': (r) => r.timings.duration < 500,
    });

    errorRate.add(!loginSuccess);
    successRate.add(loginSuccess);
    customDuration.add(new Date() - startTime);
    apiCallCount.add(1);

    // Extract token for subsequent requests
    if (loginSuccess && loginRes.json('token')) {
      params.headers.Authorization = `Bearer ${loginRes.json('token')}`;
    }
  });

  sleep(2);

  // Scenario 3: Dashboard data fetch (parallel requests)
  group('Dashboard Operations', () => {
    const responses = http.batch([
      ['GET', `${data.baseUrl}/api/dashboard/summary`, null, {
        ...params,
        tags: { ...params.tags, endpoint: 'dashboard', operation: 'summary' },
      }],
      ['GET', `${data.baseUrl}/api/notifications`, null, {
        ...params,
        tags: { ...params.tags, endpoint: 'api', operation: 'notifications' },
      }],
      ['GET', `${data.baseUrl}/api/user/profile`, null, {
        ...params,
        tags: { ...params.tags, endpoint: 'api', operation: 'profile' },
      }],
      ['GET', `${data.baseUrl}/api/settings`, null, {
        ...params,
        tags: { ...params.tags, endpoint: 'api', operation: 'settings' },
      }],
    ]);

    let allSuccess = true;
    responses.forEach((res, index) => {
      const success = check(res, {
        [`batch[${index}] status is 200`]: (r) => r.status === 200,
        [`batch[${index}] response time < 500ms`]: (r) => r.timings.duration < 500,
      });
      
      if (!success) allSuccess = false;
      apiCallCount.add(1);
    });

    errorRate.add(!allSuccess);
    successRate.add(allSuccess);
  });

  sleep(1);

  // Scenario 4: Data processing (POST request)
  group('Data Processing', () => {
    const payload = JSON.stringify({
      transactionId: `txn-${__VU}-${__ITER}-${Date.now()}`,
      amount: 100.00 + Math.random() * 900,
      currency: 'USD',
      type: 'payment',
      metadata: {
        userId: __VU,
        iteration: __ITER,
        timestamp: new Date().toISOString(),
      },
    });

    const processRes = http.post(
      `${data.baseUrl}/api/transactions`,
      payload,
      {
        ...params,
        tags: { ...params.tags, endpoint: 'api', operation: 'process_transaction' },
      }
    );

    const processSuccess = check(processRes, {
      'process status is 201': (r) => r.status === 201,
      'process returned transaction ID': (r) => r.json('transactionId') !== undefined,
      'process response time < 1000ms': (r) => r.timings.duration < 1000,
    });

    errorRate.add(!processSuccess);
    successRate.add(processSuccess);
    apiCallCount.add(1);

    // If processing succeeded, verify the transaction
    if (processSuccess && processRes.json('transactionId')) {
      const txnId = processRes.json('transactionId');
      
      sleep(0.5);

      const verifyRes = http.get(
        `${data.baseUrl}/api/transactions/${txnId}`,
        {
          ...params,
          tags: { ...params.tags, endpoint: 'api', operation: 'verify_transaction' },
        }
      );

      const verifySuccess = check(verifyRes, {
        'verify status is 200': (r) => r.status === 200,
        'verify transaction matches': (r) => r.json('transactionId') === txnId,
      });

      errorRate.add(!verifySuccess);
      successRate.add(verifySuccess);
      apiCallCount.add(1);
    }
  });

  sleep(2);

  // Scenario 5: Search operation (with query parameters)
  group('Search Operations', () => {
    const searchQueries = ['payment', 'refund', 'pending', 'completed', 'failed'];
    const query = searchQueries[Math.floor(Math.random() * searchQueries.length)];

    const searchRes = http.get(
      `${data.baseUrl}/api/search?q=${query}&limit=50&offset=0`,
      {
        ...params,
        tags: { ...params.tags, endpoint: 'api', operation: 'search' },
      }
    );

    const searchSuccess = check(searchRes, {
      'search status is 200': (r) => r.status === 200,
      'search returned results': (r) => r.json('results') !== undefined,
      'search response time < 800ms': (r) => r.timings.duration < 800,
    });

    errorRate.add(!searchSuccess);
    successRate.add(searchSuccess);
    apiCallCount.add(1);
  });

  sleep(1);

  // Random think time to simulate real user behavior
  sleep(Math.random() * 3);
}

// Teardown function - runs once after test
export function teardown(data) {
  console.log(`Load test completed at ${new Date().toISOString()}`);
  console.log(`Test started at ${data.testStartTime}`);
  console.log(`Total test duration: ${TEST_DURATION}`);
}

// Custom summary handler
export function handleSummary(data) {
  console.log('Generating test reports...');

  return {
    'stdout': textSummary(data, { indent: ' ', enableColors: true }),
    'summary.html': htmlReport(data),
    'summary.json': JSON.stringify(data, null, 2),
    'summary.txt': textSummary(data, { indent: ' ', enableColors: false }),
  };
}
