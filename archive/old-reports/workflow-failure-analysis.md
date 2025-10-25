# Comprehensive Workflow Failure Analysis

**Report Date:** 2025-10-17
**Branch:** audit-gates-final/20251017
**Workflow Run:** https://github.com/williamzujkowski/standards/actions/runs/18599316877
**Status:** FAILED ❌

## Executive Summary

The "Lint and Validate" workflow is **failing** due to two primary issues in the pre-commit checks:

1. **JSON Formatting Hook** - Modifying files (auto-fixing format issues)
2. **Markdown Linting Hook** - Multiple markdown style violations

Both failures are **NON-CRITICAL** and represent automatic formatting corrections that need to be committed.

---

## 1. Current Workflow Status

### All Workflows Overview

| Workflow | Status | URL |
|----------|--------|-----|
| Deploy MkDocs to GitHub Pages | ✅ SUCCESS | Run 18599316883 |
| **Lint and Validate** | ❌ **FAILURE** | Run 18599316877 |
| Redundancy Check | ✅ SUCCESS | Run 18599316856 |
| NIST 800-53r5 Continuous Compliance | ✅ SUCCESS | Run 18599316851 |
| Repository Health Check | ✅ SUCCESS | Run 18599316850 |

**Critical Finding:** Only 1 out of 5 workflows is failing, and it's a formatting/style issue, not a functional problem.

---

## 2. Detailed Failure Analysis

### 2.1 JSON Formatting Hook Failure

**Hook ID:** `pretty-format-json`
**Status:** Failed (files were modified)
**Exit Code:** 1

#### Root Cause

The pre-commit hook automatically reformatted **16 JSON files** to ensure consistent 2-space indentation. This is **NOT an error** - it's the hook doing its job. However, the CI fails because files were modified during the check.

#### Affected Files (All Auto-Fixed)

```
reports/generated/standards-inventory.json
skills/cloud-native/aws-advanced/templates/lambda-layer-structure/nodejs/package.json
skills/cloud-native/aws-advanced/templates/step-functions-state-machine.json
skills/coding-standards/javascript/resources/configs/jest.config.json
skills/cloud-native/aws-advanced/templates/eventbridge-patterns.json
skills/compliance/healthtech/templates/fhir-resources.json
skills/security/authorization/templates/abac-policy.json
skills/devops/monitoring-observability/templates/grafana-dashboard.json
skills/database/advanced-optimization/templates/monitoring-dashboard.json
skills/testing/performance-testing/templates/grafana-dashboard.json
examples/nist-templates/quickstart/structure-audit.json
skills/security/security-operations/templates/security-metrics-dashboard.json
reports/generated/structure-audit.json
skills/compliance/fintech/templates/compliance-dashboard.json
skills/coding-standards/javascript/resources/configs/package.json
reports/generated/script-coverage.json
```

#### Pre-Commit Configuration

File: `.pre-commit-config.yaml` (Lines 90-101)

```yaml
- id: pretty-format-json
  name: Format JSON files
  args: [--autofix, --indent=2]
  exclude: |
    (?x)^(
        .*\.vscode/.*\.json$|
        package-lock\.json$|
        .*node_modules/.*\.json$|
        .*\.min\.json$|
        .*tsconfig.*\.json$|
        .*\.eslintrc.*\.json$
    )$
```

#### Issue Analysis

**The Problem:** In CI/CD, when pre-commit modifies files, the workflow fails because:

1. CI checks out code in a clean state
2. Pre-commit modifies files during checks
3. Modified files indicate "changes were needed" → failure

**Why It's Failing Now:** The 16 JSON files listed above have inconsistent indentation that differs from the enforced 2-space standard.

---

### 2.2 Markdown Linting Hook Failure

**Hook ID:** `markdownlint`
**Status:** Failed (files were modified)
**Exit Code:** 1

#### Root Cause

Multiple markdown files contain style violations that the linter automatically fixed:

1. **MD050 (Strong Style)** - Using `__text__` instead of `**text**`
2. **MD035 (HR Style)** - Using `_______________` instead of `---`
3. **MD041 (First Line Heading)** - File doesn't start with H1
4. **MD003 (Heading Style)** - Using setext `===` instead of ATX `#`
5. **MD024 (Duplicate Heading)** - Multiple headings with same content

#### Detailed Violations

##### A. Strong Style Violations (MD050)

**File:** `docs/migration/phase1-progress-tracker.md`

```markdown
# Current (Wrong - Uses underscores)
**Day 1 Overall**: _**/9 tasks |**_% complete

# Should Be (Uses asterisks)
**Day 1 Overall**: **X/9 tasks |Y**% complete
```

**Lines Affected:** 61, 90, 128, 176, 223, 366

**Issue:** Mixing `__bold__` with `**bold**` syntax. Markdownlint enforces `**asterisk**` style.

##### B. Horizontal Rule Violations (MD035)

**Files:**

- `docs/migration/phase1-progress-tracker.md`
- `docs/migration/phase1-gate-checklist.md`
- `docs/migration/phase2-gate-checklist.md`
- `docs/migration/phase2-progress-tracker.md`
- `skills/security/zero-trust/resources/nist-800-207-checklist.md`

```markdown
# Current (Wrong)
_______________

# Should Be
---
```

**Total Violations:** 100+ lines across 5 files

**Issue:** Using underscores for horizontal rules instead of hyphens.

##### C. First Line Heading Violation (MD041)

**File:** `skills_alignment.md`

```markdown
# Current (Wrong - Starts with text)
I'll help you create a comprehensive prompt...

# Should Be (Starts with H1)
# Skills Alignment

I'll help you create a comprehensive prompt...
```

**Issue:** Markdown files should start with a top-level heading (`#`).

##### D. Heading Style Violation (MD003)

**File:** `skills/frontend/react/SKILL.md`

```markdown
# Current (Wrong - Setext style on line 5)
name: react-frontend
===

# Should Be (ATX style)
# name: react-frontend
```

**Issue:** Using setext underline style instead of ATX (`#`) style.

##### E. Duplicate Heading Violation (MD024)

**File:** `docs/guides/SKILL_AUTHORING_GUIDE.md` (Line 561)

**Issue:** Multiple `## Bundled Resources` headings exist in the document.

#### Markdownlint Configuration

File: `.markdownlint.yaml`

```yaml
# MD050 is enabled (should enforce asterisk style for bold)
default: true

MD003:
  style: atx  # Enforce ATX-style headings

MD041: true  # First line must be top-level heading

MD024:
  siblings_only: true  # Allow duplicates at different levels

MD035: false  # NOT DISABLED - Should enforce --- style
```

**Configuration Issue:** MD035 is not explicitly configured, defaulting to enforcing `---` style for horizontal rules.

---

## 3. Why These Failures Occurred

### Timeline Analysis

Recent commits show attempts to fix formatting:

```
5577cda fix: broaden yamllint ignore and fix comment spacing
2e30e42 fix: correct gitleaks and yamllint configurations
d10e8f6 fix: resolve all workflow failures identified by swarm investigation
34910a8 fix: exclude test files from ESLint
ee34174 fix: update pre-commit config and auto-fix formatting
```

**Root Cause:** The files in question weren't properly formatted when committed, and now pre-commit is catching them on CI.

---

## 4. Impact Assessment

### Severity: **LOW** ⚠️

| Aspect | Impact |
|--------|--------|
| **Functionality** | None - All code works correctly |
| **Security** | None - No security implications |
| **Data Integrity** | None - Just formatting |
| **User Experience** | None - Documentation is readable |
| **CI/CD Pipeline** | Blocking - Prevents merges |

### Affected Systems

- ✅ Code execution: **NOT AFFECTED**
- ✅ Documentation content: **NOT AFFECTED**
- ✅ Security scans: **PASSING**
- ✅ Link validation: **PASSING** (informational)
- ✅ Structure audit: **PASSING**
- ❌ Pre-commit checks: **FAILING** (formatting only)

---

## 5. Fix Recommendations

### 5.1 Immediate Fix (Recommended)

