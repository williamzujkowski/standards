# Verification Guide for Standards Router Implementation

## Quick Verification Script

Copy and run this complete verification script:

```bash
#!/bin/bash
# Standards Router Verification Script
# Run from repository root

set -e

echo "========================================="
echo "  Standards Router Verification"
echo "  Date: $(date)"
echo "========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Counters
PASS=0
FAIL=0
WARN=0

# Function to check result
check_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}❌ $2${NC}"
        FAIL=$((FAIL + 1))
    fi
}

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅ Found: $1${NC}"
        PASS=$((PASS + 1))
        return 0
    else
        echo -e "${RED}❌ Missing: $1${NC}"
        FAIL=$((FAIL + 1))
        return 1
    fi
}

echo "1️⃣  Checking Core Files"
echo "------------------------"
check_file "config/product-matrix.yaml"
check_file "docs/guides/USING_PRODUCT_MATRIX.md"
check_file "scripts/generate-standards-inventory.py"
check_file "scripts/generate-audit-reports.py"
check_file ".github/workflows/lint-and-validate.yml"
echo ""

echo "2️⃣  Checking NIST Quickstart"
echo "----------------------------"
check_file "examples/nist-templates/quickstart/auth-service.py"
check_file "examples/nist-templates/quickstart/test_auth_service.py"
check_file "examples/nist-templates/quickstart/Makefile"
check_file "examples/nist-templates/quickstart/README.md"
check_file "prompts/nist-compliance/VALIDATION_RUN.md"
echo ""

echo "3️⃣  Generating Standards Inventory"
echo "----------------------------------"
if python3 scripts/generate-standards-inventory.py 2>/dev/null; then
    if [ -f "reports/generated/standards-inventory.json" ]; then
        COUNT=$(python3 -c "import json; print(json.load(open('reports/generated/standards-inventory.json'))['summary']['total_documents'])")
        echo -e "${GREEN}✅ Generated inventory with $COUNT standards${NC}"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}❌ Inventory file not created${NC}"
        FAIL=$((FAIL + 1))
    fi
else
    echo -e "${RED}❌ Inventory generation failed${NC}"
    FAIL=$((FAIL + 1))
fi
echo ""

echo "4️⃣  Validating Product Matrix"
echo "-----------------------------"
if [ -f "config/product-matrix.yaml" ]; then
    # Check YAML is valid (basic check)
    if python3 -c "import yaml; yaml.safe_load(open('config/product-matrix.yaml'))" 2>/dev/null; then
        PRODUCTS=$(grep '^  [a-z-]*:' config/product-matrix.yaml | wc -l)
        echo -e "${GREEN}✅ Valid YAML with $PRODUCTS product types${NC}"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}❌ Invalid YAML syntax${NC}"
        FAIL=$((FAIL + 1))
    fi
else
    echo -e "${RED}❌ Product matrix not found${NC}"
    FAIL=$((FAIL + 1))
fi
echo ""

echo "5️⃣  Testing NIST Quickstart"
echo "---------------------------"
cd examples/nist-templates/quickstart 2>/dev/null || {
    echo -e "${RED}❌ Quickstart directory not found${NC}"
    FAIL=$((FAIL + 1))
}

if [ -f "Makefile" ]; then
    # Test NIST check
    if make nist-check 2>/dev/null | grep -q "NIST tags present"; then
        echo -e "${GREEN}✅ NIST tags validated${NC}"
        PASS=$((PASS + 1))
    else
        echo -e "${YELLOW}⚠️  NIST validation issues${NC}"
        WARN=$((WARN + 1))
    fi
    
    # Test Python syntax
    if python3 -m py_compile auth-service.py 2>/dev/null; then
        echo -e "${GREEN}✅ Python syntax valid${NC}"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}❌ Python syntax errors${NC}"
        FAIL=$((FAIL + 1))
    fi
fi
cd - > /dev/null 2>&1
echo ""

echo "6️⃣  Checking Router Integration"
echo "-------------------------------"
if grep -q "@load product:" CLAUDE.md 2>/dev/null; then
    echo -e "${GREEN}✅ Router fast-path added to CLAUDE.md${NC}"
    PASS=$((PASS + 1))
else
    echo -e "${RED}❌ Router integration missing in CLAUDE.md${NC}"
    FAIL=$((FAIL + 1))
fi

if grep -q "config/product-matrix.yaml" docs/guides/KICKSTART_PROMPT.md 2>/dev/null; then
    echo -e "${GREEN}✅ Kickstart references product matrix${NC}"
    PASS=$((PASS + 1))
else
    echo -e "${YELLOW}⚠️  Kickstart not updated with matrix reference${NC}"
    WARN=$((WARN + 1))
fi
echo ""

echo "7️⃣  Running Audit Reports"
echo "------------------------"
if python3 scripts/generate-audit-reports.py 2>/dev/null; then
    if [ -f "reports/generated/linkcheck.txt" ] && [ -f "reports/generated/structure-audit.md" ]; then
        echo -e "${GREEN}✅ Audit reports generated${NC}"
        PASS=$((PASS + 1))
        
        # Check for broken links
        BROKEN=$(grep "Broken links:" reports/generated/linkcheck.txt | grep -o "[0-9]*")
        if [ "$BROKEN" = "0" ]; then
            echo -e "${GREEN}✅ No broken links found${NC}"
            PASS=$((PASS + 1))
        else
            echo -e "${YELLOW}⚠️  $BROKEN broken links detected${NC}"
            WARN=$((WARN + 1))
        fi
    else
        echo -e "${RED}❌ Audit reports not created${NC}"
        FAIL=$((FAIL + 1))
    fi
else
    echo -e "${RED}❌ Audit report generation failed${NC}"
    FAIL=$((FAIL + 1))
fi
echo ""

echo "8️⃣  Checking Git Hooks"
echo "---------------------"
if [ -f "scripts/setup-nist-hooks.sh" ]; then
    if [ -x "scripts/setup-nist-hooks.sh" ]; then
        echo -e "${GREEN}✅ NIST hooks script is executable${NC}"
        PASS=$((PASS + 1))
    else
        echo -e "${YELLOW}⚠️  NIST hooks script not executable${NC}"
        WARN=$((WARN + 1))
    fi
else
    echo -e "${RED}❌ NIST hooks script missing${NC}"
    FAIL=$((FAIL + 1))
fi
echo ""

echo "========================================="
echo "  VERIFICATION SUMMARY"
echo "========================================="
echo -e "${GREEN}Passed:${NC} $PASS"
echo -e "${YELLOW}Warnings:${NC} $WARN"
echo -e "${RED}Failed:${NC} $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}🎉 All critical checks passed!${NC}"
    echo "The standards router implementation is ready."
    exit 0
else
    echo -e "${RED}❌ Some checks failed. Please review above.${NC}"
    exit 1
fi
```

