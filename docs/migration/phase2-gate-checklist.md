# Phase 2 Quality Gate Checklist

**Version**: 1.0.0
**Date**: 2025-10-17
**Phase**: Core Skills Migration (Weeks 2-3)
**Purpose**: Quality validation for each converted skill

---

## Overview

This checklist ensures every skill meets quality standards before proceeding to the next phase. Use this for:

- **Per-Skill Validation**: Check each skill individually
- **Daily Gates**: End-of-day quality checks
- **Weekly Gates**: End-of-week comprehensive validation
- **Phase Gate**: Final Phase 2 completion gate

---

## Per-Skill Validation Checklist

Complete this checklist for EVERY skill before marking it as "complete".

### Skill Information

- **Skill Name**: _______________
- **Skill Path**: `skills/_______________/SKILL.md`
- **Category**: _______________
- **Priority**: High / Medium / Low
- **Assignee**: _______________
- **Date Completed**: _______________
- **Validator**: _______________

---

### 1. File Structure ✅

- [ ] **SKILL.md exists** at correct path
- [ ] **YAML frontmatter present** and valid
- [ ] **templates/ directory exists**
- [ ] **scripts/ directory exists**
- [ ] **resources/ directory exists**
- [ ] **examples/ directory exists** (if applicable)

**Notes**: _______________

---

### 2. YAML Frontmatter ✅

- [ ] **`name` field present**
  - Lowercase with hyphens
  - ≤64 characters
  - Matches directory name
- [ ] **`description` field present**
  - ≤1024 characters
  - Includes "when to use" guidance
  - Clear and actionable

**Frontmatter Sample**:

```yaml
---
name: skill-name-here
description: Clear description of what this skill does, when Claude should use it, and key capabilities.
---
```

**Notes**: _______________

---

### 3. SKILL.md Content ✅

- [ ] **Overview section** present
  - Brief introduction (1-2 paragraphs)
  - Sets context for the skill
- [ ] **"When to Use This Skill" section** present
  - Clear triggers and use cases
  - Specific scenarios
- [ ] **"Core Instructions" section** present
  - Main procedural knowledge
  - Step-by-step guidance
- [ ] **"Advanced Topics" section** present
  - References to resources/ files
  - Progressive disclosure
- [ ] **"Examples" section** present
  - At least 2 concrete examples
  - Copy-paste ready
  - Cover common use cases

**Notes**: _______________

---

### 4. Token Count ✅

- [ ] **SKILL.md body <5,000 tokens**
  - Measured using OpenAI tokenizer
  - Excludes YAML frontmatter
  - Heavy content moved to resources/

**Token Count**: _______ tokens (Target: <5,000)

**Optimization Notes** (if >4,500 tokens):

- _______________
- _______________

**Notes**: _______________

---

### 5. Resources Directory ✅

- [ ] **All referenced resources exist**
  - Check every link in SKILL.md
  - Verify file paths are correct
- [ ] **Resources are well-organized**
  - Logical naming
  - Clear purpose
- [ ] **Resources are complete**
  - No placeholder content
  - Ready for use

**Resource Files**:

- [ ] `resources/_______________`
- [ ] `resources/_______________`
- [ ] `resources/_______________`

**Notes**: _______________

---

### 6. Templates Directory ✅

- [ ] **Templates are present**
  - At least 1 template (or README explaining why none)
- [ ] **Templates are functional**
  - Valid syntax
  - Ready to use
  - Include comments/documentation
- [ ] **Templates are relevant**
  - Match skill content
  - Cover common scenarios

**Template Files**:

- [ ] `templates/_______________`
- [ ] `templates/_______________`
- [ ] `templates/_______________`

**Notes**: _______________

---

### 7. Scripts Directory ✅

- [ ] **Scripts are present**
  - At least 1 script (or README explaining why none)
- [ ] **Scripts are executable**
  - `chmod +x` applied
  - Shebang line present
- [ ] **Scripts are tested**
  - Runs without errors
  - Produces expected output
- [ ] **Scripts are documented**
  - Header comments
  - Usage instructions

**Script Files**:

- [ ] `scripts/_______________` (Executable: YES / NO)
- [ ] `scripts/_______________` (Executable: YES / NO)
- [ ] `scripts/_______________` (Executable: YES / NO)

**Notes**: _______________

---

### 8. Examples ✅

- [ ] **At least 2 examples present**
- [ ] **Examples are concrete**
  - Real-world scenarios
  - Complete and runnable
