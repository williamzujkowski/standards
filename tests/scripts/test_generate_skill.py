#!/usr/bin/env python3
"""Comprehensive unit tests for generate-skill.py with >90% coverage."""

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


spec = importlib.util.spec_from_file_location("generate_skill", SCRIPTS_DIR / "generate-skill.py")
generate_skill = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_skill)


class TestSkillSlugGeneration:
    """Test skill slug generation."""

    def test_basic_slug_generation(self):
        """Test basic slug generation from name."""
        assert generate_skill.generate_skill_slug("API Security") == "api-security"
        assert generate_skill.generate_skill_slug("Test Driven Development") == "test-driven-development"
        assert generate_skill.generate_skill_slug("REST API") == "rest-api"

    def test_slug_with_underscores(self):
        """Test slug generation with underscores."""
        assert generate_skill.generate_skill_slug("Test_Skill_Name") == "test-skill-name"
        assert generate_skill.generate_skill_slug("API_Security_v2") == "api-security-v2"

    def test_slug_with_special_characters(self):
        """Test slug generation removes special characters."""
        result = generate_skill.generate_skill_slug("REST API v2.0")
        assert result == "rest-api-v2.0"

    def test_slug_lowercase(self):
        """Test slug is always lowercase."""
        assert generate_skill.generate_skill_slug("UPPERCASE") == "uppercase"
        assert generate_skill.generate_skill_slug("MixedCase") == "mixedcase"

    def test_slug_empty_string(self):
        """Test slug generation with empty string."""
        assert generate_skill.generate_skill_slug("") == ""


class TestDescriptionValidation:
    """Test description length validation."""

    def test_valid_description_length(self):
        """Test description within limit."""
        valid_description = "A" * 1024
        assert generate_skill.validate_description_length(valid_description) is True

    def test_description_at_limit(self):
        """Test description exactly at limit."""
        exact_limit = "A" * 1024
        assert generate_skill.validate_description_length(exact_limit) is True

    def test_description_over_limit(self):
        """Test description exceeds limit."""
        over_limit = "A" * 1025
        assert generate_skill.validate_description_length(over_limit) is False

    def test_short_description(self):
        """Test short description."""
        short = "Short description"
        assert generate_skill.validate_description_length(short) is True

    def test_empty_description(self):
        """Test empty description."""
        assert generate_skill.validate_description_length("") is True


class TestDirectoryCreation:
    """Test directory structure creation."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        temp = tempfile.mkdtemp()
        yield Path(temp)
        shutil.rmtree(temp, ignore_errors=True)

    def test_create_skill_directories(self, temp_dir):
        """Test all required directories are created."""
        skill_slug = "test-skill"
        skill_dir = generate_skill.create_skill_directories(temp_dir, skill_slug)

        # Verify base directory
        assert skill_dir.exists()
        assert skill_dir.name == skill_slug

        # Verify subdirectories
        assert (skill_dir / "templates").exists()
        assert (skill_dir / "scripts").exists()
        assert (skill_dir / "resources").exists()

    def test_create_skill_directories_nested(self, temp_dir):
        """Test creating nested skill directories."""
        skill_slug = "category/subcategory/skill"
        skill_dir = generate_skill.create_skill_directories(temp_dir, skill_slug)
        assert skill_dir.exists()

    def test_create_skill_directories_existing(self, temp_dir):
        """Test creating directories when they already exist."""
        skill_slug = "test-skill"
        # Create once
        skill_dir1 = generate_skill.create_skill_directories(temp_dir, skill_slug)
        # Create again (should not fail)
        skill_dir2 = generate_skill.create_skill_directories(temp_dir, skill_slug)
        assert skill_dir1 == skill_dir2


class TestSkillFileCreation:
    """Test SKILL.md file creation."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        temp = tempfile.mkdtemp()
        temp_path = Path(temp)
        (temp_path / "test-skill").mkdir(parents=True)
        yield temp_path
        shutil.rmtree(temp, ignore_errors=True)

    def test_create_skill_file_basic(self, temp_dir):
        """Test basic SKILL.md file creation."""
        skill_dir = temp_dir / "test-skill"
        name = "Test Skill"
        description = "Test description"

        skill_file = generate_skill.create_skill_file(skill_dir, name, description, dry_run=False)

        assert skill_file.exists()
        assert skill_file.name == "SKILL.md"

        content = skill_file.read_text()
        assert name in content
        assert description in content

    def test_create_skill_file_dry_run(self, temp_dir):
        """Test dry-run mode doesn't create files."""
        skill_dir = temp_dir / "test-skill"
        skill_file = generate_skill.create_skill_file(skill_dir, "Test", "Description", dry_run=True)
        assert not skill_file.exists()

    def test_skill_file_has_frontmatter(self, temp_dir):
        """Test SKILL.md file has YAML frontmatter."""
        skill_dir = temp_dir / "test-skill"
        skill_file = generate_skill.create_skill_file(skill_dir, "Test Skill", "Test description", dry_run=False)

        content = skill_file.read_text()
        assert content.startswith("---")

    def test_skill_file_has_all_levels(self, temp_dir):
        """Test SKILL.md file has all 3 levels."""
        skill_dir = temp_dir / "test-skill"
        skill_file = generate_skill.create_skill_file(skill_dir, "Test Skill", "Test description", dry_run=False)

        content = skill_file.read_text()
        assert "## Level 1: Quick Start" in content
        assert "## Level 2: Implementation Details" in content
        assert "## Level 3: Advanced Topics & Resources" in content


