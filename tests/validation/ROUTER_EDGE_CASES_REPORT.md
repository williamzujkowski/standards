# Router Edge Cases and Issues Report

**Generated**: 2025-10-24
**Test Suite**: Router Edge Case Validation
**Status**: ⚠️ 1 ISSUE FOUND

## Test Results: 18/19 PASSED

| Test Category | Tests | Status |
|--------------|-------|--------|
| Product Matrix Edge Cases | 4 | ⚠️ 1 FAILED |
| Skill Loader Edge Cases | 4 | ✅ PASS |
| Audit Rules Edge Cases | 4 | ✅ PASS |
| Cross-System Consistency | 3 | ✅ PASS |
| Error Handling | 3 | ✅ PASS |

---

## CRITICAL ISSUE FOUND

### Issue #1: CLI Product Missing NIST-IG:base

**Severity**: MEDIUM
**Impact**: Compliance policy violation
**Test**: `test_nist_auto_inclusion_on_security`

#### Problem

The `cli` product type includes security standard `SEC:secrets` but does not auto-include `NIST-IG:base`.

**Current Configuration**:

```yaml
cli:
  description: "Command-line tool or utility"
  standards:
    - CS:language
    - TS:unit
    - SEC:secrets        # ← Security standard present
    - DOP:packaging
    - TOOL:cli
    # ❌ Missing: NIST-IG:base
```

**Expected Configuration**:

```yaml
cli:
  description: "Command-line tool or utility"
  standards:
    - CS:language
    - TS:unit
    - SEC:secrets
    - DOP:packaging
    - TOOL:cli
    - NIST-IG:base       # ✅ Should be included
```

#### Root Cause

Per the configuration policy in `/home/william/git/standards/config/product-matrix.yaml`:

```yaml
defaults:
  include_nist_on_security: true  # Policy: Auto-include NIST when SEC is present
```

The `cli` product violates this policy by including a security standard without NIST baseline.

#### Recommended Fix

**Option 1: Add NIST-IG:base to CLI product** (Recommended)

```yaml
# File: config/product-matrix.yaml
cli:
  description: "Command-line tool or utility"
  standards:
    - CS:language
    - TS:unit
    - SEC:secrets
    - DOP:packaging
    - TOOL:cli
    - NIST-IG:base       # Add this line
```

**Option 2: Remove SEC:secrets if NIST compliance not required**

If CLI tools truly don't need NIST compliance:

- Remove `SEC:secrets` from the standards list
- Document why CLI tools are exempt from security baseline

**Option 3: Create explicit exemption**

Add to product-matrix.yaml:

```yaml
exemptions:
  - product: cli
    standard: NIST-IG:base
    reason: "CLI tools with only secrets management don't require full NIST baseline"
```

#### Recommendation

**ACTION**: Add NIST-IG:base to CLI product (Option 1)

**Rationale**:

- Command-line tools handling secrets need compliance baseline
- Aligns with repository policy: `include_nist_on_security: true`
- Consistent with other product types (api, web-service, data-pipeline, etc.)

---

## All Other Tests: PASSED ✅

### Product Matrix Edge Cases (3/4 passed)

#### ✅ test_wildcard_sec_includes_nist

Verified that SEC:* wildcard expansion includes NIST-IG:base.

**Result**: PASS

#### ✅ test_no_circular_dependencies

Verified no stack presets reference other stack presets (no circular deps).

**Result**: PASS

#### ✅ test_language_cs_consistency

Verified language mappings follow pattern: `CS:{language}`.

**Validated Languages**:

- Python → CS:python
- JavaScript → CS:javascript
- TypeScript → CS:typescript
- Go → CS:go
- Java → CS:java

**Result**: PASS

#### ✅ test_no_duplicate_standards_in_products

Verified products don't have duplicate standards entries.

**Result**: PASS (no duplicates found)

---

### Skill Loader Edge Cases (4/4 passed)

#### ✅ test_auto_inclusion_rules

Verified auto-inclusion rules have required fields:

- condition
- includes
- reason

**Result**: PASS

#### ✅ test_deprecation_settings

Verified deprecation configuration is complete:

- enabled: true
- warning_template: present
- removal_date: 2026-04-16

