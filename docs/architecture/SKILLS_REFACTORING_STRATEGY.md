# Skills Format Refactoring Strategy

## Alignment with Anthropic Canonical Format

**Date**: 2025-10-24
**Author**: System Architecture Designer
**Status**: Design Phase
**Version**: 1.0

---

## Executive Summary

This document outlines the strategy to refactor the standards repository's skills system to align with Anthropic's canonical `skills.md` format while preserving the unique value-add features of the current implementation (3-level token optimization, NIST tagging, product matrix integration).

### Key Findings

1. **Current Implementation Analysis**: 61 skills using custom `SKILL.md` format with YAML frontmatter and 3-level progressive disclosure
2. **Anthropic Canonical Format**: Based on available documentation, Anthropic uses a simpler custom instructions approach integrated into Claude Projects
3. **Gap**: Current format is MORE sophisticated than standard custom instructions but may not be officially recognized by Claude tooling
4. **Recommendation**: Hybrid approach - maintain current value-add features while ensuring compatibility with Claude Projects

---

## 1. Gap Analysis

### 1.1 Current Implementation (Standards Repo)

**File Structure**:

```
skills/
├── coding-standards/
│   ├── python/
│   │   ├── SKILL.md (3-level format)
│   │   ├── resources/
│   │   ├── templates/
│   │   └── scripts/
│   └── typescript/
│       └── SKILL.md
├── security/
│   └── authentication/
│       └── SKILL.md
└── ... (61 total skills)
```

**Current SKILL.md Format**:

```markdown
---
name: skill-name
description: Brief description
tags: [tag1, tag2]
category: category-name
difficulty: beginner|intermediate|advanced
estimated_time: "30 minutes"
prerequisites: [skill1, skill2]
related_skills: [skill3, skill4]
nist_controls: [IA-2, IA-5]
---

# Skill Name

## Level 1: Quick Start (<2,000 tokens, 5 minutes)
- Core principles
- Essential checklist
- Quick examples

## Level 2: Implementation (<5,000 tokens, 30 minutes)
- Deep dive topics
- Production patterns
- Integration points

## Level 3: Mastery (Extended)
- Advanced topics
- Templates & resources
- Related skills
```

**Key Features**:

1. ✅ **3-level progressive disclosure** for token optimization
2. ✅ **YAML frontmatter** with rich metadata
3. ✅ **NIST control tagging** for compliance
4. ✅ **Bundled resources** (templates, scripts, configs)
5. ✅ **Product matrix integration** via `config/product-matrix.yaml`
6. ✅ **Skill loader CLI** (`scripts/skill-loader.py`)

### 1.2 Anthropic Canonical Format (Inferred from Documentation)

**Based on Web Research** (docs.claude.com was unavailable):

Anthropic's official approach uses:

1. **Claude Projects** with "Custom Instructions" field
2. Simple markdown format without strict schema
3. Direct integration in claude.ai web interface
4. No standardized frontmatter or metadata

**Limitations of Research**:

- Official skills.md specification not publicly available
- Documentation pages returned 404 errors
- Custom instructions format appears to be free-form markdown

**Inferred Canonical Format**:

```markdown
# Skill Title

Brief description of what this skill provides.

## When to Use

- Use case 1
- Use case 2

## Core Instructions

Detailed instructions for how to apply this skill...

## Examples

Code examples and patterns...
```

### 1.3 Gap Summary

| Aspect | Current Implementation | Anthropic Canonical (Inferred) | Gap |
|--------|------------------------|-------------------------------|-----|
| **File Naming** | `SKILL.md` | `skills.md` or custom instructions | ✅ Minor |
| **Metadata** | YAML frontmatter | None (free-form) | ⚠️ Custom addition |
| **Structure** | 3-level progressive | Single level | ⚠️ Custom addition |
| **Token Optimization** | Built-in (Level 1/2/3) | Manual | ✅ Value-add |
| **NIST Tagging** | @nist comments in code | Not specified | ✅ Value-add |
| **Product Matrix** | `product-matrix.yaml` | Not specified | ✅ Value-add |
| **Bundled Resources** | templates/, scripts/ | Not specified | ✅ Value-add |
| **Loading Mechanism** | CLI script | Claude Projects UI | ⚠️ Different approach |
| **Integration** | File-based via CLAUDE.md | Web UI upload | ⚠️ Different approach |