- [ ] **Examples are diverse**
  - Cover different use cases
  - Show skill flexibility
- [ ] **Examples are explained**
  - Context provided
  - Expected outcomes clear

**Example Count**: _______

**Notes**: _______________

---

### 9. Cross-References ✅

- [ ] **All internal links valid**
  - Links to other skills work
  - Links to resources work
- [ ] **External links valid** (if any)
  - Check URL accessibility
  - Prefer archived/stable sources
- [ ] **No broken links**
  - Run link checker
  - Fix or remove broken links

**Link Count**: _______
**Broken Links**: _______

**Notes**: _______________

---

### 10. Consistency ✅

- [ ] **Style matches other skills**
  - Consistent tone and voice
  - Consistent formatting
- [ ] **Terminology consistent**
  - Uses standard terms
  - Matches glossary
- [ ] **Structure consistent**
  - Follows template
  - Section order matches

**Notes**: _______________

---

### 11. Technical Accuracy ✅

- [ ] **Content is accurate**
  - Best practices current
  - Examples work
- [ ] **No deprecated patterns**
  - Modern approaches used
  - Outdated methods noted
- [ ] **Security best practices**
  - No security anti-patterns
  - Secure by default

**Notes**: _______________

---

### 12. Automated Validation ✅

- [ ] **`scripts/validate-skills.py` passes**
  - No structural errors
  - All checks green
- [ ] **Token count verified**
  - Automated check confirms <5k
- [ ] **File existence verified**
  - All referenced files exist
- [ ] **Scripts execute without errors**
  - All scripts run successfully

**Validation Output**:

```
_______________
_______________
_______________
```

**Notes**: _______________

---

### Final Skill Assessment

**Overall Quality Score**: _____ / 12 categories passing

**Status**:

- [ ] ✅ **PASS** - Ready for use (≥11/12 passing)
- [ ] ⚠️ **CONDITIONAL PASS** - Minor issues to fix (10/12 passing)
- [ ] ❌ **FAIL** - Major issues, needs rework (<10/12 passing)

**Decision**: PASS / CONDITIONAL PASS / FAIL

**Reviewer Signature**: _______________
**Date**: _______________

**Action Items** (if CONDITIONAL PASS or FAIL):

1. _______________
2. _______________
3. _______________

---

## Daily Gate Checklist

Complete this checklist at the end of each day during Phase 2.

### Day Information

- **Day**: Day ___ of Phase 2
- **Date**: _______________
- **Skills Targeted**: _______
- **Skills Completed**: _______
- **Skills Validated**: _______

---

### Daily Quality Metrics

- [ ] **All completed skills passed per-skill validation**
- [ ] **No P0 or P1 issues introduced**
- [ ] **Token counts within limits**
- [ ] **Scripts tested and working**
- [ ] **All work committed to git**
- [ ] **Progress tracker updated**

**Daily Pass Rate**: _____% (Target: 100%)

**Issues Identified**:

- _______________
- _______________

**Action Plan for Tomorrow**:

1. _______________
2. _______________
3. _______________

**Daily Gate Decision**: PASS / CONDITIONAL PASS / FAIL

---

## Weekly Gate Checklist

Complete this checklist at the end of Week 2 (Day 10) and Week 3 (Day 15).

### Week Information

- **Week**: Week 2 / Week 3
- **End Date**: _______________
- **Skills Targeted**: _______
- **Skills Completed**: _______
- **Skills Validated**: _______
- **Completion Rate**: _____%

---

### Week 2 Gate (Day 10)

**Target**: 10 skills complete

- [ ] **Python skill validated**
- [ ] **JavaScript skill validated**
- [ ] **TypeScript skill validated**
- [ ] **Go skill validated**
- [ ] **Authentication skill validated**
- [ ] **Secrets Management skill validated**
- [ ] **Unit Testing skill validated**
- [ ] **Integration Testing skill validated**
- [ ] **CI/CD skill validated**
- [ ] **React skill started** (optional)

**Additional Checks**:

- [ ] **Meta-skills operational** (skill-loader, legacy-bridge)
- [ ] **Phase 1 remediation 100% complete**
- [ ] **Automation scripts tested**
- [ ] **Token optimization verified**
- [ ] **No blockers for Week 3**

**Week 2 Completion**: _____% (Target: 100%)

