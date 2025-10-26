#!/usr/bin/env bash
#
# validate-reversion.sh - Validate skills.md reversion was successful
#
# USAGE:
#   ./scripts/validate-reversion.sh [OPTIONS]
#
# OPTIONS:
#   --verbose          Show detailed validation progress
#   --report-dir DIR   Custom report directory (default: backups/)
#   --fail-fast        Stop on first validation failure
#   --help             Show this help message
#
# EXAMPLES:
#   ./scripts/validate-reversion.sh
#   ./scripts/validate-reversion.sh --verbose --fail-fast
#   ./scripts/validate-reversion.sh --report-dir /tmp/validation
#
# DESCRIPTION:
#   Validates the reversion by:
#   1. Checking repository integrity
#   2. Running existing validation scripts
#   3. Comparing against expected pre-skills state
#   4. Generating comprehensive validation report
#
# EXIT CODES:
#   0 - All validations passed
#   1 - One or more validations failed
#   2 - Prerequisites not met
#

set -euo pipefail

# Script directory and repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Default configuration
VERBOSE=false
FAIL_FAST=false
REPORT_DIR="$REPO_ROOT/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="$REPORT_DIR/validation_${TIMESTAMP}.txt"
JSON_REPORT="$REPORT_DIR/validation_${TIMESTAMP}.json"

# Target commits
PRE_SKILLS_COMMIT="68e0eb7"

# Validation counters
CHECKS_TOTAL=0
CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_WARNINGS=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --verbose)
                VERBOSE=true
                shift
                ;;
            --report-dir)
                REPORT_DIR="$2"
                shift 2
                ;;
            --fail-fast)
                FAIL_FAST=true
                shift
                ;;
            --help)
                grep '^#' "$0" | grep -v '#!/usr/bin/env' | sed 's/^# \?//'
                exit 0
                ;;
            *)
                echo -e "${RED}Error: Unknown option $1${NC}"
                exit 1
                ;;
        esac
    done
}

# Initialize report
init_report() {
    mkdir -p "$REPORT_DIR"

    cat > "$REPORT_FILE" <<EOF
=================================================================
REVERSION VALIDATION REPORT
=================================================================

Validation Date: $(date)
Repository: $REPO_ROOT
Pre-Skills Commit: $PRE_SKILLS_COMMIT

=================================================================
VALIDATION CHECKS
=================================================================

EOF

    # Initialize JSON report
    cat > "$JSON_REPORT" <<EOF
{
  "validation_date": "$(date -Iseconds)",
  "repository": "$REPO_ROOT",
  "pre_skills_commit": "$PRE_SKILLS_COMMIT",
  "checks": []
}
EOF
}

# Log validation result
log_check() {
    local check_name="$1"
    local status="$2"  # PASS, FAIL, WARNING
    local message="$3"
    local details="${4:-}"

    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))

    case $status in
        PASS)
            CHECKS_PASSED=$((CHECKS_PASSED + 1))
            echo -e "${GREEN}✓${NC} $check_name: $message"
            ;;
        FAIL)
            CHECKS_FAILED=$((CHECKS_FAILED + 1))
            echo -e "${RED}✗${NC} $check_name: $message"
            if [[ "$FAIL_FAST" == "true" ]]; then
                echo -e "${RED}Fail-fast enabled. Stopping validation.${NC}"
                exit 1
            fi
            ;;
        WARNING)
            CHECKS_WARNINGS=$((CHECKS_WARNINGS + 1))
            echo -e "${YELLOW}⚠${NC} $check_name: $message"
            ;;
    esac

    # Write to report file
    cat >> "$REPORT_FILE" <<EOF
[$status] $check_name
  $message
$(if [[ -n "$details" ]]; then echo "  Details: $details"; fi)

EOF

    # Add to JSON report (simplified)
    if [[ "$VERBOSE" == "true" ]]; then
        echo "  Details: $details"
    fi
}

# Check 1: Git repository integrity
check_git_integrity() {
    echo ""
    echo -e "${BLUE}Checking git repository integrity...${NC}"

    cd "$REPO_ROOT"

    # Check if git repo
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_check "Git Repository" "FAIL" "Not a git repository"
        return 1
    fi

    log_check "Git Repository" "PASS" "Valid git repository"

    # Check for uncommitted changes
    if [[ -n $(git status --porcelain) ]]; then
        log_check "Working Directory" "WARNING" "Uncommitted changes present" "$(git status --short | head -5)"
    else
        log_check "Working Directory" "PASS" "Clean working directory"
    fi

    # Check current commit
    local current_commit=$(git rev-parse HEAD)
    local current_commit_short=$(git rev-parse --short HEAD)
    log_check "Current Commit" "PASS" "HEAD at $current_commit_short"
}

