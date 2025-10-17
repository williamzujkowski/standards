// k6-stress-test.js - Stress testing to find system breaking points
import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const degradationRate = new Rate('degradation');

export const options = {
  // Aggressive stress test stages
  stages: [
    { duration: '2m', target: 100 },   // Baseline
    { duration: '5m', target: 200 },   // Normal load
    { duration: '2m', target: 400 },   // High load
    { duration: '5m', target: 400 },   // Sustain high load
    { duration: '2m', target: 800 },   // Extreme load
    { duration: '5m', target: 800 },   // Sustain extreme load
    { duration: '2m', target: 1200 },  // Breaking point
    { duration: '3m', target: 1200 },  // Sustain breaking point
    { duration: '10m', target: 0 },    // Recovery test
  ],

  // Relaxed thresholds to observe failure modes
  thresholds: {
    'http_req_duration': ['p(99)<5000'], // Allow up to 5s
    'http_req_failed': ['rate<0.1'],     // Allow up to 10% errors
    'errors': ['rate<0.15'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';

export default function () {
  const params = {
    headers: { 'Content-Type': 'application/json' },
    timeout: '30s',
  };

  group('Stress Test - Critical Endpoints', () => {
    const startTime = new Date();
    const res = http.get(`${BASE_URL}/api/critical-endpoint`, params);

    const success = check(res, {
      'status is 200': (r) => r.status === 200,
      'not rate limited': (r) => r.status !== 429,
      'not server error': (r) => r.status < 500,
    });

    const degraded = res.timings.duration > 1000; // Response > 1s = degraded

    errorRate.add(!success);
    degradationRate.add(degraded);

    if (!success) {
      console.error(`Request failed: Status ${res.status}, VU: ${__VU}, Iter: ${__ITER}`);
    }
  });

  sleep(0.1); // Minimal sleep to maximize stress
}

export function handleSummary(data) {
  return {
    'stress-test-results.json': JSON.stringify(data, null, 2),
  };
}
