# Skills Reversion Runbook

**Purpose**: Operational procedures for reverting skills.md refactor (commit a4b1ed1)
**Status**: Active
**Last Updated**: 2025-10-25
**Owner**: DevOps / SRE Team

---

## Quick Reference

**What**: Revert commit a4b1ed1 ("major refactor to support skills.md") → commit 68e0eb7
**Why**: Repository already 100% compliant; refactor added unnecessary complexity
**When**: As soon as practical
**Who**: Any developer with repository write access
**How Long**: 2-3 hours (preparation + execution + verification)

**Related Docs**:
- Full Context: [REVERSION_GUIDE.md](../guides/REVERSION_GUIDE.md)
- Decision Record: [ADR-SKILLS-REVERSION.md](../decisions/ADR-SKILLS-REVERSION.md)
- State Notes: [POST-REVERSION-STATE.md](../notes/POST-REVERSION-STATE.md)

---

## Pre-Flight Checklist

Before starting reversion, verify:

- [ ] Git repository is clean: `git status` → no uncommitted changes
- [ ] Current branch is main/master: `git branch --show-current`
- [ ] Local repo is up-to-date: `git pull origin master`
- [ ] You have write access: `git push --dry-run`
- [ ] Backup branch does NOT exist: `git branch -a | grep backup/pre-reversion-state` → empty
- [ ] No active PRs will conflict with reversion: `gh pr list --state open`
- [ ] Team notified of pending reversion (if team workflow requires)

**Estimated Time**: 10 minutes

---

## Reversion Procedure

### Phase 1: Backup Current State (10 minutes)

**Purpose**: Preserve a4b1ed1 state for future reference

**Commands**:
```bash
# 1. Verify you're on the post-refactor commit
git log -1 --oneline
# Expected output contains: a4b1ed1 or later commit

# 2. Create backup branch from current HEAD
git checkout -b backup/pre-reversion-state

# 3. Push backup branch to remote
git push -u origin backup/pre-reversion-state

# 4. Tag the refactor commit for easy reference
git tag -a legacy/skills-md-refactor a4b1ed1 \
  -m "skills.md refactor (preserved for reference, reverted in production)"

# 5. Push tag
git push origin legacy/skills-md-refactor

# 6. Verify backup exists
git branch -a | grep backup/pre-reversion-state
# Expected: remotes/origin/backup/pre-reversion-state

git tag -l | grep legacy/skills-md-refactor
# Expected: legacy/skills-md-refactor
```

**Verification**:
```bash
# Confirm backup branch matches current state
CURRENT_COMMIT=$(git rev-parse HEAD)
BACKUP_COMMIT=$(git rev-parse backup/pre-reversion-state)
if [ "$CURRENT_COMMIT" = "$BACKUP_COMMIT" ]; then
  echo "✅ Backup successful"
else
  echo "❌ Backup failed - investigate before proceeding"
  exit 1
fi
```

**Troubleshooting**:

| Issue | Cause | Solution |
|-------|-------|----------|
| Branch already exists | Previous reversion attempt | Delete: `git branch -D backup/pre-reversion-state` |
| Push rejected | Permission issue | Verify GitHub credentials, check repo access |
| Tag already exists | Previous tag | Delete: `git tag -d legacy/skills-md-refactor` |

**Success Criteria**:
- [ ] backup/pre-reversion-state branch created and pushed
- [ ] legacy/skills-md-refactor tag created and pushed
- [ ] Backup commit matches current HEAD

---

### Phase 2: Create Reversion Branch (5 minutes)

**Purpose**: Work on separate branch for clean PR workflow

**Commands**:
```bash
# 1. Return to master
git checkout master

# 2. Pull latest (in case of concurrent updates)
git pull origin master

# 3. Create reversion working branch
git checkout -b revert/skills-md-refactor

# 4. Verify branch creation
git branch --show-current
# Expected: revert/skills-md-refactor
```