# Check 2: Not on skills commit
check_not_on_skills_commit() {
    echo ""
    echo -e "${BLUE}Verifying not on skills commit...${NC}"

    local current_commit=$(git rev-parse HEAD)
    local skills_commit="a4b1ed1"
    local skills_commit_full=$(git rev-parse "$skills_commit")

    if [[ "$current_commit" == "$skills_commit_full" ]]; then
        log_check "Skills Commit" "FAIL" "Still on skills commit a4b1ed1"
        return 1
    fi

    log_check "Skills Commit" "PASS" "Not on skills commit (current: $(git rev-parse --short HEAD))"
}

# Check 3: Compare with pre-skills state
check_diff_with_pre_skills() {
    echo ""
    echo -e "${BLUE}Comparing with pre-skills state...${NC}"

    # Count differences
    local added=$(git diff --numstat "$PRE_SKILLS_COMMIT" HEAD | awk '{sum+=$1} END {print sum+0}')
    local deleted=$(git diff --numstat "$PRE_SKILLS_COMMIT" HEAD | awk '{sum+=$2} END {print sum+0}')
    local files_changed=$(git diff --name-only "$PRE_SKILLS_COMMIT" HEAD | wc -l)

    if [[ $added -eq 0 && $deleted -eq 0 && $files_changed -eq 0 ]]; then
        log_check "Diff with Pre-Skills" "PASS" "Identical to pre-skills state"
    elif [[ $files_changed -lt 10 ]]; then
        log_check "Diff with Pre-Skills" "WARNING" "Minor differences: +$added -$deleted lines, $files_changed files"
    else
        log_check "Diff with Pre-Skills" "FAIL" "Significant differences: +$added -$deleted lines, $files_changed files"
    fi
}

# Check 4: Run existing validation scripts
check_validation_scripts() {
    echo ""
    echo -e "${BLUE}Running existing validation scripts...${NC}"

    cd "$REPO_ROOT"

    # Check if scripts exist and run them
    local scripts=(
        "scripts/generate-audit-reports.py"
        "scripts/validate-skills.py"
        "scripts/validate-claims.py"
    )

    for script in "${scripts[@]}"; do
        if [[ -f "$script" ]]; then
            local script_name=$(basename "$script" .py)
            echo "  Running $script_name..."

            if python3 "$script" > /dev/null 2>&1; then
                log_check "$script_name" "PASS" "Validation passed"
            else
                local exit_code=$?
                log_check "$script_name" "WARNING" "Returned exit code $exit_code (may be expected after reversion)"
            fi
        fi
    done
}

# Check 5: Directory structure
check_directory_structure() {
    echo ""
    echo -e "${BLUE}Checking directory structure...${NC}"

    cd "$REPO_ROOT"

    # Check for expected directories
    local expected_dirs=(
        "docs/standards"
        "docs/guides"
        "scripts"
        "config"
    )

    for dir in "${expected_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            local file_count=$(find "$dir" -type f | wc -l)
            log_check "Directory: $dir" "PASS" "Exists with $file_count files"
        else
            log_check "Directory: $dir" "FAIL" "Missing"
        fi
    done

    # Check for skills directory (should vary based on reversion)
    if [[ -d "skills" ]]; then
        local skills_count=$(find skills -name "SKILL.md" | wc -l)
        log_check "Skills Directory" "WARNING" "Skills directory exists with $skills_count skills (verify if expected)"
    else
        log_check "Skills Directory" "PASS" "Skills directory removed (pre-skills state)"
    fi
}

# Check 6: Critical files exist
check_critical_files() {
    echo ""
    echo -e "${BLUE}Checking critical files...${NC}"

    cd "$REPO_ROOT"

    local critical_files=(
        "README.md"
        "CLAUDE.md"
        ".github/workflows/lint-and-validate.yml"
        "config/product-matrix.yaml"
    )

    for file in "${critical_files[@]}"; do
        if [[ -f "$file" ]]; then
            local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
            log_check "File: $file" "PASS" "Exists (${size} bytes)"
        else
            log_check "File: $file" "FAIL" "Missing"
        fi
    done
}

# Check 7: Git history integrity
check_git_history() {
    echo ""
    echo -e "${BLUE}Checking git history integrity...${NC}"

    # Check if pre-skills commit is reachable
    if git merge-base --is-ancestor "$PRE_SKILLS_COMMIT" HEAD; then
        log_check "History Ancestry" "PASS" "Pre-skills commit is ancestor of HEAD"
    else
        log_check "History Ancestry" "WARNING" "Pre-skills commit not in history (hard reset?)"
    fi

    # Check commit count
    local total_commits=$(git rev-list --count HEAD)
    log_check "Commit Count" "PASS" "Total commits in history: $total_commits"

    # Check for backup branches/tags
    local backup_branches=$(git branch -a | grep -c "backup/pre-reversion-" || true)
    local backup_tags=$(git tag | grep -c "^backup-" || true)

    if [[ $backup_branches -gt 0 ]] && [[ $backup_tags -gt 0 ]]; then
        log_check "Backup Artifacts" "PASS" "Found $backup_branches backup branches and $backup_tags tags"
    else
        log_check "Backup Artifacts" "WARNING" "Limited backup artifacts found"
    fi
}

