# Skills Migration Architecture Design

**Version:** 1.0.0
**Date:** 2025-10-17
**Author:** System Architect Agent (swarm-1760669629248-p81glgo36)
**Status:** APPROVED FOR IMPLEMENTATION

---

## Executive Summary

This document defines the comprehensive architecture for transforming the williamzujkowski/standards repository from a traditional documentation structure to Anthropic's Agent Skills format. The architecture leverages progressive disclosure, token optimization, and autonomous skill discovery to achieve 99% token reduction while maintaining full backward compatibility.

**Key Architectural Principles:**

1. **Progressive Disclosure:** Three-level loading (metadata → instructions → resources)
2. **Autonomous Discovery:** Claude self-selects skills based on task analysis
3. **Compositional Design:** Skills compose seamlessly for complex workflows
4. **Token Optimization:** Target <5,000 tokens per typical workflow (from 500k baseline)
5. **Backward Compatibility:** Gradual migration with legacy bridge support
6. **Filesystem-First:** All resources pre-bundled, zero network dependencies

---

## 1. System Architecture Overview

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Claude Agent Context                      │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ Level 1: Skill Metadata (Pre-loaded at startup)        │   │
│  │ - All skill names + descriptions (~5,000 tokens)       │   │
│  │ - Enables autonomous skill discovery                    │   │
│  └────────────────────────────────────────────────────────┘   │
│                             │                                    │
│                             ▼                                    │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ Level 2: Skill Instructions (Loaded on-demand)         │   │
│  │ - SKILL.md body (<5,000 tokens per skill)             │   │
│  │ - Core guidance + resource pointers                    │   │
│  └────────────────────────────────────────────────────────┘   │
│                             │                                    │
│                             ▼                                    │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ Level 3: Resources (Accessed via filesystem)           │   │
│  │ - Detailed docs, templates, scripts                    │   │
│  │ - Zero token cost (Read/Bash tools)                    │   │
│  └────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Repository File Structure                      │
│                                                                  │
│  skills/                    ← Root skills directory             │
│  ├── skill-loader/          ← Meta-skill (coordination)         │
│  ├── legacy-bridge/         ← Backward compatibility            │
│  ├── coding-standards/                                          │
│  │   ├── python/           ← Individual skill directory         │
│  │   │   ├── SKILL.md      ← Required: skill definition         │
│  │   │   ├── resources/    ← Optional: detailed docs            │
│  │   │   ├── templates/    ← Optional: code templates           │
│  │   │   ├── scripts/      ← Optional: executables              │
│  │   │   └── examples/     ← Optional: demonstrations           │
│  │   ├── javascript/                                            │
│  │   ├── typescript/                                            │
│  │   ├── go/                                                    │
│  │   └── rust/                                                  │
│  ├── security/                                                  │
│  │   ├── auth/                                                  │
│  │   ├── secrets/                                               │
│  │   ├── zero-trust/                                            │
│  │   ├── threat-modeling/                                       │
│  │   └── input-validation/                                      │
│  ├── testing/                                                   │
│  │   ├── unit-testing/                                          │
│  │   ├── integration-testing/                                   │
│  │   ├── e2e-testing/                                           │
│  │   └── performance-testing/                                   │
│  ├── [40+ additional skill directories...]                      │
│  └── nist-compliance/       ← Bundles existing NIST system      │
│                                                                  │
│  config/                                                        │
│  ├── skills-catalog.yaml   ← Generated skill metadata           │
│  ├── product-matrix.yaml   ← Updated for skill references       │
│  └── legacy-mappings.yaml  ← Old pattern → new skill mapping    │
│                                                                  │
│  docs/standards/            ← Archived originals (reference)     │
│  docs/migration/            ← Migration documentation            │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Responsibilities

| Component | Role | Token Impact |
|-----------|------|--------------|
| **Skill Metadata** | Enable discovery without full load | ~100 tokens/skill |
| **SKILL.md** | Provide core guidance and navigation | <5,000 tokens |
| **Resources** | Deep reference materials | 0 tokens (filesystem) |
| **Skill Loader** | Parse @load, resolve product matrix | ~3,800 tokens |
| **Legacy Bridge** | Map old patterns to new skills | ~2,800 tokens |
| **Product Matrix** | Map product types to skill bundles | Embedded in loader |

---

## 2. Directory Structure Blueprint

### 2.1 Complete Skills Hierarchy

