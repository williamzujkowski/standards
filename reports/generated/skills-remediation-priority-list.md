# Skills Remediation Priority List

**Generated:** 2025-10-24
**For:** Remediation Agents
**Status:** READY FOR EXECUTION

---

## 🎯 How to Use This List

1. **Pick a skill** from your assigned priority tier
2. **Read the full skill** to understand current state
3. **Apply fixes** listed in the "Required Actions" column
4. **Use templates** from the compliance report
5. **Validate** with `python3 scripts/analyze-skills-compliance.py`
6. **Commit** when skill reaches 100% compliance

---

## 🚨 TIER 1: CRITICAL (Top 10 Most-Used Skills)

**Goal:** Add universal sections (Examples, Integration, Pitfalls)
**Timeline:** Next 24 hours
**Estimated Effort:** 30 minutes per skill

| # | Skill Path | Current % | Required Actions | Est. Time |
|---|------------|-----------|------------------|-----------|
| 1 | `skills/coding-standards/python/SKILL.md` | 43% | Add Examples, Integration Points, Common Pitfalls | 30 min |
| 2 | `skills/security/authentication/SKILL.md` | 29% | Add Examples, Integration Points, Common Pitfalls, fix token budget | 45 min |
| 3 | `skills/security/authorization/SKILL.md` | 43% | Add Examples, Integration Points, Common Pitfalls | 30 min |
| 4 | `skills/testing/unit-testing/SKILL.md` | 14% | Add Examples, Integration Points, Common Pitfalls, add Level 1-3 | 60 min |
| 5 | `skills/devops/ci-cd/SKILL.md` | 14% | Add Examples, Integration Points, Common Pitfalls, add Level 1-3 | 60 min |
| 6 | `skills/cloud-native/kubernetes/SKILL.md` | 14% | Add Examples, Integration Points, Common Pitfalls, add Level 1-3 | 60 min |
| 7 | `skills/frontend/react/SKILL.md` | 14% | Add Examples, Integration Points, Common Pitfalls, add Level 1-3 | 60 min |
| 8 | `skills/database/sql/SKILL.md` | 14% | Add Examples, Integration Points, Common Pitfalls, add Level 1-3 | 60 min |
| 9 | `skills/api/graphql/SKILL.md` | 14% | Add Examples, Integration Points, Common Pitfalls, add Level 1-3 | 60 min |
| 10 | `skills/security/secrets-management/SKILL.md` | 14% | Add Examples, Integration Points, Common Pitfalls, add Level 1-3 | 60 min |

**Total Tier 1 Effort:** 7.25 hours (sequential) / 1.5 hours (5 agents parallel)

---

## 🔥 TIER 2: OVERSIZED SKILLS NEEDING REFACTORING

**Goal:** Extract content to Level 3 files, add universal sections
**Timeline:** Next 48 hours
**Estimated Effort:** 1-2 hours per skill

| # | Skill Path | Tokens | L2 Tokens | Required Actions | Priority |
|---|------------|--------|-----------|------------------|----------|
| 1 | `skills/compliance/healthtech/SKILL.md` | 7,796 | 6,346 | Extract L2 to files, add universal sections | HIGH |
| 2 | `skills/cloud-native/advanced-kubernetes/SKILL.md` | 6,303 | 3,099 | Split into subtopics, add universal sections | HIGH |
| 3 | `skills/compliance/fintech/SKILL.md` | 5,749 | 3,504 | Extract compliance details, add universal sections | HIGH |
| 4 | `skills/security/authorization/SKILL.md` | 5,508 | 321 | Content exists but needs reorganization, add universal sections | MEDIUM |
| 5 | `skills/database/advanced-optimization/SKILL.md` | 5,447 | 731 | Extract advanced patterns, add universal sections | MEDIUM |
| 6 | `skills/security/zero-trust/SKILL.md` | 5,358 | 371 | Extract architecture docs, add universal sections | HIGH |
| 7 | `skills/security/security-operations/SKILL.md` | 5,317 | 364 | Split into operational guides, add universal sections | MEDIUM |
| 8 | `skills/coding-standards/shell/SKILL.md` | 5,222 | 18 | Extract examples to files, add universal sections | LOW |
| 9 | `skills/cloud-native/aws-advanced/SKILL.md` | 5,122 | 601 | Create service-specific subdirs, add universal sections | MEDIUM |
| 10 | `skills/security/api-security/SKILL.md` | 4,832 | 24 | Split by attack vector, add universal sections | HIGH |

