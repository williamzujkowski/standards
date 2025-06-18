# Toolchain Standards

**Version:** 1.0.0
**Last Updated:** 2025-01-13
**Status:** Active
**Standard Code:** TOOL

---

## Overview

This standard provides comprehensive guidelines and best practices for the subject area.
It aims to ensure consistency, quality, and maintainability across all related implementations.

## Purpose
This document provides centralized, standardized tool recommendations for all development activities. All tool selections are managed through the [TOOLS_CATALOG.yaml](./config/TOOLS_CATALOG.yaml) for easy updates and customization.

## Table of Contents
1. [Tool Selection Guidelines](#tool-selection-guidelines)
2. [Language-Specific Toolchains](#language-specific-toolchains)
3. [Infrastructure Tools](#infrastructure-tools)
4. [Security Scanning](#security-scanning)
5. [Observability Stack](#observability-stack)
6. [Tool Configuration](#tool-configuration)
7. [Migration Paths](#migration-paths)
8. [Customization Guide](#customization-guide)

---

## Tool Selection Guidelines

### Recommendation Levels

Tools are categorized into five recommendation levels:

| Level | Description | Action |
|-------|-------------|--------|
| **Required** | Must use in all projects | Install and configure immediately |
| **Recommended** | Should use unless good reason not to | Default choice for new projects |
| **Optional** | Can use based on project needs | Evaluate based on requirements |
| **Legacy** | Existing projects only | Plan migration to modern alternatives |
| **Deprecated** | Do not use in new projects | Migrate existing projects ASAP |

### Selection Principles

1. **Consistency First**: Use the same tools across similar projects
2. **Team Expertise**: Consider existing team knowledge
3. **Community Support**: Prefer well-maintained, popular tools
4. **Integration**: Choose tools that work well together
5. **Performance**: Balance features with build/runtime speed

---

## Language-Specific Toolchains

### 🐍 Python Toolchain

#### **[REQUIRED]** Core Tools
- **Formatter**: `black` (v23.0+) - The uncompromising code formatter
- **Import Sorter**: `isort` (v5.0+) - Import statement organization
- **Type Checker**: `mypy` (v1.0+) - Static type checking
- **Test Framework**: `pytest` (v7.0+) - Modern testing framework

#### **[RECOMMENDED]** Enhanced Development
- **Linter**: `ruff` (v0.1.0+) - Fast, modern linter (replaces flake8)
- **Package Manager**: `poetry` (v1.5+) - Dependency management
- **Security Scanner**: `bandit` (v1.7+) - Find common security issues
- **Property Testing**: `hypothesis` (v6.0+) - Generate test cases

#### **[LEGACY]** Migration Required
- `flake8` → Migrate to `ruff`
- `pip` alone → Migrate to `poetry` or `pip-tools`

#### Quick Setup
```bash
# Install all required Python tools
pip install black isort mypy pytest pytest-cov
pip install --upgrade ruff bandit poetry

# Configure in pyproject.toml
poetry init
poetry add --group dev black isort mypy pytest ruff bandit
```

### 🟨 JavaScript/TypeScript Toolchain

#### **[REQUIRED]** Core Tools
- **Linter**: `eslint` (v8.0+) - Pluggable linting utility
- **Formatter**: `prettier` (v3.0+) - Opinionated code formatter
- **Test Framework**: `jest` (v29.0+) - Delightful JavaScript testing
- **Type System**: `typescript` (v5.0+) - For TypeScript projects

#### **[RECOMMENDED]** Enhanced Development
- **Package Manager**: `pnpm` (v8.0+) - Fast, disk space efficient
- **Build Tool**: `vite` (v5.0+) - Next generation frontend tooling
- **E2E Testing**: `cypress` (v13.0+) - Fast, reliable testing

#### **[OPTIONAL]** Alternatives
- **Build**: `webpack` (v5.0+) or `esbuild` (v0.19+)
- **Testing**: `playwright` (v1.40+) for cross-browser testing
- **Package Manager**: `npm` (v10.0+) if pnpm unavailable

#### Quick Setup
```bash
# Initialize with pnpm
pnpm init
pnpm add -D eslint prettier jest @types/jest typescript
pnpm add -D vite @vitejs/plugin-react

# Configure
npx eslint --init
echo '{"semi": false, "singleQuote": true}' > .prettierrc
```

### 🐹 Go Toolchain

#### **[REQUIRED]** Core Tools
- **Linter**: `golangci-lint` (v1.55+) - Fast linters runner
- **Testing**: Built-in `go test` with `-race` and `-cover` flags
- **Building**: Built-in `go build` with optimization flags

#### Quick Setup
```bash
# Install golangci-lint
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Create .golangci.yml configuration
golangci-lint run --init
```

---

## Infrastructure Tools

### 🐳 Containerization

#### **[REQUIRED]**
- **Container Runtime**: `docker` (v24.0+) or `podman` (v4.0+)

#### **[RECOMMENDED]**
- **Orchestration**: `kubernetes` (v1.28+) with `kubectl`, `helm`, `kustomize`
- **Container Scanning**: `trivy` (v0.48+) - Comprehensive vulnerability scanner

### 🏗️ Infrastructure as Code

#### **[RECOMMENDED]**
- **Primary IaC**: `terraform` (v1.6+) - Write, Plan, Create Infrastructure
- **State Management**: Use remote state (S3, Azure Storage, GCS)
- **Module Registry**: Leverage existing modules when possible

#### **[OPTIONAL]**
- **Configuration**: `ansible` (v2.15+) - For configuration management
- **Alternative IaC**: `pulumi` (v3.0+) - Infrastructure with real programming languages

### 🔄 CI/CD Pipelines

#### **[RECOMMENDED]**
- **GitHub Projects**: GitHub Actions (built-in)
- **GitLab Projects**: GitLab CI (built-in)

#### **[LEGACY]**
- **Jenkins**: Only for existing installations

---

## Security Scanning

### 🔍 Required Security Tools

1. **Dependency Scanning**: `dependabot` (GitHub) or `renovate`
2. **Container Scanning**: `trivy` for all container images
3. **SAST**: `semgrep` for multi-language static analysis

### 🛡️ Recommended Additional Security

- **Commercial Options**: `snyk` for comprehensive scanning
- **Code Quality**: `sonarqube` for quality gates
- **Python Specific**: `safety` for dependency checks
- **JavaScript Specific**: `npm audit` or `pnpm audit`

---

## Observability Stack

### 📊 Metrics & Monitoring

#### **[RECOMMENDED]** Open Source Stack
- **Collection**: `prometheus` (v2.45+)
- **Visualization**: `grafana` (v10.0+)
- **Alerting**: Prometheus Alertmanager

#### **[OPTIONAL]** Commercial Solutions
- **APM**: Datadog, New Relic, or AppDynamics
- **Error Tracking**: `sentry` (recommended even with APM)

### 📝 Logging

#### **[RECOMMENDED]**
- **Collection**: `fluentd` or `fluent-bit`
- **Storage**: Elasticsearch or cloud-native solutions
- **Visualization**: Kibana or Grafana

### 🔗 Distributed Tracing

#### **[RECOMMENDED]**
- **Framework**: OpenTelemetry (vendor-neutral)
- **Backend**: Jaeger or cloud provider solutions

---

## Tool Configuration

### 📁 Configuration Structure

All tool configurations should be centralized:

```
project-root/
├── pyproject.toml          # Python tools (black, isort, mypy, pytest)
├── package.json            # JavaScript/Node.js dependencies
├── .eslintrc.json          # ESLint configuration
├── .prettierrc             # Prettier configuration
├── tsconfig.json           # TypeScript configuration
├── .golangci.yml           # Go linting configuration
├── docker-compose.yml      # Local development services
├── .github/
│   └── workflows/          # CI/CD pipelines
└── tools-config/           # Additional tool configurations
    ├── trivy.yaml
    └── semgrep.yaml
```

### 🔧 Standard Configurations

Standard configurations for all tools are available in the [examples/project-templates/](./examples/project-templates/) directory.

---

## Migration Paths

### 🚀 Legacy Tool Migration

#### Python: flake8 → ruff
```bash
# Install ruff
pip install ruff

# Convert flake8 config to ruff
ruff check --fix .

# Update pyproject.toml
[tool.ruff]
line-length = 88
select = ["E", "F", "W", "C", "N"]
```

#### JavaScript: npm/yarn → pnpm
```bash
# Install pnpm
npm install -g pnpm

# Import from existing lockfile
pnpm import

# Install dependencies
pnpm install
```

---

## Customization Guide

### 🎯 Customizing Tool Selection

1. **Fork** the `TOOLS_CATALOG.yaml` file
2. **Modify** recommendation levels based on your needs
3. **Add** organization-specific tools
4. **Update** version requirements
5. **Document** the reasoning for changes

### 📝 Example Customization

```yaml
# In your TOOLS_CATALOG.yaml override:
languages:
  python:
    linting:
      - name: "custom-linter"
        recommendation: "required"
        version: ">=1.0.0"
        description: "Organization-specific linter"
        config_file: ".custom-linter.yml"
```

### 🔄 Keeping Tools Updated

1. **Review** quarterly for version updates
2. **Test** updates in isolated environment
3. **Update** TOOLS_CATALOG.yaml with new versions
4. **Communicate** changes to teams
5. **Provide** migration guides for breaking changes

---

## 🤖 LLM Integration

### Tool Selection with AI

When using AI assistants, reference tools by their catalog ID:

```
@load tools:[python:required] for new Python project
@suggest tools:[security:*] for security audit
@compare tools:[jest vs playwright] for testing strategy
```

### Automated Tool Configuration

```
@generate config for:[black + isort + mypy] in:[pyproject.toml]
@setup pipeline with:[required-tools] for:[github-actions]
```

---

## 📊 Tool Adoption Metrics

Track tool adoption across projects:

1. **Required Tools Compliance**: 100% expected
2. **Recommended Tools Adoption**: 80%+ target
3. **Legacy Tool Migration**: Track reduction over time
4. **Security Tool Coverage**: 100% for production code

---

## 🆘 Support

- **Tool Issues**: Check tool-specific documentation first
- **Configuration Help**: See examples/project-templates/
- **Updates**: Watch TOOLS_CATALOG.yaml for changes
- **Questions**: Create issue in standards repository

---

**Remember**: Tool standardization improves consistency, reduces onboarding time, and ensures security compliance. Always check TOOLS_CATALOG.yaml for the latest recommendations!

## Implementation

### Getting Started

1. Review the relevant sections of this standard for your use case
2. Identify which guidelines apply to your project
3. Implement the required practices and patterns
4. Validate compliance using the provided checklists

### Implementation Checklist

- [ ] Review and understand applicable standards
- [ ] Implement required practices
- [ ] Follow recommended patterns
- [ ] Validate implementation against guidelines
- [ ] Document any deviations with justification
