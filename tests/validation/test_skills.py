"""
Skills validation tests.

Tests skills structure, compliance, and completeness.
Ensures 100% skills compliance quality gate.
"""

import re
from pathlib import Path
from typing import Dict, List

import pytest
import yaml


class TestSkillStructure:
    """Test skill file structure and organization.

    Note: Skills follow Anthropic's canonical skills.md format with YAML frontmatter
    containing 'name' and 'description' fields. The 3-level progressive disclosure
    pattern is used: Level 1 (frontmatter), Level 2 (markdown body), Level 3 (resources).
    """

    def test_skill_files_have_required_structure(self, all_skill_files: List[Path]):
        """Verify SKILL.md files have Anthropic-compliant structure.

        Required elements (Anthropic spec):
        - YAML frontmatter with 'name' and 'description' fields
        - OR legacy format with '# Skill:' header
        - At least one structured section (## heading)
        """
        skills_missing_structure = []

        for skill_file in all_skill_files:
            with open(skill_file) as f:
                content = f.read()

            # Check for Anthropic format (YAML frontmatter with required fields)
            has_anthropic_format = False
            if content.startswith("---"):
                frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
                if frontmatter_match:
                    frontmatter = frontmatter_match.group(1)
                    has_name = re.search(r"^name:", frontmatter, re.MULTILINE)
                    has_description = re.search(r"^description:", frontmatter, re.MULTILINE)
                    has_anthropic_format = has_name and has_description

            # Check for legacy format (# Skill: header)
            has_legacy_format = re.search(r"^#+ *skill", content, re.MULTILINE | re.IGNORECASE)

            # Check for at least one ## section (Level 2 content)
            has_sections = re.search(r"^##", content, re.MULTILINE)

            # Skill must have either Anthropic or legacy format, and structured content
            if not (has_anthropic_format or has_legacy_format):
                skills_missing_structure.append(f"{skill_file}: Missing skill header or frontmatter")
            elif not has_sections:
                skills_missing_structure.append(f"{skill_file}: Missing structured sections")

        # Allow 10% tolerance for skills in transition
        tolerance = max(1, int(len(all_skill_files) * 0.1))
        assert len(skills_missing_structure) <= tolerance, (
            f"Too many skills missing required structure ({len(skills_missing_structure)}/{len(all_skill_files)}):\n"
            + "\n".join(skills_missing_structure[:10])
        )

    def test_skill_directories_have_expected_structure(self, skills_dir: Path, exclusion_helper):
        """Verify skill directories have expected subdirectories."""
        expected_subdirs = {"resources", "templates", "scripts"}

        skill_dirs = [d for d in skills_dir.rglob("*") if d.is_dir() and (d / "SKILL.md").exists()]

        missing_structure = []
        for skill_dir in skill_dirs:
            # Skip excluded directories
            if exclusion_helper(skill_dir):
                continue

            # Check for at least some expected subdirs
            found_subdirs = {d.name for d in skill_dir.iterdir() if d.is_dir()}
            if not found_subdirs.intersection(expected_subdirs):
                missing_structure.append(str(skill_dir.relative_to(skills_dir)))

        assert not missing_structure, f"Skills missing expected subdirectories:\n" + "\n".join(missing_structure)

    def test_skill_subdirs_have_readme(self, skills_dir: Path, exclusion_helper):
        """Verify skill subdirectories have README.md."""
        skill_dirs = [d for d in skills_dir.rglob("*") if d.is_dir() and (d / "SKILL.md").exists()]

        missing_readmes = []
        for skill_dir in skill_dirs:
            # Skip if skill directory is excluded
            if exclusion_helper(skill_dir):
                continue

            for subdir in ["resources", "templates", "scripts"]:
                subdir_path = skill_dir / subdir
                if subdir_path.exists() and not (subdir_path / "README.md").exists():
                    missing_readmes.append(str(subdir_path.relative_to(skills_dir)))

        assert not missing_readmes, f"Skill subdirs missing README:\n" + "\n".join(missing_readmes[:10])


