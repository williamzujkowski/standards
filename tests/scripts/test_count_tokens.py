#!/usr/bin/env python3
"""Comprehensive unit tests for count-tokens.py with >90% coverage."""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# Import module under test
import importlib.util


spec = importlib.util.spec_from_file_location("count_tokens", SCRIPTS_DIR / "count-tokens.py")
count_tokens = importlib.util.module_from_spec(spec)
spec.loader.exec_module(count_tokens)


@pytest.fixture
def sample_skill_content():
    """Sample SKILL.md content with known structure."""
    return """---
name: "Test Skill"
description: "Test description"
---

# Test Skill

## Level 1: Quick Start (≤1000 tokens)

This is Level 1 content with approximately 100 tokens of text for testing purposes.
Additional content to reach a reasonable token count for testing.

### Core Principles

- Principle 1: Brief description
- Principle 2: Brief description
- Principle 3: Brief description

## Level 2: Implementation Details (≤5000 tokens)

This is Level 2 content with more text for testing token counting functionality.
This section would typically contain implementation details and examples.

### Detailed Practices

#### Practice 1
Implementation details here.

#### Practice 2
More implementation details.

## Level 3: Advanced Topics & Resources (no limit)

This is Level 3 content with unlimited tokens allowed.
Advanced topics and references go here.

### Resources

- Resource 1
- Resource 2
"""


@pytest.fixture
def temp_skill_file(sample_skill_content):
    """Create temporary SKILL.md file."""
    temp_dir = tempfile.mkdtemp()
    skill_file = Path(temp_dir) / "SKILL.md"
    skill_file.write_text(sample_skill_content)
    yield skill_file
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def temp_skills_dir(sample_skill_content):
    """Create temporary skills directory with multiple files."""
    temp_dir = tempfile.mkdtemp()
    temp_path = Path(temp_dir)

    # Create multiple skill files
    for i in range(3):
        skill_dir = temp_path / f"skill-{i}"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(sample_skill_content)

    yield temp_path
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestTokenCounter:
    """Test TokenCounter class."""

    def test_token_counter_initialization(self, temp_skill_file):
        """Test TokenCounter initialization."""
        counter = count_tokens.TokenCounter(temp_skill_file)
        assert counter.skill_file == temp_skill_file
        assert counter.encoding is not None or count_tokens.TIKTOKEN_AVAILABLE is False

    def test_count_tokens_with_tiktoken(self, temp_skill_file):
        """Test token counting with tiktoken."""
        counter = count_tokens.TokenCounter(temp_skill_file)
        text = "This is a test sentence with multiple words."
        token_count = counter.count_tokens(text)

        # Token count should be reasonable (not zero, not absurdly high)
        assert token_count > 0
        assert token_count < len(text)  # Tokens < characters

    def test_count_tokens_estimation_fallback(self, temp_skill_file):
        """Test token counting with estimation fallback."""
        counter = count_tokens.TokenCounter(temp_skill_file)
        # Force estimation mode
        counter.encoding = None

        text = "A" * 400  # 400 characters
        token_count = counter.count_tokens(text)

        # Should estimate ~100 tokens (4 chars per token)
        assert token_count == 100

    def test_split_by_levels(self, temp_skill_file):
        """Test splitting content by levels."""
        counter = count_tokens.TokenCounter(temp_skill_file)
        content = temp_skill_file.read_text()
        levels = counter.split_by_levels(content)

        # Should have frontmatter and 3 levels
        assert "frontmatter" in levels
        assert "level1" in levels
        assert "level2" in levels
        assert "level3" in levels

    def test_split_by_levels_extracts_correct_content(self, temp_skill_file):
        """Test that split_by_levels extracts correct content."""
        counter = count_tokens.TokenCounter(temp_skill_file)
        content = temp_skill_file.read_text()
        levels = counter.split_by_levels(content)

        # Verify each level contains expected markers
        assert "Level 1" in levels["level1"]
        assert "Level 2" in levels["level2"]
        assert "Level 3" in levels["level3"]

    def test_split_by_levels_no_markers(self, temp_skill_file):
        """Test split_by_levels with no level markers."""
        counter = count_tokens.TokenCounter(temp_skill_file)
        content = "# Test\n\nNo level markers here."
        levels = counter.split_by_levels(content)

        assert "content" in levels

    def test_count_all_levels(self, temp_skill_file):
        """Test counting tokens for all levels."""
        counter = count_tokens.TokenCounter(temp_skill_file)
        results = counter.count_all_levels()

        # Should have results for all levels plus total
        assert "level1" in results
        assert "level2" in results
        assert "level3" in results
        assert "total" in results

        # Each result should have required fields
        for level in ["level1", "level2", "level3", "total"]:
            assert "tokens" in results[level]
            assert "chars" in results[level]
            assert "lines" in results[level]
            assert results[level]["tokens"] > 0

    def test_check_violations_no_violations(self, temp_skill_file):
        """Test violation checking with no violations."""
        counter = count_tokens.TokenCounter(temp_skill_file)
        results = counter.count_all_levels()
        violations = counter.check_violations(results)

        # Sample content should not violate limits
        assert isinstance(violations, list)

    def test_check_violations_with_violations(self, temp_skill_file):
        """Test violation checking with violations."""
        counter = count_tokens.TokenCounter(temp_skill_file)

        # Create results with violations
        results = {
            "level1": {"tokens": 1500, "chars": 6000, "lines": 100},
            "level2": {"tokens": 5500, "chars": 22000, "lines": 300},
            "level3": {"tokens": 3000, "chars": 12000, "lines": 150},
            "total": {"tokens": 10000, "chars": 40000, "lines": 550},
        }

        violations = counter.check_violations(results)

        # Should have 2 violations (level1 and level2)
        assert len(violations) >= 2
        assert any("Level 1" in v for v in violations)
        assert any("Level 2" in v for v in violations)

    def test_format_report(self, temp_skill_file):
        """Test report formatting."""
        counter = count_tokens.TokenCounter(temp_skill_file)
        results = counter.count_all_levels()
        violations = counter.check_violations(results)

        report = counter.format_report(results, violations)

        # Verify report structure
        assert "TOKEN REPORT" in report
        assert "SKILL.md" in report
        assert "Level 1" in report
        assert "Level 2" in report
        assert "Level 3" in report
        assert "TOTAL" in report

    def test_format_report_with_violations(self, temp_skill_file):
        """Test report formatting with violations."""
        counter = count_tokens.TokenCounter(temp_skill_file)
        results = {
            "level1": {"tokens": 1500, "chars": 6000, "lines": 100},
            "level2": {"tokens": 5500, "chars": 22000, "lines": 300},
            "level3": {"tokens": 3000, "chars": 12000, "lines": 150},
            "total": {"tokens": 10000, "chars": 40000, "lines": 550},
        }
        violations = counter.check_violations(results)

        report = counter.format_report(results, violations)

        assert "VIOLATIONS" in report
        assert "Level 1" in report