**Verification**:
```bash
git branch --show-current
# Output: revert/skills-md-refactor

git log -1 --oneline
# Output should show post-a4b1ed1 state (same as master)
```

**Success Criteria**:
- [ ] On revert/skills-md-refactor branch
- [ ] Branch matches current master state

---

### Phase 3: Identify Last Known Good Commit (5 minutes)

**Purpose**: Confirm target reversion commit (68e0eb7)

**Commands**:
```bash
# 1. View commits before and including a4b1ed1
git log --oneline --graph a4b1ed1~5..a4b1ed1

# Expected output (example):
# a4b1ed1 major refactor to support skills.md
# 68e0eb7 fix: apply pre-commit auto-formatting  ← TARGET
# 0db62b2 docs: resolve 5 orphans by creating reports directory README
# ...

# 2. Verify 68e0eb7 state
git show 68e0eb7:CLAUDE.md | head -20
# Verify this shows pre-refactor CLAUDE.md content

# 3. Check skills count at 68e0eb7
git show 68e0eb7:skills/ | grep -c "SKILL.md" || \
  git ls-tree -r --name-only 68e0eb7 skills/ | grep -c "SKILL.md"
# Expected: 61

# 4. Verify no REFERENCE.md files at 68e0eb7
git ls-tree -r --name-only 68e0eb7 skills/ | grep -c "REFERENCE.md"
# Expected: 0
```

**Verification Questions**:
- [ ] Does commit 68e0eb7 exist? `git cat-file -t 68e0eb7` → commit
- [ ] Is 68e0eb7 before a4b1ed1? `git merge-base --is-ancestor 68e0eb7 a4b1ed1 && echo yes`
- [ ] Does 68e0eb7 have 61 SKILL.md files?
- [ ] Does 68e0eb7 have 0 REFERENCE.md files?
- [ ] Does 68e0eb7 pre-commit pass? (check CI history or git notes)

**Success Criteria**:
- [ ] Commit 68e0eb7 verified as last known good
- [ ] 68e0eb7 state contains 61 SKILL.md files, 0 REFERENCE.md files
- [ ] 68e0eb7 is ancestor of current HEAD

---

### Phase 4: Execute Hard Revert (15 minutes)

**Purpose**: Reset repository to 68e0eb7 state

**Commands**:
```bash
# 1. Ensure on revert/skills-md-refactor branch
git branch --show-current
# Expected: revert/skills-md-refactor

# 2. Hard reset to target commit
git reset --hard 68e0eb7

# 3. Verify HEAD now at 68e0eb7
git log -1 --oneline
# Expected: 68e0eb7 fix: apply pre-commit auto-formatting

# 4. Create reversion commit for clarity
git commit --allow-empty -m "Revert 'major refactor to support skills.md'

This reverts commit a4b1ed1 (major refactor to support skills.md).

Reason: Repository was already 100% Anthropic compliant (61/61 skills)
before the refactor. The skills.md migration introduced unnecessary
complexity:
- 278 files changed (47,544 net lines added)
- 18 new scripts (5,333 lines)
- Dual format system (SKILL.md + skills.md)
- Complex validation infrastructure
- Extensive archive reorganization

All functionality from a4b1ed1 is preserved in branch:
  backup/pre-reversion-state

Tag for reference:
  legacy/skills-md-refactor

Reverting to commit 68e0eb7: 'fix: apply pre-commit auto-formatting'
Repository state: 61/61 skills compliant, all tests passing.

See docs/guides/REVERSION_GUIDE.md for full rationale.
See docs/decisions/ADR-SKILLS-REVERSION.md for decision record.
"
```

