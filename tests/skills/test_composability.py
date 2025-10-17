#!/usr/bin/env python3
"""
Test Suite: Skill Composability
Tests that multiple skills can be loaded and work together seamlessly.
"""

import re
from pathlib import Path
from typing import Dict, List, Set

import pytest
import yaml


class SkillComposability:
    """Test skill composition and interaction."""

    def __init__(self, skills_dir: Path):
        self.skills_dir = Path(skills_dir)
        self.loaded_skills = {}

    def load_skill(self, skill_name: str) -> Dict:
        """Load a skill and its metadata."""
        skill_path = self.skills_dir / skill_name / "SKILL.md"

        if not skill_path.exists():
            raise FileNotFoundError(f"Skill not found: {skill_name}")

        content = skill_path.read_text(encoding="utf-8")

        # Extract frontmatter
        frontmatter_match = re.match(r"^---\s*\n(.*?\n)---\s*\n", content, re.DOTALL)
        if not frontmatter_match:
            raise ValueError(f"No frontmatter in skill: {skill_name}")

        frontmatter = yaml.safe_load(frontmatter_match.group(1))

        skill_data = {"name": skill_name, "path": skill_path, "metadata": frontmatter, "content": content}

        self.loaded_skills[skill_name] = skill_data
        return skill_data

    def load_multiple_skills(self, skill_names: List[str]) -> Dict[str, Dict]:
        """Load multiple skills at once."""
        results = {}
        for skill_name in skill_names:
            try:
                results[skill_name] = self.load_skill(skill_name)
            except (FileNotFoundError, ValueError) as e:
                results[skill_name] = {"error": str(e)}
        return results

    def detect_skill_dependencies(self, skill_name: str) -> Set[str]:
        """Detect dependencies/references to other skills."""
        if skill_name not in self.loaded_skills:
            self.load_skill(skill_name)

        content = self.loaded_skills[skill_name]["content"]

        # Look for skill references
        # Patterns: "Load skill-name", "see skill-name", "requires skill-name"
        dependencies = set()

        # Pattern: explicit skill references
        skill_ref_patterns = [
            r"Load\s+([a-z0-9-]+)\s+skill",
            r"see\s+([a-z0-9-]+)\s+skill",
            r"requires?\s+([a-z0-9-]+)\s+skill",
            r"depends?\s+on\s+([a-z0-9-]+)",
        ]

        for pattern in skill_ref_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            dependencies.update(matches)

        return dependencies

    def check_circular_dependencies(self, skill_name: str, visited: Set[str] = None) -> bool:
        """Check for circular dependencies in skill references."""
        if visited is None:
            visited = set()

        if skill_name in visited:
            return True  # Circular dependency detected

        visited.add(skill_name)

        dependencies = self.detect_skill_dependencies(skill_name)

        for dep in dependencies:
            if dep in self.loaded_skills or (self.skills_dir / dep / "SKILL.md").exists():
                if self.check_circular_dependencies(dep, visited.copy()):
                    return True

        return False

    def test_skill_combination(self, skill_names: List[str]) -> Dict:
        """Test loading and combining multiple skills."""
        results = {
            "skills_loaded": 0,
            "skills_failed": 0,
            "total_level1_tokens": 0,
            "conflicts": [],
            "dependencies": {},
            "success": True,
        }

        loaded = self.load_multiple_skills(skill_names)

        for skill_name, skill_data in loaded.items():
            if "error" in skill_data:
                results["skills_failed"] += 1
                results["success"] = False
            else:
                results["skills_loaded"] += 1

                # Count level 1 tokens (frontmatter)
                frontmatter_text = yaml.dump(skill_data["metadata"])
                results["total_level1_tokens"] += len(frontmatter_text) // 4

                # Detect dependencies
                deps = self.detect_skill_dependencies(skill_name)
                if deps:
                    results["dependencies"][skill_name] = list(deps)

        return results

    def validate_skill_compatibility(self, skill_names: List[str]) -> Dict:
        """Validate that skills can work together without conflicts."""
        results = {"compatible": True, "issues": []}

        # Load all skills
        loaded = self.load_multiple_skills(skill_names)

        # Check for naming conflicts
        names_seen = set()
        for skill_name, skill_data in loaded.items():
            if "error" not in skill_data:
                metadata = skill_data["metadata"]
                if "name" in metadata:
                    if metadata["name"] in names_seen:
                        results["compatible"] = False
                        results["issues"].append(f"Duplicate skill name: {metadata['name']}")
                    names_seen.add(metadata["name"])

        # Check for circular dependencies
        for skill_name in skill_names:
            if self.check_circular_dependencies(skill_name):
                results["compatible"] = False
                results["issues"].append(f"Circular dependency detected for: {skill_name}")

        return results


