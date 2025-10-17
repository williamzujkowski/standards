#!/usr/bin/env python3
"""
Test Suite: SKILL.md Validation
Tests YAML frontmatter, description limits, and progressive disclosure structure.
"""

import os
import re
import yaml
import pytest
from pathlib import Path
from typing import Dict, List, Optional


class SkillValidator:
    """Validates SKILL.md format and structure."""

    DESCRIPTION_MAX_LENGTH = 1024
    SKILL_MD_FILENAME = "SKILL.md"

    def __init__(self, skills_dir: Path):
        self.skills_dir = Path(skills_dir)

    def find_all_skills(self) -> List[Path]:
        """Find all SKILL.md files in the skills directory."""
        if not self.skills_dir.exists():
            return []
        return list(self.skills_dir.rglob(self.SKILL_MD_FILENAME))

    def extract_frontmatter(self, skill_path: Path) -> Optional[Dict]:
        """Extract and parse YAML frontmatter from SKILL.md."""
        content = skill_path.read_text(encoding='utf-8')

        # Match YAML frontmatter pattern
        pattern = r'^---\s*\n(.*?\n)---\s*\n'
        match = re.match(pattern, content, re.DOTALL)

        if not match:
            return None

        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {skill_path}: {e}")

    def validate_frontmatter_structure(self, frontmatter: Dict, skill_path: Path) -> List[str]:
        """Validate required frontmatter fields."""
        errors = []

        # Required fields
        if 'name' not in frontmatter:
            errors.append(f"{skill_path}: Missing 'name' field in frontmatter")
        elif not isinstance(frontmatter['name'], str):
            errors.append(f"{skill_path}: 'name' must be a string")
        elif not frontmatter['name'].strip():
            errors.append(f"{skill_path}: 'name' cannot be empty")

        if 'description' not in frontmatter:
            errors.append(f"{skill_path}: Missing 'description' field in frontmatter")
        elif not isinstance(frontmatter['description'], str):
            errors.append(f"{skill_path}: 'description' must be a string")
        elif not frontmatter['description'].strip():
            errors.append(f"{skill_path}: 'description' cannot be empty")

        return errors

    def validate_description_length(self, description: str, skill_path: Path) -> Optional[str]:
        """Validate description is within token limits."""
        length = len(description)
        if length > self.DESCRIPTION_MAX_LENGTH:
            return f"{skill_path}: Description exceeds {self.DESCRIPTION_MAX_LENGTH} characters ({length} chars)"
        return None

    def validate_progressive_disclosure(self, skill_path: Path) -> List[str]:
        """Validate progressive disclosure structure (Level 1, 2, 3)."""
        errors = []
        content = skill_path.read_text(encoding='utf-8')

        # Remove frontmatter for analysis
        content_without_frontmatter = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

        # Level 1: Metadata (frontmatter) - already validated

        # Level 2: Core instructions should be in main body
        if len(content_without_frontmatter.strip()) == 0:
            errors.append(f"{skill_path}: Missing Level 2 content (core instructions)")

        # Level 3: Should reference additional resources
        # Look for patterns like ./resources/, ./templates/, ./scripts/
        resource_pattern = r'\.\/(resources|templates|scripts|examples)\/'
        has_resources = bool(re.search(resource_pattern, content))

        # Check for resource directory structure
        skill_dir = skill_path.parent
        resource_dirs = ['resources', 'templates', 'scripts', 'examples']
        has_resource_dirs = any((skill_dir / d).exists() for d in resource_dirs)

        # Warning if skill has no Level 3 resources (not an error, but recommended)
        if not has_resources and not has_resource_dirs:
            # This is informational, not an error
            pass

        return errors

    def validate_skill(self, skill_path: Path) -> Dict[str, any]:
        """Run all validations on a single skill."""
        results = {
            'path': str(skill_path),
            'valid': True,
            'errors': [],
            'warnings': []
        }

        # Extract frontmatter
        try:
            frontmatter = self.extract_frontmatter(skill_path)
            if frontmatter is None:
                results['errors'].append(f"{skill_path}: No valid YAML frontmatter found")
                results['valid'] = False
                return results
        except ValueError as e:
            results['errors'].append(str(e))
            results['valid'] = False
            return results

        # Validate frontmatter structure
        structure_errors = self.validate_frontmatter_structure(frontmatter, skill_path)
        results['errors'].extend(structure_errors)

        # Validate description length
        if 'description' in frontmatter:
            length_error = self.validate_description_length(frontmatter['description'], skill_path)
            if length_error:
                results['errors'].append(length_error)

        # Validate progressive disclosure
        disclosure_errors = self.validate_progressive_disclosure(skill_path)
        results['errors'].extend(disclosure_errors)

        results['valid'] = len(results['errors']) == 0
        return results

    def validate_all_skills(self) -> Dict[str, any]:
        """Validate all skills in the directory."""
        skills = self.find_all_skills()

        results = {
            'total_skills': len(skills),
            'valid_skills': 0,
            'invalid_skills': 0,
            'details': []
        }

        for skill_path in skills:
            skill_result = self.validate_skill(skill_path)
            results['details'].append(skill_result)

            if skill_result['valid']:
                results['valid_skills'] += 1
            else:
                results['invalid_skills'] += 1

        return results