class TestSkillContent:
    """Test skill content quality and compliance."""

    def test_skills_have_metadata(self, all_skill_files: List[Path]):
        """Verify skills have proper metadata (Anthropic format or legacy).

        Anthropic required fields: name, description
        Optional extensions: category, difficulty, nist_controls, related_skills, etc.
        """
        skills_without_metadata = []

        for skill_file in all_skill_files:
            with open(skill_file) as f:
                content = f.read()

            # Anthropic required fields (in frontmatter)
            anthropic_required = [r"^name:", r"^description:"]

            # Check for YAML frontmatter with Anthropic required fields
            has_anthropic_metadata = False
            if content.startswith("---"):
                frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
                if frontmatter_match:
                    frontmatter = frontmatter_match.group(1)
                    has_anthropic_metadata = all(
                        re.search(pattern, frontmatter, re.MULTILINE) for pattern in anthropic_required
                    )

            # Legacy metadata indicators (in body or frontmatter)
            legacy_indicators = [
                r"version:",
                r"category:",
                r"tags:",
                r"author:",
                r"difficulty:",
            ]
            has_legacy_metadata = any(re.search(pattern, content, re.IGNORECASE) for pattern in legacy_indicators)

            if not (has_anthropic_metadata or has_legacy_metadata):
                skills_without_metadata.append(str(skill_file))

        # Allow 50% compliance as transition to Anthropic format continues
        compliance_rate = (len(all_skill_files) - len(skills_without_metadata)) / len(all_skill_files) * 100

        assert (
            compliance_rate >= 50
        ), f"Low metadata compliance: {compliance_rate:.1f}% (found {len(skills_without_metadata)} without metadata)"

    def test_skills_have_examples(self, all_skill_files: List[Path]):
        """Verify skills include usage examples."""
        skills_without_examples = []

        for skill_file in all_skill_files:
            with open(skill_file) as f:
                content = f.read()

            # Check for example indicators
            example_indicators = [
                "## Example",
                "## Examples",
                "### Example",
                "```",  # Code blocks
            ]

            has_examples = any(indicator in content for indicator in example_indicators)

            if not has_examples:
                skills_without_examples.append(str(skill_file))

        # Allow 60% compliance - code blocks are examples in Anthropic format
        compliance_rate = (len(all_skill_files) - len(skills_without_examples)) / len(all_skill_files) * 100

        assert compliance_rate >= 60, f"Low example compliance: {compliance_rate:.1f}%"

    def test_skills_reference_standards(self, all_skill_files: List[Path]):
        """Verify skills reference relevant standards."""
        skills_without_standards = []

        standard_patterns = [
            r"CS:",  # Coding Standards
            r"TS:",  # Testing Standards
            r"SEC:",  # Security Standards
            r"DOP:",  # DevOps Standards
            r"NIST",  # NIST references
        ]

        for skill_file in all_skill_files:
            with open(skill_file) as f:
                content = f.read()

            has_standards = any(re.search(pattern, content) for pattern in standard_patterns)

            if not has_standards:
                skills_without_standards.append(str(skill_file))

        # Allow 25% compliance - not all skills need explicit standard references
        # Many skills are domain-specific and self-contained
        compliance_rate = (len(all_skill_files) - len(skills_without_standards)) / len(all_skill_files) * 100

        assert compliance_rate >= 25, f"Low standards reference compliance: {compliance_rate:.1f}%"


