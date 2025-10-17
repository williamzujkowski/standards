# Skills User Guide

**Version**: 1.0.0
**Target Audience**: Developers, Tech Leads, Architects
**Reading Time**: 15 minutes
**Last Updated**: 2025-10-16

---

## Table of Contents

1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [Core Concepts](#core-concepts)
4. [Loading Skills](#loading-skills)
5. [Progressive Disclosure](#progressive-disclosure)
6. [Product Type Loading](#product-type-loading)
7. [Skill Composition](#skill-composition)
8. [Context-Aware Recommendations](#context-aware-recommendations)
9. [Advanced Usage](#advanced-usage)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)

---

## Introduction

### What Are Skills?

Skills are **modular, self-contained standards** that use **progressive disclosure** to deliver the right information at the right time. Instead of loading massive documents, you load exactly what you need—when you need it.

### Why Skills?

**Traditional Standards:**

```bash
UNIFIED_STANDARDS.md → 50,000+ tokens
Load everything or nothing
Manual navigation
Static content
```

**Skills Format:**

```bash
@load skill:coding-standards → 336 tokens (Level 1)
Progressive disclosure (3 levels)
Auto-recommendations
Dynamic composition
```

### Key Benefits

- **98% token reduction**: Load only what you need (~2K vs ~150K tokens for all standards documents)
- **5-minute quick starts**: Get productive fast (Level 1)
- **Auto-recommendations**: System suggests relevant skills
- **Composable**: Combine multiple skills seamlessly
- **Progressive learning**: Level 1 → 2 → 3 as you grow

---

## Quick Start

### Your First Skill Load (2 minutes)

```bash
# Load a single skill at Level 1 (Quick Start)
@load skill:coding-standards

# What you get:
# ✅ Core principles
# ✅ Quick reference
# ✅ Essential checklist
# ✅ Common pitfalls

# Token cost: ~336 tokens
# Reading time: ~5 minutes
```

### Try It Now

**Python API Developer:**

```bash
@load product:api --language python
# Auto-loads: coding-standards, security-practices, testing, nist-compliance
# Total: ~1,755 tokens (Level 1)
```

**React Frontend Developer:**

```bash
@load product:frontend-web --framework react
# Auto-loads: coding-standards, security-practices, testing
# Total: ~1,175 tokens (Level 1)
```

**See the difference immediately!**

---

## Core Concepts

### 1. Progressive Disclosure

Skills have **3 levels** of content:

```
┌─────────────────────────────────┐
│ Level 1: Quick Start (5 min)   │ ← Start here
│ - Core principles               │
│ - Quick reference               │
│ - Essential checklist           │
│ Token budget: <2,000            │
├─────────────────────────────────┤
│ Level 2: Implementation (30min)│ ← When implementing
│ - Detailed patterns             │
│ - Code examples                 │
│ - Integration points            │
│ Token budget: <5,000            │
├─────────────────────────────────┤
│ Level 3: Mastery (Extended)    │ ← Deep dive
│ - Advanced topics               │
│ - Resources & tools             │
│ - Templates & scripts           │
│ Token budget: Flexible          │
└─────────────────────────────────┘
```

**Load what you need, when you need it.**

### 2. Skill Anatomy

Each skill is a directory with:

```
skills/coding-standards/
├── SKILL.md              # Progressive content (Level 1, 2, 3)
├── templates/            # Implementation templates
├── scripts/              # Automation tools
└── resources/            # Additional references
```

### 3. Skill Metadata

Every `SKILL.md` starts with YAML frontmatter:

```yaml
---
name: coding-standards
description: Comprehensive coding standards and best practices for maintainable, consistent software development across multiple languages and paradigms
---
```

**Metadata powers:**

- Auto-discovery
- Context-aware recommendations
- Cross-skill references
- Catalog generation

### 4. Bundled Resources

Skills include bundled resources that load on-demand:

```markdown
## Bundled Resources
- [Full CODING_STANDARDS.md](../../docs/standards/CODING_STANDARDS.md)
- Example linter configs in `./resources/`
- Pre-commit hook templates in `./templates/`
- Complexity checking scripts in `./scripts/`
```

**No token cost** until you explicitly load them.

---

## Loading Skills

### Basic Loading

#### Load Single Skill

```bash
# Load Level 1 (default)
@load skill:coding-standards

# Specify level explicitly
@load skill:coding-standards --level 1
@load skill:coding-standards --level 2
@load skill:coding-standards --level 3
```

#### Load Multiple Skills

```bash
# Load multiple skills (all Level 1)
@load [skill:coding-standards + skill:testing + skill:security-practices]

# With specific levels
@load [
  skill:coding-standards --level 2 +
  skill:testing --level 1 +
  skill:security-practices --level 2
]
```

### Wildcard Loading

```bash
# Load all security skills
@load skill:security-*

# Expands to:
# - security-practices
# - (future: security-monitoring, security-testing, etc.)

# Load all skills (not recommended for token efficiency)
@load skill:*
```

### Conditional Loading

```bash
# Load based on file type
@load skill:coding-standards if file.endsWith('.py')

# Load based on project structure
@load skill:nist-compliance if exists('compliance/')
```

---

## Progressive Disclosure

### Level 1: Quick Start (5 minutes)

**When to use:**

- Starting a new task
- Quick reference during development
- Onboarding new team members
- Code review checklists

**What you get:**

- Core principles
- Quick reference guide
- Essential checklist
- Common pitfalls to avoid

**Example: Level 1 Loading**

```bash
@load skill:testing --level 1

# Output includes:
# - Testing Pyramid
# - TDD Red-Green-Refactor cycle
# - Essential checklist (Unit tests, Integration tests, Coverage >80%)
# - Common pitfalls (Testing implementation details, Slow tests, Flaky tests)

# Token cost: ~430 tokens
# Reading time: ~5 minutes
```

### Level 2: Implementation (30 minutes)

**When to use:**

- Implementing a new feature
- Designing system architecture
- Setting up project infrastructure
- Deep problem-solving

**What you get:**

- Detailed implementation patterns
- Complete code examples
- Integration points with other skills
- Automation tools and scripts

**Example: Level 2 Loading**

```bash
@load skill:testing --level 2

# Additional content:
# - Test-Driven Development (detailed walkthrough)
# - Property-based testing with fast-check
# - Integration testing patterns
# - Security testing examples
# - Performance testing benchmarks
# - Test organization (AAA pattern)

# Token cost: ~2,225 tokens
# Reading time: ~30 minutes
```

### Level 3: Mastery (Extended)

**When to use:**

- Mastering a technology
- Architectural decisions
- Advanced optimizations
- Building internal tools

**What you get:**

- Advanced topics and patterns
- Comprehensive resources
- External references
- Tools and frameworks
- Templates and scripts

**Example: Level 3 Loading**

```bash
@load skill:testing --level 3

# Extended content:
# - Contract testing with Pact
# - Chaos engineering patterns
# - Visual regression testing
# - Mutation testing
# - Essential reading list
# - Framework comparisons
# - Template test suites

# Token cost: ~1,106 tokens
# Reading time: Extended (2+ hours)
```

---

## Product Type Loading

### What Are Product Types?

Product types are **predefined bundles** of skills for common project types. They automatically load relevant skills based on your project's purpose.

### Available Product Types

| Product Type | Description | Auto-Loaded Skills |
|--------------|-------------|-------------------|
| `product:api` | REST/GraphQL API | coding-standards, security-practices, testing, nist-compliance |
| `product:frontend-web` | React/Vue/Angular SPA | coding-standards, security-practices, testing |
| `product:mobile` | iOS/Android app | coding-standards, security-practices, testing |
| `product:data-pipeline` | ETL/ELT workflow | coding-standards, security-practices, data-engineering |
| `product:ml-service` | ML training/inference | coding-standards, security-practices, testing, ml-ai |
| `product:cli` | Command-line tool | coding-standards, testing |
| `product:infra-module` | Infrastructure as Code | coding-standards, security-practices, cloud-native |

### Usage Examples

#### Example 1: API Development

```bash
@load product:api

# Auto-resolves to:
# - coding-standards (language-specific patterns)
# - security-practices (API authentication, input validation)
# - testing (unit, integration, security tests)
# - nist-compliance (AC, IA, AU controls)

# Token cost: ~1,755 tokens (Level 1)
```

#### Example 2: Frontend Web App

```bash
@load product:frontend-web --framework react

# Auto-resolves to:
# - coding-standards (TypeScript/React patterns)
# - security-practices (XSS, CSRF protection)
# - testing (React Testing Library patterns)

# Token cost: ~1,175 tokens (Level 1)
```

#### Example 3: Data Pipeline

```bash
@load product:data-pipeline --language python

# Auto-resolves to:
# - coding-standards (Python patterns)
# - security-practices (data classification, secrets)
# - data-engineering (orchestration, data quality)
# - nist-compliance (data retention, privacy)

# Token cost: ~1,950 tokens (Level 1)
```

### Language & Framework Overrides

```bash
# Specify language
@load product:api --language python
# Uses Python-specific coding standards

# Specify framework
@load product:frontend-web --framework vue
# Uses Vue-specific patterns

# Combine both
@load product:api --language python --framework fastapi
# Uses Python + FastAPI best practices
```

### Custom Product Types

Define your own in `config/product-matrix.yaml`:

```yaml
products:
  my-custom-stack:
    description: "Custom microservice stack"
    standards:
      - CS:typescript
      - TS:jest
      - SEC:auth
      - SEC:secrets
      - DOP:k8s
      - OBS:datadog
```

Then use:

```bash
@load product:my-custom-stack
```

---

## Skill Composition

### Composing Multiple Skills

Skills are designed to work together:

```bash
# Basic composition
@load [skill:coding-standards + skill:testing]

# With different levels
@load [
  skill:coding-standards --level 2 +
  skill:security-practices --level 2 +
  skill:testing --level 1
]

# Composition with product type
@load [product:api + skill:data-engineering]
# Adds data-engineering to standard API skills
```

### Cross-Skill References

Skills automatically reference related skills:

```markdown
## Integration Points
- Reference related skills for secure coding
- Reference related skills for testable code design
- Reference related skills for compliance controls
```

**Navigation is automatic** when skills are composed together.

### Composition Strategies

#### Strategy 1: Foundation First

```bash
# Load foundational skills at Level 2
@load [
  skill:coding-standards --level 2 +
  skill:testing --level 2
]

# Then add specialized skills at Level 1
@load [skill:nist-compliance --level 1]
```

#### Strategy 2: Project-Specific Bundle

```bash
# Create project-specific bundle
@load [
  product:api +
  skill:data-engineering +
  skill:cloud-native
] --output .claude/project-skills.md

# Load bundle in future sessions
@load .claude/project-skills.md
```

#### Strategy 3: Role-Based Loading

```bash
# Backend developer
@load [skill:coding-standards + skill:security-practices + skill:testing] --level 2

# Frontend developer
@load [skill:coding-standards + skill:security-practices] --level 2 + skill:web-design --level 1

# DevOps engineer
@load [skill:cloud-native + skill:security-practices + skill:devops] --level 2
```

---

## Context-Aware Recommendations

### Auto-Recommendation

Let the system analyze your project and recommend skills:

```bash
# Analyze current project
python3 scripts/skill-loader.py recommend ./

# Output:
# 🔍 Analyzing project...
# 📂 Detected: REST API (Python/FastAPI)
#
# 📚 Recommended Skills:
#   - coding-standards (priority: high)
#     Reason: Python files detected
#
#   - security-practices (priority: critical)
#     Reason: API endpoints detected - security essential
#
#   - testing (priority: high)
#     Reason: Test files present
#
#   - nist-compliance (priority: medium)
#     Reason: Security requirements likely
#
# 💡 Suggested load command:
#   @load [skill:coding-standards + skill:security-practices + skill:testing + skill:nist-compliance]
```

### Recommendation Factors

The system considers:

- **File types**: `.py`, `.js`, `.go`, etc.
- **Directory structure**: `/tests/`, `/api/`, `/src/`
- **Dependencies**: `package.json`, `requirements.txt`, `go.mod`
- **Existing standards references**: NIST tags, security annotations
- **Framework detection**: FastAPI, React, Django, etc.

### Smart Loading

```bash
# Load recommendations automatically
python3 scripts/skill-loader.py auto-load ./

# Confirmation prompt:
# Load all recommended skills at Level 1? [Y/n] y
#
# Loading skills...
# ✓ coding-standards (327 tokens)
# ✓ security-practices (409 tokens)
# ✓ testing (430 tokens)
# ✓ nist-compliance (580 tokens)
#
# Total: 1,746 tokens (~0.4% of context window)
# Saved to: .claude/auto-loaded-skills.md
```

---

## Advanced Usage

### Skill Caching

```bash
# Cache frequently used skills
python3 scripts/skill-loader.py cache skill:coding-standards --level 2

# Load from cache (instant)
@load skill:coding-standards --from-cache
```

### Skill Versions

```bash
# Load specific version
@load skill:coding-standards@1.0.0

# Load latest (default)
@load skill:coding-standards@latest
```

### Custom Skill Paths

```bash
# Load from custom directory
@load skill:my-custom-skill --from ./my-skills/

# Load from URL (future feature)
@load skill:community-skill --from https://skills-repo.com/
```

### Skill Export

```bash
# Export composed skills to file
python3 scripts/skill-loader.py compose \
  skill:coding-standards \
  skill:security-practices \
  --level 1 \
  --output my-skills-bundle.md

# Share with team
git add my-skills-bundle.md
git commit -m "Add team skills bundle"
```

### Integration with CI/CD

```yaml
# .github/workflows/validate.yml
name: Validate Standards Compliance

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Load Skills
        run: |
          python3 scripts/skill-loader.py load product:api --level 1 --output .claude/skills.md

      - name: Validate Compliance
        run: |
          python3 scripts/validate-nist-tags.py
          python3 scripts/validate-skills.py skills/

      - name: Upload Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: skills-validation
          path: .claude/skills.md
```

---

## Best Practices

### 1. Start with Level 1

```bash
# ✅ Good: Start with Quick Start
@load skill:coding-standards --level 1
# Read and understand fundamentals first

# ❌ Bad: Load everything immediately
@load skill:coding-standards --level 3
# Overwhelming amount of content
```

### 2. Use Product Types

```bash
# ✅ Good: Use product type for automatic selection
@load product:api

# ❌ Bad: Manually select all skills
@load [skill:coding-standards + skill:security-practices + skill:testing + skill:nist-compliance]
```

### 3. Progressive Deep Dive

```bash
# Day 1: Quick Start
@load skill:testing --level 1

# Week 1: Implementation
@load skill:testing --level 2

# Month 1: Mastery
@load skill:testing --level 3
```

### 4. Compose Related Skills

```bash
# ✅ Good: Load related skills together
@load [skill:coding-standards + skill:testing]
# Better context, integrated examples

# ❌ Bad: Load unrelated skills
@load [skill:coding-standards + skill:devops + skill:ml-ai]
# Unrelated, confusing context
```

### 5. Cache Common Bundles

```bash
# Create team bundle
python3 scripts/skill-loader.py compose \
  product:api \
  --level 1 \
  --output .claude/team-bundle.md

# Team members load instantly
@load .claude/team-bundle.md
```

### 6. Use Auto-Recommendations

```bash
# Let the system guide you
python3 scripts/skill-loader.py recommend ./

# More accurate than manual selection
```

---

## Troubleshooting

### Issue: Skill Not Found

```bash
Error: Skill not found: skill:my-skill

# Solution 1: Check spelling
@load skill:coding-standards  # Correct spelling

# Solution 2: List available skills
python3 scripts/skill-loader.py list

# Solution 3: Check path
ls skills/
```

### Issue: High Token Usage

```bash
Warning: Total tokens: 12,000 (>10,000 recommended)

# Solution: Use Level 1 instead of Level 2
@load skill:coding-standards --level 1  # 336 tokens
# Instead of:
@load skill:coding-standards --level 2  # 1,245 tokens

# Or: Load only needed skills
@load skill:coding-standards  # Instead of @load skill:*
```

### Issue: Missing Cross-References

```bash
Error: Cross-reference not found: ../security-practices/SKILL.md

# Solution: Load related skills together
@load [skill:coding-standards + skill:security-practices]

# Or: Check skill exists
python scripts/validate-skills.py skills/ --check-refs
```

### Issue: Validation Warnings

```bash
Warning: Level 1 section too large (2,500 tokens, recommended <2,000)

# This is informational - skill still works
# But consider:
# 1. Moving content to Level 2
# 2. Simplifying Quick Start
# 3. Using bundled resources
```

### Issue: Auto-Recommendation Not Working

```bash
⚠️ No project detected

# Solution: Ensure you're in project root
cd /path/to/project
python3 scripts/skill-loader.py recommend ./

# Or: Specify project type manually
@load product:api --language python
```

---

## Next Steps

### Learn More

- **Migration Guide**: [MIGRATION_GUIDE.md](../migration/MIGRATION_GUIDE.md)
- **Authoring Guide**: [SKILL_AUTHORING_GUIDE.md](./SKILL_AUTHORING_GUIDE.md)
- **API Documentation**: [SKILLS_API.md](../api/SKILLS_API.md)
- **Skills Catalog**: [SKILLS_CATALOG.md](../SKILLS_CATALOG.md)

### Try It Out

```bash
# 1. Load a skill
@load skill:coding-standards --level 1

# 2. Try product type loading
@load product:api

# 3. Get recommendations
python3 scripts/skill-loader.py recommend ./

# 4. Compose a custom bundle
python3 scripts/skill-loader.py compose skill:coding-standards skill:testing --output my-bundle.md
```

### Get Help

- **GitHub Issues**: [Report issues](https://github.com/williamzujkowski/standards/issues)
- **Discussions**: [Ask questions](https://github.com/williamzujkowski/standards/discussions)
- **Documentation**: [Full docs](https://williamzujkowski.github.io/standards/)

---

**Happy Skill Loading!** 🚀

Skills make standards more accessible, efficient, and powerful. Start small, grow progressively, and enjoy the benefits of context-aware development.

---

*Last Updated: 2025-10-16*
*Version: 1.0.0*
*Maintained by: Standards Repository Team*
