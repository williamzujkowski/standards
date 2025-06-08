# CLAUDE.md - LLM-Optimized Project Standards Router

**Purpose:** Minimal-token abstraction layer for accessing comprehensive project standards
**Token Reduction:** ~85% compared to full standards inclusion
**Last Updated:** January 2025

---

## 🚀 Quick Project Config

```yaml
project:
  language: Python
  style: PEP8 + Black (88 chars)
  testing: pytest (85%+ coverage)
  docs: Google-style docstrings

commands:
  setup: "python -m venv venv && source venv/bin/activate && pip install -e '.[dev]'"
  lint: "black . && isort . && flake8 && mypy ."
  test: "pytest --cov=src"
```

---

## 📚 Standards Library Index

### Core Standards
- **CS** → `CODING_STANDARDS.md` - Style, architecture, patterns
- **TS** → `TESTING_STANDARDS.md` - Testing principles, QA frameworks
- **US** → `UNIFIED_STANDARDS.md` - Comprehensive development lifecycle

### Domain Standards
- **SEC** → `MODERN_SECURITY_STANDARDS.md` - Security, auth, crypto
- **CN** → `CLOUD_NATIVE_STANDARDS.md` - Containers, K8s, microservices
- **DE** → `DATA_ENGINEERING_STANDARDS.md` - Pipelines, ETL, analytics
- **FE** → `FRONTEND_MOBILE_STANDARDS.md` - UI/UX, React, mobile
- **WD** → `WEB_DESIGN_UX_STANDARDS.md` - Visual design, UX patterns
- **CON** → `CONTENT_STANDARDS.md` - Writing, editorial, SEO
- **PM** → `PROJECT_MANAGEMENT_STANDARDS.md` - Agile, planning, stakeholders
- **GH** → `GITHUB_PLATFORM_STANDARDS.md` - CI/CD, workflows, automation
- **DOP** → `DEVOPS_PLATFORM_STANDARDS.md` - IaC, platform engineering, SRE
- **EVT** → `EVENT_DRIVEN_STANDARDS.md` - Events, messaging, streaming
- **OBS** → `OBSERVABILITY_STANDARDS.md` - Monitoring, logging, tracing
- **COST** → `COST_OPTIMIZATION_STANDARDS.md` - FinOps, efficiency
- **LEG** → `LEGAL_COMPLIANCE_STANDARDS.md` - Privacy, licensing, compliance
- **SEO** → `SEO_WEB_MARKETING_STANDARDS.md` - Technical SEO, marketing automation

---

## 🎯 Task-Based Loading Guide

### For Code Generation Tasks
```
Load: CS:style,architecture + TS:core-principles
Optional: Domain-specific standards based on feature type
```

### For Bug Fixes
```
Load: TS:regression-testing + CS:error-handling
Skip: Architecture patterns, optimization standards
```

### For Security Reviews
```
Load: SEC:all + CS:security-section
Focus: Input validation, auth, encryption
```

### For API Development
```
Load: CS:api-design + SEC:api-security + TS:integration
Reference: RESTful patterns, OpenAPI specs
```

### For Performance Optimization
```
Load: CS:performance + OBS:metrics + COST:optimization
Focus: Profiling, caching, resource efficiency
```

### For Infrastructure & DevOps
```
Load: DOP:iac + CN:kubernetes + GH:cicd
Focus: Terraform, K8s, GitOps, pipelines
```

### For Design & User Experience
```
Load: WD:* + FE:ui-components + CS:patterns
Focus: Design systems, components, accessibility
```

### For Content & Documentation
```
Load: CON:* + WD:typography + CS:documentation
Focus: Writing guidelines, SEO, editorial process
```

### For Project Management
```
Load: PM:* + US:planning + CS:architecture
Focus: Agile practices, sprint planning, risk management
```

### For Legal Compliance
```
Load: LEG:privacy + LEG:licensing + CS:security
Focus: GDPR compliance, license scanning, audit trails
```

### For SEO & Marketing
```
Load: SEO:technical + CON:seo + FE:performance
Focus: Core Web Vitals, schema markup, content optimization
```

---

## 🔧 Dynamic Loading Syntax

When requesting specific standards, use these patterns:

- `@load CS:3.1` - Load specific section
- `@load TS:core` - Load core principles only
- `@load SEC:*` - Load entire security standards
- `@load [CS:style, TS:unit, SEC:auth]` - Load multiple sections

---

## 📊 Standard Abbreviations

