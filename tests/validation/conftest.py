"""
Pytest configuration for validation tests.

Provides fixtures and test utilities for comprehensive validation.
Aligns with audit-rules.yaml exclusion patterns.
"""

import json
import re
import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Get repository root directory."""
    return Path(__file__).parent.parent.parent


@pytest.fixture(scope="session")
def docs_dir(repo_root: Path) -> Path:
    """Get docs directory."""
    return repo_root / "docs"


@pytest.fixture(scope="session")
def skills_dir(repo_root: Path) -> Path:
    """Get skills directory."""
    return repo_root / "skills"


@pytest.fixture(scope="session")
def examples_dir(repo_root: Path) -> Path:
    """Get examples directory."""
    return repo_root / "examples"


@pytest.fixture(scope="session")
def config_dir(repo_root: Path) -> Path:
    """Get config directory."""
    return repo_root / "config"


@pytest.fixture(scope="session")
def product_matrix(config_dir: Path) -> dict[str, Any]:
    """Load product matrix configuration."""
    matrix_file = config_dir / "product-matrix.yaml"
    with open(matrix_file) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def audit_rules(config_dir: Path) -> dict[str, Any]:
    """Load audit rules configuration."""
    rules_file = config_dir / "audit-rules.yaml"
    with open(rules_file) as f:
        return yaml.safe_load(f)


def should_exclude_file(file_path: Path, repo_root: Path, exclusion_patterns: list[str]) -> bool:
    """Check if a file should be excluded based on audit rules patterns.

    Args:
        file_path: Absolute path to the file
        repo_root: Repository root path
        exclusion_patterns: List of glob patterns from audit-rules.yaml

    Returns:
        True if file should be excluded, False otherwise
    """
    try:
        rel_path = file_path.relative_to(repo_root)
    except ValueError:
        return False  # Not within repo

    rel_path_str = str(rel_path)

    for pattern in exclusion_patterns:
        # Handle different pattern types
        if pattern.endswith("/**"):
            # Directory and all subdirectories
            prefix = pattern[:-3]
            if rel_path_str.startswith(prefix + "/") or rel_path_str == prefix:
                return True
        elif "**/" in pattern:
            # All levels pattern (e.g., **/__pycache__/**)
            middle_part = pattern.replace("**/", "").replace("/**", "")
            if middle_part in rel_path.parts:
                return True
        elif pattern.endswith("/*"):
            # Direct children only
            prefix = pattern[:-2]
            if rel_path.parent == repo_root / prefix:
                return True
        elif "**" in pattern:
            # Glob pattern with wildcard
            from pathlib import PurePath

            if PurePath(rel_path_str).match(pattern):
                return True
        # Exact match or prefix match
        elif rel_path_str == pattern or rel_path_str.startswith(pattern + "/"):
            return True

    return False


@pytest.fixture(scope="session")
def all_markdown_files(repo_root: Path, audit_rules: dict[str, Any]) -> list[Path]:
    """Get all markdown files in repository, excluding patterns from audit-rules.yaml."""
    # Combine exclusion patterns from different sections
    exclusion_patterns = []

    # Link check exclusions
    if "link_check" in audit_rules and "exclude_files" in audit_rules["link_check"]:
        exclusion_patterns.extend(audit_rules["link_check"]["exclude_files"])

    # Orphan exclusions (these should also be excluded from general validation)
    if "orphans" in audit_rules and "exclude" in audit_rules["orphans"]:
        exclusion_patterns.extend(audit_rules["orphans"]["exclude"])

    markdown_files = []
    for md_file in repo_root.rglob("*.md"):
        if not should_exclude_file(md_file, repo_root, exclusion_patterns):
            markdown_files.append(md_file)

    return markdown_files


@pytest.fixture(scope="session")
def all_skill_files(skills_dir: Path) -> list[Path]:
    """Get all SKILL.md files."""
    return list(skills_dir.rglob("SKILL.md"))


class SkillFile:
    """Represents a skill file for testing."""

    def __init__(self, path: Path, name: str, content: str, frontmatter: dict | None):
        self.path = path
        self.name = name
        self.content = content
        self.frontmatter = frontmatter


def pytest_generate_tests(metafunc):
    """Generate parametrized tests for all skills."""
    if "skill_file" in metafunc.fixturenames:
        repo_root = Path(__file__).parent.parent.parent
        skills_dir = repo_root / "skills"

        if not skills_dir.exists():
            return

        skill_files = []
        for skill_md in sorted(skills_dir.rglob("SKILL.md")):
            with open(skill_md, encoding="utf-8") as f:
                content = f.read()

            # Extract frontmatter
            frontmatter = None
            frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
            if frontmatter_match:
                try:
                    frontmatter = yaml.safe_load(frontmatter_match.group(1))
                except yaml.YAMLError:
                    frontmatter = None

            # Get skill name from directory path
            skill_name = skill_md.parent.name

            skill_files.append(
                SkillFile(
                    path=skill_md,
                    name=skill_name,
                    content=content,
                    frontmatter=frontmatter,
                )
            )

        metafunc.parametrize(
            "skill_file",
            skill_files,
            ids=[f.name for f in skill_files],
        )


@pytest.fixture
def token_estimator():
    """Token estimation function (rough: ~4 chars per token)."""

    def estimate(text: str) -> int:
        return len(text) // 4

    return estimate


@pytest.fixture
def skills_root(skills_dir: Path) -> Path:
    """Get skills root directory (alias for skills_dir)."""
    return skills_dir


@pytest.fixture
def run_command():
    """Fixture to run shell commands."""

    def _run(cmd: list[str], cwd: Path = None, check: bool = True) -> subprocess.CompletedProcess:
        """Run a command and return result."""
        return subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)

    return _run


@pytest.fixture(scope="session")
def quality_gates() -> dict[str, Any]:
    """Define quality gates for validation."""
    return {
        "documentation_accuracy": 100,  # 100% accuracy required
        "example_functionality": 100,  # 100% examples must work
        "skills_compliance": 100,  # 100% skills must comply
        "agent_specifications": 95,  # 95% agent specs must be valid
        "integration_workflows": 90,  # 90% workflows must pass
        "code_coverage": 80,  # 80% code coverage
        "link_validity": 100,  # 100% links must be valid
        "yaml_validity": 100,  # 100% YAML must be valid
    }


@pytest.fixture
def validate_yaml():
    """Fixture to validate YAML files."""

    def _validate(file_path: Path) -> tuple[bool, str]:
        """Validate YAML file syntax."""
        try:
            with open(file_path) as f:
                yaml.safe_load(f)
            return True, "Valid"
        except yaml.YAMLError as e:
            return False, str(e)

    return _validate


@pytest.fixture
def validate_json():
    """Fixture to validate JSON files."""

    def _validate(file_path: Path) -> tuple[bool, str]:
        """Validate JSON file syntax."""
        try:
            with open(file_path) as f:
                json.load(f)
            return True, "Valid"
        except json.JSONDecodeError as e:
            return False, str(e)

    return _validate


@pytest.fixture
def check_file_size():
    """Fixture to check file size limits."""

    def _check(file_path: Path, max_lines: int = 500) -> tuple[bool, int]:
        """Check if file exceeds line limit."""
        with open(file_path) as f:
            lines = sum(1 for _ in f)
        return lines <= max_lines, lines

    return _check


@pytest.fixture
def extract_code_blocks():
    """Fixture to extract code blocks from markdown."""

    def _extract(md_file: Path) -> list[dict[str, str]]:
        """Extract fenced code blocks from markdown file."""
        code_blocks = []
        with open(md_file) as f:
            content = f.read()

        in_code_block = False
        current_block = []
        language = ""

        for line in content.split("\n"):
            if line.startswith("```"):
                if in_code_block:
                    # End of code block
                    code_blocks.append({"language": language, "code": "\n".join(current_block)})
                    current_block = []
                    in_code_block = False
                else:
                    # Start of code block
                    language = line[3:].strip()
                    in_code_block = True
            elif in_code_block:
                current_block.append(line)

        return code_blocks

    return _extract


@pytest.fixture(scope="session")
def excluded_dirs() -> set:
    """Get list of excluded directories (deprecated - use audit_rules instead)."""
    return {
        ".git",
        ".claude",
        "subagents",
        "memory",
        "prompts",
        "reports/generated",
        ".vscode",
        "node_modules",
        "__pycache__",
        ".github",
        ".hive-mind",
        ".swarm",
        ".claude-flow",
    }


@pytest.fixture(scope="session")
def exclusion_helper(repo_root: Path, audit_rules: dict[str, Any]):
    """Helper for checking if files should be excluded based on audit rules."""

    def _should_exclude(file_path: Path) -> bool:
        """Check if file should be excluded."""
        exclusion_patterns = []
        if "link_check" in audit_rules and "exclude_files" in audit_rules["link_check"]:
            exclusion_patterns.extend(audit_rules["link_check"]["exclude_files"])
        if "orphans" in audit_rules and "exclude" in audit_rules["orphans"]:
            exclusion_patterns.extend(audit_rules["orphans"]["exclude"])
        return should_exclude_file(file_path, repo_root, exclusion_patterns)

    return _should_exclude
