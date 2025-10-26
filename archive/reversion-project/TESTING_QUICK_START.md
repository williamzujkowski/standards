# Reversion Testing Quick Start Guide

**Version**: 1.0
**Purpose**: Fast-track guide for executing reversion validation tests

## TL;DR - One Command Test Execution

```bash
# Run full automated test suite
./scripts/run-reversion-tests.sh

# Review results
cat tests/reversion-test-report-*.md
```

---

## Prerequisites

1. **Clean Working Directory**:
   ```bash
   git status
   # Should show: "nothing to commit, working tree clean"
   ```

2. **Required Tools**:
   ```bash
   # Python 3.11+
   python3 --version

   # YAML support
   python3 -c "import yaml"

   # Git
   git --version
   ```

3. **Location**:
   ```bash
   # Must be in repository root
   cd /home/william/git/standards
   ```

---

## Test Execution Modes

### Mode 1: Full Automated Test (Recommended)

**Purpose**: Complete validation without executing actual reversion

```bash
# Run all test phases in dry-run mode
./scripts/run-reversion-tests.sh

# Check results
echo $?  # 0 = pass, non-zero = fail

# View report
ls -lt tests/reversion-test-report-*.md | head -1
```

**What it does**:
- ✅ Captures current state baseline
- ✅ Creates backup branch
- ✅ Tests reversion feasibility (dry-run)
- ✅ Validates recovery procedures
- ✅ Generates comprehensive report
- ❌ Does NOT actually execute reversion

**Duration**: 2-5 minutes

### Mode 2: Full Test with Actual Reversion

**Purpose**: Execute reversion and validate results

```bash
# WARNING: This will modify the repository!
# Set flag to execute actual reversion
export EXECUTE_REVERSION=true

# Run tests
./scripts/run-reversion-tests.sh

# Review report
cat tests/reversion-test-report-*.md
```

**What it does**:
- ✅ Everything from Mode 1
- ✅ Actually executes `git revert a4b1ed1`
- ✅ Validates post-reversion state
- ✅ Tests all regression scenarios

**Duration**: 3-7 minutes

⚠️ **WARNING**: This modifies your repository. Ensure you have backups.

### Mode 3: Manual Test Execution

**Purpose**: Run specific test phases manually

```bash
# Phase 1: Baseline only
./scripts/run-reversion-tests.sh | grep -A 100 "Phase 1"

# Or run specific tests manually (see Manual Testing section)
```

---

## Understanding Test Results

### Exit Codes

```bash
0  = All critical tests passed
1  = One or more critical tests failed
```

### Test Status Indicators

- ✅ **PASS**: Test passed all criteria
- ⚠️ **WARNING**: Test passed with minor issues
- ❌ **FAIL**: Test failed critical criteria
- ⏭️ **SKIPPED**: Test not executed (expected)

### Critical vs Non-Critical

**Critical Tests** (must pass):
- PRE-004: Repository integrity
- REV-001: Backup creation
- REV-002: Reversion execution
- POST-001: File structure verification
- POST-003: Broken links = 0
- POST-005: Hub violations = 0

**Non-Critical Tests** (warnings acceptable):
- PRE-003: Validation scripts baseline
- REG-001 through REG-005: Regression tests
- ROLL-001 through ROLL-003: Rollback tests

---

## Quick Verification Commands

### Check Test Completion

```bash
# Did tests run?
ls -l tests/reversion-test-report-*.md

# How many tests passed?
grep "PASS" tests/reversion-test-report-*.md | wc -l

# Any critical failures?
grep "FAIL (CRITICAL)" tests/reversion-test-report-*.md
```

### Check Gate Compliance

```bash
# After reversion (if executed)
python3 scripts/generate-audit-reports.py

# Check gates
grep "broken_links\|hub_violations\|orphans" reports/generated/structure-audit.json
```

### Verify Backup Created

```bash
# List backup branches
git branch | grep backup/pre-reversion
```

### Check File Structure

```bash
# These should NOT exist after reversion
test -d skills && echo "❌ skills/ still exists" || echo "✅ skills/ removed"
test -d archive && echo "❌ archive/ still exists" || echo "✅ archive/ removed"
test -d agents && echo "⚠️ agents/ exists" || echo "✅ agents/ removed"
```

---

## Manual Testing (Alternative to Automation)

If you prefer manual control, follow these steps:

### Step 1: Baseline Capture

```bash
# Save current state
git log --oneline -5 > /tmp/baseline-commits.txt
git status --porcelain > /tmp/baseline-status.txt
git diff --stat 68e0eb7 HEAD > /tmp/baseline-diff.txt

# Verify repo integrity
git fsck --full
```

### Step 2: Create Backup

```bash
# Create safety backup
BACKUP="backup/pre-reversion-$(date +%Y%m%d-%H%M%S)"
git branch "$BACKUP"
git branch | grep backup
```

### Step 3: Test Reversion (Dry Run)

```bash
# Test feasibility without committing
git revert --no-commit a4b1ed1 --dry-run

# Check for conflicts
# If output shows "CONFLICT", resolution required
```

### Step 4: Execute Reversion

```bash
# Only if dry-run succeeded
git revert --no-commit a4b1ed1

# Review staged changes
git status
git diff --cached --stat

# If good, commit
git commit -m "Revert \"major refactor to support skills.md\"

This reverts commit a4b1ed1.

Reason: [Your reason here]"
```

### Step 5: Validate Results

