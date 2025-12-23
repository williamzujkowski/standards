# Skills Quick Start Guide

**Time to Complete**: 5 minutes
**Prerequisites**: None
**Version**: 1.0.0

---

## What Are Skills?

Skills are **modular, bite-sized standards** that load progressively. Instead of reading 50,000+ token documents, you load exactly what you need—in 5 minutes or less.

---

## 3-Step Quick Start

### Step 1: Load Your First Skill (30 seconds)

**Note**: The `@load` directive is planned for v2.0. Current implementation uses the skill-loader script.

**Current (v1.x):**

```bash
python3 scripts/skill-loader.py load skill:coding-standards
```

**Planned (v2.0):**

```bash
@load skill:coding-standards
```

**What you get**:

- ✅ Core principles
- ✅ Quick reference
- ✅ Essential checklist
- ✅ Common pitfalls

**Token cost**: 327 tokens (~5 min read)

### Step 2: Try Product Type Loading (30 seconds)

**Current (v1.x):**

```bash
# For API projects
python3 scripts/skill-loader.py load product:api

# For frontend projects
python3 scripts/skill-loader.py load product:frontend-web

# For mobile apps
python3 scripts/skill-loader.py load product:mobile
```

**Planned (v2.0):**

```bash
# For API projects
@load product:api

# For frontend projects
@load product:frontend-web

# For mobile apps
@load product:mobile
```

**Auto-loads relevant skills** based on your project type.

### Step 3: Get Recommendations (1 minute)

```bash
python3 scripts/skill-loader.py recommend ./

# Output:
# 🔍 Detected: REST API (Python/FastAPI)
# 📚 Recommended: coding-standards, security-practices, testing, nist-compliance
# 💡 Load with (v1.x): python3 scripts/skill-loader.py load product:api
# 💡 Load with (v2.0 - planned): @load product:api
```

---

## Common Use Cases

### Starting a New Project

**Current (v1.x):**

```bash
python3 scripts/skill-loader.py load product:api --language python
# Loads: coding-standards, security-practices, testing, nist-compliance
# Token cost: ~1,755 (Level 1)
```

**Planned (v2.0):**

```bash
@load product:api --language python
```

### Code Review

**Current (v1.x):**

```bash
python3 scripts/skill-loader.py load "skill:coding-standards + skill:testing"
# Quick checklists for review
```

**Planned (v2.0):**

```bash
@load [skill:coding-standards + skill:testing] --level 1
```

### Security Audit

**Current (v1.x):**

```bash
python3 scripts/skill-loader.py load "skill:security-practices + skill:nist-compliance" --level 2
# Comprehensive security coverage
```

**Planned (v2.0):**

```bash
@load [skill:security-practices + skill:nist-compliance] --level 2
```

---

## Progressive Levels

### Level 1: Quick Start (5 min, <2,000 tokens)

**Current (v1.x):**

```bash
python3 scripts/skill-loader.py load skill:testing --level 1
```

**Planned (v2.0):**

```bash
@load skill:testing --level 1
```

**Perfect for**:

- Quick reference
- Onboarding
- Code review checklists

### Level 2: Implementation (30 min, <5,000 tokens)

**Current (v1.x):**

```bash
python3 scripts/skill-loader.py load skill:testing --level 2
```

**Planned (v2.0):**

```bash
@load skill:testing --level 2
```

**Perfect for**:

- Implementing features
- Deep problem-solving
- System design

### Level 3: Mastery (Extended)

**Current (v1.x):**

```bash
python3 scripts/skill-loader.py load skill:testing --level 3
```

**Planned (v2.0):**

```bash
@load skill:testing --level 3
```

**Perfect for**:

- Advanced topics
- Tool selection
- Architecture decisions

---

## Available Skills

| Skill | Use When | Tokens (L1) |
|-------|----------|-------------|
| `coding-standards` | Any project | 327 |
| `security-practices` | APIs, web services | 409 |
| `testing` | Any project with tests | 430 |
| `nist-compliance` | Regulated industries | 580 |
| `skill-loader` | Learning the system | 328 |

**Total (all Level 1)**: ~2,083 tokens

---

## CLI Commands

### Load Skills

```bash
# Single skill
python3 scripts/skill-loader.py load skill:coding-standards

# Multiple skills
python3 scripts/skill-loader.py load "skill:coding-standards + skill:testing"

# Product type
python3 scripts/skill-loader.py load product:api --language python
```

### Get Recommendations

```bash
python3 scripts/skill-loader.py recommend ./
```

### List Skills

```bash
python3 scripts/skill-loader.py list
```

### Validate Skills

```bash
python3 scripts/validate-skills.py skills/
```

---

## Token Efficiency

### Before Skills

```
Full standards: ~150,000 tokens (loading all documents)
Load time: Minutes
Cost: High
```

### After Skills (Level 1)

```
All skills: ~2,083 tokens
Load time: Seconds
Cost: 98% reduction compared to loading all standards documents
```

**Example**: Loading `product:api` with skills uses ~1,755 tokens vs ~150K tokens for all docs (98.8% reduction)

---

## Next Steps

1. **Try it now** (v1.x): `python3 scripts/skill-loader.py load skill:coding-standards --level 1`
2. **Get recommendations**: `python3 scripts/skill-loader.py recommend ./`
3. **Read full guide**: [SKILLS_USER_GUIDE.md](./SKILLS_USER_GUIDE.md)
4. **Explore catalog**: [SKILLS_CATALOG.md](../SKILLS_CATALOG.md)

---

## Need Help?

- **User Guide**: [SKILLS_USER_GUIDE.md](./SKILLS_USER_GUIDE.md)
- **Migration Guide**: [MIGRATION_GUIDE.md](../../archive/old-migrations/migration/MIGRATION_GUIDE.md)
- **API Docs**: [SKILLS_API.md](../api/SKILLS_API.md)
- **GitHub Issues**: [Report issues](https://github.com/williamzujkowski/standards/issues)

---

**That's it!** Start loading skills and experience 98% token reduction (compared to loading all standards documents) with better context. 🚀

---

*Last Updated: 2025-10-16 | Version: 1.0.0*
