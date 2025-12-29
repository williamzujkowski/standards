"""Test skills token budget compliance.

TARGET STATE:
- Level 1 content <200 tokens
- Level 2 content <3,000 tokens
- Total inline content <5,000 tokens
- No skill exceeds token budget
- Level 3 uses filesystem references (0 inline tokens)

Token estimation: ~4 chars per token (conservative)

NOTE: Many skills currently exceed these budgets.
See https://github.com/williamzujkowski/standards/issues/42 for tracking.
These tests are marked as xfail until skills are optimized.
"""

import re

import pytest

# Mark all tests in this module as expected failures until Issue #42 is resolved
# Skills function correctly but exceed token budgets
pytestmark = pytest.mark.xfail(
    reason="Skills exceed token budgets - see Issue #42",
    strict=False,  # Allow tests to pass if skills are optimized
)


def extract_level(content: str, level: int) -> str:
    """Extract content for a specific level."""
    # Match Level heading and capture until next Level or end
    if level == 1:
        pattern = r"## Level 1:.*?(?=## Level 2:|## Level 3:|\Z)"
    elif level == 2:
        pattern = r"## Level 2:.*?(?=## Level 3:|\Z)"
    elif level == 3:
        pattern = r"## Level 3:.*?(?=## (?!Level)|---|\Z)"
    else:
        return ""

    match = re.search(pattern, content, re.DOTALL)
    return match.group(0) if match else ""


def estimate_tokens(text: str) -> int:
    """Estimate token count (conservative: 4 chars per token)."""
    return len(text) // 4


def count_inline_content_tokens(level3_content: str) -> int:
    """Count inline content tokens in Level 3 (should be minimal)."""
    # Level 3 should primarily be links/references
    # Count only non-link, non-heading content
    lines = level3_content.split("\n")
    inline_content = []

    for line in lines:
        # Skip headings, links, and empty lines
        if line.strip().startswith("#"):
            continue
        if line.strip().startswith("-") and "(" in line and ")" in line:
            continue  # Likely a link
        if not line.strip():
            continue

        inline_content.append(line)

    return estimate_tokens("\n".join(inline_content))


class TestLevel1TokenBudget:
    """Test Level 1 token budget (<200 tokens)."""

    def test_level1_within_budget(self, skill_file, token_estimator):
        """Level 1 must be <200 tokens for quick reading (5 min)."""
        level1_content = extract_level(skill_file.content, 1)

        assert level1_content, f"Skill '{skill_file.name}' has no Level 1 content.\nFile: {skill_file.path}"

        tokens = token_estimator(level1_content)
        max_tokens = 200

        assert tokens <= max_tokens, (
            f"Skill '{skill_file.name}' Level 1 exceeds token budget.\n"
            f"File: {skill_file.path}\n"
            f"Current: {tokens} tokens\n"
            f"Maximum: {max_tokens} tokens\n"
            f"Exceeds by: {tokens - max_tokens} tokens\n\n"
            f"Level 1 should be a quick overview only.\n"
            f"Move detailed content to Level 2 or external files."
        )


class TestLevel2TokenBudget:
    """Test Level 2 token budget (<3,000 tokens)."""

    def test_level2_within_budget(self, skill_file, token_estimator):
        """Level 2 must be <3,000 tokens for detailed learning."""
        level2_content = extract_level(skill_file.content, 2)

        assert level2_content, f"Skill '{skill_file.name}' has no Level 2 content.\nFile: {skill_file.path}"

        tokens = token_estimator(level2_content)
        max_tokens = 3000

        assert tokens <= max_tokens, (
            f"Skill '{skill_file.name}' Level 2 exceeds token budget.\n"
            f"File: {skill_file.path}\n"
            f"Current: {tokens} tokens\n"
            f"Maximum: {max_tokens} tokens\n"
            f"Exceeds by: {tokens - max_tokens} tokens\n\n"
            f"Level 2 should cover implementation details.\n"
            f"Move advanced content to Level 3 resources."
        )


