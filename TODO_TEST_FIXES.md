# TODO: Test Suite Fixes

This document tracks all issues identified by our test suite that need to be fixed to achieve full compliance with KNOWLEDGE_MANAGEMENT_STANDARDS.md.

## 🧪 Test Suite Execution

### Pre-fix Baseline
- [ ] Run full test suite and capture baseline results
  ```bash
  python3 tests/validate_cross_references.py > test_results_baseline.txt 2>&1
  python3 lint/standards-linter.py > lint_results_baseline.txt 2>&1
  ```

## 🔧 Critical Fixes (Errors)

### 1. MANIFEST.yaml Completeness
- [ ] Add UNIFIED_STANDARDS.md entry to MANIFEST.yaml
  ```yaml
  UNIFIED:
    identifier: "UNIFIED"
    full_name: "UNIFIED_STANDARDS.md"
    size: "45KB"
    token_estimate: 12000
    sections:
      overview:
        tokens: 500
        priority: "critical"
        description: "Comprehensive overview"
    dependencies:
      requires: []
      recommends: ["CS", "TS", "SEC"]
  ```

### 2. Missing Metadata Headers (20 files)
Add to each *_STANDARDS.md file after the title:
- [ ] CLOUD_NATIVE_STANDARDS.md
- [ ] CODING_STANDARDS.md
- [ ] CONTENT_STANDARDS.md
- [ ] COST_OPTIMIZATION_STANDARDS.md
- [ ] DATA_ENGINEERING_STANDARDS.md
- [ ] DEVOPS_PLATFORM_STANDARDS.md
- [ ] EVENT_DRIVEN_STANDARDS.md
- [ ] FRONTEND_MOBILE_STANDARDS.md
- [ ] GITHUB_PLATFORM_STANDARDS.md
- [ ] LEGAL_COMPLIANCE_STANDARDS.md
- [ ] MODERN_SECURITY_STANDARDS.md
- [ ] OBSERVABILITY_STANDARDS.md
- [ ] PROJECT_MANAGEMENT_STANDARDS.md
- [ ] SEO_WEB_MARKETING_STANDARDS.md
- [ ] TESTING_STANDARDS.md
- [ ] TOOLCHAIN_STANDARDS.md
- [ ] WEB_DESIGN_UX_STANDARDS.md
- [ ] UNIFIED_STANDARDS.md
- [ ] VALIDATION_PATTERNS.md
- [ ] LLM_TRAINING.md

Template:
```markdown
**Version:** 1.0.0
**Last Updated:** 2025-01-13
**Status:** Active
**Standard Code:** XX (2-4 letters)

---
```

### 3. Missing Required Sections
Add "## Overview" and "## Implementation" sections to:
- [ ] CLOUD_NATIVE_STANDARDS.md
- [ ] CODING_STANDARDS.md
- [ ] CONTENT_STANDARDS.md
- [ ] COST_OPTIMIZATION_STANDARDS.md
- [ ] DATA_ENGINEERING_STANDARDS.md
- [ ] DEVOPS_PLATFORM_STANDARDS.md
- [ ] EVENT_DRIVEN_STANDARDS.md
- [ ] FRONTEND_MOBILE_STANDARDS.md
- [ ] GITHUB_PLATFORM_STANDARDS.md
- [ ] LEGAL_COMPLIANCE_STANDARDS.md
- [ ] MODERN_SECURITY_STANDARDS.md
- [ ] OBSERVABILITY_STANDARDS.md
- [ ] PROJECT_MANAGEMENT_STANDARDS.md
- [ ] SEO_WEB_MARKETING_STANDARDS.md
- [ ] TESTING_STANDARDS.md
- [ ] TOOLCHAIN_STANDARDS.md
- [ ] WEB_DESIGN_UX_STANDARDS.md
- [ ] UNIFIED_STANDARDS.md
- [ ] VALIDATION_PATTERNS.md

