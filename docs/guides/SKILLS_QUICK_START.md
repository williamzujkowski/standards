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

```bash
@load skill:coding-standards
```

**What you get**:
- ✅ Core principles
- ✅ Quick reference
- ✅ Essential checklist
- ✅ Common pitfalls

**Token cost**: 336 tokens (~5 min read)

### Step 2: Try Product Type Loading (30 seconds)

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
npm run skill-loader -- recommend ./

# Output:
# 🔍 Detected: REST API (Python/FastAPI)
# 📚 Recommended: coding-standards, security-practices, testing, nist-compliance
# 💡 Load with: @load product:api
```

---

## Common Use Cases

### Starting a New Project

```bash
@load product:api --language python
# Loads: coding-standards, security-practices, testing, nist-compliance
# Token cost: ~1,755 (Level 1)
```

### Code Review

```bash
@load [skill:coding-standards + skill:testing] --level 1
# Quick checklists for review
```

### Security Audit

```bash
@load [skill:security-practices + skill:nist-compliance] --level 2
# Comprehensive security coverage
```

---

## Progressive Levels

### Level 1: Quick Start (5 min, <2,000 tokens)

```bash
@load skill:testing --level 1
```

**Perfect for**:
- Quick reference
- Onboarding
- Code review checklists

### Level 2: Implementation (30 min, <5,000 tokens)

```bash
@load skill:testing --level 2
```

**Perfect for**:
- Implementing features
- Deep problem-solving
- System design

### Level 3: Mastery (Extended)

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
| `coding-standards` | Any project | 336 |
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
npm run skill-loader -- load skill:coding-standards

# Multiple skills
npm run skill-loader -- load "skill:coding-standards + skill:testing"

# Product type
npm run skill-loader -- load product:api --language python
```

### Get Recommendations

```bash
npm run skill-loader -- recommend ./
```

### List Skills

```bash
npm run skill-loader -- list
```

### Validate Skills

```bash
python scripts/validate-skills.py skills/
```

---

## Token Efficiency

### Before Skills

```
Full standards: 250,000+ tokens
Load time: Minutes
Cost: High
```

### After Skills (Level 1)

```
All skills: 2,083 tokens
Load time: Seconds
Cost: 99%+ reduction
```

**Example**: Loading `product:api` saves **248,245 tokens** (99.3% reduction)

---

## Next Steps

1. **Try it now**: `@load skill:coding-standards --level 1`
2. **Get recommendations**: `npm run skill-loader -- recommend ./`
3. **Read full guide**: [SKILLS_USER_GUIDE.md](./SKILLS_USER_GUIDE.md)
4. **Explore catalog**: [SKILLS_CATALOG.md](../SKILLS_CATALOG.md)

---

## Need Help?

- **User Guide**: [SKILLS_USER_GUIDE.md](./SKILLS_USER_GUIDE.md)
- **Migration Guide**: [MIGRATION_GUIDE.md](../migration/MIGRATION_GUIDE.md)
- **API Docs**: [SKILLS_API.md](../api/SKILLS_API.md)
- **GitHub Issues**: [Report issues](https://github.com/williamzujkowski/standards/issues)

---

**That's it!** Start loading skills and experience 99%+ token reduction with better context. 🚀

---

*Last Updated: 2025-10-16 | Version: 1.0.0*