# Pytest test cases
class TestSkillValidation:
    """Test cases for SKILL.md validation."""

    @pytest.fixture
    def validator(self, tmp_path):
        """Create a validator instance with temp directory."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        return SkillValidator(skills_dir)

    def test_valid_skill_structure(self, tmp_path):
        """Test that a properly formatted skill passes validation."""
        skills_dir = tmp_path / "skills" / "test-skill"
        skills_dir.mkdir(parents=True)

        skill_content = """---
name: test-skill
description: This is a valid test skill for validation purposes
---

# Test Skill

## Overview
This is a test skill.

## When to Use
Use this skill when testing.

## Core Instructions
Follow these steps:
1. Step one
2. Step two
"""

        (skills_dir / "SKILL.md").write_text(skill_content)

        validator = SkillValidator(tmp_path / "skills")
        result = validator.validate_skill(skills_dir / "SKILL.md")

        assert result['valid'] == True
        assert len(result['errors']) == 0

    def test_missing_frontmatter(self, tmp_path):
        """Test that missing frontmatter is detected."""
        skills_dir = tmp_path / "skills" / "invalid-skill"
        skills_dir.mkdir(parents=True)

        skill_content = """# Invalid Skill

This skill has no frontmatter.
"""

        (skills_dir / "SKILL.md").write_text(skill_content)

        validator = SkillValidator(tmp_path / "skills")
        result = validator.validate_skill(skills_dir / "SKILL.md")

        assert result['valid'] == False
        assert any("No valid YAML frontmatter" in error for error in result['errors'])

    def test_missing_name_field(self, tmp_path):
        """Test that missing name field is detected."""
        skills_dir = tmp_path / "skills" / "no-name"
        skills_dir.mkdir(parents=True)

        skill_content = """---
description: Missing name field
---

# Content
"""

        (skills_dir / "SKILL.md").write_text(skill_content)

        validator = SkillValidator(tmp_path / "skills")
        result = validator.validate_skill(skills_dir / "SKILL.md")

        assert result['valid'] == False
        assert any("Missing 'name'" in error for error in result['errors'])

    def test_description_length_limit(self, tmp_path):
        """Test that description length limit is enforced."""
        skills_dir = tmp_path / "skills" / "long-desc"
        skills_dir.mkdir(parents=True)

        long_description = "A" * 1025  # Exceeds 1024 limit

        skill_content = f"""---
name: long-description-skill
description: {long_description}
---

# Content
"""

        (skills_dir / "SKILL.md").write_text(skill_content)

        validator = SkillValidator(tmp_path / "skills")
        result = validator.validate_skill(skills_dir / "SKILL.md")

        assert result['valid'] == False
        assert any("exceeds" in error and "1024" in error for error in result['errors'])

    def test_empty_level2_content(self, tmp_path):
        """Test that empty Level 2 content is detected."""
        skills_dir = tmp_path / "skills" / "empty-content"
        skills_dir.mkdir(parents=True)

        skill_content = """---
name: empty-skill
description: This skill has no body content
---

"""

        (skills_dir / "SKILL.md").write_text(skill_content)

        validator = SkillValidator(tmp_path / "skills")
        result = validator.validate_skill(skills_dir / "SKILL.md")

        assert result['valid'] == False
        assert any("Missing Level 2 content" in error for error in result['errors'])

    def test_progressive_disclosure_with_resources(self, tmp_path):
        """Test that resource references are recognized."""
        skills_dir = tmp_path / "skills" / "with-resources"
        skills_dir.mkdir(parents=True)

        # Create resource directory
        (skills_dir / "resources").mkdir()
        (skills_dir / "resources" / "example.md").write_text("# Example")

        skill_content = """---
name: resource-skill
description: Skill with Level 3 resources
---

# Resource Skill

## Overview
This skill has resources.

## Advanced Topics
See ./resources/example.md for more details.
"""

        (skills_dir / "SKILL.md").write_text(skill_content)

        validator = SkillValidator(tmp_path / "skills")
        result = validator.validate_skill(skills_dir / "SKILL.md")

        assert result['valid'] == True

    def test_batch_validation(self, tmp_path):
        """Test validation of multiple skills."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        # Create multiple skills
        for i in range(3):
            skill_dir = skills_dir / f"skill-{i}"
            skill_dir.mkdir()

            skill_content = f"""---
name: skill-{i}
description: Test skill number {i}
---

# Skill {i}

Content for skill {i}.
"""

            (skill_dir / "SKILL.md").write_text(skill_content)

        validator = SkillValidator(skills_dir)
        results = validator.validate_all_skills()

        assert results['total_skills'] == 3
        assert results['valid_skills'] == 3
        assert results['invalid_skills'] == 0


if __name__ == '__main__':
    # Run validation on actual skills directory if it exists
    import sys

    repo_root = Path(__file__).parent.parent.parent
    skills_dir = repo_root / "docs" / "skills"

    if skills_dir.exists():
        validator = SkillValidator(skills_dir)
        results = validator.validate_all_skills()

        print(f"\n=== Skill Validation Results ===")
        print(f"Total skills: {results['total_skills']}")
        print(f"Valid: {results['valid_skills']}")
        print(f"Invalid: {results['invalid_skills']}")

        if results['invalid_skills'] > 0:
            print(f"\n=== Errors ===")
            for detail in results['details']:
                if not detail['valid']:
                    print(f"\n{detail['path']}:")
                    for error in detail['errors']:
                        print(f"  - {error}")
            sys.exit(1)
        else:
            print("\n✓ All skills are valid!")
            sys.exit(0)
    else:
        print(f"Skills directory not found: {skills_dir}")
        print("Run pytest to execute unit tests.")
        sys.exit(1)
