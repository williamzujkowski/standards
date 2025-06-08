# Standards Integration Guide

## 🚀 Quick Start Integration

### Option 1: Direct Reference (Simplest)

Add this to your project's README.md:

```markdown
## Development Standards

This project follows the comprehensive standards defined at:
https://github.com/williamzujkowski/standards

Key standards we follow:
- [Coding Standards](https://github.com/williamzujkowski/standards/blob/master/CODING_STANDARDS.md)
- [Testing Standards](https://github.com/williamzujkowski/standards/blob/master/TESTING_STANDARDS.md) (85% coverage required)
- [Security Standards](https://github.com/williamzujkowski/standards/blob/master/MODERN_SECURITY_STANDARDS.md)
```

### Option 2: Git Submodule (Version Control)

```bash
# Add standards as submodule
git submodule add https://github.com/williamzujkowski/standards.git .standards

# Create symbolic links to key files
ln -s .standards/CLAUDE.md docs/CLAUDE.md
ln -s .standards/MASTER_PROMPT.md docs/MASTER_PROMPT.md
```

### Option 3: Project Template (Full Integration)

Use the provided setup script:

```bash
# Download and run setup script
curl -O https://raw.githubusercontent.com/williamzujkowski/standards/master/setup-project.sh
chmod +x setup-project.sh
./setup-project.sh my-new-project
```

## 📋 Integration Checklist

### Immediate Actions
- [ ] Add standards reference to README
- [ ] Copy CLAUDE.md for AI-assisted development
- [ ] Set up pre-commit hooks
- [ ] Configure linters based on CODING_STANDARDS.md
- [ ] Set up test coverage requirements (85%+)

### Project Configuration Files

#### `.pre-commit-config.yaml`
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-merge-conflict
      - id: check-yaml
      - id: check-json
```

#### `pyproject.toml` (Python example)
```toml
[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
fail_under = 85
show_missing = true

[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"
line_length = 88
```

#### `package.json` (JavaScript example)
```json
{
  "scripts": {
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "format": "prettier --write .",
    "test": "jest --coverage",
    "test:coverage": "jest --coverage --coverageThreshold='{\"global\":{\"branches\":85,\"functions\":85,\"lines\":85,\"statements\":85}}'"
  }
}
```

## 🤖 AI-Assisted Development

### Using CLAUDE.md in Your Project

1. Copy CLAUDE.md to your project:
   ```bash
   cp standards/CLAUDE.md docs/
   ```

2. When using AI tools, reference specific standards:
   ```
   I'm working on [feature]. Please follow:
   @load [CS:api-design + SEC:api-security + TS:integration]
   ```

3. Use task-based templates:
   - Bug Fix: `@load [TS:regression + CS:error-handling]`
   - New Feature: `@load [CS:architecture + TS:tdd + SEC:relevant]`
   - Performance: `@load [CS:performance + OBS:metrics]`

## 🔧 CI/CD Integration

### GitHub Actions Example

```yaml
name: Standards Compliance

on: [push, pull_request]

jobs:
  standards-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true  # If using submodules

      - name: Set up environment
        run: |
          # Language-specific setup

      - name: Lint Check
        run: make lint

      - name: Test Coverage
        run: |
          make test
          # Ensure 85% coverage per TESTING_STANDARDS.md

      - name: Security Scan
        run: make security-check
```

## 📊 Monitoring Compliance

### Key Metrics to Track

Based on the standards, monitor:

1. **Code Quality**
   - Test coverage: ≥85% (95% for critical paths)
   - Linting scores: Zero errors
   - Security vulnerabilities: Zero high/critical

2. **Performance**
   - Response time: p95 < 200ms
   - Error rate: < 0.1%
   - Core Web Vitals: All green

3. **Development Process**
   - PR review time: < 24 hours
   - Build success rate: > 95%
   - Deployment frequency: Per your goals

### Creating a Standards Dashboard

```markdown
## Project Standards Compliance

| Standard | Target | Current | Status |
|----------|--------|---------|---------|
| Test Coverage | 85% | 87% | ✅ |
| Security Score | A+ | A+ | ✅ |
| Performance (p95) | <200ms | 150ms | ✅ |
| Accessibility | WCAG 2.1 AA | AA | ✅ |
```

## 🎯 Best Practices

1. **Start Small**
   - Don't try to implement all standards at once
   - Focus on REQUIRED items first
   - Add RECOMMENDED items gradually

2. **Customize for Your Needs**
   - Document any deviations in PROJECT_STANDARDS.md
   - Explain why certain standards don't apply
   - Create project-specific extensions

3. **Keep Standards Visible**
   - Add badges to README
   - Include in onboarding docs
   - Review in retrospectives

4. **Automate Enforcement**
   - Pre-commit hooks
   - CI/CD checks
   - Automated reporting

## 🔄 Keeping Standards Updated

```bash
# If using submodules
cd .standards
git pull origin master
cd ..
git add .standards
git commit -m "Update to latest standards"

# If using direct reference
# Just check the repository periodically for updates
```

## 💡 Tips for Success

1. **Make it Easy**: Automate as much as possible
2. **Make it Visible**: Dashboard and badges
3. **Make it Valued**: Celebrate compliance wins
4. **Make it Collaborative**: Get team buy-in early

---

Remember: Standards are meant to help, not hinder. Adapt them to work for your team and project!