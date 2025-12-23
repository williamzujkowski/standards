# Skills.md Reversion Scripts - Complete Guide

**Created**: 2025-10-25
**Purpose**: Automated, safe reversion of the skills.md refactor (commit a4b1ed1)

## Overview

This suite provides four automated scripts for safely reverting the skills.md refactor:

1. **backup-current-state.sh** - Create comprehensive backups before reversion
2. **revert-to-pre-skills.sh** - Perform the actual reversion
3. **validate-reversion.sh** - Validate the reversion was successful
4. **rollback-reversion.sh** - Emergency recovery if reversion fails

## Quick Start

```bash
# 1. Create backup (ALWAYS run this first!)
./scripts/backup-current-state.sh

# 2. Perform reversion
./scripts/revert-to-pre-skills.sh --method revert

# 3. Validate reversion
./scripts/validate-reversion.sh

# 4. If validation passes, merge and push
git checkout main
git merge reversion/skills-md-<timestamp>
git push

# 5. If something went wrong, rollback
./scripts/rollback-reversion.sh
```

## Script Details

### 1. backup-current-state.sh

**Purpose**: Create timestamped backups before any reversion attempts.

**What it does**:

- Creates backup branch: `backup/pre-reversion-<timestamp>`
- Creates backup tag: `backup-<timestamp>`
- Exports state metadata to JSON
- Exports diff with pre-skills state
- Generates comprehensive backup summary

**Usage**:

```bash
# Standard backup
./scripts/backup-current-state.sh

# Dry-run to see what would happen
./scripts/backup-current-state.sh --dry-run

# Verbose output with custom backup directory
./scripts/backup-current-state.sh --verbose --backup-dir /tmp/backups
```

**Options**:

- `--dry-run` - Show what would be done without doing it
- `--backup-dir DIR` - Custom backup directory (default: backups/)
- `--verbose` - Show detailed progress
- `--help` - Show help message

**Output**:

- Backup branch and tag
- `backups/state_<timestamp>.json` - Full state metadata
- `backups/skills_refactor_diff_<timestamp>.patch` - Diff with pre-skills state
- `backups/backup_summary_<timestamp>.txt` - Human-readable summary
- `backups/backup_<timestamp>.log` - Operation log

**Safety**:

- ✅ Idempotent - Can run multiple times safely
- ✅ Non-destructive - Only creates new branches/tags
- ✅ Fully logged - All operations recorded

---

### 2. revert-to-pre-skills.sh

**Purpose**: Revert the skills.md refactor using git revert or reset.

**What it does**:

- Verifies backup exists (fails without backup)
- Validates repository state
- Creates reversion branch: `reversion/skills-md-<timestamp>`
- Performs reversion using chosen method
- Validates reversion succeeded
- Runs existing validation scripts
- Generates reversion report

**Usage**:

```bash
# Safe method (recommended): Creates new commit undoing changes
./scripts/revert-to-pre-skills.sh --method revert

# Destructive method: Resets to pre-skills commit (requires force push)
./scripts/revert-to-pre-skills.sh --method reset

# Dry-run to preview
./scripts/revert-to-pre-skills.sh --dry-run --method revert

# Skip confirmations (dangerous!)
./scripts/revert-to-pre-skills.sh --method revert --no-confirm
```

**Reversion Methods**:

| Method | Description | Pros | Cons |
|--------|-------------|------|------|
| `revert` | Creates new commit undoing changes | Preserves history, safer, no force push needed | Adds commit to history |
| `reset` | Moves HEAD to pre-skills commit | Clean history | Destructive, requires force push, rewrites history |

**Options**:

- `--method METHOD` - Reversion method: `revert` or `reset` (default: revert)
- `--dry-run` - Show what would be done without doing it
- `--no-confirm` - Skip confirmation prompts (dangerous!)
- `--verbose` - Show detailed progress
- `--help` - Show help message

**Output**:

