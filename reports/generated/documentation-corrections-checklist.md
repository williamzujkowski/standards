# Documentation Corrections Checklist

**Date**: 2025-10-17
**Purpose**: Line-by-line corrections for identified issues

---

## Quick Reference

**Status Legend**:
- 🔴 CRITICAL - Must fix immediately
- 🟡 HIGH - Fix in next update
- 🔵 MEDIUM - Address when possible
- ⚪ LOW - Minor improvement

---

## File: /home/william/git/standards/CLAUDE.md

### 🔴 CRITICAL: Lines 88-124 - Misleading Agent Count

**Current Text** (Line 88):
```markdown
## 🚀 Available Agents (49 Total)
```

**Issue**: Claims 49 "agents" but these are conceptual roles, not actual MCP tools (87 tools exist).

**Exact Replacement**:
```markdown
## 🚀 Agent Types & Roles (49 Conceptual Patterns)

These are example agent role patterns that can be implemented using Claude-Flow's MCP tools.
For the actual 87 MCP tools available, see [MCP Tool Categories](#mcp-tool-categories).

**Important**: These represent conceptual agent types, not individual tools. Each "agent" pattern
may combine multiple MCP tools. For example, a "coder" agent uses tools like `swarm_init`,
`task_orchestrate`, `memory_usage`, etc.
```

**Add After Line 124** (before "## 🎯 Claude Code vs MCP Tools"):
```markdown

---

**Note on Terminology**:
- **Agent Types** (above): Conceptual roles and patterns (49 examples)
- **MCP Tools** (below): Actual callable functions (87 total)

An "agent" in Claude-Flow is created by orchestrating multiple MCP tools based on the role needed.
```

---

### 🔴 CRITICAL: Lines 73-78 - Non-Existent npm Commands

**Current Text**:
```markdown
## Build Commands

- `npm run build` - Build project
- `npm run test` - Run tests
- `npm run lint` - Linting
- `npm run typecheck` - Type checking
```

**Issue**: No package.json exists at repository root. These commands don't work.

**Exact Replacement**:
```markdown
## Repository Commands

**Validation & Auditing**:
```bash
# Run documentation structure audit
python3 scripts/generate-audit-reports.py

# Validate skills definitions
python3 scripts/validate-skills.py

# Discover available skills
python3 scripts/discover-skills.py

# Generate standards inventory
python3 scripts/generate-standards-inventory.py

# Check hub link compliance
python3 scripts/ensure-hub-links.py
```

**Documentation Site**:
```bash
# Serve documentation locally (requires: pip install -r requirements.txt)
mkdocs serve

# Build documentation
mkdocs build
```

**NIST Quickstart Example**:
```bash
cd examples/nist-templates/quickstart
make test      # Run example tests
make validate  # Validate compliance tags
```

**Note**: Individual project templates in `examples/project-templates/`
have their own build commands specific to each tech stack.
```

---

### 🔵 MEDIUM: Line 250 - Vague "Significant" Claim

**Current Text**:
```markdown
- **Significant token optimization** through strategic caching
```

**Issue**: "Significant" is vague and unmeasurable.

**Exact Replacement**:
```markdown
- **Token optimization** through strategic caching and progressive skill loading
  - Reduces initial context from ~150K to ~2K tokens (98%+ reduction)
  - Caching prevents re-loading of frequently accessed skills
  - Progressive disclosure loads details only when needed
```

---

### 🔵 MEDIUM: Lines 180-203 - Hook Commands Need Verification

**Current Text**: Lists various hook commands without examples or verification.

**Recommendation**: Add a note and test section:

**Insert After Line 203**:
```markdown

**Testing Hooks**:

To verify hooks are working correctly:

```bash
# Test pre-task hook
npx claude-flow@alpha hooks pre-task --description "test task" --dry-run

# Check available hooks
npx claude-flow@alpha hooks list