**Verification Commands**:
```bash
# File counts
echo "=== Verification ==="

echo "Skills count:"
find skills -name "SKILL.md" | wc -l
# Expected: 61

echo "REFERENCE.md count (should be 0):"
find skills -name "REFERENCE.md" | wc -l
# Expected: 0

echo "Scripts count:"
find scripts -name "*.py" | wc -l
# Expected: ~10-12

echo "Docs directories:"
ls -1 docs/
# Expected: core, guides, nist, standards (no architecture, optimization, research, scripts)

echo "Archive directory:"
ls -d archive/ 2>&1 || echo "Not found (expected)"
# Expected: "Not found" or pre-a4b1ed1 content only
```

**Success Criteria**:
- [ ] HEAD at 68e0eb7
- [ ] 61 SKILL.md files present
- [ ] 0 REFERENCE.md files
- [ ] ~10-12 scripts (not 28)
- [ ] 4 docs directories (not 8)
- [ ] Reversion commit created with full context

**Troubleshooting**:

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Reset fails | Error: "pathspec did not match" | Verify commit hash: `git rev-parse 68e0eb7` |
| Uncommitted changes | Error: "Cannot reset" | Stash first: `git stash`, then retry |
| Wrong commit reset | File counts don't match expected | Re-run: `git reset --hard 68e0eb7` |

---

### Phase 5: Create Reversion Documentation (30 minutes)

**Purpose**: Document reversion context for future reference

**Directory Setup**:
```bash
# Create documentation directories if needed
mkdir -p docs/decisions
mkdir -p docs/runbooks
mkdir -p docs/notes
```

**Files to Create** (use templates or copy from backup):

1. **docs/guides/REVERSION_GUIDE.md** (~15 minutes)
   - Comprehensive reversion context
   - What changed in a4b1ed1
   - Why revert
   - Lessons learned
   - Template: See backup branch or create from scratch

2. **docs/decisions/ADR-SKILLS-REVERSION.md** (~10 minutes)
   - Formal decision record
   - Options considered
   - Decision rationale
   - Template: See backup branch or create from scratch

3. **docs/runbooks/SKILLS-REVERSION-RUNBOOK.md** (~5 minutes)
   - This file (operational procedures)
   - Quick reference commands
   - Verification steps

4. **docs/notes/POST-REVERSION-STATE.md** (~5 minutes)
   - Current state summary
   - Quick reference
   - Validation commands

**Commit Documentation**:
```bash
# Add all reversion docs
git add docs/guides/REVERSION_GUIDE.md
git add docs/decisions/ADR-SKILLS-REVERSION.md
git add docs/runbooks/SKILLS-REVERSION-RUNBOOK.md
git add docs/notes/POST-REVERSION-STATE.md

# Update CHANGELOG if exists
if [ -f CHANGELOG.md ]; then
  echo "
## [Unreleased] - 2025-10-25

### Reverted
- Major skills.md refactor (commit a4b1ed1) - restored to 68e0eb7 state
- Reason: Repository already 100% Anthropic compliant; refactor added unnecessary complexity
- Documentation: docs/guides/REVERSION_GUIDE.md
- Backup: backup/pre-reversion-state branch
" >> CHANGELOG.md
  git add CHANGELOG.md
fi

# Commit documentation
git commit -m "docs: add comprehensive reversion documentation

Documents reversion of commit a4b1ed1 (skills.md refactor) to commit 68e0eb7.

Added:
- REVERSION_GUIDE.md: Full context and rationale
- ADR-SKILLS-REVERSION.md: Formal decision record
- SKILLS-REVERSION-RUNBOOK.md: Operational procedures
- POST-REVERSION-STATE.md: Current state notes
- CHANGELOG.md: Reversion entry (if CHANGELOG exists)

Provides comprehensive context for:
- Why the reversion was necessary
- What was changed in a4b1ed1
- How to verify post-reversion state
- Lessons learned
- Future considerations
"
```

**Verification**:
```bash
# Verify all docs created
ls -lh docs/guides/REVERSION_GUIDE.md
ls -lh docs/decisions/ADR-SKILLS-REVERSION.md
ls -lh docs/runbooks/SKILLS-REVERSION-RUNBOOK.md
ls -lh docs/notes/POST-REVERSION-STATE.md

# Verify commit
git log -2 --oneline
# Expected:
# <hash> docs: add comprehensive reversion documentation
# <hash> Revert 'major refactor to support skills.md'
```