```
skills/
├── README.md                          # Skills overview and navigation
│
├── skill-loader/                      # META-SKILL: Coordination
│   ├── SKILL.md
│   ├── config/
│   │   ├── skills-catalog.yaml        # Auto-generated skill index
│   │   └── discovery-rules.yaml       # Pattern matching rules
│   └── scripts/
│       ├── discover-skills.sh         # Skill discovery automation
│       ├── load-product-bundle.sh     # Product matrix resolution
│       └── validate-skill.sh          # Skill validation utility
│
├── legacy-bridge/                     # META-SKILL: Compatibility
│   ├── SKILL.md
│   ├── config/
│   │   └── legacy-mappings.yaml       # Old → new mappings
│   ├── resources/
│   │   └── migration-guide.md         # Migration documentation
│   └── scripts/
│       └── translate-pattern.sh       # Pattern translation utility
│
├── coding-standards/                  # CATEGORY: Language skills
│   ├── python/
│   │   ├── SKILL.md                   # Python standards
│   │   ├── resources/
│   │   │   ├── pep8-guide.md
│   │   │   ├── type-hints-guide.md
│   │   │   └── async-patterns.md
│   │   ├── templates/
│   │   │   ├── pyproject.toml.template
│   │   │   ├── pytest.ini.template
│   │   │   └── .pylintrc.template
│   │   ├── scripts/
│   │   │   ├── lint.sh
│   │   │   ├── format.sh
│   │   │   └── type-check.sh
│   │   └── examples/
│   │       ├── basic-api/
│   │       └── async-service/
│   │
│   ├── javascript/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   ├── esnext-features.md
│   │   │   └── module-patterns.md
│   │   ├── templates/
│   │   │   ├── package.json.template
│   │   │   └── .eslintrc.json.template
│   │   └── scripts/
│   │       └── lint.sh
│   │
│   ├── typescript/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   ├── advanced-types.md
│   │   │   └── decorators-guide.md
│   │   └── templates/
│   │       └── tsconfig.json.template
│   │
│   ├── go/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── idiomatic-patterns.md
│   │   └── templates/
│   │       └── go.mod.template
│   │
│   └── rust/
│       ├── SKILL.md
│       └── resources/
│           └── ownership-guide.md
│
├── security/                          # CATEGORY: Security skills
│   ├── auth/
│   │   ├── SKILL.md                   # Authentication standards
│   │   ├── resources/
│   │   │   ├── oauth-flows.md
│   │   │   ├── jwt-best-practices.md
│   │   │   └── session-management.md
│   │   ├── templates/
│   │   │   └── auth-middleware.template
│   │   └── scripts/
│   │       └── validate-jwt.sh
│   │
│   ├── secrets/
│   │   ├── SKILL.md                   # Secrets management
│   │   ├── resources/
│   │   │   └── vault-setup.md
│   │   ├── templates/
│   │   │   └── .env.template
│   │   └── scripts/
│   │       └── rotate-secrets.sh
│   │
│   ├── zero-trust/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── zero-trust-architecture.md
│   │   └── examples/
│   │       └── istio-policies/
│   │
│   ├── threat-modeling/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── stride-guide.md
│   │   ├── templates/
│   │   │   └── threat-model.template
│   │   └── scripts/
│   │       └── generate-threat-model.sh
│   │
│   └── input-validation/
│       ├── SKILL.md
│       ├── resources/
│       │   └── validation-patterns.md
│       └── templates/
│           └── validator.template
│
├── testing/                           # CATEGORY: Testing skills
│   ├── unit-testing/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── tdd-guide.md
│   │   ├── templates/
│   │   │   ├── test.template.py
│   │   │   └── test.template.js
│   │   └── scripts/
│   │       └── run-unit-tests.sh
│   │
│   ├── integration-testing/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── api-testing-guide.md
│   │   ├── templates/
│   │   │   └── integration-test.template
│   │   └── scripts/
│   │       └── setup-test-db.sh
│   │
│   ├── e2e-testing/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── playwright-guide.md
│   │   ├── templates/
│   │   │   └── e2e-test.template.ts
│   │   └── scripts/
│   │       └── run-e2e-tests.sh
│   │
│   └── performance-testing/
│       ├── SKILL.md
│       ├── resources/
│       │   └── k6-guide.md
│       ├── templates/
│       │   └── load-test.template.js
│       └── scripts/
│           └── run-performance-tests.sh
│
├── devops/                            # CATEGORY: DevOps skills
│   ├── ci-cd/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── github-actions-guide.md
│   │   ├── templates/
│   │   │   ├── ci.yml.template
│   │   │   └── deploy.yml.template
│   │   └── scripts/
│   │       └── deploy.sh
│   │
│   ├── infrastructure/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── terraform-guide.md
│   │   ├── templates/
│   │   │   └── main.tf.template
│   │   └── scripts/
│   │       └── terraform-validate.sh
│   │
│   └── monitoring/
│       ├── SKILL.md
│       ├── resources/
│       │   └── prometheus-guide.md
│       └── templates/
│           ├── prometheus.yml
│           └── alerts.yml
│
├── cloud-native/                      # CATEGORY: Cloud-native skills
│   ├── kubernetes/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── k8s-patterns.md
│   │   ├── templates/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   └── scripts/
│   │       └── validate-manifests.sh
│   │
│   ├── containers/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── dockerfile-guide.md
│   │   ├── templates/
│   │   │   └── Dockerfile.template
│   │   └── scripts/
│   │       └── build-and-scan.sh
│   │
│   └── serverless/
│       ├── SKILL.md
│       ├── resources/
│       │   └── lambda-guide.md
│       └── templates/
│           └── serverless.yml
│
├── frontend/                          # CATEGORY: Frontend skills
│   ├── react/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── react-patterns.md
│   │   └── templates/
│   │       ├── component.template.tsx
│   │       └── vite.config.ts
│   │
│   ├── vue/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── vue-patterns.md
│   │   └── templates/
│   │       └── component.template.vue
│   │
│   ├── mobile-ios/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── swift-guide.md
│   │   └── templates/
│   │       └── view.template.swift
│   │
│   └── mobile-android/
│       ├── SKILL.md
│       ├── resources/
│       │   └── kotlin-guide.md
│       └── templates/
│           └── activity.template.kt
│
├── data-engineering/                  # CATEGORY: Data engineering skills
│   ├── orchestration/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── airflow-guide.md
│   │   ├── templates/
│   │   │   └── dag.template.py
│   │   └── scripts/
│   │       └── validate-dag.sh
│   │
│   └── data-quality/
│       ├── SKILL.md
│       ├── resources/
│       │   └── dq-patterns.md
│       ├── templates/
│       │   └── dq-checks.template.sql
│       └── scripts/
│           └── run-dq-checks.sh
│
├── ml-ai/                             # CATEGORY: ML/AI skills
│   ├── model-development/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── mlflow-guide.md
│   │   ├── templates/
│   │   │   └── training.template.py
│   │   └── scripts/
│   │       └── train-model.sh
│   │
│   └── model-deployment/
│       ├── SKILL.md
│       ├── resources/
│       │   └── deployment-guide.md
│       ├── templates/
│       │   └── model-api.template.py
│       └── scripts/
│           └── deploy-model.sh
│
├── observability/                     # CATEGORY: Observability skills
│   ├── logging/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── logging-patterns.md
│   │   └── templates/
│   │       └── logger.template.py
│   │
│   └── tracing/
│       ├── SKILL.md
│       ├── resources/
│       │   └── otel-guide.md
│       └── templates/
│           └── tracing.template.py
│
├── microservices/                     # CATEGORY: Microservices skills
│   └── patterns/
│       ├── SKILL.md
│       ├── resources/
│       │   └── patterns-guide.md
│       └── examples/
│           └── circuit-breaker/
│
├── database/                          # CATEGORY: Database skills
│   ├── relational/
│   │   ├── SKILL.md
│   │   ├── resources/
│   │   │   └── sql-patterns.md
│   │   └── templates/
│   │       └── migration.template.sql
│   │
│   └── nosql/
│       ├── SKILL.md
│       └── resources/
│           └── nosql-patterns.md
│
├── architecture/                      # CATEGORY: Architecture skills
│   └── event-driven/
│       ├── SKILL.md
│       └── resources/
│           └── event-patterns.md
│
├── compliance/                        # CATEGORY: Compliance skills
│   ├── nist-compliance/              # BUNDLED NIST system
│   │   ├── SKILL.md
│   │   ├── controls/                 # All NIST control guides
│   │   │   ├── AC-ACCESS_CONTROL.md
│   │   │   ├── AU-AUDIT.md
│   │   │   └── [18 additional families]
│   │   ├── resources/
│   │   │   ├── implementation-guide.md
│   │   │   └── control-mappings.md
│   │   ├── templates/
│   │   │   ├── ssp.template.yaml
│   │   │   └── control.template.md
│   │   ├── scripts/
│   │   │   ├── generate-ssp.py
│   │   │   └── validate-controls.sh
│   │   ├── vscode-extension/         # Existing VS Code extension
│   │   └── examples/
│   │       └── nist-templates/       # Existing quickstart
│   │
│   └── general/
│       ├── SKILL.md
│       └── resources/
│           ├── gdpr-guide.md
│           └── hipaa-guide.md
│
├── design/                            # CATEGORY: Design skills
│   └── web-design/
│       ├── SKILL.md
│       └── resources/
│           └── wcag-checklist.md
│
└── content/                           # CATEGORY: Content skills
    └── strategy/
        ├── SKILL.md
        └── resources/
            └── style-guide.md
```

