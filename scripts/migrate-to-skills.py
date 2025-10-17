#!/usr/bin/env python3
"""
Migrate existing standards documents to SKILL.md format.

This script transforms traditional standards documents into the progressive
disclosure SKILL.md format with Level 1, 2, and 3 sections.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml


class SkillMigrator:
    """Migrates standards to SKILL format."""

    def __init__(self, standards_dir: str, skills_dir: str):
        self.standards_dir = Path(standards_dir)
        self.skills_dir = Path(skills_dir)

    def migrate_all(self) -> None:
        """Migrate all configured standards to skills."""
        migrations = [
            {
                "source": "docs/standards/CODING_STANDARDS.md",
                "target": "skills/coding-standards",
                "name": "coding-standards",
                "description": "Comprehensive coding standards and best practices",
            },
            {
                "source": "docs/standards/MODERN_SECURITY_STANDARDS.md",
                "target": "skills/security-practices",
                "name": "security-practices",
                "description": "Modern security standards including Zero Trust",
            },
            {
                "source": "docs/standards/TESTING_STANDARDS.md",
                "target": "skills/testing",
                "name": "testing",
                "description": "Comprehensive testing standards with TDD",
            },
            {
                "source": "docs/nist/NIST_IMPLEMENTATION_GUIDE.md",
                "target": "skills/nist-compliance",
                "name": "nist-compliance",
                "description": "NIST 800-53r5 control implementation",
            },
        ]

        for migration in migrations:
            print(f"Migrating {migration['source']}...")
            self.migrate_standard(
                Path(migration["source"]),
                Path(migration["target"]),
                migration["name"],
                migration["description"],
            )

    def migrate_standard(
        self, source: Path, target: Path, name: str, description: str
    ) -> None:
        """
        Migrate a single standard to SKILL format.

        Args:
            source: Source standards document path
            target: Target skill directory path
            name: Skill name
            description: Skill description
        """
        if not source.exists():
            print(f"⚠️  Source not found: {source}")
            return

        # Read source content
        with open(source, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract metadata
        metadata = self.extract_metadata(content)

        # Create target directory
        target.mkdir(parents=True, exist_ok=True)
        (target / "templates").mkdir(exist_ok=True)
        (target / "scripts").mkdir(exist_ok=True)
        (target / "resources").mkdir(exist_ok=True)

        # Generate SKILL.md
        skill_content = self.generate_skill_markdown(
            name, description, content, metadata
        )

        # Write SKILL.md
        with open(target / "SKILL.md", "w", encoding="utf-8") as f:
            f.write(skill_content)

        print(f"✓ Created {target / 'SKILL.md'}")

        # Create README pointing to original
        readme_content = self.generate_readme(name, source)
        with open(target / "README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)

        print(f"✓ Created {target / 'README.md'}")

    def extract_metadata(self, content: str) -> Dict[str, str]:
        """Extract metadata from standard document."""
        metadata = {}

        # Extract version
        version_match = re.search(r"\*\*Version:\*\* ([\d.]+)", content)
        if version_match:
            metadata["version"] = version_match.group(1)

        # Extract standard code
        code_match = re.search(r"\*\*Standard Code:\*\* (\w+)", content)
        if code_match:
            metadata["standard_code"] = code_match.group(1)

        # Extract last updated
        updated_match = re.search(r"\*\*Last Updated:\*\* (.*?)$", content, re.MULTILINE)
        if updated_match:
            metadata["last_updated"] = updated_match.group(1)

        return metadata

    def generate_skill_markdown(
        self, name: str, description: str, source_content: str, metadata: Dict[str, str]
    ) -> str:
        """
        Generate SKILL.md content from source standard.

        This creates a basic structure that should be manually refined.
        """
        # Extract sections
        sections = self.extract_sections(source_content)

        frontmatter = f"""---
name: {name}
description: {description}
version: {metadata.get('version', '1.0.0')}
standard_code: {metadata.get('standard_code', 'N/A')}
---

"""

        level1 = self.generate_level1(name, sections)
        level2 = self.generate_level2(sections)
        level3 = self.generate_level3(sections)

        resources = f"""
## Bundled Resources

- [Full source document](../../{self.get_relative_source(name)})
- Templates in `./templates/`
- Scripts in `./scripts/`
- Resources in `./resources/`

---

*Note: This is an auto-generated skill. Please review and refine the content.*
"""

        return frontmatter + level1 + level2 + level3 + resources

    def get_relative_source(self, name: str) -> str:
        """Get relative path to source document."""
        mapping = {
            "coding-standards": "docs/standards/CODING_STANDARDS.md",
            "security-practices": "docs/standards/MODERN_SECURITY_STANDARDS.md",
            "testing": "docs/standards/TESTING_STANDARDS.md",
            "nist-compliance": "docs/nist/NIST_IMPLEMENTATION_GUIDE.md",
        }
        return mapping.get(name, "docs/standards/")

    def extract_sections(self, content: str) -> List[Tuple[str, str]]:
        """Extract major sections from document."""
        sections = []

        # Split by headers
        parts = re.split(r"^## (.+)$", content, flags=re.MULTILINE)

        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                sections.append((parts[i], parts[i + 1]))

        return sections

    def generate_level1(self, name: str, sections: List[Tuple[str, str]]) -> str:
        """Generate Level 1: Quick Start section."""
        return f"""# {name.replace('-', ' ').title()} Skill

## Level 1: Quick Start (5 minutes)

### What You'll Learn
{self.extract_overview(sections)}