class TestSkillValidation:
    """Test skill structure validation."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        temp = tempfile.mkdtemp()
        temp_path = Path(temp)
        (temp_path / "test-skill").mkdir(parents=True)
        yield temp_path
        shutil.rmtree(temp, ignore_errors=True)

    def test_validate_valid_skill(self, temp_dir):
        """Test validation of valid skill."""
        skill_dir = temp_dir / "test-skill"
        skill_file = generate_skill.create_skill_file(skill_dir, "Test Skill", "Test description", dry_run=False)

        assert generate_skill.validate_skill_structure(skill_file) is True

    def test_validate_missing_frontmatter(self, temp_dir):
        """Test validation fails without frontmatter."""
        skill_dir = temp_dir / "test-skill"
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text("# Test\n\nNo frontmatter")

        assert generate_skill.validate_skill_structure(skill_file) is False

    def test_validate_missing_level(self, temp_dir):
        """Test validation fails with missing level."""
        skill_dir = temp_dir / "test-skill"
        skill_file = skill_dir / "SKILL.md"
        content = """---
name: "Test"
description: "Test"
---

# Test

## Level 1: Quick Start
Content

## Level 2: Implementation Details
Content
"""
        skill_file.write_text(content)

        assert generate_skill.validate_skill_structure(skill_file) is False

    def test_validate_invalid_yaml(self, temp_dir):
        """Test validation fails with invalid YAML."""
        skill_dir = temp_dir / "test-skill"
        skill_file = skill_dir / "SKILL.md"
        content = """---
name: "Test
invalid: yaml: structure
---

# Test

## Level 1: Quick Start
## Level 2: Implementation Details
## Level 3: Advanced Topics & Resources
"""
        skill_file.write_text(content)

        assert generate_skill.validate_skill_structure(skill_file) is False

    def test_validate_missing_name_in_frontmatter(self, temp_dir):
        """Test validation fails without name in frontmatter."""
        skill_dir = temp_dir / "test-skill"
        skill_file = skill_dir / "SKILL.md"
        content = """---
description: "Test"
---

# Test

## Level 1: Quick Start
## Level 2: Implementation Details
## Level 3: Advanced Topics & Resources
"""
        skill_file.write_text(content)

        assert generate_skill.validate_skill_structure(skill_file) is False


class TestReadmeCreation:
    """Test README.md creation."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        temp = tempfile.mkdtemp()
        temp_path = Path(temp)
        (temp_path / "test-skill").mkdir(parents=True)
        yield temp_path
        shutil.rmtree(temp, ignore_errors=True)

    def test_create_readme(self, temp_dir):
        """Test README.md creation."""
        skill_dir = temp_dir / "test-skill"
        name = "Test Skill"
        description = "Test description"

        generate_skill.create_readme(skill_dir, name, description, dry_run=False)

        readme = skill_dir / "README.md"
        assert readme.exists()

        content = readme.read_text()
        assert name in content
        assert description in content
        assert "SKILL.md" in content

    def test_create_readme_dry_run(self, temp_dir):
        """Test README.md dry-run mode."""
        skill_dir = temp_dir / "test-skill"
        generate_skill.create_readme(skill_dir, "Test", "Desc", dry_run=True)

        readme = skill_dir / "README.md"
        assert not readme.exists()


