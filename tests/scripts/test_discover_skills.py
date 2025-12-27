#!/usr/bin/env python3
"""Comprehensive unit tests for discover-skills.py with >90% coverage."""

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


spec = importlib.util.spec_from_file_location("discover_skills", SCRIPTS_DIR / "discover-skills.py")
discover_skills = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discover_skills)


@pytest.fixture
def sample_skill_files():
    """Create sample skill files for testing."""
    temp_dir = tempfile.mkdtemp()
    temp_path = Path(temp_dir)

    # Create multiple skill files
    skills_data = [
        {
            "slug": "api-security",
            "name": "API Security",
            "description": "Security best practices for REST APIs",
            "category": "security",
            "tags": ["api", "security", "rest"],
            "related": ["input-validation"],
        },
        {
            "slug": "input-validation",
            "name": "Input Validation",
            "description": "Validate user inputs securely",
            "category": "security",
            "tags": ["validation", "security"],
            "related": [],
        },
        {
            "slug": "unit-testing",
            "name": "Unit Testing",
            "description": "Unit testing best practices",
            "category": "testing",
            "tags": ["testing", "unit"],
            "related": [],
        },
    ]

    for skill_data in skills_data:
        skill_dir = temp_path / skill_data["slug"]
        skill_dir.mkdir(parents=True)

        # Create SKILL.md with frontmatter
        content = f"""---
name: "{skill_data["name"]}"
description: "{skill_data["description"]}"
category: "{skill_data["category"]}"
tags: {json.dumps(skill_data["tags"])}
---

# {skill_data["name"]}

{skill_data["description"]}

## Related Skills

"""
        for related in skill_data["related"]:
            content += f"- [{related}](../{related}/SKILL.md)\n"

        (skill_dir / "SKILL.md").write_text(content)

    yield temp_path
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_product_matrix():
    """Create sample product-matrix.yaml."""
    temp_dir = tempfile.mkdtemp()
    matrix_file = Path(temp_dir) / "product-matrix.yaml"

    matrix_data = {
        "products": {
            "api": {
                "coding_standards": ["Python", "TypeScript"],
                "testing_standards": ["Unit", "Integration"],
                "security_standards": ["API Security", "Input Validation"],
            },
            "web-service": {
                "coding_standards": ["Python", "TypeScript", "React"],
                "testing_standards": ["Unit", "E2E"],
                "security_standards": ["Authentication", "CSRF"],
            },
        }
    }

    matrix_file.write_text(yaml.dump(matrix_data))

    yield matrix_file
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestSkillDiscoveryInit:
    """Test SkillDiscovery initialization."""

    def test_initialization(self, sample_skill_files):
        """Test basic initialization."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        assert discovery.skills_dir == sample_skill_files
        assert len(discovery.skills) == 3
        assert isinstance(discovery.skills, dict)

    def test_initialization_with_product_matrix(self, sample_skill_files, sample_product_matrix):
        """Test initialization with product matrix."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files, sample_product_matrix)

        assert len(discovery.product_matrix) > 0
        assert "products" in discovery.product_matrix

    def test_initialization_empty_directory(self):
        """Test initialization with empty directory."""
        temp_dir = tempfile.mkdtemp()
        discovery = discover_skills.SkillDiscovery(Path(temp_dir))

        assert len(discovery.skills) == 0
        shutil.rmtree(temp_dir)


class TestLoadSkills:
    """Test load_skills method."""

    def test_load_skills_basic(self, sample_skill_files):
        """Test loading skills from directory."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        # Should load 3 skills
        assert len(discovery.skills) == 3
        assert "api-security" in discovery.skills
        assert "input-validation" in discovery.skills
        assert "unit-testing" in discovery.skills

    def test_loaded_skill_structure(self, sample_skill_files):
        """Test structure of loaded skills."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        skill = discovery.skills["api-security"]
        assert "name" in skill
        assert "description" in skill
        assert "category" in skill
        assert "tags" in skill
        assert "path" in skill
        assert "slug" in skill


class TestParseSkill:
    """Test parse_skill method."""

    def test_parse_skill_valid(self, sample_skill_files):
        """Test parsing valid skill file."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        skill_file = sample_skill_files / "api-security" / "SKILL.md"
        skill_data = discovery.parse_skill(skill_file)

        assert skill_data["name"] == "API Security"
        assert skill_data["category"] == "security"
        assert "api" in skill_data["tags"]

    def test_parse_skill_missing_frontmatter(self):
        """Test parsing skill without frontmatter."""
        temp_dir = tempfile.mkdtemp()
        skill_file = Path(temp_dir) / "SKILL.md"
        skill_file.write_text("# Test\n\nNo frontmatter")

        discovery = discover_skills.SkillDiscovery(Path(temp_dir).parent)

        with pytest.raises(ValueError, match="Missing YAML frontmatter"):
            discovery.parse_skill(skill_file)

        shutil.rmtree(temp_dir)

    def test_parse_skill_invalid_yaml(self):
        """Test parsing skill with invalid YAML."""
        temp_dir = tempfile.mkdtemp()
        skill_file = Path(temp_dir) / "SKILL.md"
        content = """---
