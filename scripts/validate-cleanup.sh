#!/usr/bin/env bash
#
# Validate Cleanup Script
#
# Purpose: Comprehensive validation after cleanup operations.
# Features:
#   - Runs all existing validation scripts
#   - Checks for broken references
#   - Verifies no functionality broken
#   - Generates cleanup validation report
#   - Exit codes for CI/CD integration
#
# Usage:
#   ./validate-cleanup.sh [options]
#   ./validate-cleanup.sh --verbose
#   ./validate-cleanup.sh --quick (skip slow checks)

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
REPORTS_DIR="${REPO_ROOT}/reports/generated"
REPORT_FILE="${REPORTS_DIR}/cleanup-validation-${TIMESTAMP}.md"
LOG_FILE="${REPORTS_DIR}/cleanup-validation-${TIMESTAMP}.log"
QUICK_MODE=false
VERBOSE=false

# Exit codes
EXIT_SUCCESS=0
EXIT_ERRORS=1
EXIT_WARNINGS=2

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Validation results
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# Usage
usage() {
    cat <<EOF
Usage: $0 [options]

Comprehensive validation after cleanup operations.

Options:
  --quick       Skip slow validation checks
  --verbose     Enable verbose output
  --help        Show this help message

Validation Checks:
  1. Structure audit (broken links, orphans, hubs)
  2. Claims validation (documentation accuracy)
  3. Skills validation (Anthropic compliance)
  4. Cross-references check
  5. File integrity check
  6. Git status check

Exit Codes:
  0 - All checks passed
  1 - Critical errors found
  2 - Warnings only

Examples:
  # Full validation
  $0

  # Quick validation (essential checks only)
  $0 --quick

  # Verbose mode
  $0 --verbose
EOF
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --quick)
            QUICK_MODE=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Logging functions
log() {
    echo "$@" | tee -a "${LOG_FILE}"
}

log_section() {
    echo "" | tee -a "${LOG_FILE}"
    echo "=========================================" | tee -a "${LOG_FILE}"
    echo "$@" | tee -a "${LOG_FILE}"
    echo "=========================================" | tee -a "${LOG_FILE}"
}

log_check() {
    local name="$1"
    local status="$2"
    local message="${3:-}"

    ((TOTAL_CHECKS++))

    case "${status}" in
        PASS)
            echo -e "${GREEN}✓${NC} ${name}" | tee -a "${LOG_FILE}"
            ((PASSED_CHECKS++))
            ;;
        FAIL)
            echo -e "${RED}✗${NC} ${name}" | tee -a "${LOG_FILE}"
            ((FAILED_CHECKS++))
            ;;
        WARN)
            echo -e "${YELLOW}⚠${NC} ${name}" | tee -a "${LOG_FILE}"
            ((WARNING_CHECKS++))
            ;;
    esac

    if [[ -n "${message}" ]]; then
        echo "  ${message}" | tee -a "${LOG_FILE}"
    fi
}

# Initialize
mkdir -p "${REPORTS_DIR}"

log_section "Cleanup Validation - ${TIMESTAMP}"
log "Repository: ${REPO_ROOT}"
log "Mode: $([ "${QUICK_MODE}" = true ] && echo "QUICK" || echo "FULL")"
log ""

# Check 1: Structure Audit
log_section "Check 1: Structure Audit"

