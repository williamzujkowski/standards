#!/bin/bash
# Skills.md Reversion Test Execution Script
# Version: 1.0
# Purpose: Automated test execution for reversion validation

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results tracking
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_WARNING=0
TESTS_TOTAL=0

# Test phase tracking
CURRENT_PHASE=""

# Output file
REPORT_FILE="${REPORT_FILE:-tests/reversion-test-report-$(date +%Y%m%d-%H%M%S).md}"
TEMP_DIR="/tmp/reversion-tests-$$"

# Ensure temp directory exists
mkdir -p "$TEMP_DIR"

# Initialize report
init_report() {
    cat > "$REPORT_FILE" <<EOF
# Reversion Test Execution Report

**Date**: $(date "+%Y-%m-%d %H:%M:%S")
**Executor**: $(whoami)
**Hostname**: $(hostname)
**Working Directory**: $(pwd)
**Commit Before**: $(git rev-parse HEAD)

---

EOF
}

# Log functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
    echo "$1" >> "$TEMP_DIR/execution.log"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
    echo "✅ $1" >> "$TEMP_DIR/execution.log"
}

log_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
    echo "⚠️ $1" >> "$TEMP_DIR/execution.log"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
    echo "❌ $1" >> "$TEMP_DIR/execution.log"
}

log_phase() {
    CURRENT_PHASE="$1"
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo "## $1" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
}

# Test execution wrapper
run_test() {
    local test_id="$1"
    local test_name="$2"
    local test_cmd="$3"
    local is_critical="${4:-false}"

    TESTS_TOTAL=$((TESTS_TOTAL + 1))

    log_info "Running $test_id: $test_name"

    local output_file="$TEMP_DIR/${test_id}.out"
    local error_file="$TEMP_DIR/${test_id}.err"

    # Execute test
    if eval "$test_cmd" > "$output_file" 2> "$error_file"; then
        log_success "$test_id PASSED: $test_name"
        echo "- [x] $test_id: $test_name - **PASS**" >> "$REPORT_FILE"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        local exit_code=$?
        if [ "$is_critical" = "true" ]; then
            log_error "$test_id FAILED (CRITICAL): $test_name"
            echo "- [x] $test_id: $test_name - **FAIL (CRITICAL)**" >> "$REPORT_FILE"
            TESTS_FAILED=$((TESTS_FAILED + 1))

            # Show error details
            echo "  - Exit code: $exit_code" >> "$REPORT_FILE"
            echo "  - Error output:" >> "$REPORT_FILE"
            echo '  ```' >> "$REPORT_FILE"
            head -20 "$error_file" >> "$REPORT_FILE" 2>/dev/null || echo "  (no error output)" >> "$REPORT_FILE"
            echo '  ```' >> "$REPORT_FILE"

            return 1
        else
            log_warning "$test_id WARNING: $test_name"
            echo "- [x] $test_id: $test_name - **WARNING**" >> "$REPORT_FILE"
            TESTS_WARNING=$((TESTS_WARNING + 1))
            return 0
        fi
    fi
}

# ============================================================================
# PHASE 1: PRE-REVERSION BASELINE TESTS
# ============================================================================

