# Cleanup Scripts Usage Guide

**Version**: 1.0.0
**Last Updated**: 2025-10-25
**Purpose**: Safe, automated, and auditable cleanup operations

## Overview

Three complementary scripts for cleanup operations:

1. **cleanup-vestigial-artifacts.sh** - Delete files safely with backup
2. **fix-documentation-accuracy.py** - Fix exaggerations and unverified claims
3. **validate-cleanup.sh** - Comprehensive validation after cleanup

## Script 1: cleanup-vestigial-artifacts.sh

### Purpose

Safely delete vestigial files with:

- Automatic backup before deletion
- Reference scanning and warnings
- Comprehensive logging
- Post-deletion validation
- Rollback capability

### Usage

```bash
# Dry run to preview
./scripts/cleanup-vestigial-artifacts.sh --dry-run --input vestigial-files.txt

# Execute cleanup
./scripts/cleanup-vestigial-artifacts.sh --input vestigial-files.txt

# Custom backup location
./scripts/cleanup-vestigial-artifacts.sh --input vestigial-files.txt --backup-dir /tmp/cleanup-backup

# Skip validation (not recommended)
./scripts/cleanup-vestigial-artifacts.sh --input vestigial-files.txt --no-validate
```

### Input File Format

Create a text file listing files to delete (one per line, relative to repo root):

```text
# vestigial-files.txt
docs/old-guide.md
examples/deprecated-example.py
scripts/unused-script.sh
tools-config/legacy-config.yaml
```

Lines starting with `#` are treated as comments and ignored.

### Workflow

1. **Validation Phase**
   - Check files exist
   - Scan for references in markdown and config files
   - Report reference count

2. **Backup Phase**
   - Create timestamped backup directory
   - Copy all files preserving structure
   - Verify backup success

3. **Deletion Phase**
   - Delete each file
   - Log success/failure
   - Track failures

4. **Reference Check Phase**
   - Scan for remaining broken references
   - Report files needing manual updates

5. **Validation Phase** (if enabled)
   - Run audit reports
   - Run validation scripts
   - Verify no broken links

### Output

- **Backup**: `.cleanup-backups/YYYYMMDD_HHMMSS/`
- **Log**: `reports/generated/cleanup-YYYYMMDD_HHMMSS.log`
- **Console**: Color-coded progress and summary

### Rollback

To restore all deleted files:

```bash
cd .cleanup-backups/YYYYMMDD_HHMMSS
cp -r . /home/william/git/standards/
```

To restore specific file:

```bash
cp .cleanup-backups/YYYYMMDD_HHMMSS/path/to/file.md path/to/file.md
```

### Exit Codes

- `0` - Success
- `1` - Backup or deletion failures

## Script 2: fix-documentation-accuracy.py

### Purpose

Scan and fix documentation accuracy issues:

- Detect vague/exaggerated language
- Verify claims have evidence
- Replace with evidence-based statements
- Validate links after fixes

### Usage

```bash
# Dry run to preview issues
python3 scripts/fix-documentation-accuracy.py --dry-run

# Apply safe automated fixes
python3 scripts/fix-documentation-accuracy.py --fix

# Fix specific file
python3 scripts/fix-documentation-accuracy.py --fix --target CLAUDE.md

# Fix and validate links
python3 scripts/fix-documentation-accuracy.py --fix --check-links --verbose
```

### Detection Patterns

**Prohibited Language**:

- Vague quantifiers: "significantly", "dramatically", "vastly"
- Unverifiable claims: "best", "optimal", "perfect"
- Marketing hyperbole: "game-changer", "revolutionary"
- Absolute claims: "always works", "never fails"
- Temporal vagueness: "recently", "soon", "upcoming"

**Evidence Requirements**:

- Performance claims need: measurement method, test conditions, metrics
- Count claims need: verification command, file path, timestamp
- Feature claims need: implementation file, test coverage, docs
- Compliance claims need: validation script, audit report, timestamp

### Safe Automated Fixes

The script applies conservative replacements:

| Original | Replacement |
|----------|-------------|
| game-changer/revolutionary | innovative |
| cutting-edge | modern |
| seamlessly | integrated |
| effortlessly | streamlined |
| guaranteed | designed to |
| always works | typically works |