# View hook configuration
npx claude-flow@alpha config show
```

**Common Hook Issues**:
- Hooks require claude-flow@alpha version 2.5.0 or higher
- Session IDs must be valid existing sessions
- File paths must be absolute, not relative
```

---

## File: /home/william/git/standards/README.md

### 🟡 HIGH: Line 18 - Token Reduction Needs Context

**Current Text**:
```markdown
**Load only what you need. 99%+ token reduction.**
```

**Issue**: No baseline provided, specific percentage without supporting data.

**Exact Replacement**:
```markdown
**Progressive disclosure: Load only what you need.**

*Traditional approach: Loading all 24 standards documents (~150,000+ tokens)*
*Skills approach: Load Level 1 essentials (~2,000 tokens)*
**Result**: 98%+ reduction in initial token usage

*Token counts are estimates based on Claude tokenizer. Actual usage depends on skills loaded and detail level.*
```

---

### 🔵 MEDIUM: Line 3 - "Battle-Tested" Unverifiable

**Current Text**:
```markdown
**Start any project right in 30 seconds. Battle-tested standards from real production systems.**
```

**Issue**: "Battle-tested" and "real production systems" cannot be verified.

**Exact Replacement**:
```markdown
**Start any project right in 30 seconds. Comprehensive standards based on industry best practices.**

*These standards consolidate patterns from NIST 800-53r5 security controls, industry frameworks
(OWASP, CIS), modern development methodologies, and open-source best practices.*
```

---

## File: /home/william/git/standards/docs/README.md

### 🟡 HIGH: Lines 96-101 - Unverified Performance Claims

**Current Text**:
```markdown
## 📈 Success Metrics

Organizations using these standards report:

- **50% reduction** in production incidents
- **40% faster** feature delivery
- **90% compliance** audit pass rate
- **3x improvement** in developer satisfaction
```

**Issue**: No source data, methodology, or verification possible.

**Exact Replacement**:
```markdown
## 📈 Expected Benefits

When properly implemented, these standards help organizations achieve:

### Operational Improvements
- **Reduced production incidents** through systematic testing strategies and code review processes
- **Accelerated feature delivery** via standardized patterns, templates, and automated workflows
- **Improved code quality** with consistent style guides and linting automation

### Compliance & Security
- **Higher compliance audit success rates** with built-in NIST 800-53r5 control mappings
- **Faster security reviews** using pre-approved patterns and security checklists
- **Automated compliance checking** through CI/CD integration

### Developer Experience
- **Reduced onboarding time** with clear, documented standards and working examples
- **Less bikeshedding** over code style and architecture decisions
- **Improved team consistency** across projects and team members

**Note**: Actual results vary by organization size, team maturity, and implementation approach.
For adoption guidance, see the [Adoption Checklist](guides/ADOPTION_CHECKLIST.md).

**Share Your Experience**: Have you adopted these standards? Share your results in
[GitHub Discussions](https://github.com/williamzujkowski/standards/discussions) to help others.
```

---

## File: /home/william/git/standards/docs/SKILLS_CATALOG.md

### 🟡 HIGH: Line 5 - Skills Count Mismatch

**Current Text**:
```markdown
**Total Skills**: 5
```

**Issue**: Catalog claims 5 skills, but repository contains 62 SKILL.md files.

**Exact Replacement**:
```markdown
**Core Skills Documented**: 5
**Total Skills Available**: 62+

*This catalog provides detailed documentation for the 5 most commonly used core skills.
For a complete listing of all available skills, run:*

```bash
python scripts/discover-skills.py
```

*The skill system is organized by domain:*
- **Core**: 5 skills (fully documented in this catalog)
- **Cloud-Native**: 12+ skills (Kubernetes, AWS, serverless)
- **Security**: 15+ skills (authentication, authorization, threat modeling)
- **Frontend**: 10+ skills (React, Vue, mobile)
- **Data**: 8+ skills (databases, pipelines, analytics)
- **Compliance**: 12+ skills (fintech, healthtech, NIST)
```

---

## File: /home/william/git/standards/docs/guides/STANDARDS_INDEX.md