**Week 2 Gate Decision**: PASS / CONDITIONAL PASS / FAIL

**Notes**: _______________

---

### Week 3 Gate (Day 15)

**Target**: 11 additional skills complete (21 total)

- [ ] **React skill validated** (if not done Week 2)
- [ ] **Kubernetes skill validated**
- [ ] **Rust skill validated**
- [ ] **Zero-Trust skill validated**
- [ ] **Threat Modeling skill validated**
- [ ] **Input Validation skill validated**
- [ ] **E2E Testing skill validated**
- [ ] **Performance Testing skill validated**
- [ ] **Infrastructure skill validated**
- [ ] **Monitoring skill validated**
- [ ] **Containers skill validated**
- [ ] **Serverless skill validated**

**Additional Checks**:

- [ ] **All 21 skills validated**
- [ ] **skills-catalog.yaml generated**
- [ ] **product-matrix.yaml updated**
- [ ] **Integration tests passing**
- [ ] **Documentation complete**
- [ ] **Phase 2 report generated**

**Week 3 Completion**: _____% (Target: 100%)

**Week 3 Gate Decision**: PASS / CONDITIONAL PASS / FAIL

**Notes**: _______________

---

## Phase 2 Completion Gate

Complete this checklist at the end of Phase 2 (Day 15) for final sign-off.

### Phase 2 Summary

- **Start Date**: _______________
- **End Date**: _______________
- **Duration**: _____ days
- **Skills Targeted**: 21
- **Skills Completed**: _______
- **Skills Validated**: _______
- **Completion Rate**: _____%

---

### Phase 2 Completion Criteria

#### 1. Skills Conversion ✅

- [ ] **All 21 target skills converted**
  - 5 coding skills (Python, JS, TS, Go, Rust)
  - 5 security skills (Auth, Secrets, Zero-Trust, Threat, Validation)
  - 4 testing skills (Unit, Integration, E2E, Performance)
  - 3 DevOps skills (CI/CD, Infrastructure, Monitoring)
  - 3 cloud-native skills (Kubernetes, Containers, Serverless)
  - 1 frontend skill (React)

**Skills Completed**: _____ / 21

---

#### 2. Quality Validation ✅

- [ ] **All skills passed per-skill validation**
- [ ] **All token counts <5,000**
- [ ] **All scripts executable and tested**
- [ ] **All resources present and linked**
- [ ] **All examples functional**
- [ ] **No broken links**

**Validation Pass Rate**: _____% (Target: 100%)

---

#### 3. Phase 1 Remediation ✅

- [ ] **6 remaining directories complete**
- [ ] **Script unit tests written (>90% coverage)**
- [ ] **legacy-bridge implemented**
- [ ] **skill-loader CLI complete**

**Remediation Hours**: _____ / 22 (Target: 22)

---

#### 4. Integration & Testing ✅

- [ ] **skill-loader tested with all 21 skills**
- [ ] **legacy-bridge mappings verified**
- [ ] **@load patterns working**
- [ ] **Integration test suite passing**
- [ ] **End-to-end skill loading tested**

**Integration Pass Rate**: _____% (Target: 100%)

---

#### 5. Configuration & Catalog ✅

- [ ] **skills-catalog.yaml generated**
  - All 21 skills listed
  - Metadata accurate
  - Categories correct
- [ ] **product-matrix.yaml updated**
  - New skills referenced
  - Product mappings updated
- [ ] **legacy-mappings.yaml complete**
  - Old → new mappings
  - Deprecation warnings

**Configuration Files**: _____ / 3 complete

---

#### 6. Documentation ✅

- [ ] **All skill READMEs updated**
- [ ] **SKILL_AUTHORING_GUIDE.md current**
- [ ] **MIGRATION_GUIDE.md updated**
- [ ] **Phase 2 completion report generated**
- [ ] **Phase 3 recommendations documented**

**Documentation Complete**: YES / NO

---

#### 7. Issue Resolution ✅

- [ ] **Zero P0 issues**
- [ ] **Zero P1 issues**
- [ ] **All P2 issues tracked**
- [ ] **All P3 issues documented**

**Critical Issues**: _____ (Target: 0)

---

#### 8. Performance Metrics ✅

- [ ] **Token optimization verified**
  - Average skill size: _____ tokens
  - 95th percentile: _____ tokens
  - Max skill size: _____ tokens (Target: <5,000)
- [ ] **Skill load time acceptable**
  - Average: _____ ms (Target: <500ms)
