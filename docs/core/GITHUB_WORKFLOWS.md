# GitHub Actions Workflows Documentation

**Version:** 1.0.0  
**Last Updated:** January 2025  
**Status:** Active

---

## 📋 Overview

This document provides comprehensive documentation for all GitHub Actions workflows in the standards repository. These workflows automate compliance checking, validation, and maintenance tasks.

---

## 🚀 Workflow Details

### 1. Standards Compliance (`standards-compliance.yml`)

**Purpose:** Validates that all code and documentation adheres to the defined standards.

**Triggers:**
- Push to any branch
- Pull request to main/master
- Manual dispatch

**Key Steps:**
1. Checkout code
2. Set up Python environment
3. Run standards linter (`lint/standards-linter.py`)
4. Check cross-references
5. Validate metadata consistency
6. Report compliance score

**Failure Conditions:**
- Missing required metadata in standards files
- Broken cross-references
- Non-compliant code formatting
- Missing implementation sections

---

### 2. NIST Compliance (`nist-compliance.yml`)

**Purpose:** Checks NIST 800-53r5 control coverage and validates control tagging.

**Triggers:**
- Push to branches with security-related changes
- Pull request affecting security code
- Manual dispatch

**Key Steps:**
1. Parse code for @nist annotations
2. Validate control IDs against NIST catalog
3. Check control implementation completeness
4. Generate coverage report
5. Update compliance dashboard

**Outputs:**
- Control coverage percentage
- Missing controls report
- Evidence inventory
- SSP update recommendations

---

### 3. Standards Validation (`standards-validation.yml`)

**Purpose:** Runs comprehensive validation tests on the standards framework.

**Triggers:**
- Push to main branch
- Pull request
- Daily schedule (2 AM UTC)

**Key Steps:**
1. Run knowledge management validation
2. Check token efficiency
3. Validate MANIFEST.yaml
4. Test loading patterns
5. Verify examples compile

**Test Suite:**
```bash
tests/validate_knowledge_management.sh
tests/validate_cross_references.py
tests/validate_token_efficiency.py
```

---

### 4. Redundancy Check (`redundancy-check.yml`)

**Purpose:** Detects code duplication and ensures DRY principles.

**Triggers:**
- Pull request
- Weekly schedule (Mondays)

**Key Steps:**
1. Run `test_redundancy.py`
2. Analyze for duplicate code blocks
3. Check for repeated documentation
4. Generate redundancy report
5. Suggest consolidation opportunities

**Thresholds:**
- Fail if >10% redundancy in any file
- Warn if >5% redundancy across files

---

### 5. Auto-Fix Whitespace (`auto-fix-whitespace.yml`)

**Purpose:** Automatically removes trailing whitespace and fixes line endings.

**Triggers:**
- Push to any branch (if enabled)
- Manual dispatch

**Key Steps:**
1. Run `fix_trailing_whitespace.sh`
2. Check for changes
3. Commit fixes if found
4. Push to branch

**Configuration:**
- Can be disabled via `.github/no-auto-fix` file
- Respects `.gitignore` patterns
- Preserves intentional whitespace in code blocks

---

### 6. Auto Summaries (`auto-summaries.yml`)

**Purpose:** Generates periodic summaries and reports.

**Triggers:**
- Weekly schedule (Sundays at midnight UTC)
- Monthly on the 1st
- Manual dispatch

**Key Steps:**
1. Analyze recent changes
2. Generate compliance trends
3. Create usage statistics
4. Update dashboard metrics
5. Post summary to discussions/wiki

**Reports Generated:**
- Weekly compliance summary
- Monthly standards adoption metrics
- Quarterly trend analysis

---

## 🔧 Configuration

### Environment Variables

```yaml
GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
NIST_API_KEY: ${{ secrets.NIST_API_KEY }}  # Optional
SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}  # For notifications
```

### Workflow Permissions

All workflows require:
- `contents: read` - Read repository
- `contents: write` - For auto-fix workflows
- `pull-requests: write` - For PR comments
- `issues: write` - For creating issues

---

## 📊 Workflow Matrix

| Workflow | PR Required | Auto-Fix | Blocking | Schedule |
|----------|-------------|----------|----------|----------|
| Standards Compliance | ✅ | ❌ | ✅ | ❌ |
| NIST Compliance | ✅ | ❌ | ✅ | ❌ |
| Standards Validation | ✅ | ❌ | ✅ | Daily |
| Redundancy Check | ✅ | ❌ | ⚠️ | Weekly |
| Auto-Fix Whitespace | ❌ | ✅ | ❌ | ❌ |
| Auto Summaries | ❌ | ❌ | ❌ | Weekly |

---

## 🚨 Troubleshooting

### Common Issues

1. **Workflow not triggering**
   - Check branch protection rules
   - Verify workflow file syntax
   - Ensure proper permissions

2. **Tests failing intermittently**
   - Check for race conditions
   - Verify external dependencies
   - Review timeout settings

3. **Auto-fix creating loops**
   - Add `[skip ci]` to commit messages
   - Configure branch exclusions
   - Set maximum retry limits

### Debug Mode

Enable debug logging:
```yaml
env:
  ACTIONS_RUNNER_DEBUG: true
  ACTIONS_STEP_DEBUG: true
```

---

## 🔗 Integration

### With Pre-commit Hooks

Workflows complement local pre-commit hooks:
```bash
# Local validation
pre-commit run --all-files

# Same checks run in CI
.github/workflows/standards-compliance.yml
```

### With VS Code Extension

The NIST compliance workflow uses the same parser as the VS Code extension for consistency.

### With Compliance Platform

Workflows can trigger compliance platform actions:
```bash
cd standards/compliance
./quickstart.sh --github-action
```

---

## 📈 Metrics and Monitoring

Track workflow performance:
- Average runtime per workflow
- Success/failure rates
- Most common failure reasons
- Time to fix after failure

Access metrics:
- GitHub Actions tab
- Workflow run history
- API: `GET /repos/{owner}/{repo}/actions/runs`

---

## 🔐 Security Considerations

1. **Secrets Management**
   - Use GitHub Secrets for sensitive data
   - Rotate keys regularly
   - Limit secret access by environment

2. **Third-party Actions**
   - Pin to specific versions
   - Review action code
   - Use official actions when possible

3. **Permissions**
   - Use least privilege principle
   - Scope permissions per job
   - Audit workflow permissions regularly

---

## 🎯 Best Practices

1. **Keep workflows focused** - One purpose per workflow
2. **Use caching** - Cache dependencies for faster runs
3. **Fail fast** - Exit early on critical failures
4. **Provide context** - Clear error messages and fix suggestions
5. **Monitor costs** - Track Actions minutes usage

---

## 📚 Related Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [CONTRIBUTING.md](./docs/core/CONTRIBUTING.md) - How workflows affect contributions
- [tests/README.md](./tests/README.md) - Test suite documentation
- .github/workflows/ - Workflow source files directory