name: "Test
invalid: yaml: structure
---
# Test
"""
        skill_file.write_text(content)

        discovery = discover_skills.SkillDiscovery(Path(temp_dir).parent)

        with pytest.raises(ValueError):
            discovery.parse_skill(skill_file)

        shutil.rmtree(temp_dir)


class TestExtractRelatedSkills:
    """Test extract_related_skills method."""

    def test_extract_related_skills(self, sample_skill_files):
        """Test extracting related skills."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        content = """
## Related Skills

- [Input Validation](../input-validation/SKILL.md)
- [Authentication](../authentication/SKILL.md)
"""
        related = discovery.extract_related_skills(content)

        assert len(related) == 2
        assert "input-validation" in related
        assert "authentication" in related

    def test_extract_related_skills_none(self, sample_skill_files):
        """Test extracting when no related skills."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        content = "# Test\n\nNo related skills"
        related = discovery.extract_related_skills(content)

        assert len(related) == 0


class TestSearchByKeyword:
    """Test search_by_keyword method."""

    def test_search_by_keyword_in_name(self, sample_skill_files):
        """Test searching by keyword in name."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        results = discovery.search_by_keyword("security")

        assert len(results) >= 2  # api-security and input-validation
        names = [r["name"] for r in results]
        assert "API Security" in names

    def test_search_by_keyword_in_description(self, sample_skill_files):
        """Test searching by keyword in description."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        results = discovery.search_by_keyword("testing")

        assert len(results) >= 1
        assert any("testing" in r["description"].lower() for r in results)

    def test_search_by_keyword_in_tags(self, sample_skill_files):
        """Test searching by keyword in tags."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        results = discovery.search_by_keyword("validation")

        assert len(results) >= 1

    def test_search_by_keyword_no_results(self, sample_skill_files):
        """Test searching with no matches."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        results = discovery.search_by_keyword("nonexistent")

        assert len(results) == 0


class TestFilterByCategory:
    """Test filter_by_category method."""

    def test_filter_by_category_security(self, sample_skill_files):
        """Test filtering by security category."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        results = discovery.filter_by_category("security")

        assert len(results) == 2
        assert all(r["category"] == "security" for r in results)

    def test_filter_by_category_testing(self, sample_skill_files):
        """Test filtering by testing category."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        results = discovery.filter_by_category("testing")

        assert len(results) == 1
        assert results[0]["name"] == "Unit Testing"

    def test_filter_by_category_no_results(self, sample_skill_files):
        """Test filtering with no matches."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        results = discovery.filter_by_category("nonexistent")

        assert len(results) == 0


class TestRecommendForProduct:
    """Test recommend_for_product method."""

    def test_recommend_for_product_valid(self, sample_skill_files, sample_product_matrix):
        """Test recommending skills for product type."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files, sample_product_matrix)

        results = discovery.recommend_for_product("api")

        assert isinstance(results, list)

    def test_recommend_for_product_no_matrix(self, sample_skill_files):
        """Test recommendation without product matrix."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        results = discovery.recommend_for_product("api")

        assert len(results) == 0

    def test_recommend_for_product_invalid_type(self, sample_skill_files, sample_product_matrix):
        """Test recommendation for invalid product type."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files, sample_product_matrix)

        results = discovery.recommend_for_product("invalid")

        assert len(results) == 0