## Manual Verification Steps

### 1. Standards Inventory

```bash
# Generate and check inventory
python3 scripts/generate-standards-inventory.py

# Verify output
jq '.summary' reports/generated/standards-inventory.json

# Expected output:
# {
#   "total_documents": 46,
#   "categories": 37,
#   "nist_enabled": 3,
#   ...
# }
```

### 2. Product Matrix

```bash
# Check matrix exists and is valid
cat config/product-matrix.yaml | head -30

# Count product types
grep '^  [a-z-]*:' config/product-matrix.yaml | wc -l
# Expected: 10

# Validate YAML
python3 -c "import yaml; yaml.safe_load(open('config/product-matrix.yaml'))"
# Expected: No errors
```

### 3. NIST Quickstart

```bash
cd examples/nist-templates/quickstart

# Run all validation
make validate

# Check NIST tags specifically
make nist-check

# Run tests
make test

# Expected: All pass
```

### 4. Router Integration

```bash
# Check CLAUDE.md has fast-path
grep -A5 "Fast Path" CLAUDE.md

# Check KICKSTART_PROMPT.md references matrix
grep "product-matrix.yaml" docs/guides/KICKSTART_PROMPT.md

# Expected: Both files updated
```

### 5. Git Hooks

```bash
# Install hooks
./scripts/setup-nist-hooks.sh

# Check installation
ls -la .git/hooks/pre-commit
# Expected: File exists and is executable

# Test hook (optional)
echo "# test" >> test.py
git add test.py
git commit -m "test"
# Expected: Hook runs
```

### 6. CI/CD Workflow

```bash
# Check workflow exists
cat .github/workflows/lint-and-validate.yml | head -20

# Validate YAML
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/lint-and-validate.yml'))"
# Expected: Valid YAML
```

## Diffstat

```bash
# Get change summary
git diff --stat
```

Expected output showing:
- ~18 new files
- ~2 modified files
- ~2000+ lines added

## Common Issues and Solutions

### Issue: Python module not found

```bash
# Install required modules
pip install pyyaml
```

### Issue: Scripts not executable

```bash
# Make scripts executable
chmod +x scripts/*.py scripts/*.sh
```

### Issue: Inventory generation fails

```bash
# Check Python version
python3 --version
# Required: 3.8+

# Run with debug
python3 -u scripts/generate-standards-inventory.py
```

### Issue: NIST tests fail

```bash
# Install test dependencies
cd examples/nist-templates/quickstart
pip install pytest
make test
```

## Success Criteria

✅ All files in place  
✅ Standards inventory generates (46 documents)  
✅ Product matrix valid (10 product types)  
✅ NIST quickstart works  
✅ Router integrated in CLAUDE.md  
✅ Kickstart references matrix  
✅ Audit reports generate  
✅ CI/CD workflow configured  

## Support

If verification fails, check:

1. File permissions (scripts executable)
2. Python version (3.8+ required)
3. Working directory (run from repo root)
4. Git status (all files committed)

---

**Verification complete when all checks pass!** 🚀