- [ ] **Automation efficiency confirmed**
  - Scripts success rate: _____% (Target: >90%)

**Performance Metrics**: PASS / FAIL

---

#### 9. Team Sign-Off ✅

- [ ] **Content Engineers approve** (all 3)
- [ ] **QA Engineer approves**
- [ ] **Infrastructure Engineer approves**
- [ ] **Integration Engineer approves**
- [ ] **Project Lead approves**

**Sign-Off Count**: _____ / 6

---

#### 10. Phase 3 Readiness ✅

- [ ] **Phase 3 plan reviewed**
- [ ] **Resources allocated**
- [ ] **Dependencies identified**
- [ ] **Risks documented**
- [ ] **Timeline agreed**

**Phase 3 Ready**: YES / NO

---

### Phase 2 Gate Decision

**Total Criteria Met**: _____ / 10 (Target: ≥9/10 for PASS)

**Decision**:

- [ ] ✅ **PASS** - Phase 2 complete, proceed to Phase 3
- [ ] ⚠️ **CONDITIONAL PASS** - Minor items to complete, proceed with tracking
- [ ] ❌ **FAIL** - Major issues, Phase 2 extension required

**Final Decision**: PASS / CONDITIONAL PASS / FAIL

**Approver**: _______________
**Title**: _______________
**Date**: _______________
**Signature**: _______________

---

### Action Items (if CONDITIONAL PASS or FAIL)

1. **Issue**: _______________
   **Severity**: P0 / P1 / P2 / P3
   **Owner**: _______________
   **Deadline**: _______________

2. **Issue**: _______________
   **Severity**: P0 / P1 / P2 / P3
   **Owner**: _______________
   **Deadline**: _______________

3. **Issue**: _______________
   **Severity**: P0 / P1 / P2 / P3
   **Owner**: _______________
   **Deadline**: _______________

---

## Appendix: Common Issues & Solutions

### Issue: Token Count >5,000

**Symptoms**: Skill SKILL.md exceeds token budget

**Solutions**:

1. Move detailed content to `resources/` files
2. Create summary/overview in SKILL.md
3. Reference detailed content via links
4. Use tables for dense information
5. Move examples to separate files

---

### Issue: Scripts Not Executable

**Symptoms**: Scripts fail to run

**Solutions**:

1. Add shebang line: `#!/usr/bin/env bash` or `#!/usr/bin/env python3`
2. Run: `chmod +x scripts/*.sh`
3. Test execution: `./scripts/script-name.sh`
4. Check PATH for required binaries

---

### Issue: Broken Links

**Symptoms**: References to non-existent files

**Solutions**:

1. Create missing files
2. Fix file paths
3. Remove invalid references
4. Use relative paths: `./resources/file.md`
5. Run link checker before validation

---

### Issue: Inconsistent Style

**Symptoms**: Skills look different from each other

**Solutions**:

1. Follow SKILL.md.template exactly
2. Use consistent section headers
3. Match tone and voice of other skills
4. Review SKILL_AUTHORING_GUIDE.md
5. Pair review with another engineer

---

### Issue: Unclear "When to Use"

**Symptoms**: Description doesn't explain triggers

**Solutions**:

1. Add specific scenarios: "Use when building Python APIs"
2. Include tech stack triggers: "Use with FastAPI, Django"
3. Add anti-patterns: "Don't use for shell scripts"
4. Provide decision criteria
5. Link to product-matrix for context

---

## Validation Tools

### Automated Validation

```bash
# Validate single skill
python3 scripts/validate-skills.py --skill skills/coding-standards/python

# Validate all skills
python3 scripts/validate-skills.py --all

# Check token counts
python3 scripts/validate-skills.py --tokens
```

### Manual Validation

```bash
# Count tokens (approximate)
wc -w skills/coding-standards/python/SKILL.md

# Check script permissions
ls -l skills/*/scripts/*.sh

# Find broken links
grep -r "](\./" skills/ | while read line; do
  # Parse and check file existence
done
```

### Link Checking

```bash
# Install markdown-link-check
npm install -g markdown-link-check

# Check links
markdown-link-check skills/coding-standards/python/SKILL.md
```

---

**Document Owner**: QA Lead
**Last Updated**: 2025-10-17
**Status**: Active
**Next Review**: Daily during Phase 2 execution

---

*Phase 2 Quality Gate Checklist v1.0.0*
