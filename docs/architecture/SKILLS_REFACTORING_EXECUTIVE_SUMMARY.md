# Skills Format Refactoring - Executive Summary

**Date**: 2025-10-24
**Status**: Design Phase
**Full Strategy**: [SKILLS_REFACTORING_STRATEGY.md](./SKILLS_REFACTORING_STRATEGY.md)

---

## TL;DR

**Objective**: Align standards repository skills with Anthropic's canonical format while preserving our value-add features (3-level token optimization, NIST tagging, product matrix).

**Approach**: **Hybrid dual-format strategy** - maintain existing `SKILL.md` as source of truth, auto-generate simplified `skill.md` for Claude Projects compatibility.

**Timeline**: 20 days (4 weeks)
**Impact**: Zero breaking changes, 100% backward compatible

---

## Key Decisions

### ✅ What We're Keeping

1. **SKILL.md format** - Remains source of truth with 3-level progressive disclosure
2. **Token optimization** - Level 1 <2K, Level 2 <5K structure preserved
3. **NIST tagging** - @nist comments in code examples
4. **Product matrix** - `config/product-matrix.yaml` integration
5. **Bundled resources** - templates/, scripts/, resources/ directories
6. **skill-loader CLI** - All existing functionality

### ➕ What We're Adding

1. **skill.md** - Auto-generated canonical format (simplified, Claude Projects compatible)
2. **skill-metadata.yaml** - Extracted metadata for tooling (optional)
3. **Dual-format support** - skill-loader handles both formats
4. **Format converter** - `scripts/convert-skill-format.py`
5. **Enhanced validation** - Checks both formats for consistency

### ❌ What We're NOT Changing

1. Existing skill content
2. Skill organization structure
3. Product matrix mappings
4. CLAUDE.md loading mechanism
5. CLI interface (backward compatible)

---

## Gap Analysis Summary

| Aspect | Current | Anthropic (Inferred) | Decision |
|--------|---------|----------------------|----------|
| **File name** | SKILL.md | skills.md | Keep both |
| **Metadata** | YAML frontmatter | None | Extract to separate file |
| **Structure** | 3-level progressive | Single level | Generate simplified version |
| **Token optimization** | Built-in | Manual | Preserve in SKILL.md |
| **NIST tagging** | Yes | No | Preserve via comments |
| **Resources** | Bundled | Links | Preserve bundles |

**Finding**: Our implementation is MORE sophisticated than inferred canonical format. We're adding compatibility, not removing features.

---

## Migration Plan (5 Phases)

### Phase 1: Framework (Week 1)

- Build format converter
- Update skill-loader for dual formats
- Add validation for both formats
- **Deliverable**: Working converter + updated tooling

### Phase 2: Pilot (Week 2)

- Migrate 5 representative skills
- Validate approach
- Fix edge cases
- **Deliverable**: 5 skills in both formats, validated

### Phase 3: Bulk Migration (Week 3)

- Convert all 61 skills
- Full validation suite
- Update CLAUDE.md
- **Deliverable**: All skills dual-format

### Phase 4: Documentation (Week 4)

- Update all guides
- Create migration guide
- Update CI/CD
- **Deliverable**: Complete documentation

### Phase 5: Validation (Week 5)

- Comprehensive testing
- Performance benchmarks
- Real-world validation
- **Deliverable**: Production-ready system

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Breaking workflows | High | Low | SKILL.md remains primary; full backward compat |
| Format incompatibility | Medium | Medium | Validate with Claude Projects; manual upload path |
| Token violations | Medium | Low | Automated validation in CI/CD |
| User confusion | Medium | Low | Clear docs + examples |

**Overall Risk**: **LOW** - Approach is additive, not destructive

---

## Success Criteria

### Must Have ✅

- [ ] All 61 skills have both SKILL.md and skill.md
- [ ] Both formats pass validation
- [ ] skill-loader works with both formats
- [ ] 100% backward compatibility
- [ ] 0 broken links, 0 hub violations, orphans ≤5

### Nice to Have ⭐

- [ ] Auto-generation on commit via pre-commit hook
- [ ] Claude Projects tested and validated
- [ ] Performance benchmarks documented
- [ ] Team trained on dual-format usage

---

## Resource Requirements

### People