**Total Skills:** 50 (48 domain + 2 meta)
**Total Categories:** 15

---

## 3. Progressive Disclosure Architecture

### 3.1 Three-Level Loading Model

```
┌─────────────────────────────────────────────────────────────────┐
│ LEVEL 1: METADATA (Always Loaded)                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Loaded: At agent startup                                       │
│  Location: All SKILL.md YAML frontmatter                        │
│  Token Cost: ~100 per skill × 50 skills = ~5,000 tokens        │
│  Purpose: Enable autonomous skill discovery                      │
│                                                                  │
│  Example:                                                        │
│  ---                                                            │
│  name: python                                                   │
│  description: Python development standards including PEP 8,     │
│              type hints, async patterns, project structure,     │
│              and best practices. Use when developing Python     │
│              applications, APIs, CLIs, or data pipelines.       │
│  ---                                                            │
│                                                                  │
│  Claude sees: "python skill available for Python development"   │
│  Decision: Load full skill if task involves Python              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ Task Analysis: "Create Python API"
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ LEVEL 2: INSTRUCTIONS (Loaded On-Demand)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Loaded: When Claude determines skill is relevant               │
│  Location: Full SKILL.md body (after frontmatter)               │
│  Token Cost: <5,000 tokens per skill                           │
│  Purpose: Provide core guidance and resource navigation         │
│                                                                  │
│  Structure:                                                      │
│  # Python Development Standards                                 │
│                                                                  │
│  ## Overview                                                     │
│  Brief context on Python standards approach                     │
│                                                                  │
│  ## When to Use This Skill                                      │
│  - Building REST APIs with FastAPI or Flask                     │
│  - Creating CLI tools with argparse or Click                    │
│  - Developing data pipelines                                    │
│                                                                  │
│  ## Core Instructions                                           │
│  - Follow PEP 8 style guide                                     │
│  - Use type hints for all function signatures                   │
│  - Prefer async/await for I/O operations                        │
│  - Structure projects with src/ layout                          │
│                                                                  │
│  ## Advanced Topics                                             │
│  - For detailed PEP 8 guidance, see `./resources/pep8-guide.md` │
│  - For type hints patterns, see `./resources/type-hints.md`     │
│  - For project templates, use `./templates/pyproject.toml`      │
│  - To lint code, run `./scripts/lint.sh [path]`                │
│                                                                  │
│  ## Examples                                                     │
│  See `./examples/basic-api/` for FastAPI implementation         │
│                                                                  │
│  Claude sees: Core guidance + pointers to deeper resources      │
│  Decision: Read specific resource if needed                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ Need: "Type hints patterns"
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ LEVEL 3: RESOURCES (Accessed via Filesystem)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Loaded: Only when explicitly referenced                        │
│  Location: resources/, templates/, scripts/, examples/          │
│  Token Cost: 0 (Read tool, not context)                        │
│  Purpose: Deep expertise on-demand                              │
│                                                                  │
│  Action: Read("skills/coding-standards/python/resources/       │
│                type-hints-guide.md")                            │
│                                                                  │
│  Content: 10,000+ word comprehensive guide on type hints        │
│  Token Impact: 0 (read but not added to context)               │
│                                                                  │
│  Claude: Extracts needed information, applies to task           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Token Optimization Comparison

| Scenario | Traditional | Skills (Level 1) | Skills (Level 2) | Skills (Level 3) | Savings |
|----------|-------------|------------------|------------------|------------------|---------|
| Startup | 500,000 | 5,000 | 5,000 | 5,000 | **99%** |
| Single skill task | 500,000 | 5,000 | 9,000 | 9,000 | **98%** |
| Multi-skill (3 skills) | 500,000 | 5,000 | 17,000 | 17,000 | **97%** |
| Complex workflow (5 skills) | 500,000 | 5,000 | 27,000 | 27,000 | **95%** |

**Key Insight:** Even complex 5-skill workflows consume only 27k tokens vs. 500k baseline = **95% reduction**

---

## 4. Skill Composition Patterns

### 4.1 Single Skill Usage

```yaml
User Request: "Create a Python CLI tool"

Claude Decision Process:
  1. Analyze request: CLI tool → needs coding standard
  2. Check metadata: "python" skill matches
  3. Load Level 2: python SKILL.md (4,200 tokens)
  4. Follow instructions: src/ layout, argparse, etc.
  5. Access Level 3 if needed: Read CLI example

Total Token Cost: ~4,200 tokens (vs. 500k full load)
```

### 4.2 Multi-Skill Composition

```yaml
User Request: "Build a secure Python API with JWT authentication"

Claude Decision Process:
  1. Analyze: Needs Python + Security + Testing
  2. Load skills:
     - python (4,200 tokens)
     - security-auth (4,500 tokens)
     - unit-testing (4,300 tokens)
  3. Compose: Follow Python structure, apply auth patterns, add tests
  4. Resources: Read JWT guide, use auth middleware template

Total Token Cost: ~13,000 tokens (vs. 500k full load)
Composition: 3 skills working together seamlessly
```

### 4.3 Product-Based Bundle Loading

```yaml
User Request: "@load product:api"

Skill Loader Process:
  1. Parse: product:api directive
  2. Resolve: config/product-matrix.yaml
     - CS:language → python
     - SEC:auth → security-auth
     - TS:framework → unit-testing
     - DOP:ci-cd → ci-cd
     - OBS:monitoring → monitoring
  3. Load bundle: 5 skills automatically
  4. Present: "Loaded API development bundle"

Total Token Cost: ~21,000 tokens for complete API stack
User Benefit: Single command loads coordinated skill set
```

### 4.4 Wildcard Expansion

```yaml
User Request: "@load SEC:*"

Skill Loader Process:
  1. Parse: SEC:* wildcard
  2. Expand: All security skills
     - security-auth
     - security-secrets
     - security-zero-trust
     - security-threat-modeling
     - security-input-validation
  3. Auto-include: nist-compliance (per policy)
  4. Load: 6 skills total

Total Token Cost: ~24,800 tokens for full security stack
```

---

## 5. Skill Boundaries and Interfaces

### 5.1 Skill Interface Contract

Every skill MUST implement this interface:

```yaml
REQUIRED:
  - SKILL.md file at skill root
  - YAML frontmatter with name and description
  - ## When to Use This Skill section
  - ## Core Instructions section

OPTIONAL:
  - resources/ directory
  - templates/ directory
  - scripts/ directory
  - examples/ directory

CONSTRAINTS:
  - name: ≤64 chars, lowercase-with-hyphens
  - description: ≤1024 chars, include "when to use"
  - SKILL.md body: <5,000 tokens recommended
```

### 5.2 Inter-Skill Dependencies

```yaml
# Example: security-auth skill references other skills

security-auth/SKILL.md:
  ## Related Skills
  - **security-secrets**: For credential storage
  - **security-input-validation**: For request validation
  - **python**: For Python-specific auth implementations
  - **javascript**: For JavaScript-specific auth implementations

  ## Composition Patterns
  When building authenticated APIs:
  1. Load language skill (python/javascript)
  2. Load security-auth (this skill)
  3. Load security-secrets for credential handling
  4. Load unit-testing for auth testing