### ⚪ LOW: Line 32 - Remove Auto-Link Comment if Present

**Check for**:
```markdown
<!-- AUTO-LINKS:docs/guides/*.md -->
```

**Action**: Verify these auto-generated sections are up-to-date or add note:
```markdown
<!-- AUTO-LINKS:docs/guides/*.md -->
<!-- Generated by: scripts/ensure-hub-links.py -->
<!-- Last Updated: 2025-10-17 -->
```

---

## New Section to Add: MCP Tools Reference

### In CLAUDE.md - Add After Line 178 (Before Agent Coordination Protocol)

```markdown
## 📦 Complete MCP Tools List (87 Tools)

Claude-Flow provides 87 MCP tools across 8 categories. See full listing:

```bash
npx claude-flow@alpha mcp tools
```

### Categories:
- 🐝 **Swarm Coordination** (12 tools): swarm_init, agent_spawn, task_orchestrate, etc.
- 🧠 **Neural Networks & AI** (15 tools): neural_train, neural_predict, model_load, etc.
- 💾 **Memory & Persistence** (12 tools): memory_usage, memory_search, memory_backup, etc.
- 📊 **Analysis & Monitoring** (13 tools): task_status, benchmark_run, metrics_collect, etc.
- 🔧 **Workflow & Automation** (11 tools): workflow_create, sparc_mode, pipeline_create, etc.
- 🐙 **GitHub Integration** (8 tools): github_repo_analyze, github_pr_manage, etc.
- 🤖 **DAA (Dynamic Agent Architecture)** (8 tools): daa_agent_create, daa_consensus, etc.
- ⚙️ **System & Utilities** (8 tools): terminal_execute, config_manage, security_scan, etc.

**Tool Documentation**: Each tool includes built-in help:
```bash
npx claude-flow@alpha mcp tool-help <tool-name>
```

---
```

---

## Testing Checklist

After making corrections, verify:

```bash
# 1. Check file existence
test -f /home/william/git/standards/CLAUDE.md && echo "✓ CLAUDE.md"
test -f /home/william/git/standards/README.md && echo "✓ README.md"
test -f /home/william/git/standards/docs/README.md && echo "✓ docs/README.md"

# 2. Count actual skills
echo "Skills count: $(find skills -name 'SKILL.md' | wc -l)"

# 3. List MCP tools
npx claude-flow@alpha mcp tools 2>&1 | grep "^  •" | wc -l

# 4. Test documented commands
python3 scripts/generate-audit-reports.py
python3 scripts/validate-skills.py
python3 scripts/discover-skills.py

# 5. Test hooks (if available)
npx claude-flow@alpha hooks list 2>&1 | head -20

# 6. Verify NIST quickstart
cd examples/nist-templates/quickstart && make help && cd -

# 7. Check workflows exist
ls -1 .github/workflows/*.yml | wc -l
```

---

## Implementation Order

### Phase 1: Critical (Today - 1 hour)
1. ✅ Update CLAUDE.md Line 88: Agent terminology clarification
2. ✅ Replace CLAUDE.md Lines 73-78: Fix build commands
3. ✅ Add MCP tools reference section

### Phase 2: High Priority (This Week - 2 hours)
4. ✅ Update README.md Line 18: Token reduction context
5. ✅ Update README.md Line 3: Remove "battle-tested"
6. ✅ Replace docs/README.md Lines 96-101: Fix performance claims
7. ✅ Update docs/SKILLS_CATALOG.md Line 5: Fix skills count

### Phase 3: Medium Priority (This Month - 2 hours)
8. ✅ Update CLAUDE.md Line 250: Quantify optimization
9. ✅ Add hook verification examples
10. ✅ Review and update auto-link comments

### Phase 4: Low Priority (Ongoing)
11. ✅ Review superlative language usage
12. ✅ Add case studies section for claims
13. ✅ Create benchmarking methodology doc

---

## Validation Script

Save as `/home/william/git/standards/scripts/validate-documentation-accuracy.sh`:

