"""Test skills structure compliance.

All 61 skills must have proper structure following progressive disclosure.

TARGET STATE:
- All skills have YAML frontmatter with name and description
- All skills have Level 1: Quick Start section
- All skills have Level 2: Implementation section
- All skills have Level 3: Mastery section
- All skills have Examples section
- All skills have Integration Points section
- All skills have Common Pitfalls section
"""

import re

import pytest


class TestSkillFrontmatter:
    """Test YAML frontmatter compliance."""

    def test_has_yaml_frontmatter(self, skill_file):
        """All skills must have YAML frontmatter."""
        assert skill_file.content.startswith("---\n"), (
            f"Skill '{skill_file.name}' missing YAML frontmatter.\n"
            f"Expected: ---\nname: ...\ndescription: ...\n---\n"
            f"File: {skill_file.path}"
        )

        assert skill_file.frontmatter is not None, (
            f"Skill '{skill_file.name}' has invalid YAML frontmatter.\n" f"File: {skill_file.path}"
        )

    def test_has_name_field(self, skill_file):
        """Frontmatter must have 'name' field."""
        assert skill_file.frontmatter is not None, f"Skill '{skill_file.name}' missing frontmatter"

        assert "name" in skill_file.frontmatter, (
            f"Skill '{skill_file.name}' missing 'name' field in frontmatter.\n"
            f"File: {skill_file.path}\n"
            f"Current frontmatter: {skill_file.frontmatter}"
        )

    def test_has_description_field(self, skill_file):
        """Frontmatter must have 'description' field."""
        assert skill_file.frontmatter is not None, f"Skill '{skill_file.name}' missing frontmatter"

        assert "description" in skill_file.frontmatter, (
            f"Skill '{skill_file.name}' missing 'description' field in frontmatter.\n"
            f"File: {skill_file.path}\n"
            f"Current frontmatter: {skill_file.frontmatter}"
        )

    def test_description_min_length(self, skill_file):
        """Description must be at least 50 characters."""
        if skill_file.frontmatter and "description" in skill_file.frontmatter:
            desc = skill_file.frontmatter["description"]
            assert len(desc) >= 50, (
                f"Skill '{skill_file.name}' description too short ({len(desc)} chars).\n"
                f"Minimum: 50 characters\n"
                f"File: {skill_file.path}\n"
                f"Current: {desc}"
            )


class TestSkillProgressiveDisclosure:
    """Test progressive disclosure structure (Level 1, 2, 3)."""

    def test_has_level_1_quick_start(self, skill_file):
        """All skills must have Level 1: Quick Start section."""
        assert "## Level 1: Quick Start" in skill_file.content, (
            f"Skill '{skill_file.name}' missing '## Level 1: Quick Start' section.\n"
            f"File: {skill_file.path}\n"
            f"This section is REQUIRED for all skills."
        )

    def test_has_level_2_implementation(self, skill_file):
        """All skills must have Level 2: Implementation section."""
        assert "## Level 2: Implementation" in skill_file.content, (
            f"Skill '{skill_file.name}' missing '## Level 2: Implementation' section.\n"
            f"File: {skill_file.path}\n"
            f"This section is REQUIRED for all skills."
        )

    def test_has_level_3_mastery(self, skill_file):
        """All skills must have Level 3: Mastery section."""
        # Check for either "Level 3: Mastery" or "Level 3: Mastery Resources"
        has_level_3 = (
            "## Level 3: Mastery" in skill_file.content or "## Level 3: Mastery Resources" in skill_file.content
        )

        assert has_level_3, (
            f"Skill '{skill_file.name}' missing '## Level 3: Mastery' section.\n"
            f"File: {skill_file.path}\n"
            f"This section is REQUIRED for all skills."
        )