- Reversion branch: `reversion/skills-md-<timestamp>`
- `backups/reversion_<timestamp>.log` - Operation log
- `backups/reversion_report_<timestamp>.txt` - Reversion report

**Safety**:

- ✅ Requires backup to exist (created by backup-current-state.sh)
- ✅ Validates repository state before proceeding
- ✅ Requires confirmation for destructive operations
- ✅ Validates state at each step
- ✅ Fully logged

**Target Commits**:

- Skills commit: `a4b1ed1` (major refactor to support skills.md)
- Pre-skills commit: `68e0eb7` (fix: apply pre-commit auto-formatting)

---

### 3. validate-reversion.sh

**Purpose**: Comprehensive validation that reversion was successful.

**What it does**:

- Checks git repository integrity
- Verifies not on skills commit
- Compares with pre-skills state
- Runs existing validation scripts
- Validates directory structure
- Checks critical files exist
- Verifies git history integrity
- Validates Python scripts syntax
- Generates comprehensive validation report

**Usage**:

```bash
# Standard validation
./scripts/validate-reversion.sh

# Verbose output
./scripts/validate-reversion.sh --verbose

# Stop on first failure
./scripts/validate-reversion.sh --fail-fast

# Custom report directory
./scripts/validate-reversion.sh --report-dir /tmp/validation
```

**Options**:

- `--verbose` - Show detailed validation progress
- `--report-dir DIR` - Custom report directory (default: backups/)
- `--fail-fast` - Stop on first validation failure
- `--help` - Show help message

**Validation Checks**:

1. ✅ Git repository integrity
2. ✅ Not on skills commit (a4b1ed1)
3. ✅ Diff with pre-skills state (68e0eb7)
4. ✅ Existing validation scripts pass
5. ✅ Directory structure correct
6. ✅ Critical files exist
7. ✅ Git history integrity
8. ✅ Python scripts syntax valid

**Output**:

- `backups/validation_<timestamp>.txt` - Detailed validation report
- `backups/validation_<timestamp>.json` - Machine-readable results
- Console output with colored status indicators

**Exit Codes**:

- `0` - All validations passed ✅
- `1` - One or more validations failed ❌
- `2` - Prerequisites not met ⚠️

---

### 4. rollback-reversion.sh

**Purpose**: Emergency recovery to undo a failed reversion.

**What it does**:

- Finds latest backup tag (or uses specified tag)
- Verifies backup exists and is valid
- Saves current state in reference branch
- Resets to backup state
- Validates rollback succeeded
- Optionally cleans up reversion artifacts
- Generates rollback report

**Usage**:

```bash
# Rollback to latest backup
./scripts/rollback-reversion.sh

# Rollback to specific backup tag
./scripts/rollback-reversion.sh --backup-tag backup-20251025_143022

# Dry-run to preview
./scripts/rollback-reversion.sh --dry-run

# Skip confirmations (dangerous!)
./scripts/rollback-reversion.sh --no-confirm
```

**Options**:

- `--dry-run` - Show what would be done without doing it
- `--backup-tag TAG` - Specific backup tag to restore (default: latest)
- `--no-confirm` - Skip confirmation prompts (dangerous!)
- `--verbose` - Show detailed progress
- `--help` - Show help message

**Output**:

- Rollback reference branch: `rollback/from-reversion-<timestamp>`
- `backups/rollback_<timestamp>.log` - Operation log
- `backups/rollback_report_<timestamp>.txt` - Rollback report

**Safety**:

- ✅ Requires backup tag to exist
- ✅ Creates rollback branch before restoration
- ✅ Requires confirmation before destructive operations
- ✅ Validates state after rollback
- ✅ Fully logged

---

## Complete Workflow

### Scenario 1: Successful Reversion