```yaml
patterns:
  DI: Dependency Injection
  SOLID: Single responsibility, Open/closed, Liskov, Interface segregation, Dependency inversion
  DRY: Don't Repeat Yourself
  KISS: Keep It Simple, Stupid
  YAGNI: You Aren't Gonna Need It

testing:
  TDD: Test-Driven Development
  BDD: Behavior-Driven Development
  AAA: Arrange-Act-Assert
  SUT: System Under Test

security:
  RBAC: Role-Based Access Control
  MFA: Multi-Factor Authentication
  JWT: JSON Web Token
  OWASP: Open Web Application Security Project

operations:
  CI/CD: Continuous Integration/Deployment
  IaC: Infrastructure as Code
  SLO/SLA: Service Level Objective/Agreement
  RTO/RPO: Recovery Time/Point Objective
```

---

## 💡 Smart Prompting Templates

### Basic Code Generation
```
Generate [FEATURE] following project standards.
Context: @load CS:style,arch + TS:coverage
Requirements: [SPECIFIC_NEEDS]
```

### Comprehensive Test Suite
```
Create tests for [MODULE].
Standards: @load TS:all
Coverage target: 85%+ (95% for critical paths)
Include: unit, integration, edge cases
```

### Security Hardening
```
Review and harden [COMPONENT].
Standards: @load SEC:relevant-sections
Focus: OWASP Top 10, input validation, auth
```

---

## 🔍 Section Quick Reference

### CODING_STANDARDS.md Sections
- 3.1: Style & Formatting
- 3.2: Documentation
- 3.3: Architecture & Patterns
- 3.4: Security Practices
- 3.5: Performance
- 3.6: Error Handling

### TESTING_STANDARDS.md Sections
- 4.1: Core Principles (hypothesis, regression, benchmarks)
- 4.2: Quality Assurance (coverage, static analysis)
- 4.3: Security & Resilience Testing
- 4.4: Documentation & Integration Testing

### PROJECT_MANAGEMENT_STANDARDS.md Sections
- 1-2: Core Principles & Methodology
- 3-4: Project Lifecycle & Agile
- 5-6: Planning, Risk & Issues
- 7-8: Stakeholder & Team Management
- 9-10: Metrics & Implementation

### LEGAL_COMPLIANCE_STANDARDS.md Sections
- 1-2: Principles & Privacy (GDPR)
- 3-4: Licensing & Accessibility
- 5-6: Security Compliance & IP
- 7-8: Audit & Implementation

### SEO_WEB_MARKETING_STANDARDS.md Sections
- 1-3: Technical SEO & Architecture
- 4-5: Performance & Schema
- 6-7: Content Marketing & Analytics
- 8-10: Automation & Implementation

### Key Performance Indicators
- Code Coverage: 85%+ (95% critical)
- Response Time: p95 < 200ms
- Error Rate: < 0.1%
- Security Score: A+ (via scanning tools)
- SEO Score: 90+ (Lighthouse)
- Accessibility: WCAG 2.1 AA

---

## 🚨 Critical Requirements

**ALWAYS ENFORCE:**
1. Input validation on all external data
2. Type hints for all functions
3. Error handling with custom exceptions
4. Security by default (auth, encryption)
5. Tests before implementation (TDD)

**NEVER ALLOW:**
1. Hardcoded secrets or credentials
2. Unvalidated user input
3. Empty catch blocks
4. Direct SQL queries (use ORM/parameterized)
5. Synchronous blocking I/O in async contexts

---

## 📝 Usage Examples

### Example 1: Creating a New API Endpoint
```
User: "Create a REST API endpoint for user management"
System: Loading @load [CS:api-design, SEC:api-security, TS:integration]
Result: Minimal tokens loaded, focused on API-specific standards
```

### Example 2: Debugging Performance Issue
```
User: "Debug slow database queries"
System: Loading @load [CS:performance, DE:optimization, OBS:metrics]
Result: Only performance-related standards loaded
```

### Example 3: Implementing Authentication
```
User: "Add JWT authentication to the application"
System: Loading @load [SEC:auth, CS:security, TS:security-testing]
Result: Security-focused standards without unrelated content
```

### Example 4: Privacy Compliance Implementation
```
User: "Implement GDPR compliance for user data"
System: Loading @load [LEG:privacy, SEC:encryption, CS:audit]
Result: Privacy and compliance focused standards
```

### Example 5: SEO Optimization
```
User: "Optimize website for search engines"
System: Loading @load [SEO:technical, FE:performance, CON:seo]
Result: SEO and performance optimization standards
```

---

## 🔄 Maintenance Notes

- This file serves as a router, not a content repository
- Update only when adding new standard documents
- Keep descriptions concise (< 10 words per item)
- Maintain consistent abbreviation scheme
- Test loading patterns remain valid

---

**Token Optimization Result:** This document uses ~500 tokens vs ~5000+ for full standards inclusion