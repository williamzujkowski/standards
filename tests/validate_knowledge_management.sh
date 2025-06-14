#!/bin/bash
# Knowledge Management Validation Test Runner
# Ensures compliance with KNOWLEDGE_MANAGEMENT_STANDARDS.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=================================="
echo "Knowledge Management Test Suite"
echo "=================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test and report results
run_test() {
    local test_name="$1"
    local test_command="$2"

    echo -n "Running: $test_name... "

    if eval "$test_command" > /tmp/test_output.txt 2>&1; then
        echo -e "${GREEN}PASSED${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAILED${NC}"
        echo "  Error output:"
        cat /tmp/test_output.txt | sed 's/^/    /'
        ((TESTS_FAILED++))
    fi
}

cd "$PROJECT_ROOT"

# Test 1: Python validation script
echo "1. Cross-Reference Validation Tests"
echo "-----------------------------------"
if command -v python3 &> /dev/null; then
    python3 tests/validate_cross_references.py
else
    echo -e "${YELLOW}WARNING: Python3 not found, skipping Python tests${NC}"
fi

echo ""
echo "2. File Structure Tests"
echo "----------------------"

# Test: Required files exist
run_test "README.md exists" "test -f README.md"
run_test "CLAUDE.md exists" "test -f CLAUDE.md"
run_test "MANIFEST.yaml exists" "test -f MANIFEST.yaml"
run_test "STANDARDS_INDEX.md exists" "test -f STANDARDS_INDEX.md"
run_test "STANDARDS_GRAPH.md exists" "test -f STANDARDS_GRAPH.md"
run_test "CHANGELOG.md exists" "test -f CHANGELOG.md"

echo ""
echo "3. Content Validation Tests"
echo "--------------------------"

# Test: All .md files have proper headers
run_test "All standards have version info" \
    "! grep -L 'Version:' *_STANDARDS.md 2>/dev/null"

run_test "All standards have status info" \
    "! grep -L 'Status:' *_STANDARDS.md 2>/dev/null"

# Test: MANIFEST.yaml is valid YAML
run_test "MANIFEST.yaml is valid YAML" \
    "python3 -c 'import yaml; yaml.safe_load(open(\"MANIFEST.yaml\"))' 2>/dev/null || yamllint MANIFEST.yaml"

# Test: No broken markdown links
run_test "No broken internal links" \
    "! grep -r '\[.*\](\./[^)]*\.md)' *.md | while read -r line; do file=\$(echo \"\$line\" | sed 's/.*(\.\///; s/).*//' | cut -d'#' -f1); test -f \"\$file\" || echo \"\$line\"; done | grep ."

echo ""
echo "4. Standards Compliance Tests"
echo "----------------------------"

# Test: Check for [REQUIRED] and [RECOMMENDED] tags
run_test "Standards use requirement tags" \
    "grep -l '\\[REQUIRED\\]\\|\\[RECOMMENDED\\]' *_STANDARDS.md | wc -l | grep -qE '^[1-9][0-9]*$'"

# Test: Implementation checklists present
run_test "Standards have implementation checklists" \
    "grep -l 'Implementation Checklist\\|checklist' *_STANDARDS.md | wc -l | grep -qE '^[1-9][0-9]*$'"

echo ""
echo "5. Token Optimization Tests"
echo "--------------------------"

# Test: MANIFEST.yaml has token counts
run_test "MANIFEST has token estimates" \
    "grep -q 'tokens:' MANIFEST.yaml"

# Test: CLAUDE.md has loading patterns
run_test "CLAUDE.md has @load patterns" \
    "grep -q '@load' CLAUDE.md"

echo ""
echo "6. Cross-Reference Tests"
echo "-----------------------"

# Test: Count cross-references
XREF_COUNT=$(grep -r '\[.*\](\./' *.md 2>/dev/null | wc -l)
echo "  Total cross-references found: $XREF_COUNT"

if [ "$XREF_COUNT" -gt 50 ]; then
    echo -e "  ${GREEN}✓ Healthy number of cross-references${NC}"
    ((TESTS_PASSED++))
else
    echo -e "  ${YELLOW}⚠ Low number of cross-references (expected > 50)${NC}"
fi

echo ""
echo "=================================="
echo "Test Summary"
echo "=================================="
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"

if [ "$TESTS_FAILED" -eq 0 ]; then
    echo -e "\n${GREEN}All tests passed! ✓${NC}"
    exit 0
else
    echo -e "\n${RED}Some tests failed. Please review and fix the issues.${NC}"
    exit 1
fi