```bash
# Step 1: Backup current state
./scripts/backup-current-state.sh

# Review backup summary
cat backups/backup_summary_*.txt

# Step 2: Perform reversion (using safer revert method)
./scripts/revert-to-pre-skills.sh --method revert

# Step 3: Validate reversion
./scripts/validate-reversion.sh

# If all checks pass:
# Step 4: Merge to main and push
git checkout main
git merge reversion/skills-md-<timestamp>
git push origin main

# Step 5: Clean up (optional)
git branch -d reversion/skills-md-<timestamp>
git branch -d backup/pre-reversion-<timestamp>
```

### Scenario 2: Failed Reversion (Need Rollback)

```bash
# Step 1: Backup current state
./scripts/backup-current-state.sh

# Step 2: Attempt reversion
./scripts/revert-to-pre-skills.sh --method revert

# Step 3: Validation fails!
./scripts/validate-reversion.sh
# Exit code 1 - validation failed

# Step 4: Emergency rollback
./scripts/rollback-reversion.sh

# Review rollback report
cat backups/rollback_report_*.txt

# Step 5: Investigate issues and try again
# - Review what went wrong
# - Fix any issues
# - Create new backup
# - Retry reversion
```

### Scenario 3: Testing with Dry-Run

```bash
# Preview all operations without making changes
./scripts/backup-current-state.sh --dry-run
./scripts/revert-to-pre-skills.sh --dry-run --method revert
./scripts/rollback-reversion.sh --dry-run

# Review what would happen, then run for real
./scripts/backup-current-state.sh
./scripts/revert-to-pre-skills.sh --method revert
./scripts/validate-reversion.sh
```

---

## Safety Features

All scripts include multiple safety layers:

### 1. Backup Requirements

- Reversion script requires backup to exist
- Rollback script requires backup tag
- Multiple backup artifacts created (branch, tag, metadata)

### 2. Validation at Each Step

- Repository state validated before operations
- Operations validated after completion
- Comprehensive validation script for final check

### 3. Confirmation Prompts

- Major operations require user confirmation
- Destructive operations require double confirmation
- Can be bypassed with `--no-confirm` for automation

### 4. Comprehensive Logging

- All operations logged to timestamped files
- Logs include timestamps, operation details, results
- Logs preserved for troubleshooting

### 5. Dry-Run Mode

- Preview operations without executing
- Test workflow before committing
- Verify safety before production run

### 6. Idempotency

- Scripts can be run multiple times safely
- Graceful handling of existing branches/tags
- No duplicate operations

---

## Troubleshooting

### Backup Script Issues

**Problem**: "Not a git repository"

```bash
# Solution: Ensure you're in repository root
cd /home/william/git/standards
./scripts/backup-current-state.sh
```

**Problem**: Permission denied

```bash
# Solution: Make scripts executable
chmod +x scripts/*.sh
```

### Reversion Script Issues

**Problem**: "No backup found"

```bash
# Solution: Run backup script first
./scripts/backup-current-state.sh
```

**Problem**: "Working directory has uncommitted changes"

```bash
# Solution: Commit or stash changes
git status
git add -A && git commit -m "WIP: Save before reversion"
# OR
git stash
```

**Problem**: Git revert conflicts

```bash
# Solution: Manually resolve conflicts
git status  # See conflicted files
# Edit files to resolve conflicts
git add <resolved-files>
git revert --continue
```

### Validation Script Issues

**Problem**: Validation fails after reversion

```bash
# Solution: Review validation report
cat backups/validation_*.txt

# If issues are minor, may be acceptable
# If issues are critical, rollback:
./scripts/rollback-reversion.sh
```

**Problem**: Python syntax errors detected

```bash
# Solution: Check specific files with errors
python3 -m py_compile scripts/problematic_file.py

# May indicate reversion corruption - consider rollback
```

### Rollback Script Issues

**Problem**: "No backup tags found"

```bash
# Solution: List available backups
git tag -l "backup-*"
git branch -a | grep backup

# If truly no backups exist, manual recovery needed
```

**Problem**: Uncommitted changes warning

```bash
# Solution: Either commit them or accept they'll be lost
git status
# If important, commit first:
git add -A && git commit -m "Save before rollback"
# Then run rollback
```