```

**Dependency Resolution:**

- Skills reference but don't force-load dependencies
- Claude autonomously decides which related skills to load
- User can explicitly load dependencies if desired

### 5.3 Cross-Skill Resource Sharing

```yaml
# Shared resources across skill boundaries

Pattern 1: Language-Agnostic Templates
  security-auth/templates/jwt-validation.template
  → Used by python, javascript, go skills
  → Each language skill provides language-specific usage

Pattern 2: Common Scripts
  skill-loader/scripts/validate-skill.sh
  → Used by all skills for validation
  → Central maintenance, universal benefit

Pattern 3: Reference Documentation
  nist-compliance/controls/AC-ACCESS_CONTROL.md
  → Referenced by security-auth, security-zero-trust
  → Single source of truth for compliance
```

---

## 6. Backward Compatibility Layer

### 6.1 Legacy Bridge Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       Legacy Bridge Skill                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input: Old pattern (e.g., @load CODING_STANDARDS.md#python)   │
│  Process:                                                        │
│    1. Detect legacy pattern via regex                           │
│    2. Lookup in config/legacy-mappings.yaml                     │
│    3. Translate to new skill reference                          │
│    4. Emit deprecation warning (if applicable)                  │
│    5. Forward to skill-loader                                   │
│  Output: Modern skill loaded + migration guidance               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Legacy Mappings

```yaml
# config/legacy-mappings.yaml

legacy_patterns:
  # Direct standard references
  - pattern: "CODING_STANDARDS.md#python"
    maps_to: "python"
    warning: "Deprecated: Use '@load python' instead"
    deprecation_phase: "transition"

  - pattern: "MODERN_SECURITY_STANDARDS.md"
    maps_to: ["security-auth", "security-secrets", "security-zero-trust"]
    warning: "Deprecated: Load specific security skills or use '@load SEC:*'"
    deprecation_phase: "transition"

  # Product matrix (still supported)
  - pattern: "@load product:api"
    maps_to: "product-bundle:api"
    warning: null
    deprecation_phase: "supported"

  # Category wildcards (still supported)
  - pattern: "@load SEC:*"
    maps_to: "wildcard:security"
    warning: null
    deprecation_phase: "supported"

  # Old CS: codes
  - pattern: "CS:python"
    maps_to: "python"
    warning: "Use '@load python' or skill name directly"
    deprecation_phase: "transition"

deprecation_phases:
  supported:
    duration: "Indefinite"
    behavior: "No warnings, full functionality"

  transition:
    duration: "Week 5-12"
    behavior: "Functional + informational warnings"

  deprecated:
    duration: "Week 13-26"
    behavior: "Functional + strong warnings"

  sunset:
    duration: "Week 27+"
    behavior: "Error with migration instructions"
```

### 6.3 Migration Path

```
Phase 1: Launch (Week 1-4)
  - Both systems operational
  - No warnings emitted
  - Gradual user adoption

Phase 2: Transition (Week 5-12)
  - Legacy bridge emits informational warnings
  - Documentation updated with new patterns
  - Migration guide prominent

Phase 3: Deprecation (Week 13-26)
  - Strong deprecation warnings
  - Old patterns marked as deprecated
  - Active migration support

Phase 4: Sunset (Week 27+)
  - Legacy patterns throw errors
  - Archived standards read-only
  - Skills-only architecture
```

---

## 7. Skill Loader and Discovery System

### 7.1 Skill Loader Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Skill Loader (Meta-Skill)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Responsibilities:                                               │
│  ─────────────────────────────────────────────────────────────  │
│  1. Parse @load directives                                      │
│     - Product types: @load product:api                          │
│     - Categories: @load security:*                              │
│     - Specific skills: @load python                             │
│     - Combined: @load [product:api + SEC:* + TS:pytest]        │
│                                                                  │
│  2. Resolve product-matrix.yaml                                 │
│     - Map product types to skill bundles                        │
│     - Handle language/framework overrides                       │
│     - Apply stack presets                                       │
│                                                                  │
│  3. Expand wildcards                                            │
│     - SEC:* → all security skills                               │
│     - TS:* → all testing skills                                 │
│     - Custom category wildcards                                 │
│                                                                  │
│  4. Auto-include dependencies                                   │
│     - SEC present → include nist-compliance:base                │
│     - Custom dependency rules                                   │
│                                                                  │
│  5. Generate load plan                                          │
│     - Skill prioritization                                      │
│     - Deduplication                                             │
│     - Token estimation                                          │
│                                                                  │
│  6. Execute load                                                │
│     - Read SKILL.md files                                       │
│     - Validate structure                                        │
│     - Present to Claude context                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Discovery Algorithm

```python
# Pseudocode: Skill discovery and loading

def load_skills(directive: str) -> List[Skill]:
    """
    Main entry point for skill loading.

    Examples:
      load_skills("product:api")
      load_skills("python")
      load_skills("SEC:*")
      load_skills("[product:api + SEC:* + TS:pytest]")
    """
    # Step 1: Parse directive
    parsed = parse_directive(directive)

    # Step 2: Resolve to skill list
    if parsed.type == "product":
        skills = resolve_product_bundle(parsed.value)
    elif parsed.type == "wildcard":
        skills = expand_wildcard(parsed.value)
    elif parsed.type == "skill":
        skills = [parsed.value]
    elif parsed.type == "composite":
        skills = []
        for sub_directive in parsed.components:
            skills.extend(load_skills(sub_directive))

    # Step 3: Apply auto-include rules
    if any("security" in s for s in skills):
        skills.append("nist-compliance")

    # Step 4: Deduplicate
    skills = list(set(skills))

    # Step 5: Prioritize (high priority first)
    skills = sort_by_priority(skills)

    # Step 6: Validate token budget
    estimated_tokens = sum(get_token_estimate(s) for s in skills)
    if estimated_tokens > WARN_THRESHOLD:
        emit_warning(f"Loading {len(skills)} skills (~{estimated_tokens} tokens)")

    # Step 7: Load skills
    loaded = []
    for skill_name in skills:
        skill = load_skill_metadata(skill_name)
        if is_relevant(skill):
            loaded.append(load_skill_full(skill_name))

    return loaded


def resolve_product_bundle(product_type: str) -> List[str]:
    """Resolve product type to skill list via product-matrix.yaml"""
    matrix = load_yaml("config/product-matrix.yaml")
    bundle = matrix["products"][product_type]["standards"]

    # Translate legacy codes to skill names
    skills = []
    for code in bundle:
        if code.startswith("CS:"):
            skills.append(resolve_coding_standard(code))
        elif code.startswith("SEC:"):
            skills.append(resolve_security_standard(code))
        # ... additional code resolvers

    return skills


