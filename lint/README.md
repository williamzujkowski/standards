# Standards Repository Linting System

This directory contains comprehensive linting tools to enforce standards compliance based on `KNOWLEDGE_MANAGEMENT_STANDARDS.md`.

## 🚀 Quick Start

### Setup Pre-commit Hooks

```bash
cd lint
./setup-hooks.sh
```

This will install and configure all linting tools automatically.

### Manual Linting

```bash
# Run Python linter
python lint/standards-linter.py

# Run specific checks
markdownlint --config .markdownlint.yaml *.md
yamllint -c .yamllint.yaml *.yaml

# Run all pre-commit checks
pre-commit run --all-files
```

## 📋 Linting Components

### 1. Markdown Linting (`.markdownlint.yaml`)

- General markdown formatting rules
- Customized for standards documents
- Allows [REQUIRED]/[RECOMMENDED] emphasis patterns
- Permits longer lines for comprehensive documentation

### 2. Custom Standards Linter (`standards-linter.py`)

Enforces repository-specific rules:

- **Metadata Requirements**
  - Version (semantic versioning)
  - Last Updated (YYYY-MM-DD format)
  - Status (Active/Draft/Deprecated)
  - Standard Code (2-4 letters)

- **Structure Requirements**
  - Table of Contents
  - Overview section
  - Implementation section
  - Implementation Checklist

- **Content Quality**
  - [REQUIRED]/[RECOMMENDED] tags
  - Cross-reference validity
  - Descriptive link text
  - Code examples with language specifiers

- **Token Efficiency**
  - Document size warnings (>15k tokens)
  - Section size warnings (>3k tokens)
  - Progressive disclosure recommendations

### 3. Pre-commit Hooks (`.pre-commit-config.yaml`)

Automatically runs before each commit:

- **File Checks**
  - Trailing whitespace removal
  - End-of-file fixing
  - YAML validation
  - Large file detection
  - Merge conflict detection

- **Security**
  - Private key detection
  - Secrets scanning

- **Code Quality**
  - Python formatting (black)
  - Import sorting (isort)
  - Linting (ruff)
  - Shell script checking

- **Standards Compliance**
  - Metadata validation
  - Cross-reference checking
  - MANIFEST.yaml validation
  - Token efficiency analysis

### 4. YAML Linting (`.yamllint.yaml`)

- Consistent indentation (2 spaces)
- Line length limits
- Proper spacing rules

## 🔧 Custom Rules

### JavaScript Rules (`custom-rules.js`)

Node.js-based custom rules for:

- Version metadata validation
- Section requirement checking
- Cross-reference validation
- MANIFEST.yaml inclusion
- Token efficiency analysis

### Python Linter Features

The Python linter provides:

- Comprehensive rule checking
- Multiple output formats (text, JSON)
- Detailed fix suggestions
- Severity levels (error, warning, info)
- File-by-file reporting

## 📊 Linting Reports

### Text Format (Default)

```
Standards Linting Report
==================================================
Files checked: 25
Issues found: 48
  Errors: 12
  Warnings: 30
  Info: 6

CODING_STANDARDS.md:
  1:1 ✗ [metadata-version] Missing or invalid version metadata
       Fix: Add: **Version:** X.Y.Z
  156:121 ⚠ [format-line-length] Line too long (145 > 120)
          Fix: Break line at appropriate point
```

### JSON Format

```bash
python lint/standards-linter.py --format json
```

## 🛠️ Configuration

### Customizing Rules

1. **Markdown Rules**: Edit `.markdownlint.yaml`
2. **Python Linter**: Modify `standards-linter.py`
3. **Pre-commit**: Update `.pre-commit-config.yaml`
4. **YAML Rules**: Adjust `.yamllint.yaml`

### Disabling Rules

For specific files:

```markdown
<!-- markdownlint-disable MD013 -->
Long line that should not be wrapped
<!-- markdownlint-enable MD013 -->
```

For specific commits:

```bash
git commit --no-verify -m "Emergency fix"
```

## 🧪 Testing the Linter

```bash
# Test on a single file
python lint/standards-linter.py --format json > results.json

# Test custom rules
node lint/custom-rules.js

# Validate pre-commit config
pre-commit validate-config
```

## 🔄 CI/CD Integration

The linting system integrates with GitHub Actions:

- Runs on all pull requests
- Blocks merge on errors
- Provides inline comments on issues

## 📈 Benefits

1. **Consistency**: Enforces uniform structure across all standards
2. **Quality**: Catches common issues before commit
3. **Automation**: Reduces manual review burden
4. **Education**: Provides fix suggestions
5. **Flexibility**: Configurable severity levels

## 🐛 Troubleshooting

### Common Issues

**Pre-commit not found**

```bash
pip install --user pre-commit
export PATH="$HOME/.local/bin:$PATH"
```

**Markdownlint errors**

```bash
npm install -g markdownlint-cli
```

**Python dependencies**

```bash
pip install pyyaml
```

### Skipping Hooks Temporarily

```bash
SKIP=standards-metadata git commit -m "WIP"
```

## 🚨 Important Notes

- Linting rules are based on `KNOWLEDGE_MANAGEMENT_STANDARDS.md`
- Some rules are warnings (won't block commits)
- Errors must be fixed before committing
- Run `pre-commit run --all-files` periodically

## 📝 Future Enhancements

- [ ] Auto-fix capability for common issues
- [ ] VS Code extension integration
- [ ] Performance metrics reporting
- [ ] Custom rule builder UI
- [ ] Integration with documentation generators

For more information, see [KNOWLEDGE_MANAGEMENT_STANDARDS.md](../docs/standards/KNOWLEDGE_MANAGEMENT_STANDARDS.md).