class TestLevel1Subsections:
    """Test Level 1 required subsections."""

    def test_has_core_principles(self, skill_file):
        """Level 1 must have Core Principles subsection."""
        assert "### Core Principles" in skill_file.content, (
            f"Skill '{skill_file.name}' missing '### Core Principles' in Level 1.\n"
            f"File: {skill_file.path}\n"
            f"Level 1 must include Core Principles subsection."
        )

    def test_has_essential_checklist(self, skill_file):
        """Level 1 must have Essential Checklist subsection."""
        assert "### Essential Checklist" in skill_file.content, (
            f"Skill '{skill_file.name}' missing '### Essential Checklist' in Level 1.\n"
            f"File: {skill_file.path}\n"
            f"Level 1 must include Essential Checklist subsection."
        )

    def test_has_quick_example(self, skill_file):
        """Level 1 must have Quick Example subsection."""
        # Check for various example heading patterns
        example_patterns = [
            "### Quick Example",
            "### Example",
            "### Quick Reference",
        ]

        has_example = any(pattern in skill_file.content for pattern in example_patterns)

        assert has_example, (
            f"Skill '{skill_file.name}' missing example section in Level 1.\n"
            f"File: {skill_file.path}\n"
            f"Expected one of: {', '.join(example_patterns)}"
        )


class TestRequiredSections:
    """Test required sections beyond progressive disclosure."""

    def test_has_examples_section(self, skill_file):
        """All skills must have an Examples section."""
        # Check for Examples section (can be in Level 2 or Level 3)
        examples_patterns = [
            "## Examples",
            "### Examples",
            "## Example",
            "### Example",
            "Templates & Examples",
        ]

        has_examples = any(pattern in skill_file.content for pattern in examples_patterns)

        assert has_examples, (
            f"Skill '{skill_file.name}' missing Examples section.\n"
            f"File: {skill_file.path}\n"
            f"All skills MUST have working code examples.\n"
            f"Expected one of: {', '.join(examples_patterns)}"
        )

    def test_has_integration_points_section(self, skill_file):
        """All skills must have Integration Points section."""
        integration_patterns = [
            "## Integration Points",
            "### Integration Points",
            "## Integrations",
            "### Integrations",
            "Related Skills",
        ]

        has_integration = any(pattern in skill_file.content for pattern in integration_patterns)

        assert has_integration, (
            f"Skill '{skill_file.name}' missing Integration Points section.\n"
            f"File: {skill_file.path}\n"
            f"All skills MUST list integrations with other skills.\n"
            f"Expected one of: {', '.join(integration_patterns)}"
        )

    def test_has_common_pitfalls_section(self, skill_file):
        """All skills must have Common Pitfalls section."""
        pitfall_patterns = [
            "## Common Pitfalls",
            "### Common Pitfalls",
            "## Pitfalls",
            "### Pitfalls",
            "Anti-Patterns",
            "Common Mistakes",
        ]

        has_pitfalls = any(pattern in skill_file.content for pattern in pitfall_patterns)

        assert has_pitfalls, (
            f"Skill '{skill_file.name}' missing Common Pitfalls section.\n"
            f"File: {skill_file.path}\n"
            f"All skills MUST document common pitfalls/anti-patterns.\n"
            f"Expected one of: {', '.join(pitfall_patterns)}"
        )


class TestStructuralIntegrity:
    """Test overall structural integrity."""

    def test_has_navigation_links(self, skill_file):
        """Skills should have navigation breadcrumbs."""
        # Check for quick navigation pattern
        has_navigation = (
            "Quick Navigation" in skill_file.content or "Level 1" in skill_file.content[:500]  # In first 500 chars
        )

        assert has_navigation, (
            f"Skill '{skill_file.name}' missing navigation breadcrumbs.\n"
            f"File: {skill_file.path}\n"
            f"Should include: > **Quick Navigation:**\n"
            f"Level 1: [Quick Start]... → Level 2: ... → Level 3: ..."
        )

    def test_no_placeholder_content(self, skill_file):
        """Skills must not have placeholder content."""
        placeholder_patterns = [
            "TODO",
            "FIXME",
            "TBD",
            "Coming soon",
            "To be added",
            "Under construction",
        ]

        for pattern in placeholder_patterns:
            assert pattern not in skill_file.content, (
                f"Skill '{skill_file.name}' contains placeholder: '{pattern}'.\n"
                f"File: {skill_file.path}\n"
                f"All content must be complete - no placeholders allowed."
            )

    def test_markdown_formatting_valid(self, skill_file):
        """Basic markdown formatting validation."""
        # Check for unclosed code blocks
        code_fence_count = skill_file.content.count("```")
        assert code_fence_count % 2 == 0, (
            f"Skill '{skill_file.name}' has unclosed code blocks.\n"
            f"File: {skill_file.path}\n"
            f"Found {code_fence_count} code fences (should be even number)."
        )