### 4. Broken Cross-References
Fix or remove broken links:
- [ ] GITHUB_PLATFORM_STANDARDS.md -> docs/api.md (create file or remove link)
- [ ] GITHUB_PLATFORM_STANDARDS.md -> CODE_OF_CONDUCT.md (create file or remove link)
- [ ] GITHUB_PLATFORM_STANDARDS.md -> LICENSE (create file or remove link)
- [ ] GITHUB_PLATFORM_STANDARDS.md -> CONTRIBUTING.md (link to existing file)

## ⚠️ Important Fixes (Warnings)

### 5. CLAUDE.md Routing Coverage
Add missing standard codes to CLAUDE.md natural language mappings:
- [ ] PM (PROJECT_MANAGEMENT_STANDARDS.md)
- [ ] CONT (CONTENT_STANDARDS.md)
- [ ] SEO (SEO_WEB_MARKETING_STANDARDS.md)
- [ ] TOOL (TOOLCHAIN_STANDARDS.md)
- [ ] COST (COST_OPTIMIZATION_STANDARDS.md)
- [ ] TS (TESTING_STANDARDS.md)
- [ ] OBS (OBSERVABILITY_STANDARDS.md)
- [ ] WD (WEB_DESIGN_UX_STANDARDS.md)
- [ ] EVT (EVENT_DRIVEN_STANDARDS.md)
- [ ] SEC (MODERN_SECURITY_STANDARDS.md)
- [ ] LEG (LEGAL_COMPLIANCE_STANDARDS.md)
- [ ] GH (GITHUB_PLATFORM_STANDARDS.md)

### 6. STANDARDS_INDEX.md Coverage
Add all missing standards to the index:
- [ ] Update STANDARDS_INDEX.md to include all 19 missing standards files

### 7. Bidirectional Links
Make these links bidirectional:
- [ ] Add link from CONTRIBUTING.md back to GITHUB_PLATFORM_STANDARDS.md
- [ ] Add link from STANDARD_TEMPLATE.md back to KNOWLEDGE_MANAGEMENT_STANDARDS.md
- [ ] Add link from CODING_STANDARDS.md back to KNOWLEDGE_MANAGEMENT_STANDARDS.md
- [ ] Add link from TESTING_STANDARDS.md back to KNOWLEDGE_MANAGEMENT_STANDARDS.md
- [ ] Add link from CREATING_STANDARDS_GUIDE.md back to KNOWLEDGE_MANAGEMENT_STANDARDS.md
- [ ] Add link from MANIFEST.yaml references back to KNOWLEDGE_MANAGEMENT_STANDARDS.md
- [ ] Add link from CLAUDE.md back to KNOWLEDGE_MANAGEMENT_STANDARDS.md

### 8. Code Block Language Specifiers
Add language specifiers to all code blocks (``` → ```language):
- [ ] Review all standards files and add appropriate language specifiers

### 9. Implementation Checklists
Add implementation checklists to files missing them:
- [ ] Review each standard and add an "## Implementation Checklist" section

### 10. Standard Codes
Add Standard Code metadata to files missing them:
- [ ] Assign 2-4 letter codes to each standard file

## 📊 Post-Fix Validation

### Final Testing
- [ ] Run full test suite after fixes
  ```bash
  python3 tests/validate_cross_references.py > test_results_final.txt 2>&1
  python3 lint/standards-linter.py > lint_results_final.txt 2>&1
  ```
- [ ] Compare baseline vs final results
- [ ] Ensure all errors are resolved
- [ ] Document any remaining warnings that are acceptable

### Quality Checks
- [ ] Run pre-commit hooks on all changes
  ```bash
  pre-commit run --all-files
  ```
- [ ] Update CHANGELOG.md with fixes applied
- [ ] Create PR with all fixes

## 🎯 Success Criteria

- All error-level issues resolved
- Warning count reduced by >80%
- All tests passing in CI/CD
- Pre-commit hooks passing

## 📝 Notes

- Some warnings may be acceptable (e.g., very long reference sections)
- Token efficiency warnings are informational only
- Focus on errors first, then high-impact warnings
- Use `python3 tests/fix_validation_issues.py` for automated fixes where possible

---

**Estimated Time**: 4-6 hours for all fixes
**Priority**: High - these fixes ensure repository compliance with our own standards