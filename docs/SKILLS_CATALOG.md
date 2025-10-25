# Skills Catalog

**Version**: 1.0.0
**Last Updated**: 2025-10-16
**Core Documented Skills**: 5 | **Total Available**: 62+

---

## Overview

This catalog provides a comprehensive listing of all available skills in the standards repository. Skills are organized by category and include metadata to help you quickly identify which skills to load for your project.

---

## Quick Reference

### Skills by Category

| Category | Skills | Use Cases |
|----------|--------|-----------|
| **Development** | coding-standards, testing | Code quality, TDD, maintainability |
| **Security** | security-practices, nist-compliance | Zero Trust, compliance, auditing |
| **Meta** | skill-loader | Skill discovery, composition |

### Skills by Token Cost (Level 1)

| Skill | Tokens | Reading Time | Priority |
|-------|--------|--------------|----------|
| coding-standards | 336 | 5 min | High |
| security-practices | 409 | 5 min | Critical (for APIs) |
| testing | 430 | 5 min | High |
| nist-compliance | 580 | 5 min | Medium (compliance) |
| skill-loader | 328 | 5 min | Low (meta) |

**Total (all Level 1)**: ~2,083 tokens (~0.5% of Claude context window)

---

## Complete Skills Listing

### 1. Coding Standards

```yaml
Name: coding-standards
Description: Comprehensive coding standards and best practices for maintainable, consistent software development across multiple languages and paradigms
Category: Development
Priority: High
```

**Token Estimates:**

- Level 1: 336 tokens (5 min)
- Level 2: 1,245 tokens (30 min)
- Level 3: 1,342 tokens (extended)
- **Total**: 2,923 tokens

**What You Get:**

**Level 1 (Quick Start)**

- Core principles (Consistency, Readability, Maintainability, Quality)
- Quick reference with good vs bad examples
- Essential checklist (style guide, naming, complexity, linting)
- Common pitfalls (inconsistent naming, complex functions, missing docs)

**Level 2 (Implementation)**

- Code style and formatting by language
- Documentation standards (JSDoc, docstrings)
- Architecture patterns (SOLID principles, DRY)
- Error handling strategies
- Automation tools (linters, formatters, pre-commit hooks)

**Level 3 (Mastery)**

- Performance optimization patterns (memoization, caching)
- Concurrency patterns
- API design best practices
- Refactoring strategies
- Essential reading list
- Tools and frameworks

**When to Load:**

- Starting any new project
- Code review preparation
- Team onboarding
- Establishing coding conventions

**Integration Points:**