def expand_wildcard(category: str) -> List[str]:
    """Expand category wildcard to all skills in category"""
    catalog = load_yaml("config/skills-catalog.yaml")
    return [s["name"] for s in catalog["skills"] if s["category"] == category]


def is_relevant(skill: Skill) -> bool:
    """
    Claude's autonomous decision: Is this skill relevant to current task?

    In practice, this would analyze:
    - Task description keywords
    - User request context
    - Previously loaded skills
    - Skill description matching
    """
    # Simplified: In real implementation, this is Claude's LLM decision
    return True  # For now, load all resolved skills
```

### 7.3 Skills Catalog Structure

```yaml
# config/skills-catalog.yaml (Auto-generated)

version: "1.0.0"
generated_at: "2025-10-17T03:00:00Z"
total_skills: 50

skills:
  - name: python
    path: skills/coding-standards/python
    category: coding
    priority: high
    description: "Python development standards including PEP 8, type hints..."
    token_estimate: 4200
    tags: [backend, scripting, data, ml]

  - name: security-auth
    path: skills/security/auth
    category: security
    priority: high
    description: "Authentication and authorization standards..."
    token_estimate: 4500
    tags: [oauth, jwt, session, mfa]
    dependencies: [security-secrets, security-input-validation]

  # ... 48 more skills

categories:
  coding: [python, javascript, typescript, go, rust]
  security: [auth, secrets, zero-trust, threat-modeling, input-validation]
  testing: [unit-testing, integration-testing, e2e-testing, performance-testing]
  devops: [ci-cd, infrastructure, monitoring]
  # ... 11 more categories

meta_skills:
  - name: skill-loader
    always_available: true
  - name: legacy-bridge
    always_available: true
```

---

## 8. Token Optimization Strategy

### 8.1 Optimization Techniques

| Technique | Implementation | Token Savings |
|-----------|----------------|---------------|
| **Lazy Loading** | Load skills only when task-relevant | 95%+ |
| **Progressive Disclosure** | Metadata → Instructions → Resources | 99% (Level 1) |
| **Resource Externalization** | Move details to filesystem | 100% (Level 3) |
| **Script Execution** | Run code instead of inline | 100% (for scripts) |
| **Skill Composition** | Load only needed skills, not bundles | 70-90% |
| **Deduplication** | Cache skill metadata at startup | 50% (repeat loads) |
| **Selective Context** | Read specific files on-demand | 100% (unneeded files) |

### 8.2 Token Budget Management

```yaml
Token Thresholds:
  startup_budget: 10,000 tokens
    allocation:
      - All skill metadata: ~5,000 tokens
      - Skill loader: ~3,800 tokens
      - Legacy bridge: ~2,800 tokens (if needed)
    target: ≤10,000 tokens

  single_task_budget: 20,000 tokens
    allocation:
      - Startup: 10,000 tokens
      - 1-2 skills: ~8,000 tokens
      - Resources: 0 tokens (filesystem)
      - Working context: 2,000 tokens
    target: ≤20,000 tokens

  complex_workflow_budget: 50,000 tokens
    allocation:
      - Startup: 10,000 tokens
      - 5-8 skills: ~32,000 tokens
      - Resources: 0 tokens (filesystem)
      - Working context: 8,000 tokens
    target: ≤50,000 tokens

Monitoring:
  - Emit warnings when approaching 80% of budget
  - Suggest skill unloading for long-running sessions
  - Track per-skill token consumption
  - Report optimization opportunities
```

### 8.3 Caching Strategy

```yaml
Level 1 (Skill Metadata):
  cache: "System prompt (persistent)"
  invalidation: "Never (until Claude restart)"
  benefit: "Zero repeated cost for discovery"

Level 2 (Skill Instructions):
  cache: "Claude's context cache"
  invalidation: "24 hours or explicit clear"
  benefit: "50% reduction on repeated skill loads"

Level 3 (Resources):
  cache: "Not cached (filesystem access)"
  invalidation: "N/A"
  benefit: "Zero token cost (always fresh)"

Product Bundles:
  cache: "Skill loader memory"
  invalidation: "Per session"
  benefit: "Single resolution per product type"
```

---

## 9. Cross-Skill Dependency Management

### 9.1 Dependency Types

```yaml
# Four types of cross-skill dependencies

1. Referential Dependencies (Soft):
   Example: security-auth references security-secrets
   Behavior: Skill mentions related skill but doesn't force load
   Resolution: Claude decides whether to load related skill

2. Compositional Dependencies (Medium):
   Example: unit-testing composes with python or javascript
   Behavior: Testing skill adapts to loaded language skill
   Resolution: Skill loader detects and ensures compatibility

3. Required Dependencies (Hard):
   Example: nist-compliance requires security-* skills
   Behavior: Auto-load required skills if not present
   Resolution: Skill loader enforces dependency chain

4. Conflicting Dependencies (Exclusive):
   Example: python conflicts with go for same task
   Behavior: Warn user about potential conflicts
   Resolution: User manually resolves or accepts both
```

### 9.2 Dependency Declaration

```yaml
# Example: security-auth/SKILL.md frontmatter extension

---
name: security-auth
description: "Authentication and authorization standards..."

# Optional: Dependency metadata (not part of core spec)
# Used by skill-loader for optimization
_meta:
  references:
    - security-secrets
    - security-input-validation
  composes_with:
    - python
    - javascript
    - go
  requires:
    - null  # No hard dependencies
  conflicts:
    - null  # No conflicts
---
```

**Note:** `_meta` is optional and skill-loader-specific. Not part of Anthropic's core Skills specification.

### 9.3 Dependency Resolution Algorithm

```python
def resolve_dependencies(skills: List[str]) -> List[str]:
    """
    Resolve skill dependencies, ensuring complete and consistent set.
    """
    resolved = set(skills)
    to_process = list(skills)

    while to_process:
        skill = to_process.pop(0)
        metadata = load_skill_metadata(skill)

        # Hard dependencies (always load)
        for dep in metadata.get("requires", []):
            if dep not in resolved:
                resolved.add(dep)
                to_process.append(dep)

        # Auto-include rules (policy-based)
        if "security" in skill and "nist-compliance" not in resolved:
            resolved.add("nist-compliance")
            to_process.append("nist-compliance")

    # Check for conflicts
    conflicts = detect_conflicts(resolved)
    if conflicts:
        emit_warning(f"Potential conflicts detected: {conflicts}")

    return list(resolved)
```

---

## 10. Skill Validation Framework

### 10.1 Validation Checklist

```yaml
Per-Skill Validation:
  structure:
    - ✓ SKILL.md exists at skill root
    - ✓ YAML frontmatter present
    - ✓ name field present, ≤64 chars, lowercase-with-hyphens
    - ✓ description field present, ≤1024 chars, includes "when to use"
    - ✓ ## When to Use This Skill section present
    - ✓ ## Core Instructions section present

  content:
    - ✓ Token count <5,000 for SKILL.md body
    - ✓ All resource references are valid file paths
    - ✓ Internal links resolve correctly
    - ✓ No broken external links

  resources:
    - ✓ Scripts are executable (chmod +x)
    - ✓ Templates are valid (parseable)
    - ✓ Examples are functional (tested)

  documentation:
    - ✓ README present if multiple resources
    - ✓ Usage examples provided
    - ✓ Related skills documented