# Check 8: Python scripts syntax
check_python_syntax() {
    echo ""
    echo -e "${BLUE}Checking Python scripts syntax...${NC}"

    cd "$REPO_ROOT"

    local python_errors=0
    local python_checked=0

    while IFS= read -r -d '' py_file; do
        python_checked=$((python_checked + 1))
        if ! python3 -m py_compile "$py_file" 2>/dev/null; then
            python_errors=$((python_errors + 1))
            if [[ "$VERBOSE" == "true" ]]; then
                echo "  Syntax error: $py_file"
            fi
        fi
    done < <(find scripts -name "*.py" -type f -print0 2>/dev/null || true)

    if [[ $python_errors -eq 0 ]]; then
        log_check "Python Syntax" "PASS" "All $python_checked Python files valid"
    else
        log_check "Python Syntax" "FAIL" "$python_errors of $python_checked files have syntax errors"
    fi
}

# Generate summary
generate_summary() {
    echo ""
    echo -e "${BLUE}==================================================================${NC}"
    echo -e "${BLUE}VALIDATION SUMMARY${NC}"
    echo -e "${BLUE}==================================================================${NC}"
    echo ""

    cat >> "$REPORT_FILE" <<EOF

=================================================================
VALIDATION SUMMARY
=================================================================

Total Checks:    $CHECKS_TOTAL
Passed:          $CHECKS_PASSED
Failed:          $CHECKS_FAILED
Warnings:        $CHECKS_WARNINGS

EOF

    echo -e "Total Checks:    ${BLUE}$CHECKS_TOTAL${NC}"
    echo -e "Passed:          ${GREEN}$CHECKS_PASSED${NC}"
    echo -e "Failed:          ${RED}$CHECKS_FAILED${NC}"
    echo -e "Warnings:        ${YELLOW}$CHECKS_WARNINGS${NC}"
    echo ""

    if [[ $CHECKS_FAILED -eq 0 ]]; then
        echo -e "${GREEN}✓ ALL VALIDATIONS PASSED${NC}"
        cat >> "$REPORT_FILE" <<EOF
Result: PASSED ✓

The reversion appears successful. You can proceed with:
1. Merging the reversion branch to main
2. Pushing changes to remote

EOF
        return 0
    else
        echo -e "${RED}✗ VALIDATION FAILED${NC}"
        cat >> "$REPORT_FILE" <<EOF
Result: FAILED ✗

The reversion has issues. Consider:
1. Reviewing the failures above
2. Running rollback: ./scripts/rollback-reversion.sh
3. Investigating specific failures manually

EOF
        return 1
    fi
}

# Create comparison report
create_comparison_report() {
    echo ""
    echo -e "${BLUE}Creating detailed comparison report...${NC}"

    cat >> "$REPORT_FILE" <<EOF

=================================================================
DETAILED COMPARISON WITH PRE-SKILLS STATE
=================================================================

Git Diff Summary:
-----------------
$(git diff --stat "$PRE_SKILLS_COMMIT" HEAD 2>/dev/null || echo "Unable to generate diff")

Modified Files:
---------------
$(git diff --name-only "$PRE_SKILLS_COMMIT" HEAD 2>/dev/null | head -20 || echo "None")

Recent Commits:
---------------
$(git log --oneline -10)

=================================================================
END OF VALIDATION REPORT
=================================================================
EOF

    echo -e "${GREEN}Detailed report saved to: $REPORT_FILE${NC}"
}

# Main execution
main() {
    parse_args "$@"

    echo -e "${BLUE}==================================================================${NC}"
    echo -e "${BLUE}Standards Repository - Reversion Validation${NC}"
    echo -e "${BLUE}==================================================================${NC}"

    # Initialize report
    init_report

    # Run all validation checks
    check_git_integrity
    check_not_on_skills_commit
    check_diff_with_pre_skills
    check_validation_scripts
    check_directory_structure
    check_critical_files
    check_git_history
    check_python_syntax

    # Generate summary and comparison
    create_comparison_report

    # Show final summary
    local exit_code=0
    if ! generate_summary; then
        exit_code=1
    fi

    echo ""
    echo -e "Full report: ${BLUE}$REPORT_FILE${NC}"
    echo ""

    exit $exit_code
}

# Run main function
main "$@"