**Action:** Commit the auto-fixed files

```bash
# Let pre-commit fix all files locally
pre-commit run --all-files

# Commit the changes
git add -A
git commit -m "fix: apply pre-commit auto-formatting to JSON and Markdown files

- Auto-format 16 JSON files with 2-space indentation
- Fix markdown strong style (__ -> **)
- Fix markdown HR style (_____ -> ---)
- Fix first-line heading violations
- Fix heading style violations

Files modified by pre-commit hooks (automated fixes):
- JSON: 16 files (proper indentation)
- Markdown: 6 files (style compliance)

refs: Run 18599316877"

# Push changes
git push
```

**Expected Outcome:** Next CI run will pass all pre-commit checks.

**Time Required:** 2 minutes

---

### 5.2 Prevent Future Occurrences

#### Option A: Install Pre-Commit Git Hook Locally (Best Practice)

```bash
# Install pre-commit hooks to run automatically before commits
pre-commit install

# Test it works
git commit -m "test" --allow-empty
```

**Benefit:** Catches formatting issues before pushing to remote.

#### Option B: Add Pre-Commit to CI Earlier

Update `.github/workflows/lint-and-validate.yml`:

```yaml
# Add this step BEFORE "Run pre-commit"
- name: Allow pre-commit to modify files
  run: |
    pre-commit run --all-files || true

    # Check if files were modified
    if ! git diff --quiet; then
      echo "⚠️ Files were auto-formatted by pre-commit"
      echo "::warning::The following files need formatting:"
      git diff --name-only
      echo ""
      echo "::error::Run 'pre-commit run --all-files' locally and commit changes"
      exit 1
    fi
```

**Benefit:** Provides clearer error messages about what needs fixing.

#### Option C: Disable Auto-Fix in CI (Not Recommended)

Modify `.pre-commit-config.yaml` to remove `--fix` and `--autofix` flags for CI runs only. This would make the checks informational rather than fixing.

**Downside:** Files remain improperly formatted until manually fixed.

---

## 6. Specific File Fixes

### 6.1 JSON Files - No Manual Changes Needed

**All 16 JSON files** will be automatically reformatted by pre-commit to use consistent 2-space indentation. No manual editing required.

### 6.2 Markdown Files - Manual Fixes Required

#### Fix 1: `skills_alignment.md`

**Current:**

```markdown
I'll help you create a comprehensive prompt to align your standards repo with Anthropic's new agent skills format. Let me first examine both the Anthropic documentation and your current standards repository to understand the alignment needed.Based on my analysis of your standards repository and Anthropic's new Agent Skills format, I'll create a comprehensive prompt for Claude Flow to help you modernize your standards repo. Your repository already has excellent content that aligns well with the Skills philosophy - it just needs restructuring to follow the new format.

## **Claude Flow Prompt for Standards-to-Skills Migration**
```

**Fix:**

```markdown
# Skills Alignment

I'll help you create a comprehensive prompt to align your standards repo with Anthropic's new agent skills format...

## Claude Flow Prompt for Standards-to-Skills Migration
```

#### Fix 2: `skills/frontend/react/SKILL.md`

**Current (Line 5):**

```markdown
name: react-frontend
===
description: React frontend standards...
```

**Fix:**

```markdown
# name: react-frontend

description: React frontend standards...
```

**OR** (Better - Use YAML front matter):

```markdown
---
name: react-frontend
description: React frontend standards...
---

# React Frontend Development Standards
```

#### Fix 3: Phase Progress Tracker Files

For all files in `docs/migration/phase*-progress-tracker.md` and `docs/migration/phase*-gate-checklist.md`:

**Find and Replace:**

```bash
# Fix horizontal rules
find docs/migration -name "*.md" -type f -exec sed -i 's/^_______________$/---/g' {} \;

# Fix strong style (this is trickier - pre-commit will handle it)
# Just run pre-commit and let it auto-fix
```

#### Fix 4: `docs/guides/SKILL_AUTHORING_GUIDE.md`

**Issue:** Duplicate `## Bundled Resources` headings (line 561)

