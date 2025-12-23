# Skills Format Specification

**Version**: 2.0 (Anthropic-aligned)
**Last Updated**: 2025-10-24 23:00:00 EDT
**Authority**: Based on [Anthropic's canonical skills.md format](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)

## Overview

This document specifies the SKILL.md format used in the standards repository, combining Anthropic's canonical format with value-add extensions for enterprise use cases.

## Compliance Status

- **Anthropic Compliance**: 42/61 skills (68.9%)
- **Required Fields**: 61/61 (100%)
- **Token Budget**: 42/61 (68.9%)

---

## Required Format (Anthropic Spec)

### 1. File Structure

```
skill-name/
├── SKILL.md        (required)
├── FORMS.md        (optional)
├── REFERENCE.md    (optional)
└── scripts/        (optional)
```

### 2. YAML Frontmatter

**Required fields:**

```yaml
---
name: skill-identifier
description: What the skill does and when Claude should use it
---
```

**Constraints:**

- `name`: Maximum 64 characters, lowercase letters/numbers/hyphens only, no reserved words
- `description`: Non-empty, maximum 1024 characters, no XML tags

### 3. Progressive Disclosure (3 Levels)

**Level 1: Metadata** (~100 tokens)

- YAML frontmatter
- Always loaded at startup
- Should be concise and informative

**Level 2: Instructions** (<5,000 tokens recommended)

- Markdown body of SKILL.md
- Loaded when skill is triggered
- Procedural knowledge: workflows, best practices, guidance

**Level 3: Resources** (variable size)

- Separate files (FORMS.md, REFERENCE.md, scripts)
- Loaded only when explicitly referenced
- Templates, schemas, detailed references

---

## Value-Add Extensions (Standards Repository)

### Optional Metadata Fields

```yaml
---
# Required (Anthropic)
name: skill-identifier
description: Purpose and usage

# Optional (Standards Repository Extensions)
category: coding-standards | security | testing | cloud-native | ...
difficulty: beginner | intermediate | advanced
nist_controls: ["AC-2", "SC-7", ...]
related_skills: ["other-skill-1", "other-skill-2"]
prerequisites: ["prereq-skill-1"]
estimated_time: "2-4 hours"
last_updated: "2025-10-24"
token_cost:
  level_1: "~400"
  level_2: "~2000"
  level_3: "0 (filesystem)"
---
```

### Extended Body Structure

```markdown
# Skill Name

## Level 1: Quick Start (<2,000 tokens, 5 minutes)

**Core Principles**: Key concepts

**Quick Reference**: Minimal example

**Essential Checklist**: Must-haves

## Level 2: Implementation (<5,000 tokens, 30 minutes)

**Step-by-Step Guide**: Detailed implementation

**Common Patterns**: Examples

**Common Pitfalls**: What to avoid

**Verification**: How to test

## Level 3: Mastery (Resources)

Links to FORMS.md, REFERENCE.md, scripts/, external docs
```

---

## Validation

### Automated Validation

```bash
# Check Anthropic compliance
python3 scripts/validate-anthropic-compliance.py

# Verify token counts
python3 scripts/token-counter.py skills/your-skill/SKILL.md

# Run full validation suite
python3 scripts/validate-claims.py
```

### Manual Review Checklist

- [ ] YAML frontmatter has `name` and `description`
- [ ] Name is <64 chars, lowercase/hyphens only
- [ ] Description is <1024 chars, explains purpose and usage
- [ ] Level 2 is <5,000 tokens (use token-counter.py)
- [ ] Examples are working and tested
- [ ] Links are valid (no broken references)
- [ ] NIST controls are accurate (if applicable)

---

## Known Deviations

### Token Budget Overages

**19 skills exceed 5,000 token recommendation:**

These are comprehensive reference skills (security, cloud-native, ML/AI) where completeness is prioritized over token budget.

**Rationale**: Security and compliance skills require comprehensive coverage. Users benefit from having complete information in one place rather than navigating multiple files.

**Mitigation**: Progressive disclosure still reduces initial load. Users can skim Level 1 to decide if they need the full skill.

---

## Best Practices

1. **Start with name/description**: Ensure Anthropic compliance first
2. **Write Level 1 first**: Forces clarity and conciseness
3. **Use token budget as guide**: Aim for <5K, but don't sacrifice clarity
4. **Test examples**: All code examples should be verified
5. **Link to resources**: Move verbose content to Level 3
6. **Update timestamps**: Track when skills were last reviewed
7. **Tag NIST controls**: Enables compliance traceability

---

## References

- [Anthropic Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Repository Skills Catalog](../SKILLS_CATALOG.md)
- [Skills User Guide](./SKILLS_USER_GUIDE.md)
- [Skills Authoring Guide](./SKILL_AUTHORING_GUIDE.md)
- [CLAUDE.md Anthropic Alignment Section](../../CLAUDE.md#-anthropic-skillsmd-alignment)

---

**Generated**: 2025-10-24 23:00:00 EDT
**Status**: Authoritative specification for standards repository
**Compliance**: Anthropic-aligned with enterprise extensions
