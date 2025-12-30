#!/usr/bin/env python3
"""
Fix malformed YAML frontmatter in SKILL.md files.

This script removes invalid lines that were accidentally added to YAML frontmatter,
such as JavaScript comments, malformed YAML entries, etc.
"""

import re
from pathlib import Path


def fix_frontmatter(content: str) -> str:
    """Fix malformed YAML frontmatter."""
    # Split into frontmatter and body
    parts = content.split("---", 2)
    if len(parts) < 3:
        return content

    frontmatter = parts[1]
    body = parts[2]

    # Remove duplicate --- at start of body
    body = re.sub(r"^\s*---\s*\n", "", body)

    # Lines that should be removed from frontmatter
    invalid_patterns = [
        r"^// TODO:.*$",  # JavaScript comments
        r"^'\- \*\*.*$",  # Malformed list items like '- **Tools**':
        r"^'\*\*.*$",  # Malformed entries like '**Problem':
        r"^\d+\. \*\*.*$",  # Numbered list items in YAML
        r"^  patterns'\s*$",  # Stray continuation from corrupted description
        r"^  security patterns'\s*$",  # Another stray continuation
    ]

    # Filter out invalid lines
    lines = frontmatter.split("\n")
    valid_lines = []
    for line in lines:
        is_invalid = False
        stripped = line.strip()
        for pattern in invalid_patterns:
            if re.match(pattern, stripped):
                is_invalid = True
                break
        # Also check for lines that are just stray single quotes or fragments
        if stripped in ["patterns'", "security patterns'", "'"]:
            is_invalid = True
        if not is_invalid:
            valid_lines.append(line)

    # Fix description that ends with incomplete text
    fixed_frontmatter = "\n".join(valid_lines)
    # Remove trailing incomplete lines from description
    fixed_frontmatter = re.sub(r"(description:.*?)\n\s+[a-z]+'\s*$", r"\1", fixed_frontmatter, flags=re.DOTALL)

    return f"---{fixed_frontmatter}---{body}"


def process_skill(skill_path: Path, dry_run: bool = True) -> bool:
    """Process a single skill file."""
    content = skill_path.read_text(encoding="utf-8")

    # Check if file has malformed content
    if "// TODO" not in content and "'- **" not in content:
        return False

    fixed = fix_frontmatter(content)
    if fixed != content:
        if dry_run:
            print(f"Would fix: {skill_path}")
        else:
            skill_path.write_text(fixed, encoding="utf-8")
            print(f"Fixed: {skill_path}")
        return True
    return False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Fix malformed SKILL.md frontmatter")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be fixed without making changes")
    parser.add_argument("--apply", action="store_true", help="Apply fixes")
    args = parser.parse_args()

    if not args.apply and not args.dry_run:
        args.dry_run = True
        print("Running in dry-run mode. Use --apply to make changes.\n")

    skills_dir = Path(__file__).parent.parent / "skills"
    fixed_count = 0

    for skill_path in skills_dir.rglob("SKILL.md"):
        if process_skill(skill_path, dry_run=not args.apply):
            fixed_count += 1

    print(f"\nTotal: {fixed_count} files {'would be' if args.dry_run else 'were'} fixed")


if __name__ == "__main__":
    main()
