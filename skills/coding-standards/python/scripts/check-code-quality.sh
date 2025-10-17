#!/usr/bin/env bash
# check-code-quality.sh - Run all code quality checks

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SRC_DIR="${SRC_DIR:-src}"
TEST_DIR="${TEST_DIR:-tests}"
MIN_COVERAGE="${MIN_COVERAGE:-80}"

# Counters
CHECKS_PASSED=0
CHECKS_FAILED=0
TOTAL_CHECKS=0

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

run_check() {
    local check_name=$1
    shift
    local command=("$@")

    print_header "$check_name"
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    if "${command[@]}"; then
        print_success "$check_name passed"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
        return 0
    else
        print_error "$check_name failed"
        CHECKS_FAILED=$((CHECKS_FAILED + 1))
        return 1
    fi
}

# Check if in virtual environment
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
    print_warning "Not in a virtual environment"
    print_warning "Run: source venv/bin/activate"
    exit 1
fi

print_header "Python Code Quality Checks"
echo "Source directory: $SRC_DIR"
echo "Test directory: $TEST_DIR"
echo "Minimum coverage: ${MIN_COVERAGE}%"

# 1. Black - Code formatting
run_check "Black (Code Formatting)" \
    black --check --diff "$SRC_DIR" "$TEST_DIR"

# 2. isort - Import sorting
run_check "isort (Import Sorting)" \
    isort --check-only --diff "$SRC_DIR" "$TEST_DIR"

# 3. Ruff - Fast linting
if command -v ruff >/dev/null 2>&1; then
    run_check "Ruff (Fast Linting)" \
        ruff check "$SRC_DIR" "$TEST_DIR"
else
    print_warning "Ruff not installed, skipping"
fi

# 4. mypy - Type checking
if command -v mypy >/dev/null 2>&1; then
    run_check "mypy (Type Checking)" \
        mypy "$SRC_DIR"
else
    print_warning "mypy not installed, skipping"
fi

# 5. pylint - Code analysis
if command -v pylint >/dev/null 2>&1; then
    run_check "pylint (Code Analysis)" \
        pylint "$SRC_DIR"
else
    print_warning "pylint not installed, skipping"
fi

# 6. Bandit - Security scanning
if command -v bandit >/dev/null 2>&1; then
    run_check "Bandit (Security Scanning)" \
        bandit -r "$SRC_DIR" -ll
else
    print_warning "Bandit not installed, skipping"
fi

# 7. pytest - Run tests
run_check "pytest (Unit Tests)" \
    pytest "$TEST_DIR" -v

# 8. Coverage - Test coverage
run_check "Coverage (≥${MIN_COVERAGE}%)" \
    pytest --cov="$SRC_DIR" --cov-report=term-missing --cov-fail-under="$MIN_COVERAGE" "$TEST_DIR"

# 9. Documentation check
print_header "Documentation Check"
if command -v pydocstyle >/dev/null 2>&1; then
    run_check "pydocstyle (Docstring Style)" \
        pydocstyle "$SRC_DIR"
else
    print_warning "pydocstyle not installed, skipping"
fi

# Summary
print_header "Summary"
echo "Total checks: $TOTAL_CHECKS"
echo -e "${GREEN}Passed: $CHECKS_PASSED${NC}"
echo -e "${RED}Failed: $CHECKS_FAILED${NC}"

if [[ $CHECKS_FAILED -eq 0 ]]; then
    echo -e "\n${GREEN}All checks passed! ✓${NC}\n"
    exit 0
else
    echo -e "\n${RED}Some checks failed! ✗${NC}\n"
    exit 1
fi
