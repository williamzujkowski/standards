# Validation Test Suite

Comprehensive validation framework for the standards repository ensuring documentation accuracy, example functionality, skills compliance, and integration workflow quality.

## Overview

This test suite implements a quality gate system with strict pass/fail criteria:

- **Documentation Accuracy**: 100% (all docs must be accurate)
- **Example Functionality**: 100% (all examples must work)
- **Skills Compliance**: 100% (all skills must comply)
- **Agent Specifications**: 95% (agent specs must be valid)
- **Integration Workflows**: 90% (workflows must pass)

## Test Modules

### test_documentation.py

Tests documentation structure, content quality, accuracy, and completeness.

**Key Tests:**

- Required documentation files exist
- Markdown files have proper structure
- No broken relative links
- Hub READMEs have AUTO-LINKS sections
- No placeholder content (TODO, FIXME, etc.)
- Code blocks properly fenced
- Consistent heading style
- File paths in documentation are valid
- Command examples have valid syntax

**Quality Gates:**

- `test_documentation_accuracy_gate`: 100% accuracy required
- `test_link_validity_gate`: 100% link validity required

### test_examples.py

Tests that all code examples have valid syntax and work correctly.

**Key Tests:**

- Python examples compile successfully
- Bash examples have valid syntax
- YAML examples parse correctly
- JSON examples are well-formed
- NIST quickstart templates exist
- Scripts have proper shebangs
- GitHub workflows are valid

**Quality Gates:**

- `test_example_functionality_gate`: 100% functionality required

### test_skills.py

Tests skills structure, compliance, and integration.

**Key Tests:**

- Skill files have required sections
- Skill directories have expected structure
- Skills have metadata and examples
- Skills reference relevant standards
- File size limits enforced
- Naming conventions followed
- Unique skill identifiers
- Dependencies exist

**Quality Gates:**

- `test_skills_compliance_gate`: 100% compliance required
- `test_all_skills_valid`: All skills must be valid

### test_product_matrix.py

Tests product matrix configuration and consistency.

**Key Tests:**

- Matrix has version and products
- Products have required fields
- Wildcard expansions defined
- Standard codes consistent format
- NIST auto-inclusion when SEC present
- Language/framework mappings valid
- Common products defined
- No circular dependencies
- Descriptions present

**Quality Gates:**

- `test_matrix_completeness`: Matrix must be complete

## Running Tests

### Run All Tests

```bash
pytest tests/validation/ -v
```

### Run Specific Module

```bash
pytest tests/validation/test_documentation.py -v
pytest tests/validation/test_examples.py -v
pytest tests/validation/test_skills.py -v
pytest tests/validation/test_product_matrix.py -v
```

### Run Quality Gate Tests Only

```bash
pytest tests/validation/ -m quality_gate -v
```

### Run with Coverage

```bash
pytest tests/validation/ --cov=. --cov-report=html
```

### Run in Parallel

```bash
pytest tests/validation/ -n auto
```

### Skip Slow Tests

```bash
pytest tests/validation/ -m "not slow"
```

## CI/CD Integration

The validation suite runs automatically in GitHub Actions via `.github/workflows/validation.yml`:

**Workflow Jobs:**

1. `quality-gates`: Initial gate checks
2. `documentation-validation`: Run documentation tests
3. `example-validation`: Run example tests
4. `skills-validation`: Run skills tests
5. `product-matrix-validation`: Run product matrix tests
6. `integration-validation`: Run full validation suite
7. `quality-gate-summary`: Aggregate results and enforce gates

**Artifacts Generated:**

- HTML coverage reports
- Validation summary JSON
- Test result HTML reports
- Coverage XML for analysis

## Quality Gate Enforcement

Quality gates are enforced at multiple levels:

1. **Individual Test Level**: Tests marked with `@pytest.mark.quality_gate`
2. **Module Level**: Each test module has quality gate tests
3. **CI Level**: Workflow fails if any gate fails
4. **Integration Level**: Full suite must meet coverage targets

## Configuration

### pytest.ini (in pyproject.toml)

```toml
[tool.pytest.ini_options]
markers = [
    "quality_gate: marks tests as quality gate tests",
    "slow: marks tests as slow",
]
testpaths = ["tests"]
addopts = "-ra -q --strict-markers"
```

### Fixtures (conftest.py)

Common fixtures available to all tests:

- `repo_root`: Repository root directory
- `docs_dir`: Documentation directory
- `skills_dir`: Skills directory
- `examples_dir`: Examples directory
- `config_dir`: Configuration directory
- `product_matrix`: Loaded product matrix
- `all_markdown_files`: All markdown files
- `all_skill_files`: All SKILL.md files
- `quality_gates`: Quality gate definitions
- Helper functions for validation

## Test Results Storage

Test results are stored in hive memory for coordination:

```bash
npx claude-flow@alpha memory store \
  --key "hive/tester/validation_results" \
  --value "$(pytest tests/validation/ --json-report)"
```

## Coverage Targets

- **Code Coverage**: 80% minimum
- **Documentation Coverage**: 100%
- **Example Coverage**: 100%
- **Skills Coverage**: 100%

## Excluded Directories

The following directories are excluded from validation:

- `.git`, `.github`, `.vscode`
- `.claude`, `.claude-flow`, `.hive-mind`, `.swarm`
- `subagents`, `memory`, `prompts`
- `reports/generated`
- `node_modules`, `__pycache__`

## Contributing

When adding new tests:

1. Follow existing test structure and naming
2. Use descriptive test names
3. Add quality gate tests for critical functionality
4. Update this README with new test descriptions
5. Ensure tests are fast (< 100ms for unit tests)
6. Use fixtures for common setup
7. Mark slow tests with `@pytest.mark.slow`

## Troubleshooting

### Tests Fail Locally But Pass in CI

- Check Python version (CI uses 3.11)
- Ensure all dependencies installed
- Check file permissions on scripts
- Verify no local-only files referenced

### Quality Gates Fail

- Review quality gate definitions in `conftest.py`
- Check if gates need adjustment for repo size
- Ensure all required files exist
- Verify no placeholder content

### Slow Test Execution

- Run with `-n auto` for parallel execution
- Skip slow tests with `-m "not slow"`
- Check for inefficient file operations
- Use caching where appropriate

## Maintenance

- Review and update quality gates quarterly
- Add new tests for new repository features
- Refactor tests when they become slow
- Keep fixture definitions current
- Update CI workflow as needed

## Support

For issues with validation tests:

1. Check test output for specific failures
2. Review relevant test module documentation
3. Check CI workflow logs
4. Contact repository maintainers
