# Skills.md Reversion Test Plan

**Test Framework Version**: 1.0
**Target Commit**: 68e0eb7e23d50ca666e82a544b48a788a57d9871
**Created**: 2025-10-25
**Purpose**: Validate complete reversion of skills.md refactor (a4b1ed1 → 68e0eb7)

## Executive Summary

This test plan ensures the safe reversion of commit a4b1ed1 ("major refactor to support skills.md") back to commit 68e0eb7 ("fix: apply pre-commit auto-formatting"). The plan uses a multi-phase validation approach with automated tests, manual verification, and rollback procedures.

## Test Phases

### Phase 1: Pre-Reversion Baseline

Establish current state metrics before making changes

### Phase 2: Reversion Execution

Execute the git revert with monitoring

### Phase 3: Post-Reversion Validation

Verify correct state after reversion

### Phase 4: Regression Testing

Ensure no unexpected side effects

### Phase 5: Rollback Verification

Validate recovery procedures work

---

## Phase 1: Pre-Reversion Baseline Tests

### 1.1 Current State Snapshot

**Test ID**: PRE-001
**Description**: Capture complete current state
**Commands**:

```bash
# Repository state
git log --oneline -5 > /tmp/reversion-baseline-commits.txt
git status --porcelain > /tmp/reversion-baseline-status.txt
git diff --stat 68e0eb7 HEAD > /tmp/reversion-baseline-diff.txt

# File structure
find . -type f -name "*.md" | grep -E "(skills|agents|archive)" | sort > /tmp/reversion-baseline-files.txt
find skills -name "SKILL.md" | wc -l > /tmp/reversion-baseline-skill-count.txt

# Directory structure
tree -L 3 --dirsfirst > /tmp/reversion-baseline-tree.txt 2>/dev/null || find . -type d | sort > /tmp/reversion-baseline-dirs.txt
```

**Expected**: Baseline files created in /tmp
**Pass Criteria**: All baseline files exist and contain data

### 1.2 CI/CD Pipeline Status

**Test ID**: PRE-002
**Description**: Verify CI/CD workflows are functional
**Commands**:

```bash
# Workflow syntax validation
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/lint-and-validate.yml'))"

# Check for required jobs
grep -E "(audit-gates|validate-anthropic-compliance|structure-audit)" .github/workflows/lint-and-validate.yml
```

**Expected**: YAML valid, all critical jobs present
**Pass Criteria**: No syntax errors, jobs found

### 1.3 Validation Scripts Baseline

**Test ID**: PRE-003
**Description**: Run all validation scripts to establish baseline
**Commands**:

```bash
# Run validation suite
python3 scripts/validate-skills.py --count-verify > /tmp/reversion-baseline-skills-validation.txt 2>&1
python3 scripts/validate-anthropic-compliance.py > /tmp/reversion-baseline-anthropic.txt 2>&1
python3 scripts/generate-audit-reports.py > /tmp/reversion-baseline-audit.txt 2>&1

# Capture exit codes
echo "Skills validation: $?" >> /tmp/reversion-baseline-exit-codes.txt
echo "Anthropic compliance: $?" >> /tmp/reversion-baseline-exit-codes.txt
echo "Audit reports: $?" >> /tmp/reversion-baseline-exit-codes.txt
```

**Expected**: Scripts run (may have failures)
**Pass Criteria**: Scripts execute without crashing

### 1.4 Repository Integrity

**Test ID**: PRE-004
**Description**: Check repository health
**Commands**:

```bash
# Check for uncommitted changes
git status --porcelain

# Verify no corruption
git fsck --full

# Check current branch
git rev-parse --abbrev-ref HEAD
```

**Expected**: No uncommitted changes, no corruption, on master
**Pass Criteria**: Clean working directory, fsck passes

### 1.5 Anthropic Skills Compliance

**Test ID**: PRE-005
**Description**: Capture current compliance metrics
**Commands**:

```bash
python3 scripts/validate-anthropic-compliance.py
grep "Compliant:" reports/generated/anthropic-compliance-report.md | tee /tmp/reversion-baseline-compliance.txt
```

**Expected**: Compliance report generated
**Pass Criteria**: Report exists with compliance percentage

---

## Phase 2: Reversion Execution Tests

### 2.1 Backup Creation

**Test ID**: REV-001
**Description**: Create safety backup before reversion
**Commands**:

```bash
# Create backup branch
git branch backup/pre-reversion-$(date +%Y%m%d-%H%M%S)

# Verify backup
git branch | grep backup/pre-reversion
```

**Expected**: Backup branch created
**Pass Criteria**: Branch exists and points to current HEAD

### 2.2 Reversion Execution

**Test ID**: REV-002
**Description**: Execute git revert
**Commands**:

```bash
# Perform revert
git revert --no-commit a4b1ed1

# Check status
git status --porcelain > /tmp/reversion-post-revert-status.txt
git diff --cached --stat > /tmp/reversion-post-revert-staged.txt
```

**Expected**: Revert staged, no conflicts
**Pass Criteria**: Staged changes present, no conflict markers

### 2.3 Conflict Resolution

**Test ID**: REV-003
**Description**: Handle any merge conflicts
**Commands**:

```bash
# Check for conflicts
git status | grep "Unmerged paths" && echo "CONFLICTS DETECTED" || echo "NO CONFLICTS"

# If conflicts exist, document them
git diff --check > /tmp/reversion-conflicts.txt 2>&1
```

**Expected**: Ideally no conflicts
**Pass Criteria**: If conflicts exist, all resolved before commit

---

## Phase 3: Post-Reversion Validation Tests

### 3.1 File Structure Verification

**Test ID**: POST-001
**Description**: Verify file structure matches 68e0eb7
**Commands**:

```bash
# Compare file lists
git ls-tree -r --name-only 68e0eb7 | sort > /tmp/reversion-target-files.txt
git ls-tree -r --name-only HEAD | sort > /tmp/reversion-actual-files.txt
diff /tmp/reversion-target-files.txt /tmp/reversion-actual-files.txt

# Check specific directories
test ! -d "skills" || echo "ERROR: skills/ directory still exists"
test ! -d "archive" || echo "ERROR: archive/ directory still exists"
test ! -d "agents" || echo "ERROR: agents/ directory still exists"
```

**Expected**: File lists match, refactor directories absent
**Pass Criteria**: No diff output, directories don't exist

### 3.2 Critical Files Restored

**Test ID**: POST-002
**Description**: Verify key files match target commit
**Commands**:

```bash
# Check CLAUDE.md
git diff 68e0eb7 HEAD -- CLAUDE.md || echo "CLAUDE.md matches"

# Check README.md
git diff 68e0eb7 HEAD -- README.md || echo "README.md matches"

# Check workflow file
git diff 68e0eb7 HEAD -- .github/workflows/lint-and-validate.yml || echo "Workflow matches"
```

**Expected**: No differences for critical files
**Pass Criteria**: All files match or show expected differences only

### 3.3 Broken Links Check

**Test ID**: POST-003
**Description**: Ensure no broken internal links
**Commands**:

```bash
python3 scripts/ensure-hub-links.py || true
python3 scripts/generate-audit-reports.py

# Check broken links count
grep "Broken links:" reports/generated/linkcheck.txt
grep "broken_links" reports/generated/structure-audit.json
```

**Expected**: Broken links = 0
**Pass Criteria**: Zero broken links reported

### 3.4 Orphan Pages Check

**Test ID**: POST-004
**Description**: Verify orphan count is within limits
**Commands**:

```bash
# Extract orphan count
python3 -c "import json; data=json.load(open('reports/generated/structure-audit.json')); print(f\"Orphans: {data.get('orphans', 'N/A')}\")"
```