**Fix:** Change one heading to be more specific:

```markdown
# From
## Bundled Resources

# To
## Additional Bundled Resources
```

---

## 7. Validation Commands

After applying fixes, verify with these commands:

```bash
# 1. Check JSON formatting
pre-commit run pretty-format-json --all-files

# 2. Check Markdown linting
pre-commit run markdownlint --all-files

# 3. Run full pre-commit suite
pre-commit run --all-files

# 4. Check git status
git status

# 5. Verify no uncommitted changes remain
git diff --name-only

# 6. Run audit gates locally
python3 scripts/ensure-hub-links.py
python3 scripts/generate-audit-reports.py

# 7. Check structure audit results
cat reports/generated/structure-audit.json | jq '.broken_links, .hub_violations, .orphans'

# 8. Run unit tests
pytest -q scripts/tests/test_hub_enforcement.py
```

**Expected Output:**

```
✅ All checks passed
✅ No files modified
✅ Broken links: 0
✅ Hub violations: 0
✅ Orphans: ≤5
```

---

## 8. Root Cause Summary

### Why This Happened

1. **JSON Files:** Historical commits included JSON with inconsistent indentation (mix of 2, 4, and compact formatting)
2. **Markdown Files:** Migration phase tracking documents used non-standard markdown syntax for visual effect (underscores for lines, mixed bold styles)
3. **Pre-Commit Evolution:** The `.pre-commit-config.yaml` was recently updated with stricter formatting rules
4. **No Local Pre-Commit Hook:** Contributors weren't running pre-commit locally before pushing

### Contributing Factors

- Template/scaffolding files created manually without pre-commit checks
- Phase tracking documents created for visual appeal rather than markdown compliance
- Skills alignment document generated by AI and not validated before commit
- React SKILL.md used non-standard YAML front matter format

---

## 9. Configuration Analysis

### Pre-Commit Configuration Correctness

**File:** `.pre-commit-config.yaml`

✅ **Correctly Configured:**

- Gitleaks (secret detection)
- Large file checks
- YAML linting with proper exclusions
- Python formatting (Black, isort, ruff)
- Shell script checking
- Gitignore compliance

⚠️ **Issues Found:**

1. **Deprecated Stage Names (Lines 327, 320)**

```yaml
# Warning from workflow:
# [WARNING] hook id `final-security-check` uses deprecated stage names (commit)
# [WARNING] top-level `default_stages` uses deprecated stage names (commit, push)
```

**Fix:**

```yaml
# From:
default_stages: [commit, push]

# To:
default_stages: [pre-commit, pre-push]

# And update final-security-check:
stages: [pre-commit]
```

2. **JSON Hook Could Be More Lenient**

The `pretty-format-json` hook excludes many files but misses some template directories:

```yaml
# Current exclusion:
exclude: |
  (?x)^(
      .*\.vscode/.*\.json$|
      package-lock\.json$|
      .*node_modules/.*\.json$|
      .*\.min\.json$|
      .*tsconfig.*\.json$|
      .*\.eslintrc.*\.json$
  )$

# Suggested addition:
exclude: |
  (?x)^(
      .*\.vscode/.*\.json$|
      package-lock\.json$|
      .*node_modules/.*\.json$|
      .*\.min\.json$|
      .*tsconfig.*\.json$|
      .*\.eslintrc.*\.json$|
      reports/generated/.*\.json$  # ← ADD THIS (generated files)
  )$
```

**Reasoning:** Generated files like `reports/generated/structure-audit.json` are rebuilt by scripts and don't need manual formatting.

### Markdownlint Configuration Correctness

**File:** `.markdownlint.yaml`

✅ **Well Configured:**

- MD013 (line-length) disabled for flexibility
- MD033 (inline HTML) allowed
- MD034 (bare URLs) allowed for examples
- MD024 (duplicate headings) allows siblings_only

⚠️ **Missing Configuration:**

Add explicit rules for issues found:

```yaml
# Add to .markdownlint.yaml:

# MD050: Strong style - enforce asterisk
MD050:
  style: asterisk

# MD035: HR style - enforce hyphens
MD035:
  style: consistent

# MD003: Heading style - already set to 'atx'
# MD041: First line heading - already enabled
```

