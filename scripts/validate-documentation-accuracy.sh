#!/bin/bash
# Validate Documentation Accuracy
# Usage: ./scripts/validate-documentation-accuracy.sh

set -e

echo "🔍 Documentation Accuracy Validation"
echo "======================================"
echo ""

ISSUES_FOUND=0

# Test 1: Check critical files exist
echo "📁 File Existence Check..."
files=(
  "CLAUDE.md"
  "README.md"
  "docs/README.md"
  "docs/SKILLS_CATALOG.md"
  "config/product-matrix.yaml"
  "scripts/generate-audit-reports.py"
  ".github/workflows/lint-and-validate.yml"
  "examples/nist-templates/quickstart/Makefile"
)

for file in "${files[@]}"; do
  if [ -f "$file" ]; then
    echo "  ✓ $file"
  else
    echo "  ✗ $file (MISSING)"
    ((ISSUES_FOUND++))
  fi
done

echo ""

# Test 2: Count skills
echo "📊 Skills Count Check..."
skill_count=$(find skills -name "SKILL.md" 2>/dev/null | wc -l)
echo "  Found: $skill_count SKILL.md files"
if [ "$skill_count" -ge 60 ]; then
  echo "  ✓ Skills count is accurate (expected 60+)"
else
  echo "  ⚠️  Skills count lower than expected (found $skill_count, expected 60+)"
  ((ISSUES_FOUND++))
fi

echo ""

# Test 3: MCP Tools
echo "🔧 MCP Tools Check..."
if command -v npx &> /dev/null; then
  tool_count=$(npx claude-flow@alpha mcp tools 2>&1 | grep -c "^  •" || echo "0")
  echo "  Found: $tool_count MCP tools"
  if [ "$tool_count" -ge 80 ]; then
    echo "  ✓ MCP tools accessible (expected 80+)"
  else
    echo "  ⚠️  Fewer tools than expected (found $tool_count, expected 80+)"
    ((ISSUES_FOUND++))
  fi
else
  echo "  ⚠️  npx not available, skipping MCP check"
fi

echo ""

# Test 4: Verify scripts are executable
echo "🔐 Script Permissions Check..."
scripts=(
  "scripts/generate-audit-reports.py"
  "scripts/validate-skills.py"
  "scripts/discover-skills.py"
  "scripts/ensure-hub-links.py"
)

for script in "${scripts[@]}"; do
  if [ -x "$script" ]; then
    echo "  ✓ $script (executable)"
  elif [ -f "$script" ]; then
    echo "  ⚠️  $script (exists but not executable, use: chmod +x $script)"
  else
    echo "  ✗ $script (MISSING)"
    ((ISSUES_FOUND++))
  fi
done

echo ""

# Test 5: Check for problematic claims
echo "⚠️  Checking for Exaggerations & Inaccuracies..."

# Check for "Battle-tested"
if grep -q "Battle-tested" README.md 2>/dev/null; then
  echo "  ⚠️  Found 'Battle-tested' in README.md (unverifiable claim)"
  ((ISSUES_FOUND++))
fi

# Check for specific performance percentages
if grep -q "50% reduction" docs/README.md 2>/dev/null; then
  echo "  ⚠️  Found specific performance claims in docs/README.md (unverified)"
  ((ISSUES_FOUND++))
fi

# Check for agent count without clarification
if grep -q "Available Agents (49 Total)" CLAUDE.md 2>/dev/null; then
  echo "  ⚠️  Found agent count claim without clarification in CLAUDE.md"
  ((ISSUES_FOUND++))
fi

# Check for npm commands without package.json
if grep -q "npm run build" CLAUDE.md 2>/dev/null && [ ! -f "package.json" ]; then
  echo "  ⚠️  Found npm commands in CLAUDE.md but no package.json exists"
  ((ISSUES_FOUND++))
fi

# Check skills catalog count
if grep -q "Total Skills\*\*: 5" docs/SKILLS_CATALOG.md 2>/dev/null; then
  echo "  ⚠️  Skills catalog claims 5 total skills (actual: $skill_count)"
  ((ISSUES_FOUND++))
fi

# Check for "99%+ token reduction" without context
if grep -q "99%+ token reduction" README.md 2>/dev/null; then
  if ! grep -q "baseline" README.md 2>/dev/null; then
    echo "  ⚠️  Token reduction claim lacks baseline context"
    ((ISSUES_FOUND++))
  fi
fi

echo ""

# Test 6: Verify CI workflows
echo "🔄 CI/CD Workflow Check..."
workflow_count=$(ls -1 .github/workflows/*.yml 2>/dev/null | wc -l)
echo "  Found: $workflow_count workflow files"
if [ "$workflow_count" -ge 10 ]; then
  echo "  ✓ Comprehensive CI/CD setup"
else
  echo "  ⚠️  Fewer workflows than expected"
fi

echo ""

# Test 7: Check NIST quickstart
echo "🔒 NIST Quickstart Check..."
if [ -f "examples/nist-templates/quickstart/Makefile" ]; then
  echo "  ✓ NIST quickstart Makefile exists"
  if grep -q "nist-check" "examples/nist-templates/quickstart/Makefile" 2>/dev/null; then
    echo "  ✓ NIST check target defined"
  else
    echo "  ⚠️  NIST check target not found in Makefile"
  fi
else
  echo "  ✗ NIST quickstart Makefile missing"
  ((ISSUES_FOUND++))
fi

echo ""

# Summary
echo "================================"
echo "📊 VALIDATION SUMMARY"
echo "================================"
echo ""

if [ $ISSUES_FOUND -eq 0 ]; then
  echo "✅ All checks passed! Documentation appears accurate."
  exit_code=0
elif [ $ISSUES_FOUND -le 3 ]; then
  echo "⚠️  Minor issues found: $ISSUES_FOUND"
  echo "    Review warnings above and consider updates."
  exit_code=0
else
  echo "❌ Significant issues found: $ISSUES_FOUND"
  echo "    Review the audit report for detailed corrections."
  exit_code=1
fi

echo ""
echo "📄 For detailed audit report, see:"
echo "   reports/generated/documentation-accuracy-audit.md"
echo ""
echo "📝 For specific corrections, see:"
echo "   reports/generated/documentation-corrections-checklist.md"
echo ""

exit $exit_code