**Expected**: Orphans ≤ 5
**Pass Criteria**: Orphan count within acceptable limit

### 3.5 Hub Violations Check

**Test ID**: POST-005
**Description**: Ensure hub structure compliance
**Commands**:

```bash
# Check hub violations
grep "hub_violations" reports/generated/structure-audit.json
```

**Expected**: Hub violations = 0
**Pass Criteria**: Zero hub violations

### 3.6 CI/CD Pipeline Validation

**Test ID**: POST-006
**Description**: Verify CI/CD workflows still functional
**Commands**:

```bash
# Validate workflow syntax
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/lint-and-validate.yml'))"

# Check critical jobs exist
for job in "audit-gates" "structure-audit" "link-check" "nist-quickstart"; do
    grep -q "^  $job:" .github/workflows/lint-and-validate.yml && echo "✅ $job" || echo "❌ $job MISSING"
done
```

**Expected**: YAML valid, all jobs present
**Pass Criteria**: All critical jobs found

---

## Phase 4: Regression Testing

### 4.1 Validation Scripts Functionality

**Test ID**: REG-001
**Description**: Ensure validation scripts still work
**Commands**:

```bash
# Run each validation script
python3 scripts/validate-skills.py && echo "✅ validate-skills" || echo "❌ validate-skills"
python3 scripts/generate-audit-reports.py && echo "✅ audit-reports" || echo "❌ audit-reports"
python3 scripts/validate-claims.py && echo "✅ validate-claims" || echo "❌ validate-claims"
```

**Expected**: Scripts execute successfully
**Pass Criteria**: All scripts run without fatal errors

### 4.2 Script Executability

**Test ID**: REG-002
**Description**: Verify all scripts have correct permissions
**Commands**:

```bash
# Check execute permissions
find scripts -name "*.py" -type f ! -perm -u+x > /tmp/reversion-non-executable.txt
cat /tmp/reversion-non-executable.txt
```

**Expected**: All .py scripts are executable
**Pass Criteria**: Empty output or only expected non-executables

### 4.3 Configuration Validity

**Test ID**: REG-003
**Description**: Validate all YAML/JSON configs
**Commands**:

```bash
# Validate YAML files
for yaml in $(find config -name "*.yaml" -o -name "*.yml"); do
    python3 -c "import yaml; yaml.safe_load(open('$yaml'))" && echo "✅ $yaml" || echo "❌ $yaml"
done

# Validate JSON files
for json in $(find reports/generated -name "*.json" 2>/dev/null); do
    python3 -c "import json; json.load(open('$json'))" && echo "✅ $json" || echo "❌ $json"
done
```

**Expected**: All configs valid
**Pass Criteria**: No syntax errors

### 4.4 Documentation Coherence

**Test ID**: REG-004
**Description**: Check documentation references are valid
**Commands**:

```bash
# Check for references to removed directories
grep -r "skills/" docs/ 2>/dev/null | grep -v "Binary" | wc -l
grep -r "archive/" docs/ 2>/dev/null | grep -v "Binary" | grep -v "old-migrations" | wc -l

# Check CLAUDE.md for orphaned references
grep -E "(skills/|@load skill:|61 active skills)" CLAUDE.md && echo "⚠️ Found skills references" || echo "✅ No skills references"
```

**Expected**: Minimal or zero references to removed content
**Pass Criteria**: No dangling references that break context

### 4.5 Concurrent Execution Tests

**Test ID**: REG-005
**Description**: Ensure concurrent operations still work
**Commands**:

```bash
# Test parallel script execution
python3 scripts/generate-audit-reports.py &
PID1=$!
python3 scripts/validate-skills.py &
PID2=$!

wait $PID1 && echo "✅ audit-reports completed" || echo "❌ audit-reports failed"
wait $PID2 && echo "✅ validate-skills completed" || echo "❌ validate-skills failed"
```

