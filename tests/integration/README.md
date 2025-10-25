# Router Validation Integration Tests

Comprehensive integration tests for the Standards Router system.

## Purpose

These tests ensure that no routing paths break when files are moved or updated.
They validate the entire routing infrastructure:

1. **Product Matrix Router** (`config/product-matrix.yaml`)
2. **Skill Loader** (`scripts/skill-loader.py`)
3. **Audit Rules** (`config/audit-rules.yaml`)
4. **Hub Linking** (`scripts/ensure-hub-links.py`)

## Test Coverage

### Product Matrix Router Tests

- ✅ Product definitions exist and are valid
- ✅ All products have descriptions and standards
- ✅ Wildcard expansions are properly defined
- ✅ Language and framework mappings are consistent
- ✅ Stack presets reference valid product types

### Skill Loader Tests

- ✅ Legacy mappings align with product matrix
- ✅ Referenced skill paths exist
- ✅ Wildcard expansions match across systems
- ✅ Product mappings are complete

### Audit Rules Tests

- ✅ Hub requirements have valid patterns
- ✅ Hub files exist or can be created
- ✅ Exclusion patterns are valid
- ✅ Audit limits are reasonable

### Hub Linking Tests

- ✅ Hub linking script exists and is executable
- ✅ Generated hub files contain valid AUTO-LINKS sections
- ✅ Hub markers are properly formatted

### End-to-End Routing Tests

- ✅ Complete product:api routing flow
- ✅ SEC:* wildcard expansion with NIST auto-inclusion
- ✅ No broken internal route references
- ✅ All critical routing files exist

### Path Resolution Tests

- ✅ Standard documents exist
- ✅ Skills directory structure is valid
- ✅ Config directory is complete

## Running Tests

```bash
# Run all integration tests
pytest tests/integration/test_router_validation.py -v

# Run specific test class
pytest tests/integration/test_router_validation.py::TestProductMatrixRouter -v

# Run with detailed output
pytest tests/integration/test_router_validation.py -v --tb=long

# Generate coverage report
pytest tests/integration/test_router_validation.py --cov=scripts --cov=config

# Generate HTML report
pytest tests/integration/test_router_validation.py --html=reports/test-report.html
```

## Test Organization

```
tests/integration/
├── README.md                        # This file
├── conftest.py                      # Shared fixtures
├── test_router_validation.py        # Main test suite
└── fixtures/                        # Test fixtures (future)
    ├── sample-product-matrix.yaml
    └── sample-legacy-mappings.yaml
```

## Expected Behavior

### Passing Tests

All tests should pass when:

- All routing configuration files exist
- File paths are correctly resolved
- Hub requirements are satisfied
- No broken internal references exist

### Skipped Tests

Some tests may be skipped when:

- Skills system is incomplete (directories not yet created)
- Optional features are not implemented
- Test fixtures are missing

### Failed Tests

Tests fail when:

- Configuration files are missing
- Internal routes are broken
- Hub requirements are violated
- Path resolution fails

## Continuous Integration

These tests are integrated into the CI/CD pipeline:

```yaml
# .github/workflows/lint-and-validate.yml
- name: Run Router Validation Tests
  run: pytest tests/integration/test_router_validation.py -v
```

## Troubleshooting

### Common Issues

**Issue**: Tests fail with "Skills directory not found"
**Solution**: Create the skills directory structure:

```bash
mkdir -p skills/{coding-standards,testing,security,devops}
```

**Issue**: Hub files not found
**Solution**: Run the hub linking script:

```bash
python3 scripts/ensure-hub-links.py
```

**Issue**: Product matrix and legacy mappings out of sync
**Solution**: Update both files to align product definitions:

- `config/product-matrix.yaml`
- `skills/legacy-bridge/resources/legacy-mappings.yaml`

## Maintenance

### Adding New Tests

1. Add test methods to appropriate test class
2. Use descriptive test names starting with `test_`
3. Include docstrings explaining test purpose
4. Update this README with new coverage

### Updating Fixtures

When routing configuration changes:

1. Update test assertions to match new structure
2. Add new test cases for new features
3. Deprecate old tests if routes are removed
4. Document breaking changes

## Related Documentation

- [Product Matrix Documentation](/home/william/git/standards/config/product-matrix.yaml)
- [Skill Loader Guide](/home/william/git/standards/scripts/skill-loader.py)
- [Audit Rules Reference](/home/william/git/standards/config/audit-rules.yaml)
- [Hub Linking Documentation](/home/william/git/standards/scripts/ensure-hub-links.py)

## Contributing

When modifying routing logic:

1. Update tests FIRST (TDD approach)
2. Run tests locally before committing
3. Ensure all tests pass
4. Add regression tests for bug fixes

## License

Part of the Standards Repository
Author: REVIEWER Agent
Created: 2025-10-24
