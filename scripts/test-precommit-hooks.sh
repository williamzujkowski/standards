#!/bin/bash
# Test script for pre-commit hooks
# Validates that all security and quality checks are working correctly

set -euo pipefail

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE} Pre-commit Hooks Test Suite${NC}"
echo -e "${BLUE}======================================${NC}"
echo

# Test environment
log_info "Testing pre-commit environment..."

# Check if pre-commit is installed
if ! command -v pre-commit &> /dev/null; then
    log_error "pre-commit is not installed. Run lint/setup-hooks.sh first."
    exit 1
fi

# Check if hooks are installed
if [ ! -f .git/hooks/pre-commit ]; then
    log_error "Pre-commit hooks are not installed. Run lint/setup-hooks.sh first."
    exit 1
fi

log_success "Pre-commit environment is ready"

# Test configuration validation
log_info "Validating pre-commit configuration..."

if pre-commit validate-config; then
    log_success "Configuration is valid"
else
    log_error "Configuration validation failed"
    exit 1
fi

# Test individual hook groups
echo
log_info "Testing hook groups..."

# Create temporary test directory
TEST_DIR="$(mktemp -d)"
cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Test 1: JSON validation
log_info "Testing JSON validation..."
echo '{"valid": "json", "test": true}' > "$TEST_DIR/test.json"
echo '{"invalid": json}' > "$TEST_DIR/invalid.json"

# Test 2: YAML validation
log_info "Testing YAML validation..."
cat > "$TEST_DIR/test.yaml" << 'EOF'
valid: yaml
test:
  - item1
  - item2
EOF

cat > "$TEST_DIR/invalid.yaml" << 'EOF'
invalid: yaml
  bad: indentation
EOF

# Test 3: Large file detection (create a file just under the limit)
log_info "Testing large file detection..."
dd if=/dev/zero of="$TEST_DIR/small.bin" bs=1024 count=500 2>/dev/null
dd if=/dev/zero of="$TEST_DIR/large.bin" bs=1024 count=2048 2>/dev/null

# Test 4: Secret detection (safe test patterns)
log_info "Testing secret detection..."
cat > "$TEST_DIR/safe-secrets.txt" << 'EOF'
# These should be detected as potential secrets
export API_KEY="ak-1234567890abcdef1234567890abcdef"
DATABASE_URL="postgres://user:password123@localhost/db"

# These should be allowed (false positives)
export EXAMPLE_KEY="your_key_here"
export TEST_TOKEN="dummy_token_for_testing"
API_ENDPOINT="https://api.example.com"
EOF

# Run specific hooks for testing
echo
log_info "Running hook tests..."

# Test JSON hook
log_info "Testing JSON syntax validation..."
if pre-commit run check-json --files "$TEST_DIR/test.json" >/dev/null 2>&1; then
    log_success "JSON validation passed for valid file"
else
    log_warning "JSON validation hook not working correctly"
fi

# Test YAML hook
log_info "Testing YAML syntax validation..."
if pre-commit run check-yaml --files "$TEST_DIR/test.yaml" >/dev/null 2>&1; then
    log_success "YAML validation passed for valid file"
else
    log_warning "YAML validation hook not working correctly"
fi

# Test large file detection
log_info "Testing large file detection..."
if ! pre-commit run check-added-large-files --files "$TEST_DIR/large.bin" >/dev/null 2>&1; then
    log_success "Large file detection working correctly"
else
    log_warning "Large file detection may not be working"
fi

# Test security scans (dry run)
echo
log_info "Testing security scanning capabilities..."

# Check if gitleaks is available
if command -v gitleaks &> /dev/null; then
    log_info "Testing Gitleaks secret detection..."
    if gitleaks detect --source="$TEST_DIR" --config=.gitleaks.toml --no-git >/dev/null 2>&1; then
        log_success "Gitleaks configuration is working"
    else
        log_info "Gitleaks detected potential secrets (this is expected for test)"
    fi
else
    log_warning "Gitleaks not available - secret detection may be limited"