**Success Criteria**:
- [ ] All 4 reversion docs created
- [ ] CHANGELOG.md updated (if exists)
- [ ] Documentation committed with clear message
- [ ] Git log shows 2 commits: reversion + documentation

---

### Phase 6: Comprehensive Verification (20 minutes)

**Purpose**: Confirm repository in expected post-reversion state

**Verification Script**:
```bash
#!/bin/bash
# reversion-verification.sh

echo "=== Skills Reversion Verification ==="
echo "Date: $(date)"
echo ""

# Skills count
SKILLS_COUNT=$(find skills -name "SKILL.md" | wc -l)
echo "✓ Skills count: $SKILLS_COUNT (expected: 61)"
if [ "$SKILLS_COUNT" -ne 61 ]; then
  echo "  ❌ FAIL: Expected 61 skills"
  exit 1
fi

# REFERENCE.md count (should be 0)
REF_COUNT=$(find skills -name "REFERENCE.md" 2>/dev/null | wc -l)
echo "✓ REFERENCE.md count: $REF_COUNT (expected: 0)"
if [ "$REF_COUNT" -ne 0 ]; then
  echo "  ❌ FAIL: REFERENCE.md files should not exist"
  exit 1
fi

# Scripts count
SCRIPTS_COUNT=$(find scripts -name "*.py" | wc -l)
echo "✓ Scripts count: $SCRIPTS_COUNT (expected: 10-12)"
if [ "$SCRIPTS_COUNT" -gt 15 ]; then
  echo "  ⚠️  WARN: More scripts than expected (may include new reversion scripts)"
fi

# Docs directories
DOCS_DIRS=$(ls -1 docs/ | wc -l)
echo "✓ Docs directories: $DOCS_DIRS"
ls -1 docs/
if [ -d docs/architecture ] || [ -d docs/optimization ]; then
  echo "  ❌ FAIL: Should not have architecture or optimization directories"
  exit 1
fi

# Anthropic compliance
echo ""
echo "=== Running Anthropic Compliance Check ==="
if [ -f scripts/validate-anthropic-compliance.py ]; then
  python3 scripts/validate-anthropic-compliance.py
else
  echo "⚠️  WARN: validate-anthropic-compliance.py not found"
fi

# Pre-commit hooks
echo ""
echo "=== Running Pre-commit Hooks ==="
if command -v pre-commit &> /dev/null; then
  pre-commit run --all-files || echo "⚠️  WARN: Some pre-commit checks failed"
else
  echo "⚠️  WARN: pre-commit not installed"
fi

# Git verification
echo ""
echo "=== Git State ==="
echo "Current HEAD:"
git log -1 --oneline

echo ""
echo "Backup branch exists:"
git branch -a | grep backup/pre-reversion-state || echo "❌ FAIL: Backup branch missing"

echo ""
echo "Tag exists:"
git tag -l | grep legacy/skills-md-refactor || echo "❌ FAIL: Tag missing"

# Reversion docs
echo ""
echo "=== Reversion Documentation ==="
for doc in \
  docs/guides/REVERSION_GUIDE.md \
  docs/decisions/ADR-SKILLS-REVERSION.md \
  docs/runbooks/SKILLS-REVERSION-RUNBOOK.md \
  docs/notes/POST-REVERSION-STATE.md
do
  if [ -f "$doc" ]; then
    echo "✓ $doc exists"
  else
    echo "❌ $doc missing"
  fi
done

echo ""
echo "=== Verification Complete ==="
```

**Run Verification**:
```bash
chmod +x reversion-verification.sh
./reversion-verification.sh
```

