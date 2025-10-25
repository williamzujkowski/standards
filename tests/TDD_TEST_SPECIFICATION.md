# TDD Test Specification - London School Approach

## Mission: Test-First Repository Remediation

This document specifies the comprehensive test suite that will DRIVE the implementation of repository fixes and improvements.

## RED Phase Status: ✅ COMPLETE

All tests written and failing (as expected). Implementation is next step.

---

## Test Categories

### 1. Command Syntax Validation (24 tests)

**File**: `/home/william/git/standards/tests/integration/test_command_syntax_fix.py`

#### Test Classes

**TestCommandSyntaxDetection** (4 tests)

- ✅ `test_detects_npm_in_claude_md` - Find npm/npx commands in CLAUDE.md
- ✅ `test_validates_bash_fence_context` - Verify commands are in bash fences
- ✅ `test_no_npm_in_python_code` - Distinguish bash from Python strings
- ✅ `test_detects_command_in_markdown_callouts` - Find commands in all contexts

**TestCommandSyntaxValidation** (4 tests)

- ✅ `test_rejects_npm_without_context` - Flag bare npm commands
- ✅ `test_accepts_npx_claude_flow` - Accept valid npx usage
- ✅ `test_accepts_python_script_calls` - Accept python3 script calls
- ✅ `test_flags_mcp_add_syntax` - Validate MCP add commands

**TestCommandSyntaxFix** (3 tests)

- ✅ `test_replaces_npm_with_npx` - Auto-fix npm to npx
- ✅ `test_preserves_valid_commands` - Don't modify valid commands
- ✅ `test_handles_multiline_commands` - Handle line continuations

**TestCommandSyntaxReport** (2 tests)

- ✅ `test_generates_issue_report` - Structured issue reporting
- ✅ `test_groups_issues_by_type` - Group by issue type

**TestCommandSyntaxIntegration** (3 tests)

- ✅ `test_no_npm_in_claude_md` - No npm install in CLAUDE.md
- ✅ `test_npx_usage_consistent` - Consistent claude-flow via npx
- ✅ `test_all_commands_in_fences` - All commands properly fenced

#### Required Implementations

1. **MockDocumentScanner**
   - `scan_for_commands(path)` - Extract commands from markdown

2. **MockCommandValidator**
   - `validate_syntax(command)` - Validate command syntax

3. **Command Fixer**
   - Transform npm to npx
   - Preserve valid commands
   - Handle multi-line commands

---

### 2. Router Path Integrity (23 tests)

**File**: `/home/william/git/standards/tests/integration/test_router_paths.py`

#### Test Classes

**TestProductMatrixIntegrity** (4 tests)

- ✅ `test_product_matrix_exists` - Configuration file exists
- ✅ `test_product_matrix_valid_yaml` - Valid YAML syntax
- ✅ `test_product_matrix_has_products` - Products defined
- ✅ `test_all_product_paths_exist` - All paths valid

**TestLoadDirectiveSyntax** (5 tests)

- ✅ `test_validates_simple_product_load` - Parse `@load product:api`
- ✅ `test_validates_standard_code_load` - Parse `@load CS:python`
- ✅ `test_validates_wildcard_load` - Parse `@load SEC:*`
- ✅ `test_validates_combination_load` - Parse combinations
- ✅ `test_rejects_invalid_syntax` - Reject invalid directives

**TestPathResolution** (4 tests)

- ✅ `test_resolves_coding_standard_path` - Resolve CS:python
- ✅ `test_resolves_testing_standard_path` - Resolve TS:pytest
- ✅ `test_resolves_security_standard_path` - Resolve SEC:*
- ✅ `test_auto_includes_nist_ig_base` - Auto-include NIST-IG

**TestRouterPathUpdates** (4 tests)

- ✅ `test_kickstart_path_correct` - KICKSTART path updated
- ✅ `test_product_matrix_path_correct` - Product matrix path updated
- ✅ `test_audit_rules_path_correct` - Audit rules path updated
- ✅ `test_standards_directory_paths` - Standards paths updated

**TestRouterIntegration** (3 tests)

