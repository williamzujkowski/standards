# NIST Compliance Validation Run

**Version:** 1.0.0  
**Last Updated:** 2025-08-23

## Overview

This document provides step-by-step instructions to validate the NIST 800-53r5 control tagging implementation, including local development hooks and CI/CD integration.

## Prerequisites

- Git repository with standards installed
- Python 3.8+ (for the example)
- Make command available
- Write access to `.git/hooks/` directory

## Local Validation Steps

### 1. Install NIST Hooks

```bash
# From repository root
./scripts/setup-nist-hooks.sh
```

Expected output:
```
🔧 Setting up NIST compliance git hooks...
Installing pre-commit hook...
Setting up commit message template...
✅ NIST compliance hooks installed successfully!
```

### 2. Test the Quickstart Example

```bash
# Navigate to quickstart
cd examples/nist-templates/quickstart

# Run NIST compliance check
make nist-check
```

Expected output:
```
Checking NIST control tags...
=================================
Checking for NIST annotations in security code...
[Shows lines with @nist tags]

Security patterns found:
  Security-related lines: 150+

NIST control coverage:
  Unique NIST controls: 14
  ac-12, ac-2, ac-3, ac-6, ac-7, au-2, au-3, ia-2, ia-5, ia-8, sc-13, si-10, si-11

Validation result:
  ✅ NIST tags present
```

### 3. Test Git Hook Behavior

```bash
# Make a change to trigger the hook
echo "# Test comment" >> auth-service.py

# Stage the file
git add auth-service.py

# Attempt commit (hook will run)
git commit -m "Test NIST hook"
```

Expected hook output:
```
🔍 NIST 800-53r5 Compliance Check
=================================
✓ auth-service.py (has NIST tags)

📊 Summary
==========
Files checked: 1
Files with security code: 1
Files missing NIST tags: 0
Warnings: 0
Errors: 0

✅ All NIST compliance checks passed
```

### 4. Test Missing Tags Detection

Create a test file without tags:

```bash
cat > test_security.py << 'EOF'
def authenticate_user(username, password):
    """Login function without NIST tags."""
    # This should trigger a warning
    return check_password(username, password)
EOF

git add test_security.py
git commit -m "Add security code"
```

Expected warning:
```
⚠️  Security code without NIST tags: test_security.py
  Suggested NIST controls:
  - @nist ia-2 "User authentication"
  - @nist ia-5 "Authenticator management"

⚠️  Proceeding with warnings
  Consider adding NIST tags to security-related code
```

### 5. Full Validation Suite

```bash
cd examples/nist-templates/quickstart
make validate
```

Expected output:
```
Running linters...
Running tests...
..........
----------------------------------------------------------------------
Ran 10 tests in 0.XXXs
OK

Checking NIST control tags...
[Details as above]
=================================
✅ All validation checks passed!
```

## CI/CD Validation

### GitHub Actions Integration

Add this job to `.github/workflows/nist-compliance.yml`:

```yaml
name: NIST Compliance Check

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  nist-compliance:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pylint black
    
    - name: Run NIST quickstart validation
      run: |
        cd examples/nist-templates/quickstart
        make ci
    
    - name: Check for NIST tags in changed files
      if: github.event_name == 'pull_request'
      run: |
        # Get changed files
        changed_files=$(git diff --name-only origin/${{ github.base_ref }}...HEAD | grep -E '\.(py|js|ts|go|java)$' || true)
        
        if [ -n "$changed_files" ]; then
          echo "Checking NIST tags in changed files..."
          for file in $changed_files; do
            if grep -q "auth\|password\|encrypt\|session\|permission" "$file"; then
              if ! grep -q "@nist" "$file"; then
                echo "⚠️  Security code without NIST tags: $file"
                echo "::warning file=$file::Security code detected without NIST control tags"
              fi
            fi
          done
        fi
```

### Local CI Simulation

Test the CI workflow locally:

```bash
# From repository root
cd examples/nist-templates/quickstart

# Run CI target
make ci
```

Expected output:
```
Installing dependencies...
Running linters...
Running tests...
Checking NIST control tags...
=================================
✅ All validation checks passed!
CI validation complete
```

## Validation Checklist

### ✅ Local Development
- [ ] NIST hooks installed (`./scripts/setup-nist-hooks.sh`)
- [ ] Pre-commit hook triggers on git commit
- [ ] Warnings shown for security code without tags
- [ ] Commit message includes detected NIST controls
- [ ] VS Code extension provides suggestions (if installed)

### ✅ Quickstart Example
- [ ] `make nist-check` shows 14+ unique controls
- [ ] `make test` passes all tests
- [ ] `make validate` completes successfully
- [ ] Example service runs (`make run`)

### ✅ CI/CD Pipeline
- [ ] GitHub Actions workflow configured
- [ ] CI checks run on pull requests
- [ ] Warnings generated for missing tags
- [ ] Build passes with tagged security code

## Troubleshooting

### Hook Not Running

```bash
# Check hook is executable
ls -la .git/hooks/pre-commit
# Should show: -rwxr-xr-x

# Make executable if needed
chmod +x .git/hooks/pre-commit
```

### False Positives

If non-security code triggers warnings:

```bash
# Adjust sensitivity
export SUGGEST_TAGS=false  # Disable suggestions
export BLOCK_ON_MISSING=false  # Don't block commits
```

### CI Failures

Check the logs for:
1. Missing dependencies (install in workflow)
2. Path issues (use correct relative paths)
3. Permission errors (ensure scripts are executable)

## Success Criteria

The NIST implementation is validated when:

1. **Local hooks work**: Pre-commit checks run automatically
2. **Tags are present**: Security code has appropriate NIST controls
3. **Tests pass**: All compliance tests succeed
4. **CI runs**: Automated checks work in pull requests
5. **Documentation exists**: Control mappings are documented

## Next Steps

After successful validation:

1. **Extend coverage**: Add NIST tags to existing security code
2. **Write more tests**: Validate each control implementation
3. **Generate reports**: Use tags to create compliance documentation
4. **Train team**: Share this guide with developers
5. **Monitor compliance**: Track coverage metrics over time

## Resources

- [NIST 800-53r5 Controls](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [Quickstart Example](../../examples/nist-templates/quickstart/)
- [Implementation Guide](../../docs/nist/NIST_IMPLEMENTATION_GUIDE.md)
- [Annotation Framework](../../standards/compliance/ANNOTATION_FRAMEWORK.md)
- [Setup Script](../../scripts/setup-nist-hooks.sh)