```bash
# Run audit
python3 scripts/ensure-hub-links.py || true
python3 scripts/generate-audit-reports.py

# Check gates
python3 -c "
import json
data = json.load(open('reports/generated/structure-audit.json'))
broken = data.get('broken_links', 999)
hubs = data.get('hub_violations', 999)
orphans = data.get('orphans', 999)
print(f'Broken: {broken}, Hubs: {hubs}, Orphans: {orphans}')
assert broken == 0, 'Broken links > 0'
assert hubs == 0, 'Hub violations > 0'
assert orphans <= 5, 'Orphans > 5'
print('✅ All gates passed')
"
```

### Step 6: Verify File Structure

```bash
# Compare with target
git diff 68e0eb7 HEAD --stat

# Check removed directories
for dir in skills archive agents; do
    if [ -d "$dir" ]; then
        echo "❌ $dir/ still exists"
    else
        echo "✅ $dir/ removed"
    fi
done
```

---

## Troubleshooting

### Test Script Won't Run

```bash
# Make executable
chmod +x scripts/run-reversion-tests.sh

# Check Python version
python3 --version  # Should be 3.11+

# Check dependencies
python3 -c "import yaml; print('YAML OK')"
```

### Tests Fail at PRE-004 (Repository Integrity)

```bash
# You have uncommitted changes
git status

# Solution: Commit or stash
git stash
# OR
git add . && git commit -m "Pre-reversion checkpoint"
```

### Conflicts During Reversion

```bash
# Check conflict files
git status | grep "both modified"

# View conflicts
git diff

# Manual resolution required
# Edit files, remove conflict markers
# Then stage and commit
git add <resolved-files>
git revert --continue
```

### Gates Fail After Reversion

```bash
# Re-run audit to refresh
python3 scripts/ensure-hub-links.py
python3 scripts/generate-audit-reports.py

# Check specific failures
cat reports/generated/structure-audit.md

# May need manual fixes
# See reversion-test-plan.md for remediation steps
```

---

## Rollback Procedures

### If Reversion Fails

```bash
# Option 1: Abort reversion
git revert --abort

# Option 2: Reset to backup
BACKUP=$(git branch | grep backup/pre-reversion | head -1 | xargs)
git reset --hard "$BACKUP"
```

### If Reversion Succeeds but Needs Undo

```bash
# Revert the revert (restore skills.md refactor)
git revert HEAD

# Or reset to backup
BACKUP=$(git branch | grep backup/pre-reversion | head -1 | xargs)
git reset --hard "$BACKUP"
```

---

## Success Criteria Checklist

Use this to quickly verify success:

```bash
# After running tests, verify:

# 1. Test report exists
ls -l tests/reversion-test-report-*.md

# 2. Overall result is PASS
grep "Overall Result.*PASS" tests/reversion-test-report-*.md

# 3. Zero critical failures
! grep "FAIL (CRITICAL)" tests/reversion-test-report-*.md

# 4. Backup exists
git branch | grep -q backup/pre-reversion

# 5. Gates pass (if reversion executed)
if [ "$EXECUTE_REVERSION" = "true" ]; then
    python3 -c "
    import json
    data = json.load(open('reports/generated/structure-audit.json'))
    assert data.get('broken_links', 1) == 0
    assert data.get('hub_violations', 1) == 0
    assert data.get('orphans', 999) <= 5
    " && echo "✅ All gates passed"
fi
```

---

## Next Steps After Testing

### If Tests Pass

1. Review test report: `cat tests/reversion-test-report-*.md`
2. Check recommendations section
3. If `EXECUTE_REVERSION` was false, run with `true` to actually revert
4. Verify changes with team before pushing
5. Push to remote: `git push origin master`

### If Tests Fail

1. Review failure details in test report
2. Check `TEST_ARTIFACTS` section for debug files
3. Examine `/tmp/reversion-tests-*/` for detailed output
4. Consult `tests/reversion-test-plan.md` for remediation
5. Fix issues and re-run tests
6. Consider consulting with team if critical failures persist

### If Warnings Present

1. Review warning details
2. Determine if warnings are acceptable (see expected-results-baseline.md)
3. Document warnings in test report
4. Proceed if warnings are expected, investigate if not

---

## Common Questions

**Q: Can I run tests multiple times?**
A: Yes, tests are idempotent in dry-run mode. Each run creates a new report.

**Q: Will tests modify my repository?**
A: Only if `EXECUTE_REVERSION=true` is set. Default is dry-run only.

**Q: How do I know if a test failure is critical?**
A: Check the test report. Critical failures are marked as "FAIL (CRITICAL)".

**Q: Can I skip certain test phases?**
A: Yes, but not recommended. Modify the script to comment out unwanted phases.

**Q: What if I accidentally run with EXECUTE_REVERSION=true?**
A: Use the backup branch to restore: `git reset --hard backup/pre-reversion-*`

**Q: How long should tests take?**
A: 2-5 minutes for dry-run, 3-7 minutes for actual reversion.

**Q: Where are test artifacts stored?**
A: `/tmp/reversion-tests-<PID>/` and `tests/reversion-test-report-*.md`

---

## Support

**Issues**: See `tests/reversion-test-plan.md` for detailed test documentation

**Baseline**: See `tests/expected-results-baseline.md` for expected states

**Template**: See `tests/reversion-test-report-template.md` for manual report creation

---

**Quick Reference Card**:
```
Test:     ./scripts/run-reversion-tests.sh
Report:   cat tests/reversion-test-report-*.md
Status:   echo $?
Gates:    grep "broken_links\|hub_violations\|orphans" reports/generated/structure-audit.json
Backup:   git branch | grep backup/pre-reversion
Rollback: git reset --hard $(git branch | grep backup/pre-reversion | head -1 | xargs)
```
