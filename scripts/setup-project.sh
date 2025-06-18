#!/bin/bash
# Project Setup Script - Integrates standards into new projects

PROJECT_DIR=${1:-"."}
STANDARDS_REPO="https://github.com/williamzujkowski/standards.git"

echo "🚀 Setting up project with development standards..."

# Create project structure
mkdir -p "$PROJECT_DIR"/{.github/workflows,docs,scripts,tests}

# Clone standards temporarily
TEMP_DIR=$(mktemp -d)
git clone --depth 1 "$STANDARDS_REPO" "$TEMP_DIR/standards"

# Copy essential files
cp "$TEMP_DIR/standards/docs/core/CLAUDE.md" "$PROJECT_DIR/docs/"
cp "$TEMP_DIR/standards/docs/guides/KICKSTART_PROMPT.md" "$PROJECT_DIR/docs/"
cp "$TEMP_DIR/standards/docs/guides/KICKSTART_ADVANCED.md" "$PROJECT_DIR/docs/"

# Create project-specific standards reference
cat > "$PROJECT_DIR/docs/PROJECT_STANDARDS.md" << 'EOF'
# Project Standards Reference

This project follows the comprehensive standards defined at:
https://github.com/williamzujkowski/standards

## Quick Links

- [Coding Standards](https://github.com/williamzujkowski/standards/blob/master/docs/standards/CODING_STANDARDS.md)
- [Testing Standards](https://github.com/williamzujkowski/standards/blob/master/docs/standards/TESTING_STANDARDS.md)
- [Security Standards](https://github.com/williamzujkowski/standards/blob/master/docs/standards/MODERN_SECURITY_STANDARDS.md)

## Local Standards Loading (via CLAUDE.md)

For AI-assisted development, use the loading patterns in `docs/CLAUDE.md`:

```
@load [CS:style,architecture + TS:core + SEC:auth]
```

## Project-Specific Overrides

Document any project-specific deviations here:

1. **Language**: [Your language]
2. **Framework**: [Your framework]
3. **Special Requirements**: [Any deviations from standards]

EOF

# Create configuration files based on standards
cat > "$PROJECT_DIR/.editorconfig" << 'EOF'
# EditorConfig helps maintain consistent coding styles
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.py]
indent_size = 4

[*.go]
indent_style = tab

[*.md]
trim_trailing_whitespace = false
EOF

# Create pre-commit config
cat > "$PROJECT_DIR/.pre-commit-config.yaml" << 'EOF'
# Pre-commit hooks based on standards
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
      - id: check-merge-conflict

  # Add language-specific hooks here
EOF

# Create GitHub Actions workflow for standards compliance
cat > "$PROJECT_DIR/.github/workflows/standards-check.yml" << 'EOF'
name: Standards Compliance Check

on:
  pull_request:
    branches: [ main, master ]
  push:
    branches: [ main, master ]

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Standards Checks
        run: |
          echo "Running standards compliance checks..."
          # Add your language-specific linters and checks here

      - name: Check Test Coverage
        run: |
          echo "Checking test coverage meets 85% requirement..."
          # Add coverage check commands
EOF

# Create Makefile with standards-based targets
cat > "$PROJECT_DIR/Makefile" << 'EOF'
# Standards-compliant Makefile

.PHONY: help install test lint format security-check

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	@echo "Installing dependencies..."
	# Add language-specific install commands

test: ## Run tests with coverage
	@echo "Running tests (target: 85% coverage)..."
	# Add test commands

lint: ## Run linting checks
	@echo "Running linters..."
	# Add linting commands

format: ## Format code according to standards
	@echo "Formatting code..."
	# Add formatting commands

security-check: ## Run security scanning
	@echo "Running security checks..."
	# Add security scanning commands

ci: lint test security-check ## Run all CI checks
EOF

# Cleanup
rm -rf "$TEMP_DIR"

echo "✅ Project setup complete!"
echo ""
echo "Next steps:"
echo "1. Review docs/PROJECT_STANDARDS.md and customize for your project"
echo "2. Install pre-commit hooks: pre-commit install"
echo "3. Configure language-specific tools in Makefile"
echo "4. Set up CI/CD based on .github/workflows/standards-check.yml"
echo ""
echo "For LLM-assisted development, use docs/CLAUDE.md patterns"