# Test cases
class TestSkillComposability:
    """Test skill composition scenarios."""

    @pytest.fixture
    def composability_tester(self, tmp_path):
        """Create composability tester with sample skills."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        # Create sample skills
        self._create_sample_skill(skills_dir, "python-standards", "Python coding standards and best practices")
        self._create_sample_skill(skills_dir, "testing-standards", "Testing methodologies and frameworks")
        self._create_sample_skill(skills_dir, "security-standards", "Security best practices and compliance")

        return SkillComposability(skills_dir)

    def _create_sample_skill(self, skills_dir: Path, name: str, description: str):
        """Helper to create sample skill."""
        skill_dir = skills_dir / name
        skill_dir.mkdir()

        content = f"""---
name: {name}
description: {description}
---

# {name.replace('-', ' ').title()}

## Overview
This is the {name} skill.

## Core Instructions
Follow these guidelines.
"""

        (skill_dir / "SKILL.md").write_text(content)

    def test_load_single_skill(self, composability_tester):
        """Test loading a single skill."""
        skill = composability_tester.load_skill("python-standards")

        assert skill["name"] == "python-standards"
        assert "metadata" in skill
        assert "content" in skill

    def test_load_multiple_skills(self, composability_tester):
        """Test loading multiple skills simultaneously."""
        skills = composability_tester.load_multiple_skills(
            ["python-standards", "testing-standards", "security-standards"]
        )

        assert len(skills) == 3
        assert all("error" not in s for s in skills.values())

    def test_skill_combination(self, composability_tester):
        """Test combining multiple skills."""
        result = composability_tester.test_skill_combination(["python-standards", "testing-standards"])

        assert result["success"] == True
        assert result["skills_loaded"] == 2
        assert result["skills_failed"] == 0

    def test_nonexistent_skill(self, composability_tester):
        """Test handling of nonexistent skills."""
        with pytest.raises(FileNotFoundError):
            composability_tester.load_skill("nonexistent-skill")

    def test_skill_compatibility(self, composability_tester):
        """Test skill compatibility checking."""
        result = composability_tester.validate_skill_compatibility(
            ["python-standards", "testing-standards", "security-standards"]
        )

        assert result["compatible"] == True
        assert len(result["issues"]) == 0

    def test_dependency_detection(self, tmp_path):
        """Test detection of skill dependencies."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        # Create skill with dependency
        skill_dir = skills_dir / "advanced-skill"
        skill_dir.mkdir()

        content = """---
name: advanced-skill
description: Advanced skill that depends on basics
---

# Advanced Skill

This skill requires basic-skill skill for fundamental concepts.
Load python-standards skill first.
"""

        (skill_dir / "SKILL.md").write_text(content)

        tester = SkillComposability(skills_dir)
        deps = tester.detect_skill_dependencies("advanced-skill")

        assert "basic-skill" in deps
        assert "python-standards" in deps

    def test_circular_dependency_detection(self, tmp_path):
        """Test detection of circular dependencies."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        # Create skill A that depends on B
        skill_a_dir = skills_dir / "skill-a"
        skill_a_dir.mkdir()
        (skill_a_dir / "SKILL.md").write_text(
            """---
name: skill-a
description: Skill A
---

Requires skill-b skill.
"""
        )

        # Create skill B that depends on A (circular)
        skill_b_dir = skills_dir / "skill-b"
        skill_b_dir.mkdir()
        (skill_b_dir / "SKILL.md").write_text(
            """---
name: skill-b
description: Skill B
---

Requires skill-a skill.
"""
        )

        tester = SkillComposability(skills_dir)
        has_circular = tester.check_circular_dependencies("skill-a")

        assert has_circular == True


if __name__ == "__main__":
    # Run composability analysis on real skills
    repo_root = Path(__file__).parent.parent.parent
    skills_dir = repo_root / "docs" / "skills"

    if skills_dir.exists():
        print("\n=== Skill Composability Analysis ===\n")

        tester = SkillComposability(skills_dir)

        # Find all skills
        all_skills = [d.name for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]

        print(f"Found {len(all_skills)} skills\n")

        # Test loading all skills together
        result = tester.test_skill_combination(all_skills)

        print(f"Skills loaded: {result['skills_loaded']}")
        print(f"Skills failed: {result['skills_failed']}")
        print(f"Total Level 1 tokens: {result['total_level1_tokens']:,}")

        if result["dependencies"]:
            print("\nDependencies detected:")
            for skill, deps in result["dependencies"].items():
                print(f"  {skill} -> {', '.join(deps)}")

        # Check compatibility
        compatibility = tester.validate_skill_compatibility(all_skills)
        print(f"\nCompatibility: {'✓ Compatible' if compatibility['compatible'] else '✗ Issues found'}")

        if compatibility["issues"]:
            print("Issues:")
            for issue in compatibility["issues"]:
                print(f"  - {issue}")
    else:
        print(f"Skills directory not found: {skills_dir}")
        print("Run pytest to execute unit tests.")
