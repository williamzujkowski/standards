#!/usr/bin/env bash
#
# verify-reversion-scripts.sh - Verify reversion scripts are properly installed
#
# USAGE:
#   ./scripts/verify-reversion-scripts.sh
#
# DESCRIPTION:
#   Checks that all reversion automation scripts are present, executable,
#   and working correctly. Runs basic tests on each script.
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Test counters
TESTS_TOTAL=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
test_check() {
    local name="$1"
    local condition="$2"

    TESTS_TOTAL=$((TESTS_TOTAL + 1))

    if eval "$condition"; then
        echo -e "${GREEN}✓${NC} $name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}✗${NC} $name"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Reversion Scripts Verification${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Test 1: Scripts exist
echo -e "${BLUE}Checking scripts exist...${NC}"
test_check "backup-current-state.sh exists" "[[ -f '$SCRIPT_DIR/backup-current-state.sh' ]]"
test_check "revert-to-pre-skills.sh exists" "[[ -f '$SCRIPT_DIR/revert-to-pre-skills.sh' ]]"
test_check "validate-reversion.sh exists" "[[ -f '$SCRIPT_DIR/validate-reversion.sh' ]]"
test_check "rollback-reversion.sh exists" "[[ -f '$SCRIPT_DIR/rollback-reversion.sh' ]]"
echo ""

# Test 2: Scripts are executable
echo -e "${BLUE}Checking scripts are executable...${NC}"
test_check "backup-current-state.sh executable" "[[ -x '$SCRIPT_DIR/backup-current-state.sh' ]]"
test_check "revert-to-pre-skills.sh executable" "[[ -x '$SCRIPT_DIR/revert-to-pre-skills.sh' ]]"
test_check "validate-reversion.sh executable" "[[ -x '$SCRIPT_DIR/validate-reversion.sh' ]]"
test_check "rollback-reversion.sh executable" "[[ -x '$SCRIPT_DIR/rollback-reversion.sh' ]]"
echo ""

# Test 3: Help flag works
echo -e "${BLUE}Checking --help flag works...${NC}"
test_check "backup-current-state.sh --help" "$SCRIPT_DIR/backup-current-state.sh --help >/dev/null 2>&1"
test_check "revert-to-pre-skills.sh --help" "$SCRIPT_DIR/revert-to-pre-skills.sh --help >/dev/null 2>&1"
test_check "validate-reversion.sh --help" "$SCRIPT_DIR/validate-reversion.sh --help >/dev/null 2>&1"
test_check "rollback-reversion.sh --help" "$SCRIPT_DIR/rollback-reversion.sh --help >/dev/null 2>&1"
echo ""

# Test 4: Documentation exists
echo -e "${BLUE}Checking documentation exists...${NC}"
test_check "REVERSION_SCRIPTS_GUIDE.md exists" "[[ -f '$SCRIPT_DIR/REVERSION_SCRIPTS_GUIDE.md' ]]"
test_check "REVERSION_AUTOMATION_SUMMARY.md exists" "[[ -f '$SCRIPT_DIR/REVERSION_AUTOMATION_SUMMARY.md' ]]"
echo ""

# Test 5: Dependencies
echo -e "${BLUE}Checking dependencies...${NC}"
test_check "bash available" "command -v bash >/dev/null 2>&1"
test_check "git available" "command -v git >/dev/null 2>&1"
test_check "python3 available" "command -v python3 >/dev/null 2>&1"
echo ""

# Test 6: Git repository
echo -e "${BLUE}Checking git repository...${NC}"
test_check "In git repository" "git rev-parse --git-dir >/dev/null 2>&1"
test_check "Skills commit exists (a4b1ed1)" "git cat-file -e a4b1ed1 2>/dev/null"
test_check "Pre-skills commit exists (68e0eb7)" "git cat-file -e 68e0eb7 2>/dev/null"
echo ""

# Test 7: Script content validation
echo -e "${BLUE}Validating script content...${NC}"
test_check "backup script has logging" "grep -q 'log()' '$SCRIPT_DIR/backup-current-state.sh'"
test_check "revert script has confirmation" "grep -q 'confirm()' '$SCRIPT_DIR/revert-to-pre-skills.sh'"
test_check "validate script has checks" "grep -q 'check_git_integrity' '$SCRIPT_DIR/validate-reversion.sh'"
test_check "rollback script has safety" "grep -q 'verify_backup' '$SCRIPT_DIR/rollback-reversion.sh'"
echo ""

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}VERIFICATION SUMMARY${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Total Tests: ${BLUE}$TESTS_TOTAL${NC}"
echo -e "Passed:      ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed:      ${RED}$TESTS_FAILED${NC}"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}✓ ALL VERIFICATION TESTS PASSED${NC}"
    echo ""
    echo -e "${YELLOW}Scripts are ready to use!${NC}"
    echo ""
    echo "Quick Start:"
    echo "  1. Create backup:    ./scripts/backup-current-state.sh"
    echo "  2. Perform revert:   ./scripts/revert-to-pre-skills.sh --method revert"
    echo "  3. Validate:         ./scripts/validate-reversion.sh"
    echo "  4. If needed:        ./scripts/rollback-reversion.sh"
    echo ""
    echo "For detailed guide: cat scripts/REVERSION_SCRIPTS_GUIDE.md"
    exit 0
else
    echo -e "${RED}✗ VERIFICATION FAILED${NC}"
    echo ""
    echo -e "${YELLOW}Please fix the failed tests before using the scripts.${NC}"
    exit 1
fi