---

## File Locations

All scripts and artifacts are organized as follows:

```
standards/
├── scripts/
│   ├── backup-current-state.sh      # Script 1: Backup
│   ├── revert-to-pre-skills.sh      # Script 2: Reversion
│   ├── validate-reversion.sh        # Script 3: Validation
│   ├── rollback-reversion.sh        # Script 4: Rollback
│   └── REVERSION_SCRIPTS_GUIDE.md   # This guide
│
└── backups/                          # All outputs go here
    ├── backup_<timestamp>.log
    ├── backup_summary_<timestamp>.txt
    ├── state_<timestamp>.json
    ├── skills_refactor_diff_<timestamp>.patch
    ├── reversion_<timestamp>.log
    ├── reversion_report_<timestamp>.txt
    ├── validation_<timestamp>.txt
    ├── validation_<timestamp>.json
    ├── rollback_<timestamp>.log
    └── rollback_report_<timestamp>.txt
```

---

## Technical Details

### Key Commits

- **Skills Refactor**: `a4b1ed1` (major refactor to support skills.md)
- **Pre-Skills State**: `68e0eb7` (fix: apply pre-commit auto-formatting)

### Git Operations Used

- `git checkout -b <branch>` - Create branches
- `git tag -a <tag>` - Create annotated tags
- `git revert <commit>` - Undo changes with new commit
- `git reset --hard <commit>` - Destructive reset
- `git diff --stat` - Compare states
- `git merge-base` - Find common ancestors

### Dependencies

- **bash** >= 4.0
- **git** >= 2.0
- **python3** >= 3.6 (for validation scripts)
- **jq** (for JSON processing, optional)

### Script Architecture

Each script follows the same pattern:

1. **Argument Parsing** - Handle CLI options
2. **Logging Setup** - Initialize timestamped logs
3. **Validation** - Check prerequisites
4. **Execution** - Perform operations
5. **Validation** - Verify results
6. **Reporting** - Generate comprehensive reports

---

## Best Practices

1. **Always backup first** - Never run reversion without backup
2. **Use dry-run** - Preview operations before executing
3. **Read reports** - Review generated reports after each step
4. **Validate thoroughly** - Run validation script after reversion
5. **Keep logs** - Don't delete backup artifacts until verified
6. **Test in branch** - Never run directly on main/master
7. **Communicate** - Inform team before major reversions
8. **Document** - Add notes about why reversion was needed

---

## FAQ

**Q: Which reversion method should I use?**
A: Use `--method revert` (default) unless you need clean history and are comfortable with force pushing.

**Q: Can I run these scripts multiple times?**
A: Yes, all scripts are idempotent. Backup creates new timestamped artifacts each time.

**Q: What if I need to revert a reversion?**
A: Use the rollback script to restore to backup state. The backup includes the pre-reversion state.

**Q: Are these scripts safe for production?**
A: Yes, with proper testing. Always use dry-run first and validate thoroughly.

**Q: What happens to remote branches?**
A: Scripts only affect local repository. You control when to push changes.

**Q: Can I customize the scripts?**
A: Yes, scripts are well-commented and modular. Fork and modify as needed.

**Q: How do I clean up old backups?**
A: Manually delete old backup branches/tags after verifying reversion:

```bash
git branch -d backup/pre-reversion-<old-timestamp>
git tag -d backup-<old-timestamp>
```

---

## Support & Contribution

**Issues**: If you encounter problems:

1. Check logs in `backups/` directory
2. Run validation with `--verbose` flag
3. Review this guide's troubleshooting section
4. Check git status and recent commits

**Improvements**: To enhance these scripts:

1. Test changes in dry-run mode first
2. Maintain idempotency and safety features
3. Update this guide with new options
4. Add comprehensive comments in scripts

---

## License

These scripts are part of the Standards Repository and follow the same license.

---

**Last Updated**: 2025-10-25
**Version**: 1.0.0
**Author**: Hive Mind Collective (Coder Agent)