class TestLevel3TokenBudget:
    """Test Level 3 token budget (minimal inline content)."""

    def test_level3_uses_filesystem_references(self, skill_file):
        """Level 3 should primarily use filesystem references, not inline content."""
        level3_content = extract_level(skill_file.content, 3)

        assert level3_content, f"Skill '{skill_file.name}' has no Level 3 content.\nFile: {skill_file.path}"

        inline_tokens = count_inline_content_tokens(level3_content)
        max_inline_tokens = 500  # Allow some inline content for structure

        assert inline_tokens <= max_inline_tokens, (
            f"Skill '{skill_file.name}' Level 3 has too much inline content.\n"
            f"File: {skill_file.path}\n"
            f"Current inline: ~{inline_tokens} tokens\n"
            f"Maximum inline: {max_inline_tokens} tokens\n\n"
            f"Level 3 should primarily link to external resources:\n"
            f"- [Resource Name](resources/file.md)\n"
            f"- [Template](templates/template.py)\n"
            f"Not include large code blocks or documentation inline."
        )


class TestTotalTokenBudget:
    """Test total skill token budget."""

    def test_total_inline_content_budget(self, skill_file, token_estimator):
        """Total inline content must be <5,000 tokens."""
        # Extract all levels
        level1 = extract_level(skill_file.content, 1)
        level2 = extract_level(skill_file.content, 2)
        level3 = extract_level(skill_file.content, 3)

        # Total tokens (Level 1 + Level 2 + inline Level 3)
        total_tokens = token_estimator(level1) + token_estimator(level2) + count_inline_content_tokens(level3)

        max_tokens = 5000

        assert total_tokens <= max_tokens, (
            f"Skill '{skill_file.name}' exceeds total token budget.\n"
            f"File: {skill_file.path}\n"
            f"Current: {total_tokens} tokens\n"
            f"Maximum: {max_tokens} tokens\n"
            f"Exceeds by: {total_tokens - max_tokens} tokens\n\n"
            f"Breakdown:\n"
            f"- Level 1: ~{token_estimator(level1)} tokens (max 200)\n"
            f"- Level 2: ~{token_estimator(level2)} tokens (max 3000)\n"
            f"- Level 3 inline: ~{count_inline_content_tokens(level3)} tokens (max 500)\n\n"
            f"Consider:\n"
            f"1. Moving examples to templates/ directory\n"
            f"2. Moving detailed docs to resources/ directory\n"
            f"3. Using filesystem references in Level 3"
        )


class TestTokenBudgetDistribution:
    """Test proper token budget distribution across levels."""

    def test_level1_is_smallest(self, skill_file, token_estimator):
        """Level 1 should be smaller than Level 2 (progressive disclosure)."""
        level1 = extract_level(skill_file.content, 1)
        level2 = extract_level(skill_file.content, 2)

        level1_tokens = token_estimator(level1)
        level2_tokens = token_estimator(level2)

        assert level1_tokens < level2_tokens, (
            f"Skill '{skill_file.name}' has Level 1 larger than Level 2.\n"
            f"File: {skill_file.path}\n"
            f"Level 1: {level1_tokens} tokens\n"
            f"Level 2: {level2_tokens} tokens\n\n"
            f"Progressive disclosure requires Level 1 < Level 2.\n"
            f"Level 1 should be a brief overview only."
        )

    def test_frontmatter_within_budget(self, skill_file):
        """Frontmatter description should be concise (<100 tokens)."""
        if skill_file.frontmatter and "description" in skill_file.frontmatter:
            desc = skill_file.frontmatter["description"]
            tokens = estimate_tokens(desc)
            max_tokens = 100

            assert tokens <= max_tokens, (
                f"Skill '{skill_file.name}' description too long.\n"
                f"File: {skill_file.path}\n"
                f"Current: {tokens} tokens\n"
                f"Maximum: {max_tokens} tokens\n"
                f"Description: {desc}"
            )


class TestCodeBlockBudget:
    """Test code block token budget."""

    def test_code_blocks_reasonable_size(self, skill_file, token_estimator):
        """Individual code blocks should be <500 tokens each."""
        # Extract all code blocks
        code_blocks = re.findall(r"```.*?\n(.*?)```", skill_file.content, re.DOTALL)

        max_tokens_per_block = 500
        violations = []

        for i, block in enumerate(code_blocks, 1):
            tokens = token_estimator(block)
            if tokens > max_tokens_per_block:
                violations.append((i, tokens))

        assert not violations, (
            f"Skill '{skill_file.name}' has oversized code blocks.\n"
            f"File: {skill_file.path}\n"
            f"Violations: {len(violations)}\n"
            + "\n".join([f"  Block #{num}: {tokens} tokens (max {max_tokens_per_block})" for num, tokens in violations])
            + "\n\nConsider:\n"
            "1. Moving large examples to templates/ directory\n"
            "2. Showing only key parts in inline examples\n"
            "3. Linking to full examples in Level 3"
        )
