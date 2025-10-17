#!/usr/bin/env python3
"""
Validate skills for proper structure, frontmatter, and progressive disclosure.

Checks:
- YAML frontmatter with name and description
- Level 1, 2, 3 sections present
- Token estimates within guidelines
- Required subdirectories exist
- Cross-references are valid
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml


class SkillValidator:
    """Validates skill structure and content."""

    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.skills_validated = 0

    def validate_all(self) -> bool:
        """Validate all skills in directory."""
        if not self.skills_dir.exists():
            print(f"❌ Skills directory not found: {self.skills_dir}")
            return False

        skill_dirs = [d for d in self.skills_dir.iterdir() if d.is_dir()]

        if not skill_dirs:
            print(f"⚠️  No skills found in {self.skills_dir}")
            return False

        print(f"🔍 Validating {len(skill_dirs)} skills...\n")

        all_valid = True
        for skill_dir in sorted(skill_dirs):
            if not self.validate_skill(skill_dir):
                all_valid = False

        return all_valid

    def validate_skill(self, skill_dir: Path) -> bool:
        """Validate a single skill."""
        skill_name = skill_dir.name
        print(f"Validating: {skill_name}")

        skill_file = skill_dir / "SKILL.md"

        # Check SKILL.md exists
        if not skill_file.exists():
            self.errors.append(f"{skill_name}: Missing SKILL.md")
            print(f"  ❌ Missing SKILL.md")
            return False

        # Read content
        with open(skill_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Validate frontmatter
        frontmatter_valid = self.validate_frontmatter(skill_name, content)

        # Validate structure
        structure_valid = self.validate_structure(skill_name, content)

        # Validate token estimates
        token_valid = self.validate_token_counts(skill_name, content)

        # Validate directories
        dirs_valid = self.validate_directories(skill_dir)

        # Validate cross-references
        refs_valid = self.validate_cross_references(skill_name, content)

        is_valid = (
            frontmatter_valid
            and structure_valid
            and token_valid
            and dirs_valid
            and refs_valid
        )

        if is_valid:
            print(f"  ✅ Valid\n")
        else:
            print(f"  ❌ Invalid\n")

        self.skills_validated += 1
        return is_valid

    def validate_frontmatter(self, skill_name: str, content: str) -> bool:
        """Validate YAML frontmatter."""
        frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)

        if not frontmatter_match:
            self.errors.append(f"{skill_name}: Missing YAML frontmatter")
            print("  ❌ Missing YAML frontmatter")
            return False

        try:
            frontmatter = yaml.safe_load(frontmatter_match.group(1))
        except yaml.YAMLError as e:
            self.errors.append(f"{skill_name}: Invalid YAML frontmatter: {e}")
            print(f"  ❌ Invalid YAML: {e}")
            return False

        # Check required fields
        valid = True

        if "name" not in frontmatter:
            self.errors.append(f"{skill_name}: Missing 'name' in frontmatter")
            print("  ❌ Missing 'name' field")
            valid = False
        elif frontmatter["name"] != skill_name:
            self.warnings.append(
                f"{skill_name}: Name mismatch (dir: {skill_name}, "
                f"frontmatter: {frontmatter['name']})"
            )
            print(
                f"  ⚠️  Name mismatch: {skill_name} != {frontmatter['name']}"
            )

        if "description" not in frontmatter:
            self.errors.append(f"{skill_name}: Missing 'description' in frontmatter")
            print("  ❌ Missing 'description' field")
            valid = False
        elif len(frontmatter["description"]) < 20:
            self.warnings.append(
                f"{skill_name}: Description too short "
                f"({len(frontmatter['description'])} chars)"
            )
            print("  ⚠️  Description too short")

        if valid:
            print("  ✅ Frontmatter valid")

        return valid

    def validate_structure(self, skill_name: str, content: str) -> bool:
        """Validate Level 1, 2, 3 structure."""
        valid = True

        # Check Level 1
        if "## Level 1: Quick Start" not in content:
            self.errors.append(f"{skill_name}: Missing 'Level 1: Quick Start' section")
            print("  ❌ Missing Level 1 section")
            valid = False

        # Check Level 2 (optional but recommended)
        if "## Level 2: Implementation" not in content:
            self.warnings.append(f"{skill_name}: Missing 'Level 2: Implementation' section")
            print("  ⚠️  Missing Level 2 section (recommended)")

        # Check Level 3 (optional)
        if "## Level 3: Mastery" not in content:
            self.warnings.append(f"{skill_name}: Missing 'Level 3: Mastery' section")
            print("  ⚠️  Missing Level 3 section (optional)")

        # Check Level 1 subsections
        level1_required = [
            "### What You'll Learn",
            "### Core Principles",
            "### Quick Reference",
            "### Essential Checklist",
        ]

        for subsection in level1_required:
            if subsection not in content:
                self.warnings.append(
                    f"{skill_name}: Missing recommended subsection: {subsection}"
                )
                print(f"  ⚠️  Missing {subsection}")

        if valid:
            print("  ✅ Structure valid")

        return valid

    def validate_token_counts(self, skill_name: str, content: str) -> bool:
        """Validate token counts for each level."""
        valid = True

        # Extract levels
        level1 = self.extract_level(content, 1)
        level2 = self.extract_level(content, 2)
        level3 = self.extract_level(content, 3)

        # Estimate tokens (rough: ~4 chars per token)
        level1_tokens = len(level1) // 4 if level1 else 0
        level2_tokens = len(level2) // 4 if level2 else 0
        level3_tokens = len(level3) // 4 if level3 else 0

        # Level 1 should be quick (< 2000 tokens for 5 min read)
        if level1_tokens > 2000:
            self.warnings.append(
                f"{skill_name}: Level 1 too long ({level1_tokens} tokens, "
                "recommended < 2000)"
            )
            print(f"  ⚠️  Level 1 too long: {level1_tokens} tokens")
            valid = False

        # Level 2 should be comprehensive but not overwhelming (< 5000 tokens)
        if level2_tokens > 5000:
            self.warnings.append(
                f"{skill_name}: Level 2 too long ({level2_tokens} tokens, "
                "recommended < 5000)"
            )
            print(f"  ⚠️  Level 2 too long: {level2_tokens} tokens")

        print(
            f"  ℹ️  Token estimates: L1={level1_tokens}, L2={level2_tokens}, "
            f"L3={level3_tokens}"
        )

        return valid

    def extract_level(self, content: str, level: int) -> str:
        """Extract content for a specific level."""
        pattern = rf"## Level {level}:.*?(?=## Level|\Z)"
        match = re.search(pattern, content, re.DOTALL)
        return match.group(0) if match else ""

    def validate_directories(self, skill_dir: Path) -> bool:
        """Validate required subdirectories exist."""
        required_dirs = ["templates", "scripts", "resources"]
        valid = True

        for dir_name in required_dirs:
            dir_path = skill_dir / dir_name
            if not dir_path.exists():
                self.warnings.append(
                    f"{skill_dir.name}: Missing '{dir_name}/' directory"
                )
                print(f"  ⚠️  Missing {dir_name}/ directory")

        return valid

    def validate_cross_references(self, skill_name: str, content: str) -> bool:
        """Validate cross-references to other skills."""
        valid = True

        # Find all skill references
        refs = re.findall(r"\.\./([^/]+)/SKILL\.md", content)

        for ref in refs:
            ref_path = self.skills_dir / ref / "SKILL.md"
            if not ref_path.exists():
                self.errors.append(
                    f"{skill_name}: Invalid reference to skill '{ref}'"
                )
                print(f"  ❌ Invalid reference: {ref}")
                valid = False

        return valid

    def print_summary(self) -> None:
        """Print validation summary."""
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Skills validated: {self.skills_validated}")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")

        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ All skills valid!")

    def export_report(self, output_path: Path) -> None:
        """Export validation report as JSON."""
        report = {
            "skills_validated": self.skills_validated,
            "errors": self.errors,
            "warnings": self.warnings,
            "valid": len(self.errors) == 0,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"\n📄 Report exported to: {output_path}")


def main():
    """Main validation entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print(__doc__)
        print("\nUsage: python validate-skills.py [--export report.json]")
        return

    # Get repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    skills_dir = repo_root / "skills"

    validator = SkillValidator(skills_dir)

    print("🔍 Skills Validation")
    print("=" * 60)
    print()

    all_valid = validator.validate_all()

    validator.print_summary()

    # Export report if requested
    if "--export" in sys.argv:
        idx = sys.argv.index("--export")
        if idx + 1 < len(sys.argv):
            output_path = Path(sys.argv[idx + 1])
            validator.export_report(output_path)

    # Exit with error code if validation failed
    sys.exit(0 if all_valid and not validator.errors else 1)


if __name__ == "__main__":
    main()
