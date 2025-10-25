# Router Validation - Next Steps

**Date**: 2025-10-24
**Priority**: MEDIUM
**Estimated Time**: 15 minutes

---

## Immediate Action Required

### Fix CLI Product NIST-IG:base Issue

**File**: `/home/william/git/standards/config/product-matrix.yaml`
**Line**: ~46
**Time**: 2 minutes

**Current State**:

```yaml
cli:
  description: "Command-line tool or utility"
  standards:
    - CS:language
    - TS:unit
    - SEC:secrets       # ← Security standard present
    - DOP:packaging
    - TOOL:cli
    # Missing: NIST-IG:base
```

**Required Change**:

```yaml
cli:
  description: "Command-line tool or utility"
  standards:
    - CS:language
    - TS:unit
    - SEC:secrets
    - DOP:packaging
    - TOOL:cli
    - NIST-IG:base       # ← Add this line
```

**Steps**:

1. Open `/home/william/git/standards/config/product-matrix.yaml`
2. Find the `cli:` section (around line 46)
3. Add `- NIST-IG:base` to the standards list
4. Save the file
5. Run: `pytest tests/integration/test_router_edge_cases.py::TestProductMatrixEdgeCases::test_nist_auto_inclusion_on_security -v`
6. Verify test passes

**Expected Result**: All 45 router validation tests should pass

---

## Optional Improvements

### 1. Integrate Tests into CI/CD (15 minutes)

**File**: `.github/workflows/lint-and-validate.yml`

**Add After Existing Tests**:

```yaml
- name: Router Validation Tests
  run: |
    echo "Validating routing configuration..."
    pytest tests/integration/test_router_validation.py -v
    pytest tests/integration/test_router_edge_cases.py -v

- name: Upload Router Test Results
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: router-test-results
    path: |
      tests/validation/ROUTER_VALIDATION_REPORT.md
      tests/validation/ROUTER_EDGE_CASES_REPORT.md
```

### 2. Add Pre-commit Hook (5 minutes)

**File**: `.pre-commit-config.yaml`

**Add to Existing Hooks**:

```yaml
- repo: local
  hooks:
    - id: router-validation
      name: Validate Router Configuration
      entry: pytest tests/integration/test_router_validation.py -q --tb=no
      language: system
      pass_filenames: false
      files: ^(config/.*\.yaml|scripts/skill-loader\.py|scripts/ensure-hub-links\.py)$
```

**Test**:

```bash
pre-commit run router-validation --all-files
```

### 3. Create Automated Sync Check (Future)

**File**: `scripts/check-router-sync.py` (to be created)

**Purpose**: Verify product-matrix.yaml and legacy-mappings.yaml stay synchronized

**Integration**: Add to pre-commit hooks

---

## Verification Steps

After fixing the CLI issue, run these commands to verify:

```bash
# 1. Run specific failing test
pytest tests/integration/test_router_edge_cases.py::TestProductMatrixEdgeCases::test_nist_auto_inclusion_on_security -v

# 2. Run all router tests
pytest tests/integration/test_router_validation.py -v
pytest tests/integration/test_router_edge_cases.py -v

# 3. Quick validation script
bash scripts/validate-router.sh

# 4. Check all tests pass
pytest tests/integration/test_router_*.py -v
```

**Expected Output**: `45 passed in ~0.75s`

---

## Documentation Updates

No documentation updates required - all reports are already generated:

- ✅ `/home/william/git/standards/tests/validation/ROUTER_VALIDATION_REPORT.md`
- ✅ `/home/william/git/standards/tests/validation/ROUTER_EDGE_CASES_REPORT.md`
- ✅ `/home/william/git/standards/tests/integration/TESTING_SUMMARY.md`
- ✅ `/home/william/git/standards/ROUTER_VALIDATION_SUMMARY.md`

---

## Success Metrics

After completing the fix:

- ✅ 45/45 router tests pass (100%)
- ✅ No routing configuration issues
- ✅ NIST auto-inclusion policy fully enforced
- ✅ All product types compliant

---

## Timeline

| Task | Time | Priority |
|------|------|----------|
| Fix CLI NIST issue | 2 min | HIGH |
| Verify tests pass | 3 min | HIGH |
| Add to CI/CD | 15 min | MEDIUM |
| Add pre-commit hook | 5 min | MEDIUM |
| **Total** | **25 min** | - |

---

## Questions?

See the comprehensive documentation:

- **Quick Start**: `/home/william/git/standards/tests/integration/README.md`
- **Detailed Results**: `/home/william/git/standards/tests/validation/ROUTER_VALIDATION_REPORT.md`
- **Edge Cases**: `/home/william/git/standards/tests/validation/ROUTER_EDGE_CASES_REPORT.md`
- **Full Summary**: `/home/william/git/standards/ROUTER_VALIDATION_SUMMARY.md`

Or run:

```bash
pytest tests/integration/test_router_validation.py --help
```

---

**Status**: Ready for implementation
**Blocker**: None
**Risk**: Low (single line change, well-tested)