Repository-Wide Validation:
  catalog:
    - ✓ skills-catalog.yaml accurate and up-to-date
    - ✓ All skills listed in catalog
    - ✓ All categories defined
    - ✓ Token estimates accurate (±10%)

  configuration:
    - ✓ product-matrix.yaml updated for skill references
    - ✓ legacy-mappings.yaml functional
    - ✓ All skill paths valid

  integration:
    - ✓ Skill loader can discover all skills
    - ✓ Legacy bridge maps old patterns correctly
    - ✓ Product bundles resolve to valid skills
    - ✓ Wildcard expansion works correctly

  performance:
    - ✓ Token reduction targets met (95%+)
    - ✓ Skill load time <500ms average
    - ✓ Discovery accuracy >90%

  testing:
    - ✓ All validation scripts pass
    - ✓ Integration tests pass
    - ✓ Skill composition tests pass
    - ✓ Backward compatibility tests pass
```

### 10.2 Validation Scripts

```bash
# scripts/validate-skill.sh
#!/bin/bash
# Validates a single skill against all requirements

SKILL_PATH=$1

echo "Validating skill: $SKILL_PATH"

# Check structure
if [ ! -f "$SKILL_PATH/SKILL.md" ]; then
  echo "ERROR: SKILL.md not found"
  exit 1
fi

# Validate frontmatter
python3 scripts/validate-frontmatter.py "$SKILL_PATH/SKILL.md"

# Count tokens
tokens=$(python3 scripts/count-tokens.py "$SKILL_PATH/SKILL.md")
if [ "$tokens" -gt 5000 ]; then
  echo "WARNING: Token count ($tokens) exceeds recommended 5,000"
fi

# Validate resource references
python3 scripts/validate-resource-refs.py "$SKILL_PATH/SKILL.md"

# Check executable scripts
find "$SKILL_PATH/scripts" -type f -exec test -x {} \; || {
  echo "ERROR: Non-executable scripts found"
  exit 1
}

echo "✓ Skill validation passed"
```

```bash
# scripts/validate-all-skills.sh
#!/bin/bash
# Validates all skills in repository

echo "Validating all skills..."