### Manual Review Required

For these patterns, the script flags but doesn't auto-fix:

- Performance metrics without evidence
- Count claims without verification
- Unqualified superlatives in critical sections

### Output

- **Report**: `reports/generated/accuracy-report-YYYYMMDD_HHMMSS.md`
- **Log**: `reports/generated/accuracy-fixes-YYYYMMDD_HHMMSS.log`
- **Console**: Summary with issue counts

### Example Report

```markdown
# Documentation Accuracy Report

Generated: 2025-10-25 14:30:00
Mode: FIX

## Summary

- Total issues found: 15
- Errors: 3
- Warnings: 12
- Fixes applied: 10

## Issues by File

### CLAUDE.md

- **Line 42**: Vague quantifier
  - Original: `significantly improved performance`
  - Suggestion: Use specific metrics

- **Line 156**: Performance claim without evidence
  - Original: `91-99.6% token reduction`
  - Evidence needed: measurement method, test conditions, actual metrics
```

### Exit Codes

- `0` - No errors (warnings OK)
- `1` - Errors found requiring manual fix

## Script 3: validate-cleanup.sh

### Purpose

Comprehensive post-cleanup validation:

- Run all existing validation scripts
- Check for broken references
- Verify file integrity
- Generate validation report

### Usage

```bash
# Full validation
./scripts/validate-cleanup.sh

# Quick validation (essential checks only)
./scripts/validate-cleanup.sh --quick

# Verbose output
./scripts/validate-cleanup.sh --verbose
```

### Validation Checks

**Check 1: Structure Audit**

- Broken links count (must be 0)
- Orphan count (must be ≤5)
- Hub violations (must be 0)

**Check 2: Claims Validation**

- Documentation accuracy
- Verified counts
- Evidence-based claims

**Check 3: Skills Validation**

- Skills structure
- Required fields present
- File organization

**Check 4: Anthropic Compliance** (full mode only)

- Token budgets
- Format compliance
- Frontmatter validation

**Check 5: Cross-References**

- Agent count matches actual files
- Skill count matches actual files
- Common reference patterns

**Check 6: File Integrity**

- Required files present
- No empty critical files
- Proper permissions

**Check 7: Git Status**

- Uncommitted changes check
- Untracked files check

### Output

- **Report**: `reports/generated/cleanup-validation-YYYYMMDD_HHMMSS.md`
- **Log**: `reports/generated/cleanup-validation-YYYYMMDD_HHMMSS.log`
- **Console**: Color-coded check results

### Example Output

```
=========================================
Check 1: Structure Audit
=========================================
  Broken links: 0
  Orphans: 3
  Hub violations: 0
✓ No broken links
✓ No hub violations
✓ Orphan count acceptable

=========================================
Validation Summary
=========================================
Total Checks: 15
Passed: 14 (93%)
Failed: 0
Warnings: 1

✅ All validation checks passed!
```

### Exit Codes

- `0` - All checks passed
- `1` - Critical errors found
- `2` - Warnings only

## Complete Cleanup Workflow

### Step 1: Identify Vestigial Files

Create list of files to delete:

```bash
# Review and create file list
cat > vestigial-files.txt <<EOF
# Documentation duplicates
docs/old-version/
examples/deprecated/

# Unused scripts
scripts/legacy-migrate.py

# Outdated configs
config/old-matrix.yaml
EOF
```

### Step 2: Preview Cleanup

```bash
# Dry run to preview
./scripts/cleanup-vestigial-artifacts.sh --dry-run --input vestigial-files.txt

# Review output
# Check for references
# Confirm file list is correct
```

### Step 3: Fix Documentation Accuracy

```bash
# Scan for accuracy issues
python3 scripts/fix-documentation-accuracy.py --dry-run --verbose

# Review issues
less reports/generated/accuracy-report-*.md

# Apply fixes
python3 scripts/fix-documentation-accuracy.py --fix --check-links
```

### Step 4: Execute Cleanup

