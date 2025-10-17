# Secrets Detection Tools Guide

## Overview

This guide compares popular secrets detection tools and provides usage instructions.

## Tool Comparison

| Tool | Best For | Language | Speed | False Positives |
|------|----------|----------|-------|-----------------|
| **TruffleHog** | Git history scanning | Go | Fast | Low |
| **Gitleaks** | Git + filesystem | Go | Very Fast | Very Low |
| **detect-secrets** | Pre-commit hooks | Python | Medium | Medium |
| **git-secrets** | AWS-specific | Shell | Fast | Low |

## TruffleHog

**Installation:**
```bash
brew install trufflehog  # macOS
# or
go install github.com/trufflesecurity/trufflehog/v3@latest
```

**Usage:**
```bash
# Scan filesystem
trufflehog filesystem . --json

# Scan Git repository
trufflehog git https://github.com/user/repo --json

# Scan with verification
trufflehog git https://github.com/user/repo --only-verified
```

## Gitleaks

**Installation:**
```bash
brew install gitleaks  # macOS
# or
docker pull zricethezav/gitleaks:latest
```

**Usage:**
```bash
# Detect secrets
gitleaks detect --source . --report-format json

# Protect (pre-commit)
gitleaks protect --staged

# Custom config
gitleaks detect --config .gitleaks.toml
```

**Configuration (.gitleaks.toml):**
```toml
[allowlist]
description = "Allowlist for false positives"
paths = [
    ".*test.*",
    ".*example.*"
]

[extend]
useDefault = true

[[rules]]
id = "custom-api-key"
description = "Custom API Key Pattern"
regex = '''api[_-]?key['"]?\s*[:=]\s*['"]([a-zA-Z0-9]{32,})['"]'''
```

## detect-secrets

**Installation:**
```bash
pip install detect-secrets
```

**Usage:**
```bash
# Create baseline
detect-secrets scan > .secrets.baseline

# Audit findings
detect-secrets audit .secrets.baseline

# Scan with baseline
detect-secrets scan --baseline .secrets.baseline
```

## git-secrets

**Installation:**
```bash
brew install git-secrets  # macOS
# or
git clone https://github.com/awslabs/git-secrets
cd git-secrets && make install
```

**Usage:**
```bash
# Install hooks
cd /path/to/repo
git secrets --install

# Register AWS patterns
git secrets --register-aws

# Scan
git secrets --scan
git secrets --scan-history
```

## CI/CD Integration

### GitHub Actions
```yaml
- name: Run Gitleaks
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

- name: Run TruffleHog
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./
    base: ${{ github.event.repository.default_branch }}
    head: HEAD
```

### GitLab CI
```yaml
gitleaks:
  image: zricethezav/gitleaks:latest
  script:
    - gitleaks detect --source . --report-format json
  allow_failure: false
```

## Best Practices

1. **Use Multiple Tools**: Each tool has different detection patterns
2. **Automate Scanning**: Run in CI/CD and pre-commit hooks
3. **Regular Audits**: Scan entire repository history periodically
4. **Custom Patterns**: Add organization-specific secret patterns
5. **False Positive Management**: Maintain allowlists carefully

## Common Patterns Detected

- AWS keys (Access Key ID, Secret Access Key)
- API keys (various formats)
- Private SSH keys
- Database connection strings
- OAuth tokens
- JWT secrets
- Stripe keys
- GitHub tokens
- Slack webhooks
- Password fields

## Remediation

If secrets are found in git history:

1. **Rotate immediately**: Assume compromised
2. **Remove from history**: Use `git filter-branch` or BFG Repo-Cleaner
3. **Force push**: Update remote repository
4. **Audit access**: Check for unauthorized use
5. **Add prevention**: Install pre-commit hooks