**Manual Checks**:
```bash
# Sample skill file structure
cat skills/coding-standards/python/SKILL.md | head -20
# Should show: YAML frontmatter, 3-level structure

# Product matrix loading
python3 scripts/skill-loader.py load product:api
# Should work without errors

# Git history preserved
git log --oneline | grep a4b1ed1
# Should show a4b1ed1 still in history (not deleted)
```

**Success Criteria**:
- [ ] All automated checks pass
- [ ] 61/61 skills compliant
- [ ] Pre-commit hooks pass
- [ ] Sample skills have expected structure
- [ ] skill-loader.py works
- [ ] Git history intact
- [ ] All reversion docs present

**Troubleshooting**:

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Compliance fails | <61 skills compliant | Investigate which skills changed, re-run revert |
| Pre-commit fails | Formatting issues | Run `pre-commit run --all-files` and commit fixes |
| skill-loader broken | Import errors | Verify Python environment, check requirements.txt |
| Missing docs | Reversion docs not found | Re-create from templates or backup branch |

---

### Phase 7: Push and PR (15 minutes)

**Purpose**: Submit reversion for review and merge

**Commands**:
```bash
# 1. Push reversion branch
git push -u origin revert/skills-md-refactor

# 2. Create pull request
gh pr create \
  --title "Revert skills.md refactor (a4b1ed1 → 68e0eb7)" \
  --body "## Summary

Reverts commit a4b1ed1 ('major refactor to support skills.md') back to
commit 68e0eb7 (last known good state before refactor).

## Rationale

1. **Already Compliant**: Repository was 100% Anthropic compliant before refactor
   - Evidence: \`python3 scripts/validate-anthropic-compliance.py\` → 61/61 (100%)

2. **Scope Creep**: 278 files changed, 47,544 net lines added
   - 18 new scripts (5,333 lines)
   - Dual format system introduced
   - Extensive test/documentation overhaul

3. **Unnecessary Complexity**: No documented production requirement
   - No GitHub issues requesting skills.md support
   - No external integration requirement proven
   - Current SKILL.md format working perfectly

4. **No Production Need**: No user reports of incompatibility

## What Changed

**Removed**:
- 18 REFERENCE.md files (extracted Level 3 content)
- 18 new scripts (analyze, validate, optimize, migrate)
- 4 new documentation directories (architecture, optimization, research, scripts)
- 30+ report files
- 2 new CI/CD workflows
- Extensive test suite additions

**Preserved**:
- All 61 SKILL.md files (back to 68e0eb7 state)
- 100% Anthropic compliance (61/61)
- skill-loader.py functionality
- Product matrix integration
- Original validation scripts
- Pre-commit hooks

**Added**:
- Comprehensive reversion documentation (4 files)
- Backup branch: backup/pre-reversion-state
- Tag: legacy/skills-md-refactor

## Verification

- ✅ 61/61 skills present and compliant
- ✅ All pre-commit hooks pass
- ✅ No breaking changes to existing workflows
- ✅ Validation scripts working
- ✅ Product matrix functional
- ✅ skill-loader.py works correctly

## Documentation

Full context in:
- docs/guides/REVERSION_GUIDE.md (comprehensive overview)
- docs/decisions/ADR-SKILLS-REVERSION.md (decision record)
- docs/runbooks/SKILLS-REVERSION-RUNBOOK.md (operational procedures)
- docs/notes/POST-REVERSION-STATE.md (quick reference)

## Backup

Original a4b1ed1 state preserved:
- Branch: backup/pre-reversion-state
- Tag: legacy/skills-md-refactor

## Testing Checklist

- [ ] All 61 SKILL.md files present
- [ ] \`validate-anthropic-compliance.py\` passes (61/61)
- [ ] \`skill-loader.py load product:api\` works
- [ ] Pre-commit hooks pass
- [ ] No REFERENCE.md files exist
- [ ] scripts/ directory contains <15 files
- [ ] docs/ structure matches pre-refactor (4 base directories)
- [ ] Reversion documentation complete (4 files)
- [ ] Backup branch and tag created

## Rollback Plan

If this reversion causes issues:
1. Merge backup/pre-reversion-state branch
2. Verify with: \`git diff a4b1ed1 HEAD\` → should show no diff

## Stakeholders

@team-leads @maintainers (update with actual GitHub handles)
" \
  --label "reversion,documentation" \
  --assignee @me

# 3. Get PR URL
PR_URL=$(gh pr view --json url -q .url)
echo "PR created: $PR_URL"
```

