#!/usr/bin/env bash
#
# Test Suite for Cleanup Scripts
#
# Tests:
#   1. cleanup-vestigial-artifacts.sh
#   2. fix-documentation-accuracy.py
#   3. validate-cleanup.sh
#
# Usage:
#   ./tests/test-cleanup-scripts.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TEST_DIR="${REPO_ROOT}/tests/cleanup-test-workspace"
CLEANUP_SCRIPT="${REPO_ROOT}/scripts/cleanup-vestigial-artifacts.sh"
ACCURACY_SCRIPT="${REPO_ROOT}/scripts/fix-documentation-accuracy.py"
VALIDATE_SCRIPT="${REPO_ROOT}/scripts/validate-cleanup.sh"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Test helper functions
setup_test_env() {
    echo "Setting up test environment..."
    rm -rf "${TEST_DIR}"
    mkdir -p "${TEST_DIR}"
    cd "${TEST_DIR}"
}

teardown_test_env() {
    echo "Cleaning up test environment..."
    cd "${REPO_ROOT}"
    rm -rf "${TEST_DIR}"
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    local test_name="$3"

    ((TOTAL_TESTS++))

    if [[ "${expected}" == "${actual}" ]]; then
        echo -e "${GREEN}✓${NC} ${test_name}"
        ((PASSED_TESTS++))
        return 0
    else
        echo -e "${RED}✗${NC} ${test_name}"
        echo "  Expected: ${expected}"
        echo "  Actual: ${actual}"
        ((FAILED_TESTS++))
        return 1
    fi
}

assert_file_exists() {
    local file="$1"
    local test_name="$2"

    ((TOTAL_TESTS++))

    if [[ -f "${file}" ]]; then
        echo -e "${GREEN}✓${NC} ${test_name}"
        ((PASSED_TESTS++))
        return 0
    else
        echo -e "${RED}✗${NC} ${test_name}"
        echo "  File not found: ${file}"
        ((FAILED_TESTS++))
        return 1
    fi
}

assert_file_not_exists() {
    local file="$1"
    local test_name="$2"

    ((TOTAL_TESTS++))

    if [[ ! -f "${file}" ]]; then
        echo -e "${GREEN}✓${NC} ${test_name}"
        ((PASSED_TESTS++))
        return 0
    else
        echo -e "${RED}✗${NC} ${test_name}"
        echo "  File should not exist: ${file}"
        ((FAILED_TESTS++))
        return 1
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local test_name="$3"

    ((TOTAL_TESTS++))

    if echo "${haystack}" | grep -q "${needle}"; then
        echo -e "${GREEN}✓${NC} ${test_name}"
        ((PASSED_TESTS++))
        return 0
    else
        echo -e "${RED}✗${NC} ${test_name}"
        echo "  '${needle}' not found in output"
        ((FAILED_TESTS++))
        return 1
    fi
}

# Test Suite 1: cleanup-vestigial-artifacts.sh
test_cleanup_script() {
    echo ""
    echo "========================================="
    echo "Test Suite 1: cleanup-vestigial-artifacts.sh"
    echo "========================================="

    setup_test_env

    # Create test files
    mkdir -p docs examples
    echo "test content" > docs/test-file.md
    echo "example content" > examples/example.py

    # Create input file
    cat > files-to-delete.txt <<EOF
docs/test-file.md
examples/example.py
EOF

    # Test 1: Dry run doesn't delete files
    echo ""
    echo "Test 1: Dry run mode"
    "${CLEANUP_SCRIPT}" --dry-run --input files-to-delete.txt > output.txt 2>&1 || true

    assert_file_exists "docs/test-file.md" "Dry run preserves files"
    assert_contains "$(cat output.txt)" "DRY RUN MODE" "Dry run message displayed"

    # Test 2: Backup creation
    echo ""
    echo "Test 2: Backup creation"
    yes | "${CLEANUP_SCRIPT}" --input files-to-delete.txt --backup-dir backup > output.txt 2>&1 || true

    assert_file_exists "backup/docs/test-file.md" "Backup created for file 1"
    assert_file_exists "backup/examples/example.py" "Backup created for file 2"

    # Test 3: Files deleted
    echo ""
    echo "Test 3: File deletion"
    assert_file_not_exists "docs/test-file.md" "File 1 deleted"
    assert_file_not_exists "examples/example.py" "File 2 deleted"

    # Test 4: Log file created
    echo ""
    echo "Test 4: Logging"
    LOG_COUNT=$(find "${REPO_ROOT}/reports/generated" -name "cleanup-*.log" | wc -l)
    [[ ${LOG_COUNT} -gt 0 ]] && echo -e "${GREEN}✓${NC} Log file created" || echo -e "${RED}✗${NC} No log file"
    ((TOTAL_TESTS++))
    [[ ${LOG_COUNT} -gt 0 ]] && ((PASSED_TESTS++)) || ((FAILED_TESTS++))

    teardown_test_env
}

