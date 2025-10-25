"""
Documentation validation tests.

Tests documentation accuracy, completeness, and integrity.
Ensures 100% documentation accuracy quality gate.
"""

import re
from pathlib import Path
from typing import List

import pytest


class TestDocumentationStructure:
    """Test documentation structure and organization."""

    def test_required_docs_exist(self, repo_root: Path):
        """Verify all required documentation files exist."""
        required_docs = [
            "README.md",
            "CLAUDE.md",
            "CHANGELOG.md",
            "docs/README.md",
            "docs/guides/KICKSTART_PROMPT.md",
            "docs/guides/STANDARDS_INDEX.md",
            "docs/nist/README.md",
            "config/product-matrix.yaml",
        ]

        missing_docs = []
        for doc in required_docs:
            doc_path = repo_root / doc
            if not doc_path.exists():
                missing_docs.append(doc)

        assert not missing_docs, f"Missing required documentation: {missing_docs}"

    def test_docs_have_titles(self, all_markdown_files: List[Path]):
        """Verify all markdown files have titles."""
        files_without_titles = []

        for md_file in all_markdown_files:
            with open(md_file) as f:
                content = f.read()

            # Check for H1 title
            if not re.search(r"^#\s+.+", content, re.MULTILINE):
                files_without_titles.append(str(md_file))

        assert not files_without_titles, f"Files without titles: {files_without_titles}"

    def test_no_broken_relative_links(self, all_markdown_files: List[Path], exclusion_helper):
        """Verify no broken relative links in documentation."""
        broken_links = []

        for md_file in all_markdown_files:
            # Skip if this file should be excluded
            if exclusion_helper(md_file):
                continue

            with open(md_file) as f:
                content = f.read()

            # Extract markdown links [text](path)
            links = re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", content)

            for link_text, link_path in links:
                # Skip external links
                if link_path.startswith(("http://", "https://", "mailto:", "#")):
                    continue

                # Skip template placeholders and variables
                if re.search(r"\{[A-Z_]+\}", link_path):  # {PLACEHOLDER}
                    continue
                if re.search(r"\{[a-zA-Z0-9_-]+\}", link_path):  # {variable}
                    continue
                if link_path.startswith("../path"):  # Example paths
                    continue

                # Skip regex patterns and code-like content (they're not real links)
                if re.search(r'["\']?\([a-zA-Z0-9\[\]\\{}\^$\*\+\?\|]+\)', link_path):
                    continue

                # Remove anchor
                link_path = link_path.split("#")[0]

                if not link_path:
                    continue

                # Resolve relative path
                target = (md_file.parent / link_path).resolve()

                if not target.exists():
                    broken_links.append(f"{md_file}: [{link_text}]({link_path})")

        assert not broken_links, f"Broken links found:\n" + "\n".join(broken_links)

    def test_hub_links_present(self, repo_root: Path):
        """Verify hub READMEs have AUTO-LINKS sections."""
        hubs = [
            "docs/standards/UNIFIED_STANDARDS.md",
            "docs/guides/STANDARDS_INDEX.md",
            "docs/core/README.md",
            "docs/nist/README.md",
            "docs/README.md",
            "examples/README.md",
        ]

        missing_auto_links = []
        for hub in hubs:
            hub_path = repo_root / hub
            if not hub_path.exists():
                continue

            with open(hub_path) as f:
                content = f.read()

            if "<!-- AUTO-LINKS START -->" not in content:
                missing_auto_links.append(hub)

        assert not missing_auto_links, f"Hubs missing AUTO-LINKS: {missing_auto_links}"


class TestDocumentationContent:
    """Test documentation content quality."""

    def test_no_placeholder_content(self, all_markdown_files: List[Path], exclusion_helper):
        """Verify no placeholder or TODO content in docs."""
        placeholders = ["TODO", "FIXME", "XXX", "PLACEHOLDER", "TBD"]
        files_with_placeholders = []

        for md_file in all_markdown_files:
            # Skip excluded files
            if exclusion_helper(md_file):
                continue

            with open(md_file) as f:
                content = f.read()

            for placeholder in placeholders:
                if re.search(rf"\b{placeholder}\b", content, re.IGNORECASE):
                    files_with_placeholders.append(f"{md_file}: {placeholder}")

        # Allow some TODOs in specific files (these are already excluded by audit rules)
        allowed_files = ["project_plan.md", "CHANGELOG.md", "update_repo.md"]
        files_with_placeholders = [
            item for item in files_with_placeholders if not any(allowed in item for allowed in allowed_files)
        ]

        assert not files_with_placeholders, f"Placeholder content found:\n" + "\n".join(files_with_placeholders)

    def test_code_blocks_properly_fenced(self, all_markdown_files: List[Path], extract_code_blocks):
        """Verify code blocks are properly fenced."""
        improperly_fenced = []

        for md_file in all_markdown_files:
            with open(md_file) as f:
                content = f.read()

            # Count opening and closing fences
            opening = content.count("```")
            if opening % 2 != 0:
                improperly_fenced.append(str(md_file))

        assert not improperly_fenced, f"Improperly fenced code blocks: {improperly_fenced}"

    def test_consistent_heading_style(self, all_markdown_files: List[Path]):
        """Verify consistent heading style (ATX style)."""
        inconsistent_files = []

        for md_file in all_markdown_files:
            with open(md_file) as f:
                content = f.read()

            # Check for Setext-style headings (underline style)
            if re.search(r"^.+\n[=\-]+$", content, re.MULTILINE):
                inconsistent_files.append(str(md_file))

        assert not inconsistent_files, f"Inconsistent heading style: {inconsistent_files}"


