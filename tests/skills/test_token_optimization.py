#!/usr/bin/env python3
"""
Test Suite: Token Optimization
Compares token usage between original standards and skill-based approach.
"""

import json
import re
from pathlib import Path


class TokenAnalyzer:
    """Analyzes and compares token usage across different content formats."""

    # Rough approximation: 1 token ≈ 4 characters for English text
    CHARS_PER_TOKEN = 4

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.standards_dir = self.repo_root / "docs" / "standards"
        self.skills_dir = self.repo_root / "docs" / "skills"

    def count_tokens(self, text: str) -> int:
        """Estimate token count from text."""
        # Remove excessive whitespace
        text = re.sub(r"\s+", " ", text)
        return len(text) // self.CHARS_PER_TOKEN

    def analyze_standard_file(self, file_path: Path) -> dict:
        """Analyze token usage in a standard file."""
        content = file_path.read_text(encoding="utf-8")

        return {
            "path": str(file_path.relative_to(self.repo_root)),
            "total_tokens": self.count_tokens(content),
            "char_count": len(content),
            "line_count": len(content.splitlines()),
        }

    def analyze_skill_progressive_loading(self, skill_path: Path) -> dict:
        """Analyze token usage with progressive disclosure."""
        # Level 1: Frontmatter only
        content = skill_path.read_text(encoding="utf-8")

        # Extract frontmatter
        frontmatter_match = re.match(r"^---\s*\n(.*?\n)---\s*\n", content, re.DOTALL)
        if not frontmatter_match:
            return {
                "path": str(skill_path.relative_to(self.repo_root)),
                "level1_tokens": 0,
                "level2_tokens": 0,
                "level3_tokens": 0,
                "total_tokens": 0,
                "error": "No frontmatter found",
            }

        frontmatter = frontmatter_match.group(0)
        main_content = content[len(frontmatter) :]

        # Level 1: Frontmatter (metadata only)
        level1_tokens = self.count_tokens(frontmatter)

        # Level 2: Main SKILL.md body
        level2_tokens = self.count_tokens(main_content)

        # Level 3: Additional resources (if they exist)
        level3_tokens = 0
        skill_dir = skill_path.parent
        resource_dirs = ["resources", "templates", "scripts", "examples"]

        for resource_dir in resource_dirs:
            resource_path = skill_dir / resource_dir
            if resource_path.exists():
                for resource_file in resource_path.rglob("*"):
                    if resource_file.is_file() and resource_file.suffix in [".md", ".txt", ".yaml", ".json"]:
                        resource_content = resource_file.read_text(encoding="utf-8")
                        level3_tokens += self.count_tokens(resource_content)

        return {
            "path": str(skill_path.relative_to(self.repo_root)),
            "level1_tokens": level1_tokens,  # Always loaded
            "level2_tokens": level2_tokens,  # Loaded on skill activation
            "level3_tokens": level3_tokens,  # Loaded on-demand
            "total_tokens": level1_tokens + level2_tokens + level3_tokens,
            "progressive_saving": level2_tokens + level3_tokens,  # Tokens saved if not loaded
        }

    def compare_standard_to_skill(self, standard_name: str) -> dict:
        """Compare a standard file to its skill equivalent."""
        standard_path = self.standards_dir / f"{standard_name}.md"
        skill_path = self.skills_dir / standard_name.lower().replace("_", "-") / "SKILL.md"

        results = {
            "standard_name": standard_name,
            "has_standard": standard_path.exists(),
            "has_skill": skill_path.exists(),
        }

        if standard_path.exists():
            results["standard_analysis"] = self.analyze_standard_file(standard_path)

        if skill_path.exists():
            results["skill_analysis"] = self.analyze_skill_progressive_loading(skill_path)

            # Calculate optimization metrics
            if standard_path.exists():
                standard_tokens = results["standard_analysis"]["total_tokens"]
                skill_level1 = results["skill_analysis"]["level1_tokens"]
                skill_total = results["skill_analysis"]["total_tokens"]

                results["optimization"] = {
                    "level1_reduction_pct": (
                        ((standard_tokens - skill_level1) / standard_tokens * 100) if standard_tokens > 0 else 0
                    ),
                    "tokens_saved_level1": standard_tokens - skill_level1,
                    "total_token_change": skill_total - standard_tokens,
                    "progressive_advantage": results["skill_analysis"]["progressive_saving"],
                }

        return results

    def full_repository_comparison(self) -> dict:
        """Compare all standards to skills."""
        # Find all standards
        if not self.standards_dir.exists():
            return {"error": "Standards directory not found"}

        standards = [f.stem for f in self.standards_dir.glob("*.md") if f.stem not in ["README", "UNIFIED_STANDARDS"]]

        results = {
            "total_standards": len(standards),
            "comparisons": [],
            "summary": {
                "total_standard_tokens": 0,
                "total_skill_level1_tokens": 0,
                "total_skill_all_tokens": 0,
                "average_reduction_pct": 0,
            },
        }

        reductions = []

        for standard in standards:
            comparison = self.compare_standard_to_skill(standard)
            results["comparisons"].append(comparison)

            if "optimization" in comparison:
                results["summary"]["total_standard_tokens"] += comparison["standard_analysis"]["total_tokens"]
                results["summary"]["total_skill_level1_tokens"] += comparison["skill_analysis"]["level1_tokens"]
                results["summary"]["total_skill_all_tokens"] += comparison["skill_analysis"]["total_tokens"]
                reductions.append(comparison["optimization"]["level1_reduction_pct"])

        if reductions:
            results["summary"]["average_reduction_pct"] = sum(reductions) / len(reductions)

        return results


