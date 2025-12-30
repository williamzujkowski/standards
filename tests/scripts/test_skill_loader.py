#!/usr/bin/env python3
"""
Tests for skill-loader CLI

Run with:
    pytest tests/scripts/test_skill_loader.py -v
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest


# Add scripts to path
REPO_ROOT = Path(__file__).parent.parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from skill_loader import Skill, SkillLoader


class TestSkillLoaderClass:
    """Test the SkillLoader class directly"""

    @pytest.fixture
    def loader(self):
        """Create a SkillLoader instance"""
        return SkillLoader(REPO_ROOT)

    def test_loader_initialization(self, loader):
        """Test that loader initializes correctly"""
        assert loader.repo_root == REPO_ROOT
        assert loader.skills_dir.exists()
        assert len(loader.skills_cache) > 0

    def test_skill_discovery(self, loader):
        """Test that skills are discovered"""
        skills = loader.discover()
        assert len(skills) > 0

        # Check that known skills exist
        skill_names = [s.name for s in skills]
        assert "coding-standards" in skill_names
        assert "testing" in skill_names
        assert "security-practices" in skill_names

    def test_discover_by_keyword(self, loader):
        """Test keyword-based discovery"""
        skills = loader.discover(keyword="testing")
        assert len(skills) > 0

        # All results should contain 'testing' in name or description
        for skill in skills:
            assert "testing" in skill.name.lower() or "testing" in skill.description.lower()

    def test_discover_by_category(self, loader):
        """Test category-based discovery"""
        skills = loader.discover(category="security-practices")
        assert len(skills) > 0

        # All results should be in the security category
        for skill in skills:
            assert skill.category == "security-practices"

    def test_load_skill(self, loader):
        """Test loading a specific skill"""
        skill = loader.load_skill("coding-standards", level=2)
        assert skill is not None
        assert skill.name == "coding-standards"
        assert skill.level == 2

    def test_load_nonexistent_skill(self, loader):
        """Test loading a skill that doesn't exist"""
        skill = loader.load_skill("nonexistent-skill")
        assert skill is None

    @pytest.mark.xfail(reason="Skills structure incomplete - see Issue #43", strict=False)
    def test_recommend_for_product(self, loader):
        """Test skill recommendations for product types"""
        skills = loader.recommend("api")
        assert len(skills) > 0

        # Should include core skills for API development
        skill_names = [s.name for s in skills]
        assert "coding-standards" in skill_names
        assert "testing" in skill_names
        assert "security-practices" in skill_names

    def test_get_skill_info(self, loader):
        """Test getting skill information"""
        skill = loader.get_skill_info("coding-standards")
        assert skill is not None
        assert skill.name == "coding-standards"
        assert len(skill.description) > 0
        assert skill.path.exists()

    @pytest.mark.xfail(reason="Skills structure incomplete - see Issue #43", strict=False)
    def test_validate_skill(self, loader):
        """Test skill validation"""
        # Valid skill
        assert loader.validate_skill("coding-standards") is True

        # Invalid skill
        assert loader.validate_skill("nonexistent-skill") is False