class TestIntegrationTests:
    """Integration tests for full workflow."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        temp = tempfile.mkdtemp()
        yield Path(temp)
        shutil.rmtree(temp, ignore_errors=True)

    def test_full_skill_generation_workflow(self, temp_dir):
        """Test complete skill generation workflow."""
        name = "Integration Test Skill"
        description = "Integration test description"
        skill_slug = generate_skill.generate_skill_slug(name)

        # Create directories
        skill_dir = generate_skill.create_skill_directories(temp_dir, skill_slug)

        # Create skill file
        skill_file = generate_skill.create_skill_file(skill_dir, name, description, dry_run=False)

        # Create README
        generate_skill.create_readme(skill_dir, name, description, dry_run=False)

        # Validate structure
        assert skill_dir.exists()
        assert skill_file.exists()
        assert (skill_dir / "README.md").exists()
        assert (skill_dir / "templates").exists()
        assert (skill_dir / "scripts").exists()
        assert (skill_dir / "resources").exists()

        # Validate content
        assert generate_skill.validate_skill_structure(skill_file) is True

    def test_command_line_execution(self, temp_dir):
        """Test command-line execution."""
        result = subprocess.run(
            [
                "python3",
                str(SCRIPTS_DIR / "generate-skill.py"),
                "--name",
                "CLI Test Skill",
                "--description",
                "CLI test description",
                "--output-dir",
                str(temp_dir),
                "--dry-run",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        # Output may be in stdout or stderr depending on logging config
        combined_output = (result.stdout + result.stderr).lower()
        assert "cli-test-skill" in combined_output

    def test_validation_flag(self, temp_dir):
        """Test --validate flag."""
        name = "Validation Test"
        description = "Test"
        skill_slug = generate_skill.generate_skill_slug(name)

        # Create skill
        skill_dir = generate_skill.create_skill_directories(temp_dir, skill_slug)
        generate_skill.create_skill_file(skill_dir, name, description, dry_run=False)

        # Run with validation
        result = subprocess.run(
            [
                "python3",
                str(SCRIPTS_DIR / "generate-skill.py"),
                "--name",
                name,
                "--description",
                description,
                "--output-dir",
                str(temp_dir),
                "--validate",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        assert "validation passed" in result.stdout.lower() or result.returncode == 0


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        temp = tempfile.mkdtemp()
        yield Path(temp)
        shutil.rmtree(temp, ignore_errors=True)

    def test_special_characters_in_name(self, temp_dir):
        """Test handling special characters in skill name."""
        name = "REST API v2.0 (Beta)"
        description = "Test"
        skill_slug = generate_skill.generate_skill_slug(name)

        skill_dir = generate_skill.create_skill_directories(temp_dir, skill_slug)
        skill_file = generate_skill.create_skill_file(skill_dir, name, description, dry_run=False)

        assert skill_file.exists()
        content = skill_file.read_text()
        assert name in content

    def test_very_long_name(self, temp_dir):
        """Test handling very long skill name."""
        name = "A" * 100
        description = "Test"
        skill_slug = generate_skill.generate_skill_slug(name)

        skill_dir = generate_skill.create_skill_directories(temp_dir, skill_slug)
        assert skill_dir.exists()

    def test_unicode_characters(self, temp_dir):
        """Test handling unicode characters."""
        name = "Skill with émojis 🚀"
        description = "Test with üñíçödé"
        skill_slug = generate_skill.generate_skill_slug(name)

        skill_dir = generate_skill.create_skill_directories(temp_dir, skill_slug)
        skill_file = generate_skill.create_skill_file(skill_dir, name, description, dry_run=False)

        assert skill_file.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=generate_skill", "--cov-report=term-missing"])