---

## 10. GitHub Actions Workflow Analysis

**File:** `.github/workflows/lint-and-validate.yml`

✅ **Correctly Configured:**

- Python 3.11 setup
- Pre-commit caching
- SKIP environment variable for `no-commit-to-branch`
- Multiple validation jobs (link-check, structure-audit, audit-gates)
- Artifact uploads for debugging

⚠️ **Improvements Needed:**

### Issue 1: Pre-commit Job Doesn't Handle Auto-Fixes

**Current (Line 39-42):**

```yaml
- name: Run pre-commit
  env:
    SKIP: no-commit-to-branch
  run: pre-commit run --all-files
```

**Improved:**

```yaml
- name: Run pre-commit
  env:
    SKIP: no-commit-to-branch
  run: |
    pre-commit run --all-files || {
      echo "❌ Pre-commit checks failed"
      echo ""
      echo "Files were modified by pre-commit hooks:"
      git diff --name-only
      echo ""
      echo "To fix, run locally:"
      echo "  pre-commit run --all-files"
      echo "  git add -A"
      echo "  git commit -m 'fix: apply pre-commit auto-formatting'"
      echo "  git push"
      exit 1
    }
```

### Issue 2: Markdown-Lint Job Is Redundant

The `markdown-lint` job (lines 44-89) is redundant because markdownlint is already included in pre-commit. This job could be removed to simplify the workflow.

**Recommendation:** Remove the entire `markdown-lint` job and rely on pre-commit.

### Issue 3: YAML-Lint Job Is Redundant

Same as markdown-lint - yamllint is already in pre-commit.

**Recommendation:** Remove the `yaml-lint` job.

---

## 11. Detailed Fix Plan (Step-by-Step)

### Phase 1: Immediate Fix (5 minutes)

```bash
# 1. Ensure you're on the correct branch
git checkout audit-gates-final/20251017

# 2. Install pre-commit if not already installed
pip install pre-commit

# 3. Run pre-commit to auto-fix everything
pre-commit run --all-files

# 4. Check what was changed
git status
git diff --stat

# 5. Commit the auto-fixes
git add -A
git commit -m "fix: apply pre-commit auto-formatting (JSON indentation, markdown style)

Automated fixes applied by pre-commit hooks:
- pretty-format-json: Fixed indentation in 16 JSON files
- markdownlint: Fixed style violations in 6 markdown files
  - MD050: Changed __bold__ to **bold**
  - MD035: Changed _____ to ---
  - MD041: Added H1 headings where missing
  - MD003: Changed setext to ATX heading style

All changes are cosmetic formatting only - no content modified.

Closes workflow failure: https://github.com/williamzujkowski/standards/actions/runs/18599316877"

# 6. Push to remote
git push origin audit-gates-final/20251017
```

### Phase 2: Manual Markdown Fixes (5 minutes)

Only needed if pre-commit doesn't auto-fix everything:

```bash
# Fix skills_alignment.md
cat > /tmp/fix.md << 'EOF'
# Skills Alignment

EOF
cat skills_alignment.md >> /tmp/fix.md
mv /tmp/fix.md skills_alignment.md

# Fix react SKILL.md setext heading
sed -i '5s/^===$//' skills/frontend/react/SKILL.md

# Commit manual fixes
git add skills_alignment.md skills/frontend/react/SKILL.md
git commit -m "fix: correct markdown heading violations not caught by auto-fix"
git push
```

### Phase 3: Prevent Future Issues (10 minutes)

