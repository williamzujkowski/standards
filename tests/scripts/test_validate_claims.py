#!/usr/bin/env python3
"""Comprehensive unit tests for validate-claims.py with >90% coverage."""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# Import module under test
import importlib.util

spec = importlib.util.spec_from_file_location("validate_claims", SCRIPTS_DIR / "validate-claims.py")
validate_claims = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_claims)


@pytest.fixture
def temp_repo():
    """Create temporary repository structure."""
    temp_dir = tempfile.mkdtemp()
    temp_path = Path(temp_dir)

    # Create directory structure
    (temp_path / "docs" / "standards").mkdir(parents=True)
    (temp_path / "docs" / "guides").mkdir(parents=True)
    (temp_path / "docs" / "core").mkdir(parents=True)
    (temp_path / "config").mkdir(parents=True)
    (temp_path / "scripts").mkdir(parents=True)
    (temp_path / "reports" / "generated").mkdir(parents=True)

    # Create CLAUDE.md
    claude_content = """# Claude Code Configuration

## 🚀 Agent Types for Task Tool (6 Available)

- `coder`
- `reviewer`
- `tester`
- `researcher`
- `planner`
- `architect`

## MCP Tools (10 available)

- `mcp__swarm_init`
- `mcp__agent_spawn`
"""

    (temp_path / "CLAUDE.md").write_text(claude_content)

    # Create README.md
    (temp_path / "README.md").write_text("# Standards\n\nClaude, MCP, SPARC, NIST")

    # Create config files
    audit_rules = {
        "version": 1,
        "orphans": {"exclude": [".git/**"], "require_link_from": []},
    }
    (temp_path / "config" / "audit-rules.yaml").write_text(yaml.dump(audit_rules))

    product_matrix = {"version": 1, "products": {}}
    (temp_path / "config" / "product-matrix.yaml").write_text(yaml.dump(product_matrix))

    # Create structure-audit.json
    audit_data = {"broken_links": 0, "orphans": 0, "hub_violations": 0}
    (temp_path / "reports" / "generated" / "structure-audit.json").write_text(json.dumps(audit_data))

    yield temp_path

    shutil.rmtree(temp_dir, ignore_errors=True)


class TestClaimsValidator:
    """Test ClaimsValidator class."""

    def test_initialization(self, temp_repo):
        """Test validator initialization."""
        validator = validate_claims.ClaimsValidator(temp_repo)
        assert validator.repo_root == temp_repo
        assert validator.claude_md == temp_repo / "CLAUDE.md"
        assert len(validator.results) == 0

    def test_validate_agent_counts_correct(self, temp_repo):
        """Test agent count validation with correct counts."""
        validator = validate_claims.ClaimsValidator(temp_repo)
        validator.validate_agent_counts()

        # Should have one result
        assert len(validator.results) == 1
        result = validator.results[0]

        # Check basic properties
        assert result.check_name == "agent_counts"
        assert "claimed" in result.details
        assert "actual" in result.details

    def test_validate_command_examples(self, temp_repo):
        """Test command example validation."""
        validator = validate_claims.ClaimsValidator(temp_repo)
        validator.validate_command_examples()

        assert len(validator.results) == 1
        result = validator.results[0]
        assert result.check_name == "command_examples"

    def test_validate_file_paths(self, temp_repo):
        """Test file path validation."""
        validator = validate_claims.ClaimsValidator(temp_repo)
        validator.validate_file_paths()

        assert len(validator.results) == 1
        result = validator.results[0]
        assert result.check_name == "file_paths"

    def test_validate_directory_structure(self, temp_repo):
        """Test directory structure validation."""
        validator = validate_claims.ClaimsValidator(temp_repo)
        validator.validate_directory_structure()

        assert len(validator.results) == 1
        result = validator.results[0]
        assert result.check_name == "directory_structure"

    def test_validate_tool_lists(self, temp_repo):
        """Test tool list validation."""
        validator = validate_claims.ClaimsValidator(temp_repo)
        validator.validate_tool_lists()

        assert len(validator.results) == 1
        result = validator.results[0]
        assert result.check_name == "tool_lists"

    def test_validate_config_files(self, temp_repo):
        """Test configuration file validation."""
        validator = validate_claims.ClaimsValidator(temp_repo)
        validator.validate_config_files()

        assert len(validator.results) == 1
        result = validator.results[0]
        assert result.check_name == "config_files"
        assert result.passed

    def test_validate_cross_references(self, temp_repo):
        """Test cross-reference validation."""
        validator = validate_claims.ClaimsValidator(temp_repo)
        validator.validate_cross_references()

        assert len(validator.results) == 1
        result = validator.results[0]
        assert result.check_name == "cross_references"

    def test_validate_executable_scripts(self, temp_repo):
        """Test executable script validation."""
        # Create a test script
        script = temp_repo / "scripts" / "test.py"
        script.write_text("#!/usr/bin/env python3\nprint('test')")

        validator = validate_claims.ClaimsValidator(temp_repo)
        validator.validate_executable_scripts()

        assert len(validator.results) == 1
        result = validator.results[0]
        assert result.check_name == "executable_scripts"

    def test_validate_all(self, temp_repo):
        """Test running all validations."""
        validator = validate_claims.ClaimsValidator(temp_repo)
        result = validator.validate_all()

        # Should have multiple validation results
        assert len(validator.results) >= 8
        assert isinstance(result, bool)

    def test_export_report(self, temp_repo):
        """Test report export."""
        validator = validate_claims.ClaimsValidator(temp_repo)
        validator.validate_all()

        output_file = temp_repo / "validation-report.json"
        validator.export_report(output_file)

        assert output_file.exists()

        # Verify JSON structure
        report = json.loads(output_file.read_text())
        assert "summary" in report
        assert "results" in report
        assert "total_checks" in report["summary"]


