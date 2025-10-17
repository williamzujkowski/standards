# Scripts Directory

This directory contains utility scripts for managing the standards repository.

## Skill Management

### skill-loader.py

The skill-loader CLI provides comprehensive skill discovery, loading, and management capabilities.

**Installation:**

```bash
# Make executable
chmod +x scripts/skill-loader.py

# Install dependencies
pip install pyyaml
```

**Usage:**

```bash
# Discover skills by keyword
python scripts/skill-loader.py discover --keyword testing

# Discover skills by category
python scripts/skill-loader.py discover --category security

# List all skills
python scripts/skill-loader.py list --category all

# List skills in JSON format
python scripts/skill-loader.py list --format json

# Get skill information
python scripts/skill-loader.py info python

# Load a single skill
python scripts/skill-loader.py load python --level 2

# Load multiple skills
python scripts/skill-loader.py load [python,typescript] --level 2

# Load skills for a product type
python scripts/skill-loader.py load product:api

# Get skill recommendations
python scripts/skill-loader.py recommend --product-type api

# Validate skill structure
python scripts/skill-loader.py validate python
```

**Features:**

- **Skill Discovery**: Search skills by keyword or category
- **Skill Loading**: Load skills individually or in groups at different levels
- **Recommendations**: Get skill recommendations based on product type
- **Legacy Support**: Translate legacy @load patterns to new Skills format
- **Validation**: Validate skill structure and completeness
- **JSON Output**: Machine-readable output for automation

## Audit and Validation Scripts

- 📄 [Auto Fix Links](./auto-fix-links.py) - Automatically fix broken links
- 📄 [Calculate Compliance Score](./calculate_compliance_score.py) - Calculate compliance scores
- 📄 [Generate Audit Reports](./generate-audit-reports.py) - Generate audit reports
- 📄 [Generate Readmes](./generate-readmes.py) - Generate README files
- 📄 [Generate Standards Inventory](./generate-standards-inventory.py) - Generate standards inventory
- 📄 [Generate Digest](./generate_digest.py) - Generate documentation digest
- 📄 [Generate Reference](./generate_reference.py) - Generate reference documentation
- 📄 [Generate Standards Index](./generate_standards_index.py) - Generate standards index
- 📄 [Generate Summary](./generate_summary.py) - Generate summary reports
- 📄 [Inject Unified Crossref](./inject-unified-crossref.py) - Inject cross-references
- 📄 [Validate Markdown Links](./validate_markdown_links.py) - Validate markdown links
- 📄 [Validate Standards Consistency](./validate_standards_consistency.py) - Validate consistency
- 📄 [Validate Standards Graph](./validate_standards_graph.py) - Validate standards graph

## Shell Scripts

- 📄 [Check Whitespace](./check_whitespace.sh) - Check for whitespace issues
- 📄 [Fix Trailing Whitespace](./fix_trailing_whitespace.sh) - Fix trailing whitespace
- 📄 [Generate Badges](./generate-badges.sh) - Generate status badges
- 📄 [Nist Pre Commit](./nist-pre-commit.sh) - NIST pre-commit hooks
- 📄 [Setup Development](./setup-development.sh) - Setup development environment
- 📄 [Setup Nist Hooks](./setup-nist-hooks.sh) - Setup NIST hooks
- 📄 [Setup Project](./setup-project.sh) - Setup project
- 📄 [Test Precommit Hooks](./test-precommit-hooks.sh) - Test pre-commit hooks
- 📄 [Validate Mcp Integration](./validate_mcp_integration.sh) - Validate MCP integration

## Testing

Run tests for all scripts:

```bash
# Run all script tests
pytest tests/scripts/ -v

# Run specific test file
pytest tests/scripts/test_skill_loader.py -v

# Run with coverage
pytest tests/scripts/ --cov=scripts --cov-report=html
```

## Development

### Adding New Scripts

1. Create the script in `scripts/`
2. Add tests in `tests/scripts/test_<script_name>.py`
3. Update this README with usage documentation
4. Add script to CI pipeline if needed

### Style Guide

- Use Python 3.8+ features
- Follow PEP 8 style guidelines
- Include docstrings for all functions
- Add type hints where appropriate
- Handle errors gracefully with clear messages

### Dependencies

Common dependencies used across scripts:

- `pyyaml`: YAML parsing
- `pytest`: Testing framework
- `pathlib`: Path manipulation
- Standard library modules: `argparse`, `json`, `re`, `sys`

Install all dependencies:

```bash
pip install pyyaml pytest pytest-cov
```

## Integration with CI/CD

Scripts are integrated into GitHub Actions workflows:

- `.github/workflows/lint-and-validate.yml`: Runs audit and validation
- `.github/workflows/test.yml`: Runs script tests

See workflow files for configuration details.

## Troubleshooting

### Common Issues

**Script not executable:**

```bash
chmod +x scripts/skill-loader.py
```

**Import errors:**

```bash
# Install dependencies
pip install pyyaml

# Or use virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Tests failing:**

```bash
# Run tests with verbose output
pytest tests/scripts/ -v --tb=short

# Run specific test
pytest tests/scripts/test_skill_loader.py::TestSkillLoaderCLI::test_cli_discover -v
```

## Support

For issues or questions about scripts:

1. Check this README
2. Review script source code and docstrings
3. Check test files for usage examples
4. Open an issue on GitHub

## Related Documentation

- [Skills README](../skills/README.md)
- [CLAUDE.md](../CLAUDE.md)

---

← Back to [Main Repository](../README.md)