### Refactoring Template

For each oversized skill:

1. Create `advanced/` subdirectory:

   ```bash
   mkdir -p skills/[category]/[skill-name]/advanced
   ```

2. Extract detailed content to files:

   ```
   advanced/
   ├── architecture.md
   ├── patterns.md
   ├── troubleshooting.md
   ├── case-studies.md
   └── performance.md
   ```

3. Update Level 3 to reference these files:

   ```markdown
   ## Level 3: Mastery

   For advanced topics, refer to:
   - [Architecture Guide](./advanced/architecture.md)
   - [Design Patterns](./advanced/patterns.md)
   - [Troubleshooting](./advanced/troubleshooting.md)
   ```

4. Add universal sections (Examples, Integration, Pitfalls)

**Total Tier 2 Effort:** 15-20 hours (sequential) / 4-5 hours (4 agents parallel)

---

## 📝 TIER 3: STUB SKILLS (Minimal Content)

**Goal:** Complete all sections from scratch
**Timeline:** Next 7 days
**Estimated Effort:** 2 hours per skill

### Subcategory: Cloud Native (Priority: HIGH)

| # | Skill Path | Current State | Required Actions |
|---|------------|---------------|------------------|
| 1 | `skills/cloud-native/containers/SKILL.md` | Placeholder | Full implementation (all levels + universal sections) |
| 2 | `skills/cloud-native/service-mesh/SKILL.md` | Placeholder | Full implementation |
| 3 | `skills/cloud-native/serverless/SKILL.md` | Placeholder | Full implementation |

### Subcategory: Frontend (Priority: HIGH)

| # | Skill Path | Current State | Required Actions |
|---|------------|---------------|------------------|
| 1 | `skills/frontend/mobile-ios/SKILL.md` | Placeholder | Full implementation |
| 2 | `skills/frontend/mobile-android/SKILL.md` | Placeholder | Full implementation |
| 3 | `skills/frontend/mobile-react-native/SKILL.md` | Placeholder | Full implementation |
| 4 | `skills/frontend/vue/SKILL.md` | Placeholder | Full implementation |

### Subcategory: Security (Priority: CRITICAL)

| # | Skill Path | Current State | Required Actions |
|---|------------|---------------|------------------|
| 1 | `skills/security/input-validation/SKILL.md` | Placeholder | Full implementation |
| 2 | `skills/security/threat-modeling/SKILL.md` | Placeholder | Full implementation |

### Subcategory: Testing (Priority: HIGH)

| # | Skill Path | Current State | Required Actions |
|---|------------|---------------|------------------|
| 1 | `skills/testing/e2e-testing/SKILL.md` | Placeholder | Full implementation |
| 2 | `skills/testing/integration-testing/SKILL.md` | Placeholder | Full implementation |
| 3 | `skills/testing/performance-testing/SKILL.md` | Placeholder | Full implementation |

### Subcategory: DevOps (Priority: MEDIUM)

| # | Skill Path | Current State | Required Actions |
|---|------------|---------------|------------------|
| 1 | `skills/devops/monitoring/SKILL.md` | Placeholder | Full implementation |
| 2 | `skills/devops/monitoring-observability/SKILL.md` | Placeholder | Full implementation |
| 3 | `skills/devops/infrastructure-as-code/SKILL.md` | Placeholder | Full implementation |

### Subcategory: ML/AI (Priority: MEDIUM)

| # | Skill Path | Current State | Required Actions |
|---|------------|---------------|------------------|
| 1 | `skills/ml-ai/model-development/SKILL.md` | Placeholder | Full implementation |
| 2 | `skills/ml-ai/model-deployment/SKILL.md` | Placeholder | Full implementation |
| 3 | `skills/ml-ai/mlops/SKILL.md` | Placeholder | Full implementation |

### Subcategory: Observability (Priority: MEDIUM)

| # | Skill Path | Current State | Required Actions |
|---|------------|---------------|------------------|
| 1 | `skills/observability/logging/SKILL.md` | Placeholder | Full implementation |
| 2 | `skills/observability/metrics/SKILL.md` | Placeholder | Full implementation |

### Subcategory: Data Engineering (Priority: MEDIUM)