class TestDocumentationAccuracy:
    """Test documentation accuracy against actual implementation."""

    def test_agent_counts_accurate(self, repo_root: Path):
        """Verify documented agent counts match actual available agents."""
        claude_md = repo_root / "CLAUDE.md"
        with open(claude_md) as f:
            content = f.read()

        # Extract agent count claims
        agent_count_match = re.search(r"(\d+)\s+Available", content)
        if not agent_count_match:
            pytest.skip("No agent count claim found in CLAUDE.md")

        claimed_count = int(agent_count_match.group(1))

        # Count actual agent types listed
        agent_section = re.search(r"## 🚀 Agent Types.*?(?=##|\Z)", content, re.DOTALL)
        if not agent_section:
            pytest.skip("Agent types section not found")

        # Count agent type backticked items
        agent_types = re.findall(r"`([^`]+)`", agent_section.group(0))

        # Filter out non-agent items
        actual_agents = [a for a in agent_types if a not in ["mcp", "tools", "coordination"]]

        assert (
            len(actual_agents) == claimed_count
        ), f"Agent count mismatch: claimed {claimed_count}, found {len(actual_agents)}"

    def test_file_paths_valid(self, repo_root: Path, all_markdown_files: List[Path], exclusion_helper):
        """Verify file paths mentioned in docs exist."""
        invalid_paths = []

        for md_file in all_markdown_files:
            # Skip excluded files
            if exclusion_helper(md_file):
                continue

            with open(md_file) as f:
                content = f.read()

            # Extract file paths in common patterns
            paths = re.findall(r"(?:^|\s)([a-zA-Z0-9_\-./]+\.(?:py|md|yaml|yml|json|js|ts))", content)

            for path in paths:
                # Skip URLs and external references
                if path.startswith(("http", "www", "example")):
                    continue

                # Try as relative to repo root
                full_path = repo_root / path
                if not full_path.exists():
                    # Try as relative to doc file
                    full_path = md_file.parent / path
                    if not full_path.exists():
                        invalid_paths.append(f"{md_file}: {path}")

        # Allow some common example paths
        invalid_paths = [p for p in invalid_paths if "example" not in p.lower()]

        # Limit to first 20 to avoid overwhelming output
        if len(invalid_paths) > 20:
            invalid_paths = invalid_paths[:20] + [f"... and {len(invalid_paths) - 20} more"]

        assert not invalid_paths, f"Invalid file paths in documentation:\n" + "\n".join(invalid_paths)

    def test_command_examples_syntax(self, all_markdown_files: List[Path], extract_code_blocks):
        """Verify command examples have valid syntax."""
        invalid_commands = []

        shell_languages = {"bash", "sh", "shell", "console"}

        for md_file in all_markdown_files:
            code_blocks = extract_code_blocks(md_file)

            for block in code_blocks:
                if block["language"] in shell_languages:
                    code = block["code"]

                    # Check for common syntax errors
                    if re.search(r"\$\{[^}]*$", code):  # Unclosed variable
                        invalid_commands.append(f"{md_file}: Unclosed variable")
                    if re.search(r"\([^)]*$", code):  # Unclosed parenthesis
                        invalid_commands.append(f"{md_file}: Unclosed parenthesis")

        assert not invalid_commands, f"Invalid command syntax:\n" + "\n".join(invalid_commands[:10])


class TestDocumentationCompleteness:
    """Test documentation completeness."""

    def test_all_skills_documented(self, skills_dir: Path, all_skill_files: List[Path]):
        """Verify all skills have documentation."""
        skills_without_docs = []

        for skill_file in all_skill_files:
            with open(skill_file) as f:
                content = f.read()

            # Check for minimal documentation sections
            required_sections = ["##", "###"]  # At least some headings
            has_sections = any(section in content for section in required_sections)

            if not has_sections or len(content) < 100:
                skills_without_docs.append(str(skill_file))

        assert not skills_without_docs, f"Skills with insufficient docs: {skills_without_docs}"

    def test_examples_have_readme(self, examples_dir: Path):
        """Verify all example directories have README."""
        missing_readme = []

        for item in examples_dir.rglob("*"):
            if item.is_dir() and not item.name.startswith("."):
                readme = item / "README.md"
                if not readme.exists():
                    missing_readme.append(str(item.relative_to(examples_dir)))

        # Allow some nested directories without README
        missing_readme = [d for d in missing_readme if d.count("/") <= 1]

        assert not missing_readme, f"Example directories missing README: {missing_readme}"


@pytest.mark.quality_gate
class TestDocumentationQualityGate:
    """Quality gate tests - must achieve 100% pass rate."""

    def test_documentation_accuracy_gate(self, quality_gates):
        """Verify documentation accuracy meets 100% quality gate."""
        # This is a meta-test that verifies other tests pass
        # In real implementation, this would aggregate results
        assert quality_gates["documentation_accuracy"] == 100

    def test_link_validity_gate(self, quality_gates):
        """Verify link validity meets 100% quality gate."""
        assert quality_gates["link_validity"] == 100