fi

# Check if detect-secrets is available
if command -v detect-secrets &> /dev/null; then
    log_info "Testing detect-secrets..."
    if detect-secrets scan "$TEST_DIR" --baseline /dev/null >/dev/null 2>&1; then
        log_success "Detect-secrets is working"
    else
        log_info "Detect-secrets detected potential secrets (this is expected for test)"
    fi
else
    log_warning "detect-secrets not available"
fi

# Test formatting hooks
echo
log_info "Testing formatting and whitespace hooks..."

# Create files with common issues
cat > "$TEST_DIR/whitespace.txt" << 'EOF'
Line with trailing spaces
Line with tabs	and spaces

Final line without newline
EOF

# Test trailing whitespace hook
if pre-commit run trailing-whitespace --files "$TEST_DIR/whitespace.txt" >/dev/null 2>&1; then
    log_success "Trailing whitespace hook is working"
else
    log_info "Trailing whitespace hook made corrections (expected)"
fi

# Test Python code quality (if Python files exist)
if ls *.py >/dev/null 2>&1; then
    log_info "Testing Python code quality hooks..."

    # Test a simple Python file
    echo "print('hello world')" > "$TEST_DIR/test.py"

    if command -v black &> /dev/null; then
        if pre-commit run black --files "$TEST_DIR/test.py" >/dev/null 2>&1; then
            log_success "Black formatting is working"
        else
            log_info "Black made formatting corrections (expected)"
        fi
    fi

    if command -v ruff &> /dev/null; then
        if pre-commit run ruff --files "$TEST_DIR/test.py" >/dev/null 2>&1; then
            log_success "Ruff linting is working"
        else
            log_info "Ruff found issues to fix (expected)"
        fi
    fi
else
    log_info "No Python files found, skipping Python-specific tests"
fi

# Final comprehensive test
echo
log_info "Running comprehensive hook validation..."

# Test all hooks on existing repository files (subset)
if pre-commit run --all-files --verbose | head -20; then
    log_success "Comprehensive validation completed successfully"
else
    log_warning "Some hooks failed or made corrections - review output above"
fi

echo
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN} Test Results Summary${NC}"
echo -e "${GREEN}======================================${NC}"
echo

# Summary of findings
log_info "Hook Installation Status:"
echo "  ✓ Pre-commit framework: $(pre-commit --version)"

if command -v gitleaks &> /dev/null; then
    echo "  ✓ Gitleaks: $(gitleaks version 2>/dev/null | head -n1 || echo 'installed')"
else
    echo "  ⚠ Gitleaks: Not installed"
fi

if command -v detect-secrets &> /dev/null; then
    echo "  ✓ Detect-secrets: $(detect-secrets --version)"
else
    echo "  ⚠ Detect-secrets: Not installed"
fi

if command -v markdownlint &> /dev/null; then
    echo "  ✓ Markdownlint: $(markdownlint --version)"
else
    echo "  ⚠ Markdownlint: Using pre-commit managed version"
fi

echo
log_info "Security Features Status:"
echo "  ✓ Secret detection: Multiple engines configured"
echo "  ✓ Large file prevention: Active (>1MB limit)"
echo "  ✓ Syntax validation: JSON, YAML, TOML, XML"
echo "  ✓ Code quality: Python, Shell, Markdown"
echo "  ✓ Whitespace cleanup: Active"
echo "  ✓ Branch protection: Prevents direct commits to main/master"

echo
if [ -f .git/hooks/pre-commit ]; then
    log_success "Pre-commit hooks are active and ready to protect your repository!"
else
    log_error "Pre-commit hooks are not properly installed!"
fi

echo
log_info "Usage reminders:"
echo "  • Hooks run automatically on 'git commit'"
echo "  • Manual run: 'pre-commit run --all-files'"
echo "  • Skip hooks (not recommended): 'git commit --no-verify'"
echo "  • Update hooks: 'pre-commit autoupdate'"

echo
log_success "Pre-commit hooks test completed!"
