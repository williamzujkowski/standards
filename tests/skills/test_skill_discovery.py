#!/usr/bin/env python3
"""
Test Suite: Skill Discovery
Tests skill discovery and loading mechanisms.
"""

import re
from pathlib import Path

import pytest
import yaml


class SkillDiscovery:
    """Skill discovery and loading system."""

    def __init__(self, skills_dir: Path):
        self.skills_dir = Path(skills_dir)
        self.skill_cache = {}

    def discover_all_skills(self) -> list[dict]:
        """Discover all available skills."""
        if not self.skills_dir.exists():
            return []

        skills = []

        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue

            skill_info = self._extract_skill_metadata(skill_md)
            if skill_info:
                skill_info["directory"] = str(skill_dir)
                skills.append(skill_info)

        return skills

    def _extract_skill_metadata(self, skill_path: Path) -> dict | None:
        """Extract metadata from SKILL.md."""
        try:
            content = skill_path.read_text(encoding="utf-8")

            # Extract frontmatter
            frontmatter_match = re.match(r"^---\s*\n(.*?\n)---\s*\n", content, re.DOTALL)
            if not frontmatter_match:
                return None

            metadata = yaml.safe_load(frontmatter_match.group(1))

            return {
                "name": metadata.get("name", ""),
                "description": metadata.get("description", ""),
                "path": str(skill_path),
            }
        except Exception:
            return None

    def search_skills(self, query: str) -> list[dict]:
        """Search skills by keyword."""
        all_skills = self.discover_all_skills()
        query_lower = query.lower()

        matches = []

        for skill in all_skills:
            # Search in name
            if query_lower in skill["name"].lower():
                skill["match_score"] = 2  # High relevance
                matches.append(skill)
                continue

            # Search in description
            if query_lower in skill["description"].lower():
                skill["match_score"] = 1  # Medium relevance
                matches.append(skill)

        # Sort by match score
        matches.sort(key=lambda x: x.get("match_score", 0), reverse=True)

        return matches

    def find_skills_by_category(self, category: str) -> list[dict]:
        """Find skills by category/domain."""
        all_skills = self.discover_all_skills()
        category_lower = category.lower()

        matches = []

        for skill in all_skills:
            # Check if category appears in name or description
            if category_lower in skill["name"].lower() or category_lower in skill["description"].lower():
                matches.append(skill)

        return matches

    def get_skill_by_name(self, name: str) -> dict | None:
        """Get a specific skill by name."""
        if name in self.skill_cache:
            return self.skill_cache[name]

        skill_path = self.skills_dir / name / "SKILL.md"

        if not skill_path.exists():
            return None

        skill_info = self._extract_skill_metadata(skill_path)

        if skill_info:
            skill_info["directory"] = str(self.skills_dir / name)
            self.skill_cache[name] = skill_info

        return skill_info

    def recommend_skills(self, context: str) -> list[dict]:
        """Recommend skills based on context."""
        # Simple keyword-based recommendation
        keywords = {
            "api": ["security", "testing", "coding"],
            "web": ["frontend", "security", "performance"],
            "mobile": ["frontend", "mobile", "testing"],
            "security": ["security", "nist-compliance", "testing"],
            "testing": ["testing", "tdd", "integration"],
            "data": ["data-engineering", "observability", "performance"],
        }

        context_lower = context.lower()
        relevant_categories = set()

        for trigger, categories in keywords.items():
            if trigger in context_lower:
                relevant_categories.update(categories)

        if not relevant_categories:
            return []

        # Find skills matching any category
        all_skills = self.discover_all_skills()
        recommendations = []

        for skill in all_skills:
            for category in relevant_categories:
                if category in skill["name"].lower() or category in skill["description"].lower():
                    recommendations.append(skill)
                    break

        return recommendations


# Test cases
class TestSkillDiscovery:
    """Test skill discovery mechanisms."""

    @pytest.fixture
    def discovery(self, tmp_path):
        """Create discovery system with sample skills."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        # Create sample skills
        self._create_skill(skills_dir, "python-coding", "Python coding standards and best practices")
        self._create_skill(skills_dir, "security-basics", "Basic security principles and practices")
        self._create_skill(skills_dir, "testing-tdd", "Test-driven development methodology")
        self._create_skill(skills_dir, "api-design", "RESTful API design patterns")

        return SkillDiscovery(skills_dir)

    def _create_skill(self, skills_dir: Path, name: str, description: str):
        """Helper to create sample skill."""
        skill_dir = skills_dir / name
        skill_dir.mkdir()

        content = f"""---