**Expected**: Both scripts complete successfully
**Pass Criteria**: Both scripts exit cleanly

---

## Phase 5: Rollback Tests

### 5.1 Backup Restoration

**Test ID**: ROLL-001
**Description**: Verify we can restore from backup
**Commands**:

```bash
# Switch to backup branch
CURRENT=$(git rev-parse HEAD)
BACKUP=$(git branch | grep backup/pre-reversion | head -1 | xargs)

git checkout "$BACKUP"
git log --oneline -1

# Return to reverted state
git checkout master
git log --oneline -1
```

**Expected**: Backup branch accessible, restoration works
**Pass Criteria**: Can switch to backup and back without errors

### 5.2 Revert the Revert (Emergency Recovery)

**Test ID**: ROLL-002
**Description**: Test emergency recovery procedure
**Commands**:

```bash
# Create test branch
git checkout -b test/revert-recovery

# Revert the revert (return to skills.md state)
git revert HEAD --no-commit

# Check status
git status --porcelain

# Cleanup
git checkout master
git branch -D test/revert-recovery
```

**Expected**: Can undo the reversion
**Pass Criteria**: Revert-revert succeeds without conflicts

### 5.3 State Recovery from Reports

**Test ID**: ROLL-003
**Description**: Verify audit reports enable state reconstruction
**Commands**:

```bash
# Check audit reports exist
test -f reports/generated/structure-audit.json && echo "✅ Audit data preserved" || echo "❌ Audit data missing"
test -f reports/generated/linkcheck.txt && echo "✅ Link data preserved" || echo "❌ Link data missing"

# Verify reports are usable
python3 -c "import json; data=json.load(open('reports/generated/structure-audit.json')); print(f\"Report timestamp: {data.get('timestamp', 'N/A')}\")"
```

**Expected**: Reports exist and are parseable
**Pass Criteria**: Reports accessible with valid data

---

## Test Execution Matrix

| Phase | Test ID | Priority | Automated | Manual | Blocking |
|-------|---------|----------|-----------|--------|----------|
| 1 | PRE-001 | HIGH | ✅ | ❌ | ✅ |
| 1 | PRE-002 | HIGH | ✅ | ❌ | ✅ |
| 1 | PRE-003 | HIGH | ✅ | ❌ | ❌ |
| 1 | PRE-004 | CRITICAL | ✅ | ❌ | ✅ |
| 1 | PRE-005 | MEDIUM | ✅ | ❌ | ❌ |
| 2 | REV-001 | CRITICAL | ✅ | ❌ | ✅ |
| 2 | REV-002 | CRITICAL | ✅ | ⚠️ | ✅ |
| 2 | REV-003 | HIGH | ⚠️ | ✅ | ✅ |
| 3 | POST-001 | CRITICAL | ✅ | ❌ | ✅ |
| 3 | POST-002 | CRITICAL | ✅ | ❌ | ✅ |
| 3 | POST-003 | HIGH | ✅ | ❌ | ✅ |
| 3 | POST-004 | HIGH | ✅ | ❌ | ✅ |
| 3 | POST-005 | HIGH | ✅ | ❌ | ✅ |
| 3 | POST-006 | HIGH | ✅ | ❌ | ✅ |
| 4 | REG-001 | HIGH | ✅ | ❌ | ❌ |
| 4 | REG-002 | MEDIUM | ✅ | ❌ | ❌ |
| 4 | REG-003 | MEDIUM | ✅ | ❌ | ❌ |
| 4 | REG-004 | HIGH | ✅ | ⚠️ | ❌ |
| 4 | REG-005 | MEDIUM | ✅ | ❌ | ❌ |
| 5 | ROLL-001 | HIGH | ✅ | ❌ | ❌ |
| 5 | ROLL-002 | HIGH | ✅ | ❌ | ❌ |
| 5 | ROLL-003 | MEDIUM | ✅ | ❌ | ❌ |