- 1 Senior Developer (full-time, 2 weeks)
- 1 Technical Writer (part-time, 1 week)
- 1 QA Engineer (part-time, 1 week)
- Repository Owner (review and approval, 4 hours)

### Tools

- Existing Python environment
- pytest for testing
- No new dependencies required

### Timeline

- **Week 1**: Framework development
- **Week 2**: Pilot migration + validation
- **Week 3**: Bulk conversion + docs
- **Week 4**: Final validation + deployment

---

## Key Architectural Changes

### Before (Current)

```
skills/
├── coding-standards/
│   └── python/
│       ├── SKILL.md              # 3-level format
│       ├── resources/
│       ├── templates/
│       └── scripts/
```

### After (Dual-Format)

```
skills/
├── coding-standards/
│   └── python/
│       ├── SKILL.md              # Source of truth (3-level)
│       ├── skill.md              # Generated (canonical)
│       ├── skill-metadata.yaml   # Generated (metadata)
│       ├── resources/
│       ├── templates/
│       └── scripts/
```

### Loading Behavior

```bash
# Load 3-level format (default, unchanged)
python3 scripts/skill-loader.py load python

# Load canonical format (new)
python3 scripts/skill-loader.py load python --format canonical

# Load specific level (unchanged)
python3 scripts/skill-loader.py load python --level 1
```

---

## What "Anthropic-Compliant" Means

Since official specification is unavailable, we define compliance as:

1. **Format**: Markdown file with clear sections (Overview, Instructions, Examples)
2. **Content**: Concise, actionable, self-contained
3. **Integration**: Works when pasted into Claude Projects custom instructions
4. **Syntax**: No proprietary syntax requiring custom tooling

**Validation Method**: See `scripts/validate-anthropic-compliance.py`

---

## Rollback Plan

If migration fails, rollback is simple:

```bash
# Remove generated files
find skills -name "skill.md" -delete
find skills -name "skill-metadata.yaml" -delete

# Restore original tooling
git checkout v1.x.x -- scripts/skill-loader.py

# Validate system is stable
python3 scripts/validate-skills.py --all
```

**Rollback Time**: <15 minutes
**Data Loss**: None (SKILL.md unchanged)

---

## Next Steps

### Immediate (This Week)

1. ✅ Review and approve strategy document
2. ⬜ Allocate resources (1 senior dev)
3. ⬜ Create feature branch: `feature/skills-v2-dual-format`
4. ⬜ Begin converter implementation

### Short-Term (2-4 Weeks)

1. Complete Phase 1-2 (framework + pilot)
2. Validate approach with 5 skills
3. Iterate based on results

### Medium-Term (1-2 Months)

1. Complete Phase 3-5 (bulk migration + validation)
2. Finalize documentation
3. Deploy to production

---

## Questions and Answers

### Q: Will this break existing workflows?

**A**: No. SKILL.md remains unchanged. skill-loader default behavior is identical to current behavior.

### Q: Why not just use canonical format everywhere?

**A**: Our 3-level format provides superior token optimization (46-99% savings in some scenarios) and progressive disclosure that benefits learning workflows.

### Q: What if Anthropic releases official specification later?

**A**: Dual-format approach allows us to quickly adapt. We'll update the generator to match official spec while keeping SKILL.md as source.

### Q: How do we validate canonical format works with Claude Projects?

**A**: Manual testing - upload generated skill.md to Claude Projects and verify functionality. Automate validation once integration patterns are clear.

### Q: What happens to NIST tagging in canonical format?

**A**: NIST controls preserved as comments in code examples (e.g., `# @nist IA-2 "User authentication"`). Also documented in metadata file.

---

## Approval Checklist

- [ ] Repository Owner reviewed and approved
- [ ] Standards Team Lead reviewed and approved
- [ ] Technical approach validated
- [ ] Resource allocation confirmed
- [ ] Timeline accepted
- [ ] Risk assessment accepted

**Approved By**: ___________________
**Date**: ___________________
**Implementation Start Date**: ___________________

---

## Contact and Questions

- **Strategy Author**: System Architecture Designer
- **Full Documentation**: [SKILLS_REFACTORING_STRATEGY.md](./SKILLS_REFACTORING_STRATEGY.md)
- **Repository**: https://github.com/williamzujkowski/standards
- **Questions**: File issue or contact repository owner

---

**Status**: ⏳ Awaiting Approval
**Next Review**: Upon stakeholder feedback