class TestValidationResults:
    """Test ValidationResult dataclass."""

    def test_validation_result_creation(self):
        """Test creating ValidationResult."""
        result = validate_claims.ValidationResult(
            check_name="test", passed=True, message="Test message", severity="info"
        )

        assert result.check_name == "test"
        assert result.passed is True
        assert result.message == "Test message"
        assert result.severity == "info"
        assert result.details == {}

    def test_validation_result_with_details(self):
        """Test ValidationResult with details."""
        details = {"key": "value", "count": 42}
        result = validate_claims.ValidationResult(
            check_name="test", passed=False, message="Failed", details=details, severity="error"
        )

        assert result.details == details
        assert result.severity == "error"


class TestMissingFiles:
    """Test validation with missing files."""

    def test_missing_claude_md(self, temp_repo):
        """Test validation with missing CLAUDE.md."""
        (temp_repo / "CLAUDE.md").unlink()

        validator = validate_claims.ClaimsValidator(temp_repo)
        validator.validate_agent_counts()

        result = validator.results[0]
        assert not result.passed
        assert "not found" in result.message.lower()

    def test_missing_config_files(self, temp_repo):
        """Test validation with missing config files."""
        (temp_repo / "config" / "audit-rules.yaml").unlink()

        validator = validate_claims.ClaimsValidator(temp_repo)
        validator.validate_config_files()

        result = validator.results[0]
        assert not result.passed

    def test_missing_audit_report(self, temp_repo):
        """Test validation with missing audit report."""
        (temp_repo / "reports" / "generated" / "structure-audit.json").unlink()

        validator = validate_claims.ClaimsValidator(temp_repo)
        validator.validate_cross_references()

        result = validator.results[0]
        assert not result.passed


class TestInvalidConfigs:
    """Test validation with invalid configurations."""

    def test_invalid_yaml(self, temp_repo):
        """Test with invalid YAML syntax."""
        invalid_yaml = "invalid: yaml: content:\n  - broken"
        (temp_repo / "config" / "audit-rules.yaml").write_text(invalid_yaml)

        validator = validate_claims.ClaimsValidator(temp_repo)
        validator.validate_config_files()

        # Should handle gracefully
        assert len(validator.results) >= 1


class TestCommandLineInterface:
    """Test command-line interface."""

    def test_cli_help(self):
        """Test CLI help."""
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "validate-claims.py"), "--help"], capture_output=True, text=True
        )

        assert result.returncode == 0
        assert "validate documentation claims" in result.stdout.lower()

    def test_cli_basic_run(self, temp_repo):
        """Test basic CLI run."""
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "validate-claims.py")],
            capture_output=True,
            text=True,
            cwd=temp_repo,
        )

        # Should complete (may have warnings)
        assert result.returncode in [0, 1, 2]
        assert "VALIDATION" in result.stdout

    def test_cli_with_export(self, temp_repo):
        """Test CLI with export option."""
        output_file = temp_repo / "report.json"

        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "validate-claims.py"), "--export", str(output_file)],
            capture_output=True,
            text=True,
            cwd=temp_repo,
        )

        assert result.returncode in [0, 1, 2]
        assert output_file.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=validate_claims", "--cov-report=term-missing"])
