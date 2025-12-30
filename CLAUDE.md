# Claude Code Configuration - Standards Router & SPARC Environment

## 🚀 Fast Path: Standards Auto-Loading

### Quick Load by Product Type

```
@load product:api              # REST/GraphQL API service
@load product:web-service       # Full-stack web application
@load product:frontend-web      # React/Vue/Angular SPA
@load product:mobile           # iOS/Android application
@load product:data-pipeline    # ETL/ELT data workflow
@load product:ml-service       # ML training/inference service
```

### Custom Combinations

```
@load [product:api + CS:python + TS:pytest]       # Python API
@load [product:frontend-web + FE:react + SEC:*]   # React with all security
@load [CS:python + TS:* + SEC:* + NIST-IG:full]  # Full compliance stack
```

### How It Works

1. **Reads** `config/product-matrix.yaml` for product mappings
2. **Resolves** standard codes (CS, TS, SEC, etc.) to specific docs
3. **Expands** wildcards (SEC:* → all security standards)
4. **Auto-includes** NIST-IG:base when SEC is present
5. **Loads** relevant standards from `docs/standards/` and related paths

### Routing Contracts

- **Input**: `@load` directive with product type and/or standard codes
- **Processing**: Matrix resolution → wildcard expansion → NIST inclusion
- **Output**: Loaded standards with implementation guidance

**Implementation Note**: The `@load` directive syntax shown above represents the planned interface. Current implementation requires using the skill-loader script:

```bash
python3 scripts/skill-loader.py load product:api
python3 scripts/skill-loader.py load skill:coding-standards/python
```

---

## 📘 Anthropic Skills.md Alignment

**Compliance Status**: 61/61 skills fully compliant (100%) ✅

**Last Optimized**: 2025-10-24 23:30:00 EDT (Phase 2 complete)

This repository implements Anthropic's canonical skills.md format with value-add extensions:

### ✅ Required Compliance (Anthropic Spec)

1. **YAML Frontmatter** with required fields:
   - `name`: Skill identifier (<64 chars, lowercase/hyphens only)
   - `description`: What the skill does and when to use it (<1024 chars)

2. **3-Level Progressive Disclosure**:
   - **Level 1**: Metadata (YAML frontmatter) - always loaded
   - **Level 2**: Instructions (markdown body) - loaded when triggered
   - **Level 3**: Resources (separate files) - loaded as needed

3. **Token Budget Recommendation**: <5,000 tokens for Level 2

### 🚀 Value-Add Extensions (Standards Repository)

We extend Anthropic's format with optional metadata for automation:

- `category`: Skill grouping (coding-standards, security, etc.)
- `difficulty`: Learning level (beginner, intermediate, advanced)
- `nist_controls`: Compliance traceability (e.g., AC-2, SC-7)
- `related_skills`: Navigation and discovery
- `prerequisites`: Learning dependencies
- `estimated_time`: Time planning
- `last_updated`: Maintenance tracking

**Compatibility**: All extensions are optional - skills work with or without them.

### ✅ Optimization Complete (Phase 2)

**All 61 skills now meet Anthropic's <5K token budget:**

- Comprehensive content preserved in REFERENCE.md files (18 skills)
- Level 2 optimized for essential patterns and workflows
- 102,142 tokens reduced (61.4% average reduction)
- Zero information loss - all content reorganized, not deleted

**Strategy Used**: Progressive disclosure enhanced with Level 3 REFERENCE.md files containing complete examples, detailed configurations, and production-ready templates.

### 📊 Compliance Metrics

**Last Validated**: 2025-10-24 23:30:00 EDT (Phase 2 complete)

```bash
# Verify compliance status
python3 scripts/validate-anthropic-compliance.py

# View detailed report
cat reports/generated/anthropic-compliance-report.md
```

**Current Compliance**:

- Required fields: 61/61 (100%) ✅
- Token budget: 61/61 (100%) ✅
- Overall: 61/61 compliant (100%) ✅