- Links to [Security Practices](#2-security-practices) for secure coding
- Links to [Testing](#3-testing-standards) for testable code design
- Links to [NIST Compliance](#4-nist-compliance) for SI-10, SI-11 controls

**Load Command:**

```bash
# Quick Start
@load skill:coding-standards

# Deep Dive
@load skill:coding-standards --level 2

# Mastery
@load skill:coding-standards --level 3
```

**Product Types:**

- `product:api`
- `product:frontend-web`
- `product:mobile`
- `product:cli`
- `product:data-pipeline`
- `product:ml-service`

**Languages Supported:**

- Python
- JavaScript/TypeScript
- Go
- Java
- (Extensible via `language_mappings` in product-matrix.yaml)

---

### 2. Security Practices

```yaml
Name: security-practices
Description: Modern security standards including Zero Trust Architecture, supply chain security, container security, and API protection patterns
Category: Security
Priority: Critical (for APIs/web services)
```

**Token Estimates:**

- Level 1: 409 tokens (5 min)
- Level 2: 2,082 tokens (30 min)
- Level 3: 1,451 tokens (extended)
- **Total**: 3,942 tokens

**What You Get:**

**Level 1 (Quick Start)**

- Essential security checklist (auth, secrets, input validation, encryption)
- Common vulnerabilities (SQLi, XSS, CSRF, auth bypass)
- Quick reference for secure code patterns
- Immediate action items

**Level 2 (Implementation)**

- Zero Trust Architecture implementation
- Supply chain security (SBOM, dependency scanning)
- Container security (image scanning, runtime protection)
- API security (authentication, rate limiting, CORS)
- Secrets management (vaults, rotation, detection)
- Security testing integration

**Level 3 (Mastery)**

- Incident response planning
- Cryptography best practices
- Security monitoring and alerting
- Advanced threat detection
- Compliance integration

**When to Load:**

- Building APIs or web services (Critical)
- Handling sensitive data (Critical)
- Deploying to production (High)
- Security audits/reviews (High)
- Compliance requirements (High)

**Integration Points:**

- Links to [NIST Compliance](#4-nist-compliance) for control implementation
- Links to [Coding Standards](#1-coding-standards) for secure coding patterns
- Links to [Testing](#3-testing-standards) for security testing

**Load Command:**

```bash
# Quick Start
@load skill:security-practices

# Deep Dive
@load skill:security-practices --level 2

# Full Security Bundle
@load [skill:security-practices + skill:nist-compliance] --level 2
```

**Product Types:**

- `product:api` (Critical)
- `product:web-service` (Critical)
- `product:frontend-web` (High)
- `product:mobile` (High)
- `product:data-pipeline` (High)
- `product:ml-service` (High)

**NIST Controls Covered:**

- AC (Access Control): AC-2, AC-3, AC-6
- IA (Identification & Authentication): IA-2, IA-5
- SC (System & Communications Protection): SC-8, SC-13
- SI (System & Information Integrity): SI-10, SI-11

---

### 3. Testing Standards

```yaml
Name: testing
Description: Comprehensive testing standards including unit, integration, security, and property-based testing with TDD methodology
Category: Development
Priority: High
```

**Token Estimates:**

- Level 1: 430 tokens (5 min)
- Level 2: 2,225 tokens (30 min)
- Level 3: 1,106 tokens (extended)
- **Total**: 3,761 tokens

**What You Get:**

**Level 1 (Quick Start)**

- Testing pyramid (Unit → Integration → E2E)
- TDD Red-Green-Refactor cycle
- Essential checklist (unit tests, integration tests, >80% coverage)
- Common pitfalls (testing implementation details, slow tests, flaky tests)

**Level 2 (Implementation)**

- Test-Driven Development walkthrough
- Property-based testing with fast-check
- Integration testing patterns (API tests, database tests)
- Security testing (SQLi, XSS, auth bypass)
- Performance testing (benchmarks, load tests)
- Test organization (AAA pattern, fixtures)

**Level 3 (Mastery)**

- Contract testing with Pact
- Chaos engineering
- Visual regression testing
- Mutation testing
- Testing frameworks comparison
- Template test suites

**When to Load:**

- Starting new projects (High)
- Implementing TDD (High)
- Code review for tests (High)
- Setting up CI/CD (Medium)
- Improving test coverage (Medium)

**Integration Points:**

- Links to [Coding Standards](#1-coding-standards) for testable code design
- Links to [Security Practices](#2-security-practices) for security testing
- Links to [NIST Compliance](#4-nist-compliance) for SI-10, SI-11 controls

**Load Command:**

```bash
# Quick Start
@load skill:testing

# Deep Dive
@load skill:testing --level 2

# Development Bundle
@load [skill:coding-standards + skill:testing] --level 2
```

**Product Types:**

- `product:api` (High)
- `product:frontend-web` (High)
- `product:mobile` (High)
- `product:cli` (Medium)
- `product:data-pipeline` (Medium)
- `product:ml-service` (Critical - model testing)

**Frameworks Covered:**

- **Unit Testing**: Jest, Vitest, pytest, JUnit
- **Integration Testing**: Supertest, TestContainers
- **E2E Testing**: Playwright, Cypress, Selenium
- **Property Testing**: fast-check, Hypothesis, QuickCheck

---

### 4. NIST Compliance

```yaml
Name: nist-compliance
Description: NIST 800-53r5 control implementation guidance with automated tagging, evidence collection, and SSP generation
Category: Security & Compliance
Priority: Medium (when compliance required)
```

**Token Estimates:**

- Level 1: 580 tokens (5 min)
- Level 2: 2,734 tokens (30 min)
- Level 3: 731 tokens (extended)
- **Total**: 4,045 tokens

**What You Get:**

**Level 1 (Quick Start)**

- Control tagging reference (@nist-controls syntax)
- Common control families (AC, IA, AU, SC, SI)
- Quick Start tagging examples
- Essential checklist (tag functions, validate coverage, collect evidence)

**Level 2 (Implementation)**

- AC (Access Control) family implementation
- IA (Identification & Authentication) patterns
- AU (Audit & Accountability) logging
- SC (System & Communications Protection) encryption
- SI (System & Information Integrity) validation
- Evidence collection automation
- SSP generation tools

**Level 3 (Mastery)**

- Continuous compliance monitoring
- Automated control testing
- Audit preparation
- Multi-framework mapping (NIST → SOC2 → ISO27001)
- VS Code extension integration

**When to Load:**

- Government/regulated industries (Critical)
- Security audits (Critical)
- Compliance certifications (Critical)
- Security-conscious organizations (Medium)
- API services with auth (Medium)

**Integration Points:**

- Links to [Security Practices](#2-security-practices) for security implementation
- Links to [Coding Standards](#1-coding-standards) for SI-10, SI-11
- Links to [Testing](#3-testing-standards) for control validation

**Load Command:**

```bash
# Quick Start
@load skill:nist-compliance

# Deep Dive
@load skill:nist-compliance --level 2

# Full Compliance Bundle
@load [skill:security-practices + skill:nist-compliance] --level 2
```

**Product Types:**

- `product:api` (Auto-included when security present)
- `product:web-service` (Auto-included)
- `product:data-pipeline` (High for sensitive data)
- `product:ml-service` (Medium)
- `product:compliance-artifacts` (Critical)

**Control Families Covered:**

- **AC**: Access Control (AC-2, AC-3, AC-6)
- **IA**: Identification & Authentication (IA-2, IA-5)
- **AU**: Audit & Accountability (AU-2, AU-3, AU-12)
- **SC**: System & Communications Protection (SC-8, SC-13)
- **SI**: System & Information Integrity (SI-10, SI-11)
- **CM**: Configuration Management (CM-2, CM-6)
- **CP**: Contingency Planning (CP-9, CP-10)

**Tools Included:**

- VS Code extension for auto-tagging
- Validation scripts
- Evidence collection automation
- SSP generation templates

---

### 5. Skill Loader (Meta-Skill)

```yaml
Name: skill-loader
Description: Meta-skill for loading, composing, and applying standards as progressive-disclosure skills with context-aware recommendations
Category: Meta
Priority: Low (infrastructure)
```

**Token Estimates:**

- Level 1: 328 tokens (5 min)
- Level 2: 1,177 tokens (30 min)
- Level 3: 15 tokens (extended)
- **Total**: 1,520 tokens

**What You Get:**

**Level 1 (Quick Start)**

- Quick load commands (@load syntax)
- Skill catalog overview
- Product type mappings
- Token cost reference

**Level 2 (Implementation)**

- Skill resolution engine (TypeScript implementation)
- Progressive disclosure loader
- Context-aware recommendations (project analysis)
- Skill composition patterns
- CLI usage examples

**Level 3 (Mastery)**

- Custom skill creation
- Skill validation tools
- Advanced composition strategies

**When to Load:**

- Understanding the skills system (Informational)
- Building custom loaders (Advanced)
- Contributing new skills (Authoring)

**Integration Points:**

- References all other skills (meta-skill)
- Links to product-matrix.yaml
- Links to validation tools

**Load Command:**

```bash
# Learn about the loader
@load skill:skill-loader

# Understand implementation
@load skill:skill-loader --level 2
```

**Note:** This is a **meta-skill** that explains the skills system itself. Most users won't need to load this directly.

---

## Skills by Use Case

### Starting a New Project

**Minimal Bundle:**

```bash
@load [skill:coding-standards + skill:testing]
# Token cost: ~766 tokens (Level 1)
```

**Comprehensive Bundle:**

```bash
@load product:api
# Auto-loads: coding-standards, security-practices, testing, nist-compliance
# Token cost: ~1,755 tokens (Level 1)
```

### Code Review

```bash
@load [skill:coding-standards + skill:testing] --level 1
# Quick checklists for review
# Token cost: ~766 tokens
```

### Security Audit

```bash
@load [skill:security-practices + skill:nist-compliance] --level 2
# Comprehensive security coverage
# Token cost: ~4,907 tokens
```

### Compliance Certification

```bash
@load [skill:nist-compliance + skill:security-practices] --level 2
# Full compliance implementation
# Token cost: ~4,907 tokens
```

### Team Onboarding

```bash
# Day 1: Fundamentals
@load skill:coding-standards --level 1

# Week 1: Testing
@load skill:testing --level 1

# Week 2: Security
@load skill:security-practices --level 1

# Week 3: Deep Dive
@load [skill:coding-standards + skill:testing] --level 2
```

---

## Skills by Product Type

### product:api

```bash
@load product:api

# Auto-loads:
# - coding-standards (language-specific patterns)
# - security-practices (API auth, input validation)
# - testing (unit, integration, security tests)
# - nist-compliance (AC, IA, AU controls)

# Token cost: ~1,755 tokens (Level 1)
```

### product:frontend-web

```bash
@load product:frontend-web

# Auto-loads:
# - coding-standards (TypeScript/framework patterns)
# - security-practices (XSS, CSRF protection)
# - testing (component testing, E2E)

# Token cost: ~1,175 tokens (Level 1)
```

### product:mobile

```bash
@load product:mobile

# Auto-loads:
# - coding-standards (platform languages)
# - security-practices (mobile auth, secure storage)
# - testing (unit, integration, UI tests)

# Token cost: ~1,175 tokens (Level 1)
```

### product:data-pipeline

```bash
@load product:data-pipeline

# Auto-loads:
# - coding-standards (Python/Scala patterns)
# - security-practices (data classification, secrets)
# - testing (data quality, integration tests)
# - nist-compliance (data retention, privacy)

# Token cost: ~1,755 tokens (Level 1)
```

### product:ml-service

```bash
@load product:ml-service

# Auto-loads:
# - coding-standards (ML frameworks)
# - security-practices (model security)
# - testing (model validation, A/B tests)
# - nist-compliance (AI ethics, privacy)

# Token cost: ~1,755 tokens (Level 1)
```

---

## Skills Roadmap

### Planned Skills (Coming Soon)

#### Development

- [ ] `api-design-patterns` - RESTful/GraphQL API design
- [ ] `microservices` - Microservice architecture patterns
- [ ] `data-engineering` - ETL/ELT best practices
- [ ] `ml-ai` - ML model development and deployment

#### Operations

- [ ] `cloud-native` - Cloud-native architecture (K8s, containers)
- [ ] `devops` - CI/CD, IaC, automation
- [ ] `observability` - Logging, monitoring, tracing

#### Specialized

- [ ] `web-design` - Frontend design systems
- [ ] `mobile-development` - iOS/Android best practices
- [ ] `cost-optimization` - Cloud cost management
- [ ] `legal-compliance` - Privacy, GDPR, data retention

### Contributing New Skills

See [SKILL_AUTHORING_GUIDE.md](./guides/SKILL_AUTHORING_GUIDE.md) to contribute:

1. Create skill in `skills/your-skill-name/`
2. Follow progressive disclosure pattern (Level 1, 2, 3)
3. Validate with `python scripts/validate-skills.py`
4. Submit PR with skill metadata

---

## Skills Maintenance

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-10-16 | Initial release with 5 core skills |

### Deprecation Policy

Skills are versioned and deprecated with 6-month notice:

1. **Deprecation Notice**: Added to skill frontmatter
2. **Migration Guide**: Published in docs/migration/
3. **6-Month Grace Period**: Both old and new skills available
4. **Archive**: Deprecated skills moved to `skills/archived/`

### Feedback

Help us improve skills:

- **GitHub Issues**: [Report issues](https://github.com/williamzujkowski/standards/issues)
- **Discussions**: [Suggest improvements](https://github.com/williamzujkowski/standards/discussions)
- **PRs**: [Contribute enhancements](https://github.com/williamzujkowski/standards/pulls)

---

## Additional Resources

### Documentation

- **User Guide**: [SKILLS_USER_GUIDE.md](./guides/SKILLS_USER_GUIDE.md)
- **Migration Guide**: [MIGRATION_GUIDE.md](./migration/MIGRATION_GUIDE.md)
- **Authoring Guide**: [SKILL_AUTHORING_GUIDE.md](./guides/SKILL_AUTHORING_GUIDE.md)
- **API Docs**: [SKILLS_API.md](./api/SKILLS_API.md)

### Tools

- **Skill Loader**: `python3 scripts/skill-loader.py`
- **Validator**: `python3 scripts/validate-skills.py`
- **Generator**: `python3 scripts/generate-skill.py`

### Support

- **GitHub**: [williamzujkowski/standards](https://github.com/williamzujkowski/standards)
- **Issues**: [Report bugs](https://github.com/williamzujkowski/standards/issues)
- **Discussions**: [Community support](https://github.com/williamzujkowski/standards/discussions)

---

*Last Updated: 2025-10-16*
*Version: 1.0.0*
*Core Documented Skills: 5 | Total Available: 62+*
*Maintained by: Standards Repository Team*
