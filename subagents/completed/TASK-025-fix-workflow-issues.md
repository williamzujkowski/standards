# Task Assignment: Fix Workflow Issues

**Task ID:** TASK-025
**Priority:** High
**Assigned:** 2025-01-20

## Issues to Fix

### 1. Missing npm script in NIST compliance workflow
- **Location:** `.github/workflows/nist-compliance.yml`
- **Issue:** References `validate-file` npm script that doesn't exist
- **Solution:** Add the missing script to `standards/compliance/package.json` or update workflow to use correct script name

### 2. Inaccessible GitHub Action SHA pins
- **Issue:** 3 action SHA pins return 422 errors when accessed
- **Solution:** Update to valid, accessible SHA commits for these actions

### 3. Minor YAML formatting issues
- **Issue:** Comment spacing and line length warnings
- **Solution:** Fix formatting to pass yamllint without warnings

## Testing Requirements
- Verify workflows pass validation after fixes
- Test that all referenced scripts exist
- Ensure action SHAs are accessible
- Validate YAML formatting is correct

## Expected Output Location
`/subagents/reports/REPORT-025-workflow-fixes.md`