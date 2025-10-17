#!/usr/bin/env python3
"""
Token counting for SKILL.md validation.

Counts tokens using tiktoken library with cl100k_base encoding,
reports by level, and flags violations.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional
import json
import re
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


# Try to import tiktoken, fall back to estimation
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
    logger.debug("tiktoken library available")
except ImportError:
    TIKTOKEN_AVAILABLE = False
    logger.warning("tiktoken not available, using estimation")


class TokenCounter:
    """Token counter for SKILL.md files."""

    def __init__(self, skill_file: Path):
        self.skill_file = skill_file
        self.encoding = None

        if TIKTOKEN_AVAILABLE:
            try:
                self.encoding = tiktoken.get_encoding("cl100k_base")
            except Exception as e:
                logger.warning(f"Failed to load tiktoken encoding: {e}")
                self.encoding = None

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        if self.encoding:
            return len(self.encoding.encode(text))
        else:
            # Fallback estimation: ~4 chars per token
            return len(text) // 4

    def split_by_levels(self, content: str) -> Dict[str, str]:
        """Split content into levels."""
        levels = {}

        # Extract frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                levels["frontmatter"] = parts[1]
                content = parts[2]

        # Split by level headers
        level_pattern = r"## Level (\d+):"
        matches = list(re.finditer(level_pattern, content))

        if not matches:
            logger.warning("No level markers found")
            levels["content"] = content
            return levels

        # Extract each level
        for i, match in enumerate(matches):
            level_num = match.group(1)
            start = match.start()

            # Find end (next level or end of content)
            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(content)

            level_content = content[start:end]
            levels[f"level{level_num}"] = level_content

        return levels

    def count_all_levels(self) -> Dict[str, Dict[str, int]]:
        """Count tokens for all levels."""
        content = self.skill_file.read_text()
        levels = self.split_by_levels(content)

        results = {}
        total_tokens = 0

        for level_name, level_content in levels.items():
            tokens = self.count_tokens(level_content)
            results[level_name] = {
                "tokens": tokens,
                "chars": len(level_content),
                "lines": level_content.count("\n") + 1
            }
            total_tokens += tokens

        results["total"] = {
            "tokens": total_tokens,
            "chars": len(content),
            "lines": content.count("\n") + 1
        }

        return results

    def check_violations(self, results: Dict[str, Dict[str, int]]) -> List[str]:
        """Check for token limit violations."""
        violations = []

        limits = {
            "level1": 1000,
            "level2": 5000,
            # level3 has no limit
        }

        for level_name, limit in limits.items():
            if level_name in results:
                tokens = results[level_name]["tokens"]
                if tokens > limit:
                    violations.append(
                        f"{level_name.replace('level', 'Level ')}: "
                        f"{tokens} tokens (limit: {limit}, over by {tokens - limit})"
                    )

        return violations

    def format_report(self, results: Dict[str, Dict[str, int]], violations: List[str]) -> str:
        """Format human-readable report."""
        lines = []
        lines.append("="*60)
        lines.append(f"TOKEN REPORT: {self.skill_file.name}")
        lines.append("="*60)
        lines.append("")

        # Method used
        if TIKTOKEN_AVAILABLE and self.encoding:
            lines.append("Method: tiktoken (cl100k_base)")
        else:
            lines.append("Method: Estimation (~4 chars/token)")
        lines.append("")

        # Level breakdown
        lines.append("Level Breakdown:")
        lines.append("-" * 60)

        for level_name in ["level1", "level2", "level3"]:
            if level_name in results:
                data = results[level_name]
                level_display = level_name.replace("level", "Level ")
                lines.append(f"{level_display:15} {data['tokens']:6,} tokens  "
                           f"{data['chars']:7,} chars  {data['lines']:5,} lines")

        lines.append("-" * 60)

        # Total
        if "total" in results:
            data = results["total"]
            lines.append(f"{'TOTAL':15} {data['tokens']:6,} tokens  "
                        f"{data['chars']:7,} chars  {data['lines']:5,} lines")

        lines.append("")

        # Violations
        if violations:
            lines.append("❌ VIOLATIONS:")
            for violation in violations:
                lines.append(f"  • {violation}")
        else:
            lines.append("✓ No violations detected")

        lines.append("="*60)

        return "\n".join(lines)


def count_directory(directory: Path, output_json: Optional[Path] = None) -> Dict[str, any]:
    """Count tokens for all SKILL.md files in directory."""
    skill_files = list(directory.rglob("SKILL.md"))

    if not skill_files:
        logger.warning(f"No SKILL.md files found in {directory}")
        return {}

    all_results = {}
    total_violations = []

    for skill_file in skill_files:
        logger.info(f"Analyzing: {skill_file}")

        counter = TokenCounter(skill_file)
        results = counter.count_all_levels()
        violations = counter.check_violations(results)

        all_results[str(skill_file)] = {
            "results": results,
            "violations": violations
        }

        if violations:
            total_violations.extend([f"{skill_file.parent.name}: {v}" for v in violations])

        # Print individual report
        print(counter.format_report(results, violations))
        print()

    # Summary
    print("="*60)
    print(f"SUMMARY: {len(skill_files)} skills analyzed")
    print("="*60)
    print(f"Total violations: {len(total_violations)}")

    if total_violations:
        print("\nAll violations:")
        for violation in total_violations:
            print(f"  • {violation}")

    # Export JSON if requested
    if output_json:
        output_json.write_text(json.dumps(all_results, indent=2))
        logger.info(f"Exported JSON report to: {output_json}")

    return all_results


def main():
    parser = argparse.ArgumentParser(
        description="Count tokens in SKILL.md files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Count tokens in single skill
  python3 count-tokens.py skills/api-security/SKILL.md

  # Count all skills in directory
  python3 count-tokens.py --directory skills/

  # Export JSON report
  python3 count-tokens.py --directory skills/ \\
    --output-json reports/token-counts.json

  # Check if tiktoken is available
  python3 count-tokens.py --check-tiktoken

Exit codes:
  0 - No violations
  1 - Violations detected
  2 - No skills found
        """
    )

    parser.add_argument(
        "skill_file",
        nargs="?",
        type=Path,
        help="Path to SKILL.md file"
    )

    parser.add_argument(
        "--directory",
        type=Path,
        help="Count tokens for all SKILL.md files in directory"
    )

    parser.add_argument(
        "--output-json",
        type=Path,
        help="Export results to JSON file"
    )

    parser.add_argument(
        "--check-tiktoken",
        action="store_true",
        help="Check if tiktoken library is available"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Check tiktoken
    if args.check_tiktoken:
        if TIKTOKEN_AVAILABLE:
            print("✓ tiktoken is available")
            print("To install: pip install tiktoken")
        else:
            print("✗ tiktoken not available (using estimation)")
            print("To install: pip install tiktoken")
        sys.exit(0)

    # Single file mode
    if args.skill_file:
        counter = TokenCounter(args.skill_file)
        results = counter.count_all_levels()
        violations = counter.check_violations(results)

        print(counter.format_report(results, violations))

        if args.output_json:
            output_data = {
                str(args.skill_file): {
                    "results": results,
                    "violations": violations
                }
            }
            args.output_json.write_text(json.dumps(output_data, indent=2))
            logger.info(f"Exported JSON report to: {args.output_json}")

        sys.exit(1 if violations else 0)

    # Directory mode
    elif args.directory:
        all_results = count_directory(args.directory, args.output_json)

        if not all_results:
            sys.exit(2)

        # Count total violations
        total_violations = sum(
            len(data["violations"])
            for data in all_results.values()
        )

        sys.exit(1 if total_violations > 0 else 0)

    else:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