```bash
# 1. Install pre-commit git hook locally
pre-commit install

# 2. Update pre-commit config to fix deprecated warnings
cat > /tmp/pre-commit-fix.yaml << 'EOF'
# Update these lines in .pre-commit-config.yaml:
default_stages: [pre-commit, pre-push]  # Line 327

# Update final-security-check hook:
stages: [pre-commit]  # Line 320
EOF

# Apply the fix manually or use sed:
sed -i 's/default_stages: \[commit, push\]/default_stages: [pre-commit, pre-push]/' .pre-commit-config.yaml
sed -i 's/stages: \[commit\]/stages: [pre-commit]/' .pre-commit-config.yaml

# 3. Add generated files to JSON exclusion
# (Edit .pre-commit-config.yaml line ~100 to add reports/generated/)

# 4. Commit configuration improvements
git add .pre-commit-config.yaml
git commit -m "fix: update pre-commit config to use new stage names"
git push
```

### Phase 4: Workflow Optimization (Optional - 15 minutes)

```bash
# 1. Remove redundant jobs from workflow
# Edit .github/workflows/lint-and-validate.yml
# Remove: markdown-lint job (lines 44-89)
# Remove: yaml-lint job (lines 91-108)

# 2. Improve pre-commit job error messages
# Add the improved run script shown in Section 10

# 3. Commit workflow improvements
git add .github/workflows/lint-and-validate.yml
git commit -m "refactor: remove redundant lint jobs (already in pre-commit)"
git push
```

---

## 12. Success Criteria

After applying all fixes, verify success:

### Local Checks

```bash
✅ pre-commit run --all-files     # Should pass with no modifications
✅ git status                      # Should show "working tree clean"
✅ pytest scripts/tests/          # All unit tests pass
✅ python3 scripts/generate-audit-reports.py  # Generates clean reports
```

### CI/CD Checks

```bash
✅ Lint and Validate workflow     # Should pass all jobs
✅ Pre-commit job                  # No files modified
✅ Link check                      # No broken links
✅ Structure audit                 # Pass audit gates
✅ Audit gates enforcement         # broken=0, hubs=0, orphans≤5
```

### Artifacts to Verify

```bash
✅ linkcheck.txt                   # No broken links
✅ structure-audit.json            # All gates satisfied
✅ hub-matrix.tsv                  # No violations
✅ standards-inventory.json        # Successfully generated
```

---

## 13. Long-Term Recommendations

### Documentation Standards

1. **Create Contributing Guide**
   - Add `.github/CONTRIBUTING.md` with pre-commit installation instructions
   - Document markdown style guidelines
   - Provide JSON formatting examples

2. **Add Pre-Commit Check to PR Template**

   ```markdown
   ## Pre-Submission Checklist
   - [ ] Pre-commit hooks installed (`pre-commit install`)
   - [ ] All pre-commit checks pass (`pre-commit run --all-files`)
   - [ ] No auto-formatting changes needed
   ```

3. **CI/CD Pipeline Improvements**
   - Add pre-commit check to branch protection rules
   - Require pre-commit status check before merge
   - Auto-comment on PRs with formatting instructions if checks fail

### Monitoring & Alerts

1. **Add Workflow Status Badge to README**

   ```markdown
   ![Lint Status](https://github.com/williamzujkowski/standards/actions/workflows/lint-and-validate.yml/badge.svg)
   ```

2. **Set Up Slack/Discord Notifications**
   - Notify on workflow failures
   - Include quick-fix instructions in alerts

---

## 14. Related Issues & References

### Recent Commits Addressing Similar Issues

- `5577cda` - fix: broaden yamllint ignore and fix comment spacing
- `2e30e42` - fix: correct gitleaks and yamllint configurations
- `d10e8f6` - fix: resolve all workflow failures identified by swarm investigation

### Configuration Files

- `.pre-commit-config.yaml` - Pre-commit hook definitions
- `.markdownlint.yaml` - Markdown linting rules
- `.yamllint.yaml` - YAML linting rules
- `.gitleaks.toml` - Secret scanning configuration
- `.github/workflows/lint-and-validate.yml` - CI/CD workflow

### Audit Scripts

- `scripts/ensure-hub-links.py` - Maintains hub link sections
- `scripts/generate-audit-reports.py` - Generates audit reports
- `scripts/tests/test_hub_enforcement.py` - Unit tests for hub enforcement

---

## 15. Questions & Answers

### Q: Why do these checks exist?

**A:** To maintain consistency, catch errors early, and ensure all documentation is accessible and properly linked.

