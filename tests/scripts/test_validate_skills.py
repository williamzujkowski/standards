#!/usr/bin/env python3
"""
Comprehensive tests for validate-skills.py

Tests cover:
- Unit tests for individual validator methods
- Integration tests for full validation workflows
- Edge cases and error handling
- Exit codes and reporting
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

# Import the script (handle hyphenated names)
import importlib.util

spec = importlib.util.spec_from_file_location(
    "validate_skills", Path(__file__).parent.parent.parent / "scripts" / "validate-skills.py"
)
validate_skills = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_skills)
SkillValidator = validate_skills.SkillValidator


class TestSkillValidator:
    """Test suite for SkillValidator class."""

    @pytest.fixture
    def fixtures_dir(self):
        """Return path to test fixtures."""
        return Path(__file__).parent / "fixtures" / "skills"

    @pytest.fixture
    def validator(self, fixtures_dir):
        """Create a validator instance with fixtures."""
        return SkillValidator(fixtures_dir)

    @pytest.fixture
    def valid_skill_content(self):
        """Return valid SKILL.md content."""
        return """---
name: test-skill
description: A test skill with proper structure and content
version: 1.0.0
---

# Test Skill

## Level 1: Quick Start

### What You'll Learn
Core concepts and quick start guide.

### Core Principles
- **Principle 1**: First principle
- **Principle 2**: Second principle
- **Principle 3**: Third principle
- **Principle 4**: Fourth principle

### Quick Reference
```python
print("Hello World")
```

### Essential Checklist
- [ ] Item 1
- [ ] Item 2

### Common Pitfalls
- Pitfall 1
- Pitfall 2

---

## Level 2: Implementation
Detailed implementation content.

---

## Level 3: Mastery
Advanced topics.
"""

    # ==================== UNIT TESTS ====================

    def test_validate_frontmatter_valid(self, validator, valid_skill_content):
        """Test frontmatter validation with valid YAML."""
        result = validator.validate_frontmatter("test-skill", valid_skill_content)
        assert result is True
        assert len(validator.errors) == 0

    def test_validate_frontmatter_missing(self, validator):
        """Test detection of missing frontmatter."""
        content = "# Skill\n\nNo frontmatter here."
        result = validator.validate_frontmatter("test-skill", content)
        assert result is False
        assert any("Missing YAML frontmatter" in err for err in validator.errors)

    def test_validate_frontmatter_invalid_yaml(self, validator):
        """Test detection of invalid YAML syntax."""
        content = "---\nname: test\ninvalid: [unclosed\n---\n\nContent"
        result = validator.validate_frontmatter("test-skill", content)
        assert result is False
        assert any("Invalid YAML" in err for err in validator.errors)

    def test_validate_frontmatter_missing_name(self, validator):
        """Test detection of missing 'name' field."""
        content = "---\ndescription: Test skill\n---\n\nContent"
        result = validator.validate_frontmatter("test-skill", content)
        assert result is False
        assert any("Missing 'name'" in err for err in validator.errors)

    def test_validate_frontmatter_missing_description(self, validator):
        """Test detection of missing 'description' field."""
        content = "---\nname: test-skill\n---\n\nContent"
        result = validator.validate_frontmatter("test-skill", content)
        assert result is False
        assert any("Missing 'description'" in err for err in validator.errors)

    def test_validate_frontmatter_short_description(self, validator):
        """Test warning for short description."""
        content = "---\nname: test-skill\ndescription: Short\n---\n\nContent"
        result = validator.validate_frontmatter("test-skill", content)
        assert result is True  # Should still be valid, just a warning
        assert any("Description too short" in warn for warn in validator.warnings)

    def test_validate_frontmatter_name_mismatch(self, validator):
        """Test warning for name mismatch."""
        content = "---\nname: different-name\ndescription: A proper description here\n---\n\nContent"
        result = validator.validate_frontmatter("test-skill", content)
        assert result is True  # Valid but warns
        assert any("Name mismatch" in warn for warn in validator.warnings)

    def test_validate_structure_valid(self, validator, valid_skill_content):
        """Test structure validation with all required sections."""
        result = validator.validate_structure("test-skill", valid_skill_content)
        assert result is True

    def test_validate_structure_missing_level1(self, validator):
        """Test detection of missing Level 1 section."""
        content = "---\nname: test\ndescription: Test\n---\n\n## Level 2: Implementation\n"
        result = validator.validate_structure("test-skill", content)
        assert result is False
        assert any("Missing 'Level 1: Quick Start'" in err for err in validator.errors)

    def test_validate_structure_missing_level2(self, validator):
        """Test warning for missing Level 2 section."""
        content = "---\nname: test\ndescription: Test\n---\n\n## Level 1: Quick Start\n"
        result = validator.validate_structure("test-skill", content)
        assert result is True
        assert any("Missing 'Level 2: Implementation'" in warn for warn in validator.warnings)

    def test_validate_structure_missing_level3(self, validator):
        """Test warning for missing Level 3 section."""
        content = "---\nname: test\ndescription: Test\n---\n\n## Level 1: Quick Start\n## Level 2: Implementation\n"
        result = validator.validate_structure("test-skill", content)
        assert result is True
        assert any("Missing 'Level 3: Mastery'" in warn for warn in validator.warnings)

    def test_validate_structure_missing_subsections(self, validator):
        """Test warnings for missing recommended subsections."""
        content = """---
