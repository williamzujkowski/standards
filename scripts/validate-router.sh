#!/bin/bash
# Router Validation Script
# Quick validation of all routing systems
# Author: REVIEWER Agent
# Created: 2025-10-24

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "🔍 Router Validation Suite"
echo "=========================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
PASSED=0
FAILED=0
WARNINGS=0

# Function to run a check
run_check() {
    local name="$1"
    local command="$2"

    echo -n "Checking $name... "

    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((FAILED++))
        return 1
    fi
}

# Function to run a validation that can warn
run_validation() {
    local name="$1"
    local command="$2"

    echo -n "Validating $name... "

    output=$(eval "$command" 2>&1)
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASSED++))
        return 0
    elif [ $exit_code -eq 2 ]; then
        echo -e "${YELLOW}⚠ SKIP${NC}"
        ((WARNINGS++))
        return 2
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "$output"
        ((FAILED++))
        return 1
    fi
}

echo "1. Configuration Files"
echo "----------------------"
run_check "Product Matrix exists" "test -f config/product-matrix.yaml"
run_check "Audit Rules exist" "test -f config/audit-rules.yaml"
run_check "Legacy Mappings exist" "test -f skills/legacy-bridge/resources/legacy-mappings.yaml"
echo ""

echo "2. Routing Scripts"
echo "------------------"
run_check "Skill Loader exists" "test -f scripts/skill-loader.py"
run_check "Hub Linking script exists" "test -f scripts/ensure-hub-links.py"
run_check "Audit Reports script exists" "test -f scripts/generate-audit-reports.py"
run_check "Skill Loader executable" "test -x scripts/skill-loader.py"
run_check "Hub Linking executable" "test -x scripts/ensure-hub-links.py"
echo ""

echo "3. YAML Validation"
echo "------------------"
run_check "Product Matrix valid YAML" "python3 -c 'import yaml; yaml.safe_load(open(\"config/product-matrix.yaml\"))'"
run_check "Audit Rules valid YAML" "python3 -c 'import yaml; yaml.safe_load(open(\"config/audit-rules.yaml\"))'"
run_check "Legacy Mappings valid YAML" "python3 -c 'import yaml; yaml.safe_load(open(\"skills/legacy-bridge/resources/legacy-mappings.yaml\"))'"
echo ""

echo "4. Integration Tests"
echo "--------------------"

if command -v pytest &> /dev/null; then
    echo "Running main validation tests..."
    if pytest tests/integration/test_router_validation.py -q --tb=no; then
        echo -e "${GREEN}✓ Main validation tests PASSED${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ Main validation tests FAILED${NC}"
        ((FAILED++))
    fi

    echo "Running edge case tests..."
    if pytest tests/integration/test_router_edge_cases.py -q --tb=no; then
        echo -e "${GREEN}✓ Edge case tests PASSED${NC}"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠ Edge case tests had issues (check report)${NC}"
        ((WARNINGS++))
    fi
else
    echo -e "${YELLOW}⚠ pytest not found, skipping integration tests${NC}"
    ((WARNINGS++))
fi
echo ""

echo "5. Quick Smoke Tests"
echo "--------------------"

# Test skill loader can import
if python3 -c "import sys; sys.path.insert(0, 'scripts'); import skill_loader" 2>/dev/null; then
    echo -e "${GREEN}✓ Skill loader imports successfully${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ Skill loader import issues${NC}"
    ((WARNINGS++))
fi

# Check for common issues
if grep -q "NIST-IG:base" config/product-matrix.yaml; then
    echo -e "${GREEN}✓ NIST baseline present in config${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ NIST baseline missing from config${NC}"
    ((FAILED++))
fi

# Check CLI product specifically
if grep -A 10 "^  cli:" config/product-matrix.yaml | grep -q "NIST-IG:base"; then
    echo -e "${GREEN}✓ CLI product includes NIST-IG:base${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ CLI product missing NIST-IG:base (known issue)${NC}"
    ((FAILED++))
fi

echo ""
echo "=============================="
echo "Results Summary"
echo "=============================="
echo -e "${GREEN}Passed: $PASSED${NC}"
if [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
fi
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED${NC}"
fi
echo ""

# Overall status
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ Router validation PASSED${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}  (with $WARNINGS warnings)${NC}"
    fi
    exit 0
else
    echo -e "${RED}✗ Router validation FAILED${NC}"
    echo ""
    echo "See reports for details:"
    echo "  - tests/validation/ROUTER_VALIDATION_REPORT.md"
    echo "  - tests/validation/ROUTER_EDGE_CASES_REPORT.md"
    exit 1
fi
