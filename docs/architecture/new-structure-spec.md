# Repository Structure Redesign Specification

**Version:** 2.0.0
**Status:** Architecture Design Phase
**Author:** System Architect Agent
**Date:** 2025-10-24
**Repository:** https://github.com/williamzujkowski/standards

---

## Executive Summary

This specification defines the complete architectural transformation of the standards repository to align with Anthropic's agent skills standards. The redesign focuses on LLM optimization, progressive disclosure, token efficiency, and maintainability while preserving existing valuable content.

**Key Metrics:**

- Current Skills: 416 files across 22 categories
- Current Agents: 65 agent specifications
- Current Docs: 101 markdown files
- Target: Anthropic-aligned, token-optimized structure with metadata-driven discovery

---

## Table of Contents

1. [Current State Analysis](#1-current-state-analysis)
2. [Target Architecture](#2-target-architecture)
3. [Migration Strategy](#3-migration-strategy)
4. [Implementation Phases](#4-implementation-phases)
5. [Anthropic Alignment](#5-anthropic-alignment)

---

## 1. Current State Analysis

### 1.1 Existing Directory Inventory

#### Skills Directory (`skills/`)

**Total Files:** 416 files
**Categories:** 22 domain areas
**Current Structure:**

```
skills/
├── README.md (status: good - documents 50 skills)
├── api/graphql
├── architecture/patterns
├── cloud-native/ (6 subdirs)
├── coding-standards/ (9 subdirs + SKILL.md ✓)
├── compliance/ (4 subdirs)
├── content/documentation
├── data-engineering/ (2 subdirs)
├── database/ (3 subdirs)
├── design/ux
├── devops/ (5 subdirs)
├── frontend/ (4 subdirs)
├── legacy-bridge/
├── microservices/patterns
├── ml-ai/ (various)
├── nist-compliance/
├── observability/ (various)
├── security/ (10 subdirs)
├── security-practices/
├── skill-loader/ (meta-skill)
└── testing/ (6 subdirs)
```

**Quality Assessment:**

- ✅ Good: coding-standards/SKILL.md follows Anthropic format with Level 1/2/3 structure
- ✅ Good: README.md documents skill inventory
- ❌ Inconsistent: Most skills lack SKILL.md files
- ❌ Missing: Metadata registry (metadata.json)
- ⚠️ Mixed: Some directories have templates/, scripts/, resources/

**Preservation Decision:**

- **PRESERVE:** All skill content (migrate to consistent structure)
- **ENHANCE:** Add missing SKILL.md files
- **ADD:** Create metadata.json registry

#### Agents Directory (`.claude/agents/`)

**Total Files:** 65 agent specifications
**Current Structure:**

```
.claude/agents/
├── README.md
├── MIGRATION_SUMMARY.md
├── analysis/ (2 specs)
├── architecture/system-design
├── base-template-generator.md
├── consensus/ (8 specs)
├── core/ (5 specs: coder, planner, researcher, reviewer, tester)
├── data/ml
├── development/backend
├── devops/ci-cd
├── documentation/api-docs
├── github/ (13 specs)
├── hive-mind/ (3 specs)
├── optimization/ (6 specs)
├── sparc/ (4 specs)
├── specialized/mobile
├── swarm/ (4 specs)
├── templates/ (9 templates)
└── testing/ (2 subdirs)
```

**Quality Assessment:**

- ✅ Excellent: Core agents (coder, tester, etc.) have full YAML frontmatter + markdown
- ✅ Good: Consistent structure across agent specs
- ✅ Good: Templates directory exists
- ❌ Missing: Centralized registry.json
- ⚠️ Location: Hidden in `.claude/` (not discoverable)

**Preservation Decision:**

- **PRESERVE:** All agent specifications
- **RELOCATE:** Move from `.claude/agents/` to top-level `agents/`
- **ADD:** Create registry.json with searchable metadata

#### Documentation Directory (`docs/`)

**Total Files:** 101 markdown files
**Current Structure:**

```
docs/
├── api/
├── core/
├── guides/
├── migration/ (phase2/, extension/)
├── nist/
├── reports/
└── standards/ (25 standard documents)
```

**Quality Assessment:**

- ✅ Good: Standards documents are comprehensive
- ✅ Good: Migration documentation is detailed
- ⚠️ Mixed: Some duplication between docs/ and skills/
- ❌ Issue: Audit found documentation accuracy issues (48.75% score)

**Preservation Decision:**

- **PRESERVE:** All standards documents
- **REORGANIZE:** Create clearer hierarchy
- **FIX:** Address accuracy issues identified in audit

#### Configuration Directory (`config/`)

**Files:**

- `product-matrix.yaml` (7.5K) - Product to standards mapping ✅
- `audit-rules.yaml` (4.1K) - Structure validation rules ✅
- `standards-api.json` (9.4K) - API definitions ✅
- `standards-schema.yaml` (5.6K) - Data schemas ✅
- `MANIFEST.yaml` (31K) - Full manifest ✅
- `TOOLS_CATALOG.yaml` (9.1K) - Tool catalog ✅

**Preservation Decision:** **PRESERVE ALL** - All config files are functional

### 1.2 Content Categorization

| Category | Current Location | File Count | Quality | Migrate To |
|----------|------------------|------------|---------|------------|
| Skills (Meta) | skills/skill-loader/ | ~10 | Good | skills/core/ |
| Skills (Domain) | skills/*/ | ~400 | Mixed | skills/specialized/ |
| Agent Specs | .claude/agents/ | 65 | Excellent | agents/specifications/ |
| Agent Templates | .claude/agents/templates/ | 9 | Good | agents/templates/ |
| Standards Docs | docs/standards/ | 25 | Good | docs/standards/ |
| Guides | docs/guides/ | ~15 | Mixed | docs/guides/ |
| Config Files | config/ | 6 | Excellent | config/ |
| Examples | examples/ | ~30 | Good | examples/ |

### 1.3 Preservation vs. Migration Decisions

#### PRESERVE AS-IS (No Migration)

1. `config/*.yaml` - All configuration files
2. `docs/standards/*.md` - Standard documents (fix accuracy only)
3. `examples/` - All example templates
4. `.github/workflows/` - CI/CD pipelines
5. `scripts/` - Audit and utility scripts

#### MIGRATE WITH RESTRUCTURE

1. **skills/** → Add consistent SKILL.md to all categories
2. **.claude/agents/** → Move to `agents/` (remove hidden prefix)
3. **docs/guides/** → Consolidate and fix command syntax errors
4. **docs/migration/** → ✅ Archived to archive/old-migrations/migration/

#### ADD NEW STRUCTURE

1. **skills/metadata.json** - Searchable skill registry
2. **agents/registry.json** - Agent capability index
3. **agents/workflows/** - Orchestration patterns
4. **docs/api/** - API reference documentation

#### REMOVE/ARCHIVE

1. Old audit reports (>30 days) → reports/archive/
2. Duplicate documentation → Consolidate
3. Non-functional examples → Fix or remove

### 1.4 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking existing workflows | High | High | Create compatibility layer for 6 months |
| Content loss during migration | Medium | Critical | Git branch + automated backups |
| Token count increase | Low | Medium | Strict metadata limits + validation |
| User confusion | High | Medium | Clear migration guide + gradual rollout |
| Incomplete migration | Medium | High | Phased approach with validation gates |

---

## 2. Target Architecture

### 2.1 Complete Directory Tree

```
standards/                                    # Root
│
├── skills/                                   # Anthropic-aligned skills (50+)
│   ├── metadata.json                         # Searchable skill registry ⭐ NEW
│   ├── README.md                             # Skill system overview
│   │
│   ├── core/                                 # Essential meta-skills (2)
│   │   ├── skill-loader/                     # Progressive loading skill
│   │   │   ├── SKILL.md                      # 3-level disclosure
│   │   │   ├── templates/skill-template.md
│   │   │   └── scripts/loader.py
│   │   └── legacy-bridge/                    # Backward compatibility
│   │       └── SKILL.md
│   │
│   └── specialized/                          # Domain-specific skills (48)
│       ├── coding-standards/                 # Language standards
│       │   ├── SKILL.md                      # Hub skill
│       │   ├── python/
│       │   │   ├── SKILL.md                  # Level 1/2/3
│       │   │   ├── templates/               # FastAPI, pytest templates
│       │   │   ├── scripts/                 # Linters, formatters
│       │   │   └── resources/               # PEP references
│       │   ├── javascript/
│       │   ├── typescript/
│       │   ├── go/
│       │   └── rust/
│       │
│       ├── security/                         # Security practices
│       │   ├── SKILL.md                      # Hub skill
│       │   ├── authentication/
│       │   │   └── SKILL.md
│       │   ├── secrets-management/
│       │   ├── zero-trust/
│       │   ├── threat-modeling/
│       │   └── input-validation/
│       │
│       ├── testing/                          # Testing standards
│       │   ├── SKILL.md                      # Hub skill
│       │   ├── unit-testing/
│       │   ├── integration-testing/
│       │   ├── e2e-testing/
│       │   └── performance-testing/
│       │
│       ├── devops/                           # DevOps practices
│       │   ├── ci-cd/
│       │   ├── infrastructure/
│       │   └── monitoring/
│       │
│       ├── cloud-native/                     # Cloud-native patterns
│       │   ├── kubernetes/
│       │   ├── containers/
│       │   └── serverless/
│       │
│       ├── frontend/                         # Frontend development
│       │   ├── react/
│       │   ├── vue/
│       │   ├── mobile-ios/
│       │   └── mobile-android/
│       │
│       ├── data-engineering/                 # Data pipelines
│       │   ├── orchestration/
│       │   └── data-quality/
│       │
│       ├── ml-ai/                            # ML/AI standards
│       │   ├── model-development/
│       │   └── model-deployment/
│       │
│       ├── observability/                    # Monitoring & logging
│       │   ├── logging/
│       │   └── metrics/
│       │
│       ├── microservices/                    # Microservices patterns
│       │   └── patterns/
│       │
│       ├── database/                         # Database standards
│       │   ├── sql/
│       │   └── nosql/
│       │
│       ├── architecture/                     # System design
│       │   └── patterns/
│       │
│       ├── compliance/                       # Regulatory compliance
│       │   ├── nist/
│       │   └── gdpr/
│       │
│       ├── design/                           # UX/UI standards
│       │   └── ux/
│       │
│       └── content/                          # Documentation standards
│           └── documentation/
│
├── agents/                                   # Agent configurations ⭐ MOVED
│   ├── registry.json                         # Agent capability index ⭐ NEW
│   ├── README.md                             # Agent system overview
│   │
│   ├── specifications/                       # Agent definitions
│   │   ├── core/                             # Essential agents
│   │   │   ├── coder.md                      # Implementation specialist
│   │   │   ├── researcher.md                 # Context gathering
│   │   │   ├── planner.md                    # Task orchestration
│   │   │   ├── tester.md                     # Quality assurance
│   │   │   └── reviewer.md                   # Code review
│   │   │
│   │   ├── specialized/                      # Domain experts
│   │   │   ├── backend-dev.md
│   │   │   ├── mobile-dev.md
│   │   │   ├── ml-developer.md
│   │   │   └── cicd-engineer.md
│   │   │
│   │   ├── coordination/                     # Swarm coordinators
│   │   │   ├── hierarchical-coordinator.md
│   │   │   ├── mesh-coordinator.md
│   │   │   ├── adaptive-coordinator.md
│   │   │   └── swarm-init.md
│   │   │
│   │   ├── github/                           # GitHub integration
│   │   │   ├── pr-manager.md
│   │   │   ├── issue-tracker.md
│   │   │   ├── release-manager.md
│   │   │   └── code-review-swarm.md
│   │   │
│   │   ├── consensus/                        # Distributed consensus
│   │   │   ├── raft-manager.md
│   │   │   ├── byzantine-coordinator.md
│   │   │   └── quorum-manager.md
│   │   │
│   │   ├── optimization/                     # Performance agents
│   │   │   ├── perf-analyzer.md
│   │   │   ├── load-balancer.md
│   │   │   └── resource-allocator.md
│   │   │
│   │   └── sparc/                            # SPARC methodology
│   │       ├── specification.md
│   │       ├── pseudocode.md
│   │       ├── architecture.md
│   │       └── refinement.md
│   │
│   ├── workflows/                            # Orchestration patterns ⭐ NEW
│   │   ├── tdd-workflow.yaml                 # Test-driven development
│   │   ├── feature-development.yaml          # Feature implementation
│   │   ├── bug-fix-workflow.yaml             # Bug remediation
│   │   ├── refactoring-workflow.yaml         # Code refactoring
│   │   └── documentation-workflow.yaml       # Doc generation
│   │
│   └── templates/                            # Agent templates
│       ├── base-agent-template.md
│       ├── coordinator-template.md
│       ├── specialist-template.md
│       └── workflow-template.yaml
│
├── docs/                                     # Documentation
│   ├── README.md                             # Documentation hub
│   │
│   ├── skills/                               # Skills documentation ⭐ NEW
│   │   ├── authoring-guide.md                # How to write skills
│   │   ├── metadata-schema.md                # Metadata format
│   │   ├── progressive-disclosure.md         # Level 1/2/3 design
│   │   └── token-optimization.md             # Token efficiency guide
│   │
│   ├── agents/                               # Agents documentation ⭐ NEW
│   │   ├── agent-development-guide.md        # Creating agents
│   │   ├── workflow-design.md                # Orchestration patterns
│   │   ├── coordination-protocols.md         # Swarm communication
│   │   └── capability-matrix.md              # Agent capabilities
│   │
│   ├── standards/                            # Standards library (KEEP)
│   │   ├── README.md
│   │   ├── UNIFIED_STANDARDS.md
│   │   ├── CODING_STANDARDS.md
│   │   ├── SECURITY_STANDARDS.md
│   │   └── ... (22 more standards)
│   │
│   ├── guides/                               # User guides (FIX SYNTAX)
│   │   ├── KICKSTART_PROMPT.md               # Quick start
│   │   ├── SKILLS_QUICK_START.md             # Skills loading
│   │   ├── SKILLS_USER_GUIDE.md              # Detailed guide
│   │   └── STANDARDS_INDEX.md                # Standards navigation
│   │
│   ├── core/                                 # Core documentation (KEEP)
│   │   ├── README.md
│   │   ├── CONTRIBUTING.md
│   │   └── ARCHITECTURE.md
│   │
│   ├── api/                                  # API reference ⭐ NEW
│   │   ├── skill-loader-api.md               # Skill loading API
│   │   ├── agent-registry-api.md             # Agent registry API
│   │   └── product-matrix-api.md             # Product matrix API
│   │
│   ├── nist/                                 # NIST compliance (KEEP)
│   │   └── ...
│   │
│   └── archive/                              # Archived content ⭐ NEW
│       └── migration/                        # Old migration docs
│
├── config/                                   # Configuration (KEEP AS-IS)
│   ├── product-matrix.yaml                   # Product definitions ✅
│   ├── audit-rules.yaml                      # Validation rules ✅
│   ├── standards-api.json                    # API definitions ✅
│   ├── standards-schema.yaml                 # Data schemas ✅
│   ├── MANIFEST.yaml                         # Full manifest ✅
│   └── TOOLS_CATALOG.yaml                    # Tool catalog ✅
│
├── examples/                                 # Example implementations (KEEP)
│   ├── nist-templates/
│   ├── project-templates/
│   └── ai-generation-hints/
│
├── scripts/                                  # Utility scripts (KEEP)
│   ├── skill-loader.py                       # Skill loading ✅
│   ├── generate-audit-reports.py             # Audit tools ✅
│   ├── validate-skills.py                    # Validation ✅
│   └── ensure-hub-links.py                   # Link checking ✅
│
├── reports/                                  # Generated reports
│   ├── README.md
│   ├── generated/                            # Current reports
│   └── archive/                              # Old reports (>30 days)
│
├── .github/                                  # GitHub configuration (KEEP)
│   └── workflows/
│       └── lint-and-validate.yml             # CI/CD ✅
│
├── CLAUDE.md                                 # Router configuration (FIX)
├── README.md                                 # Repository overview (FIX)
├── CHANGELOG.md                              # Change history
└── LICENSE                                   # MIT license
```

### 2.2 Metadata Schema Designs

#### Skills Metadata Registry (`skills/metadata.json`)

```json
{
  "version": "2.0.0",
  "generated": "2025-10-24T19:30:00Z",
  "total_skills": 50,
  "categories": {
    "core": 2,
    "specialized": 48
  },

  "skills": [
    {
      "id": "coding-standards-python",
      "name": "Python Coding Standards",
      "category": "specialized/coding-standards",
      "path": "skills/specialized/coding-standards/python/SKILL.md",
      "description": "PEP 8 compliant Python development standards with type hints and modern tooling",

      "capabilities": [
        "code_generation",
        "linting",
        "formatting",
        "type_checking"
      ],

      "dependencies": [
        "coding-standards",
        "testing-unit"
      ],

      "related_standards": [
        "docs/standards/CODING_STANDARDS.md"
      ],

      "token_cost": {
        "level_1": 120,
        "level_2": 1850,
        "level_3": 0,
        "metadata_only": 85
      },

      "tags": [
        "python",
        "linting",
        "formatting",
        "pep8",
        "type-hints"
      ],

      "version": "1.2.0",
      "last_updated": "2025-10-15",
      "status": "stable",

      "examples": [
        "skills/specialized/coding-standards/python/templates/fastapi-project.py",
        "skills/specialized/coding-standards/python/templates/pytest-fixture.py"
      ],

      "scripts": [
        "skills/specialized/coding-standards/python/scripts/setup-linters.sh"
      ]
    },

    {
      "id": "security-authentication",
      "name": "Authentication & Authorization",
      "category": "specialized/security",
      "path": "skills/specialized/security/authentication/SKILL.md",
      "description": "OAuth 2.0, JWT, RBAC, and zero-trust authentication patterns",

      "capabilities": [
        "oauth_implementation",
        "jwt_handling",
        "rbac_design",
        "session_management"
      ],

      "dependencies": [
        "security",
        "coding-standards"
      ],

      "related_standards": [
        "docs/standards/MODERN_SECURITY_STANDARDS.md",
        "docs/nist/AC-controls.md"
      ],

      "token_cost": {
        "level_1": 150,
        "level_2": 2400,
        "level_3": 0,
        "metadata_only": 95
      },

      "tags": [
        "security",
        "authentication",
        "oauth",
        "jwt",
        "rbac",
        "nist-ac"
      ],

      "version": "1.5.0",
      "last_updated": "2025-10-20",
      "status": "stable",

      "nist_controls": ["AC-2", "AC-3", "AC-6", "IA-2"],

      "examples": [
        "skills/specialized/security/authentication/templates/oauth-server.ts",
        "skills/specialized/security/authentication/templates/jwt-middleware.ts"
      ]
    }
  ],

  "categories_detail": {
    "core": {
      "description": "Essential meta-skills for system operation",
      "skills": ["skill-loader", "legacy-bridge"]
    },
    "specialized": {
      "description": "Domain-specific implementation skills",
      "subcategories": {
        "coding-standards": {
          "count": 5,
          "languages": ["python", "javascript", "typescript", "go", "rust"]
        },
        "security": {
          "count": 5,
          "areas": ["authentication", "secrets", "zero-trust", "threat-modeling", "validation"]
        },
        "testing": {
          "count": 4,
          "types": ["unit", "integration", "e2e", "performance"]
        }
      }
    }
  },

  "indexes": {
    "by_capability": {
      "code_generation": ["coding-standards-python", "coding-standards-typescript"],
      "oauth_implementation": ["security-authentication"],
      "test_generation": ["testing-unit", "testing-integration"]
    },

    "by_tag": {
      "python": ["coding-standards-python", "testing-pytest"],
      "security": ["security-authentication", "security-secrets"],
      "nist": ["security-authentication", "compliance-nist"]
    },

    "by_nist_control": {
      "AC-2": ["security-authentication"],
      "AC-3": ["security-authentication"],
      "SI-10": ["coding-standards", "security-validation"]
    }
  }
}
```

**Token Cost Strategy:**

- **metadata_only**: Just ID, name, description, capabilities (~85 tokens)
- **level_1**: Add quick start, checklist (~120 tokens)
- **level_2**: Full implementation guide (~2000 tokens)
- **level_3**: Load external resources on-demand (0 tokens, filesystem access)

#### Agents Registry (`agents/registry.json`)

```json
{
  "version": "2.0.0",
  "generated": "2025-10-24T19:30:00Z",
  "total_agents": 49,

  "agents": [
    {
      "id": "coder",
      "name": "Code Implementation Agent",
      "type": "developer",
      "category": "core",
      "path": "agents/specifications/core/coder.md",
      "description": "Implementation specialist for writing clean, efficient code",

      "capabilities": [
        "code_generation",
        "refactoring",
        "optimization",
        "api_design",
        "error_handling"
      ],

      "required_skills": [
        "coding-standards-*",
        "testing-unit"
      ],

      "optional_skills": [
        "security-*",
        "devops-ci-cd"
      ],

      "collaboration": {
        "reports_to": ["planner"],
        "coordinates_with": ["researcher", "tester"],
        "delegates_to": ["reviewer"]
      },

      "workflows": [
        "agents/workflows/tdd-workflow.yaml",
        "agents/workflows/feature-development.yaml"
      ],

      "priority": "high",
      "concurrency_safe": true,

      "hooks": {
        "pre": "Check for existing tests",
        "post": "Run linter validation"
      },

      "token_cost": 450,
      "color": "#FF6B35",
      "version": "1.3.0"
    },

    {
      "id": "hierarchical-coordinator",
      "name": "Hierarchical Swarm Coordinator",
      "type": "coordinator",
      "category": "coordination",
      "path": "agents/specifications/coordination/hierarchical-coordinator.md",
      "description": "Manages hierarchical task delegation with clear chains of command",

      "capabilities": [
        "task_decomposition",
        "agent_orchestration",
        "dependency_resolution",
        "priority_management"
      ],

      "coordination_pattern": "hierarchical",
      "max_agents": 8,
      "topology": "tree",

      "delegates_to": [
        "coder",
        "tester",
        "researcher",
        "reviewer"
      ],

      "workflows": [
        "agents/workflows/feature-development.yaml",
        "agents/workflows/refactoring-workflow.yaml"
      ],

      "priority": "critical",
      "token_cost": 680,
      "color": "#4ECDC4",
      "version": "1.1.0"
    }
  ],

  "indexes": {
    "by_capability": {
      "code_generation": ["coder", "sparc-coder"],
      "task_orchestration": ["hierarchical-coordinator", "mesh-coordinator"],
      "github_integration": ["pr-manager", "issue-tracker"]
    },

    "by_type": {
      "developer": ["coder", "backend-dev", "mobile-dev"],
      "coordinator": ["hierarchical-coordinator", "mesh-coordinator"],
      "specialist": ["ml-developer", "cicd-engineer"]
    },

    "by_workflow": {
      "tdd-workflow": ["coder", "tester", "reviewer"],
      "feature-development": ["planner", "coder", "tester"],
      "bug-fix": ["researcher", "coder", "tester"]
    }
  },

  "workflows_catalog": [
    {
      "id": "tdd-workflow",
      "name": "Test-Driven Development",
      "path": "agents/workflows/tdd-workflow.yaml",
      "agents_required": ["tester", "coder", "reviewer"],
      "phases": ["test-first", "implement", "refactor", "validate"]
    },
    {
      "id": "feature-development",
      "name": "Full Feature Development",
      "path": "agents/workflows/feature-development.yaml",
      "agents_required": ["planner", "researcher", "coder", "tester"],
      "phases": ["research", "design", "implement", "test", "document"]
    }
  ]
}
```

### 2.3 File Naming Conventions

#### Skill Files

- **Skill Definition:** `SKILL.md` (uppercase, mandatory in every skill directory)
- **Templates:** `{purpose}-template.{ext}` (e.g., `fastapi-project-template.py`)
- **Scripts:** `{action}.{ext}` (e.g., `setup-linters.sh`, `validate.py`)
- **Resources:** `{topic}.md` (e.g., `pep8-reference.md`)

#### Agent Files

- **Agent Specification:** `{agent-name}.md` (kebab-case, e.g., `hierarchical-coordinator.md`)
- **Workflow Definition:** `{workflow-name}-workflow.yaml` (e.g., `tdd-workflow.yaml`)
- **Templates:** `{type}-template.{ext}` (e.g., `coordinator-template.md`)

#### Documentation

- **Guide Files:** `{TITLE}.md` (UPPERCASE for guides, e.g., `KICKSTART_PROMPT.md`)
- **Standards:** `{DOMAIN}_STANDARDS.md` (e.g., `CODING_STANDARDS.md`)
- **API Docs:** `{component}-api.md` (e.g., `skill-loader-api.md`)

### 2.4 Organization Principles

#### 1. Progressive Disclosure

Every skill follows a 3-level structure:

- **Level 1:** Metadata + quick start (100-150 tokens)
- **Level 2:** Implementation guide (1500-2500 tokens)
- **Level 3:** Detailed resources (filesystem, 0 tokens until accessed)

#### 2. Single Source of Truth

- Skills are defined once in `skills/*/SKILL.md`
- Agents reference skills via registry
- Documentation links to skills, never duplicates

#### 3. Metadata-Driven Discovery

- `skills/metadata.json` is the canonical skill index
- `agents/registry.json` is the canonical agent index
- Both are generated, not hand-edited

#### 4. Clear Separation of Concerns

- **skills/**: What can be done (capabilities)
- **agents/**: Who does it (specifications)
- **docs/**: How to use it (guides)
- **config/**: System configuration

#### 5. Token Efficiency

- Metadata files are compact JSON (<50KB each)
- Skill descriptions <50 words
- Level 1 content <200 tokens
- Level 2 content <3000 tokens

---

## 3. Migration Strategy

### 3.1 Old Path → New Path Mapping

#### Skills Migration

```
OLD → NEW

skills/coding-standards/python/README.md
  → skills/specialized/coding-standards/python/SKILL.md

skills/security/authentication/README.md
  → skills/specialized/security/authentication/SKILL.md

skills/skill-loader/*
  → skills/core/skill-loader/* (PRESERVE structure)

skills/legacy-bridge/*
  → skills/core/legacy-bridge/* (PRESERVE structure)
```

#### Agents Migration

```
OLD → NEW

.claude/agents/core/coder.md
  → agents/specifications/core/coder.md

.claude/agents/swarm/hierarchical-coordinator.md
  → agents/specifications/coordination/hierarchical-coordinator.md

.claude/agents/github/pr-manager.md
  → agents/specifications/github/pr-manager.md

.claude/agents/templates/*
  → agents/templates/* (PRESERVE structure)
```

#### Documentation Migration

```
OLD → NEW

docs/migration/phase2/*
  → docs/archive/migration/phase2/* (ARCHIVE)

docs/guides/SKILLS_QUICK_START.md
  → docs/guides/SKILLS_QUICK_START.md (FIX command syntax)

docs/reports/
  → reports/ (RELOCATE to top-level)
```

### 3.2 Preservation Rules

#### MUST PRESERVE (No Content Changes)

1. All `SKILL.md` files with Level 1/2/3 structure
2. All agent `.md` files with YAML frontmatter
3. All `config/*.yaml` files
4. All `examples/` templates
5. All `scripts/*.py` utilities
6. All `.github/workflows/*.yml` CI/CD

#### MAY ENHANCE (Add Missing Structure)

1. Add `SKILL.md` to skills lacking it (copy from template)
2. Add `metadata.json` to skills/ (generate from existing)
3. Add `registry.json` to agents/ (generate from existing)
4. Add `workflows/` to agents/ (extract from documentation)

#### MUST FIX (Accuracy Issues)

1. Replace `npm run` with `python3 scripts/` (20+ files)
2. Fix standards count: "24 Documents" → "25 Documents"
3. Qualify "98% reduction" → "91-99.6% reduction range"
4. Add disclaimer to `@load` directive examples

### 3.3 Consolidation Opportunities

#### Duplicate Content to Merge

1. **Coding Standards:**
   - Merge `docs/standards/CODING_STANDARDS.md` references into `skills/specialized/coding-standards/*/SKILL.md`
   - Keep docs version as comprehensive reference
   - Keep skills version as actionable guide

2. **Security Standards:**
   - Consolidate `skills/security/*` and `skills/security-practices/*`
   - Single hierarchy: `skills/specialized/security/*`

3. **Testing Standards:**
   - Merge `skills/testing/*` subdirectories
   - Single structure with clear test types

#### Documentation to Consolidate

1. Merge `docs/guides/SKILLS_QUICK_START.md` and `docs/guides/SKILLS_USER_GUIDE.md` → Single progressive guide
2. Archive old migration docs to `docs/archive/migration/`
3. Consolidate API docs to `docs/api/`

### 3.4 Migration Script Pseudocode

```python
#!/usr/bin/env python3
"""Repository structure migration script"""

def migrate_repository():
    # Phase 1: Backup
    create_git_branch("migration-v2.0")
    create_backup_archive()

    # Phase 2: Skills Migration
    for skill_dir in find_skill_directories("skills/"):
        if not has_skill_md(skill_dir):
            create_skill_md_from_template(skill_dir)

        # Move to specialized/ if not core
        if skill_dir not in ["skill-loader", "legacy-bridge"]:
            new_path = f"skills/specialized/{skill_dir}"
            git_mv(skill_dir, new_path)

    # Phase 3: Agents Migration
    git_mv(".claude/agents/", "agents/specifications/")

    # Reorganize by category
    reorganize_agents_by_type()

    # Phase 4: Generate Metadata
    generate_skills_metadata()
    generate_agents_registry()

    # Phase 5: Fix Documentation
    fix_command_syntax_global()
    fix_standards_count()
    add_load_directive_disclaimers()

    # Phase 6: Archive Old Content
    archive_old_reports()
    archive_old_migration_docs()

    # Phase 7: Validate
    run_validation_suite()
    check_no_broken_links()
    verify_token_counts()

    # Phase 8: Commit
    git_add_all()
    git_commit("feat: migrate to Anthropic-aligned structure v2.0")

def create_skill_md_from_template(skill_dir):
    """Generate SKILL.md from template if missing"""
    template = load_template("templates/skill-template.md")

    # Extract metadata from README if exists
    readme = f"{skill_dir}/README.md"
    if exists(readme):
        metadata = extract_metadata(readme)
    else:
        metadata = infer_metadata_from_path(skill_dir)

    # Generate 3-level structure
    skill_content = template.format(
        name=metadata['name'],
        description=metadata['description'],
        level_1=generate_level_1(metadata),
        level_2=generate_level_2(skill_dir),
        level_3=generate_level_3(skill_dir)
    )

    write_file(f"{skill_dir}/SKILL.md", skill_content)

def generate_skills_metadata():
    """Generate skills/metadata.json from filesystem"""
    skills = []

    for skill_md in find_all("skills/**/SKILL.md"):
        skill_data = parse_skill_metadata(skill_md)
        token_cost = calculate_token_cost(skill_md)

        skills.append({
            "id": generate_skill_id(skill_md),
            "name": skill_data['name'],
            "path": skill_md,
            "description": skill_data['description'],
            "capabilities": skill_data['capabilities'],
            "token_cost": token_cost,
            # ... more fields
        })

    metadata = {
        "version": "2.0.0",
        "generated": now(),
        "total_skills": len(skills),
        "skills": skills,
        "indexes": generate_indexes(skills)
    }

    write_json("skills/metadata.json", metadata)

def fix_command_syntax_global():
    """Fix npm → python3 across all docs"""
    for doc_file in find_all("docs/**/*.md", "README.md", "CLAUDE.md"):
        content = read_file(doc_file)

        # Fix command syntax
        content = content.replace(
            "npm run skill-loader --",
            "python3 scripts/skill-loader.py"
        )
        content = content.replace(
            "npm run skill-loader",
            "python3 scripts/skill-loader.py"
        )

        write_file(doc_file, content)
```

---

## 4. Implementation Phases

### Phase 1: Structure Setup (Week 1, Days 1-2)

**Goal:** Create new directory structure without moving content

**Tasks:**

1. Create `agents/` directory structure

   ```bash
   mkdir -p agents/{specifications/{core,specialized,coordination,github,consensus,optimization,sparc},workflows,templates}
   ```

2. Create `skills/core/` and `skills/specialized/` directories

   ```bash
   mkdir -p skills/{core,specialized}
   ```

3. Create `docs/skills/`, `docs/agents/`, `docs/api/`, `docs/archive/`

   ```bash
   mkdir -p docs/{skills,agents,api,archive}
   ```

4. Create metadata template files

   ```bash
   touch skills/metadata.json
   touch agents/registry.json
   ```

**Deliverables:**

- [ ] New directory tree created
- [ ] Template files in place
- [ ] No content moved yet (structure only)

**Validation:**

- Tree structure matches spec
- All directories have README.md placeholders

---

### Phase 2: Skills Migration (Week 1, Days 3-5)

**Goal:** Migrate all skills to new structure with SKILL.md consistency

**Tasks:**

1. **Move meta-skills to core/**

   ```bash
   git mv skills/skill-loader skills/core/
   git mv skills/legacy-bridge skills/core/
   ```

2. **Move domain skills to specialized/**

   ```bash
   # For each skill category:
   git mv skills/coding-standards skills/specialized/
   git mv skills/security skills/specialized/
   # ... repeat for all categories
   ```

3. **Add missing SKILL.md files**
   - Identify skills without SKILL.md: ~40 directories
   - Generate from template using existing README content
   - Ensure Level 1/2/3 structure in each

4. **Generate skills/metadata.json**

   ```bash
   python3 scripts/generate-skills-metadata.py
   ```

5. **Consolidate duplicate security skills**
   - Merge `skills/specialized/security/` and `skills/specialized/security-practices/`

**Deliverables:**

- [ ] All 50 skills in correct locations
- [ ] Every skill has SKILL.md
- [ ] metadata.json generated and validated
- [ ] Token counts calculated for all skills

**Validation:**

```bash
# All skills have SKILL.md
find skills/specialized -type d -maxdepth 2 ! -exec test -f {}/SKILL.md \; -print

# Metadata is valid JSON
python3 -m json.tool skills/metadata.json

# Token counts are within limits
python3 scripts/validate-token-costs.py skills/metadata.json
```

---

### Phase 3: Agents Migration (Week 2, Days 1-2)

**Goal:** Move agents from .claude/ to top-level agents/

**Tasks:**

1. **Move core agents**

   ```bash
   git mv .claude/agents/core/* agents/specifications/core/
   ```

2. **Reorganize by category**

   ```bash
   git mv .claude/agents/swarm/* agents/specifications/coordination/
   git mv .claude/agents/github/* agents/specifications/github/
   git mv .claude/agents/consensus/* agents/specifications/consensus/
   # ... etc
   ```

3. **Move templates**

   ```bash
   git mv .claude/agents/templates/* agents/templates/
   ```

4. **Extract workflow patterns**
   - Create `agents/workflows/tdd-workflow.yaml`
   - Create `agents/workflows/feature-development.yaml`
   - Create `agents/workflows/bug-fix-workflow.yaml`
   - Create `agents/workflows/refactoring-workflow.yaml`

5. **Generate agents/registry.json**

   ```bash
   python3 scripts/generate-agents-registry.py
   ```

**Deliverables:**

- [ ] All 49 agents in agents/specifications/
- [ ] 4+ workflow YAML files created
- [ ] registry.json generated and validated
- [ ] .claude/agents/ removed

**Validation:**

```bash
# No agents left in old location
test ! -d .claude/agents || echo "FAIL: .claude/agents still exists"

# Registry is valid
python3 -m json.tool agents/registry.json

# All agents referenced in workflows exist
python3 scripts/validate-agent-workflows.py
```

---

### Phase 4: Documentation Fixes (Week 2, Days 3-4)

**Goal:** Fix accuracy issues identified in audit

**Tasks:**

1. **Fix command syntax (CRITICAL)**

   ```bash
   # Global search/replace
   python3 scripts/fix-command-syntax.py --dry-run
   python3 scripts/fix-command-syntax.py --apply
   ```

   Files affected (~20):
   - README.md
   - CLAUDE.md
   - docs/guides/SKILLS_QUICK_START.md
   - docs/guides/SKILLS_USER_GUIDE.md

2. **Fix standards count**
   - README.md:189: "24 Documents" → "25 Documents"

3. **Qualify performance claims**
   - Find all "98% reduction" occurrences (17 files)
   - Replace with: "Progressive loading reduces token usage by 91-99.6% depending on scenario"
   - Add baseline context and measurement methodology

4. **Add @load disclaimers**
   - Add "🚧 Planned Feature" marker before @load examples
   - Reference actual python3 command as current implementation

5. **Archive old reports**

   ```bash
   mkdir -p reports/archive/2025-10
   mv reports/generated/*-2025-10-1[0-7]* reports/archive/2025-10/
   ```

6. **Create new documentation**
   - docs/skills/authoring-guide.md
   - docs/agents/agent-development-guide.md
   - docs/api/skill-loader-api.md
   - docs/api/agent-registry-api.md

**Deliverables:**

- [ ] All command syntax fixed (npm → python3)
- [ ] Performance claims qualified with ranges
- [ ] @load directive clearly marked as planned
- [ ] Old reports archived
- [ ] New documentation created

**Validation:**

```bash
# No npm commands remain
! grep -r "npm run skill-loader" docs/ README.md CLAUDE.md

# No unqualified "98%" claims
! grep -r "98% reduction" docs/ | grep -v "91-99.6%"

# All @load examples have disclaimers
grep -B2 "@load" docs/ | grep -q "Planned Feature"
```

---

### Phase 5: Validation & Testing (Week 2, Day 5)

**Goal:** Ensure migration is complete and correct

**Tasks:**

1. **Run audit suite**

   ```bash
   python3 scripts/generate-audit-reports.py
   ```

   Expected results:
   - Broken links: 0
   - Hub violations: 0
   - Orphans: ≤5
   - Documentation accuracy: >95%

2. **Validate metadata**

   ```bash
   python3 scripts/validate-skills-metadata.py
   python3 scripts/validate-agents-registry.py
   ```

3. **Check token costs**

   ```bash
   python3 scripts/verify-token-costs.py
   ```

   Limits:
   - metadata_only: <100 tokens
   - level_1: <200 tokens
   - level_2: <3000 tokens

4. **Test skill loading**

   ```bash
   python3 scripts/skill-loader.py load skill:coding-standards/python
   python3 scripts/skill-loader.py recommend api
   ```

5. **CI/CD validation**

   ```bash
   pre-commit run --all-files
   pytest tests/
   ```

6. **Manual checks**
   - [ ] Navigate repository structure
   - [ ] Verify all READMEs are accurate
   - [ ] Check all links work
   - [ ] Confirm examples execute

**Deliverables:**

- [ ] All automated tests pass
- [ ] Audit gates pass (0/0/≤5)
- [ ] Token costs within limits
- [ ] Manual validation complete

**Validation:**

```bash
# Audit gates
python3 scripts/check-audit-gates.py

# Token limits
python3 scripts/check-token-limits.py

# CI passes
.github/workflows/lint-and-validate.yml
```

---

### Phase 6: Rollout & Documentation (Week 3)

**Goal:** Deploy changes and communicate to users

**Tasks:**

1. **Create migration guide**
   - docs/MIGRATION_GUIDE_V2.md
   - Document all breaking changes
   - Provide before/after examples
   - Include troubleshooting section

2. **Update README.md**
   - New structure overview
   - Updated quick start
   - Fixed all accuracy issues

3. **Update CLAUDE.md**
   - New directory references
   - Correct command syntax throughout
   - Updated agent/skill counts

4. **Create CHANGELOG entry**
   - Version 2.0.0
   - List all structural changes
   - Note breaking changes
   - Credit contributors

5. **Generate comparison report**

   ```bash
   python3 scripts/generate-migration-report.py > reports/migration-v2-report.md
   ```

6. **Create PR**
   - Branch: migration-v2.0
   - PR title: "feat: migrate to Anthropic-aligned structure v2.0"
   - Include before/after metrics
   - Link to migration guide

**Deliverables:**

- [ ] Migration guide complete
- [ ] README.md updated
- [ ] CLAUDE.md updated
- [ ] CHANGELOG.md updated
- [ ] Migration report generated
- [ ] PR created

---

## 5. Anthropic Alignment

### 5.1 Progressive Disclosure Implementation

Every skill MUST follow this exact structure:

```markdown
---
name: skill-name
description: One-sentence description under 50 words
---

# Skill Name

## Level 1: Quick Start (5 minutes)

### What You'll Learn
[One paragraph describing the skill's purpose]

### Core Principles
- [3-5 bullet points of key concepts]

### Quick Reference
[Minimal working example - 10-20 lines of code]

### Essential Checklist
- [ ] [5-7 actionable items]

### Common Pitfalls
- [3-5 things to avoid]

---

## Level 2: Implementation (30 minutes)

### Deep Dive Topics

#### 1. [Topic Name]
[Detailed explanation with code examples]

#### 2. [Topic Name]
[Detailed explanation with code examples]

### Implementation Patterns
[Reusable patterns with before/after examples]

### Automation Tools
[Configuration examples for linters, formatters, CI]

### Integration Points
- Links to [Related Skill](../path/to/SKILL.md)

---

## Level 3: Mastery (Extended Learning)

### Advanced Topics
[Complex patterns, edge cases, optimization]

### Resources
#### Essential Reading
[External references]

#### Tools and Frameworks
[Tool recommendations]

### Templates
[Full file templates]

### Scripts
[Automation scripts]

---

## Bundled Resources

- [Full {STANDARD}.md](../../docs/standards/{STANDARD}.md)
- [UNIFIED_STANDARDS.md](../../docs/standards/UNIFIED_STANDARDS.md)
- Example configs in `./resources/`
- Automation scripts in `./scripts/`
```

**Token Budgets:**

- Level 1 (metadata + quick start): 100-150 tokens
- Level 2 (implementation): 1500-2500 tokens
- Level 3 (mastery): 0 tokens (filesystem references)

### 5.2 Skill Template Format

**File:** `skills/templates/skill-template.md`

```markdown
---
name: {skill-id}
description: {one-sentence-description}
category: {specialized/domain}
version: 1.0.0
status: draft|stable|deprecated
---

# {Skill Title}

## Level 1: Quick Start (5 minutes)

### What You'll Learn

{Brief paragraph explaining what this skill provides and who should use it}

### Core Principles

- **{Principle 1}**: {One-sentence explanation}
- **{Principle 2}**: {One-sentence explanation}
- **{Principle 3}**: {One-sentence explanation}

### Quick Reference

```{language}
# ✅ Good: {Example of correct usage}
{minimal-working-example}

# ❌ Bad: {Example of incorrect usage}
{anti-pattern-example}
```

### Essential Checklist

- [ ] {Actionable item 1}
- [ ] {Actionable item 2}
- [ ] {Actionable item 3}
- [ ] {Actionable item 4}
- [ ] {Actionable item 5}

### Common Pitfalls

- {Pitfall 1 and how to avoid it}
- {Pitfall 2 and how to avoid it}
- {Pitfall 3 and how to avoid it}

---

## Level 2: Implementation (30 minutes)

### Deep Dive Topics

#### 1. {Topic Name}

**{Context}:**

```{language}
// Implementation example
{detailed-code-example}
```

**{Explanation}:**
{Paragraph explaining the pattern}

#### 2. {Topic Name}

[Repeat structure]

### Implementation Patterns

#### {Pattern Name}

```{language}
// ❌ Before
{before-code}

// ✅ After
{after-code}
```

### Automation Tools

```{language}
// Configuration example
{tool-config}
```

### Integration Points

- Links to [{Related Skill}](../path/SKILL.md) for {reason}
- Links to [{Standard}](../../docs/standards/{STANDARD}.md)

---

## Level 3: Mastery (Extended Learning)

### Advanced Topics

#### 1. {Advanced Topic}

```{language}
{complex-example}
```

### Resources

#### Essential Reading

- [{Book/Article Title}]({URL})

#### Tools and Frameworks

- **{Tool Name}**: {Purpose}

### Templates

#### {Template Name}

```{language}
{full-template-file}
```

### Scripts

#### {Script Name}

```{language}
#!/usr/bin/env {interpreter}
{automation-script}
```

---

## Bundled Resources

- [Full {STANDARD}.md](../../docs/standards/{STANDARD}.md)
- Template files in `./templates/`
- Scripts in `./scripts/`
- References in `./resources/`

```

### 5.3 Capability Declaration Format

Skills declare capabilities in metadata:

```json
{
  "capabilities": [
    "code_generation",      // Can generate code
    "linting",             // Can lint existing code
    "formatting",          // Can format code
    "type_checking",       // Can check types
    "refactoring",         // Can refactor code
    "testing",             // Can generate tests
    "documentation",       // Can generate docs
    "api_design",          // Can design APIs
    "error_handling",      // Can handle errors
    "optimization",        // Can optimize performance
    "security_review",     // Can review security
    "deployment",          // Can deploy services
    "monitoring",          // Can setup monitoring
    "compliance_check"     // Can check compliance
  ]
}
```

Agents reference capabilities:

```json
{
  "required_capabilities": [
    "code_generation",
    "testing"
  ],
  "optional_capabilities": [
    "security_review",
    "documentation"
  ]
}
```

**Capability Taxonomy:**

1. **Code Operations:** `code_generation`, `refactoring`, `optimization`
2. **Quality Assurance:** `linting`, `formatting`, `type_checking`, `testing`
3. **Security:** `security_review`, `threat_modeling`, `secrets_management`
4. **Documentation:** `documentation`, `api_design`, `schema_generation`
5. **Operations:** `deployment`, `monitoring`, `compliance_check`

### 5.4 Token Cost Estimation Approach

**Methodology:**

1. **Metadata Only (Target: <100 tokens)**

   ```json
   {
     "id": "coding-standards-python",
     "name": "Python Coding Standards",
     "description": "PEP 8 compliant Python development standards with type hints and modern tooling",
     "capabilities": ["code_generation", "linting", "formatting"]
   }
   ```

   Estimated: 85 tokens

2. **Level 1: Quick Start (Target: <200 tokens)**
   - Metadata (85 tokens)
   - Core Principles (3 bullets × 10 tokens = 30 tokens)
   - Quick Reference (code block = 40 tokens)
   - Checklist (5 items × 5 tokens = 25 tokens)
   - Common Pitfalls (3 items × 5 tokens = 15 tokens)
   - **Total:** ~195 tokens

3. **Level 2: Implementation (Target: <3000 tokens)**
   - Level 1 content (195 tokens)
   - Deep Dive (3 topics × 300 tokens = 900 tokens)
   - Implementation Patterns (5 patterns × 150 tokens = 750 tokens)
   - Automation Tools (config examples = 200 tokens)
   - Integration Points (links = 50 tokens)
   - **Total:** ~2095 tokens

4. **Level 3: Mastery (0 tokens initially)**
   - Advanced topics loaded from filesystem on-demand
   - Resources are external links
   - Templates and scripts accessed via file reads

**Calculation Script:**

```python
def estimate_token_cost(skill_file: str) -> dict:
    """Estimate token cost for each level"""
    content = read_file(skill_file)

    # Extract sections
    metadata = extract_yaml_frontmatter(content)
    level1 = extract_section(content, "Level 1")
    level2 = extract_section(content, "Level 2")

    # Count tokens (approximation: 1 token ≈ 4 characters)
    metadata_tokens = len(json.dumps(metadata)) // 4
    level1_tokens = len(level1) // 4
    level2_tokens = len(level2) // 4

    return {
        "metadata_only": metadata_tokens,
        "level_1": metadata_tokens + level1_tokens,
        "level_2": metadata_tokens + level1_tokens + level2_tokens,
        "level_3": 0  # Loaded on-demand
    }
```

**Validation:**

Every skill MUST pass:

```bash
python3 scripts/validate-token-costs.py skills/metadata.json
```

Checks:

- metadata_only < 100 tokens ✅
- level_1 < 200 tokens ✅
- level_2 < 3000 tokens ✅

---

## Appendix A: File Count Summary

| Directory | Before | After | Change |
|-----------|--------|-------|--------|
| skills/ | 416 files | 416 files | Reorganized |
| .claude/agents/ | 65 files | 0 files | Moved |
| agents/ | 0 files | 65+ files | Created |
| docs/ | 101 files | 110+ files | Enhanced |
| config/ | 6 files | 6 files | Preserved |
| **TOTAL** | ~590 files | ~600 files | +10 files |

**New Files Added:**

- skills/metadata.json
- agents/registry.json
- agents/workflows/*.yaml (4 files)
- docs/skills/*.md (4 files)
- docs/agents/*.md (4 files)
- docs/api/*.md (3 files)

---

## Appendix B: Migration Checklist

### Pre-Migration

- [ ] Create git branch: `migration-v2.0`
- [ ] Backup repository: `git archive`
- [ ] Review audit findings
- [ ] Document current state

### Phase 1: Structure

- [ ] Create directory tree
- [ ] Add template files
- [ ] Validate structure

### Phase 2: Skills

- [ ] Move meta-skills to core/
- [ ] Move domain skills to specialized/
- [ ] Add missing SKILL.md files
- [ ] Generate metadata.json
- [ ] Validate token costs

### Phase 3: Agents

- [ ] Move agents to top-level
- [ ] Reorganize by category
- [ ] Create workflow files
- [ ] Generate registry.json
- [ ] Validate references

### Phase 4: Documentation

- [ ] Fix command syntax
- [ ] Qualify performance claims
- [ ] Add @load disclaimers
- [ ] Archive old reports
- [ ] Create new docs

### Phase 5: Validation

- [ ] Run audit suite
- [ ] Check token costs
- [ ] Test skill loading
- [ ] CI/CD passes
- [ ] Manual review

### Phase 6: Rollout

- [ ] Create migration guide
- [ ] Update README.md
- [ ] Update CLAUDE.md
- [ ] Update CHANGELOG.md
- [ ] Create PR

---

## Appendix C: Validation Commands

```bash
# Structure validation
tree agents/ -L 2
tree skills/ -L 3
ls -lh {skills,agents}/metadata.json {agents,agents}/registry.json

# Metadata validation
python3 -m json.tool skills/metadata.json
python3 -m json.tool agents/registry.json

# Token cost validation
python3 scripts/validate-token-costs.py skills/metadata.json

# Command syntax check
! grep -r "npm run skill-loader" docs/ README.md CLAUDE.md

# Audit gates
python3 scripts/generate-audit-reports.py
python3 scripts/check-audit-gates.py

# CI validation
pre-commit run --all-files
pytest tests/

# Skill loading test
python3 scripts/skill-loader.py load skill:coding-standards/python
python3 scripts/skill-loader.py recommend api
```

---

**END OF SPECIFICATION**

---

**Next Steps for Implementation:**

1. Review this specification with team
2. Create implementation scripts based on pseudocode
3. Execute Phase 1 (structure setup)
4. Begin Phase 2 (skills migration)
5. Validate at each phase boundary

**Questions/Concerns:**

- Compatibility layer design for 6-month deprecation period
- Token cost validation methodology refinement
- Workflow YAML schema definition
- Agent capability taxonomy expansion