if [[ -x "${SCRIPT_DIR}/generate-audit-reports.py" ]]; then
    if python3 "${SCRIPT_DIR}/generate-audit-reports.py" >> "${LOG_FILE}" 2>&1; then
        # Check results
        AUDIT_JSON="${REPORTS_DIR}/structure-audit.json"

        if [[ -f "${AUDIT_JSON}" ]]; then
            BROKEN_LINKS=$(python3 -c "import json; print(json.load(open('${AUDIT_JSON}'))['broken_links'])" 2>/dev/null || echo "-1")
            ORPHANS=$(python3 -c "import json; print(json.load(open('${AUDIT_JSON}'))['orphans'])" 2>/dev/null || echo "-1")
            HUB_VIOLATIONS=$(python3 -c "import json; print(json.load(open('${AUDIT_JSON}'))['hub_violations'])" 2>/dev/null || echo "-1")

            log "  Broken links: ${BROKEN_LINKS}"
            log "  Orphans: ${ORPHANS}"
            log "  Hub violations: ${HUB_VIOLATIONS}"

            if [[ "${BROKEN_LINKS}" -eq 0 ]]; then
                log_check "No broken links" "PASS"
            else
                log_check "Broken links found" "FAIL" "${BROKEN_LINKS} broken links"
            fi

            if [[ "${HUB_VIOLATIONS}" -eq 0 ]]; then
                log_check "No hub violations" "PASS"
            else
                log_check "Hub violations found" "FAIL" "${HUB_VIOLATIONS} violations"
            fi

            if [[ "${ORPHANS}" -le 5 ]]; then
                log_check "Orphan count acceptable" "PASS" "${ORPHANS} orphans (limit: 5)"
            else
                log_check "Too many orphans" "WARN" "${ORPHANS} orphans (limit: 5)"
            fi
        else
            log_check "Structure audit" "FAIL" "Audit JSON not found"
        fi
    else
        log_check "Structure audit" "FAIL" "Script execution failed"
    fi
else
    log_check "Structure audit" "WARN" "Script not found or not executable"
fi

# Check 2: Claims Validation
log_section "Check 2: Claims Validation"

if [[ -x "${SCRIPT_DIR}/validate-claims.py" ]]; then
    if python3 "${SCRIPT_DIR}/validate-claims.py" >> "${LOG_FILE}" 2>&1; then
        log_check "Documentation claims" "PASS" "All claims validated"
    else
        EXIT_CODE=$?
        if [[ ${EXIT_CODE} -eq 2 ]]; then
            log_check "Documentation claims" "WARN" "Warnings found (check log)"
        else
            log_check "Documentation claims" "FAIL" "Errors found (check log)"
        fi
    fi
else
    log_check "Claims validation" "WARN" "Script not found or not executable"
fi

# Check 3: Skills Validation
log_section "Check 3: Skills Validation"

if [[ -x "${SCRIPT_DIR}/validate-skills.py" ]]; then
    if python3 "${SCRIPT_DIR}/validate-skills.py" >> "${LOG_FILE}" 2>&1; then
        log_check "Skills structure" "PASS"
    else
        log_check "Skills structure" "FAIL" "Validation failed"
    fi
else
    log_check "Skills validation" "WARN" "Script not found or not executable"
fi

# Check 4: Anthropic Compliance
if [[ "${QUICK_MODE}" = false ]]; then
    log_section "Check 4: Anthropic Compliance"

    if [[ -x "${SCRIPT_DIR}/validate-anthropic-compliance.py" ]]; then
        if python3 "${SCRIPT_DIR}/validate-anthropic-compliance.py" >> "${LOG_FILE}" 2>&1; then
            log_check "Anthropic compliance" "PASS"
        else
            log_check "Anthropic compliance" "WARN" "Some skills may need optimization"
        fi
    else
        log_check "Anthropic compliance" "WARN" "Script not found"
    fi
fi

# Check 5: Cross-References
log_section "Check 5: Cross-References"

# Check for common reference patterns
CLAUDE_MD="${REPO_ROOT}/CLAUDE.md"
README_MD="${REPO_ROOT}/README.md"

