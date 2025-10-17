---
name: legacy-bridge
description: Backward compatibility bridge that translates legacy @load patterns to new Skills format. Enables seamless migration with zero breaking changes during 6-month transition period.
---

# Legacy Bridge Skill

## Overview

The legacy-bridge skill provides backward compatibility for existing `@load` patterns used in CLAUDE.md and the product-matrix system. This bridge enables a zero-breaking-change migration path from the legacy standards loader to the new Skills-based architecture.

**Migration Timeline**: 6-month transition period (deprecation warnings only, no breaking changes)

## When to Use This Skill

Use this skill when:

- You have existing code using `@load product:*` patterns
- You need to maintain backward compatibility during migration
- You want to gradually transition to the new Skills format
- You're supporting both old and new loading patterns simultaneously

## Core Instructions

### Pattern Translation

The legacy-bridge automatically translates old `@load` patterns to new skill loads:

#### Product Type Patterns

```bash
# Old Pattern → New Skill Loading
@load product:api              → Load: [coding-standards, testing, security, devops]
@load product:web-service      → Load: [coding-standards, testing, security, frontend, devops]
@load product:frontend-web     → Load: [frontend, testing, security]
@load product:mobile           → Load: [frontend/mobile, testing, security]
@load product:data-pipeline    → Load: [data-engineering, testing, security, compliance]
@load product:ml-service       → Load: [ml-ai, data-engineering, testing, security]
```

#### Standard Code Patterns

```bash
# Coding Standards (CS)
@load CS:python       → Load: skills/coding-standards/python
@load CS:javascript   → Load: skills/coding-standards/javascript
@load CS:typescript   → Load: skills/coding-standards/typescript
@load CS:go           → Load: skills/coding-standards/go
@load CS:java         → Load: skills/coding-standards/java

# Testing Standards (TS)
@load TS:pytest       → Load: skills/testing/pytest
@load TS:jest         → Load: skills/testing/jest
@load TS:vitest       → Load: skills/testing/vitest
@load TS:*            → Load: skills/testing/* (all testing skills)

# Security Standards (SEC)
@load SEC:auth                → Load: skills/security/authentication
@load SEC:secrets             → Load: skills/security/secrets-management
@load SEC:input-validation    → Load: skills/security/input-validation
@load SEC:*                   → Load: skills/security/* + NIST-IG:base

# Frontend (FE)
@load FE:react        → Load: skills/frontend/react
@load FE:vue          → Load: skills/frontend/vue
@load FE:angular      → Load: skills/frontend/angular
@load FE:accessibility → Load: skills/frontend/accessibility

# DevOps (DOP)
@load DOP:ci-cd       → Load: skills/devops/ci-cd
@load DOP:iac         → Load: skills/devops/infrastructure-as-code
@load DOP:monitoring  → Load: skills/devops/monitoring

# NIST Compliance (NIST-IG)
@load NIST-IG:base    → Load: skills/nist-compliance/baseline
@load NIST-IG:full    → Load: skills/nist-compliance/full-implementation
```

#### Composite Patterns

```bash
# Multiple standards combined
@load [product:api + CS:python + TS:pytest]
  → Load: product:api skills + python coding + pytest testing

@load [product:frontend-web + FE:react + SEC:*]
  → Load: frontend-web skills + react + all security skills + NIST baseline

@load [CS:python + TS:* + SEC:* + NIST-IG:full]
  → Load: python coding + all testing + all security + full NIST compliance
```

### Wildcard Expansion

The bridge automatically expands wildcards:

```yaml
SEC:*  expands to:
  - SEC:auth
  - SEC:secrets
  - SEC:input-validation
  - SEC:encryption
  - SEC:audit
  - NIST-IG:base  # Auto-included with any security standard

TS:* expands to:
  - TS:unit
  - TS:integration
  - TS:e2e
  - TS:performance
  - TS:security

DOP:* expands to:
  - DOP:ci-cd
  - DOP:iac
  - DOP:monitoring
  - DOP:incident-response

FE:* expands to:
  - FE:design-system
  - FE:accessibility
  - FE:performance
  - FE:responsive
```

### Auto-Inclusion Rules

**NIST Baseline Auto-Loading**:

- Any security standard (`SEC:*`) automatically includes `NIST-IG:base`
- This ensures compliance requirements are never missed
- Explicit override available with `--no-auto-nist` flag

## Migration Guide

### Phase 1: Compatibility Mode (Current)

Both patterns work side-by-side:

```bash
# Legacy pattern (still works)
@load product:api

# New skill pattern (recommended)
skill-loader.py load product:api

# Both produce identical output
```

### Phase 2: Deprecation Warnings (Month 3-6)

```bash
⚠️  DEPRECATION WARNING: @load syntax will be removed in 6 months
    Please migrate to: skill-loader.py load product:api
    See: docs/guides/migration-guide.md
```

### Phase 3: Legacy Removal (Month 6+)

```bash
❌ ERROR: @load syntax removed. Use skill-loader.py instead.
    Migration guide: docs/guides/migration-guide.md
```

## Advanced Topics

### Custom Mapping Files

Create custom legacy mappings for your organization:

```yaml
# config/custom-legacy-mappings.yaml
custom_products:
  internal-api:
    description: "Our internal API standard"
    maps_to:
      - product:api
      - CS:python
      - SEC:auth
      - custom-skill:internal-standards

custom_codes:
  INT:api-gateway:
    description: "Internal API gateway standards"
    maps_to:
      - skills/internal/api-gateway
```

Load custom mappings:

```bash
skill-loader.py load product:internal-api --custom-mappings config/custom-legacy-mappings.yaml
```

### Translation Validation

Verify your legacy patterns translate correctly:

```bash
# Dry-run translation
skill-loader.py translate "@load [product:api + CS:python]" --dry-run

# Output:
# Translation Preview:
# - Load product:api → [coding-standards, testing, security, devops]
# - Load CS:python   → skills/coding-standards/python
# Total skills: 5 unique skills
```

### Conflict Resolution

When patterns conflict, explicit specifications win:

```bash
# product:api includes generic coding-standards
# CS:python provides specific python standards
@load [product:api + CS:python]

# Resolution: Use CS:python (more specific) over product:api's generic coding
```

## Resources

### Legacy Mapping Files

All translation rules are defined in:

- `resources/legacy-mappings.yaml` - Complete mapping definitions
- `config/product-matrix.yaml` - Original product definitions

### Migration Tools

```bash
# Scan codebase for legacy patterns
skill-loader.py audit-legacy --path .

# Generate migration report
skill-loader.py migration-report --output migration-plan.md

# Auto-migrate files (with backup)
skill-loader.py migrate --path . --backup
```

### Examples

See `examples/legacy-patterns/` for:

- Common legacy pattern usage
- Side-by-side comparisons
- Migration examples

## Related Skills

- [skill-loader](../skill-loader/SKILL.md) - New skill loading mechanism
- [coding-standards](../coding-standards/SKILL.md) - Base coding standards
- [security-practices](../security-practices/SKILL.md) - Security implementations
- [nist-compliance](../nist-compliance/SKILL.md) - Compliance requirements

## Bundled Resources

- [Legacy Mappings YAML](./resources/legacy-mappings.yaml)
- [Product Matrix Reference](../../config/product-matrix.yaml)
- [Migration Scripts](./scripts/)
- [Example Translations](./examples/)