### Q: Can I disable these checks temporarily?

**A:** Yes, but not recommended. Use `SKIP=hook-id git commit` for one-off exceptions.

### Q: What if I disagree with a markdown rule?

**A:** Update `.markdownlint.yaml` to disable specific rules, then document the reasoning in comments.

### Q: Why are JSON files being reformatted?

**A:** Consistent formatting improves git diffs, code review, and reduces merge conflicts.

### Q: Is this blocking other work?

**A:** No - other workflows (MkDocs, NIST compliance, health checks) are all passing.

---

## 16. Contact & Support

**For Issues:**

- GitHub Issues: https://github.com/williamzujkowski/standards/issues
- Workflow Runs: https://github.com/williamzujkowski/standards/actions

**Documentation:**

- Pre-commit: https://pre-commit.com/
- Markdownlint: https://github.com/DavidAnson/markdownlint
- YAML Lint: https://yamllint.readthedocs.io/

---

## Appendix A: Complete File List

### JSON Files Needing Auto-Format (16 files)

```
1.  reports/generated/standards-inventory.json
2.  skills/cloud-native/aws-advanced/templates/lambda-layer-structure/nodejs/package.json
3.  skills/cloud-native/aws-advanced/templates/step-functions-state-machine.json
4.  skills/coding-standards/javascript/resources/configs/jest.config.json
5.  skills/cloud-native/aws-advanced/templates/eventbridge-patterns.json
6.  skills/compliance/healthtech/templates/fhir-resources.json
7.  skills/security/authorization/templates/abac-policy.json
8.  skills/devops/monitoring-observability/templates/grafana-dashboard.json
9.  skills/database/advanced-optimization/templates/monitoring-dashboard.json
10. skills/testing/performance-testing/templates/grafana-dashboard.json
11. examples/nist-templates/quickstart/structure-audit.json
12. skills/security/security-operations/templates/security-metrics-dashboard.json
13. reports/generated/structure-audit.json
14. skills/compliance/fintech/templates/compliance-dashboard.json
15. skills/coding-standards/javascript/resources/configs/package.json
16. reports/generated/script-coverage.json
```

### Markdown Files With Violations (6 files)

```
1. skills_alignment.md (MD041 - no H1)
2. skills/frontend/react/SKILL.md (MD003 - setext heading)
3. docs/guides/SKILL_AUTHORING_GUIDE.md (MD024 - duplicate heading)
4. docs/migration/phase1-progress-tracker.md (MD050, MD035 - 18 violations)
5. docs/migration/phase2-progress-tracker.md (MD035 - 64 violations)
6. docs/migration/phase1-gate-checklist.md (MD035 - 3 violations)
7. docs/migration/phase2-gate-checklist.md (MD035 - 8 violations)
8. skills/security/zero-trust/resources/nist-800-207-checklist.md (MD035 - 9 violations)
```

---

## Appendix B: Command Reference

### Pre-Commit Commands

```bash
pre-commit install                    # Install git hooks
pre-commit run --all-files           # Run all hooks
pre-commit run <hook-id>             # Run specific hook
pre-commit run --all-files --show-diff-on-failure  # Show diffs
pre-commit clean                     # Clean cache
pre-commit autoupdate                # Update hook versions
SKIP=<hook-id> pre-commit run       # Skip specific hook
```

### Git Commands

```bash
git diff --name-only                 # List changed files
git diff --stat                      # Show change summary
git diff HEAD~1 HEAD                 # Show last commit changes
git reset --hard HEAD                # Discard all local changes
git commit --amend --no-edit        # Amend last commit
```

### Audit Commands

```bash
python3 scripts/ensure-hub-links.py                    # Update hub links
python3 scripts/generate-audit-reports.py              # Generate reports
pytest scripts/tests/test_hub_enforcement.py           # Run unit tests
cat reports/generated/structure-audit.json | jq '.'   # View audit JSON
```

---

**END OF REPORT**

Generated by: Code Analyzer Agent
Report Version: 1.0
Last Updated: 2025-10-17T16:52:00Z
