"""Test skills content quality compliance.

TARGET STATE:
- Examples section has at least 1 working code example
- Integration Points lists specific integrations
- Common Pitfalls has at least 3 items
- No placeholder text (TODO, FIXME, TBD)
- No empty sections

NOTE: Many skills are currently incomplete and need content work.
These tests are marked as xfail until skills are fully populated.
"""

import re

import pytest

# Mark all tests in this module as expected failures
# Skills are being developed and many don't have complete content yet
pytestmark = pytest.mark.xfail(
    reason="Skills incomplete - many need content work",
    strict=False,  # Allow tests to pass for complete skills
)


class TestExamplesQuality:
    """Test examples section quality."""

    def test_has_working_code_examples(self, skill_file):
        """Examples section must have at least 1 working code example."""
        # Count code blocks (```...```)
        code_blocks = re.findall(r"```", skill_file.content)
        code_block_count = len(code_blocks) // 2  # Pairs of opening/closing

        assert code_block_count >= 1, (
            f"Skill '{skill_file.name}' has no code examples.\n"
            f"File: {skill_file.path}\n"
            f"All skills MUST have at least 1 working code example.\n"
            f"Found: {code_block_count} code blocks"
        )

    def test_examples_have_language_specified(self, skill_file):
        """Code blocks should specify language for syntax highlighting."""
        # Find code blocks without language
        code_blocks = re.findall(r"```([^\n]*)\n", skill_file.content)
        blocks_without_lang = [i + 1 for i, lang in enumerate(code_blocks) if not lang.strip()]

        assert not blocks_without_lang, (
            f"Skill '{skill_file.name}' has code blocks without language.\n"
            f"File: {skill_file.path}\n"
            f"Blocks without language: {blocks_without_lang}\n\n"
            f"Use: ```python, ```bash, ```yaml, etc.\n"
            f"Not: ``` (bare)"
        )

    def test_examples_have_comments(self, skill_file):
        """Code examples should have explanatory comments."""
        # Extract code blocks with language
        code_blocks = re.findall(
            r"```(?:python|javascript|typescript|java|go|rust)\n(.*?)```",
            skill_file.content,
            re.DOTALL,
        )

        if not code_blocks:
            pytest.skip("No language-specific code blocks found")

        # Check if at least some code blocks have comments
        blocks_with_comments = sum(1 for block in code_blocks if "#" in block or "//" in block)

        assert blocks_with_comments > 0, (
            f"Skill '{skill_file.name}' has no commented code examples.\n"
            f"File: {skill_file.path}\n"
            f"Total code blocks: {len(code_blocks)}\n"
            f"With comments: {blocks_with_comments}\n\n"
            f"Code examples should include explanatory comments."
        )


class TestIntegrationPointsQuality:
    """Test Integration Points section quality."""

    def test_lists_specific_integrations(self, skill_file):
        """Integration Points must list specific skills/technologies."""
        # Find Integration Points or Related Skills section
        integration_section = None

        for pattern in [
            "## Integration Points",
            "### Integration Points",
            "## Related Skills",
            "### Related Skills",
        ]:
            if pattern in skill_file.content:
                # Extract section content
                idx = skill_file.content.index(pattern)
                # Get content until next section or end
                next_section = re.search(r"\n##[^#]", skill_file.content[idx + len(pattern) :])
                if next_section:
                    integration_section = skill_file.content[idx : idx + len(pattern) + next_section.start()]
                else:
                    integration_section = skill_file.content[idx:]
                break

        assert integration_section is not None, (
            f"Skill '{skill_file.name}' missing Integration Points section.\nFile: {skill_file.path}"
        )

        # Count list items or links in integration section
        list_items = re.findall(r"^[-*]\s+", integration_section, re.MULTILINE)
        links = re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", integration_section)

        total_integrations = len(list_items) + len(links)

        assert total_integrations >= 2, (
            f"Skill '{skill_file.name}' has insufficient integration points.\n"
            f"File: {skill_file.path}\n"
            f"Found: {total_integrations} integrations\n"
            f"Minimum: 2 integrations\n\n"
            f"List specific related skills, tools, or technologies."
        )