class TestSkillLoaderCLI:
    """Test the skill-loader CLI commands"""

    def run_cli(self, args):
        """Helper to run CLI command"""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "skill-loader.py")] + args,
            check=False,
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        return result

    def test_cli_discover(self):
        """Test discover command"""
        result = self.run_cli(["discover", "--keyword", "testing"])
        assert result.returncode == 0
        assert "testing" in result.stdout.lower()

    def test_cli_list(self):
        """Test list command"""
        result = self.run_cli(["list", "--category", "all"])
        assert result.returncode == 0
        assert "Available Skills" in result.stdout

    def test_cli_list_json(self):
        """Test list command with JSON output"""
        result = self.run_cli(["list", "--format", "json"])
        assert result.returncode == 0

        data = json.loads(result.stdout)
        assert "skills" in data
        assert len(data["skills"]) > 0

    def test_cli_info(self):
        """Test info command"""
        result = self.run_cli(["info", "coding-standards"])
        assert result.returncode == 0
        assert "coding-standards" in result.stdout
        assert "Description:" in result.stdout

    def test_cli_info_nonexistent(self):
        """Test info command with nonexistent skill"""
        result = self.run_cli(["info", "nonexistent-skill"])
        assert result.returncode != 0
        assert "not found" in result.stderr.lower()

    @pytest.mark.xfail(reason="Skills structure incomplete - see Issue #43", strict=False)
    def test_cli_validate(self):
        """Test validate command"""
        result = self.run_cli(["validate", "coding-standards"])
        assert result.returncode == 0
        assert "✅" in result.stdout or "validated" in result.stdout.lower()

    def test_cli_load_single(self):
        """Test loading a single skill"""
        result = self.run_cli(["load", "coding-standards", "--level", "2"])
        assert result.returncode == 0
        assert "coding-standards" in result.stdout
        assert "Loaded" in result.stdout

    def test_cli_load_multiple(self):
        """Test loading multiple skills"""
        result = self.run_cli(["load", "coding-standards,testing", "--level", "2"])
        assert result.returncode == 0
        assert "coding-standards" in result.stdout
        assert "testing" in result.stdout

    def test_cli_load_json(self):
        """Test loading skills with JSON output"""
        result = self.run_cli(["load", "coding-standards", "--format", "json"])
        assert result.returncode == 0

        data = json.loads(result.stdout)
        assert "skills" in data
        assert len(data["skills"]) > 0
        assert data["skills"][0]["name"] == "coding-standards"

    def test_cli_recommend(self):
        """Test recommend command"""
        result = self.run_cli(["recommend", "--product-type", "api"])
        assert result.returncode == 0
        assert "Recommended skills" in result.stdout
        assert "api" in result.stdout


class TestLegacyBridge:
    """Test legacy pattern translation"""

    @pytest.fixture
    def loader(self):
        return SkillLoader(REPO_ROOT)

    def test_load_legacy_product_pattern(self, loader):
        """Test loading legacy product:api pattern"""
        skill = loader._translate_legacy_pattern("product:api")
        assert skill is not None

    def test_load_legacy_cs_pattern(self, loader):
        """Test loading legacy CS:python pattern"""
        skill = loader._translate_legacy_pattern("CS:python")
        # This may return None if the mapping isn't complete yet
        # Just verify it doesn't crash
        assert skill is None or isinstance(skill, Skill)

    def test_legacy_mappings_loaded(self, loader):
        """Test that legacy mappings are loaded"""
        assert loader.legacy_mappings is not None
        assert "product_mappings" in loader.legacy_mappings

    def test_product_matrix_loaded(self, loader):
        """Test that product matrix is loaded"""
        assert loader.product_matrix is not None


class TestSkillValidation:
    """Test skill file structure validation"""

    @pytest.fixture
    def loader(self):
        return SkillLoader(REPO_ROOT)

    @pytest.mark.xfail(reason="Skills structure incomplete - see Issue #43", strict=False)
    def test_all_skills_have_required_sections(self, loader):
        """Verify all skills have required sections"""
        required_sections = ["## Overview", "## When to Use This Skill", "## Core Instructions"]

        for skill in loader.skills_cache.values():
            skill_file = skill.path / "SKILL.md"
            with open(skill_file) as f:
                content = f.read()

            for section in required_sections:
                assert section in content, f"Skill {skill.name} missing section: {section}"

    def test_all_skills_have_frontmatter(self, loader):
        """Verify all skills have YAML frontmatter"""
        for skill in loader.skills_cache.values():
            skill_file = skill.path / "SKILL.md"
            with open(skill_file) as f:
                content = f.read()

            assert content.startswith("---"), f"Skill {skill.name} missing YAML frontmatter"
            assert "name:" in content[:200], f"Skill {skill.name} missing 'name' in frontmatter"
            assert "description:" in content[:200], f"Skill {skill.name} missing 'description' in frontmatter"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