```bash
# Run cleanup (creates backup)
./scripts/cleanup-vestigial-artifacts.sh --input vestigial-files.txt

# Review log
less reports/generated/cleanup-*.log

# Check backup
ls -la .cleanup-backups/
```

### Step 5: Validate Results

```bash
# Run full validation
./scripts/validate-cleanup.sh --verbose

# Review validation report
cat reports/generated/cleanup-validation-*.md

# If issues found, review and fix
python3 scripts/auto-fix-links.py  # Fix any broken links
```

### Step 6: Manual Review

Check files that had references:

```bash
# Review log for reference warnings
grep "reference" reports/generated/cleanup-*.log

# Manually update files as needed
```

### Step 7: Final Validation

```bash
# Run validation again
./scripts/validate-cleanup.sh

# Should show all passed
# ✅ All validation checks passed!
```

### Step 8: Commit

```bash
# Check git status
git status

# Review changes
git diff

# Stage and commit
git add .
git commit -m "cleanup: remove vestigial artifacts

- Deleted X outdated files
- Fixed documentation accuracy (Y issues)
- Validation: 0 broken links, Z orphans
- Backup: .cleanup-backups/YYYYMMDD_HHMMSS

Evidence:
- Cleanup log: reports/generated/cleanup-YYYYMMDD_HHMMSS.log
- Validation report: reports/generated/cleanup-validation-YYYYMMDD_HHMMSS.md
"
```

## Best Practices

### Before Cleanup

1. **Backup**: Ensure git is clean and up-to-date
2. **Branch**: Work in a feature branch
3. **Review**: Manually review file list
4. **Dry Run**: Always run with `--dry-run` first

### During Cleanup

1. **Read Output**: Review all warnings and errors
2. **Check References**: Note files with references for manual review
3. **Verify Backup**: Confirm backup created successfully
4. **Monitor Progress**: Watch for failures

### After Cleanup

1. **Validate**: Run `validate-cleanup.sh`
2. **Review**: Check validation report
3. **Fix Issues**: Address any broken references
4. **Test**: Manually verify critical functionality
5. **Document**: Update CHANGELOG or commit message

## Troubleshooting

### Issue: Backup Failed

**Symptom**: "Failed to backup: file.md"

**Solution**:

```bash
# Check disk space
df -h

# Check permissions
ls -la path/to/file.md

# Manually backup
mkdir -p manual-backup
cp -r files-to-delete/ manual-backup/
```

### Issue: Validation Failures After Cleanup

**Symptom**: "Broken links: 5"

**Solution**:

```bash
# Run link fixer
python3 scripts/auto-fix-links.py

# Or manually review
cat reports/generated/linkcheck.txt

# Restore if needed
cp .cleanup-backups/YYYYMMDD_HHMMSS/file.md file.md
```

### Issue: Too Many References

**Symptom**: "Found 20 references to file.md"

**Solution**:

```bash
# Don't delete yet - file is still needed
# Remove from vestigial-files.txt

# Or update references first
grep -r "filename" docs/ --files-with-matches
# Manually update each file
```

### Issue: Rollback Needed

**Symptom**: Accidentally deleted important files

**Solution**:

```bash
# Full rollback
cd .cleanup-backups/YYYYMMDD_HHMMSS
cp -r . /home/william/git/standards/

# Verify restoration
./scripts/validate-cleanup.sh

# Commit restoration
git add .
git commit -m "restore: rollback cleanup operation"
```

## Safety Features

All scripts include:

- ✅ Dry-run mode
- ✅ Automatic backups
- ✅ Comprehensive logging
- ✅ Error handling
- ✅ Rollback instructions
- ✅ Validation gates
- ✅ Exit codes for CI/CD

## Integration with CI/CD

Add to `.github/workflows/cleanup-validation.yml`:

```yaml
name: Cleanup Validation

on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Cleanup Validation
        run: ./scripts/validate-cleanup.sh

      - name: Upload Reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: validation-reports
          path: reports/generated/cleanup-validation-*.md
```

## Support

**Documentation Issues**: File issue with `documentation` label
**Script Bugs**: File issue with `scripts` label
**Feature Requests**: File issue with `enhancement` label

---

*Last Updated: 2025-10-25*
*Maintained by: Standards Repository Team*