**Result**: PASS

#### ✅ test_skill_level_consistency

Verified all skill levels are valid (1, 2, or 3).

**Result**: PASS (all levels valid)

#### ✅ test_wildcard_nist_inclusion

Verified SEC:* wildcard in legacy-mappings includes nist-compliance/baseline.

**Result**: PASS

---

### Audit Rules Edge Cases (4/4 passed)

#### ✅ test_hub_requirements_no_duplicates

Verified no duplicate hub requirement patterns.

**Result**: PASS (no duplicates)

#### ✅ test_exclusions_dont_overlap_requirements

Verified exclusion patterns don't conflict with hub requirements.

**Result**: PASS (no conflicts)

#### ✅ test_limits_non_negative

Verified all audit limits are non-negative:

- broken_links: 0
- hub_violations: 0
- max_orphans: 5

**Result**: PASS

#### ✅ test_all_hubs_have_reasonable_paths

Verified hub paths are not too deeply nested (max depth: 5 levels).

**Result**: PASS (all hubs reasonable depth)

---

### Cross-System Consistency (3/3 passed)

#### ✅ test_product_types_aligned

Verified product types align across product-matrix.yaml and legacy-mappings.yaml.

**Shared Products**: 8

- api, web-service, frontend-web, mobile, data-pipeline, ml-service, cli

**Result**: PASS (sufficient overlap)

#### ✅ test_wildcard_keys_aligned

Verified wildcard keys match exactly across systems.

**Wildcards**: SEC:*, TS:*, DOP:*, FE:*

**Result**: PASS (perfect match)

#### ✅ test_nist_auto_inclusion_consistent

Verified NIST auto-inclusion logic is consistent:

- Product matrix: `include_nist_on_security: true`
- Legacy mappings: Auto-inclusion rule for SEC conditions

**Result**: PASS

---

### Error Handling (3/3 passed)

#### ✅ test_malformed_pattern_detection

Verified handling of edge case patterns:

- Empty strings
- Double wildcards
- Parent directory references

**Result**: PASS

#### ✅ test_yaml_structure_validation

Verified YAML files have expected top-level structure:

- product-matrix.yaml: version, defaults, products, wildcards
- audit-rules.yaml: version, limits, orphans

**Result**: PASS

#### ✅ test_version_fields_present

Verified all configs have version fields:

- config/product-matrix.yaml: ✅
- config/audit-rules.yaml: ✅
- skills/legacy-bridge/resources/legacy-mappings.yaml: ✅

**Result**: PASS

---

## Edge Cases Validated

### 1. NIST Auto-Inclusion Policy

**Policy**: When any SEC standard is present, NIST-IG:base must be included.

**Validation Results**:

- ✅ api: Has SEC standards + NIST-IG:base
- ✅ web-service: Has SEC standards + NIST-IG:base
- ✅ frontend-web: Has SEC standards + NIST-IG:base
- ✅ mobile: Has SEC standards + NIST-IG:base
- ✅ data-pipeline: Has SEC standards + NIST-IG:base
- ✅ ml-service: Has SEC standards + NIST-IG:base
- ✅ infra-module: Has SEC standards + NIST-IG:base
- ❌ cli: Has SEC:secrets but missing NIST-IG:base **(ISSUE)**

### 2. Circular Dependencies

**Check**: Stack presets should not reference other stack presets.

**Validation Results**:

- ✅ MERN → uses: web-service (product type, not stack)
- ✅ MEAN → uses: web-service (product type, not stack)
- ✅ LAMP → uses: web-service (product type, not stack)
- ✅ JAMstack → uses: frontend-web (product type, not stack)

**Result**: No circular dependencies

### 3. Duplicate Standards

**Check**: Products should not have duplicate standards in their lists.

**Validation Results**: All products clean (no duplicates)

### 4. Wildcard Consistency

**Check**: Wildcard definitions match across product-matrix and legacy-mappings.

**Validation Results**:

- ✅ SEC:* consistent
- ✅ TS:* consistent
- ✅ DOP:* consistent
- ✅ FE:* consistent

### 5. Hub Requirement Conflicts

**Check**: Excluded patterns should not overlap with required hub patterns.

