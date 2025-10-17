# Agent Skills Transformation Requirements

**Document Version:** 1.0.0
**Date:** 2025-10-17
**Status:** Draft
**Owner:** Researcher Agent (swarm-1760669629248-p81glgo36)

---

## 1. Overview

This document specifies the technical and functional requirements for transforming the williamzujkowski/standards repository from its current documentation-centric architecture to Anthropic's Agent Skills format.

### 1.1 Objectives

1. Convert all standards documents into self-contained Skills
2. Implement progressive disclosure for token optimization
3. Enable autonomous skill discovery and composition
4. Maintain backward compatibility during transition
5. Enhance automation through executable resources

### 1.2 Success Criteria

- ✅ All 25+ standards converted to Skills format
- ✅ Token usage reduced by 95%+ (from baseline)
- ✅ Skill discovery accuracy >90%
- ✅ Zero breaking changes for existing users
- ✅ All automation scripts bundled and executable

---

## 2. Structural Requirements

### 2.1 Directory Structure

```
standards/
├── skills/                          # NEW: Primary skills directory
│   ├── coding-standards/
│   │   ├── python/
│   │   │   ├── SKILL.md            # Required: Skill definition
│   │   │   ├── resources/
│   │   │   │   ├── style-guide.md
│   │   │   │   ├── type-hints.md
│   │   │   │   └── async-patterns.md
│   │   │   ├── templates/
│   │   │   │   ├── pyproject.toml.template
│   │   │   │   └── pytest.ini.template
│   │   │   ├── scripts/
│   │   │   │   ├── lint.sh
│   │   │   │   └── format.sh
│   │   │   └── examples/
│   │   │       └── fastapi-api/
│   │   ├── javascript/
│   │   ├── typescript/
│   │   └── go/
│   ├── security/
│   │   ├── auth/
│   │   ├── secrets/
│   │   ├── zero-trust/
│   │   └── threat-modeling/
│   ├── testing/
│   │   ├── unit-testing/
│   │   ├── integration-testing/
│   │   └── e2e-testing/
│   ├── nist-compliance/            # Bundle existing NIST system
│   │   ├── SKILL.md
│   │   ├── controls/
│   │   ├── templates/              # Existing NIST templates
│   │   ├── scripts/                # SSP generator, validators
│   │   └── vscode-extension/       # Existing VS Code extension
│   ├── skill-loader/               # Meta-skill for discovery
│   │   └── SKILL.md
│   └── legacy-bridge/              # Backward compatibility
│       └── SKILL.md
├── docs/
│   ├── standards/                  # ARCHIVED: Original standards
│   ├── guides/
│   │   ├── SKILL_AUTHORING.md     # NEW: How to create skills
│   │   └── MIGRATION_GUIDE.md     # NEW: User transition guide
│   └── migration/                  # NEW: Transformation docs
│       ├── research-findings.md
│       ├── requirements.md         # This document
│       └── skill-mapping.yaml
├── config/
│   ├── product-matrix.yaml         # UPDATED: Reference skills
│   └── skills-catalog.yaml         # NEW: Skill inventory
├── CLAUDE.md                        # UPDATED: Reference skill-loader
└── README.md                        # UPDATED: Skills overview
```

**Requirements:**

- REQ-2.1.1: Create `skills/` directory at repository root
- REQ-2.1.2: Maintain original standards in `docs/standards/` as archived reference
- REQ-2.1.3: Create migration documentation in `docs/migration/`
- REQ-2.1.4: Update CLAUDE.md to reference skill-loader skill

---

## 3. SKILL.md Format Requirements

### 3.1 YAML Frontmatter

**Requirements:**

- REQ-3.1.1: Every skill MUST have YAML frontmatter
- REQ-3.1.2: Frontmatter MUST include `name` field (max 64 chars, lowercase-with-hyphens)
- REQ-3.1.3: Frontmatter MUST include `description` field (max 1024 chars)
- REQ-3.1.4: Description MUST specify both WHAT the skill does AND WHEN to use it
- REQ-3.1.5: No custom frontmatter fields permitted (only name and description)

**Template:**

```yaml
---
name: skill-name
description: |
  [What] Describes the core capability provided by this skill, including key techniques, frameworks, or patterns used.
  [When] Specifies clear trigger conditions: "Use when [scenario], [need], or [requirement]."
  [Why] Optional: Value proposition or expected outcome.
---
```