**Alternative (Manual PR Creation)**:
```bash
# If gh CLI not available, create PR manually:
git push -u origin revert/skills-md-refactor
echo "Visit: https://github.com/williamzujkowski/standards/compare/revert/skills-md-refactor"
# Then fill in PR template with body content from gh pr create command above
```

**PR Checklist** (ensure these are checked in PR):
- [ ] Title clearly states reversion intent
- [ ] Body explains rationale comprehensively
- [ ] Verification section shows all checks passed
- [ ] Documentation references included
- [ ] Backup strategy documented
- [ ] Testing checklist complete
- [ ] Labels applied (reversion, documentation)
- [ ] Assignees added
- [ ] Linked to related issues (if any)

**Success Criteria**:
- [ ] PR created successfully
- [ ] PR URL accessible
- [ ] PR body contains full context
- [ ] All checklists included
- [ ] Team notified (via PR mention or separate communication)

---

## Post-Merge Actions (10 minutes)

**After PR Merged**:

```bash
# 1. Pull updated master
git checkout master
git pull origin master

# 2. Verify merge successful
git log -3 --oneline
# Should show reversion commits

# 3. Run final verification
python3 scripts/validate-anthropic-compliance.py
# Expected: 61/61 (100%)

# 4. Tag production state
git tag -a stable/post-reversion-2025-10-25 \
  -m "Stable state after skills.md refactor reversion"
git push origin stable/post-reversion-2025-10-25

# 5. Clean up local branches (optional)
git branch -d revert/skills-md-refactor
git branch -d backup/pre-reversion-state  # Keep remote, delete local
```

**Team Communication Template**:
```markdown
Subject: Skills.md Refactor Reverted - Repository Returned to Stable State

Team,

The skills.md refactor (commit a4b1ed1) has been successfully reverted.

**Current State**:
- Repository at commit 68e0eb7 (pre-refactor stable state)
- 61/61 skills Anthropic compliant (100%)
- All validation scripts functional
- No breaking changes to existing workflows

**Why Revert**:
- Repository was already 100% compliant before refactor
- No production requirement for dual format system
- Refactor added significant complexity without clear benefit

**What's Preserved**:
- Backup branch: backup/pre-reversion-state
- Tag: legacy/skills-md-refactor
- Full documentation: docs/guides/REVERSION_GUIDE.md

**Action Required**:
- Pull latest master: `git checkout master && git pull`
- If you had local work based on a4b1ed1, see: docs/guides/REVERSION_GUIDE.md#impact-on-in-flight-work

**Questions**: See comprehensive FAQ in docs/guides/REVERSION_GUIDE.md or ask in #dev-standards

Thanks,
[Your Name]
```

**Success Criteria**:
- [ ] Master branch updated
- [ ] Final verification passes
- [ ] Production tag created
- [ ] Team notified
- [ ] Local cleanup done

---

## Rollback Procedure (Emergency)

**If Reversion Causes Unexpected Issues**:

```bash
# EMERGENCY ROLLBACK - Return to a4b1ed1 state

# 1. Verify problem
echo "Document the issue:"
# [Describe what broke]

# 2. Immediate rollback
git checkout master
git merge backup/pre-reversion-state

# 3. Verify rollback
git log -1 --oneline
# Should show a4b1ed1 or later commit

# 4. Verify system health
python3 scripts/validate-anthropic-compliance.py
# Should pass

# 5. Create incident report
cat > incident-report.md << 'EOF'
# Reversion Rollback Incident Report

**Date**: $(date)
**Issue**: [Describe what broke after reversion]
**Impact**: [Describe user/system impact]
**Root Cause**: [Why reversion caused issue]
**Resolution**: Rolled back to pre-reversion state (a4b1ed1)
**Next Steps**: [Investigate before attempting reversion again]
EOF

# 6. Notify team
gh issue create --title "Reversion Rollback Required" \
  --body "$(cat incident-report.md)" \
  --label "incident,high-priority"
```

**Rollback Verification**:
```bash
# Confirm state matches a4b1ed1
git diff a4b1ed1 HEAD
# Should show no differences (or only new incident report)

# Confirm functionality restored
python3 scripts/validate-anthropic-compliance.py
python3 scripts/skill-loader.py load product:api
pre-commit run --all-files
```

**Success Criteria**:
- [ ] System restored to pre-reversion state
- [ ] All functionality verified working
- [ ] Incident documented
- [ ] Team notified
- [ ] Investigation plan created

---

## Troubleshooting Guide

### Common Issues

#### Issue 1: Merge Conflicts During PR

**Symptoms**: PR shows merge conflicts with master

**Cause**: Master branch updated after reversion branch created

**Solution**:
```bash
# Update reversion branch with latest master
git checkout revert/skills-md-refactor
git fetch origin
git merge origin/master

# Resolve conflicts (favor reversion state for most files)
# For new files in master not in 68e0eb7: keep them
# For modified files: prefer 68e0eb7 version

git add .
git commit -m "Merge master into reversion branch, resolve conflicts"
git push origin revert/skills-md-refactor
```

#### Issue 2: Pre-commit Hooks Fail After Revert

**Symptoms**: `pre-commit run --all-files` fails on reverted code

**Cause**: Pre-commit config changed between 68e0eb7 and current

**Solution**:
```bash
# Check if .pre-commit-config.yaml changed
git diff 68e0eb7 HEAD -- .pre-commit-config.yaml

# Option 1: Update code to pass new hooks
pre-commit run --all-files
# Fix reported issues
git add .
git commit -m "fix: apply current pre-commit standards to reverted code"

# Option 2: Revert .pre-commit-config.yaml too (if hooks changed in a4b1ed1)
git checkout 68e0eb7 -- .pre-commit-config.yaml
git commit -m "revert: restore pre-refactor pre-commit config"
```

#### Issue 3: skill-loader.py Broken After Revert

**Symptoms**: `python3 scripts/skill-loader.py load product:api` fails

**Cause**: Dependencies changed between versions

**Solution**:
```bash
# Check if requirements.txt changed
git diff 68e0eb7 HEAD -- requirements.txt

# If yes, revert requirements.txt
git checkout 68e0eb7 -- requirements.txt
pip install -r requirements.txt

# Re-test
python3 scripts/skill-loader.py load product:api

# If still fails, check skill-loader.py itself
git diff 68e0eb7 HEAD -- scripts/skill-loader.py
# If changed in a4b1ed1, revert it too
git checkout 68e0eb7 -- scripts/skill-loader.py
```

#### Issue 4: Compliance Validation Returns <61 Skills

**Symptoms**: `validate-anthropic-compliance.py` shows <61 compliant skills

**Cause**: Incomplete revert or validation script changed

**Solution**:
```bash
# 1. Verify skills count
find skills -name "SKILL.md" | wc -l
# If not 61, revert was incomplete

# 2. Re-run hard reset
git reset --hard 68e0eb7

# 3. Check validation script
git diff 68e0eb7 HEAD -- scripts/validate-anthropic-compliance.py
# If changed, revert it
git checkout 68e0eb7 -- scripts/validate-anthropic-compliance.py

# 4. Re-test
python3 scripts/validate-anthropic-compliance.py
```

#### Issue 5: Documentation Build Fails