| # | Skill Path | Current State | Required Actions |
|---|------------|---------------|------------------|
| 1 | `skills/data-engineering/data-quality/SKILL.md` | Placeholder | Full implementation |
| 2 | `skills/data-engineering/orchestration/SKILL.md` | Placeholder | Full implementation |

### Subcategory: Compliance (Priority: LOW - Already have detailed compliance skills)

| # | Skill Path | Current State | Required Actions |
|---|------------|---------------|------------------|
| 1 | `skills/compliance/gdpr/SKILL.md` | Placeholder | Full implementation |
| 2 | `skills/compliance/nist/SKILL.md` | Placeholder | Full implementation |

### Subcategory: Other (Priority: LOW)

| # | Skill Path | Current State | Required Actions |
|---|------------|---------------|------------------|
| 1 | `skills/architecture/patterns/SKILL.md` | Placeholder | Full implementation |
| 2 | `skills/content/documentation/SKILL.md` | Placeholder | Full implementation |
| 3 | `skills/design/ux/SKILL.md` | Placeholder | Full implementation |
| 4 | `skills/microservices/patterns/SKILL.md` | Placeholder | Full implementation |

**Total Tier 3 Effort:** 46 skills × 2 hours = 92 hours (sequential) / 23 hours (4 agents parallel)

---

## 🔧 TIER 4: PARTIAL SKILLS (Need Universal Sections Only)

**Goal:** Add Examples, Integration Points, Common Pitfalls
**Timeline:** Next 3 days
**Estimated Effort:** 30 minutes per skill

These skills already have Level 1-3 structure but are missing the 3 universal sections:

| # | Skill Path | Current % | Missing Sections |
|---|------------|-----------|------------------|
| 1 | `skills/coding-standards/go/SKILL.md` | 43% | Examples, Integration, Pitfalls |
| 2 | `skills/coding-standards/javascript/SKILL.md` | 43% | Examples, Integration, Pitfalls |
| 3 | `skills/coding-standards/kotlin/SKILL.md` | 43% | Examples, Integration, Pitfalls |
| 4 | `skills/coding-standards/python/SKILL.md` | 43% | Examples, Integration, Pitfalls |
| 5 | `skills/coding-standards/rust/SKILL.md` | 43% | Examples, Integration, Pitfalls |
| 6 | `skills/coding-standards/swift/SKILL.md` | 43% | Examples, Integration, Pitfalls |
| 7 | `skills/coding-standards/typescript/SKILL.md` | 43% | Examples, Integration, Pitfalls |
| 8 | `skills/database/nosql/SKILL.md` | 43% | Examples, Integration, Pitfalls |
| 9 | `skills/devops/infrastructure/SKILL.md` | 43% | Examples, Integration, Pitfalls |

**Total Tier 4 Effort:** 9 skills × 30 min = 4.5 hours (sequential) / 1.5 hours (3 agents parallel)

---

## 📋 Batch Processing Strategy

### Batch 1: Critical Security Skills (Agent 1)

- `skills/security/authentication/SKILL.md`
- `skills/security/authorization/SKILL.md`
- `skills/security/secrets-management/SKILL.md`
- `skills/security/input-validation/SKILL.md`
- `skills/security/api-security/SKILL.md`

### Batch 2: Core Coding Standards (Agent 2)

- `skills/coding-standards/python/SKILL.md`
- `skills/coding-standards/javascript/SKILL.md`
- `skills/coding-standards/typescript/SKILL.md`
- `skills/coding-standards/go/SKILL.md`

### Batch 3: Testing & Quality (Agent 3)

- `skills/testing/unit-testing/SKILL.md`
- `skills/testing/integration-testing/SKILL.md`
- `skills/testing/e2e-testing/SKILL.md`
- `skills/testing/performance-testing/SKILL.md`

### Batch 4: Cloud Native (Agent 4)

- `skills/cloud-native/kubernetes/SKILL.md`
- `skills/cloud-native/containers/SKILL.md`
- `skills/cloud-native/serverless/SKILL.md`
- `skills/cloud-native/service-mesh/SKILL.md`

### Batch 5: DevOps & Infrastructure (Agent 5)

- `skills/devops/ci-cd/SKILL.md`
- `skills/devops/infrastructure-as-code/SKILL.md`
- `skills/devops/monitoring-observability/SKILL.md`