### 🔗 Official Specification

- Anthropic Documentation: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- Standards Repository Format Spec: `docs/guides/SKILL_FORMAT_SPEC.md`
- Phase 2 Optimization: `reports/generated/FINAL_OPTIMIZATION_REPORT.md`

---

## 🚨 CRITICAL: CONCURRENT EXECUTION & FILE MANAGEMENT

**ABSOLUTE RULES**:

1. ALL operations MUST be concurrent/parallel in a single message
2. **NEVER save working files, text/mds and tests to the root folder**
3. ALWAYS organize files in appropriate subdirectories

### ⚡ GOLDEN RULE: "1 MESSAGE = ALL RELATED OPERATIONS"

**MANDATORY PATTERNS:**

- **TodoWrite**: ALWAYS batch ALL todos in ONE call (5-10+ todos minimum)
- **Task tool**: ALWAYS spawn ALL agents in ONE message with full instructions
- **File operations**: ALWAYS batch ALL reads/writes/edits in ONE message
- **Bash commands**: ALWAYS batch ALL terminal operations in ONE message
- **Memory operations**: ALWAYS batch ALL memory store/retrieve in ONE message

### 📁 File Organization Rules

**NEVER save to root folder. Use these directories:**

- `/src` - Source code files
- `/tests` - Test files
- `/docs` - Documentation and markdown files
- `/config` - Configuration files
- `/scripts` - Utility scripts
- `/examples` - Example code

## 📐 Quality & Accuracy Framework

### Documentation Integrity Policy

**Core Principles**:

- **No Exaggeration**: All performance claims must be measurable and verified
- **Primary Evidence**: Link to actual files, configs, scripts - not abstractions
- **Temporal Precision**: Use exact timestamps in ISO 8601 + timezone format
- **Trade-offs Required**: Every feature must document limitations
- **Refusal to Guess**: Mark uncertain information as "Unknown" or "Planned"

### Enforcement Mechanisms

**Automated Validation** (run before every commit):

```bash
# Verify all documentation claims
python3 scripts/validate-claims.py --verbose

# Verify skill counts and structure
python3 scripts/validate-skills.py --count-verify

# Check for broken links and orphans
python3 scripts/generate-audit-reports.py
```

**Review Cadence**:

- **Per Commit**: Automated validation passes
- **Weekly**: Structure audit (broken links = 0, hub violations = 0, orphans ≤ 5)
- **Quarterly**: External review of all claims against repository state

### Evidence Requirements

All claims must link to:

1. **Code**: Implementation file paths (e.g., `scripts/skill-loader.py:139`)
2. **Configuration**: Relevant config files (e.g., `config/product-matrix.yaml`)
3. **Tests**: Validation scripts proving the claim
4. **Audit Reports**: Generated reports in `reports/generated/`

**Example of Evidence-Based Claim**:

```markdown
✅ GOOD: "48 agent types available (verified 2025-10-24, see `.claude/agents/`)"
❌ BAD: "Numerous agents available for various tasks"
```

### Prohibited Language

**Never use without data**:

- Vague quantifiers: "significantly", "dramatically", "vastly"
- Unverifiable claims: "best", "optimal", "perfect"
- Marketing language: "game-changer", "revolutionary", "cutting-edge"

**Always prefer**:

- Specific metrics: "91-99.6% token reduction" (with measurement method)
- Qualified statements: "In testing with 61 skills..." (with test conditions)
- Honest limitations: "Requires external MCP server" (with workarounds if any)

### Verification Checklist

Before updating CLAUDE.md:

- [ ] All performance claims include measurement method
- [ ] All counts verified against actual files (use `find`, `ls`, `wc -l`)
- [ ] All timestamps in ISO 8601 + timezone (e.g., `2025-10-24 21:50:00 EDT`)
- [ ] All "available" features actually implemented (not planned)
- [ ] All scripts referenced are executable and working
- [ ] Validation scripts pass: `python3 scripts/validate-claims.py`