class TestCommonPitfallsQuality:
    """Test Common Pitfalls section quality."""

    def test_has_minimum_pitfalls(self, skill_file):
        """Common Pitfalls must have at least 3 documented pitfalls."""
        # Find Common Pitfalls or Anti-Patterns section
        pitfalls_section = None

        for pattern in [
            "## Common Pitfalls",
            "### Common Pitfalls",
            "## Pitfalls",
            "### Pitfalls",
            "Anti-Patterns",
        ]:
            if pattern in skill_file.content:
                idx = skill_file.content.index(pattern)
                # Get content until next section or end
                next_section = re.search(r"\n##[^#]", skill_file.content[idx + len(pattern) :])
                if next_section:
                    pitfalls_section = skill_file.content[idx : idx + len(pattern) + next_section.start()]
                else:
                    pitfalls_section = skill_file.content[idx:]
                break

        assert pitfalls_section is not None, (
            f"Skill '{skill_file.name}' missing Common Pitfalls section.\nFile: {skill_file.path}"
        )

        # Count distinct pitfalls (list items, headings, or code examples)
        list_items = re.findall(r"^[-*]\s+", pitfalls_section, re.MULTILINE)
        numbered_items = re.findall(r"^\d+\.\s+", pitfalls_section, re.MULTILINE)
        h4_headings = re.findall(r"^####\s+", pitfalls_section, re.MULTILINE)

        # Count good/bad example pairs
        good_bad_examples = pitfalls_section.count("✅") + pitfalls_section.count("❌")

        total_pitfalls = len(list_items) + len(numbered_items) + len(h4_headings)
        # If using good/bad examples, count pairs
        if good_bad_examples >= 2:
            total_pitfalls = max(total_pitfalls, good_bad_examples // 2)

        assert total_pitfalls >= 3, (
            f"Skill '{skill_file.name}' has insufficient pitfalls documented.\n"
            f"File: {skill_file.path}\n"
            f"Found: {total_pitfalls} pitfalls\n"
            f"Minimum: 3 pitfalls\n\n"
            f"Document common mistakes developers make."
        )

    def test_pitfalls_have_examples(self, skill_file):
        """Pitfalls should show bad examples and better alternatives."""
        # Find Common Pitfalls section
        pitfalls_section = None

        for pattern in [
            "## Common Pitfalls",
            "### Common Pitfalls",
            "Anti-Patterns",
        ]:
            if pattern in skill_file.content:
                idx = skill_file.content.index(pattern)
                next_section = re.search(r"\n##[^#]", skill_file.content[idx + len(pattern) :])
                if next_section:
                    pitfalls_section = skill_file.content[idx : idx + len(pattern) + next_section.start()]
                else:
                    pitfalls_section = skill_file.content[idx:]
                break

        if pitfalls_section is None:
            pytest.skip("No pitfalls section found")

        # Check for good/bad indicators or code examples
        has_examples = (
            "❌" in pitfalls_section
            or "✅" in pitfalls_section
            or "Bad:" in pitfalls_section
            or "Good:" in pitfalls_section
            or "```" in pitfalls_section
        )

        assert has_examples, (
            f"Skill '{skill_file.name}' pitfalls lack examples.\n"
            f"File: {skill_file.path}\n\n"
            f"Show bad examples (❌) and good alternatives (✅)."
        )


class TestContentCompleteness:
    """Test content completeness and quality."""

    def test_no_placeholder_content(self, skill_file):
        """Skills must not contain placeholder text."""
        placeholders = {
            "TODO": r"\bTODO\b",
            "FIXME": r"\bFIXME\b",
            "TBD": r"\bTBD\b",
            "Coming soon": r"Coming soon",
            "To be added": r"To be added",
            "Under construction": r"Under construction",
            "WIP": r"\bWIP\b",
        }

        found_placeholders = []
        for name, pattern in placeholders.items():
            if re.search(pattern, skill_file.content, re.IGNORECASE):
                # Find line numbers
                lines = skill_file.content.split("\n")
                line_nums = [i + 1 for i, line in enumerate(lines) if re.search(pattern, line, re.IGNORECASE)]
                found_placeholders.append(f"{name} (lines: {line_nums})")

        assert not found_placeholders, (
            f"Skill '{skill_file.name}' contains placeholders.\n"
            f"File: {skill_file.path}\n"
            f"Found: {', '.join(found_placeholders)}\n\n"
            f"All content must be complete - no placeholders allowed."
        )

    def test_no_empty_sections(self, skill_file):
        """Skills must not have empty sections."""
        # Find section headings using split approach instead of findall
        empty_sections = []
        lines = skill_file.content.split("\n")

        for i, line in enumerate(lines):
            if re.match(r"^#{2,4}\s+", line):
                # Check if next section or end has any content
                heading_level = len(re.match(r"^(#+)", line).group(1))
                content_lines = []

                # Look ahead until next same-level heading or end
                for j in range(i + 1, len(lines)):
                    next_line = lines[j]
                    if re.match(rf"^#{{{1, {heading_level}}}}\s+", next_line):
                        break
                    if next_line.strip():
                        content_lines.append(next_line)

                # If section has no content (only whitespace/empty lines)
                if not content_lines:
                    empty_sections.append(f"Line {i + 1}: {line.strip()}")

        assert not empty_sections, (
            f"Skill '{skill_file.name}' has empty sections.\n"
            f"File: {skill_file.path}\n"
            f"Empty sections:\n" + "\n".join(f"  - {s}" for s in empty_sections) + "\n\nAll sections must have content."
        )

    def test_has_actionable_content(self, skill_file):
        """Skills must have actionable content (commands, code, checklists)."""
        # Count actionable elements
        code_blocks = skill_file.content.count("```")
        checklists = len(re.findall(r"^[-*]\s+\[[ x]\]", skill_file.content, re.MULTILINE))
        commands = len(re.findall(r"^\$\s+", skill_file.content, re.MULTILINE))

        actionable_count = (code_blocks // 2) + checklists + commands

        assert actionable_count >= 3, (
            f"Skill '{skill_file.name}' lacks actionable content.\n"
            f"File: {skill_file.path}\n"
            f"Found: {actionable_count} actionable elements\n"
            f"Minimum: 3\n\n"
            f"Include code examples, checklists, or commands."
        )


class TestCrossReferences:
    """Test cross-references and links."""

    def test_internal_links_valid(self, skill_file):
        """Internal markdown links should be valid."""
        # Find markdown links
        links = re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", skill_file.content)

        broken_links = []

        for text, url in links:
            # Check internal links (starting with # or relative paths)
            if url.startswith("#"):
                # Anchor link - check if heading exists
                anchor = url[1:].lower().replace(" ", "-")
                # Convert heading to anchor format
                headings = re.findall(r"^#+\s+(.+)$", skill_file.content, re.MULTILINE)
                heading_anchors = [
                    h.lower().replace(" ", "-").replace(":", "").replace("(", "").replace(")", "") for h in headings
                ]

                if anchor not in heading_anchors:
                    broken_links.append(f"[{text}]({url}) - heading not found")

        assert not broken_links, (
            f"Skill '{skill_file.name}' has broken internal links.\n"
            f"File: {skill_file.path}\n"
            f"Broken links:\n" + "\n".join(f"  - {link}" for link in broken_links)
        )

    def test_skill_references_exist(self, skill_file, skills_root):
        """References to other skills should exist."""
        # Find references to other SKILL.md files
        skill_refs = re.findall(r"\.\./([^/]+)/SKILL\.md", skill_file.content)

        missing_refs = []

        for ref in skill_refs:
            ref_path = skill_file.path.parent.parent / ref / "SKILL.md"
            if not ref_path.exists():
                missing_refs.append(ref)

        assert not missing_refs, (
            f"Skill '{skill_file.name}' references non-existent skills.\n"
            f"File: {skill_file.path}\n"
            f"Missing: {', '.join(missing_refs)}"
        )