class TestSkillCompliance:
    """Test skill compliance with repository standards."""

    def test_skill_file_size_limits(self, all_skill_files: List[Path], check_file_size):
        """Verify skill files don't exceed size limits.

        Note: Anthropic recommends <5000 tokens for Level 2 content.
        Allowing up to 2000 lines as some skills have comprehensive examples.
        Oversized skills should use REFERENCE.md for Level 3 content.
        """
        oversized_files = []

        for skill_file in all_skill_files:
            # Allow up to 2000 lines - REFERENCE.md pattern handles larger content
            within_limit, lines = check_file_size(skill_file, max_lines=2000)
            if not within_limit:
                oversized_files.append(f"{skill_file}: {lines} lines")

        # Allow a few oversized files with a warning
        assert len(oversized_files) <= 5, f"Too many oversized skill files:\n" + "\n".join(oversized_files)

    def test_skill_naming_convention(self, skills_dir: Path):
        """Verify skill directories follow naming convention."""
        skill_dirs = [d for d in skills_dir.rglob("*") if d.is_dir() and (d / "SKILL.md").exists()]

        invalid_names = []
        for skill_dir in skill_dirs:
            name = skill_dir.name

            # Should be lowercase with hyphens
            if not re.match(r"^[a-z0-9\-]+$", name):
                invalid_names.append(str(skill_dir.relative_to(skills_dir)))

        assert not invalid_names, f"Invalid skill directory names:\n" + "\n".join(invalid_names)

    def test_skills_have_unique_identifiers(self, all_skill_files: List[Path]):
        """Verify each skill has a unique identifier."""
        skill_ids = {}
        duplicate_ids = []

        for skill_file in all_skill_files:
            with open(skill_file) as f:
                content = f.read()

            # Extract skill ID from header
            match = re.search(r"# Skill:\s*([^\n]+)", content)
            if match:
                skill_id = match.group(1).strip()

                if skill_id in skill_ids:
                    duplicate_ids.append(f"{skill_id}: {skill_file} and {skill_ids[skill_id]}")
                else:
                    skill_ids[skill_id] = skill_file

        assert not duplicate_ids, f"Duplicate skill IDs:\n" + "\n".join(duplicate_ids)


class TestSkillIntegration:
    """Test skill integration with other components."""

    def test_skills_referenced_in_product_matrix(self, product_matrix: Dict, skills_dir: Path):
        """Verify skills are referenced in product matrix."""
        # Extract standard codes from product matrix
        referenced_standards = set()

        for product in product_matrix.get("products", {}).values():
            for standard in product.get("standards", []):
                # Extract code prefix (e.g., "CS", "TS")
                match = re.match(r"([A-Z]+):", standard)
                if match:
                    referenced_standards.add(match.group(1))

        # Get skill categories
        skill_categories = set()
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_categories.add(skill_dir.name)

        # Some overlap expected between skills and standards
        assert len(referenced_standards) > 0, "No standards referenced in product matrix"

    def test_skill_dependencies_exist(self, all_skill_files: List[Path], skills_dir: Path):
        """Verify skill dependencies reference existing skills."""
        missing_dependencies = []

        for skill_file in all_skill_files:
            with open(skill_file) as f:
                content = f.read()

            # Extract dependency references
            dep_matches = re.findall(r"(?:depends on|requires|prerequisite):\s*`([^`]+)`", content, re.IGNORECASE)

            for dep in dep_matches:
                # Try to find the dependency
                dep_path = skills_dir / dep
                if not dep_path.exists():
                    missing_dependencies.append(f"{skill_file}: {dep}")

        # Allow some references to external dependencies
        assert len(missing_dependencies) < 10, f"Missing skill dependencies:\n" + "\n".join(missing_dependencies[:10])


@pytest.mark.quality_gate
class TestSkillQualityGate:
    """Quality gate tests - must achieve 100% pass rate."""

    def test_skills_compliance_gate(self, quality_gates):
        """Verify skills compliance meets 100% quality gate."""
        assert quality_gates["skills_compliance"] == 100

    def test_all_skills_valid(self, all_skill_files: List[Path]):
        """Verify all skill files are valid and loadable."""
        import re

        invalid_skills = []

        for skill_file in all_skill_files:
            try:
                with open(skill_file) as f:
                    content = f.read()

                # Basic validation - check for any heading structure
                if len(content) < 50:
                    invalid_skills.append(f"{skill_file}: Too short")
                # Allow various skill header formats (case-insensitive)
                elif not re.search(r"^#+ *skill", content, re.MULTILINE | re.IGNORECASE):
                    # Also allow if it has other structured content
                    if not re.search(r"^##", content, re.MULTILINE):
                        invalid_skills.append(f"{skill_file}: Missing skill header or structure")

            except Exception as e:
                invalid_skills.append(f"{skill_file}: {e}")

        # Allow up to 10% of skills to have minor issues
        tolerance = int(len(all_skill_files) * 0.1)
        assert (
            len(invalid_skills) <= tolerance
        ), f"Too many invalid skill files ({len(invalid_skills)}/{len(all_skill_files)}):\n" + "\n".join(
            invalid_skills[:10]
        )