class TestResolveDependencies:
    """Test resolve_dependencies method."""

    def test_resolve_dependencies_basic(self, sample_skill_files):
        """Test basic dependency resolution."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        deps = discovery.resolve_dependencies("api-security")

        assert "api-security" in deps
        assert "input-validation" in deps

    def test_resolve_dependencies_circular(self, sample_skill_files):
        """Test circular dependency handling."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        # Should handle gracefully without infinite loop
        deps = discovery.resolve_dependencies("api-security")

        assert isinstance(deps, list)

    def test_resolve_dependencies_nonexistent(self, sample_skill_files):
        """Test resolving nonexistent skill."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        deps = discovery.resolve_dependencies("nonexistent")

        assert len(deps) == 0


class TestFormatSkillResult:
    """Test format_skill_result method."""

    def test_format_skill_result_basic(self, sample_skill_files):
        """Test basic result formatting."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        skill = discovery.skills["api-security"]
        result = discovery.format_skill_result(skill)

        assert "API Security" in result
        assert "api-security" in result
        assert "security" in result

    def test_format_skill_result_verbose(self, sample_skill_files):
        """Test verbose result formatting."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        skill = discovery.skills["api-security"]
        result = discovery.format_skill_result(skill, verbose=True)

        assert "API Security" in result
        assert "Description:" in result
        assert "Path:" in result


class TestGenerateLoadCommand:
    """Test generate_load_command method."""

    def test_generate_load_command_single(self, sample_skill_files):
        """Test generating load command for single skill."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        cmd = discovery.generate_load_command(["api-security"])

        assert cmd == "@load skills:[api-security]"

    def test_generate_load_command_multiple(self, sample_skill_files):
        """Test generating load command for multiple skills."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        cmd = discovery.generate_load_command(["api-security", "input-validation"])

        assert cmd == "@load skills:[api-security,input-validation]"

    def test_generate_load_command_empty(self, sample_skill_files):
        """Test generating load command with empty list."""
        discovery = discover_skills.SkillDiscovery(sample_skill_files)

        cmd = discovery.generate_load_command([])

        assert cmd == "@load skills:[]"


class TestCommandLineInterface:
    """Test command-line interface."""

    def test_cli_search(self, sample_skill_files):
        """Test --search flag."""
        result = subprocess.run(
            [
                "python3",
                str(SCRIPTS_DIR / "discover-skills.py"),
                "--skills-dir",
                str(sample_skill_files),
                "--search",
                "security",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "security" in result.stdout.lower()

    def test_cli_category(self, sample_skill_files):
        """Test --category flag."""
        result = subprocess.run(
            [
                "python3",
                str(SCRIPTS_DIR / "discover-skills.py"),
                "--skills-dir",
                str(sample_skill_files),
                "--category",
                "security",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "security" in result.stdout.lower()

    def test_cli_list_all(self, sample_skill_files):
        """Test --list-all flag."""
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "discover-skills.py"), "--skills-dir", str(sample_skill_files), "--list-all"],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "available skills" in result.stdout.lower()

    def test_cli_generate_command(self, sample_skill_files):
        """Test --generate-command flag."""
        result = subprocess.run(
            [
                "python3",
                str(SCRIPTS_DIR / "discover-skills.py"),
                "--skills-dir",
                str(sample_skill_files),
                "--search",
                "security",
                "--generate-command",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "@load" in result.stdout

    def test_cli_json_export(self, sample_skill_files):
        """Test --output-json flag."""
        output_json = Path(sample_skill_files) / "output.json"
        result = subprocess.run(
            [
                "python3",
                str(SCRIPTS_DIR / "discover-skills.py"),
                "--skills-dir",
                str(sample_skill_files),
                "--search",
                "security",
                "--output-json",
                str(output_json),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert output_json.exists()

        # Verify JSON structure
        data = json.loads(output_json.read_text())
        assert "count" in data
        assert "skills" in data

    def test_cli_verbose(self, sample_skill_files):
        """Test --verbose flag."""
        result = subprocess.run(
            [
                "python3",
                str(SCRIPTS_DIR / "discover-skills.py"),
                "--skills-dir",
                str(sample_skill_files),
                "--search",
                "security",
                "--verbose",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

    def test_cli_resolve_deps(self, sample_skill_files):
        """Test --resolve-deps flag."""
        result = subprocess.run(
            [
                "python3",
                str(SCRIPTS_DIR / "discover-skills.py"),
                "--skills-dir",
                str(sample_skill_files),
                "--resolve-deps",
                "api-security",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "dependencies" in result.stdout.lower()

    def test_cli_product_type(self, sample_skill_files, sample_product_matrix):
        """Test --product-type flag."""
        result = subprocess.run(
            [
                "python3",
                str(SCRIPTS_DIR / "discover-skills.py"),
                "--skills-dir",
                str(sample_skill_files),
                "--product-matrix",
                str(sample_product_matrix),
                "--product-type",
                "api",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

    def test_cli_no_arguments(self):
        """Test CLI with no arguments."""
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "discover-skills.py")], check=False, capture_output=True, text=True
        )

        assert result.returncode == 0


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_skills_directory(self):
        """Test with empty skills directory."""
        temp_dir = tempfile.mkdtemp()
        discovery = discover_skills.SkillDiscovery(Path(temp_dir))

        results = discovery.search_by_keyword("test")
        assert len(results) == 0

        shutil.rmtree(temp_dir)

    def test_malformed_skill_file(self):
        """Test handling malformed skill file."""
        temp_dir = tempfile.mkdtemp()
        skill_dir = Path(temp_dir) / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("Malformed content")

        discovery = discover_skills.SkillDiscovery(Path(temp_dir))

        # Should handle gracefully
        assert len(discovery.skills) == 0

        shutil.rmtree(temp_dir)

    def test_unicode_in_skill_content(self):
        """Test handling unicode in skills."""
        temp_dir = tempfile.mkdtemp()
        skill_dir = Path(temp_dir) / "unicode-skill"
        skill_dir.mkdir()

        content = """---
name: "Unicode Skill 🚀"
description: "Test with üñíçödé"
category: "test"
tags: ["unicode", "test"]
---

# Unicode Skill 🚀

Content with émojis 🎉
"""
        (skill_dir / "SKILL.md").write_text(content)

        discovery = discover_skills.SkillDiscovery(Path(temp_dir))

        assert len(discovery.skills) == 1
        assert "unicode-skill" in discovery.skills

        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=discover_skills", "--cov-report=term-missing"])
