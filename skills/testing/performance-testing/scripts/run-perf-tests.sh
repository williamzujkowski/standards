#!/bin/bash
# run-perf-tests.sh - Automated performance test execution script

set -euo pipefail

# Configuration
BASE_URL="${BASE_URL:-https://api.example.com}"
TEST_TYPE="${TEST_TYPE:-load}"
VUS="${VUS:-100}"
DURATION="${DURATION:-10m}"
OUTPUT_DIR="${OUTPUT_DIR:-./results}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "======================================"
echo "Performance Test Execution"
echo "======================================"
echo "Base URL: $BASE_URL"
echo "Test Type: $TEST_TYPE"
echo "Virtual Users: $VUS"
echo "Duration: $DURATION"
echo "======================================"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Function to run k6 tests
run_k6_test() {
    local test_file=$1
    local output_file="$OUTPUT_DIR/k6-${TEST_TYPE}-${TIMESTAMP}"

    echo -e "${YELLOW}Running k6 $TEST_TYPE test...${NC}"

    k6 run \
        --vus "$VUS" \
        --duration "$DURATION" \
        --out json="$output_file.json" \
        --summary-export="$output_file-summary.json" \
        "$test_file"

    echo -e "${GREEN}k6 test completed. Results saved to: $output_file${NC}"
}

# Function to run JMeter tests
run_jmeter_test() {
    local test_plan=$1
    local output_file="$OUTPUT_DIR/jmeter-${TEST_TYPE}-${TIMESTAMP}"

    echo -e "${YELLOW}Running JMeter $TEST_TYPE test...${NC}"

    jmeter -n \
        -t "$test_plan" \
        -Jbase_url="$BASE_URL" \
        -Jusers="$VUS" \
        -l "$output_file.jtl" \
        -e -o "$output_file-report/"

    echo -e "${GREEN}JMeter test completed. Results saved to: $output_file${NC}"
}

# Function to analyze results
analyze_results() {
    local results_file=$1

    echo -e "${YELLOW}Analyzing results...${NC}"

    if [[ -f "$results_file" ]]; then
        # Extract key metrics from k6 JSON summary
        p95=$(jq -r '.metrics.http_req_duration.values["p(95)"]' "$results_file" 2>/dev/null || echo "N/A")
        p99=$(jq -r '.metrics.http_req_duration.values["p(99)"]' "$results_file" 2>/dev/null || echo "N/A")
        error_rate=$(jq -r '.metrics.http_req_failed.values.rate' "$results_file" 2>/dev/null || echo "N/A")
        rps=$(jq -r '.metrics.http_reqs.values.rate' "$results_file" 2>/dev/null || echo "N/A")

        echo "======================================"
        echo "Test Results Summary"
        echo "======================================"
        echo "p95 Latency: $p95 ms"
        echo "p99 Latency: $p99 ms"
        echo "Error Rate: $(echo "$error_rate * 100" | bc -l 2>/dev/null || echo "$error_rate")%"
        echo "Throughput: $rps RPS"
        echo "======================================"

        # Check thresholds
        if (( $(echo "$p95 > 500" | bc -l 2>/dev/null || echo 0) )); then
            echo -e "${RED}FAIL: p95 latency exceeds 500ms threshold${NC}"
            return 1
        fi

        if (( $(echo "$error_rate > 0.01" | bc -l 2>/dev/null || echo 0) )); then
            echo -e "${RED}FAIL: Error rate exceeds 1% threshold${NC}"
            return 1
        fi

        echo -e "${GREEN}PASS: All thresholds met${NC}"
        return 0
    else
        echo -e "${RED}Results file not found: $results_file${NC}"
        return 1
    fi
}

# Main execution
case "$TEST_TYPE" in
    load)
        run_k6_test "templates/k6-load-test.js"
        analyze_results "$OUTPUT_DIR/k6-load-${TIMESTAMP}-summary.json"
        ;;
    stress)
        run_k6_test "templates/k6-stress-test.js"
        analyze_results "$OUTPUT_DIR/k6-stress-${TIMESTAMP}-summary.json"
        ;;
    jmeter)
        run_jmeter_test "config/jmeter-test-plan.jmx"
        ;;
    *)
        echo -e "${RED}Unknown test type: $TEST_TYPE${NC}"
        echo "Valid options: load, stress, jmeter"
        exit 1
        ;;
esac

echo -e "${GREEN}Performance test execution completed successfully${NC}"