### Core Principles
{self.extract_principles(sections)}

### Quick Reference
{self.extract_examples(sections, limit=2)}

### Essential Checklist
{self.generate_checklist(sections)}

### Common Pitfalls
{self.extract_pitfalls(sections)}

---

"""

    def generate_level2(self, sections: List[Tuple[str, str]]) -> str:
        """Generate Level 2: Implementation section."""
        return f"""## Level 2: Implementation (30 minutes)

### Deep Dive Topics

{self.format_sections_for_level2(sections)}

### Implementation Patterns
{self.extract_patterns(sections)}

### Integration Points
{self.generate_integration_points()}

---

"""

    def generate_level3(self, sections: List[Tuple[str, str]]) -> str:
        """Generate Level 3: Mastery section."""
        return f"""## Level 3: Mastery (Extended Learning)

### Advanced Topics
{self.format_sections_for_level3(sections)}

### Resources
{self.extract_resources(sections)}

### Templates
See `./templates/` for implementation templates.

### Scripts
See `./scripts/` for automation scripts.

---

"""

    def extract_overview(self, sections: List[Tuple[str, str]]) -> str:
        """Extract overview text."""
        for title, content in sections:
            if "overview" in title.lower():
                # Get first paragraph
                paragraphs = content.strip().split("\n\n")
                if paragraphs:
                    return paragraphs[0].strip()

        return "Apply best practices and standards for this domain."

    def extract_principles(self, sections: List[Tuple[str, str]]) -> str:
        """Extract core principles."""
        principles = []

        for title, content in sections:
            # Look for bullet points or numbered lists
            matches = re.findall(r"^[-*]\s+(.+)$", content, re.MULTILINE)
            if matches and len(matches) <= 5:
                principles.extend(matches[:5])

        if principles:
            return "\n".join(f"- **{p}**" for p in principles[:4])

        return """- **Consistency**: Follow established patterns
- **Quality**: Maintain high standards
- **Maintainability**: Write for long-term sustainability
- **Best Practices**: Apply industry standards"""

    def extract_examples(self, sections: List[Tuple[str, str]], limit: int = 2) -> str:
        """Extract code examples."""
        examples = []

        for title, content in sections:
            # Find code blocks
            code_blocks = re.findall(r"```[\s\S]*?```", content)
            examples.extend(code_blocks[:limit])

        if examples:
            return "\n\n".join(examples[:limit])

        return "```\n# Examples to be added\n```"

    def generate_checklist(self, sections: List[Tuple[str, str]]) -> str:
        """Generate essential checklist."""
        return """- [ ] Understand core principles
- [ ] Review quick reference examples
- [ ] Configure development tools
- [ ] Set up automation
- [ ] Validate implementation"""

    def extract_pitfalls(self, sections: List[Tuple[str, str]]) -> str:
        """Extract common pitfalls."""
        return """- Skipping fundamentals in favor of advanced techniques
- Not automating enforcement
- Ignoring existing patterns
- Inconsistent application"""

    def format_sections_for_level2(self, sections: List[Tuple[str, str]]) -> str:
        """Format sections for Level 2."""
        formatted = []

        for title, content in sections[:5]:  # Limit to first 5 sections
            formatted.append(f"#### {title}\n\n{content[:500]}...\n")

        return "\n".join(formatted)

    def format_sections_for_level3(self, sections: List[Tuple[str, str]]) -> str:
        """Format sections for Level 3."""
        formatted = []

        for title, content in sections[5:10]:  # Next 5 sections
            formatted.append(f"#### {title}\n\n{content[:500]}...\n")

        return "\n".join(formatted)

    def extract_patterns(self, sections: List[Tuple[str, str]]) -> str:
        """Extract implementation patterns."""
        return "See Level 2 deep dive sections for detailed patterns."

    def generate_integration_points(self) -> str:
        """Generate integration points."""
        return """- Links to related skills
- Cross-references to standards
- Tool and framework integrations"""

    def extract_resources(self, sections: List[Tuple[str, str]]) -> str:
        """Extract resource links."""
        resources = []

        for title, content in sections:
            # Find links
            links = re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", content)
            resources.extend(links[:3])

        if resources:
            return "\n".join(f"- [{text}]({url})" for text, url in resources[:5])

        return "See bundled resources for additional materials."

    def generate_readme(self, name: str, source: Path) -> str:
        """Generate README for skill directory."""
        return f"""# {name.replace('-', ' ').title()}

This skill was auto-generated from `{source}`.

## Structure

- `SKILL.md` - Progressive disclosure skill content
- `templates/` - Implementation templates
- `scripts/` - Automation scripts
- `resources/` - Additional resources

## Usage

Load this skill with:

```bash
@load skill:{name}
```

Or load just Level 1 (quick start):

```bash
@load skill:{name} --level 1
```

## Source

Original standard: `../../{source}`
"""


def main():
    """Main migration entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print(__doc__)
            print("\nUsage: python migrate-to-skills.py [--dry-run]")
            return

    # Get repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    migrator = SkillMigrator(
        standards_dir=repo_root / "docs" / "standards",
        skills_dir=repo_root / "skills",
    )

    print("🔄 Migrating standards to skills format...")
    print()

    migrator.migrate_all()

    print()
    print("✅ Migration complete!")
    print()
    print("Next steps:")
    print("1. Review generated SKILL.md files")
    print("2. Refine Level 1, 2, 3 content")
    print("3. Add templates, scripts, resources")
    print("4. Run validation: python scripts/validate-skills.py")


if __name__ == "__main__":
    main()