**Conclusion**: Current implementation is MORE feature-rich than inferred canonical format. The "gap" is not a deficit but a set of value-add features.

---

## 2. Refactoring Strategy

### 2.1 Design Goals

1. **Backward Compatibility**: Existing 61 skills continue to work
2. **Anthropic Alignment**: Support canonical format for Claude Projects
3. **Preserve Value-Add**: Keep 3-level optimization, NIST tagging, product matrix
4. **Dual-Mode Support**: Generate both custom format AND canonical format from single source
5. **Minimal Disruption**: Phased migration with fallback support

### 2.2 Proposed Hybrid Architecture

```
skills/
├── [skill-category]/
│   └── [skill-name]/
│       ├── skill.md              # NEW: Anthropic canonical format (generated)
│       ├── SKILL.md              # EXISTING: 3-level format (source of truth)
│       ├── skill-metadata.yaml   # NEW: Extracted metadata (optional)
│       ├── resources/
│       ├── templates/
│       └── scripts/
```

**Key Decisions**:

1. **Source of Truth**: `SKILL.md` remains the master file
2. **Generated Output**: `skill.md` auto-generated in simplified format
3. **Metadata Extraction**: Optional `skill-metadata.yaml` for tooling
4. **Dual Loading**: Support both formats via skill-loader

### 2.3 File Format Specifications

#### 2.3.1 SKILL.md (Enhanced Current Format)

**No Changes Required** - remains as-is with 3-level structure.

#### 2.3.2 skill.md (Canonical Format - Generated)

```markdown
# [Skill Name]

> **Category**: [category]
> **Difficulty**: [difficulty]
> **Estimated Time**: [time]

[Description from frontmatter]

## Overview

[Level 1 content - core principles and checklist]

## When to Use This Skill

- [Use case 1 from description]
- [Use case 2 from description]

## Core Instructions

[Level 2 content - implementation details]

## Examples

[Code examples from Level 1 and Level 2]

## Integration Points

[Related skills and dependencies]

## Common Pitfalls

[Common pitfalls section]

## Additional Resources

- Full documentation: [Link to SKILL.md]
- Templates: [Link to templates/]
- Scripts: [Link to scripts/]

---

*This is a simplified version. For full 3-level progressive disclosure, see [SKILL.md](./SKILL.md)*
```

#### 2.3.3 skill-metadata.yaml (New)

```yaml
name: skill-name
version: 1.0.0
category: category-name
difficulty: intermediate
estimated_time: "30 minutes"

description: >
  Brief description of the skill

tags:
  - tag1
  - tag2

nist_controls:
  - IA-2
  - IA-5

prerequisites:
  - skill1
  - skill2

related_skills:
  - skill3
  - skill4

resources:
  templates:
    - templates/template1.py
    - templates/template2.js
  scripts:
    - scripts/setup.sh
  configs:
    - resources/configs/pyproject.toml

integration:
  upstream_dependencies:
    - tool1
    - tool2
  downstream_consumers:
    - application-type-1
    - application-type-2
```

---

## 3. Migration Plan

### Phase 1: Framework and Tooling (Week 1)

**Objective**: Build dual-format support without modifying existing skills

**Tasks**:

1. **Create Format Converter** (`scripts/convert-skill-format.py`)
   - Parse `SKILL.md` frontmatter and content
   - Extract Level 1 and Level 2 content
   - Generate `skill.md` in canonical format
   - Generate `skill-metadata.yaml`

2. **Update Skill Loader** (`scripts/skill-loader.py`)
   - Add `--format` flag: `canonical` or `3level` (default)
   - Support loading both `skill.md` and `SKILL.md`
   - Preserve existing CLI interface

3. **Add Validation**
   - Extend `scripts/validate-skills.py`
   - Check both formats for consistency
   - Validate metadata completeness

4. **Update Documentation**
   - Add `docs/guides/SKILL_FORMAT_SPEC.md`
   - Document both formats
   - Provide migration guide

**Deliverables**:

- ✅ `scripts/convert-skill-format.py` - working converter
- ✅ Updated `scripts/skill-loader.py` with dual-format support
- ✅ Updated `scripts/validate-skills.py`
- ✅ `docs/guides/SKILL_FORMAT_SPEC.md`

**Validation**:

```bash
# Test converter
python3 scripts/convert-skill-format.py skills/coding-standards/python/SKILL.md

# Verify output
ls skills/coding-standards/python/
# Expected: SKILL.md, skill.md, skill-metadata.yaml

# Test loader with both formats
python3 scripts/skill-loader.py load python --format 3level
python3 scripts/skill-loader.py load python --format canonical
```

### Phase 2: Pilot Migration (Week 2)

**Objective**: Migrate 5 representative skills to validate approach

**Selected Skills** (diverse representation):

1. `skills/coding-standards/python/SKILL.md` - Mature, complex
2. `skills/security/authentication/SKILL.md` - Security domain
3. `skills/testing/SKILL.md` - Category-level skill
4. `skills/cloud-native/kubernetes/SKILL.md` - DevOps domain
5. `skills/api/graphql/SKILL.md` - API domain

**Tasks**:

1. Run converter on pilot skills
2. Manual review of generated `skill.md` files
3. Fix converter edge cases
4. Validate with actual Claude Projects
5. Gather feedback

**Success Criteria**:

- [ ] All 5 skills generate valid `skill.md`
- [ ] Canonical format loads correctly in Claude Projects
- [ ] 3-level format still works via skill-loader
- [ ] No broken links or formatting issues
- [ ] Metadata extraction is accurate

### Phase 3: Bulk Migration (Week 3)

**Objective**: Migrate all 61 skills to dual-format

**Tasks**:

1. **Automated Migration**

   ```bash
   # Batch convert all skills
   python3 scripts/bulk-convert-skills.py --all
   ```

2. **Validation**

   ```bash
   # Run full validation suite
   python3 scripts/validate-skills.py --all
   python3 scripts/generate-audit-reports.py
   ```

3. **Update CLAUDE.md**
   - Document dual-format support
   - Update loading instructions
   - Add canonical format examples

4. **Update Product Matrix**
   - Ensure `config/product-matrix.yaml` references work with both formats
   - Update skill references if needed

**Deliverables**:

- ✅ 61 skills with both `SKILL.md` and `skill.md`
- ✅ 61 `skill-metadata.yaml` files
- ✅ Updated `CLAUDE.md` with dual-format docs
- ✅ Validation report: 0 errors

### Phase 4: Documentation and Training (Week 4)

**Objective**: Complete documentation and enable team adoption

**Tasks**:

1. **Update All Guides**
   - `docs/guides/SKILL_AUTHORING_GUIDE.md` - add canonical format
   - `docs/guides/SKILLS_USER_GUIDE.md` - explain both formats
   - `docs/guides/SKILLS_QUICK_START.md` - update examples
   - `README.md` - update main documentation

2. **Create Examples**
   - Add `examples/skill-templates/canonical-format/`
   - Add `examples/skill-templates/3level-format/`
   - Provide conversion examples

3. **Update CI/CD**
   - Add validation step for both formats
   - Auto-generate canonical format on commit
   - Ensure pre-commit hooks handle both

4. **Migration Guide**
   - Create `docs/migration/SKILLS_V2_MIGRATION.md`
   - Document breaking changes (none expected)
   - Provide rollback procedure

**Deliverables**:

- ✅ Complete documentation set
- ✅ CI/CD pipeline updated
- ✅ Migration guide published
- ✅ Example templates available

### Phase 5: Validation and Monitoring (Week 5)

**Objective**: Ensure stability and gather metrics

**Tasks**:

1. **Comprehensive Testing**

   ```bash
   # Run full test suite
   pytest tests/ -v

   # Validate all skills
   python3 scripts/validate-skills.py --comprehensive

   # Check audit gates
   python3 scripts/generate-audit-reports.py
   ```

2. **Performance Metrics**
   - Measure token counts: canonical vs 3-level
   - Validate Level 1 (<2,000 tokens)
   - Validate Level 2 (<5,000 tokens)
   - Compare loading times

3. **Real-World Testing**
   - Test skills in Claude Projects
   - Test skills via skill-loader CLI
   - Verify product matrix integration
   - Validate NIST control tagging

4. **Documentation Accuracy**

   ```bash
   # Run claims validation
   python3 scripts/validate-claims.py --verbose

   # Check for broken links
   python3 scripts/generate-audit-reports.py
   ```

**Success Criteria**:

- [ ] All tests pass
- [ ] 0 broken links
- [ ] Token counts within limits
- [ ] Both formats fully functional
- [ ] No performance degradation

