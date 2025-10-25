#!/bin/bash
# Performance Validation Script
# Verifies token budgets and performance metrics

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "=================================="
echo "Performance Validation"
echo "=================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0
WARNINGS=0

# Function to check metric
check_metric() {
    local name="$1"
    local actual="$2"
    local threshold="$3"
    local operator="$4"  # lt, gt, eq
    local unit="$5"

    if [ "$operator" = "lt" ]; then
        if [ "$actual" -lt "$threshold" ]; then
            echo -e "${GREEN}✓${NC} $name: $actual $unit (< $threshold)"
            ((PASSED++))
        else
            echo -e "${RED}✗${NC} $name: $actual $unit (>= $threshold)"
            ((FAILED++))
        fi
    elif [ "$operator" = "gt" ]; then
        if [ "$actual" -gt "$threshold" ]; then
            echo -e "${GREEN}✓${NC} $name: $actual $unit (> $threshold)"
            ((PASSED++))
        else
            echo -e "${RED}✗${NC} $name: $actual $unit (<= $threshold)"
            ((FAILED++))
        fi
    elif [ "$operator" = "eq" ]; then
        if [ "$actual" -eq "$threshold" ]; then
            echo -e "${GREEN}✓${NC} $name: $actual $unit (= $threshold)"
            ((PASSED++))
        else
            echo -e "${RED}✗${NC} $name: $actual $unit (!= $threshold)"
            ((FAILED++))
        fi
    fi
}

check_warning() {
    local name="$1"
    local actual="$2"
    local threshold="$3"
    local operator="$4"
    local unit="$5"

    if [ "$operator" = "gt" ]; then
        if [ "$actual" -gt "$threshold" ]; then
            echo -e "${YELLOW}⚠${NC} $name: $actual $unit (> $threshold recommended)"
            ((WARNINGS++))
        else
            echo -e "${GREEN}✓${NC} $name: $actual $unit (<= $threshold)"
            ((PASSED++))
        fi
    fi
}

echo "1. Repository Structure Metrics"
echo "--------------------------------"

# Count directories
DIR_COUNT=$(find "$REPO_ROOT" -type d \
    -not -path "*/.git/*" \
    -not -path "*/node_modules/*" \
    -not -path "*/__pycache__/*" \
    -not -path "*/.venv/*" | wc -l)
check_warning "Total Directories" "$DIR_COUNT" "1000" "gt" "dirs"

# Count files
FILE_COUNT=$(find "$REPO_ROOT" -type f \
    -not -path "*/.git/*" \
    -not -path "*/node_modules/*" \
    -not -path "*/__pycache__/*" \
    -not -path "*/.venv/*" | wc -l)
check_warning "Total Files" "$FILE_COUNT" "3000" "gt" "files"

# Maximum depth
MAX_DEPTH=$(find "$REPO_ROOT" -type d \
    -not -path "*/.git/*" \
    -not -path "*/node_modules/*" \
    -printf '%d\n' 2>/dev/null | sort -rn | head -1)
check_metric "Maximum Depth" "$MAX_DEPTH" "7" "lt" "levels"

# Count markdown files
MD_COUNT=$(find "$REPO_ROOT" -name "*.md" \
    -not -path "*/.git/*" \
    -not -path "*/node_modules/*" | wc -l)
echo -e "${GREEN}ℹ${NC} Markdown Files: $MD_COUNT"

echo ""
echo "2. Skill Token Budget Validation"
echo "---------------------------------"

# Find large skills (>1500 tokens)
LARGE_SKILLS=0
if [ -d "$REPO_ROOT/skills" ]; then
    while IFS= read -r skill; do
        TOKENS=$(python3 "$SCRIPT_DIR/token-counter.py" --directory "$(dirname "$skill")" 2>/dev/null | grep "Total Tokens" | awk '{print $3}' || echo "0")
        if [ "$TOKENS" -gt 1500 ] 2>/dev/null; then
            echo -e "${YELLOW}⚠${NC} Large skill: $(basename $(dirname "$skill")): $TOKENS tokens"
            ((LARGE_SKILLS++))
            ((WARNINGS++))
        fi
    done < <(find "$REPO_ROOT/skills" -name "SKILL.md" -type f)
fi

if [ "$LARGE_SKILLS" -eq 0 ]; then
    echo -e "${GREEN}✓${NC} All skills within budget (<1500 tokens)"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠${NC} $LARGE_SKILLS skills exceed 1500 token budget"
fi

echo ""
echo "3. Token Usage Analysis"
echo "-----------------------"

# Run token counter on key directories
if [ -x "$SCRIPT_DIR/token-counter.py" ]; then
    # Docs directory
    if [ -d "$REPO_ROOT/docs/standards" ]; then
        STANDARDS_TOKENS=$(python3 "$SCRIPT_DIR/token-counter.py" \
            --directory "$REPO_ROOT/docs/standards" 2>/dev/null | \
            grep "Total Tokens" | awk '{print $3}' || echo "0")

        if [ "$STANDARDS_TOKENS" != "0" ]; then
            check_warning "Standards Tokens" "$STANDARDS_TOKENS" "300000" "gt" "tokens"
        fi
    fi

    # Skills directory
    if [ -d "$REPO_ROOT/skills" ]; then
        SKILLS_TOKENS=$(python3 "$SCRIPT_DIR/token-counter.py" \
            --directory "$REPO_ROOT/skills" 2>/dev/null | \
            grep "Total Tokens" | awk '{print $3}' || echo "0")

        if [ "$SKILLS_TOKENS" != "0" ]; then
            echo -e "${GREEN}ℹ${NC} Skills Total: $SKILLS_TOKENS tokens"
        fi
    fi
else
    echo -e "${YELLOW}⚠${NC} token-counter.py not found or not executable"
    ((WARNINGS++))
fi

echo ""
echo "4. Audit Compliance"
echo "-------------------"

# Check for orphans
if [ -f "$REPO_ROOT/reports/generated/structure-audit.json" ]; then
    ORPHANS=$(grep -o '"orphans":[0-9]*' "$REPO_ROOT/reports/generated/structure-audit.json" | cut -d: -f2 || echo "999")
    check_metric "Orphaned Files" "$ORPHANS" "5" "lt" "files"

    BROKEN=$(grep -o '"broken":[0-9]*' "$REPO_ROOT/reports/generated/structure-audit.json" | cut -d: -f2 || echo "999")
    check_metric "Broken Links" "$BROKEN" "1" "lt" "links"
else
    echo -e "${YELLOW}⚠${NC} structure-audit.json not found - run generate-audit-reports.py"
    ((WARNINGS++))
fi

echo ""
echo "=================================="
echo "Summary"
echo "=================================="
echo -e "${GREEN}Passed:${NC}   $PASSED"
echo -e "${RED}Failed:${NC}   $FAILED"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
echo ""

if [ $FAILED -gt 0 ]; then
    echo -e "${RED}VALIDATION FAILED${NC}"
    exit 1
elif [ $WARNINGS -gt 5 ]; then
    echo -e "${YELLOW}VALIDATION PASSED WITH WARNINGS${NC}"
    exit 0
else
    echo -e "${GREEN}VALIDATION PASSED${NC}"
    exit 0
fi
