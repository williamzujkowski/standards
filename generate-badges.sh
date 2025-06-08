#!/bin/bash
# Generate standards compliance badges for your README

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
COVERAGE="${COVERAGE:-85}"
SECURITY_SCORE="${SECURITY_SCORE:-A+}"
LIGHTHOUSE_SCORE="${LIGHTHOUSE_SCORE:-95}"
STANDARDS_VERSION="${STANDARDS_VERSION:-2.0.0}"

echo -e "${BLUE}🎯 Generating Standards Compliance Badges${NC}"

# Create badges directory
mkdir -p badges

# Generate badge markdown
cat > badges/README.md << EOF
# Standards Compliance Badges

Add these badges to your project README to show standards compliance:

## Core Standards

\`\`\`markdown
[![Standards](https://img.shields.io/badge/standards-v${STANDARDS_VERSION}-blue.svg)](https://github.com/williamzujkowski/standards)
[![Code Coverage](https://img.shields.io/badge/coverage-${COVERAGE}%25-brightgreen.svg)](https://github.com/williamzujkowski/standards/blob/master/TESTING_STANDARDS.md)
[![Security](https://img.shields.io/badge/security-${SECURITY_SCORE}-brightgreen.svg)](https://github.com/williamzujkowski/standards/blob/master/MODERN_SECURITY_STANDARDS.md)
\`\`\`

## Quality Metrics

\`\`\`markdown
[![Lighthouse](https://img.shields.io/badge/lighthouse-${LIGHTHOUSE_SCORE}-brightgreen.svg)](https://github.com/williamzujkowski/standards/blob/master/SEO_WEB_MARKETING_STANDARDS.md)
[![Accessibility](https://img.shields.io/badge/WCAG-2.1%20AA-brightgreen.svg)](https://github.com/williamzujkowski/standards/blob/master/LEGAL_COMPLIANCE_STANDARDS.md)
[![License Compliance](https://img.shields.io/badge/licenses-compliant-brightgreen.svg)](https://github.com/williamzujkowski/standards/blob/master/LEGAL_COMPLIANCE_STANDARDS.md)
\`\`\`

## Process Standards

\`\`\`markdown
[![Agile](https://img.shields.io/badge/process-agile-blue.svg)](https://github.com/williamzujkowski/standards/blob/master/PROJECT_MANAGEMENT_STANDARDS.md)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-automated-brightgreen.svg)](https://github.com/williamzujkowski/standards/blob/master/DEVOPS_PLATFORM_STANDARDS.md)
[![Monitoring](https://img.shields.io/badge/monitoring-enabled-brightgreen.svg)](https://github.com/williamzujkowski/standards/blob/master/OBSERVABILITY_STANDARDS.md)
\`\`\`

## Technology Specific

### Frontend
\`\`\`markdown
[![React](https://img.shields.io/badge/React-standards-61DAFB.svg?logo=react)](https://github.com/williamzujkowski/standards/blob/master/FRONTEND_MOBILE_STANDARDS.md)
[![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178C6.svg?logo=typescript)](https://github.com/williamzujkowski/standards/blob/master/CODING_STANDARDS.md)
\`\`\`

### Backend
\`\`\`markdown
[![Node.js](https://img.shields.io/badge/Node.js-standards-339933.svg?logo=node.js)](https://github.com/williamzujkowski/standards/blob/master/CODING_STANDARDS.md)
[![Python](https://img.shields.io/badge/Python-PEP8-3776AB.svg?logo=python)](https://github.com/williamzujkowski/standards/blob/master/CODING_STANDARDS.md)
[![Go](https://img.shields.io/badge/Go-standards-00ADD8.svg?logo=go)](https://github.com/williamzujkowski/standards/blob/master/CODING_STANDARDS.md)
\`\`\`

### Infrastructure
\`\`\`markdown
[![Docker](https://img.shields.io/badge/Docker-secure-2496ED.svg?logo=docker)](https://github.com/williamzujkowski/standards/blob/master/CLOUD_NATIVE_STANDARDS.md)
[![Kubernetes](https://img.shields.io/badge/K8s-production-326CE5.svg?logo=kubernetes)](https://github.com/williamzujkowski/standards/blob/master/CLOUD_NATIVE_STANDARDS.md)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC.svg?logo=terraform)](https://github.com/williamzujkowski/standards/blob/master/DEVOPS_PLATFORM_STANDARDS.md)
\`\`\`

## Custom Badge Generator

Generate custom badges for your specific metrics:

\`\`\`bash
# Test Coverage
https://img.shields.io/badge/coverage-{PERCENTAGE}%25-{COLOR}.svg

# Where COLOR is:
# - brightgreen: >= 85%
# - green: >= 70%
# - yellow: >= 50%
# - red: < 50%

# Security Score
https://img.shields.io/badge/security-{SCORE}-{COLOR}.svg

# Performance
https://img.shields.io/badge/performance-{METRIC}-{COLOR}.svg
\`\`\`

## All-in-One Standards Badge

\`\`\`markdown
[![Comprehensive Standards](https://img.shields.io/badge/Standards-Comprehensive%20v${STANDARDS_VERSION}-blue.svg?longCache=true&style=for-the-badge)](https://github.com/williamzujkowski/standards)
\`\`\`

## Example README Header

\`\`\`markdown
# My Awesome Project

[![Standards](https://img.shields.io/badge/standards-v${STANDARDS_VERSION}-blue.svg)](https://github.com/williamzujkowski/standards)
[![Code Coverage](https://img.shields.io/badge/coverage-${COVERAGE}%25-brightgreen.svg)](./coverage)
[![Security](https://img.shields.io/badge/security-${SECURITY_SCORE}-brightgreen.svg)](./security)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

A project following comprehensive development standards for quality, security, and maintainability.

## 📋 Standards Compliance

This project adheres to the [Comprehensive Software Development Standards](https://github.com/williamzujkowski/standards):

- ✅ **Code Quality**: Following coding standards with automated linting and formatting
- ✅ **Testing**: ${COVERAGE}% test coverage with unit, integration, and e2e tests  
- ✅ **Security**: ${SECURITY_SCORE} rating with automated vulnerability scanning
- ✅ **Performance**: Optimized for Core Web Vitals and scalability
- ✅ **Documentation**: Comprehensive docs following content standards
- ✅ **Accessibility**: WCAG 2.1 AA compliant
- ✅ **DevOps**: Fully automated CI/CD pipeline with IaC

[View Full Standards Compliance Report →](./docs/standards-compliance.md)
\`\`\`
EOF

# Generate dynamic badge script
cat > badges/generate-dynamic-badge.sh << 'EOF'
#!/bin/bash
# Generate dynamic badge based on actual metrics

# Get test coverage from your test output
COVERAGE=$(npm test -- --coverage --coverageReporters=text-summary | grep "Statements" | awk '{print $3}' | sed 's/%//')

# Determine color based on coverage
if (( $(echo "$COVERAGE >= 85" | bc -l) )); then
    COLOR="brightgreen"
elif (( $(echo "$COVERAGE >= 70" | bc -l) )); then
    COLOR="green"
elif (( $(echo "$COVERAGE >= 50" | bc -l) )); then
    COLOR="yellow"
else
    COLOR="red"
fi

# Generate badge URL
echo "https://img.shields.io/badge/coverage-${COVERAGE}%25-${COLOR}.svg"

# Update README with new badge
sed -i "s|https://img.shields.io/badge/coverage-[0-9]*%25-[a-z]*.svg|https://img.shields.io/badge/coverage-${COVERAGE}%25-${COLOR}.svg|g" README.md
EOF

chmod +x badges/generate-dynamic-badge.sh

# Generate standards compliance report template
cat > badges/standards-compliance-template.md << EOF
# Standards Compliance Report

**Project**: \${PROJECT_NAME}  
**Date**: \$(date +%Y-%m-%d)  
**Standards Version**: ${STANDARDS_VERSION}

## Executive Summary

This project implements the [Comprehensive Software Development Standards](https://github.com/williamzujkowski/standards) v${STANDARDS_VERSION}.

### Overall Compliance Score: \${SCORE}%

## Detailed Compliance

### ✅ Implemented Standards

#### Code Quality (CODING_STANDARDS.md)
- [x] Linting configured (ESLint/Flake8/GolangCI)
- [x] Auto-formatting (Prettier/Black/gofmt)
- [x] Type checking (TypeScript/mypy)
- [x] Code review process
- [x] Architecture patterns documented

#### Testing (TESTING_STANDARDS.md)
- [x] Unit tests: \${UNIT_COVERAGE}% coverage
- [x] Integration tests implemented
- [x] E2E tests for critical paths
- [x] Performance benchmarks
- [x] Security testing automated

#### Security (MODERN_SECURITY_STANDARDS.md)
- [x] Dependency scanning (Snyk/npm audit)
- [x] SAST scanning in CI/CD
- [x] Secret scanning enabled
- [x] Security headers configured
- [x] HTTPS enforced

#### DevOps (DEVOPS_PLATFORM_STANDARDS.md)
- [x] CI/CD pipeline automated
- [x] Infrastructure as Code
- [x] Container security scanning
- [x] Automated deployments
- [x] Rollback procedures

#### Observability (OBSERVABILITY_STANDARDS.md)
- [x] Structured logging
- [x] Metrics collection
- [x] Distributed tracing
- [x] Alerting configured
- [x] SLOs defined

### 🚧 In Progress

- [ ] Achieve 95% coverage for critical paths
- [ ] Implement advanced performance monitoring
- [ ] Complete accessibility audit

### 📊 Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Code Coverage | 85% | \${COVERAGE}% | \${COVERAGE_STATUS} |
| Security Score | A+ | \${SECURITY_SCORE} | ✅ |
| Performance (Lighthouse) | 90+ | \${LIGHTHOUSE_SCORE} | ✅ |
| Bundle Size | <200KB | \${BUNDLE_SIZE}KB | \${BUNDLE_STATUS} |
| Build Time | <5min | \${BUILD_TIME} | ✅ |
| Deployment Frequency | Daily | \${DEPLOY_FREQ} | ✅ |

### 📋 Compliance Checklist

Use this checklist to track your progress:

**Core Standards**
- [ ] UNIFIED_STANDARDS.md reviewed
- [ ] CODING_STANDARDS.md implemented
- [ ] TESTING_STANDARDS.md requirements met
- [ ] Team trained on standards

**Domain-Specific**
- [ ] Relevant domain standards identified
- [ ] Implementation plan created
- [ ] Automation configured
- [ ] Monitoring in place

**Continuous Improvement**
- [ ] Regular standards review scheduled
- [ ] Metrics dashboard created
- [ ] Team feedback collected
- [ ] Standards updates tracked

## Next Steps

1. Complete remaining implementation items
2. Schedule quarterly standards review
3. Share compliance report with stakeholders
4. Plan standards training for new team members

---

Generated by [Standards Compliance Tool](https://github.com/williamzujkowski/standards)
EOF

echo -e "${GREEN}✅ Badge generation complete!${NC}"
echo ""
echo "Files created:"
echo "  - badges/README.md (Badge documentation)"
echo "  - badges/generate-dynamic-badge.sh (Dynamic badge generator)"
echo "  - badges/standards-compliance-template.md (Compliance report template)"
echo ""
echo "Add badges to your README by copying from badges/README.md"