## Project Overview

This project provides comprehensive software development standards with Claude-Flow orchestration for systematic development workflows.

## Repository Commands

- `python3 scripts/generate-audit-reports.py` - Generate audit reports
- `python3 scripts/validate-skills.py` - Validate skills
- `pre-commit run --all-files` - Run all checks
- `pytest tests/` - Run test suite

### Validation & Verification Commands

**Accuracy Checks** (run before commits):

```bash
# Verify documentation claims against reality
python3 scripts/validate-claims.py --verbose

# Verify actual counts match documented counts
python3 scripts/validate-claims.py --verbose

# Check agent definitions
ls -1 .claude/agents/*.md | grep -v README | wc -l  # Should match agent count

# Check skills count
find skills -name "SKILL.md" | wc -l  # Should match skills count

# Verify standards count
ls -1 docs/standards/*.md | wc -l  # Should match documented count
```

**Structure Validation**:

```bash
# Full audit (broken links, orphans, hub violations)
python3 scripts/generate-audit-reports.py

# Expected output (as of 2025-10-24):
# - Broken links: 0
# - Orphans: ≤5
# - Hub violations: 0
```

**Performance Verification**:

```bash
# Measure actual token usage
python3 scripts/token-counter.py --product api --language python

# Compare full load vs skills load
python3 scripts/token-counter.py --compare
```

## Code Style & Best Practices

- **Modular Design**: Files under 500 lines
- **Environment Safety**: Never hardcode secrets
- **Test-First**: Write tests before implementation
- **Clean Architecture**: Separate concerns
- **Documentation**: Keep updated

## 🚀 Agent Types for Task Tool (49 Agent Types)

**Last Updated**: 2025-10-25 21:40:00 EDT (UTC-04:00)

**Note**: These are conceptual agent types used with the Task tool, not separate callable tools. The 49 agent types below are implemented across 60 agent definition files in `.claude/agents/` directory (some types have multiple implementation variants). See MCP Tools section for actual callable tools from claude-flow MCP server.

**Verification**:

```bash
# Verify agent type count (unique conceptual types)
grep -o '`[a-z-]*`' CLAUDE.md | sort -u | wc -l
# Expected: 50 unique agent types

# Verify physical file count (implementation files)
find .claude/agents -name "*.md" ! -name "README.md" ! -name "MIGRATION_SUMMARY.md" | wc -l
# Expected: 60 agent definition files
```

Last verified: 2025-10-24 22:15:00 EDT

### Core Development

`coder`, `reviewer`, `tester`, `planner`, `researcher`

### Swarm Coordination

`hierarchical-coordinator`, `mesh-coordinator`, `adaptive-coordinator`, `collective-intelligence-coordinator`, `swarm-memory-manager`

### Consensus & Distributed

`byzantine-coordinator`, `raft-manager`, `gossip-coordinator`, `consensus-builder`, `crdt-synchronizer`, `quorum-manager`, `security-manager`

### Performance & Optimization

`perf-analyzer`, `performance-benchmarker`, `task-orchestrator`, `memory-coordinator`, `smart-agent`

### GitHub & Repository

`github-modes`, `pr-manager`, `code-review-swarm`, `issue-tracker`, `release-manager`, `workflow-automation`, `project-board-sync`, `repo-architect`, `multi-repo-swarm`

### SPARC Methodology

`sparc-coord`, `sparc-coder`, `specification`, `pseudocode`, `architecture`, `refinement`

### Specialized Development

`backend-dev`, `mobile-dev`, `ml-developer`, `cicd-engineer`, `api-docs`, `system-architect`, `code-analyzer`, `base-template-generator`

### Testing & Validation

`tdd-london-swarm`, `production-validator`

### Migration & Planning

`migration-planner`, `swarm-init`

## 🎯 Claude Code vs MCP Tools

### Claude Code Handles ALL