### 3.2 Body Structure

**Requirements:**

- REQ-3.2.1: SKILL.md body MUST follow standardized section structure
- REQ-3.2.2: Body content SHOULD target <5,000 tokens
- REQ-3.2.3: MUST include "When to Use This Skill" section with clear triggers
- REQ-3.2.4: MUST include "Core Instructions" with procedural guidance
- REQ-3.2.5: MUST include "Advanced Topics" with resource references
- REQ-3.2.6: MUST include at least 2 concrete "Examples"

**Mandatory Sections:**

1. Overview
2. When to Use This Skill
3. Core Instructions
4. Advanced Topics (with resource links)
5. Examples

**Optional Sections:**

- Prerequisites
- Common Pitfalls
- Best Practices
- Related Skills
- Troubleshooting

### 3.3 Resource References

**Requirements:**

- REQ-3.3.1: Reference external resources using relative paths
- REQ-3.3.2: Use explicit pointers: "For [topic], see `./resources/file.md`"
- REQ-3.3.3: Reference scripts as executable: "Run `./scripts/tool.sh [args]`"
- REQ-3.3.4: Link to examples: "Explore `./examples/use-case/`"
- REQ-3.3.5: Never embed full resource content in SKILL.md

---

## 4. Progressive Disclosure Requirements

### 4.1 Level 1: Metadata

**Requirements:**

- REQ-4.1.1: Frontmatter MUST be loadable in <100 tokens
- REQ-4.1.2: Description MUST enable accurate skill selection
- REQ-4.1.3: Name MUST be unique across all skills
- REQ-4.1.4: Description MUST include actionable trigger keywords

### 4.2 Level 2: Core Instructions

**Requirements:**

- REQ-4.2.1: SKILL.md body SHOULD be <5,000 tokens
- REQ-4.2.2: Content MUST provide sufficient guidance for task execution
- REQ-4.2.3: MUST avoid embedding large code blocks (use resource files)
- REQ-4.2.4: MUST avoid exhaustive detail (link to resources instead)

### 4.3 Level 3: Resources

**Requirements:**

- REQ-4.3.1: Detailed content MUST be in separate resource files
- REQ-4.3.2: Resources MUST be organized in subdirectories (resources/, scripts/, templates/, examples/)
- REQ-4.3.3: Scripts MUST be executable without modification
- REQ-4.3.4: Templates MUST include placeholder documentation
- REQ-4.3.5: No token limit for resource files (filesystem-based)

---

## 5. Skill Transformation Requirements

### 5.1 Content Conversion

**Requirements:**

- REQ-5.1.1: Extract YAML frontmatter from each standard
- REQ-5.1.2: Restructure content to follow SKILL.md template
- REQ-5.1.3: Split standards >5k tokens into multiple related skills
- REQ-5.1.4: Move detailed sections to resource files
- REQ-5.1.5: Convert automation instructions to executable scripts

### 5.2 Resource Bundling

**Requirements:**

- REQ-5.2.1: Bundle related templates into skill's templates/ directory
- REQ-5.2.2: Bundle related scripts into skill's scripts/ directory
- REQ-5.2.3: Bundle reference materials into skill's resources/ directory
- REQ-5.2.4: Bundle examples into skill's examples/ directory
- REQ-5.2.5: Ensure all bundled resources are referenced in SKILL.md

### 5.3 Automation Scripts

**Requirements:**