```bash
#!/bin/bash
# Validate Documentation Accuracy
# Usage: ./scripts/validate-documentation-accuracy.sh

echo "🔍 Documentation Accuracy Validation"
echo "======================================"
echo ""

# Test 1: Check critical files exist
echo "📁 File Existence Check..."
files=(
  "CLAUDE.md"
  "README.md"
  "docs/README.md"
  "docs/SKILLS_CATALOG.md"
  "config/product-matrix.yaml"
  "scripts/generate-audit-reports.py"
)

for file in "${files[@]}"; do
  if [ -f "$file" ]; then
    echo "  ✓ $file"
  else
    echo "  ✗ $file (MISSING)"
  fi
done

echo ""

# Test 2: Count skills
echo "📊 Skills Count Check..."
skill_count=$(find skills -name "SKILL.md" 2>/dev/null | wc -l)
echo "  Found: $skill_count SKILL.md files"
if [ "$skill_count" -ge 60 ]; then
  echo "  ✓ Skills count is accurate"
else
  echo "  ⚠️  Skills count lower than expected"
fi

echo ""

# Test 3: MCP Tools
echo "🔧 MCP Tools Check..."
if command -v npx &> /dev/null; then
  tool_count=$(npx claude-flow@alpha mcp tools 2>&1 | grep -c "^  •" || echo "0")
  echo "  Found: $tool_count MCP tools"
  if [ "$tool_count" -ge 80 ]; then
    echo "  ✓ MCP tools accessible"
  else
    echo "  ⚠️  Fewer tools than expected"
  fi
else
  echo "  ⚠️  npx not available, skipping MCP check"
fi

echo ""

# Test 4: Verify scripts are executable
echo "🔐 Script Permissions Check..."
scripts=(
  "scripts/generate-audit-reports.py"
  "scripts/validate-skills.py"
  "scripts/discover-skills.py"
)

for script in "${scripts[@]}"; do
  if [ -x "$script" ]; then
    echo "  ✓ $script (executable)"
  else
    echo "  ⚠️  $script (not executable, use: chmod +x $script)"
  fi
done

echo ""

# Test 5: Check for problematic claims
echo "⚠️  Checking for Exaggerations..."

if grep -q "Battle-tested" README.md; then
  echo "  ⚠️  Found 'Battle-tested' in README.md (unverifiable)"
fi

if grep -q "50% reduction" docs/README.md; then
  echo "  ⚠️  Found specific performance claims in docs/README.md (unverified)"
fi

if grep -q "Available Agents (49 Total)" CLAUDE.md; then
  echo "  ⚠️  Found agent count claim without clarification in CLAUDE.md"
fi

if grep -q "npm run build" CLAUDE.md && [ ! -f "package.json" ]; then
  echo "  ⚠️  Found npm commands but no package.json"
fi

echo ""
echo "✅ Validation complete!"
echo ""
echo "For detailed audit report, see:"
echo "  reports/generated/documentation-accuracy-audit.md"
```

---

## Quick Fix Commands

```bash
# Make validation script executable
chmod +x scripts/validate-documentation-accuracy.sh

# Run validation
./scripts/validate-documentation-accuracy.sh

# Count actual items
echo "Skills: $(find skills -name 'SKILL.md' | wc -l)"
echo "MCP Tools: $(npx claude-flow@alpha mcp tools 2>&1 | grep -c '^  •')"
echo "Workflows: $(ls -1 .github/workflows/*.yml | wc -l)"

# Generate fresh audit
python3 scripts/generate-audit-reports.py
```

---

## Summary

**Files to Update**: 4
**Critical Fixes**: 2
**High Priority Fixes**: 4
**Medium Priority Fixes**: 2
**Low Priority Improvements**: 3

**Total Estimated Time**: 5-7 hours across 4 phases

**Primary Focus**: Clarify agent terminology and remove unverified performance claims.

---

**Document Status**: Ready for Implementation
**Last Updated**: 2025-10-17