- File operations (Read, Write, Edit, MultiEdit, Glob, Grep)
- Code generation and programming
- Bash commands and system operations
- Implementation work
- Project navigation and analysis
- TodoWrite and task management
- Git operations
- Package management
- Testing and debugging

### MCP Tools ONLY

- Coordination and planning
- Memory management
- Neural features
- Performance tracking
- Swarm orchestration
- GitHub integration

**KEY**: MCP coordinates, Claude Code executes.

## 🚀 Quick Setup

```bash
# Add Claude Flow MCP server (EXTERNAL - requires npx/npm)
# This is an external MCP server, not a local Python script
claude mcp add claude-flow npx claude-flow@alpha mcp start
```

## MCP Tool Categories

### Coordination

`swarm_init`, `agent_spawn`, `task_orchestrate`

### Monitoring

`swarm_status`, `agent_list`, `agent_metrics`, `task_status`, `task_results`

### Memory & Neural

`memory_usage`, `neural_status`, `neural_train`, `neural_patterns`

### GitHub Integration

`github_swarm`, `repo_analyze`, `pr_enhance`, `issue_triage`, `code_review`

### System

`benchmark_run`, `features_detect`, `swarm_monitor`

## 📋 Agent Coordination Protocol

### Every Agent MUST

> **NOTE**: The `npx claude-flow@alpha` commands below are for the EXTERNAL Claude Flow MCP server.
> These are NOT local Python scripts. See Quick Setup section for installation.

**1️⃣ BEFORE Work:**

```bash
npx claude-flow@alpha hooks pre-task --description "[task]"
npx claude-flow@alpha hooks session-restore --session-id "swarm-[id]"
```

**2️⃣ DURING Work:**

```bash
npx claude-flow@alpha hooks post-edit --file "[file]" --memory-key "swarm/[agent]/[step]"
npx claude-flow@alpha hooks notify --message "[what was done]"
```

**3️⃣ AFTER Work:**

```bash
npx claude-flow@alpha hooks post-task --task-id "[task]"
npx claude-flow@alpha hooks session-end --export-metrics true
```

## 🎯 Concurrent Execution Examples

### ✅ CORRECT (Single Message)

```javascript
[BatchTool]:
  // Initialize swarm
  mcp__claude-flow__swarm_init { topology: "mesh", maxAgents: 6 }
  mcp__claude-flow__agent_spawn { type: "researcher" }
  mcp__claude-flow__agent_spawn { type: "coder" }
  mcp__claude-flow__agent_spawn { type: "tester" }

  // Spawn agents with Task tool
  Task("Research agent: Analyze requirements...")
  Task("Coder agent: Implement features...")
  Task("Tester agent: Create test suite...")

  // Batch todos
  TodoWrite { todos: [
    {id: "1", content: "Research", status: "in_progress", priority: "high"},
    {id: "2", content: "Design", status: "pending", priority: "high"},
    {id: "3", content: "Implement", status: "pending", priority: "high"},
    {id: "4", content: "Test", status: "pending", priority: "medium"},
    {id: "5", content: "Document", status: "pending", priority: "low"}
  ]}

  // File operations
  Bash "mkdir -p app/{src,tests,docs}"
  Write "app/src/index.js"
  Write "app/tests/index.test.js"
  Write "app/docs/README.md"
```

### ❌ WRONG (Multiple Messages)

```javascript
Message 1: mcp__claude-flow__swarm_init
Message 2: Task("agent 1")
Message 3: TodoWrite { todos: [single todo] }
Message 4: Write "file.js"
// This breaks parallel coordination!
```

## Performance Benefits

**Last Verified**: 2025-10-24 22:10:00 EDT (UTC-04:00)

**Token Optimization**:

- Skills system reduces token usage by 91-99.6% depending on scenario:
  - Repository metadata: 127K → 500 tokens (99.6% reduction)
  - Typical usage: 8.9K → 573 tokens (93.6% reduction)
  - Single skill Level 1: ~300-600 tokens

**Verification Method**:

```bash
# Measure actual token reduction
python3 scripts/token-counter.py --compare full-load skills-load

# Test specific product type
python3 scripts/token-counter.py --product api --language python
```

**Evidence**:

- 61 active skills in `/home/william/git/standards/skills/`
- Product-matrix driven auto-loading in `config/product-matrix.yaml`
- Measurement script: `scripts/token-counter.py`

**Additional Capabilities**:

- Parallel execution for improved speed
- Multiple coordination strategies for different task types
- Persistent memory for context retention across sessions

**Anthropic Compatibility**: Our 3-level progressive disclosure aligns with Anthropic's canonical skills.md format, ensuring skills work across Claude API, Claude Code, Agent SDK, and Claude.ai platforms (with manual upload per platform).

**Limitations**:

- Token reduction assumes single product type; complex projects may require multiple skill loads
- Parallel execution requires proper swarm initialization
- Memory persistence depends on MCP server configuration

## Hooks Integration

### Pre-Operation

- Auto-assign agents by file type
- Validate commands for safety
- Prepare resources automatically
- Optimize topology by complexity
- Cache searches

### Post-Operation

- Auto-format code
- Train neural patterns
- Update memory
- Analyze performance
- Track token usage

### Session Management

- Generate summaries
- Persist state
- Track metrics
- Restore context
- Export workflows

## Advanced Features

- 🚀 Automatic Topology Selection
- ⚡ Parallel Execution for improved performance
- 🧠 Pattern Learning Capabilities
- 📊 Bottleneck Analysis
- 🤖 Smart Auto-Spawning
- 🛡️ Self-Healing Workflows
- 💾 Cross-Session Memory
- 🔗 GitHub Integration

## Known Limitations & Current State

**Last Audit**: 2025-10-24 22:10:00 EDT (UTC-04:00)

### Implementation Status

**Fully Implemented** ✅:

- Skills loading via `scripts/skill-loader.py`
- Product matrix mapping (`config/product-matrix.yaml`)
- 60 agent definition files available via Task tool (49 conceptual types listed)
- Validation framework (validate-claims.py, generate-audit-reports.py)
- CI/CD gates (lint-and-validate.yml)

**Partially Implemented** ⚠️:

- `@load` syntax: Documented as planned interface; current implementation requires `python3 scripts/skill-loader.py load`
- Claude-Flow MCP integration: Requires external `npx claude-flow@alpha` installation
- Neural training features: Dependent on MCP server configuration

**Not Yet Implemented** ❌:

- Automatic topology optimization (concept documented, no implementation)
- Self-healing workflows (requires MCP server features)
- Pattern learning from success (MCP-dependent)

### Known Issues

**Documentation**:

- Some MCP tool features documented without local verification (external dependency)
- @load directive presented throughout docs but requires script wrapper

**Dependencies**:

- Many advanced features require external Claude-Flow MCP server (`npx claude-flow@alpha`)
- MCP features not testable without Node.js + npx installation

**Validation**:

- validate-claims.py shows 60% pass rate (6/10 checks passing as of 2025-10-24)
- Remaining issues: Minor path references, executable permissions

### Verification Commands

**Verify implementation status**:

```bash
# Check agent definitions
find .claude/agents -name "*.md" ! -name "README.md" | wc -l

# Check skills count
find skills -name "SKILL.md" | wc -l

# Verify validation scripts exist and are executable
ls -l scripts/validate-claims.py scripts/token-counter.py scripts/generate-audit-reports.py

# Test product matrix loading (dry-run)
python3 scripts/skill-loader.py load product:api --dry-run
```

### Transparency Policy

This section is updated with each audit. If you find discrepancies between documented and actual capabilities:

1. File an issue with verification commands showing the discrepancy
2. Run `python3 scripts/validate-claims.py` to check current state
3. Refer to audit reports in `reports/generated/` for latest assessments

## Integration Tips

1. Start with basic swarm init
2. Scale agents gradually
3. Use memory for context
4. Monitor progress regularly
5. Train patterns from success
6. Enable hooks automation
7. Use GitHub tools first