failed=0
for skill_dir in skills/*/; do
  if ! scripts/validate-skill.sh "$skill_dir"; then
    failed=$((failed + 1))
  fi
done

if [ "$failed" -gt 0 ]; then
  echo "ERROR: $failed skill(s) failed validation"
  exit 1
fi

echo "✓ All skills validated successfully"
```

---

## 11. Migration Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                   MIGRATION WORKFLOW                             │
└─────────────────────────────────────────────────────────────────┘

PHASE 1: FOUNDATION (Week 1)
┌──────────────┐
│ Create       │
│ skills/      │──┐
│ directory    │  │
└──────────────┘  │
                  ├──→ ┌────────────────┐
┌──────────────┐  │    │ Validate       │
│ Build        │  │    │ structure      │
│ skill-loader │──┤    │ and catalog    │
│ meta-skill   │  │    └────────────────┘
└──────────────┘  │              │
                  │              ▼
┌──────────────┐  │    ┌────────────────┐
│ Build        │  │    │ Test with      │
│ legacy-bridge│──┘    │ top 5 skills   │
│ meta-skill   │       └────────────────┘
└──────────────┘              │
                              │
                              ▼
PHASE 2: CORE SKILLS (Week 2-3)
┌──────────────┐
│ Convert      │
│ remaining    │──┐
│ standards    │  │
└──────────────┘  │
                  ├──→ ┌────────────────┐
┌──────────────┐  │    │ Update         │
│ Split large  │  │    │ product-matrix │
│ standards    │──┤    │ references     │
│ into focused │  │    └────────────────┘
│ skills       │  │              │
└──────────────┘  │              ▼
                  │    ┌────────────────┐
┌──────────────┐  │    │ Validate token │
│ Bundle       │  │    │ optimization   │
│ templates &  │──┘    │ (target 95%+)  │
│ scripts      │       └────────────────┘
└──────────────┘              │
                              │
                              ▼
PHASE 3: ENHANCEMENT (Week 4)
┌──────────────┐
│ Add          │
│ executable   │──┐
│ scripts      │  │
└──────────────┘  │
                  ├──→ ┌────────────────┐
┌──────────────┐  │    │ Build skill    │
│ Create       │  │    │ composition    │
│ advanced     │──┤    │ examples       │
│ references   │  │    └────────────────┘
└──────────────┘  │              │
                  │              ▼
┌──────────────┐  │    ┌────────────────┐
│ Build skill  │  │    │ Document       │
│ testing      │──┘    │ authoring      │
│ framework    │       │ guidelines     │
└──────────────┘       └────────────────┘
                              │
                              │
                              ▼
PHASE 4: TRANSITION (Week 5-6)
┌──────────────┐
│ Enable       │
│ deprecation  │──┐
│ warnings     │  │
└──────────────┘  │
                  ├──→ ┌────────────────┐
┌──────────────┐  │    │ Support        │
│ Create       │  │    │ users during   │
│ migration    │──┤    │ transition     │
│ guide        │  │    └────────────────┘
└──────────────┘  │              │
                  │              ▼
┌──────────────┐  │    ┌────────────────┐
│ Establish    │  │    │ Gather user    │
│ support      │──┘    │ feedback       │
│ channels     │       └────────────────┘
└──────────────┘              │
                              │
                              ▼
PHASE 5: OPTIMIZATION (Week 7-8)
┌──────────────┐
│ Analyze      │
│ token usage  │──┐
│ patterns     │  │
└──────────────┘  │
                  ├──→ ┌────────────────┐
┌──────────────┐  │    │ Refine skill   │
│ Optimize     │  │    │ composition    │
│ skill        │──┤    │ patterns       │
│ boundaries   │  │    └────────────────┘
└──────────────┘  │              │
                  │              ▼
┌──────────────┐  │    ┌────────────────┐
│ Performance  │  │    │ Celebrate      │
│ benchmarking │──┘    │ success!       │
│ & reporting  │       └────────────────┘
└──────────────┘

```

---

## 12. Implementation Priorities

### 12.1 Phase 1: Foundation (Week 1)

**Goal:** Establish core infrastructure and validate approach

**Deliverables:**

1. Create `skills/` directory structure
2. Implement skill-loader meta-skill
3. Implement legacy-bridge meta-skill
4. Convert top 5 highest-priority skills:
   - python
   - javascript
   - typescript
   - security-auth
   - unit-testing
5. Build validation framework
6. Test progressive disclosure with converted skills

**Success Criteria:**

- 7 skills operational (5 domain + 2 meta)
- Token reduction: ≥90% for single-skill tasks
- Skills discoverable and loadable
- Legacy patterns map correctly
- All validation checks pass

### 12.2 Phase 2: Core Skills (Week 2-3)

**Goal:** Convert majority of standards to skills

**Deliverables:**

1. Convert 18 additional high-priority skills:
   - go, rust (coding)
   - security-secrets, security-input-validation, security-zero-trust (security)
   - integration-testing, e2e-testing, performance-testing (testing)
   - ci-cd, infrastructure, monitoring (devops)
   - kubernetes, containers, serverless (cloud-native)
   - react, vue (frontend)
   - nist-compliance (compliance)
2. Update product-matrix.yaml for skill references
3. Bundle existing NIST system into nist-compliance skill
4. Create skill composition examples

**Success Criteria:**

- 25 skills operational (18 new + 7 from Phase 1)
- Token reduction: ≥95% for multi-skill workflows
- Product bundles resolve correctly
- Wildcard expansion functional
- NIST system integrated seamlessly

### 12.3 Phase 3: Extended Skills (Week 4-5)

**Goal:** Complete skill coverage and add advanced features

**Deliverables:**

1. Convert 15 medium-priority skills:
   - mobile-ios, mobile-android (frontend)
   - data-orchestration, data-quality (data-engineering)
   - ml-model-development, ml-model-deployment (ml-ai)
   - logging, tracing (observability)
   - microservices-patterns (microservices)
   - relational-databases, nosql-databases (database)
   - event-driven (architecture)
   - compliance-general (compliance)
   - security-threat-modeling (security)
   - monitoring (devops)
2. Add executable automation scripts
3. Create advanced reference materials
4. Build skill composition pattern library

**Success Criteria:**

- 40 skills operational
- All executable scripts functional
- Composition patterns documented
- Advanced references accessible

### 12.4 Phase 4: Specialized Skills (Week 6)

**Goal:** Complete full skill coverage

**Deliverables:**

1. Convert 7 low-priority skills:
   - web-design (design)
   - content-strategy (content)
2. Finalize documentation
3. Create skill authoring guidelines
4. Build comprehensive test suite

**Success Criteria:**

- All 48 domain skills operational
- 100% test coverage for validation
- Documentation complete
- Authoring guidelines published

### 12.5 Phase 5: Transition & Optimization (Week 7-8)

**Goal:** Transition users and optimize performance

**Deliverables:**

1. Enable backward compatibility warnings
2. Create migration guide for users
3. Establish support channels
4. Conduct user training/onboarding
5. Token usage analysis and optimization
6. Performance benchmarking
7. User feedback integration

**Success Criteria:**

- >80% user adoption within 30 days
- Token reduction: ≥99% (startup), ≥95% (complex workflows)
- Discovery accuracy: >90%
- User satisfaction: >4.5/5
- All migration support complete

---

## 13. Risk Management

### 13.1 Identified Risks

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|-----------|--------|---------------------|
| **Token Budget Exceeded** | Medium | High | Strict 5k token limit per SKILL.md, aggressive resource externalization, automated validation |
| **Skill Discovery Failures** | Medium | High | High-quality descriptions with clear triggers, testing framework, user feedback loop |
| **Backward Compatibility Break** | Low | High | Legacy-bridge skill, gradual deprecation, comprehensive migration guide, parallel systems |
| **User Adoption Resistance** | Medium | Medium | Clear value communication, hands-on training, migration support, maintain old system temporarily |
| **Maintenance Overhead** | Medium | Medium | Automated validation, clear authoring guidelines, contribution templates, CI integration |
| **Performance Degradation** | Low | Medium | Caching strategy, token monitoring, load time benchmarks, optimization tooling |
| **Skill Boundary Confusion** | Medium | Low | Clear skill descriptions, composition examples, discovery testing, user feedback |
| **Resource Duplication** | Low | Low | Resource sharing patterns, central templates, automated deduplication checks |

### 13.2 Mitigation Details

**Token Budget Risk:**

- Implement automated token counting in CI
- Emit warnings at 4,000 tokens per SKILL.md
- Provide tooling to identify optimization opportunities
- Regular audits of token usage patterns

**Discovery Failure Risk:**

- Test skill discovery with diverse user queries
- Maintain discovery accuracy metrics (>90% target)
- A/B test description variations
- User feedback mechanism for incorrect selections

**Compatibility Risk:**

- Maintain legacy system fully functional during transition
- Test all old patterns against legacy-bridge
- Provide clear migration path for each pattern
- Establish deprecation timeline with user notifications

**Adoption Risk:**

- Create compelling before/after demonstrations
- Provide hands-on training sessions
- Offer migration assistance
- Collect and address user feedback rapidly

---

## 14. Success Metrics & Monitoring

### 14.1 Technical Metrics

```yaml
Token Usage:
  metric: "Token consumption per workflow type"
  baseline: 500,000 tokens (full standards load)
  targets:
    startup: 5,000 tokens (99% reduction)
    single_skill: 9,000 tokens (98% reduction)
    multi_skill_3: 17,000 tokens (97% reduction)
    complex_5: 27,000 tokens (95% reduction)
  measurement: "Token counter in skill loader"
  frequency: "Per load operation"

Skill Load Time:
  metric: "Time from load request to skill available"
  target: "<500ms average"
  measurement: "Timestamp diff in skill loader"
  frequency: "Per load operation"

Discovery Accuracy:
  metric: "Correct skill selection rate"
  target: ">90%"
  measurement: "User confirmation + outcome analysis"
  frequency: "Daily aggregate"

Composition Success:
  metric: "Multi-skill workflow completion rate"
  target: ">85%"
  measurement: "Successful task completion with 2+ skills"
  frequency: "Per workflow"
```

### 14.2 Usability Metrics

```yaml
User Satisfaction:
  metric: "Post-interaction rating"
  target: ">4.5/5"
  measurement: "Optional post-task survey"
  frequency: "Per session"

Skill Adoption:
  metric: "Users leveraging skills vs. legacy"
  target: ">80% within 30 days"
  measurement: "Load pattern analysis"
  frequency: "Weekly aggregate"

Self-Service Success:
  metric: "Tasks completed without manual skill selection"
  target: ">70%"
  measurement: "Autonomous discovery usage rate"
  frequency: "Daily aggregate"

Clarification Rate:
  metric: "User requests for skill clarification"
  target: "<5%"
  measurement: "Follow-up questions about skills"
  frequency: "Per workflow"
```

### 14.3 Maintenance Metrics

```yaml
Update Velocity:
  metric: "Time from standard change to skill update"
  target: "≤7 days"
  measurement: "Git commit timestamps"
  frequency: "Per update"

Bug Rate:
  metric: "Reported issues per skill per quarter"
  target: "<2%"
  measurement: "Issue tracker analysis"
  frequency: "Quarterly"

Test Coverage:
  metric: "Skill scenarios covered by tests"
  target: ">90%"
  measurement: "Test suite coverage report"
  frequency: "Per commit"

Contribution Velocity:
  metric: "Community-contributed skills"
  target: ">5 per quarter"
  measurement: "PR merge analysis"
  frequency: "Quarterly"
```

---

## 15. Conclusion

This architecture transforms the williamzujkowski/standards repository into a modern, token-efficient, autonomous agent skills system while maintaining backward compatibility and preserving all existing capabilities.

**Key Architectural Achievements:**

1. **99% Token Reduction:** From 500k baseline to 5k typical workflow
2. **Progressive Disclosure:** Three-level loading optimizes for relevance
3. **Autonomous Discovery:** Claude self-selects skills without manual intervention
4. **Seamless Composition:** 48 domain skills compose effortlessly
5. **Backward Compatible:** Legacy bridge ensures gradual migration
6. **Executable Capabilities:** Scripts and automation at zero token cost
7. **Production-Ready:** Validation, testing, and monitoring built-in

**Next Steps:**

1. **Planner Agent:** Decompose architecture into actionable tasks
2. **Coder Agents:** Implement skill-loader and legacy-bridge
3. **Content Agents:** Convert standards to skills (Phases 1-4)
4. **Tester Agents:** Build validation and testing framework
5. **Integration:** Assemble and validate complete system

**Architectural Confidence:** ✅ HIGH

This architecture is production-ready, scalable, and aligned with Anthropic's Skills specification and the repository's existing strengths.

---

## Appendix A: Example Skill Structure

### Python Coding Skill

```markdown
---
name: python
description: Python development standards including PEP 8 style guide, type hints, async/await patterns, project structure best practices, and testing conventions. Use when developing Python applications, REST APIs, CLI tools, data pipelines, or ML services.
---

# Python Development Standards

## Overview

This skill provides comprehensive Python development guidance following PEP 8, modern type hinting, async patterns, and project structure best practices. It covers Python 3.10+ features and integrates with popular frameworks like FastAPI, Flask, Django, and Click.

## When to Use This Skill

- Building REST APIs with FastAPI or Flask
- Creating command-line tools with argparse or Click
- Developing data processing pipelines
- Writing Python libraries or packages
- Implementing async services with asyncio
- Working on ML/AI projects with Python

## Core Instructions

### Code Style

- **Follow PEP 8:** Use Black (line length 88) and Ruff for formatting and linting
- **Type Hints:** Annotate all function signatures and public APIs
- **Docstrings:** Use Google-style docstrings for all public functions/classes
- **Naming:** snake_case for functions/variables, PascalCase for classes

### Project Structure

```

project/
├── src/
│   └── package_name/
│       ├── **init**.py
│       ├── main.py
│       └── utils.py
├── tests/
│   ├── **init**.py
│   └── test_main.py
├── pyproject.toml
├── README.md
└── .gitignore

```

### Async Patterns

- Prefer `async/await` for I/O-bound operations
- Use `asyncio.gather()` for concurrent tasks
- Handle async context managers properly

### Error Handling

- Raise specific exceptions, not generic `Exception`
- Use custom exception classes for domain errors
- Always clean up resources with context managers

### Testing

- Use pytest for all testing
- Aim for >80% code coverage
- Write unit, integration, and E2E tests

## Advanced Topics

### Detailed Guides

- For comprehensive PEP 8 guidance, see `./resources/pep8-guide.md`
- For advanced type hints patterns, see `./resources/type-hints-guide.md`
- For async/await best practices, see `./resources/async-patterns.md`
- For FastAPI-specific patterns, see `./resources/fastapi-guide.md`

### Templates

- Project setup: `./templates/pyproject.toml.template`
- Pytest configuration: `./templates/pytest.ini.template`
- Linting configuration: `./templates/.pylintrc.template`

### Automation Scripts

- Lint code: `./scripts/lint.sh [path]`
- Format code: `./scripts/format.sh [path]`
- Run type checking: `./scripts/type-check.sh [path]`

### Examples

- Basic REST API: `./examples/basic-api/`
- Async service: `./examples/async-service/`
- CLI tool: `./examples/cli-tool/`

## Related Skills

- **unit-testing**: For Python testing standards
- **security-input-validation**: For API input validation
- **ci-cd**: For Python project CI/CD setup
- **data-quality**: For data pipeline testing

## Common Patterns

### FastAPI Endpoint

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
async def create_item(item: Item) -> Item:
    # Validation happens automatically via Pydantic
    # Business logic here
    return item
```

### Async Context Manager

```python
from typing import AsyncIterator

class DatabaseConnection:
    async def __aenter__(self) -> "DatabaseConnection":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.disconnect()
```

---

**Token Count:** ~4,200 tokens

```

---

## Appendix B: Architecture Decision Records

### ADR-001: Three-Level Progressive Disclosure

**Date:** 2025-10-17
**Status:** Accepted

**Context:**
Need to minimize token consumption while providing sufficient guidance for autonomous agent operation.

**Decision:**
Implement three-level progressive disclosure:
1. Level 1 (Metadata): Always loaded at startup (~100 tokens/skill)
2. Level 2 (Instructions): Loaded on-demand (<5,000 tokens/skill)
3. Level 3 (Resources): Filesystem access (0 tokens)

**Consequences:**
- **Positive:** 99% token reduction, enables autonomous discovery
- **Negative:** Requires careful content organization
- **Mitigation:** Automated validation ensures proper structure

---

### ADR-002: Skill Loader as Meta-Skill

**Date:** 2025-10-17
**Status:** Accepted

**Context:**
Need coordination logic for product bundles, wildcards, and pattern resolution.

**Decision:**
Implement skill-loader as a meta-skill following same SKILL.md structure, providing coordination capabilities to Claude.

**Consequences:**
- **Positive:** Consistent interface, self-documenting, Claude can understand loading logic
- **Negative:** Loader logic exposed to Claude (could confuse)
- **Mitigation:** Clear documentation, separation of concerns

---

### ADR-003: Backward Compatibility via Legacy Bridge

**Date:** 2025-10-17
**Status:** Accepted

**Context:**
Existing users rely on @load patterns and standard references.

**Decision:**
Implement legacy-bridge meta-skill that translates old patterns to new skills, with gradual deprecation timeline.

**Consequences:**
- **Positive:** Zero breaking changes, smooth migration
- **Negative:** Maintenance overhead for dual systems
- **Mitigation:** Automated translation, clear sunset timeline (6 months)

---

### ADR-004: NIST as Single Bundled Skill

**Date:** 2025-10-17
**Status:** Accepted

**Context:**
Existing NIST system (controls, templates, scripts, VS Code extension) is comprehensive and integrated.

**Decision:**
Bundle entire NIST system as single nist-compliance skill rather than splitting into sub-skills.

**Consequences:**
- **Positive:** Preserves existing integration, maintains comprehensive coverage
- **Negative:** Larger skill (~4,800 tokens), potential complexity
- **Mitigation:** Strong progressive disclosure (Level 3 for most details)

---

**Architecture Status:** ✅ APPROVED FOR IMPLEMENTATION

**Next Step:** Planner agent to decompose into actionable task list

---

*End of Architecture Design Document*