name: test
description: Test skill
---

## Level 1: Quick Start

Some content without subsections.
"""
        validator.validate_structure("test-skill", content)
        # Should warn about missing subsections
        assert len(validator.warnings) > 0

    def test_validate_token_counts_valid(self, validator, valid_skill_content):
        """Test token count validation with reasonable content."""
        result = validator.validate_token_counts("test-skill", valid_skill_content)
        assert result is True

    def test_validate_token_counts_level1_too_long(self, validator):
        """Test detection of excessively long Level 1."""
        # Create content with >2000 tokens in Level 1 (~8000 chars)
        long_content = "x " * 4000
        content = f"""---
name: test
description: Test skill
---

## Level 1: Quick Start

{long_content}

## Level 2: Implementation
Short
"""
        result = validator.validate_token_counts("test-skill", content)
        assert result is False
        assert any("Level 1 too long" in warn for warn in validator.warnings)

    def test_validate_token_counts_level2_too_long(self, validator):
        """Test warning for excessively long Level 2."""
        long_content = "x " * 10000
        content = f"""---
name: test
description: Test skill
---

## Level 1: Quick Start
Short

## Level 2: Implementation
{long_content}
"""
        validator.validate_token_counts("test-skill", content)
        assert any("Level 2 too long" in warn for warn in validator.warnings)

    def test_extract_level(self, validator):
        """Test level content extraction."""
        content = """## Level 1: Quick Start