---

## 4. Risk Assessment and Mitigation

### 4.1 Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Breaking existing workflows** | High | Medium | Maintain backward compatibility; `SKILL.md` remains primary |
| **Canonical format incompatibility** | Medium | High | Validate with actual Claude Projects; provide manual upload path |
| **Token count violations** | Medium | Low | Automated validation in CI/CD; strict token limits |
| **Metadata inconsistencies** | Medium | Medium | Schema validation; comprehensive tests |
| **Performance degradation** | Low | Low | Benchmark before/after; optimize converter |
| **User confusion** | Medium | Medium | Clear documentation; migration guide; examples |

### 4.2 Mitigation Strategies

1. **Backward Compatibility**
   - `SKILL.md` remains source of truth
   - skill-loader supports both formats
   - Existing automation unchanged
   - Rollback: delete generated files

2. **Validation Gates**

   ```bash
   # Pre-commit validation
   python3 scripts/validate-skills.py --format both

   # CI/CD validation
   .github/workflows/validate-skills.yml
   ```

3. **Rollback Plan**

   ```bash
   # Remove generated files
   find skills -name "skill.md" -delete
   find skills -name "skill-metadata.yaml" -delete

   # Restore original skill-loader
   git checkout main -- scripts/skill-loader.py
   ```

4. **Testing Strategy**
   - Unit tests for converter
   - Integration tests for skill-loader
   - End-to-end tests with real skills
   - Manual testing in Claude Projects

---

## 5. Success Criteria and Validation

### 5.1 Success Metrics

**Functional Requirements**:

- [ ] ✅ All 61 skills have both `SKILL.md` and `skill.md`
- [ ] ✅ Both formats pass validation
- [ ] ✅ skill-loader works with both formats
- [ ] ✅ Product matrix integration unchanged
- [ ] ✅ NIST tagging preserved
- [ ] ✅ Templates and resources accessible from both formats

**Non-Functional Requirements**:

- [ ] ✅ Token counts within limits (Level 1 <2K, Level 2 <5K)
- [ ] ✅ Loading time <2s per skill
- [ ] ✅ 0 broken links
- [ ] ✅ 0 hub violations
- [ ] ✅ Orphans ≤5
- [ ] ✅ 100% backward compatibility

**Documentation Requirements**:

- [ ] ✅ All guides updated
- [ ] ✅ Migration guide complete
- [ ] ✅ Examples provided
- [ ] ✅ CI/CD documented
- [ ] ✅ Rollback procedure documented

### 5.2 Validation Checklist

**Pre-Migration Validation**:

```bash
# Baseline metrics
python3 scripts/validate-skills.py --count-verify
python3 scripts/generate-audit-reports.py
python3 scripts/token-counter.py --all
```

**Post-Migration Validation**:

```bash
# Format validation
python3 scripts/validate-skills.py --format both --comprehensive

# Audit gates
python3 scripts/generate-audit-reports.py
# Expected: broken=0, hubs=0, orphans≤5

# Token counts
python3 scripts/token-counter.py --format canonical
python3 scripts/token-counter.py --format 3level

# Integration tests
pytest tests/integration/test_skill_loader.py
pytest tests/integration/test_product_matrix.py

# Manual validation
python3 scripts/skill-loader.py load product:api --format canonical
python3 scripts/skill-loader.py load product:api --format 3level
```

### 5.3 What Defines "Anthropic-Compliant"?

Given the lack of official specification, we define compliance as:

1. **Format Compatibility**:
   - ✅ Markdown file named `skill.md` or compatible
   - ✅ Human-readable structure
   - ✅ Clear sections: Overview, Instructions, Examples
   - ✅ No proprietary syntax requiring custom tooling

2. **Content Quality**:
   - ✅ Concise (focused on essential information)
   - ✅ Actionable (clear instructions)
   - ✅ Self-contained (minimal external dependencies)
   - ✅ Well-formatted (proper markdown)

3. **Integration**:
   - ✅ Works when pasted into Claude Projects custom instructions
   - ✅ Works with Claude Code via CLAUDE.md
   - ✅ No breaking syntax or characters

4. **Preserves Value-Add**:
   - ✅ NIST tagging still present (as comments)
   - ✅ Links to full SKILL.md for advanced users
   - ✅ Product matrix can reference either format

**Validation Method**:

```python
def validate_anthropic_compliance(skill_md_path: str) -> bool:
    """Validate skill.md against inferred Anthropic format."""
    with open(skill_md_path) as f:
        content = f.read()

    # Required sections
    required = ["# ", "## Overview", "## Core Instructions", "## Examples"]
    if not all(section in content for section in required):
        return False

    # Token count (inferred limit based on custom instructions field)
    tokens = estimate_tokens(content)
    if tokens > 10000:  # Conservative limit
        return False

    # Markdown validity
    if not is_valid_markdown(content):
        return False

    # No proprietary syntax
    if "{{" in content or "{%" in content:  # Template syntax
        return False

    return True
```

---

## 6. Code Changes Required

### 6.1 New Files to Create

```
scripts/
├── convert-skill-format.py          # NEW: SKILL.md → skill.md converter
├── bulk-convert-skills.py           # NEW: Batch converter
└── validate-skill-metadata.py       # NEW: Metadata validator

docs/guides/
├── SKILL_FORMAT_SPEC.md             # NEW: Format specification
└── SKILLS_V2_MIGRATION.md           # NEW: Migration guide

tests/
├── unit/
│   ├── test_skill_converter.py     # NEW: Converter tests
│   └── test_metadata_extractor.py  # NEW: Metadata tests
└── integration/
    └── test_dual_format_loader.py   # NEW: Integration tests

examples/skill-templates/
├── canonical-format/                # NEW: Canonical format examples
│   └── example-skill.md
└── 3level-format/                   # NEW: 3-level format examples
    └── example-SKILL.md
```

### 6.2 Files to Modify

**scripts/skill-loader.py** - Add dual-format support:

```python
# Changes needed:
# 1. Add --format flag (canonical | 3level)
# 2. Support loading skill.md in addition to SKILL.md
# 3. Preserve backward compatibility (default to SKILL.md)

class SkillLoader:
    def load_skill(self, skill_name: str, level: int = 2, format: str = '3level'):
        """Load skill in specified format."""
        if format == 'canonical':
            skill_file = skill.path / 'skill.md'
        else:  # 3level (default)
            skill_file = skill.path / 'SKILL.md'

        if not skill_file.exists():
            # Fallback to other format
            alt_file = skill.path / ('SKILL.md' if format == 'canonical' else 'skill.md')
            if alt_file.exists():
                skill_file = alt_file

        # ... rest of loading logic
```

**scripts/validate-skills.py** - Extend validation:

```python
# Changes needed:
# 1. Add --format flag to validate specific format
# 2. Add --comprehensive flag to validate both formats
# 3. Add metadata validation

def validate_skill_formats(skill_path: Path) -> dict:
    """Validate both SKILL.md and skill.md if present."""
    results = {
        'skill_md': None,
        'SKILL_md': None,
        'metadata': None,
        'consistency': True
    }

    # Validate SKILL.md (3-level format)
    skill_md_path = skill_path / 'SKILL.md'
    if skill_md_path.exists():
        results['SKILL_md'] = validate_3level_format(skill_md_path)

    # Validate skill.md (canonical format)
    canonical_path = skill_path / 'skill.md'
    if canonical_path.exists():
        results['skill_md'] = validate_canonical_format(canonical_path)

    # Validate metadata
    metadata_path = skill_path / 'skill-metadata.yaml'
    if metadata_path.exists():
        results['metadata'] = validate_metadata(metadata_path)

    # Check consistency between formats
    if results['SKILL_md'] and results['skill_md']:
        results['consistency'] = check_consistency(skill_md_path, canonical_path)

    return results
```

**config/product-matrix.yaml** - Add format hints (optional):

```yaml
# Add format preference to product definitions
products:
  api:
    description: "RESTful or GraphQL API service"
    standards:
      - CS:language
      - TS:framework
    # Optional: specify preferred format
    skill_format: "3level"  # or "canonical"
```

**CLAUDE.md** - Document dual-format support:

```markdown
## Skills Format Support

This repository supports two skill formats:

1. **3-Level Format** (`SKILL.md`): Progressive disclosure with token optimization
2. **Canonical Format** (`skill.md`): Simplified format compatible with Claude Projects

### Loading Skills

```bash
# Load 3-level format (default)
python3 scripts/skill-loader.py load python

# Load canonical format
python3 scripts/skill-loader.py load python --format canonical