**Validation Results**: No conflicts detected

---

## Test Execution Details

### Command

```bash
python3 -m pytest tests/integration/test_router_edge_cases.py -v --tb=short
```

### Output

```
collected 19 items

tests/integration/test_router_edge_cases.py::TestProductMatrixEdgeCases::test_nist_auto_inclusion_on_security FAILED
tests/integration/test_router_edge_cases.py::TestProductMatrixEdgeCases::test_wildcard_sec_includes_nist PASSED
tests/integration/test_router_edge_cases.py::TestProductMatrixEdgeCases::test_no_circular_dependencies PASSED
tests/integration/test_router_edge_cases.py::TestProductMatrixEdgeCases::test_language_cs_consistency PASSED
tests/integration/test_router_edge_cases.py::TestProductMatrixEdgeCases::test_no_duplicate_standards_in_products PASSED
tests/integration/test_router_edge_cases.py::TestSkillLoaderEdgeCases::test_auto_inclusion_rules PASSED
tests/integration/test_router_edge_cases.py::TestSkillLoaderEdgeCases::test_deprecation_settings PASSED
tests/integration/test_router_edge_cases.py::TestSkillLoaderEdgeCases::test_skill_level_consistency PASSED
tests/integration/test_router_edge_cases.py::TestSkillLoaderEdgeCases::test_wildcard_nist_inclusion PASSED
tests/integration/test_router_edge_cases.py::TestAuditRulesEdgeCases::test_hub_requirements_no_duplicates PASSED
tests/integration/test_router_edge_cases.py::TestAuditRulesEdgeCases::test_exclusions_dont_overlap_requirements PASSED
tests/integration/test_router_edge_cases.py::TestAuditRulesEdgeCases::test_limits_non_negative PASSED
tests/integration/test_router_edge_cases.py::TestAuditRulesEdgeCases::test_all_hubs_have_reasonable_paths PASSED
tests/integration/test_router_edge_cases.py::TestCrossSystemConsistency::test_product_types_aligned PASSED
tests/integration/test_router_edge_cases.py::TestCrossSystemConsistency::test_wildcard_keys_aligned PASSED
tests/integration/test_router_edge_cases.py::TestCrossSystemConsistency::test_nist_auto_inclusion_consistent PASSED
tests/integration/test_router_edge_cases.py::TestErrorHandling::test_malformed_pattern_detection PASSED
tests/integration/test_router_edge_cases.py::TestErrorHandling::test_yaml_structure_validation PASSED
tests/integration/test_router_edge_cases.py::TestErrorHandling::test_version_fields_present PASSED

========================= 1 failed, 18 passed in 0.39s =========================
```

---

## Recommendations

### Immediate Action Required

**Fix CLI Product Configuration**

```bash
# Edit config/product-matrix.yaml
# Add NIST-IG:base to cli product standards list
```

### Future Enhancements

1. **Automated Policy Enforcement**
   - Add pre-commit hook to validate NIST auto-inclusion
   - Fail CI if policy is violated

2. **Configuration Validation Tool**
   - Create `validate-product-matrix.py` script
   - Run as part of CI/CD pipeline

3. **Documentation**
   - Document NIST auto-inclusion policy in CLAUDE.md
   - Add examples of compliant vs non-compliant configurations

### Test Coverage Metrics

**Edge Case Coverage**: 19 tests

- Product Matrix: 5 tests
- Skill Loader: 4 tests
- Audit Rules: 4 tests
- Cross-System: 3 tests
- Error Handling: 3 tests

**Overall Router Test Coverage**:

- Main validation: 26 tests (all passed)
- Edge cases: 19 tests (18 passed, 1 failed)
- **Total: 45 tests** (44 passed, 1 issue found)

---

## Conclusion

Router validation comprehensive with **97.8% pass rate** (44/45 tests).

**Single Issue**: CLI product missing NIST-IG:base (policy violation)

**Recommendation**: Add NIST-IG:base to CLI product configuration.

**Overall Assessment**: Router infrastructure is robust with one minor configuration issue.

---

**Report Author**: REVIEWER Agent
**Date**: 2025-10-24
**Test Framework**: pytest 8.3.0
**Python**: 3.12.3
