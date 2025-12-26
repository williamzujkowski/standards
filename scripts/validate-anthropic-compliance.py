#!/usr/bin/env python3
"""
Validate SKILL.md files against Anthropic's canonical format.

Requirements from Anthropic's official spec:
1. File Structure: Directory with SKILL.md file
2. YAML Frontmatter Required Fields:
   - name: max 64 chars, lowercase letters/numbers/hyphens only, no XML tags, no reserved words
   - description: non-empty, max 1024 chars, no XML tags
3. Level 2 Size: Main body should be <5k tokens
4. Optional Files: FORMS.md, REFERENCE.md, scripts/ directory

Reserved words: skill, name, description, content, type, version
"""

import re
import sys
from pathlib import Path

import yaml


class SkillValidator:
    """Validator for Anthropic SKILL.md compliance."""

    RESERVED_WORDS = {"skill", "name", "description", "content", "type", "version"}
    XML_TAG_PATTERN = re.compile(r"<[^>]+>")
    NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")
    MAX_NAME_LENGTH = 64
    MAX_DESCRIPTION_LENGTH = 1024
    MAX_LEVEL2_TOKENS = 5000

    # Approximate tokens: 1 token ≈ 4 characters (OpenAI estimation)
    CHARS_PER_TOKEN = 4

    def __init__(self, skills_dir: Path):
        """Initialize validator with skills directory."""
        self.skills_dir = skills_dir
        self.results = {"compliant": [], "non_compliant": [], "total": 0, "errors": []}

    def validate_all_skills(self) -> dict:
        """Validate all SKILL.md files in the skills directory."""
        skill_files = list(self.skills_dir.rglob("SKILL.md"))
        self.results["total"] = len(skill_files)

        for skill_file in sorted(skill_files):
            self._validate_skill(skill_file)

        return self.results

    def _validate_skill(self, skill_file: Path):
        """Validate a single SKILL.md file."""
        relative_path = skill_file.relative_to(self.skills_dir)
        issues = []

        try:
            content = skill_file.read_text(encoding="utf-8")

            # Extract YAML frontmatter
            frontmatter, body = self._extract_frontmatter(content)

            if frontmatter is None:
                issues.append("Missing or invalid YAML frontmatter")
                self.results["non_compliant"].append({"path": str(relative_path), "issues": issues})
                return

            # Validate required fields
            issues.extend(self._validate_frontmatter(frontmatter))

            # Validate Level 2 token count
            level2_issues = self._validate_level2_tokens(body)
            issues.extend(level2_issues)

            # Validate file structure
            structure_issues = self._validate_file_structure(skill_file.parent)
            issues.extend(structure_issues)

            # Record results
            if issues:
                self.results["non_compliant"].append({"path": str(relative_path), "issues": issues})
            else:
                self.results["compliant"].append(str(relative_path))

        except Exception as e:
            self.results["errors"].append({"path": str(relative_path), "error": str(e)})

    def _extract_frontmatter(self, content: str) -> tuple[dict, str]:
        """Extract YAML frontmatter and body from content."""
        if not content.startswith("---"):
            return None, content

        parts = content.split("---", 2)
        if len(parts) < 3:
            return None, content

        try:
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2]
            return frontmatter, body
        except yaml.YAMLError:
            return None, content

    def _validate_frontmatter(self, frontmatter: dict) -> list[str]:
        """Validate YAML frontmatter fields."""
        issues = []

        # Check required fields
        if "name" not in frontmatter:
            issues.append("Missing required field: 'name'")
        else:
            issues.extend(self._validate_name(frontmatter["name"]))

        if "description" not in frontmatter:
            issues.append("Missing required field: 'description'")
        else:
            issues.extend(self._validate_description(frontmatter["description"]))

        return issues

    def _validate_name(self, name: str) -> list[str]:
        """Validate the 'name' field."""
        issues = []

        if not name or not isinstance(name, str):
            issues.append("Name must be a non-empty string")
            return issues

        # Check length
        if len(name) > self.MAX_NAME_LENGTH:
            issues.append(f"Name exceeds {self.MAX_NAME_LENGTH} characters (current: {len(name)})")

        # Check format (lowercase letters, numbers, hyphens only)
        if not self.NAME_PATTERN.match(name):
            issues.append(
                f"Name '{name}' contains invalid characters (only lowercase letters, numbers, hyphens allowed)"
            )

        # Check for XML tags
        if self.XML_TAG_PATTERN.search(name):
            issues.append("Name contains XML tags")

        # Check for reserved words
        if name.lower() in self.RESERVED_WORDS:
            issues.append(f"Name '{name}' is a reserved word")

        return issues

    def _validate_description(self, description: str) -> list[str]:
        """Validate the 'description' field."""
        issues = []

        if not description or not isinstance(description, str):
            issues.append("Description must be a non-empty string")
            return issues

        # Check length
        if len(description) > self.MAX_DESCRIPTION_LENGTH:
            issues.append(f"Description exceeds {self.MAX_DESCRIPTION_LENGTH} characters (current: {len(description)})")

        # Check for XML tags
        if self.XML_TAG_PATTERN.search(description):
            issues.append("Description contains XML tags")

        return issues

    def _validate_level2_tokens(self, body: str) -> list[str]:
        """Validate Level 2 section token count."""
        issues = []

        # Extract Level 2 section
        level2_match = re.search(r"## Level 2:.*?(?=## Level 3:|$)", body, re.DOTALL | re.IGNORECASE)

        if not level2_match:
            # No Level 2 section found - not necessarily an error
            return issues

        level2_content = level2_match.group(0)

        # Estimate tokens (rough approximation)
        estimated_tokens = len(level2_content) // self.CHARS_PER_TOKEN

        if estimated_tokens > self.MAX_LEVEL2_TOKENS:
            issues.append(
                f"Level 2 section exceeds {self.MAX_LEVEL2_TOKENS} tokens "
                f"(estimated: {estimated_tokens} tokens, {len(level2_content)} chars)"
            )

        return issues

    def _validate_file_structure(self, skill_dir: Path) -> list[str]:
        """Validate optional file structure (FORMS.md, REFERENCE.md, scripts/)."""
        # This is informational only - optional files don't cause compliance failure
        # Just noting if they exist for completeness
        return []

    def generate_report(self, output_file: Path) -> None:
        """Generate markdown compliance report."""
        report = [
            "# Anthropic SKILL.md Compliance Report",
            "",
            f"**Generated**: {Path(__file__).name}",
            f"**Total Skills**: {self.results['total']}",
            f"**Compliant**: {len(self.results['compliant'])}",
            f"**Non-Compliant**: {len(self.results['non_compliant'])}",
            f"**Errors**: {len(self.results['errors'])}",
            "",
            "## Summary",
            "",
            f"- ✅ Compliant: {len(self.results['compliant'])} / {self.results['total']} "
            f"({len(self.results['compliant']) / self.results['total'] * 100:.1f}%)",
            f"- ❌ Non-Compliant: {len(self.results['non_compliant'])} / {self.results['total']} "
            f"({len(self.results['non_compliant']) / self.results['total'] * 100:.1f}%)",
            "",
            "## Anthropic Requirements",
            "",
            "### Required",
            "",
            "1. **YAML Frontmatter**:",
            "   - `name`: max 64 chars, lowercase letters/numbers/hyphens only",
            "   - `description`: max 1024 chars, non-empty",
            "   - No XML tags in either field",
            "   - Name cannot be reserved word (skill, name, description, content, type, version)",
            "",
            "2. **Level 2 Section**: <5,000 tokens (~20,000 characters)",
            "",
            "### Optional",
            "",
            "- FORMS.md file",
            "- REFERENCE.md file",
            "- scripts/ directory",
            "",
            "---",
            "",
        ]

        # Compliant skills
        if self.results["compliant"]:
            report.append("## ✅ Compliant Skills")
            report.append("")
            for skill in self.results["compliant"]:
                report.append(f"- `{skill}`")
            report.append("")

        # Non-compliant skills
        if self.results["non_compliant"]:
            report.append("## ❌ Non-Compliant Skills")
            report.append("")
            for item in self.results["non_compliant"]:
                report.append(f"### `{item['path']}`")
                report.append("")
                for issue in item["issues"]:
                    report.append(f"- ⚠️ {issue}")
                report.append("")

        # Errors
        if self.results["errors"]:
            report.append("## 🔥 Errors During Validation")
            report.append("")
            for item in self.results["errors"]:
                report.append(f"### `{item['path']}`")
                report.append("")
                report.append("```")
                report.append(f"{item['error']}")
                report.append("```")
                report.append("")

        # Recommendations
        report.append("## Recommendations")
        report.append("")

        if self.results["non_compliant"]:
            report.append("### Priority Fixes")
            report.append("")

            # Collect common issues
            name_issues = []
            description_issues = []
            token_issues = []

            for item in self.results["non_compliant"]:
                for issue in item["issues"]:
                    if "name" in issue.lower():
                        name_issues.append(item["path"])
                    elif "description" in issue.lower():
                        description_issues.append(item["path"])
                    elif "token" in issue.lower():
                        token_issues.append(item["path"])

            if name_issues:
                report.append(f"1. **Fix Name Field Issues** ({len(name_issues)} skills)")
                report.append("   - Ensure lowercase letters, numbers, hyphens only")
                report.append("   - Keep under 64 characters")
                report.append("   - Avoid reserved words")
                report.append("")

            if description_issues:
                report.append(f"2. **Fix Description Field Issues** ({len(description_issues)} skills)")
                report.append("   - Keep under 1024 characters")
                report.append("   - Remove XML tags")
                report.append("")

            if token_issues:
                report.append(f"3. **Reduce Level 2 Token Count** ({len(token_issues)} skills)")
                report.append("   - Target: <5,000 tokens (~20,000 characters)")
                report.append("   - Move detailed content to Level 3 or REFERENCE.md")
                report.append("")
        else:
            report.append("✨ All skills are compliant with Anthropic's canonical format!")
            report.append("")

        # Write report
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text("\n".join(report), encoding="utf-8")


def main():
    """Main entry point."""
    # Determine skills directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    skills_dir = repo_root / "skills"

    if not skills_dir.exists():
        print(f"❌ Skills directory not found: {skills_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"🔍 Validating skills in: {skills_dir}")

    # Run validation
    validator = SkillValidator(skills_dir)
    results = validator.validate_all_skills()

    # Generate report
    report_file = repo_root / "reports" / "generated" / "anthropic-compliance-report.md"
    validator.generate_report(report_file)

    # Print summary
    print("\n📊 Validation Complete:")
    print(f"   Total: {results['total']}")
    print(f"   ✅ Compliant: {len(results['compliant'])}")
    print(f"   ❌ Non-Compliant: {len(results['non_compliant'])}")
    print(f"   🔥 Errors: {len(results['errors'])}")
    print(f"\n📄 Report generated: {report_file}")

    # Exit with error code if non-compliant
    if results["non_compliant"] or results["errors"]:
        sys.exit(1)
    else:
        print("\n✨ All skills are compliant!")
        sys.exit(0)


if __name__ == "__main__":
    main()