- REQ-5.3.1: All scripts MUST be executable (chmod +x)
- REQ-5.3.2: Scripts MUST include shebang line (#!/bin/bash or #!/usr/bin/env python3)
- REQ-5.3.3: Scripts MUST use only pre-installed dependencies
- REQ-5.3.4: Scripts MUST accept command-line arguments as documented
- REQ-5.3.5: Scripts MUST output structured results (JSON preferred)
- REQ-5.3.6: Scripts MUST have error handling with exit codes

---

## 6. Skill Discovery Requirements

### 6.1 Skill Loader Meta-Skill

**Requirements:**

- REQ-6.1.1: Create skill-loader/ skill for intelligent discovery
- REQ-6.1.2: Implement @load pattern compatibility
- REQ-6.1.3: Support product-matrix.yaml integration
- REQ-6.1.4: Enable multi-skill composition
- REQ-6.1.5: Provide skill search and filtering

**Functionality:**

```markdown
@load product:api              # Discovers and loads API-related skills
@load security:*              # Discovers and loads all security skills
@load python + testing        # Composes Python and testing skills
```

### 6.2 Skills Catalog

**Requirements:**

- REQ-6.2.1: Create config/skills-catalog.yaml with complete skill inventory
- REQ-6.2.2: Include skill dependencies and relationships
- REQ-6.2.3: Map skills to product types
- REQ-6.2.4: Define skill composition patterns
- REQ-6.2.5: Version each skill independently

**Catalog Schema:**

```yaml
skills:
  - name: python
    path: skills/coding-standards/python
    category: coding
    tags: [language, backend, scripting]
    dependencies: []
    related: [python-testing, python-security]
    product_types: [api, cli, ml-service]
    version: 1.0.0
```

---

## 7. Backward Compatibility Requirements

### 7.1 Legacy Bridge Skill

**Requirements:**

- REQ-7.1.1: Create legacy-bridge/ skill for old @load pattern support
- REQ-7.1.2: Map old standard names to new skill names
- REQ-7.1.3: Provide deprecation warnings with migration paths
- REQ-7.1.4: Support gradual transition (both systems work in parallel)
- REQ-7.1.5: Maintain original file structure in docs/standards/ as archive

**Mapping Logic:**

```yaml
legacy_mappings:
  CODING_STANDARDS.md: [python, javascript, typescript, go]
  MODERN_SECURITY_STANDARDS.md: [security-auth, zero-trust, threat-modeling]
  TESTING_STANDARDS.md: [unit-testing, integration-testing, e2e-testing]
```

### 7.2 Product Matrix Updates

**Requirements:**

- REQ-7.2.1: Update product-matrix.yaml to reference skills instead of standards
- REQ-7.2.2: Maintain existing product type definitions
- REQ-7.2.3: Support wildcard expansion to skills
- REQ-7.2.4: Preserve language and framework mappings
- REQ-7.2.5: Add skill composition examples

---

## 8. Token Optimization Requirements

### 8.1 Measurement and Targets

**Requirements:**

- REQ-8.1.1: Establish baseline token usage for current system
- REQ-8.1.2: Measure token usage for each skill (Level 1, 2, 3 separately)
- REQ-8.1.3: Target 95%+ reduction from baseline (current: 90%)
- REQ-8.1.4: Monitor token usage in production workflows
- REQ-8.1.5: Optimize skills exceeding token targets

### 8.2 Optimization Strategies

**Requirements:**

- REQ-8.2.1: Extract code blocks to resource files
- REQ-8.2.2: Convert inline examples to separate files
- REQ-8.2.3: Use script execution instead of inline commands
- REQ-8.2.4: Implement caching for frequently used skills
- REQ-8.2.5: Minimize repetition across skills (use skill composition)

---

## 9. Testing and Validation Requirements

### 9.1 Skill Validation

**Requirements:**

- REQ-9.1.1: Validate YAML frontmatter syntax and constraints
- REQ-9.1.2: Verify all resource references are valid paths
- REQ-9.1.3: Check token counts for SKILL.md bodies
- REQ-9.1.4: Test script executability
- REQ-9.1.5: Validate template placeholders

**Validation Script:**

```bash
./scripts/validate-skill.sh skills/python/
# Checks:
# - YAML frontmatter valid
# - name ≤64 chars, lowercase-with-hyphens
# - description ≤1024 chars, includes "when"
# - All referenced files exist
# - Scripts are executable
# - Token count <5000 for SKILL.md
```

### 9.2 Integration Testing

**Requirements:**

- REQ-9.2.1: Test skill discovery for each product type
- REQ-9.2.2: Test multi-skill composition scenarios
- REQ-9.2.3: Test backward compatibility with legacy @load patterns
- REQ-9.2.4: Test script execution within skills
- REQ-9.2.5: Test skill loader with product-matrix integration

### 9.3 Performance Testing

**Requirements:**

- REQ-9.3.1: Measure skill load time (<500ms target)
- REQ-9.3.2: Measure discovery accuracy (>90% target)
- REQ-9.3.3: Measure token reduction (95%+ target)
- REQ-9.3.4: Measure composition success rate (>85% target)
- REQ-9.3.5: Benchmark against current system

---

## 10. Documentation Requirements

### 10.1 User Documentation

**Requirements:**

- REQ-10.1.1: Create SKILL_AUTHORING.md guide for contributors
- REQ-10.1.2: Create MIGRATION_GUIDE.md for existing users
- REQ-10.1.3: Update README.md with skills overview
- REQ-10.1.4: Update CLAUDE.md to reference skill-loader
- REQ-10.1.5: Create skill usage examples for each product type

### 10.2 Technical Documentation

**Requirements:**

- REQ-10.2.1: Document skill directory structure
- REQ-10.2.2: Document SKILL.md template and requirements
- REQ-10.2.3: Document progressive disclosure implementation
- REQ-10.2.4: Document skill discovery algorithm
- REQ-10.2.5: Document token optimization strategies

### 10.3 API Documentation

**Requirements:**

- REQ-10.3.1: Document skill-loader API and @load syntax
- REQ-10.3.2: Document skills-catalog.yaml schema
- REQ-10.3.3: Document script execution conventions
- REQ-10.3.4: Document template placeholder syntax
- REQ-10.3.5: Document skill composition patterns

---

## 11. Migration Process Requirements

### 11.1 Phase 1: Foundation

**Requirements:**

- REQ-11.1.1: Create skills/ directory structure
- REQ-11.1.2: Convert top 5 most-used standards to skills
- REQ-11.1.3: Implement skill-loader meta-skill
- REQ-11.1.4: Validate progressive disclosure pattern
- REQ-11.1.5: Establish testing framework

**Deliverables:**

- skills/ directory with 5 complete skills
- skill-loader/ meta-skill functional
- Validation scripts operational
- Initial token metrics collected

### 11.2 Phase 2: Core Conversion

**Requirements:**

- REQ-11.2.1: Convert all remaining standards to skills
- REQ-11.2.2: Split large standards into focused sub-skills
- REQ-11.2.3: Bundle templates and scripts into skill directories
- REQ-11.2.4: Create skill composition examples
- REQ-11.2.5: Validate token optimization targets

**Deliverables:**

- All 25+ skills converted and validated
- Skills catalog complete
- Token usage <5% of baseline
- Composition patterns documented

### 11.3 Phase 3: Enhancement

**Requirements:**

- REQ-11.3.1: Add executable automation scripts to skills
- REQ-11.3.2: Create advanced reference materials
- REQ-11.3.3: Build comprehensive skill testing framework
- REQ-11.3.4: Document skill authoring guidelines
- REQ-11.3.5: Create contribution templates

**Deliverables:**

- All skills have automation scripts
- SKILL_AUTHORING.md complete
- Test coverage >90%
- Contribution workflow established

### 11.4 Phase 4: Transition

**Requirements:**

- REQ-11.4.1: Update product-matrix.yaml for skill references
- REQ-11.4.2: Create comprehensive migration guide
- REQ-11.4.3: Establish backward compatibility layer
- REQ-11.4.4: Communicate deprecation timeline
- REQ-11.4.5: Provide automated migration tools

**Deliverables:**

- MIGRATION_GUIDE.md complete
- legacy-bridge/ skill functional
- Deprecation timeline published
- Migration scripts available

### 11.5 Phase 5: Optimization

**Requirements:**

- REQ-11.5.1: Conduct token usage analysis
- REQ-11.5.2: Refine skill composition patterns
- REQ-11.5.3: Integrate user feedback
- REQ-11.5.4: Perform performance benchmarking
- REQ-11.5.5: Continuous improvement cycle

**Deliverables:**

- Performance benchmark report
- User satisfaction survey results
- Optimization recommendations
- Continuous improvement plan

---

## 12. Quality Assurance Requirements

### 12.1 Acceptance Criteria

**Functional:**

- ✅ All standards converted to skills without data loss
- ✅ Skill discovery working for all product types
- ✅ Multi-skill composition functional
- ✅ Backward compatibility maintained
- ✅ All automation scripts executable

**Performance:**

- ✅ Token usage reduced by 95%+
- ✅ Skill load time <500ms
- ✅ Discovery accuracy >90%
- ✅ Composition success >85%

**Quality:**

- ✅ All skills pass validation
- ✅ Test coverage >90%
- ✅ Documentation complete
- ✅ Zero breaking changes
- ✅ User satisfaction >4.5/5

### 12.2 Validation Checklist

**Per Skill:**

- [ ] YAML frontmatter valid and complete
- [ ] Description includes "when to use"
- [ ] Token count <5,000 for SKILL.md
- [ ] All resource references valid
- [ ] Scripts executable and tested
- [ ] Examples functional
- [ ] Documentation complete

**Repository-Wide:**

- [ ] Skills catalog accurate
- [ ] Product matrix updated
- [ ] Legacy mappings functional
- [ ] Migration guide complete
- [ ] Validation scripts pass
- [ ] Performance targets met

---

## 13. Risk Management

### 13.1 Technical Risks

**Risk:** Skills exceed 5k token target

- **Impact:** High (degrades performance)
- **Mitigation:** Automated token counting, aggressive resource externalization
- **Contingency:** Split into sub-skills

**Risk:** Script dependencies unavailable

- **Impact:** Medium (limits automation)
- **Mitigation:** Document required packages, use only pre-installed dependencies
- **Contingency:** Alternative script implementations

**Risk:** Skill discovery accuracy below target

- **Impact:** High (poor UX)
- **Mitigation:** High-quality descriptions, extensive testing
- **Contingency:** Manual skill selection fallback

### 13.2 Process Risks

**Risk:** Migration timeline overruns

- **Impact:** Medium (delays adoption)
- **Mitigation:** Phased approach, clear milestones
- **Contingency:** Prioritize most-used skills

**Risk:** User adoption resistance

- **Impact:** Medium (low utilization)
- **Mitigation:** Comprehensive migration guide, parallel systems
- **Contingency:** Extended backward compatibility period

**Risk:** Breaking changes introduced

- **Impact:** High (disrupts users)
- **Mitigation:** Extensive testing, legacy bridge, gradual rollout
- **Contingency:** Rollback capability, hotfix process

---

## 14. Compliance and Standards

### 14.1 Anthropic Requirements

- Comply with official Skills specification
- Follow SKILL.md frontmatter constraints (name, description only)
- Implement progressive disclosure as specified
- Use supported file formats and structures

### 14.2 Repository Standards

- Maintain existing code quality standards
- Follow git workflow and branch policies
- Use semantic versioning for skills
- Document all changes in CHANGELOG.md

### 14.3 Open Source Compliance

- Maintain MIT license
- Document all dependencies
- Provide clear contribution guidelines
- Respect existing repository governance

---

## 15. Appendix

### 15.1 Skill Categories

1. **Coding Standards:** Language-specific development practices
2. **Security:** Authentication, authorization, secrets management, threat modeling
3. **Testing:** Unit, integration, E2E, performance, security testing
4. **DevOps:** CI/CD, infrastructure, deployment, monitoring
5. **Cloud Native:** Kubernetes, containers, serverless, microservices
6. **Frontend:** React, Vue, Angular, mobile, accessibility
7. **Data Engineering:** Pipelines, orchestration, quality, storage
8. **ML/AI:** Model development, training, inference, monitoring
9. **Compliance:** NIST, legal, audit, governance
10. **Content:** Documentation, SEO, marketing, knowledge management

### 15.2 Transformation Priorities

**High Priority (Convert First):**

1. CODING_STANDARDS.md → Language-specific skills
2. MODERN_SECURITY_STANDARDS.md → Security skills
3. TESTING_STANDARDS.md → Testing skills
4. NIST system → nist-compliance skill
5. CLAUDE.md → skill-loader skill

**Medium Priority:**
6. DEVOPS_PLATFORM_STANDARDS.md
7. CLOUD_NATIVE_STANDARDS.md
8. FRONTEND_MOBILE_STANDARDS.md
9. DATA_ENGINEERING_STANDARDS.md
10. ML_AI_STANDARDS.md

**Lower Priority:**
11. OBSERVABILITY_STANDARDS.md
12. MICROSERVICES_STANDARDS.md
13. DATABASE_STANDARDS.md
14. EVENT_DRIVEN_STANDARDS.md
15. Remaining specialized standards

### 15.3 Token Optimization Reference

**Current System:**

- Baseline: 100,000 tokens (all standards loaded)
- Optimized: 10,000 tokens (CLAUDE.md @load system)
- Reduction: 90%

**Target System:**

- Level 1: 2,500 tokens (all skill metadata)
- Level 2: 5,000 tokens average (2-3 skills loaded)
- Level 3: Unlimited (filesystem-based)
- Target Reduction: 95%+

---

**Document Status:** Ready for review by planner agent
**Next Steps:** Create skill-mapping.yaml and begin Phase 1 transformation
