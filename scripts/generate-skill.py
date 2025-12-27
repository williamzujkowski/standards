#!/usr/bin/env python3
"""
Generate SKILL.md files from template with YAML frontmatter.

This script creates properly structured SKILL.md files following the
progressive disclosure pattern (Level 1/2/3) with YAML frontmatter.
"""

import argparse
import logging
import sys
from pathlib import Path

import yaml


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


SKILL_TEMPLATE = """---
name: "{name}"
description: "{description}"
---

# {name}

{description}

## Level 1: Quick Start (≤1000 tokens)

### Core Principles

- **Principle 1**: Brief description
- **Principle 2**: Brief description
- **Principle 3**: Brief description

### Quick Checklist

- [ ] Essential item 1
- [ ] Essential item 2
- [ ] Essential item 3

### When to Use

Brief guidance on when this skill applies.

---

## Level 2: Implementation Details (≤5000 tokens)

### Detailed Practices

#### Practice 1: [Name]

**Context**: When and why to use this practice.

**Implementation**:
1. Step one
2. Step two
3. Step three

**Example**:
```
# Code or configuration example
```

#### Practice 2: [Name]

**Context**: When and why to use this practice.

**Implementation**:
1. Step one
2. Step two
3. Step three

### Common Patterns

#### Pattern 1
Description and usage guidelines.

#### Pattern 2
Description and usage guidelines.

### Validation Checklist

- [ ] Implementation requirement 1
- [ ] Implementation requirement 2
- [ ] Implementation requirement 3

---

## Level 3: Advanced Topics & Resources (no limit)

### Deep Dive Topics

#### Advanced Topic 1
Detailed exploration of complex scenarios.

#### Advanced Topic 2
Detailed exploration of edge cases.

### Resources

- [Resource 1](./resources/resource1.md)
- [Resource 2](./resources/resource2.md)
- [Template](./templates/template1.yaml)

### Related Skills

- [Related Skill 1](../related-skill-1/SKILL.md)
- [Related Skill 2](../related-skill-2/SKILL.md)

### References

- External documentation links
- Standards references
- Best practice guides
"""


def validate_description_length(description: str, max_length: int = 1024) -> bool:
    """Validate that description is within token limit."""
    if len(description) > max_length:
        logger.error(f"Description exceeds {max_length} characters: {len(description)}")
        return False
    return True


def create_skill_directories(base_path: Path, skill_slug: str) -> Path:
    """Create skill directory structure."""
    skill_dir = base_path / skill_slug

    directories = [skill_dir, skill_dir / "templates", skill_dir / "scripts", skill_dir / "resources"]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")

    return skill_dir


def generate_skill_slug(name: str) -> str:
    """Generate URL-friendly skill slug from name."""
    return name.lower().replace(" ", "-").replace("_", "-")


def create_skill_file(skill_dir: Path, name: str, description: str, dry_run: bool = False) -> Path:
    """Create SKILL.md file with content."""
    skill_file = skill_dir / "SKILL.md"

    content = SKILL_TEMPLATE.format(name=name, description=description)

    if dry_run:
        logger.info(f"[DRY RUN] Would create: {skill_file}")
        logger.info(f"Content preview:\n{content[:500]}...")
        return skill_file

    skill_file.write_text(content)
    logger.info(f"Created skill file: {skill_file}")

    return skill_file


def validate_skill_structure(skill_file: Path) -> bool:
    """Validate the generated skill file structure."""
    content = skill_file.read_text()

    # Check for YAML frontmatter
    if not content.startswith("---"):
        logger.error("Missing YAML frontmatter")
        return False

    # Check for required sections
    required_sections = [
        "## Level 1: Quick Start",
        "## Level 2: Implementation Details",
        "## Level 3: Advanced Topics & Resources",
    ]

    for section in required_sections:
        if section not in content:
            logger.error(f"Missing required section: {section}")
            return False

    # Validate YAML frontmatter
    try:
        parts = content.split("---", 2)
        if len(parts) < 3:
            logger.error("Invalid YAML frontmatter structure")
            return False

        frontmatter = yaml.safe_load(parts[1])
        if not frontmatter.get("name"):
            logger.error("Missing 'name' in frontmatter")
            return False
        if not frontmatter.get("description"):
            logger.error("Missing 'description' in frontmatter")
            return False

    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML frontmatter: {e}")
        return False

    logger.info("Skill structure validation passed")
    return True


def create_readme(skill_dir: Path, name: str, description: str, dry_run: bool = False):
    """Create README.md for the skill."""
    readme_path = skill_dir / "README.md"

    readme_content = f"""# {name}

{description}

## Structure

- `SKILL.md` - Main skill documentation (progressive disclosure)
- `templates/` - Reusable templates
- `scripts/` - Automation scripts
- `resources/` - Supporting documentation

## Usage

See [SKILL.md](./SKILL.md) for detailed skill documentation.
"""

    if dry_run:
        logger.info(f"[DRY RUN] Would create: {readme_path}")
        return

    readme_path.write_text(readme_content)
    logger.info(f"Created README: {readme_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate SKILL.md files from template with YAML frontmatter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a new skill
  python3 generate-skill.py --name "API Security" \\
    --description "Security practices for REST APIs" \\
    --category security

  # Dry run to preview
  python3 generate-skill.py --name "Test Skill" \\
    --description "Test description" --dry-run

  # Specify output directory
  python3 generate-skill.py --name "My Skill" \\
    --description "Description" \\
    --output-dir /path/to/skills
        """,
    )

    parser.add_argument("--name", required=True, help="Skill name (e.g., 'API Security')")

    parser.add_argument("--description", required=True, help="Skill description (≤1024 characters)")

    parser.add_argument("--category", help="Skill category (e.g., security, testing, development)")

    parser.add_argument(
        "--output-dir", type=Path, default=Path("skills"), help="Output directory for skills (default: ./skills)"
    )

    parser.add_argument("--dry-run", action="store_true", help="Preview without creating files")

    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    parser.add_argument("--validate", action="store_true", help="Validate generated skill structure")

    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Validate description length
    if not validate_description_length(args.description):
        sys.exit(1)

    # Generate skill slug
    skill_slug = generate_skill_slug(args.name)
    logger.info(f"Generated skill slug: {skill_slug}")

    # Create directory structure
    try:
        skill_dir = create_skill_directories(args.output_dir, skill_slug)
    except Exception as e:
        logger.error(f"Failed to create directories: {e}")
        sys.exit(1)

    # Create skill file
    try:
        skill_file = create_skill_file(skill_dir, args.name, args.description, dry_run=args.dry_run)
    except Exception as e:
        logger.error(f"Failed to create skill file: {e}")
        sys.exit(1)

    # Create README
    try:
        create_readme(skill_dir, args.name, args.description, dry_run=args.dry_run)
    except Exception as e:
        logger.error(f"Failed to create README: {e}")
        sys.exit(1)

    # Validate if requested
    if args.validate and not args.dry_run:
        if not validate_skill_structure(skill_file):
            logger.error("Skill validation failed")
            sys.exit(1)

    if not args.dry_run:
        logger.info(f"✓ Skill '{args.name}' created successfully at {skill_dir}")
        logger.info(f"  Edit: {skill_file}")
    else:
        logger.info("[DRY RUN] No files were created")

    return 0


if __name__ == "__main__":
    sys.exit(main())