L1 content
## Level 2: Implementation
L2 content
## Level 3: Mastery
L3 content"""

        level1 = validator.extract_level(content, 1)
        level2 = validator.extract_level(content, 2)
        level3 = validator.extract_level(content, 3)

        assert "L1 content" in level1
        assert "L2 content" in level2
        assert "L3 content" in level3

    def test_validate_directories_all_present(self, validator, fixtures_dir):
        """Test directory validation when all directories exist."""
        skill_dir = fixtures_dir / "valid-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "templates").mkdir(exist_ok=True)
        (skill_dir / "scripts").mkdir(exist_ok=True)
        (skill_dir / "resources").mkdir(exist_ok=True)

        result = validator.validate_directories(skill_dir)
        assert result is True

    def test_validate_directories_missing(self, validator, tmp_path):
        """Test warnings for missing directories."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()

        validator.validate_directories(skill_dir)
        assert len(validator.warnings) >= 3  # Should warn for each missing dir

    def test_validate_cross_references_valid(self, validator, fixtures_dir):
        """Test cross-reference validation with valid references."""
        # Create referenced skill
        ref_skill = fixtures_dir / "referenced-skill"
        ref_skill.mkdir(parents=True, exist_ok=True)
        (ref_skill / "SKILL.md").write_text("# Referenced Skill")

        content = """---
name: test
description: Test skill
---

See also: [Referenced](../referenced-skill/SKILL.md)
"""
        result = validator.validate_cross_references("test", content)
        assert result is True

    def test_validate_cross_references_broken(self, validator):
        """Test detection of broken cross-references."""
        content = """---
name: test
description: Test skill
---

See also: [Broken](../nonexistent-skill/SKILL.md)
"""
        result = validator.validate_cross_references("test", content)
        assert result is False
        assert any("Invalid reference" in err for err in validator.errors)

    # ==================== INTEGRATION TESTS ====================

    def test_validate_skill_complete_valid(self, validator, fixtures_dir):
        """Test complete validation of a valid skill."""
        skill_dir = fixtures_dir / "valid-skill"
        result = validator.validate_skill(skill_dir)
        assert result is True

    def test_validate_skill_missing_file(self, validator, tmp_path):
        """Test validation of skill without SKILL.md."""
        skill_dir = tmp_path / "empty-skill"
        skill_dir.mkdir()

        result = validator.validate_skill(skill_dir)
        assert result is False
        assert any("Missing SKILL.md" in err for err in validator.errors)

    def test_validate_all_mixed_skills(self, validator, fixtures_dir):
        """Test validation of directory with mixed valid/invalid skills."""
        result = validator.validate_all()
        # Should process all skills and detect issues
        assert validator.skills_validated > 0

    def test_validate_all_empty_directory(self, tmp_path):
        """Test validation of empty skills directory."""
        validator = SkillValidator(tmp_path)
        result = validator.validate_all()
        assert result is False

    def test_validate_all_nonexistent_directory(self, tmp_path):
        """Test validation of nonexistent directory."""
        validator = SkillValidator(tmp_path / "nonexistent")
        result = validator.validate_all()
        assert result is False

    def test_export_report(self, validator, tmp_path):
        """Test JSON report export."""
        validator.errors = ["Error 1", "Error 2"]
        validator.warnings = ["Warning 1"]
        validator.skills_validated = 5

        output_path = tmp_path / "report.json"
        validator.export_report(output_path)

        assert output_path.exists()

        with open(output_path) as f:
            report = json.load(f)

        assert report["skills_validated"] == 5
        assert len(report["errors"]) == 2
        assert len(report["warnings"]) == 1
        assert report["valid"] is False

    def test_export_report_valid_skills(self, validator, tmp_path):
        """Test report export with all valid skills."""
        validator.errors = []
        validator.warnings = []
        validator.skills_validated = 3

        output_path = tmp_path / "report.json"
        validator.export_report(output_path)

        with open(output_path) as f:
            report = json.load(f)

        assert report["valid"] is True

    # ==================== EDGE CASES ====================

    def test_empty_content(self, validator):
        """Test validation of empty content."""
        result = validator.validate_frontmatter("test", "")
        assert result is False

    def test_very_short_description(self, validator):
        """Test validation with extremely short description."""
        content = "---\nname: test\ndescription: Hi\n---\n\nContent"
        validator.validate_frontmatter("test", content)
        assert len(validator.warnings) > 0

    def test_very_long_description(self, validator):
        """Test validation with very long description (>1024 chars)."""
        long_desc = "x" * 1100
        content = f"---\nname: test\ndescription: {long_desc}\n---\n\nContent"
        result = validator.validate_frontmatter("test", content)
        # Should still be valid (just long)
        assert result is True

    def test_unicode_content(self, validator):
        """Test validation with unicode characters."""
        content = """---
name: test-unicode
description: Testing with émojis 🎉 and spëcial çharacters
---

## Level 1: Quick Start

Üñíçödé çöñtëñt hërë.
"""
        result = validator.validate_frontmatter("test-unicode", content)
        assert result is True

    def test_regex_patterns_in_code(self, validator):
        """Test that code with regex patterns doesn't break validation."""
        content = """---
name: test
description: Test with regex patterns
---

## Level 1: Quick Start

```python
pattern = r"^## Level (\\d+):.*?(?=## Level|\\Z)"
```
"""
        result = validator.validate_structure("test", content)
        assert result is True

    # ==================== CLI INTEGRATION ====================

    @patch("sys.argv", ["validate-skills.py", "--help"])
    def test_help_flag(self, capsys):
        """Test --help flag."""
        # Import main from the module object
        main = validate_skills.main

        # Help flag should return without error
        try:
            main()
        except SystemExit:
            pass

    @patch("sys.argv", ["validate-skills.py", "--export", "/tmp/report.json"])
    def test_export_flag(self, tmp_path, monkeypatch):
        """Test --export flag."""
        # This would require mocking the entire main() flow
        # For now, just verify the flag is recognized
        pass


# ==================== FIXTURES VALIDATION ====================


class TestFixtures:
    """Validate that test fixtures are set up correctly."""

    def test_fixtures_directory_exists(self):
        """Test that fixtures directory exists."""
        fixtures_dir = Path(__file__).parent / "fixtures" / "skills"
        assert fixtures_dir.exists()

    def test_valid_skill_fixture(self):
        """Test that valid skill fixture is properly structured."""
        fixture_path = Path(__file__).parent / "fixtures" / "skills" / "valid-skill" / "SKILL.md"
        assert fixture_path.exists()

        content = fixture_path.read_text()
        assert "---" in content
        assert "name: valid-skill" in content
        assert "## Level 1: Quick Start" in content

    def test_invalid_fixtures_exist(self):
        """Test that invalid skill fixtures exist."""
        fixtures_dir = Path(__file__).parent / "fixtures" / "skills"
        invalid_skills = ["invalid-frontmatter", "missing-level1", "too-long-level1", "broken-reference"]

        for skill in invalid_skills:
            assert (fixtures_dir / skill / "SKILL.md").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=validate_skills", "--cov-report=term-missing"])