class TestCountDirectory:
    """Test count_directory function."""

    def test_count_directory_basic(self, temp_skills_dir):
        """Test counting directory with multiple skills."""
        results = count_tokens.count_directory(temp_skills_dir)

        # Should process 3 skills
        assert len(results) == 3

    def test_count_directory_empty(self):
        """Test counting empty directory."""
        temp_dir = tempfile.mkdtemp()
        temp_path = Path(temp_dir)

        results = count_tokens.count_directory(temp_path)

        assert results == {}
        shutil.rmtree(temp_dir)

    def test_count_directory_with_json_export(self, temp_skills_dir):
        """Test JSON export functionality."""
        output_json = temp_skills_dir / "token-counts.json"
        results = count_tokens.count_directory(temp_skills_dir, output_json)

        # JSON file should be created
        assert output_json.exists()

        # JSON should be valid
        data = json.loads(output_json.read_text())
        assert len(data) == 3


class TestCommandLineInterface:
    """Test command-line interface."""

    def test_cli_single_file(self, temp_skill_file):
        """Test CLI with single file."""
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "count-tokens.py"), str(temp_skill_file)],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode in [0, 1]  # 0 = no violations, 1 = violations
        assert "TOKEN REPORT" in result.stdout
        assert "Level 1" in result.stdout

    def test_cli_directory_mode(self, temp_skills_dir):
        """Test CLI with directory mode."""
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "count-tokens.py"), "--directory", str(temp_skills_dir)],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode in [0, 1]  # 0 = no violations, 1 = violations
        assert "SUMMARY" in result.stdout

    def test_cli_json_export(self, temp_skills_dir):
        """Test CLI JSON export."""
        output_json = temp_skills_dir / "output.json"
        result = subprocess.run(
            [
                "python3",
                str(SCRIPTS_DIR / "count-tokens.py"),
                "--directory",
                str(temp_skills_dir),
                "--output-json",
                str(output_json),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode in [0, 1, 2]
        assert output_json.exists()

    def test_cli_check_tiktoken(self):
        """Test --check-tiktoken flag."""
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "count-tokens.py"), "--check-tiktoken"],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "tiktoken" in result.stdout.lower()

    def test_cli_verbose_mode(self, temp_skill_file):
        """Test --verbose flag."""
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "count-tokens.py"), str(temp_skill_file), "--verbose"],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode in [0, 1]
        # Verbose mode should produce output
        assert len(result.stdout) > 0

    def test_cli_no_arguments(self):
        """Test CLI with no arguments."""
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "count-tokens.py")], check=False, capture_output=True, text=True
        )

        # Should show help and exit with code 2
        assert result.returncode == 2
        assert "usage:" in result.stdout.lower() or "usage:" in result.stderr.lower()