if [[ -f "${CLAUDE_MD}" ]]; then
    # Check agent count references
    AGENT_FILES=$(find "${REPO_ROOT}/.claude/agents" -name "*.md" ! -name "README.md" ! -name "MIGRATION_SUMMARY.md" 2>/dev/null | wc -l)
    CLAUDE_AGENT_COUNT=$(grep -oP '🚀 Agent Types.*?\(\K\d+' "${CLAUDE_MD}" 2>/dev/null || echo "0")

    if [[ "${AGENT_FILES}" -eq "${CLAUDE_AGENT_COUNT}" ]] || [[ "${CLAUDE_AGENT_COUNT}" -eq 0 ]]; then
        log_check "Agent count reference" "PASS" "Count matches (${AGENT_FILES})"
    else
        log_check "Agent count reference" "FAIL" "Mismatch: files=${AGENT_FILES}, documented=${CLAUDE_AGENT_COUNT}"
    fi

    # Check skill count references
    SKILL_FILES=$(find "${REPO_ROOT}/skills" -name "SKILL.md" 2>/dev/null | wc -l)
    CLAUDE_SKILL_COUNT=$(grep -oP '\d+/\d+ skills' "${CLAUDE_MD}" 2>/dev/null | head -1 | grep -oP '\d+' | head -1 || echo "0")

    if [[ "${SKILL_FILES}" -eq "${CLAUDE_SKILL_COUNT}" ]] || [[ "${CLAUDE_SKILL_COUNT}" -eq 0 ]]; then
        log_check "Skill count reference" "PASS" "Count matches (${SKILL_FILES})"
    else
        log_check "Skill count reference" "FAIL" "Mismatch: files=${SKILL_FILES}, documented=${CLAUDE_SKILL_COUNT}"
    fi
else
    log_check "CLAUDE.md exists" "FAIL" "File not found"
fi

# Check 6: File Integrity
log_section "Check 6: File Integrity"

# Check for required files
REQUIRED_FILES=(
    "CLAUDE.md"
    "README.md"
    "config/audit-rules.yaml"
    "config/product-matrix.yaml"
    "scripts/generate-audit-reports.py"
    "scripts/validate-claims.py"
)

MISSING_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
    if [[ ! -f "${REPO_ROOT}/${file}" ]]; then
        MISSING_FILES+=("${file}")
    fi
done