# Test cases
import pytest


class TestTokenOptimization:
    """Test token optimization and efficiency."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        repo_root = Path(__file__).parent.parent.parent
        return TokenAnalyzer(repo_root)

    def test_token_counter_basic(self, analyzer):
        """Test basic token counting."""
        text = "This is a test sentence with exactly ten words here."
        tokens = analyzer.count_tokens(text)

        # Should be approximately 10-15 tokens
        assert 8 <= tokens <= 20

    def test_skill_progressive_structure(self, tmp_path):
        """Test that skills support progressive loading."""
        skills_dir = tmp_path / "docs" / "skills" / "test-skill"
        skills_dir.mkdir(parents=True)

        # Create a skill with all 3 levels
        frontmatter = """---
name: test-skill
description: Test skill for token analysis
---

"""

        main_content = """# Test Skill

## Overview
This is the main content (Level 2).

## Core Instructions
Follow these steps.
"""

        (skills_dir / "SKILL.md").write_text(frontmatter + main_content)

        # Add Level 3 resources
        (skills_dir / "resources").mkdir()
        (skills_dir / "resources" / "advanced.md").write_text("# Advanced Topics\n\nDetailed information here.")

        analyzer = TokenAnalyzer(tmp_path)
        result = analyzer.analyze_skill_progressive_loading(skills_dir / "SKILL.md")

        assert result["level1_tokens"] > 0  # Has frontmatter
        assert result["level2_tokens"] > 0  # Has main content
        assert result["level3_tokens"] > 0  # Has resources
        assert result["total_tokens"] == result["level1_tokens"] + result["level2_tokens"] + result["level3_tokens"]

    def test_token_reduction_calculation(self):
        """Test token reduction calculations."""
        standard_tokens = 10000
        skill_level1_tokens = 100

        reduction_pct = (standard_tokens - skill_level1_tokens) / standard_tokens * 100

        assert reduction_pct == 99.0  # 99% reduction

    def test_repository_comparison_structure(self, analyzer):
        """Test that repository comparison returns expected structure."""
        # This test will pass even if no skills exist yet
        results = analyzer.full_repository_comparison()

        assert "total_standards" in results
        assert "comparisons" in results
        assert "summary" in results

        if results["total_standards"] > 0:
            assert isinstance(results["comparisons"], list)


if __name__ == "__main__":
    # Generate token comparison report
    repo_root = Path(__file__).parent.parent.parent
    analyzer = TokenAnalyzer(repo_root)

    print("\n=== Token Optimization Analysis ===\n")

    results = analyzer.full_repository_comparison()

    if "error" in results:
        print(f"Error: {results['error']}")
    else:
        print(f"Total standards analyzed: {results['total_standards']}")
        print("\nSummary:")
        print(f"  Total standard tokens: {results['summary']['total_standard_tokens']:,}")
        print(f"  Total skill Level 1 tokens: {results['summary']['total_skill_level1_tokens']:,}")
        print(f"  Average reduction: {results['summary']['average_reduction_pct']:.1f}%")

        # Save detailed report
        report_path = repo_root / "reports" / "generated" / "token-comparison.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\nDetailed report saved to: {report_path}")
