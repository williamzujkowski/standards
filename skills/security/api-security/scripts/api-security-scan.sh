#!/bin/bash
# OWASP ZAP API Security Scanning Automation
# NIST Controls: RA-5 (Vulnerability Scanning)

set -euo pipefail

API_URL="${1:-https://api.example.com}"
OPENAPI_SPEC="${2:-openapi.json}"
OUTPUT_DIR="./security-reports"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "Starting API security scan for: $API_URL"
mkdir -p "$OUTPUT_DIR"

# Pull latest ZAP Docker image
docker pull owasp/zap2docker-stable

# Run ZAP API scan
echo "Running OWASP ZAP scan..."
docker run -v "$(pwd):/zap/wrk/:rw" -t owasp/zap2docker-stable \
  zap-api-scan.py \
  -t "$API_URL/$OPENAPI_SPEC" \
  -f openapi \
  -r "$OUTPUT_DIR/zap-report-$TIMESTAMP.html" \
  -J "$OUTPUT_DIR/zap-report-$TIMESTAMP.json" \
  -w "$OUTPUT_DIR/zap-report-$TIMESTAMP.md" \
  -d

# Run custom security tests
echo "Running custom security checks..."

# Test rate limiting
echo "Testing rate limiting..."
for i in {1..150}; do
  curl -s -o /dev/null -w "%{http_code}\n" "$API_URL/api/test" >> "$OUTPUT_DIR/rate-limit-test-$TIMESTAMP.txt"
done

RATE_LIMIT_429=$(grep -c "429" "$OUTPUT_DIR/rate-limit-test-$TIMESTAMP.txt" || true)
echo "Rate limit 429 responses: $RATE_LIMIT_429"

# Test CORS configuration
echo "Testing CORS..."
curl -H "Origin: https://evil.com" \
  -H "Access-Control-Request-Method: POST" \
  -X OPTIONS "$API_URL/api/test" \
  -v 2>&1 | grep -i "access-control" > "$OUTPUT_DIR/cors-test-$TIMESTAMP.txt" || true

# Test TLS configuration
echo "Testing TLS..."
if command -v testssl &> /dev/null; then
  testssl --quiet "$API_URL" > "$OUTPUT_DIR/tls-test-$TIMESTAMP.txt"
fi

# Generate summary
echo "Generating summary..."
cat > "$OUTPUT_DIR/summary-$TIMESTAMP.txt" << EOF
API Security Scan Summary
========================
Date: $(date)
Target: $API_URL

Rate Limiting: $([ "$RATE_LIMIT_429" -gt 0 ] && echo "PASS" || echo "FAIL")
CORS: $(grep -q "access-control-allow-origin" "$OUTPUT_DIR/cors-test-$TIMESTAMP.txt" && echo "CONFIGURED" || echo "NOT CONFIGURED")

Full reports available in: $OUTPUT_DIR
EOF

cat "$OUTPUT_DIR/summary-$TIMESTAMP.txt"
echo "Scan complete!"