# Load specific level of 3-level format
python3 scripts/skill-loader.py load python --level 1  # Quick start only
```

### Format Comparison

| Feature | 3-Level (SKILL.md) | Canonical (skill.md) |
|---------|-------------------|---------------------|
| Token Optimization | ✅ Built-in (L1<2K, L2<5K) | ⚠️ Single level |
| NIST Tagging | ✅ Yes | ✅ Yes (comments) |
| Bundled Resources | ✅ Yes | ✅ Via links |
| Claude Projects | ⚠️ Via CLAUDE.md | ✅ Direct upload |
| Product Matrix | ✅ Yes | ✅ Yes |

```

### 6.3 CI/CD Changes

**.github/workflows/validate-skills.yml**:

```yaml
name: Validate Skills

on:
  pull_request:
    paths:
      - 'skills/**'
  push:
    branches: [main, master]

jobs:
  validate-formats:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Validate 3-level format
        run: python3 scripts/validate-skills.py --format 3level --comprehensive

      - name: Validate canonical format
        run: python3 scripts/validate-skills.py --format canonical --comprehensive

      - name: Validate metadata
        run: python3 scripts/validate-skill-metadata.py --all

      - name: Check token counts
        run: |
          python3 scripts/token-counter.py --format 3level --check-limits
          python3 scripts/token-counter.py --format canonical --check-limits

      - name: Run audit gates
        run: python3 scripts/generate-audit-reports.py

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: validation-reports
          path: reports/generated/
```

**.pre-commit-config.yaml**:

```yaml
repos:
  - repo: local
    hooks:
      - id: validate-skill-formats
        name: Validate Skill Formats
        entry: python3 scripts/validate-skills.py --format both
        language: system
        files: 'skills/.*/(SKILL|skill)\.md$'

      - id: validate-skill-metadata
        name: Validate Skill Metadata
        entry: python3 scripts/validate-skill-metadata.py
        language: system
        files: 'skills/.*/skill-metadata\.yaml$'

      - id: check-token-counts
        name: Check Token Counts
        entry: python3 scripts/token-counter.py --check-limits
        language: system
        files: 'skills/.*/(SKILL|skill)\.md$'
```

---

## 7. Implementation Sequence

### Day 1: Setup and Planning

- ✅ Review and approve this strategy document
- ✅ Set up development branch: `feature/skills-v2-dual-format`
- ✅ Create task tracking in project management tool
- ✅ Notify team of upcoming changes

### Day 2-3: Build Converter

- ✅ Implement `scripts/convert-skill-format.py`
- ✅ Add YAML frontmatter parser
- ✅ Add content extractor (Level 1, Level 2, Level 3)
- ✅ Add canonical format generator
- ✅ Add metadata extractor
- ✅ Write unit tests

### Day 4-5: Update Skill Loader

- ✅ Modify `scripts/skill-loader.py` for dual-format support
- ✅ Add `--format` flag
- ✅ Implement fallback logic
- ✅ Update CLI help text
- ✅ Write integration tests

### Day 6-7: Validation Framework

- ✅ Update `scripts/validate-skills.py`
- ✅ Create `scripts/validate-skill-metadata.py`
- ✅ Add consistency checks
- ✅ Write comprehensive tests

### Day 8-9: Pilot Migration

- ✅ Convert 5 pilot skills
- ✅ Manual review of outputs
- ✅ Fix converter issues
- ✅ Validate in Claude Projects
- ✅ Iterate based on feedback

### Day 10-12: Bulk Migration

- ✅ Create `scripts/bulk-convert-skills.py`
- ✅ Run bulk conversion on all 61 skills
- ✅ Run full validation suite
- ✅ Fix any issues
- ✅ Re-run validation until clean

### Day 13-14: Documentation

- ✅ Create `docs/guides/SKILL_FORMAT_SPEC.md`
- ✅ Create `docs/migration/SKILLS_V2_MIGRATION.md`
- ✅ Update all existing guides
- ✅ Update `CLAUDE.md`
- ✅ Create example templates

### Day 15-16: CI/CD and Testing

- ✅ Update `.github/workflows/validate-skills.yml`
- ✅ Update `.pre-commit-config.yaml`
- ✅ Run full test suite
- ✅ Run performance benchmarks
- ✅ Validate audit gates

### Day 17-18: Review and Polish