### Batch 6: Frontend (Agent 6)

- `skills/frontend/react/SKILL.md`
- `skills/frontend/vue/SKILL.md`
- `skills/frontend/mobile-ios/SKILL.md`
- `skills/frontend/mobile-android/SKILL.md`
- `skills/frontend/mobile-react-native/SKILL.md`

### Batch 7: Data & ML (Agent 7)

- `skills/database/sql/SKILL.md`
- `skills/database/nosql/SKILL.md`
- `skills/ml-ai/model-development/SKILL.md`
- `skills/ml-ai/model-deployment/SKILL.md`
- `skills/ml-ai/mlops/SKILL.md`

### Batch 8: Compliance (Agent 8)

- `skills/compliance/fintech/SKILL.md`
- `skills/compliance/healthtech/SKILL.md`
- `skills/compliance/gdpr/SKILL.md`
- `skills/compliance/nist/SKILL.md`

---

## ✅ Validation Checklist (Use After Each Skill)

After fixing each skill, verify:

- [ ] YAML frontmatter complete with all fields
- [ ] Level 1: Quick Start (100-150 tokens)
- [ ] Level 2: Implementation (1,500-2,500 tokens)
- [ ] Level 3: Mastery (filesystem references only, <100 tokens)
- [ ] Examples section with 2-3 practical examples
- [ ] Integration Points section with related skills/systems
- [ ] Common Pitfalls section with 3-5 known issues
- [ ] Total token count < 1,500 (or content extracted to advanced/)
- [ ] All internal links work
- [ ] Code examples are syntactically correct
- [ ] NIST controls referenced where applicable

**Validation Command:**

```bash
python3 scripts/analyze-skills-compliance.py
# Check the specific skill's compliance score in the output
```

---

## 📊 Progress Tracking

Use this table to track batch completion:

| Batch | Agent | Skills Count | Status | Completion Date |
|-------|-------|--------------|--------|-----------------|
| Batch 1 | Agent 1 | 5 | ⏳ Pending | - |
| Batch 2 | Agent 2 | 4 | ⏳ Pending | - |
| Batch 3 | Agent 3 | 4 | ⏳ Pending | - |
| Batch 4 | Agent 4 | 4 | ⏳ Pending | - |
| Batch 5 | Agent 5 | 3 | ⏳ Pending | - |
| Batch 6 | Agent 6 | 5 | ⏳ Pending | - |
| Batch 7 | Agent 7 | 5 | ⏳ Pending | - |
| Batch 8 | Agent 8 | 4 | ⏳ Pending | - |

**Total:** 34 skills (covers Tier 1 + critical Tier 2 + high-priority Tier 3)

---

## 🎯 Success Criteria

### Per-Skill Success

- Compliance score: 100%
- Token budget: Within limits
- All 7 required sections present
- Validation passes

### Per-Batch Success

- All skills in batch at 100% compliance
- No broken internal links
- Cross-references verified
- Commit pushed to branch

### Overall Success

- 61/61 skills at 100% compliance
- Average compliance: 100%
- CI/CD validation passes
- Documentation complete

---

## 📚 Required Resources

### Templates

All templates available in:
`/home/william/git/standards/reports/generated/skills-compliance-report.md`

Sections: YAML Frontmatter, Level 1, Level 2, Level 3, Examples, Integration Points, Common Pitfalls

### Reference Skills

Use these as examples of good structure:

- `skills/coding-standards/python/SKILL.md` (partial but well-structured)
- `skills/security/authorization/SKILL.md` (good YAML frontmatter)

### Standards Documentation

Refer to existing standards for content:

- `/home/william/git/standards/docs/standards/`
- `/home/william/git/standards/docs/nist/`

---

## 🚀 Quick Start for Remediation Agents

1. **Claim a batch** (comment on tracking issue)
2. **Read compliance report** for templates
3. **Start with Tier 1** (quick wins)
4. **Work through batch** systematically
5. **Validate after each skill**
6. **Commit when batch complete**
7. **Move to next batch**

**Remember:** Quality over speed. 100% compliance is the goal.

---

**Document Status:** ✅ READY FOR REMEDIATION
**Last Updated:** 2025-10-24
**Total Skills:** 61
**Current Compliance:** 0%
**Target Compliance:** 100%