# Test Suite 2: fix-documentation-accuracy.py
test_accuracy_script() {
    echo ""
    echo "========================================="
    echo "Test Suite 2: fix-documentation-accuracy.py"
    echo "========================================="

    setup_test_env

    # Create test document with accuracy issues
    mkdir -p docs
    cat > docs/TEST.md <<EOF
# Test Document

This is a revolutionary game-changer that significantly improves performance.

We have numerous agents available for seamless integration.

This always works perfectly with guaranteed results.
EOF

    # Test 1: Detection
    echo ""
    echo "Test 1: Issue detection"
    python3 "${ACCURACY_SCRIPT}" --dry-run --target docs/TEST.md > output.txt 2>&1 || true

    assert_contains "$(cat output.txt)" "Marketing hyperbole" "Detects marketing language"
    assert_contains "$(cat output.txt)" "Vague quantifier" "Detects vague language"

    # Test 2: Dry run preserves file
    echo ""
    echo "Test 2: Dry run preservation"
    ORIGINAL_CONTENT=$(cat docs/TEST.md)
    python3 "${ACCURACY_SCRIPT}" --dry-run --target docs/TEST.md > /dev/null 2>&1 || true
    CURRENT_CONTENT=$(cat docs/TEST.md)

    assert_equals "${ORIGINAL_CONTENT}" "${CURRENT_CONTENT}" "Dry run doesn't modify file"

    # Test 3: Fix application
    echo ""
    echo "Test 3: Fix application"
    python3 "${ACCURACY_SCRIPT}" --fix --target docs/TEST.md > /dev/null 2>&1 || true

    NEW_CONTENT=$(cat docs/TEST.md)
    [[ "${NEW_CONTENT}" != "${ORIGINAL_CONTENT}" ]] && FIX_APPLIED=true || FIX_APPLIED=false

    assert_equals "true" "${FIX_APPLIED}" "Fixes applied to file"

    # Test 4: Report generation
    echo ""
    echo "Test 4: Report generation"
    REPORT_COUNT=$(find "${REPO_ROOT}/reports/generated" -name "accuracy-report-*.md" | wc -l)
    [[ ${REPORT_COUNT} -gt 0 ]] && echo -e "${GREEN}✓${NC} Report generated" || echo -e "${RED}✗${NC} No report"
    ((TOTAL_TESTS++))
    [[ ${REPORT_COUNT} -gt 0 ]] && ((PASSED_TESTS++)) || ((FAILED_TESTS++))

    teardown_test_env
}

# Test Suite 3: validate-cleanup.sh
test_validate_script() {
    echo ""
    echo "========================================="
    echo "Test Suite 3: validate-cleanup.sh"
    echo "========================================="

    # Test 1: Script execution
    echo ""
    echo "Test 1: Script execution"
    cd "${REPO_ROOT}"
    "${VALIDATE_SCRIPT}" --quick > /tmp/validate-output.txt 2>&1 || true

    assert_contains "$(cat /tmp/validate-output.txt)" "Validation Summary" "Validation runs"

    # Test 2: Check execution
    echo ""
    echo "Test 2: Validation checks"
    assert_contains "$(cat /tmp/validate-output.txt)" "Structure Audit" "Structure check runs"
    assert_contains "$(cat /tmp/validate-output.txt)" "Claims Validation" "Claims check runs"

    # Test 3: Report generation
    echo ""
    echo "Test 3: Report generation"
    REPORT_COUNT=$(find "${REPO_ROOT}/reports/generated" -name "cleanup-validation-*.md" | wc -l)
    [[ ${REPORT_COUNT} -gt 0 ]] && echo -e "${GREEN}✓${NC} Validation report created" || echo -e "${RED}✗${NC} No report"
    ((TOTAL_TESTS++))
    [[ ${REPORT_COUNT} -gt 0 ]] && ((PASSED_TESTS++)) || ((FAILED_TESTS++))

    # Test 4: Exit codes
    echo ""
    echo "Test 4: Exit codes"
    "${VALIDATE_SCRIPT}" --quick > /dev/null 2>&1
    EXIT_CODE=$?
    [[ ${EXIT_CODE} -le 2 ]] && echo -e "${GREEN}✓${NC} Valid exit code (${EXIT_CODE})" || echo -e "${RED}✗${NC} Invalid exit code"
    ((TOTAL_TESTS++))
    [[ ${EXIT_CODE} -le 2 ]] && ((PASSED_TESTS++)) || ((FAILED_TESTS++))
}

# Main execution
main() {
    echo "========================================="
    echo "Cleanup Scripts Test Suite"
    echo "========================================="
    echo ""

    # Check scripts exist
    if [[ ! -x "${CLEANUP_SCRIPT}" ]]; then
        echo -e "${RED}Error: cleanup-vestigial-artifacts.sh not found or not executable${NC}"
        exit 1
    fi

    if [[ ! -x "${ACCURACY_SCRIPT}" ]]; then
        echo -e "${RED}Error: fix-documentation-accuracy.py not found or not executable${NC}"
        exit 1
    fi

    if [[ ! -x "${VALIDATE_SCRIPT}" ]]; then
        echo -e "${RED}Error: validate-cleanup.sh not found or not executable${NC}"
        exit 1
    fi

    # Run test suites
    test_cleanup_script
    test_accuracy_script
    test_validate_script

    # Summary
    echo ""
    echo "========================================="
    echo "Test Summary"
    echo "========================================="
    echo "Total Tests: ${TOTAL_TESTS}"
    echo -e "${GREEN}Passed: ${PASSED_TESTS}${NC}"

    if [[ ${FAILED_TESTS} -gt 0 ]]; then
        echo -e "${RED}Failed: ${FAILED_TESTS}${NC}"
        echo ""
        echo -e "${RED}❌ Some tests failed${NC}"
        exit 1
    else
        echo ""
        echo -e "${GREEN}✅ All tests passed!${NC}"
        exit 0
    fi
}

# Run tests
main "$@"