## Documentation Integrity Principles

**Note**: For comprehensive quality standards, see "Quality & Accuracy Framework" (lines 76-140).

### Quick Reference Verification Checklist

**Last Audit**: 2025-10-24 22:10:00 EDT (UTC-04:00)

**Current State** (verified via scripts):

- ✅ Agent counts: 60 agent definition files in `.claude/agents/` (49 conceptual types documented)
- ✅ Skills count: 61 active SKILL.md files in `skills/` directory
- ✅ Anthropic skills compliance: 61/61 skills (100%) - Phase 2 complete
- ✅ Standards count: 25 documents in `docs/standards/`
- ✅ Command examples: Tested against repository structure
- ✅ File paths: Validated via audit scripts
- ✅ Integration instructions: Current as of 2025-10-24
- ✅ Performance claims: Evidence-based with verification methods
- ✅ Tool lists: MCP tools documented with external dependency note
- ✅ Audit status: 0 broken links, 1 orphan (under limit), hub violations resolved

**Validation Commands**:

```bash
# Run full validation suite
python3 scripts/validate-claims.py
python3 scripts/generate-audit-reports.py

# Verify specific counts
find .claude/agents -name "*.md" ! -name "README.md" ! -name "MIGRATION_SUMMARY.md" | wc -l  # Agents
find skills -name "SKILL.md" | wc -l  # Skills
ls -1 docs/standards/*.md | wc -l  # Standards
```

**Accuracy Policy**: All claims must be verifiable via script output or file inspection. See "Quality & Accuracy Framework" for full policy.

## Support

- Documentation: <https://github.com/ruvnet/claude-flow>
- Issues: <https://github.com/ruvnet/claude-flow/issues>
- Standards Repo: <https://github.com/williamzujkowski/standards>

---

Remember: **Claude Flow coordinates, Claude Code creates!**

# important-instruction-reminders

Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
Never save working files, text/mds and tests to the root folder.

<!-- BEGIN: STANDARDS_GATEKEEPER v1 -->
# CLAUDE.md — Standards Repo Gatekeeper (Claude-Flow)

> Purpose: Orchestrate a full audit + remediation + CI gating pass on the standards repo,
> excluding non-doc trees, auto-populating hubs, and aligning Kickstart ↔ Router ↔ Product Matrix.

## ROLE

You are **Senior Standards Orchestrator** for this repository. You remediate documentation structure, enforce policy gates, align the Kickstart/Router flow, and produce a merge-ready PR.

## INPUTS (templated)

- Repo URL: {{repo_url|default:"<https://github.com/williamzujkowski/standards"}}>
- Working branch: {{working_branch|default:"audit-gates-final/{{today}}"}}
- Orphan limit (gate): {{orphan_limit|default:"5"}}
- Intentional exclusions (extra, optional): {{extra_exclusions|default:""}}
- PR number (if updating an open PR): {{pr_number|default:""}}

## SCOPE & EXCLUSIONS

Exclude from orphan math & hub rules:
`.claude/**`, `subagents/**`, `memory/**`, `prompts/**`, `reports/generated/**`, `.vscode/**`, `.git/**`, `node_modules/**`, `__pycache__/**`, `.github/**`
Also exclude any items listed in `{{extra_exclusions}}`.

## GATES (hard fail if violated)

- **Broken internal links = 0**
- **Hub violations = 0**
- **Orphans ≤ {{orphan_limit}}**

## GROUND TRUTH FILES

- Kickstart: `docs/guides/KICKSTART_PROMPT.md`
- Router: `CLAUDE.md` (this file) & `docs/core/*`
- Product Matrix: `config/product-matrix.yaml`
- Audit tools: `scripts/generate-audit-reports.py`, `scripts/ensure-hub-links.py`
- CI workflow: `.github/workflows/lint-and-validate.yml`

## REQUIRED HUB RULES

Ensure `config/audit-rules.yaml` includes:

- `docs/standards/**/*.md` → `docs/standards/UNIFIED_STANDARDS.md`
- `docs/guides/**/*.md` → `docs/guides/STANDARDS_INDEX.md`
- `docs/core/**/*.md` → `docs/core/README.md`
- `docs/nist/**/*.md` → `docs/nist/README.md`
- `docs/*.md` → `docs/README.md`
- `examples/**/*.md` → `examples/README.md`
- `monitoring/**/*.md` → `monitoring/README.md`
- `tools-config/**/*.md` → `tools-config/README.md`
- `micro/**/*.md` → `micro/README.md`
- `badges/**/*.md` → `README.md`

## OPERATING RULES

- Be **idempotent**: no duplicate `AUTO-LINKS` blocks; minimal diffs.
- Treat regex-looking text as **code**, not links; fence or inline-backtick it.
- Prefer linking docs into hubs over exclusions; exclude only truly non-navigable scaffolding.

## EXECUTION PLAN (authoritative)

1) Branch

```
git checkout -b {{working_branch}} || git checkout {{working_branch}}
```

2) Policy

- Ensure `config/audit-rules.yaml` exists with the exclusions & hub rules above; append `{{extra_exclusions}}` if provided.

3) Populate hubs

```
python3 scripts/ensure-hub-links.py
```

4) Audit & Gate

```
python3 scripts/generate-audit-reports.py
```

Read `reports/generated/structure-audit.json` and enforce:

- `broken_links == 0`
- `hub_violations == 0`
- `orphans <= {{orphan_limit}}`
If any fail: fix (link or exclude) and re-run until green.

5) Kickstart ↔ Router alignment

- `docs/guides/KICKSTART_PROMPT.md` references product-matrix usage & router.
- `CLAUDE.md`/`docs/core/*` expose fast-path load (e.g., `@load product:api`) aligned with repo convention.

6) Standards inventory

```
python3 scripts/generate-standards-inventory.py
```

7) NIST quickstart

```
cd examples/nist-templates/quickstart
make test && make nist-check && make validate
cd -
```

8) CI gate (must exist)

- `.github/workflows/lint-and-validate.yml` job reads `reports/generated/structure-audit.json` and **fails** if (broken>0 OR hubs>0 OR orphans>{{orphan_limit}}). Upload artifacts from `reports/generated/`.

9) PR

- If `{{pr_number}}` empty:

  ```
  git add -A
  git commit -m "audit: enforce links=0 hubs=0 orphans<={{orphan_limit}} + router/kickstart alignment"
  git push --set-upstream origin {{working_branch}}
  ```

  Open PR titled: `Finalize audit gates (links=0, hubs=0, orphans≤{{orphan_limit}}) + router/kickstart alignment`
- Else, update PR `#{{pr_number}}`.

## EXPECTED ARTIFACTS

- `reports/generated/linkcheck.txt`
- `reports/generated/structure-audit.md`
- `reports/generated/structure-audit.json`
- `reports/generated/hub-matrix.tsv`
- `reports/generated/standards-inventory.json`
- Updated hub READMEs with `AUTO-LINKS` sections

## OUTPUT FORMAT (STRICT)

1. Diffstat
2. Gate Summary: `broken=0 hubs=0 orphans=N (limit={{orphan_limit}})`
3. Remaining Orphans (if any): one per line → `link|exclude  <path>  <hub-target or policy-line>`
4. Kickstart/Router Alignment Notes (paths + one-line changes)
5. Verification Commands (copy-paste)
6. PR Body (Markdown): Before→After table; gate compliance; intentional exclusions; artifact locations

## SUCCESS CRITERIA (MUST PRINT)

- `Broken links: 0`
- `Hub violations: 0`
- `Orphans (post-policy): ≤ {{orphan_limit}}`
- `CI: audit gates present and pass locally`
- `Kickstart ↔ Router ↔ Product Matrix: aligned and current`
<!-- END: STANDARDS_GATEKEEPER v1 -->