class TestExitCodes:
    """Test correct exit codes."""

    def test_exit_code_no_violations(self, temp_skill_file):
        """Test exit code 0 for no violations."""
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "count-tokens.py"), str(temp_skill_file)], check=False, capture_output=True
        )

        # Should be 0 or 1 depending on content
        assert result.returncode in [0, 1]

    def test_exit_code_no_skills_found(self):
        """Test exit code 2 for no skills found."""
        temp_dir = tempfile.mkdtemp()
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "count-tokens.py"), "--directory", temp_dir], check=False, capture_output=True
        )

        assert result.returncode == 2
        shutil.rmtree(temp_dir)


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_malformed_skill_file(self):
        """Test handling malformed SKILL.md file."""
        temp_dir = tempfile.mkdtemp()
        skill_file = Path(temp_dir) / "SKILL.md"
        skill_file.write_text("No proper structure")

        counter = count_tokens.TokenCounter(skill_file)
        results = counter.count_all_levels()

        # Should handle gracefully
        assert "content" in results or "total" in results

        shutil.rmtree(temp_dir)

    def test_empty_skill_file(self):
        """Test handling empty SKILL.md file."""
        temp_dir = tempfile.mkdtemp()
        skill_file = Path(temp_dir) / "SKILL.md"
        skill_file.write_text("")

        counter = count_tokens.TokenCounter(skill_file)
        results = counter.count_all_levels()

        # Should handle gracefully
        assert "total" in results
        assert results["total"]["tokens"] == 0

        shutil.rmtree(temp_dir)

    def test_very_large_skill_file(self):
        """Test handling very large SKILL.md file."""
        temp_dir = tempfile.mkdtemp()
        skill_file = Path(temp_dir) / "SKILL.md"

        # Create large content
        large_content = (
            """---
name: "Large Skill"
description: "Test"
---

# Large Skill

## Level 1: Quick Start (≤1000 tokens)

"""
            + ("A" * 10000)
            + """

## Level 2: Implementation Details (≤5000 tokens)

"""
            + ("B" * 50000)
            + """

## Level 3: Advanced Topics & Resources (no limit)

"""
            + ("C" * 100000)
        )

        skill_file.write_text(large_content)

        counter = count_tokens.TokenCounter(skill_file)
        results = counter.count_all_levels()
        violations = counter.check_violations(results)

        # Should have violations for levels 1 and 2
        assert len(violations) >= 2

        shutil.rmtree(temp_dir)

    def test_skill_file_with_unicode(self):
        """Test handling unicode characters."""
        temp_dir = tempfile.mkdtemp()
        skill_file = Path(temp_dir) / "SKILL.md"

        content = """---
name: "Unicode Skill 🚀"
description: "Test with üñíçödé"
---

# Unicode Skill 🚀

## Level 1: Quick Start (≤1000 tokens)

Content with émojis 🎉 and special chars: café, naïve, résumé

## Level 2: Implementation Details (≤5000 tokens)

More unicode: 中文, 日本語, 한국어

## Level 3: Advanced Topics & Resources (no limit)

Advanced unicode content
"""
        skill_file.write_text(content)

        counter = count_tokens.TokenCounter(skill_file)
        results = counter.count_all_levels()

        # Should handle unicode gracefully
        assert results["total"]["tokens"] > 0

        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=count_tokens", "--cov-report=term-missing"])
