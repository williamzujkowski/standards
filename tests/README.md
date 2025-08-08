# Knowledge Management Test Suite

This directory contains comprehensive tests to validate the integrity and compliance of our knowledge management system according to `KNOWLEDGE_MANAGEMENT_STANDARDS.md`.

## 🧪 Test Coverage

### 1. Cross-Reference Validation (`validate_cross_references.py`)

Comprehensive Python test suite that validates:

- **Manifest Completeness**: All standards have entries in MANIFEST.yaml
- **CLAUDE.md Routing**: All standard codes are covered in routing patterns
- **Bidirectional Links**: Cross-references work in both directions
- **Metadata Consistency**: All files have required version/status headers
- **Required Sections**: Standards follow the required structure
- **Version Information**: Semantic versioning compliance
- **Link Validity**: All cross-references point to existing files
- **Index Coverage**: STANDARDS_INDEX.md includes all standards
- **Graph Relationships**: STANDARDS_GRAPH.md defines all relationship types
- **README References**: Major standards are referenced in README.md

### 2. Knowledge Management Validation (`validate_knowledge_management.sh`)

Bash script that performs:

- **File Structure Tests**: Required files exist
- **Content Validation**: Headers and metadata present
- **YAML Validation**: MANIFEST.yaml is valid
- **Link Integrity**: No broken markdown links
- **Standards Compliance**: Proper use of tags and checklists
- **Token Optimization**: Checks for token-related metadata
- **Cross-Reference Metrics**: Counts and validates references

### 3. Token Efficiency Analysis (`validate_token_efficiency.py`)

Analyzes documentation for token efficiency:

- **Token Estimation**: Calculates token usage per section
- **Efficiency Scoring**: Rates documents on token efficiency
- **Recommendations**: Suggests optimizations
- **MANIFEST Alignment**: Validates token estimates match reality
- **Progressive Disclosure**: Checks for proper information layering

## 🚀 Running the Tests

### Run All Tests
```bash
cd tests
./validate_knowledge_management.sh
```

### Run Individual Test Suites
```bash
# Cross-reference validation
python3 validate_cross_references.py

# Token efficiency analysis
python3 validate_token_efficiency.py

# Bash validation suite
bash validate_knowledge_management.sh
```

## 📊 Test Output

### Success Output
```
✓ PASS - Manifest Completeness
  All standards present in MANIFEST.yaml
✓ PASS - Claude Routing Coverage
  All standard codes covered in CLAUDE.md
...
SUMMARY: 10 passed, 0 failed
```

### Failure Output
```
✗ FAIL - Bidirectional Links
  Found 3 unidirectional links
  Details:
    - CODING_STANDARDS.md -> TESTING_STANDARDS.md
    - SECURITY_STANDARDS.md -> CLAUDE.md
    ...
```

## 🔧 Requirements

- Python 3.6+
- PyYAML (`pip install pyyaml`)
- Bash 4.0+
- Optional: yamllint for YAML validation

## 🎯 Test Philosophy

These tests implement the validation requirements from `KNOWLEDGE_MANAGEMENT_STANDARDS.md`:

1. **Automated Validation**: All tests can run in CI/CD
2. **Comprehensive Coverage**: Tests cover structure, content, and relationships
3. **Token Efficiency**: Validates progressive disclosure and optimization
4. **Clear Reporting**: Provides actionable feedback on failures
5. **Fast Execution**: Designed for quick feedback loops

## 🛠️ Adding New Tests

To add new validation tests:

1. **Python Tests**: Add methods to `StandardsValidator` class
2. **Bash Tests**: Add `run_test` calls in the shell script
3. **Document**: Update this README with new test coverage

Example test method:
```python
def test_new_validation(self) -> ValidationResult:
    """Test: Description of what this validates"""
    # Implementation
    if issues_found:
        return ValidationResult(False, "Error message", details_list)
    return ValidationResult(True, "Success message")
```

## 📈 Continuous Improvement

These tests should evolve as the standards grow:

- Add tests for new standard requirements
- Update token estimates as documents change
- Enhance cross-reference validation patterns
- Improve performance for large repositories

## 🐛 Known Limitations

- Token estimation is approximate (0.75 tokens per word)
- Bidirectional link checking may miss complex references
- Section detection uses simple header patterns

For issues or improvements, please update the tests according to `CREATING_STANDARDS_GUIDE.md`.
