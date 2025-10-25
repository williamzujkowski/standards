#!/usr/bin/env python3
"""
Automated fixer for SKILL.md Anthropic API compliance.

This script fixes common compliance issues in SKILL.md files:
- Missing YAML frontmatter
- Missing name/description fields
- Token count overages (>5000 tokens)

Usage:
    python3 fix-anthropic-compliance.py --dry-run          # Preview changes
    python3 fix-anthropic-compliance.py --skill path/to/skill  # Fix one skill
    python3 fix-anthropic-compliance.py --all              # Fix all non-compliant
    python3 fix-anthropic-compliance.py --all --skip-token-optimization
"""

import argparse
import json
import logging
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

# Token estimation (rough approximation: 1 token ≈ 4 chars)
TOKEN_LIMIT = 5000
CHARS_PER_TOKEN = 4
CHAR_LIMIT = TOKEN_LIMIT * CHARS_PER_TOKEN

# Field limits per Anthropic API
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024

# Paths
REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
BACKUP_DIR = REPO_ROOT / ".backup" / f"skill-fixes-{datetime.now():%Y%m%d-%H%M%S}"
LOG_DIR = REPO_ROOT / "reports" / "generated"
LOG_FILE = LOG_DIR / "skill-fixes.log"


def setup_logging(verbose: bool = False) -> None:
    """Configure logging to file and console."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    level = logging.DEBUG if verbose else logging.INFO

    # File handler
    file_handler = logging.FileHandler(LOG_FILE, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(
        logging.Formatter('%(levelname)s: %(message)s')
    )

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def estimate_tokens(text: str) -> int:
    """Estimate token count (rough approximation)."""
    return len(text) // CHARS_PER_TOKEN


def extract_yaml_frontmatter(content: str) -> Tuple[Optional[Dict], str]:
    """Extract YAML frontmatter and remaining content."""
    if not content.startswith('---\n'):
        return None, content

    # Find the closing --- delimiter
    end_match = re.search(r'\n---\n', content[4:])  # Skip first ---

    if end_match:
        # Properly formatted frontmatter
        yaml_content = content[4:end_match.start() + 4]
        remaining = content[end_match.end() + 4:]
    else:
        # Malformed frontmatter - missing closing delimiter
        # Try to find where YAML ends and Markdown begins
        # YAML ends when we hit a line starting with # (Markdown header)
        logging.debug("Malformed frontmatter: missing closing '---'")

        lines = content[4:].split('\n')
        yaml_lines = []
        markdown_start = 0

        for i, line in enumerate(lines):
            # YAML content detection
            stripped = line.strip()
            if stripped.startswith('#'):
                # Found markdown header - YAML section ended
                markdown_start = i
                break
            elif stripped.startswith('```'):
                # Found code block - definitely not YAML
                markdown_start = i
                break
            elif stripped and ':' in line and not stripped.startswith('-'):
                # Valid YAML line
                yaml_lines.append(line)
            elif not stripped:
                # Empty line - keep for formatting
                yaml_lines.append(line)
            else:
                # Unknown format - assume end of YAML
                markdown_start = i
                break

        yaml_content = '\n'.join(yaml_lines)
        remaining = '\n'.join(lines[markdown_start:]) if markdown_start > 0 else ''

    try:
        frontmatter = yaml.safe_load(yaml_content)
        if frontmatter is None:
            frontmatter = {}
        return frontmatter, remaining
    except yaml.YAMLError as e:
        logging.debug(f"Failed to parse YAML frontmatter: {e}")
        # Try to salvage what we can - parse line by line
        lines = yaml_content.split('\n')
        frontmatter = {}
        for line in lines:
            if ':' in line and not line.strip().startswith('#'):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if key and value:
                        frontmatter[key] = value
        if frontmatter:
            return frontmatter, remaining
        return None, content


def derive_name_from_path(skill_path: Path) -> str:
    """Derive skill name from directory path."""
    # Get relative path from skills directory
    rel_path = skill_path.relative_to(SKILLS_DIR)

    # Use the last directory name (most specific)
    name = rel_path.parent.name if rel_path.parent != Path('.') else rel_path.name

    # Clean up: remove hyphens, capitalize
    name = name.replace('-', ' ').title()

    # Ensure within length limit
    if len(name) > MAX_NAME_LENGTH:
        name = name[:MAX_NAME_LENGTH].rsplit(' ', 1)[0]  # Cut at word boundary

    return name


def extract_description_from_content(content: str) -> Optional[str]:
    """Extract description from Level 1 Quick Start or first meaningful paragraph."""
    # Try to find Level 1 section
    level1_match = re.search(
        r'##\s+Level\s+1[^\n]*\n+(.*?)(?=##\s+Level\s+[23]|$)',
        content,
        re.DOTALL | re.IGNORECASE
    )

    if level1_match:
        level1_content = level1_match.group(1).strip()
        # Get first paragraph that's not a code block or heading
        paragraphs = level1_content.split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if para and not para.startswith('```') and not para.startswith('#') and not para.startswith('-'):
                # Remove markdown formatting
                clean_para = re.sub(r'[*_`]', '', para)
                clean_para = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_para)
                clean_para = re.sub(r'\n', ' ', clean_para)

                if clean_para and len(clean_para) <= MAX_DESCRIPTION_LENGTH:
                    return clean_para
                elif clean_para:
                    # Truncate at sentence boundary
                    sentences = re.split(r'[.!?]\s+', clean_para)
                    desc = ""
                    for sentence in sentences:
                        if len(desc) + len(sentence) + 2 <= MAX_DESCRIPTION_LENGTH:
                            desc += sentence + ". "
                        else:
                            break
                    if desc:
                        return desc.strip()

    # Try to find a title or first heading after frontmatter
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    in_code_block = False
    found_title = False

    for i, line in enumerate(lines):
        if line.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block or line.startswith('---'):
            continue

        # Look for first heading as context
        if line.startswith('#') and not found_title:
            found_title = True
            title_text = line.lstrip('#').strip()
            continue

        # Skip common template markers
        if 'TODO' in line.upper() or line.startswith('//'):
            continue

        # Found a meaningful content line
        if line and not line.startswith('#') and ':' not in line[:20]:
            clean_line = re.sub(r'[*_`]', '', line)
            clean_line = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_line)

            if len(clean_line) > 20:  # Skip very short lines
                if len(clean_line) <= MAX_DESCRIPTION_LENGTH:
                    return clean_line
                else:
                    return clean_line[:MAX_DESCRIPTION_LENGTH].rsplit(' ', 1)[0] + "..."

    return None


def create_generic_description(name: str, skill_path: Path) -> str:
    """Create a generic description based on skill category and path."""
    # Get full path components for better context
    rel_path = skill_path.relative_to(SKILLS_DIR)
    parts = list(rel_path.parents)[:-1]  # Exclude '.' and skill file itself

    if len(parts) >= 2:
        # e.g., data-engineering/orchestration
        category = parts[-1].name.replace('-', ' ').title()
        subcategory = parts[-2].name.replace('-', ' ')
        return f"{name.title()} standards for {subcategory} in {category} environments. Covers best practices, implementation patterns, and integration guidelines."
    elif len(parts) == 1:
        # e.g., testing
        category = parts[0].name.replace('-', ' ').title()
        return f"{name.title()} standards and best practices for {category}. Includes implementation guidelines, common patterns, and testing strategies."
    else:
        # Fallback
        return f"{name.title()} standards and implementation best practices for software development."


def split_level_content(content: str) -> Tuple[str, str, str]:
    """Split content into Level 1, Level 2, and Level 3 sections."""
    # Find level boundaries
    level1_match = re.search(r'(##\s+Level\s+1[^\n]*\n+.*?)(?=##\s+Level\s+[23]|$)', content, re.DOTALL | re.IGNORECASE)
    level2_match = re.search(r'(##\s+Level\s+2[^\n]*\n+.*?)(?=##\s+Level\s+3|$)', content, re.DOTALL | re.IGNORECASE)
    level3_match = re.search(r'(##\s+Level\s+3[^\n]*\n+.*?)$', content, re.DOTALL | re.IGNORECASE)

    level1 = level1_match.group(1) if level1_match else ""
    level2 = level2_match.group(1) if level2_match else ""
    level3 = level3_match.group(1) if level3_match else ""

    return level1, level2, level3


def optimize_token_count(content: str, frontmatter: Dict) -> Tuple[str, bool]:
    """
    Optimize content to stay under token limit.
    Move verbose examples to Level 3, condense Level 2.

    Returns: (optimized_content, was_modified)
    """
    current_tokens = estimate_tokens(content)

    if current_tokens <= TOKEN_LIMIT:
        return content, False

    logging.info(f"Optimizing content: {current_tokens} tokens → target {TOKEN_LIMIT}")

    level1, level2, level3 = split_level_content(content)

    # Strategy: Move detailed examples from Level 2 to Level 3
    # Identify code blocks in Level 2
    code_blocks = re.findall(r'```[\s\S]*?```', level2)

    if code_blocks and len(code_blocks) > 2:
        # Keep first 2 examples in Level 2, move rest to Level 3
        examples_to_move = code_blocks[2:]

        # Remove examples from Level 2
        level2_condensed = level2
        for example in examples_to_move:
            level2_condensed = level2_condensed.replace(example, '', 1)

        # Add to Level 3
        if not level3:
            level3 = "\n\n## Level 3: Complete Reference\n\n### Additional Examples\n\n"
        elif "Additional Examples" not in level3:
            level3 += "\n\n### Additional Examples\n\n"

        for example in examples_to_move:
            level3 += f"\n{example}\n"

        # Rebuild content
        optimized = level1 + "\n\n" + level2_condensed + "\n\n" + level3

        # Check if optimization was sufficient
        new_tokens = estimate_tokens(optimized)
        if new_tokens <= TOKEN_LIMIT:
            logging.info(f"Optimization successful: {current_tokens} → {new_tokens} tokens")
            return optimized, True
        else:
            logging.warning(f"Optimization insufficient: {current_tokens} → {new_tokens} tokens (still over limit)")
            return optimized, True

    # If no code blocks to move, try condensing text
    # Remove excessive whitespace
    condensed = re.sub(r'\n{3,}', '\n\n', content)

    new_tokens = estimate_tokens(condensed)
    if new_tokens < current_tokens:
        logging.info(f"Condensed whitespace: {current_tokens} → {new_tokens} tokens")
        return condensed, True

    logging.warning("Could not optimize below token limit without manual intervention")
    return content, False


def fix_skill_file(
    skill_path: Path,
    dry_run: bool = False,
    skip_token_optimization: bool = False
) -> Dict[str, any]:
    """
    Fix a single SKILL.md file for Anthropic compliance.

    Returns dict with:
        - fixed: bool
        - issues_found: List[str]
        - changes_made: List[str]
        - diff_preview: Optional[str]
    """
    result = {
        "fixed": False,
        "issues_found": [],
        "changes_made": [],
        "diff_preview": None
    }

    logging.info(f"Processing: {skill_path.relative_to(REPO_ROOT)}")

    # Read original content
    try:
        original_content = skill_path.read_text(encoding='utf-8')
    except Exception as e:
        logging.error(f"Failed to read {skill_path}: {e}")
        return result

    content = original_content
    modified = False

    # Extract or create frontmatter
    frontmatter, body = extract_yaml_frontmatter(content)

    if frontmatter is None:
        result["issues_found"].append("Missing YAML frontmatter")
        frontmatter = {}
        modified = True

    # Check/fix name field
    if 'name' not in frontmatter or not frontmatter['name']:
        result["issues_found"].append("Missing 'name' field")
        name = derive_name_from_path(skill_path)
        frontmatter['name'] = name
        result["changes_made"].append(f"Added name: '{name}'")
        modified = True
    elif len(frontmatter['name']) > MAX_NAME_LENGTH:
        result["issues_found"].append(f"Name too long ({len(frontmatter['name'])} > {MAX_NAME_LENGTH})")
        old_name = frontmatter['name']
        frontmatter['name'] = old_name[:MAX_NAME_LENGTH].rsplit(' ', 1)[0]
        result["changes_made"].append(f"Truncated name: '{old_name}' → '{frontmatter['name']}'")
        modified = True

    # Check/fix description field
    desc_value = frontmatter.get('description', '').strip()
    if not desc_value or desc_value.startswith('TODO'):
        result["issues_found"].append("Missing or placeholder 'description' field")
        desc = extract_description_from_content(body)
        if not desc:
            desc = create_generic_description(frontmatter.get('name', 'Skill'), skill_path)
        frontmatter['description'] = desc
        result["changes_made"].append(f"Added description: '{desc[:50]}...'")
        modified = True
    elif len(desc_value) > MAX_DESCRIPTION_LENGTH:
        result["issues_found"].append(f"Description too long ({len(desc_value)} > {MAX_DESCRIPTION_LENGTH})")
        old_desc = desc_value
        frontmatter['description'] = old_desc[:MAX_DESCRIPTION_LENGTH].rsplit(' ', 1)[0] + "..."
        result["changes_made"].append("Truncated description to fit limit")
        modified = True

    # Check token count
    full_content = body if frontmatter else content
    token_count = estimate_tokens(full_content)

    if token_count > TOKEN_LIMIT:
        result["issues_found"].append(f"Token count exceeded ({token_count} > {TOKEN_LIMIT})")

        if not skip_token_optimization:
            optimized_body, was_optimized = optimize_token_count(body, frontmatter)
            if was_optimized:
                body = optimized_body
                result["changes_made"].append(f"Optimized content: {token_count} → {estimate_tokens(body)} tokens")
                modified = True

    # Rebuild content if modified
    if modified:
        # Ensure frontmatter is properly formatted
        yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)
        new_content = f"---\n{yaml_str}---\n\n{body}"

        result["new_frontmatter"] = frontmatter  # Store for display

        if dry_run:
            result["diff_preview"] = generate_diff_preview(original_content, new_content)
            logging.info(f"[DRY RUN] Would fix: {skill_path.relative_to(REPO_ROOT)}")
        else:
            # Backup original
            backup_path = BACKUP_DIR / skill_path.relative_to(REPO_ROOT)
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(skill_path, backup_path)

            # Write fixed content
            skill_path.write_text(new_content, encoding='utf-8')
            logging.info(f"Fixed: {skill_path.relative_to(REPO_ROOT)}")
            result["fixed"] = True

    return result


def generate_diff_preview(original: str, new: str, context_lines: int = 3) -> str:
    """Generate a simple diff preview."""
    orig_lines = original.split('\n')
    new_lines = new.split('\n')

    diff = []
    diff.append("--- Original")
    diff.append("+++ Fixed")

    # Simple line-by-line diff (not optimal but sufficient)
    max_len = max(len(orig_lines), len(new_lines))

    for i in range(max_len):
        orig_line = orig_lines[i] if i < len(orig_lines) else ""
        new_line = new_lines[i] if i < len(new_lines) else ""

        if orig_line != new_line:
            if orig_line:
                diff.append(f"- {orig_line}")
            if new_line:
                diff.append(f"+ {new_line}")

    return '\n'.join(diff[:50])  # Limit preview length


def find_non_compliant_skills() -> List[Path]:
    """Find all SKILL.md files that need fixing."""
    non_compliant = []

    for skill_file in SKILLS_DIR.rglob("SKILL.md"):
        try:
            content = skill_file.read_text(encoding='utf-8')
            frontmatter, body = extract_yaml_frontmatter(content)

            needs_fix = False

            # Check frontmatter
            if frontmatter is None:
                needs_fix = True
            else:
                # Check required fields
                if 'name' not in frontmatter or not frontmatter['name']:
                    needs_fix = True
                elif len(frontmatter['name']) > MAX_NAME_LENGTH:
                    needs_fix = True

                desc_value = frontmatter.get('description', '').strip()
                if not desc_value or desc_value.startswith('TODO'):
                    needs_fix = True
                elif len(desc_value) > MAX_DESCRIPTION_LENGTH:
                    needs_fix = True

            # Check token count
            token_count = estimate_tokens(content)
            if token_count > TOKEN_LIMIT:
                needs_fix = True

            if needs_fix:
                non_compliant.append(skill_file)

        except Exception as e:
            logging.error(f"Error checking {skill_file}: {e}")

    return non_compliant


def main():
    parser = argparse.ArgumentParser(
        description="Fix SKILL.md files for Anthropic API compliance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--skill',
        type=str,
        help="Path to specific skill directory (relative to skills/)"
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help="Fix all non-compliant skills"
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Preview changes without modifying files"
    )

    parser.add_argument(
        '--skip-token-optimization',
        action='store_true',
        help="Skip token count optimization (only fix fields)"
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)

    # Determine which skills to process
    skills_to_fix: List[Path] = []

    if args.skill:
        skill_path = SKILLS_DIR / args.skill / "SKILL.md"
        if not skill_path.exists():
            logging.error(f"Skill not found: {skill_path}")
            return 1
        skills_to_fix.append(skill_path)
    elif args.all:
        skills_to_fix = find_non_compliant_skills()
        logging.info(f"Found {len(skills_to_fix)} non-compliant skills")
    else:
        parser.print_help()
        return 0

    # Process skills
    results = []
    for skill_path in skills_to_fix:
        result = fix_skill_file(
            skill_path,
            dry_run=args.dry_run,
            skip_token_optimization=args.skip_token_optimization
        )
        result["skill"] = str(skill_path.relative_to(REPO_ROOT))
        results.append(result)

    # Summary report
    print("\n" + "="*80)
    print("SUMMARY REPORT")
    print("="*80)

    if args.dry_run:
        print("\n[DRY RUN MODE - No files were modified]\n")

    total = len(results)
    fixed = sum(1 for r in results if r["fixed"] or (r["issues_found"] and args.dry_run))

    print(f"\nTotal skills processed: {total}")
    print(f"Skills {'that would be ' if args.dry_run else ''}fixed: {fixed}")

    # Detailed breakdown
    print("\nIssues found:")
    issue_counts = {}
    for result in results:
        for issue in result["issues_found"]:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1

    if issue_counts:
        for issue, count in sorted(issue_counts.items(), key=lambda x: -x[1]):
            print(f"  - {issue}: {count}")
    else:
        print("  No issues found!")

    # Show what changes would be made
    if args.dry_run and results:
        print("\nChanges that would be made:")
        print("-" * 80)
        for result in results:
            if result["changes_made"]:
                print(f"\n{result['skill']}:")
                for change in result["changes_made"]:
                    print(f"  - {change}")

                # Show new frontmatter if available
                if result.get("new_frontmatter"):
                    print("  New frontmatter:")
                    for key, value in result["new_frontmatter"].items():
                        display_value = str(value)[:100]
                        if len(str(value)) > 100:
                            display_value += "..."
                        print(f"    {key}: {display_value}")

    # Show example files
    if args.dry_run and results and sum(1 for r in results if r["changes_made"]) > 0:
        print("\nExample: First 3 files that would be fixed:")
        print("-" * 80)
        count = 0
        for result in results:
            if result["changes_made"] and count < 3:
                print(f"\n{count + 1}. {result['skill']}")
                print(f"   Issues: {', '.join(result['issues_found'])}")
                count += 1

    print(f"\nLog file: {LOG_FILE}")
    if not args.dry_run and fixed > 0:
        print(f"Backups saved to: {BACKUP_DIR}")

    print("\n" + "="*80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