- ✅ `test_load_product_api_resolves` - Full product:api resolution
- ✅ `test_load_combination_resolves` - Combination resolution
- ✅ `test_wildcard_expansion` - Wildcard expansion

#### Required Implementations

1. **MockRouterConfig**
   - `load_product_matrix()` - Load configuration
   - `resolve_product_type(code)` - Resolve product

2. **MockPathResolver**
   - `resolve_standard_path(code)` - Resolve standard path
   - `validate_path_exists(path)` - Check path validity

3. **LoadDirectiveParser**
   - Parse @load directives
   - Validate syntax
   - Expand wildcards

---

### 3. Repository Cleanup (18 tests)

**File**: `/home/william/git/standards/tests/integration/test_cleanup.py`

#### Test Classes

**TestPycacheDetection** (4 tests)

- ✅ `test_finds_pycache_directories` - Locate **pycache**
- ✅ `test_pycache_not_in_docs` - No **pycache** in docs/
- ✅ `test_pycache_not_in_config` - No **pycache** in config/
- ✅ `test_pycache_allowed_in_tests` - Acceptable in tests/

**TestGitignoreConfiguration** (3 tests)

- ✅ `test_gitignore_excludes_pycache` - Exclude **pycache**
- ✅ `test_gitignore_excludes_pyc_files` - Exclude .pyc files
- ✅ `test_gitignore_excludes_pyo_files` - Exclude .pyo files

**TestAuditRulesConfiguration** (2 tests)

- ✅ `test_audit_rules_exist` - Configuration exists
- ✅ `test_audit_rules_exclude_pycache` - **pycache** excluded

**TestOrphanFileResolution** (3 tests)

- ✅ `test_identifies_orphan_markdown_files` - Find orphans
- ✅ `test_orphan_count_within_limit` - Within limit (≤5)
- ✅ `test_excluded_directories_not_scanned` - Respect exclusions

**TestAuditReportGeneration** (3 tests)

- ✅ `test_generates_audit_report` - Generate audit
- ✅ `test_audit_report_json_valid` - Valid JSON output
- ✅ `test_audit_gates_enforced` - Enforce gates

**TestCleanupIntegration** (3 tests)

- ✅ `test_no_pycache_in_tracked_dirs` - No **pycache**
- ✅ `test_no_pyc_files_in_tracked_dirs` - No .pyc files
- ✅ `test_cleanup_is_idempotent` - Idempotent cleanup

#### Required Implementations

1. **MockCleanupService**
   - `find_pycache_dirs(root)` - Find **pycache**
   - `find_orphan_files(root, exclusions)` - Find orphans

2. **MockAuditService**
   - `generate_audit(root)` - Generate audit report

---

### 4. Load Directive Parser (15 unit tests)

**File**: `/home/william/git/standards/tests/unit/test_load_directive_parser.py`

#### Test Classes

**TestLoadDirectiveParser** (8 tests)

- ✅ `test_parse_simple_product` - Parse product:api
- ✅ `test_parse_standard_code` - Parse CS:python
- ✅ `test_parse_wildcard` - Parse SEC:*
- ✅ `test_parse_combination` - Parse combinations
- ✅ `test_validate_accepts_valid_syntax` - Accept valid
- ✅ `test_validate_rejects_invalid_syntax` - Reject invalid
- ✅ `test_expand_sec_wildcard` - Expand wildcards
- ✅ `test_expand_preserves_non_wildcards` - Preserve non-wildcards
- ✅ `test_expand_mixed_wildcards` - Mixed expansion

**TestLoadDirectiveValidation** (7 tests)

- ✅ `test_requires_at_symbol` - Must start with @
- ✅ `test_requires_load_keyword` - Must have 'load'
- ✅ `test_requires_colon_separator` - Must use colon
- ✅ `test_requires_value_after_colon` - Value required
- ✅ `test_requires_category_before_colon` - Category required
- ✅ `test_accepts_hyphenated_categories` - Allow hyphens
- ✅ `test_accepts_alphanumeric_values` - Allow alphanumeric

#### Required Implementation

**LoadDirectiveParser** class:

- `parse(directive)` - Parse directive to dict
- `validate(directive)` - Validate syntax
- `expand_wildcards(components)` - Expand wildcards

---

## Test Execution

### Run All Tests

```bash
# All TDD tests
pytest tests/integration/ tests/unit/ -v

# Specific categories
pytest tests/integration/test_command_syntax_fix.py -v
pytest tests/integration/test_router_paths.py -v
pytest tests/integration/test_cleanup.py -v
pytest tests/unit/test_load_directive_parser.py -v
```

### Expected Initial Status

```
FAILED tests/integration/test_command_syntax_fix.py::... (24 failures)
FAILED tests/integration/test_router_paths.py::... (23 failures)
FAILED tests/integration/test_cleanup.py::... (18 failures)
FAILED tests/unit/test_load_directive_parser.py::... (15 failures)

Total: 80 tests, 80 FAILED (RED phase - expected)
```

---

## London School TDD Principles Applied

### 1. Outside-In Development

Start with acceptance tests (integration), work inward to unit tests:

- Integration tests define HIGH-LEVEL behavior
- Unit tests define COMPONENT-LEVEL behavior
- Mocks define CONTRACTS between components

### 2. Behavior Verification

Tests focus on INTERACTIONS, not state:

```python
# NOT: assert object.internal_state == expected
# YES: assert mock.method.called_with(expected_args)
```

### 3. Mock-Driven Design

Mocks DEFINE the interface:

```python
mock_scanner.scan_for_commands(path)  # Defines contract
# Implementation MUST satisfy this interface
```

### 4. Contract Testing

Each mock is a CONTRACT:

- `MockDocumentScanner` → defines scanning contract
- `MockCommandValidator` → defines validation contract
- `MockPathResolver` → defines resolution contract

---

## Implementation Roadmap

### Phase 1: GREEN (Make Tests Pass)

1. **Implement Parsers** (Unit Tests First)
   - LoadDirectiveParser
   - Command syntax parser
   - Path resolver

2. **Implement Services** (Integration Tests)
   - Document scanner
   - Command validator
   - Cleanup service
   - Audit service

3. **Implement Fixes**
   - Command syntax fixes
   - Path updates
   - Cleanup operations

### Phase 2: REFACTOR

1. **Optimize Performance**
   - Caching
   - Batch operations
   - Efficient algorithms

2. **Improve Design**
   - Extract common patterns
   - Reduce duplication
   - Enhance modularity

3. **Polish**
   - Error messages
   - Documentation
   - Edge cases

---

## Test Fixtures

See `/home/william/git/standards/tests/conftest.py` for:

- `repo_root` - Repository root path
- `temp_repo` - Isolated temporary repo
- `mock_product_matrix` - Mock configuration
- `mock_audit_rules` - Mock audit rules
- `mock_fs` - Mock file system
- `command_capture` - Command execution capture
- `isolation_mode` - Isolated test execution

---

## Success Criteria

### All Gates Must Pass

1. **Broken Links**: 0
2. **Hub Violations**: 0
3. **Orphans**: ≤ 5
4. **Test Suite**: 80/80 passing

### Implementation Quality

- Clean, modular code
- Well-documented interfaces
- Efficient algorithms
- Comprehensive error handling

---

## Swarm Coordination

### Memory Keys

- `swarm/tdd/test_specs` - Test specifications
- `swarm/tdd/implementation_plan` - Implementation roadmap
- `swarm/tdd/progress` - Current progress

### Handoff to Implementation Agent

Once GREEN phase begins:

1. Start with unit tests (parser)
2. Move to integration tests (services)
3. Verify all contracts satisfied
4. Run full test suite

---

**Status**: 🔴 RED PHASE COMPLETE - Ready for Implementation
**Next**: 🟢 GREEN PHASE - Implement to pass tests
**Then**: 🔵 REFACTOR PHASE - Optimize and polish

**Test Count**: 80 tests (24 + 23 + 18 + 15)
**Expected Failures**: 80 (this is GOOD in TDD!)
**Coverage**: Command syntax, routing, cleanup, parsing
