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

## Project Overview

This project provides comprehensive software development standards with Claude-Flow orchestration for systematic development workflows.

## Build Commands

- `npm run build` - Build project
- `npm run test` - Run tests
- `npm run lint` - Linting
- `npm run typecheck` - Type checking

## Code Style & Best Practices

- **Modular Design**: Files under 500 lines
- **Environment Safety**: Never hardcode secrets
- **Test-First**: Write tests before implementation
- **Clean Architecture**: Separate concerns
- **Documentation**: Keep updated

## 🚀 Available Agents (49 Total)

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
# Add Claude Flow MCP server
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

- **Significant token optimization** through strategic caching
- **Parallel execution capabilities** for improved speed
- **Multiple coordination strategies** for different task types
- **Persistent memory** for context retention across sessions

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

## Integration Tips

1. Start with basic swarm init
2. Scale agents gradually
3. Use memory for context
4. Monitor progress regularly
5. Train patterns from success
6. Enable hooks automation
7. Use GitHub tools first

## Documentation Integrity Principles

### Accuracy Standards

- **No Unverifiable Claims**: All performance metrics and capabilities must be demonstrable
- **Honest Representation**: Features described must actually exist and work as documented
- **Regular Validation**: Documentation reviewed and updated with each major change
- **Clear Limitations**: Known issues and limitations explicitly documented

### Verification Checklist

- ✅ Agent counts match actual available agents
- ✅ Command examples are tested and working
- ✅ File paths and directories exist
- ✅ Integration instructions are current
- ✅ Performance claims are measurable
- ✅ Tool lists are accurate and complete

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

- `.github/workflows/lint-and-validate.yml` job reads `structure-audit.json` and **fails** if (broken>0 OR hubs>0 OR orphans>{{orphan_limit}}). Upload artifacts: `linkcheck.txt`, `structure-audit.md/json`, `hub-matrix.tsv`.

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