**Legend**:

- ✅ = Fully implemented
- ⚠️ = Partial/requires judgment
- ❌ = Not applicable/not implemented
- Blocking = Must pass before proceeding to next phase

---

## Pass/Fail Criteria

### Critical Success Criteria (MUST PASS)

1. **File Structure**: All files match target commit 68e0eb7
2. **Broken Links**: Zero broken internal links
3. **Hub Violations**: Zero hub structure violations
4. **Orphans**: ≤ 5 orphaned pages
5. **CI/CD**: All workflow jobs present and functional
6. **Backup**: Successful backup branch created

### Warning Criteria (INVESTIGATE BUT DON'T BLOCK)

1. **Orphan Count**: 3-5 orphans (acceptable but should be reviewed)
2. **Script Permissions**: Minor permission issues on non-critical scripts
3. **Documentation References**: Non-breaking references to old structure
4. **Regression Tests**: Non-critical script failures

### Failure Criteria (ABORT REVERSION)

1. **Merge Conflicts**: Unresolvable conflicts during revert
2. **Data Loss**: Critical files deleted or corrupted
3. **Broken Links**: > 0 broken internal links
4. **Hub Violations**: > 0 hub violations
5. **CI/CD Failure**: Critical jobs missing or broken
6. **Repository Corruption**: Git fsck failures

---

## Test Report Template

```markdown
# Reversion Test Execution Report

**Date**: YYYY-MM-DD HH:MM:SS
**Executor**: [Name]
**Commit Before**: [hash]
**Commit After**: [hash]

## Phase 1: Pre-Reversion Baseline
- [ ] PRE-001: Current state snapshot - PASS/FAIL
- [ ] PRE-002: CI/CD pipeline status - PASS/FAIL
- [ ] PRE-003: Validation scripts baseline - PASS/FAIL
- [ ] PRE-004: Repository integrity - PASS/FAIL
- [ ] PRE-005: Anthropic compliance - PASS/FAIL

## Phase 2: Reversion Execution
- [ ] REV-001: Backup creation - PASS/FAIL
- [ ] REV-002: Reversion execution - PASS/FAIL
- [ ] REV-003: Conflict resolution - PASS/FAIL/N/A

## Phase 3: Post-Reversion Validation
- [ ] POST-001: File structure verification - PASS/FAIL
- [ ] POST-002: Critical files restored - PASS/FAIL
- [ ] POST-003: Broken links check - PASS/FAIL
- [ ] POST-004: Orphan pages check - PASS/FAIL
- [ ] POST-005: Hub violations check - PASS/FAIL
- [ ] POST-006: CI/CD pipeline validation - PASS/FAIL

## Phase 4: Regression Testing
- [ ] REG-001: Validation scripts functionality - PASS/FAIL
- [ ] REG-002: Script executability - PASS/FAIL
- [ ] REG-003: Configuration validity - PASS/FAIL
- [ ] REG-004: Documentation coherence - PASS/FAIL
- [ ] REG-005: Concurrent execution - PASS/FAIL

## Phase 5: Rollback Tests
- [ ] ROLL-001: Backup restoration - PASS/FAIL
- [ ] ROLL-002: Revert the revert - PASS/FAIL
- [ ] ROLL-003: State recovery - PASS/FAIL

## Summary
**Total Tests**: 23
**Passed**: X
**Failed**: Y
**Warnings**: Z
**Overall Result**: PASS/FAIL

## Issues Encountered
[List any issues and resolutions]

## Recommendations
[Any follow-up actions needed]
```

---

## Automation Notes

- All commands in this plan are designed for bash execution
- Tests can be run individually or via automation script
- Exit codes: 0 = pass, non-zero = fail
- Output files stored in /tmp for inspection
- Critical tests must pass before proceeding to next phase

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-10-25 | Initial test plan | Tester Agent |
