# Skills Compliance Test Specification

## Overview

Comprehensive TDD test suite for ensuring 100% skills compliance across all 61 skills in the repository.

## Test Files Created

1. **/home/william/git/standards/tests/validation/test_skills_structure.py**
2. **/home/william/git/standards/tests/validation/test_skills_token_budget.py**
3. **/home/william/git/standards/tests/validation/test_skills_content_quality.py**
4. **/home/william/git/standards/tests/validation/conftest.py** (updated with skill_file fixture)

## Test Coverage

### 1. Structure Tests (`test_skills_structure.py`)

**TestSkillFrontmatter**

- `test_has_yaml_frontmatter`: All skills must start with valid YAML frontmatter
- `test_has_name_field`: Frontmatter must include `name` field
- `test_has_description_field`: Frontmatter must include `description` field
- `test_description_min_length`: Description must be ≥50 characters

**TestSkillProgressiveDisclosure**

- `test_has_level_1_quick_start`: All skills must have Level 1: Quick Start section
- `test_has_level_2_implementation`: All skills must have Level 2: Implementation section
- `test_has_level_3_mastery`: All skills must have Level 3: Mastery section

**TestLevel1Subsections**

- `test_has_core_principles`: Level 1 must include Core Principles subsection
- `test_has_essential_checklist`: Level 1 must include Essential Checklist subsection
- `test_has_quick_example`: Level 1 must include example/quick reference section

**TestRequiredSections**

- `test_has_examples_section`: All skills must have Examples section
- `test_has_integration_points_section`: All skills must have Integration Points section
- `test_has_common_pitfalls_section`: All skills must have Common Pitfalls section

**TestStructuralIntegrity**

- `test_has_navigation_links`: Skills should have navigation breadcrumbs
- `test_no_placeholder_content`: No TODO, FIXME, TBD, or other placeholders allowed
- `test_markdown_formatting_valid`: Code blocks must be properly closed

### 2. Token Budget Tests (`test_skills_token_budget.py`)

**TestLevel1TokenBudget**

- `test_level1_within_budget`: Level 1 must be <200 tokens (quick overview)

**TestLevel2TokenBudget**

- `test_level2_within_budget`: Level 2 must be <3,000 tokens (detailed learning)

**TestLevel3TokenBudget**

- `test_level3_uses_filesystem_references`: Level 3 should use external references, not inline content (<500 tokens inline)

**TestTotalTokenBudget**

- `test_total_inline_content_budget`: Total inline content <5,000 tokens

**TestTokenBudgetDistribution**

- `test_level1_is_smallest`: Level 1 must be smaller than Level 2 (progressive disclosure)
- `test_frontmatter_within_budget`: Description should be <100 tokens

**TestCodeBlockBudget**

- `test_code_blocks_reasonable_size`: Individual code blocks should be <500 tokens

### 3. Content Quality Tests (`test_skills_content_quality.py`)

**TestExamplesQuality**

- `test_has_working_code_examples`: Minimum 1 code block per skill
- `test_examples_have_language_specified`: Code blocks must specify language (```python, etc.)
- `test_examples_have_comments`: Code examples should include explanatory comments

**TestIntegrationPointsQuality**

- `test_lists_specific_integrations`: Minimum 2 specific integrations listed

**TestCommonPitfallsQuality**

- `test_has_minimum_pitfalls`: Minimum 3 documented pitfalls
- `test_pitfalls_have_examples`: Pitfalls should show bad examples (❌) and good alternatives (✅)

**TestContentCompleteness**

- `test_no_placeholder_content`: No TODO, FIXME, TBD, etc.
- `test_no_empty_sections`: All sections must have content
- `test_has_actionable_content`: Minimum 3 actionable elements (code, checklists, commands)

**TestCrossReferences**

- `test_internal_links_valid`: Anchor links must point to existing headings
- `test_skill_references_exist`: References to other skills must exist

## Execution Results (RED Phase)

**Total Tests**: ~1,952 tests (32 test types × 61 skills)

**Current Status**: FAILING (as expected in RED phase)

### Sample Failures Detected:

1. **Invalid YAML frontmatter**: `patterns`, `gdpr` skills
2. **Missing sections**: Multiple skills missing Examples, Integration Points, or Common Pitfalls
3. **Placeholder content**: 19 skills contain TODO/FIXME/TBD placeholders
4. **Token budget violations**: Multiple skills exceed token budgets
5. **Broken internal links**: 10 skills have broken anchor links
6. **Missing skill references**: 11 skills reference non-existent skills

## Usage

### Run All Skills Compliance Tests

```bash
pytest tests/validation/test_skills_structure.py \
       tests/validation/test_skills_token_budget.py \
       tests/validation/test_skills_content_quality.py -v
```

### Run Specific Test Class

```bash
pytest tests/validation/test_skills_structure.py::TestSkillFrontmatter -v
```

### Run Single Skill Validation

```bash
pytest tests/validation/ -k "python" -v
```

### Generate Detailed Report

```bash
pytest tests/validation/ \
  --tb=short \
  --junit-xml=reports/skills-compliance.xml \
  -v > reports/skills-test-results.txt
```

## Implementation Path (GREEN Phase)

Once these tests pass (GREEN), we will have achieved:

1. **100% structural compliance** - All 61 skills follow progressive disclosure
2. **100% token budget compliance** - All skills respect cognitive load limits
3. **100% content quality** - All skills have examples, integrations, and pitfalls
4. **0 placeholders** - All content complete and production-ready
5. **Valid cross-references** - All internal links and skill references working

## Test Design Principles

1. **Parametrized**: All tests run against all 61 skills automatically
2. **Descriptive failures**: Error messages show exactly what's wrong and how to fix it
3. **Progressive**: Tests can be run incrementally as skills are fixed
4. **Maintainable**: Adding new compliance rules is straightforward
5. **Fast**: Structure and token tests run in <1 second

## Next Steps

1. Fix skills with invalid YAML frontmatter
2. Add missing required sections (Examples, Integration Points, Common Pitfalls)
3. Remove all placeholder content (TODO, FIXME, TBD)
4. Optimize token budgets (move content to external files)
5. Fix broken internal links and skill references
6. Re-run tests until all pass (GREEN phase)

## Swarm Coordination

**Memory Key**: `swarm/tdd/skills_tests`

**Handoff to Implementation Agents**:

- Coder agents can use these tests to verify fixes
- Each skill can be fixed independently (parallelizable)
- Tests provide clear acceptance criteria
- No guesswork - tests define "done"

## Verification

```bash
# Verify tests exist
ls -lh tests/validation/test_skills_*.py

# Count total tests
pytest tests/validation/test_skills_*.py --collect-only | grep "test session starts" -A 1

# Run single skill to see detailed failures
pytest tests/validation/ -k "python" -v --tb=short
```

## Success Metrics

- **Target**: 100% pass rate (all 1,952 tests passing)
- **Current**: ~40% pass rate (estimated 780 passing, 1,172 failing)
- **Priority failures**: Placeholder content (19), broken links (21), token budgets (TBD)

---

**Created**: 2025-10-24
**TDD Agent**: tdd-london-swarm
**Status**: RED phase complete ✅
**Next**: GREEN phase (implementation)