name: {name}
description: {description}
---

# {name.replace("-", " ").title()}

Content here.
"""

        (skill_dir / "SKILL.md").write_text(content)

    def test_discover_all_skills(self, discovery):
        """Test discovering all available skills."""
        skills = discovery.discover_all_skills()

        assert len(skills) == 4
        assert all("name" in skill for skill in skills)
        assert all("description" in skill for skill in skills)

    def test_search_by_keyword(self, discovery):
        """Test searching skills by keyword."""
        results = discovery.search_skills("python")

        assert len(results) > 0
        assert any("python" in skill["name"].lower() for skill in results)

    def test_search_ranking(self, discovery):
        """Test that search results are ranked."""
        results = discovery.search_skills("security")

        assert len(results) > 0
        # Skills with keyword in name should rank higher
        if len(results) > 1:
            assert results[0]["match_score"] >= results[-1]["match_score"]

    def test_find_by_category(self, discovery):
        """Test finding skills by category."""
        results = discovery.find_skills_by_category("testing")

        assert len(results) > 0
        assert any("testing" in skill["name"].lower() for skill in results)

    def test_get_specific_skill(self, discovery):
        """Test getting a specific skill by name."""
        skill = discovery.get_skill_by_name("python-coding")

        assert skill is not None
        assert skill["name"] == "python-coding"

    def test_get_nonexistent_skill(self, discovery):
        """Test getting a skill that doesn't exist."""
        skill = discovery.get_skill_by_name("nonexistent-skill")

        assert skill is None

    def test_skill_caching(self, discovery):
        """Test that skills are cached after first load."""
        # First load
        skill1 = discovery.get_skill_by_name("python-coding")

        # Second load (should come from cache)
        skill2 = discovery.get_skill_by_name("python-coding")

        assert skill1 is skill2  # Same object reference

    def test_recommend_skills(self, discovery):
        """Test skill recommendation based on context."""
        recommendations = discovery.recommend_skills("Building a REST API")

        # Should recommend API and security skills
        assert len(recommendations) > 0
        names = [skill["name"] for skill in recommendations]
        assert any("api" in name or "security" in name for name in names)

    def test_recommend_web_context(self, discovery):
        """Test recommendations for web development context."""
        recommendations = discovery.recommend_skills("Creating a web application")

        assert len(recommendations) > 0

    def test_empty_skills_directory(self, tmp_path):
        """Test discovery in empty directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        discovery = SkillDiscovery(empty_dir)
        skills = discovery.discover_all_skills()

        assert len(skills) == 0

    def test_invalid_skill_format(self, tmp_path):
        """Test handling of invalid skill format."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        # Create skill with invalid frontmatter
        skill_dir = skills_dir / "invalid-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Invalid\n\nNo frontmatter")

        discovery = SkillDiscovery(skills_dir)
        skills = discovery.discover_all_skills()

        # Should skip invalid skills
        assert len(skills) == 0


if __name__ == "__main__":
    # Run discovery analysis
    repo_root = Path(__file__).parent.parent.parent
    skills_dir = repo_root / "docs" / "skills"

    print("\n=== Skill Discovery Analysis ===\n")

    if skills_dir.exists():
        discovery = SkillDiscovery(skills_dir)

        # Discover all skills
        all_skills = discovery.discover_all_skills()

        print(f"Total skills discovered: {len(all_skills)}\n")

        if all_skills:
            print("Available skills:")
            for skill in all_skills:
                print(f"  - {skill['name']}: {skill['description'][:60]}...")

            # Test search
            print("\n=== Search Test: 'security' ===")
            results = discovery.search_skills("security")
            print(f"Found {len(results)} matches:")
            for result in results:
                print(f"  - {result['name']} (score: {result.get('match_score', 0)})")

            # Test recommendations
            print("\n=== Recommendation Test: 'Building an API' ===")
            recommendations = discovery.recommend_skills("Building an API")
            print(f"Recommended {len(recommendations)} skills:")
            for rec in recommendations:
                print(f"  - {rec['name']}")
        else:
            print("No skills found. Skills may not be created yet.")
    else:
        print(f"Skills directory not found: {skills_dir}")
        print("Run pytest to execute unit tests.")