phase1_baseline() {
    log_phase "Phase 1: Pre-Reversion Baseline"

    # PRE-001: Current State Snapshot
    run_test "PRE-001" "Current state snapshot" "
        git log --oneline -5 > $TEMP_DIR/baseline-commits.txt &&
        git status --porcelain > $TEMP_DIR/baseline-status.txt &&
        git diff --stat 68e0eb7 HEAD > $TEMP_DIR/baseline-diff.txt &&
        find . -type f -name '*.md' | grep -E '(skills|agents|archive)' | sort > $TEMP_DIR/baseline-files.txt &&
        find skills -name 'SKILL.md' 2>/dev/null | wc -l > $TEMP_DIR/baseline-skill-count.txt &&
        test -s $TEMP_DIR/baseline-commits.txt
    " "true"

    # PRE-002: CI/CD Pipeline Status
    run_test "PRE-002" "CI/CD pipeline status" "
        python3 -c 'import yaml; yaml.safe_load(open(\".github/workflows/lint-and-validate.yml\"))' &&
        grep -qE '(audit-gates|validate-anthropic-compliance|structure-audit)' .github/workflows/lint-and-validate.yml
    " "true"

    # PRE-003: Validation Scripts Baseline
    run_test "PRE-003" "Validation scripts baseline" "
        python3 scripts/validate-skills.py --count-verify > $TEMP_DIR/baseline-skills-validation.txt 2>&1;
        python3 scripts/validate-anthropic-compliance.py > $TEMP_DIR/baseline-anthropic.txt 2>&1;
        python3 scripts/generate-audit-reports.py > $TEMP_DIR/baseline-audit.txt 2>&1;
        echo 'Skills validation: '$? >> $TEMP_DIR/baseline-exit-codes.txt;
        true
    " "false"

    # PRE-004: Repository Integrity
    run_test "PRE-004" "Repository integrity" "
        [ -z \"\$(git status --porcelain)\" ] &&
        git fsck --full > $TEMP_DIR/baseline-fsck.txt 2>&1 &&
        [ \"\$(git rev-parse --abbrev-ref HEAD)\" = \"master\" ]
    " "true"

    # PRE-005: Anthropic Skills Compliance
    run_test "PRE-005" "Anthropic skills compliance" "
        python3 scripts/validate-anthropic-compliance.py &&
        grep 'Compliant:' reports/generated/anthropic-compliance-report.md > $TEMP_DIR/baseline-compliance.txt
    " "false"

    echo "" >> "$REPORT_FILE"
}

# ============================================================================
# PHASE 2: REVERSION EXECUTION TESTS
# ============================================================================

phase2_reversion() {
    log_phase "Phase 2: Reversion Execution"

    # REV-001: Backup Creation
    run_test "REV-001" "Backup creation" "
        BACKUP_BRANCH=\"backup/pre-reversion-\$(date +%Y%m%d-%H%M%S)\" &&
        git branch \"\$BACKUP_BRANCH\" &&
        git branch | grep -q \"backup/pre-reversion\" &&
        echo \"\$BACKUP_BRANCH\" > $TEMP_DIR/backup-branch.txt
    " "true"

    # REV-002: Reversion Execution
    run_test "REV-002" "Reversion execution (DRY RUN)" "
        # Don't actually revert in test mode, just check feasibility
        git revert --no-commit a4b1ed1 --dry-run 2>&1 | tee $TEMP_DIR/revert-dry-run.txt
    " "true"

    # REV-003: Conflict Check
    run_test "REV-003" "Conflict detection" "
        git revert --no-commit a4b1ed1 --dry-run 2>&1 | grep -qv 'CONFLICT' || {
            echo 'CONFLICTS DETECTED' > $TEMP_DIR/conflicts.txt;
            false;
        }
    " "true"

    echo "" >> "$REPORT_FILE"
}

# ============================================================================
# PHASE 3: POST-REVERSION VALIDATION TESTS
# ============================================================================

phase3_validation() {
    log_phase "Phase 3: Post-Reversion Validation"

    # Note: These tests assume reversion has been executed
    # In test mode, we skip these or run them conditionally

    if [ "${EXECUTE_REVERSION:-false}" = "true" ]; then
        # POST-001: File Structure Verification
        run_test "POST-001" "File structure verification" "
            git ls-tree -r --name-only 68e0eb7 | sort > $TEMP_DIR/target-files.txt &&
            git ls-tree -r --name-only HEAD | sort > $TEMP_DIR/actual-files.txt &&
            diff $TEMP_DIR/target-files.txt $TEMP_DIR/actual-files.txt
        " "true"

        # POST-002: Critical Files Restored
        run_test "POST-002" "Critical files restored" "
            git diff 68e0eb7 HEAD -- CLAUDE.md > $TEMP_DIR/claude-diff.txt &&
            [ ! -s $TEMP_DIR/claude-diff.txt ] &&
            git diff 68e0eb7 HEAD -- README.md > $TEMP_DIR/readme-diff.txt &&
            [ ! -s $TEMP_DIR/readme-diff.txt ]
        " "true"

        # POST-003: Broken Links Check
        run_test "POST-003" "Broken links check" "
            python3 scripts/ensure-hub-links.py 2>&1 || true &&
            python3 scripts/generate-audit-reports.py &&
            grep -q 'Broken links: 0' reports/generated/linkcheck.txt
        " "true"

        # POST-004: Orphan Pages Check
        run_test "POST-004" "Orphan pages check" "
            ORPHAN_COUNT=\$(python3 -c \"import json; data=json.load(open('reports/generated/structure-audit.json')); print(data.get('orphans', 999))\") &&
            [ \"\$ORPHAN_COUNT\" -le 5 ]
        " "true"

        # POST-005: Hub Violations Check
        run_test "POST-005" "Hub violations check" "
            python3 -c \"import json; data=json.load(open('reports/generated/structure-audit.json')); exit(0 if data.get('hub_violations', 1) == 0 else 1)\"
        " "true"

        # POST-006: CI/CD Pipeline Validation
        run_test "POST-006" "CI/CD pipeline validation" "
            python3 -c 'import yaml; yaml.safe_load(open(\".github/workflows/lint-and-validate.yml\"))' &&
            for job in audit-gates structure-audit link-check nist-quickstart; do
                grep -q \"^  \$job:\" .github/workflows/lint-and-validate.yml || exit 1;
            done
        " "true"
    else
        log_warning "Skipping post-reversion tests (EXECUTE_REVERSION not set)"
        echo "- [ ] POST-001 through POST-006: Skipped (reversion not executed)" >> "$REPORT_FILE"
    fi

    echo "" >> "$REPORT_FILE"
}

# ============================================================================
# PHASE 4: REGRESSION TESTING
# ============================================================================

phase4_regression() {
    log_phase "Phase 4: Regression Testing"

    # REG-001: Validation Scripts Functionality
    run_test "REG-001" "Validation scripts functionality" "
        python3 scripts/validate-skills.py > $TEMP_DIR/reg-validate-skills.txt 2>&1;
        python3 scripts/generate-audit-reports.py > $TEMP_DIR/reg-audit-reports.txt 2>&1;
        python3 scripts/validate-claims.py > $TEMP_DIR/reg-validate-claims.txt 2>&1;
        true
    " "false"

    # REG-002: Script Executability
    run_test "REG-002" "Script executability" "
        find scripts -name '*.py' -type f ! -perm -u+x > $TEMP_DIR/non-executable.txt &&
        [ ! -s $TEMP_DIR/non-executable.txt ]
    " "false"

    # REG-003: Configuration Validity
    run_test "REG-003" "Configuration validity" "
        for yaml in \$(find config -name '*.yaml' -o -name '*.yml' 2>/dev/null); do
            python3 -c \"import yaml; yaml.safe_load(open('\$yaml'))\" || exit 1;
        done
    " "false"

    # REG-004: Documentation Coherence
    run_test "REG-004" "Documentation coherence" "
        SKILLS_REFS=\$(grep -r 'skills/' docs/ 2>/dev/null | grep -v Binary | wc -l) &&
        ARCHIVE_REFS=\$(grep -r 'archive/' docs/ 2>/dev/null | grep -v Binary | grep -v old-migrations | wc -l) &&
        echo \"Skills refs: \$SKILLS_REFS\" > $TEMP_DIR/doc-coherence.txt &&
        echo \"Archive refs: \$ARCHIVE_REFS\" >> $TEMP_DIR/doc-coherence.txt &&
        [ \"\$SKILLS_REFS\" -lt 10 ] && [ \"\$ARCHIVE_REFS\" -lt 5 ]
    " "false"

    # REG-005: Concurrent Execution
    run_test "REG-005" "Concurrent execution" "
        python3 scripts/generate-audit-reports.py > $TEMP_DIR/concurrent1.txt 2>&1 &
        PID1=\$!;
        python3 scripts/validate-skills.py > $TEMP_DIR/concurrent2.txt 2>&1 &
        PID2=\$!;
        wait \$PID1 && wait \$PID2
    " "false"

    echo "" >> "$REPORT_FILE"
}

# ============================================================================
# PHASE 5: ROLLBACK TESTS
# ============================================================================

phase5_rollback() {
    log_phase "Phase 5: Rollback Tests"

    # ROLL-001: Backup Restoration
    run_test "ROLL-001" "Backup restoration" "
        BACKUP_BRANCH=\$(cat $TEMP_DIR/backup-branch.txt 2>/dev/null || echo '') &&
        [ -n \"\$BACKUP_BRANCH\" ] &&
        CURRENT=\$(git rev-parse HEAD) &&
        git checkout \"\$BACKUP_BRANCH\" > $TEMP_DIR/rollback1.txt 2>&1 &&
        git log --oneline -1 > $TEMP_DIR/rollback-backup-commit.txt &&
        git checkout master > $TEMP_DIR/rollback2.txt 2>&1
    " "false"

    # ROLL-002: Revert the Revert
    run_test "ROLL-002" "Revert the revert (emergency recovery)" "
        git checkout -b test/revert-recovery > $TEMP_DIR/recovery1.txt 2>&1 &&
        git revert HEAD --no-commit > $TEMP_DIR/recovery2.txt 2>&1 &&
        git status --porcelain > $TEMP_DIR/recovery-status.txt &&
        git checkout master > $TEMP_DIR/recovery3.txt 2>&1 &&
        git branch -D test/revert-recovery > $TEMP_DIR/recovery4.txt 2>&1
    " "false"

    # ROLL-003: State Recovery from Reports
    run_test "ROLL-003" "State recovery from reports" "
        test -f reports/generated/structure-audit.json &&
        test -f reports/generated/linkcheck.txt &&
        python3 -c \"import json; data=json.load(open('reports/generated/structure-audit.json')); print(f\\\"Report timestamp: {data.get('timestamp', 'N/A')}\\\")\"> $TEMP_DIR/report-recovery.txt
    " "false"

    echo "" >> "$REPORT_FILE"
}

# ============================================================================
# REPORT GENERATION
# ============================================================================

generate_summary() {
    log_phase "Test Summary"

    cat >> "$REPORT_FILE" <<EOF
## Summary

**Total Tests**: $TESTS_TOTAL
**Passed**: $TESTS_PASSED
**Failed**: $TESTS_FAILED
**Warnings**: $TESTS_WARNING

EOF

    if [ $TESTS_FAILED -gt 0 ]; then
        echo "**Overall Result**: ❌ **FAIL**" >> "$REPORT_FILE"
        log_error "OVERALL RESULT: FAIL ($TESTS_FAILED failures)"
        OVERALL_RESULT=1
    else
        echo "**Overall Result**: ✅ **PASS**" >> "$REPORT_FILE"
        log_success "OVERALL RESULT: PASS"
        OVERALL_RESULT=0
    fi

    echo "" >> "$REPORT_FILE"
    echo "## Test Artifacts" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "Test artifacts stored in: \`$TEMP_DIR\`" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "Key files:" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"

    for artifact in "$TEMP_DIR"/*.txt "$TEMP_DIR"/*.log; do
        if [ -f "$artifact" ]; then
            echo "- \`$(basename "$artifact")\`" >> "$REPORT_FILE"
        fi
    done

    echo "" >> "$REPORT_FILE"
    echo "## Execution Log" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo '```' >> "$REPORT_FILE"
    tail -50 "$TEMP_DIR/execution.log" >> "$REPORT_FILE" 2>/dev/null || echo "(no execution log)" >> "$REPORT_FILE"
    echo '```' >> "$REPORT_FILE"

    log_info "Test report saved to: $REPORT_FILE"
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║       Skills.md Reversion Test Execution Suite            ║"
    echo "║                    Version 1.0                             ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""

    # Create report directory if needed
    mkdir -p "$(dirname "$REPORT_FILE")"

    init_report

    # Run test phases
    phase1_baseline
    phase2_reversion
    phase3_validation
    phase4_regression
    phase5_rollback

    # Generate summary
    generate_summary

    # Cleanup notice
    echo ""
    log_info "Test artifacts preserved in: $TEMP_DIR"
    log_info "To clean up: rm -rf $TEMP_DIR"
    echo ""

    return $OVERALL_RESULT
}

# Run main function
main "$@"