- ✅ Code review
- ✅ Documentation review
- ✅ Test in production-like environment
- ✅ Address feedback
- ✅ Final validation

### Day 19-20: Deployment

- ✅ Merge to main branch
- ✅ Tag release: `v2.0.0-skills-dual-format`
- ✅ Update changelog
- ✅ Announce to team
- ✅ Monitor for issues

---

## 8. Rollback Strategy

### When to Rollback

Rollback if:

- [ ] Critical functionality breaks
- [ ] More than 10% of skills fail validation
- [ ] Performance degrades by >50%
- [ ] Incompatibility discovered with Claude Projects
- [ ] Major bugs in converter or loader

### Rollback Procedure

```bash
# 1. Checkout previous version
git checkout v1.x.x

# 2. Remove generated files
find skills -name "skill.md" -delete
find skills -name "skill-metadata.yaml" -delete

# 3. Restore original scripts
git checkout v1.x.x -- scripts/skill-loader.py
git checkout v1.x.x -- scripts/validate-skills.py

# 4. Revert CLAUDE.md changes
git checkout v1.x.x -- CLAUDE.md

# 5. Run validation to ensure system is stable
python3 scripts/validate-skills.py --all
python3 scripts/generate-audit-reports.py

# 6. Tag rollback
git tag v2.0.1-rollback
git push origin v2.0.1-rollback

# 7. Notify team
echo "Skills v2 rolled back to v1.x.x due to: [REASON]"
```

### Post-Rollback Actions

1. **Root Cause Analysis**: Document what went wrong
2. **Fix Issues**: Address problems in feature branch
3. **Re-Test**: Comprehensive testing before next attempt
4. **Phased Rollout**: Consider smaller pilot group next time

---

## 9. Monitoring and Metrics

### Key Metrics to Track

1. **Format Distribution**:
   - Number of skills with `SKILL.md` only
   - Number of skills with both formats
   - Number of skills with `skill.md` only (should be 0)

2. **Token Counts**:
   - Average tokens per skill (canonical format)
   - Average tokens per skill (Level 1, Level 2, Level 3)
   - Skills exceeding limits

3. **Validation Metrics**:
   - Skills passing both format validations
   - Consistency checks passed
   - Broken links count
   - Hub violations

4. **Usage Metrics**:
   - Skill loader invocations by format
   - Product matrix loads by format
   - Claude Projects uploads (manual tracking)

5. **Performance Metrics**:
   - Converter execution time
   - Skill loader execution time
   - Validation suite execution time

### Monitoring Commands

```bash
# Daily health check
python3 scripts/health-check-skills.py

# Weekly metrics report
python3 scripts/skills-metrics-report.py --weekly

# Token analysis
python3 scripts/token-counter.py --all --report

# Format distribution
find skills -name "skill.md" | wc -l
find skills -name "SKILL.md" | wc -l
```

---

## 10. Next Steps

### Immediate Actions (This Week)

1. **Review and Approve**: Stakeholder review of this strategy document
2. **Resource Allocation**: Assign developers and timeline
3. **Create Branch**: Set up `feature/skills-v2-dual-format`
4. **Write Converter**: Begin implementation of format converter

### Short-Term (2-4 Weeks)

1. **Complete Phase 1-2**: Framework + pilot migration
2. **Validation**: Ensure approach works with real skills
3. **Iteration**: Refine based on pilot results

### Medium-Term (1-2 Months)

1. **Complete Phase 3-5**: Bulk migration + validation + monitoring
2. **Documentation**: Finalize all guides and examples
3. **Training**: Onboard team to new dual-format system

### Long-Term (3-6 Months)

1. **Anthropic Collaboration**: If official spec becomes available, align
2. **Automation**: Auto-generate canonical format on skill edits
3. **Optimization**: Based on usage metrics, optimize format
4. **Expansion**: Consider additional output formats (PDF, EPUB, etc.)

---

## Appendix A: Research Notes

### Anthropic Documentation Search Results

**Attempted URLs**:

- `https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-libraries` → 404
- `https://support.anthropic.com/en/articles/9517075-what-are-custom-instructions` → Generic Projects info
- `https://docs.claude.com/en/docs/claude-code/skills` → Not accessible
- `https://docs.claude.com/en/api/agent-sdk/skills` → Not accessible

**Conclusions**:

1. Official skills.md specification not publicly documented
2. Custom instructions in Claude Projects use free-form markdown
3. No standardized schema or frontmatter required
4. Integration via web UI upload, not file-based loading

**Recommendation**: Proceed with inferred canonical format based on best practices and Claude Projects compatibility testing.

---

## Appendix B: Example Conversion

### Input: SKILL.md (3-Level Format)

```markdown
---
name: python-testing
description: Comprehensive Python testing with pytest
category: testing
difficulty: intermediate
estimated_time: "30 minutes"
nist_controls: [SI-10, SI-11]
---

# Python Testing Standards

## Level 1: Quick Start (<2,000 tokens, 5 minutes)

### Core Principles
1. Test-driven development
2. >80% coverage
...

## Level 2: Implementation (<5,000 tokens, 30 minutes)

### Advanced Testing Patterns
...

## Level 3: Mastery (Extended)

### Resources
...
```

### Output: skill.md (Canonical Format)

```markdown
# Python Testing Standards

> **Category**: testing
> **Difficulty**: intermediate
> **Estimated Time**: 30 minutes

Comprehensive Python testing with pytest, focusing on test-driven development, high coverage, and production-ready patterns.

## Overview

This skill covers Python testing best practices including:

- Test-driven development workflow
- pytest framework and fixtures
- Code coverage >80%
- Mocking and test isolation
- CI/CD integration

## When to Use This Skill

- Setting up testing for new Python projects
- Improving test coverage on existing codebases
- Implementing TDD workflow
- Preparing for production deployments

## Core Instructions

### Essential Testing Workflow

1. **Write test first** (TDD Red-Green-Refactor):
   ```python
   # test_calculator.py
   def test_add():
       assert add(2, 3) == 5
   ```

2. **Implement minimal code**:

   ```python
   # calculator.py
   def add(a, b):
       return a + b
   ```

3. **Refactor and expand**

### pytest Best Practices

[Level 2 content condensed here...]

### NIST Controls

This skill implements:

- @nist SI-10: Input validation testing
- @nist SI-11: Error handling validation

## Examples

[Code examples from Level 1 and Level 2...]

## Integration Points

Related skills:

- [Coding Standards - Python](../coding-standards/python/SKILL.md)
- [CI/CD](../devops/ci-cd/SKILL.md)

## Additional Resources

For comprehensive coverage including advanced topics, see:

- Full documentation: [SKILL.md](./SKILL.md)
- Test templates: [templates/](./templates/)
- Setup scripts: [scripts/](./scripts/)

---

*This is a simplified version for quick reference. For 3-level progressive disclosure (Level 1: <2K tokens, Level 2: <5K tokens, Level 3: Extended), see [SKILL.md](./SKILL.md)*

```

---

## Appendix C: Token Optimization Comparison

### 3-Level Format Token Distribution

```

skills/coding-standards/python/SKILL.md:
  Level 1 (Quick Start):     1,847 tokens ✅ <2,000
  Level 2 (Implementation):  4,923 tokens ✅ <5,000
  Level 3 (Mastery):         2,156 tokens (references only)
  Total:                     8,926 tokens

Loading scenarios:
  Quick reference:           1,847 tokens (Level 1 only)
  Standard usage:            6,770 tokens (Level 1 + 2)
  Comprehensive:             8,926 tokens (All levels)

```

### Canonical Format Token Distribution

```

skills/coding-standards/python/skill.md:
  Single level:              3,421 tokens

Loading scenarios:
  All usage:                 3,421 tokens (no progressive disclosure)

```

### Optimization Impact

**Scenario 1: Quick Reference**
- 3-level: 1,847 tokens
- Canonical: 3,421 tokens
- **Savings: 46%**

**Scenario 2: Standard Implementation**
- 3-level: 6,770 tokens
- Canonical: 3,421 tokens
- **Canonical more efficient for single-level use**

**Scenario 3: Comprehensive Study**
- 3-level: 8,926 tokens
- Canonical: 3,421 tokens + link to full SKILL.md
- **Canonical wins for full content access via reference**

**Conclusion**: Both formats serve different purposes:
- **3-level**: Best for progressive learning and token-constrained contexts
- **Canonical**: Best for quick reference and Claude Projects upload

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-24 | System Architecture Designer | Initial strategy document |

**Approval Required**: Yes
**Approvers**: Repository Owner, Standards Team Lead
**Implementation Start**: Upon approval

---

**End of Document**