**Symptoms**: `mkdocs build` fails after reversion

**Cause**: mkdocs.yml references removed files

**Solution**:
```bash
# Check if mkdocs.yml changed
git diff 68e0eb7 HEAD -- mkdocs.yml

# If it references new files from a4b1ed1, revert mkdocs.yml
git checkout 68e0eb7 -- mkdocs.yml

# Re-test
mkdocs build

# If still fails, check nav section for broken links
mkdocs build 2>&1 | grep "WARNING"
# Remove or fix broken references
```

---

## Time Estimates

| Phase | Estimated Time | Dependencies |
|-------|----------------|--------------|
| Pre-flight checklist | 10 min | None |
| Phase 1: Backup | 10 min | None |
| Phase 2: Reversion branch | 5 min | Phase 1 |
| Phase 3: Identify commit | 5 min | None |
| Phase 4: Hard revert | 15 min | Phase 2, 3 |
| Phase 5: Documentation | 30 min | Phase 4 |
| Phase 6: Verification | 20 min | Phase 4, 5 |
| Phase 7: Push & PR | 15 min | Phase 6 |
| **Total** | **~2 hours** | Sequential |

**Buffer Time**: Add 50% (1 hour) for unexpected issues → **3 hours total**

**Parallel Opportunities**: Phases 3 and 5 can be prepared in advance

---

## Success Metrics

### Immediate Success (Day 0)

- [ ] PR merged successfully
- [ ] All validation scripts pass (100%)
- [ ] No user-reported issues
- [ ] Team notified and aware

### Short-term Success (Week 1)

- [ ] No regressions reported
- [ ] skill-loader.py usage unchanged
- [ ] Documentation builds successfully
- [ ] CI/CD pipelines pass

### Long-term Success (Month 1)

- [ ] Compliance maintained at 100%
- [ ] No skills.md requirement emerged
- [ ] Reduced maintenance burden confirmed
- [ ] Team satisfied with decision

**Failure Indicators**:
- User reports of skill loading failures
- Compliance drops below 95%
- External requirement for skills.md emerges within 1 month
- Significant rework required post-reversion

---

## Appendix: Quick Command Reference

### Verification Commands

```bash
# Skills count
find skills -name "SKILL.md" | wc -l  # Expected: 61

# REFERENCE.md count
find skills -name "REFERENCE.md" | wc -l  # Expected: 0

# Scripts count
find scripts -name "*.py" | wc -l  # Expected: ~10-12

# Docs structure
ls -1 docs/  # Expected: core, guides, nist, standards

# Compliance
python3 scripts/validate-anthropic-compliance.py  # Expected: 61/61 (100%)

# Pre-commit
pre-commit run --all-files  # Expected: All checks pass

# skill-loader
python3 scripts/skill-loader.py load product:api  # Expected: Works

# Git state
git log -1 --oneline  # Should show reversion commit
git branch -a | grep backup/pre-reversion-state  # Should exist
git tag -l | grep legacy/skills-md-refactor  # Should exist
```

### Rollback Commands

```bash
# Emergency rollback to a4b1ed1 state
git checkout master
git merge backup/pre-reversion-state
git push origin master

# Verify rollback
git log -1 --oneline  # Should show a4b1ed1 or later
python3 scripts/validate-anthropic-compliance.py  # Should pass
```

### Cleanup Commands

```bash
# After successful reversion, clean up local branches
git checkout master
git pull origin master
git branch -d revert/skills-md-refactor
git branch -d backup/pre-reversion-state  # Deletes local only, remote preserved
```

---

## Document Maintenance

**Update Triggers**:
- Reversion procedure changes
- New troubleshooting scenarios identified
- Team feedback on clarity
- Post-mortem findings

**Review Schedule**:
- Immediately after first use
- 1 month post-reversion
- Annually (or when referenced)

**Owner**: DevOps / SRE Team

**Last Updated**: 2025-10-25

**Version**: 1.0.0