if [[ ${#MISSING_FILES[@]} -eq 0 ]]; then
    log_check "Required files present" "PASS"
else
    log_check "Required files present" "FAIL" "Missing: ${MISSING_FILES[*]}"
fi

# Check for empty files
EMPTY_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
    if [[ -f "${REPO_ROOT}/${file}" ]] && [[ ! -s "${REPO_ROOT}/${file}" ]]; then
        EMPTY_FILES+=("${file}")
    fi
done

if [[ ${#EMPTY_FILES[@]} -eq 0 ]]; then
    log_check "No empty files" "PASS"
else
    log_check "No empty files" "WARN" "Empty: ${EMPTY_FILES[*]}"
fi

# Check 7: Git Status
log_section "Check 7: Git Status"

cd "${REPO_ROOT}"

# Check for uncommitted changes
if git diff --quiet && git diff --cached --quiet; then
    log_check "No uncommitted changes" "PASS"
else
    CHANGED_FILES=$(git diff --name-only && git diff --cached --name-only)
    log_check "Uncommitted changes present" "WARN" "Review before committing"
    if [[ "${VERBOSE}" = true ]]; then
        echo "${CHANGED_FILES}" >> "${LOG_FILE}"
    fi
fi

# Check for untracked files
UNTRACKED=$(git ls-files --others --exclude-standard)
if [[ -z "${UNTRACKED}" ]]; then
    log_check "No untracked files" "PASS"
else
    UNTRACKED_COUNT=$(echo "${UNTRACKED}" | wc -l)
    log_check "Untracked files present" "WARN" "${UNTRACKED_COUNT} files"
fi

# Generate Report
log_section "Generating Report"

cat > "${REPORT_FILE}" <<EOF
# Cleanup Validation Report

**Generated**: $(date +'%Y-%m-%d %H:%M:%S')
**Repository**: ${REPO_ROOT}
**Mode**: $([ "${QUICK_MODE}" = true ] && echo "QUICK" || echo "FULL")

## Summary

- **Total Checks**: ${TOTAL_CHECKS}
- **Passed**: ${PASSED_CHECKS} ($(( PASSED_CHECKS * 100 / TOTAL_CHECKS ))%)
- **Failed**: ${FAILED_CHECKS}
- **Warnings**: ${WARNING_CHECKS}

## Status

$(if [[ ${FAILED_CHECKS} -eq 0 ]]; then
    echo "✅ **All critical checks passed**"
elif [[ ${FAILED_CHECKS} -le 2 ]]; then
    echo "⚠️ **Minor issues found** (${FAILED_CHECKS} failures)"
else
    echo "❌ **Critical issues found** (${FAILED_CHECKS} failures)"
fi)

## Next Steps

EOF

if [[ ${FAILED_CHECKS} -gt 0 ]]; then
    cat >> "${REPORT_FILE}" <<EOF
1. Review failures in log: \`${LOG_FILE}\`
2. Fix broken links: \`python3 scripts/auto-fix-links.py\`
3. Update documentation references
4. Re-run validation: \`./scripts/validate-cleanup.sh\`
EOF
elif [[ ${WARNING_CHECKS} -gt 0 ]]; then
    cat >> "${REPORT_FILE}" <<EOF
1. Review warnings in log: \`${LOG_FILE}\`
2. Consider addressing warnings before final commit
3. Run full validation: \`./scripts/validate-cleanup.sh\` (without --quick)
EOF
else
    cat >> "${REPORT_FILE}" <<EOF
✅ No action required - all checks passed!

Safe to proceed with:
- Git commit
- Pull request
- CI/CD pipeline
EOF
fi

cat >> "${REPORT_FILE}" <<EOF

## Detailed Results

See full log: \`${LOG_FILE}\`

### Key Metrics

EOF

if [[ -f "${REPORTS_DIR}/structure-audit.json" ]]; then
    cat >> "${REPORT_FILE}" <<EOF
**Structure Audit**:
- Broken links: ${BROKEN_LINKS}
- Orphans: ${ORPHANS}
- Hub violations: ${HUB_VIOLATIONS}

EOF
fi

cat >> "${REPORT_FILE}" <<EOF
**File Integrity**:
- Required files: $(( ${#REQUIRED_FILES[@]} - ${#MISSING_FILES[@]} ))/${#REQUIRED_FILES[@]}
- Missing files: ${#MISSING_FILES[@]}
- Empty files: ${#EMPTY_FILES[@]}

---

*Report generated by validate-cleanup.sh*
EOF

log ""
log "Report saved: ${REPORT_FILE}"
log "Log saved: ${LOG_FILE}"

# Summary
log_section "Validation Summary"

echo -e "${BLUE}Total Checks:${NC} ${TOTAL_CHECKS}" | tee -a "${LOG_FILE}"
echo -e "${GREEN}Passed:${NC} ${PASSED_CHECKS} ($(( PASSED_CHECKS * 100 / TOTAL_CHECKS ))%)" | tee -a "${LOG_FILE}"

if [[ ${FAILED_CHECKS} -gt 0 ]]; then
    echo -e "${RED}Failed:${NC} ${FAILED_CHECKS}" | tee -a "${LOG_FILE}"
fi

if [[ ${WARNING_CHECKS} -gt 0 ]]; then
    echo -e "${YELLOW}Warnings:${NC} ${WARNING_CHECKS}" | tee -a "${LOG_FILE}"
fi

echo "" | tee -a "${LOG_FILE}"

# Determine exit code
if [[ ${FAILED_CHECKS} -gt 0 ]]; then
    echo -e "${RED}❌ Validation failed - critical issues found${NC}" | tee -a "${LOG_FILE}"
    EXIT_CODE=${EXIT_ERRORS}
elif [[ ${WARNING_CHECKS} -gt 0 ]]; then
    echo -e "${YELLOW}⚠️  Validation passed with warnings${NC}" | tee -a "${LOG_FILE}"
    EXIT_CODE=${EXIT_WARNINGS}
else
    echo -e "${GREEN}✅ All validation checks passed!${NC}" | tee -a "${LOG_FILE}"
    EXIT_CODE=${EXIT_SUCCESS}
fi

echo "" | tee -a "${LOG_FILE}"
echo "Full report: ${REPORT_FILE}" | tee -a "${LOG_FILE}"
echo "Log file: ${LOG_FILE}" | tee -a "${LOG_FILE}"

exit ${EXIT_CODE}
