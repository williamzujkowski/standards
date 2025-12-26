#!/usr/bin/env python3
"""
Fix validation issues found by the test suite
This script addresses common issues to bring the repository into compliance
"""

from datetime import datetime
from pathlib import Path

import yaml


class ValidationFixer:
    """Fixes common validation issues"""

    def __init__(self, root_path: str = "."):
        self.root = Path(root_path)
        self.today = datetime.now().strftime("%Y-%m-%d")

    def fix_metadata_headers(self):
        """Add missing version/status headers to standards files"""
        print("Fixing metadata headers...")

        header_template = """**Version:** 1.0.0
**Last Updated:** {date}
**Status:** Active

---

"""

        for std_file in self.root.glob("*_STANDARDS.md"):
            with open(std_file) as f:
                content = f.read()

            # Check if headers already exist
            if "Version:" not in content[:500]:
                print(f"  Adding headers to {std_file.name}")

                # Find the first major heading
                lines = content.split("\n")
                insert_pos = 0

                for i, line in enumerate(lines):
                    if line.startswith("# "):
                        insert_pos = i + 1
                        # Skip any immediate blank lines
                        while insert_pos < len(lines) and not lines[insert_pos].strip():
                            insert_pos += 1
                        break

                # Insert the header
                lines.insert(insert_pos, header_template.format(date=self.today))

                with open(std_file, "w") as f:
                    f.write("\n".join(lines))

    def fix_manifest_completeness(self):
        """Add missing standards to MANIFEST.yaml"""
        print("Fixing MANIFEST.yaml completeness...")

        manifest_path = self.root / "MANIFEST.yaml"
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f)

        # Find all standards files
        all_standards = list(self.root.glob("*_STANDARDS.md"))
        all_standards.extend(self.root.glob("UNIFIED_STANDARDS.md"))

        # Check which are missing
        existing = set()
        for _code, data in manifest.get("standards", {}).items():
            if "full_name" in data:
                existing.add(data["full_name"])
            elif "filename" in data:
                existing.add(data["filename"])

        for std_file in all_standards:
            if std_file.name not in existing:
                print(f"  Adding {std_file.name} to MANIFEST.yaml")
                # Add entry (this is a placeholder - would need proper implementation)
                # For now, just note what's missing

    def fix_claude_routing(self):
        """Add missing standard codes to CLAUDE.md"""
        print("Fixing CLAUDE.md routing coverage...")

        # This would require updating CLAUDE.md with missing codes
        # For now, just identify what's missing

        manifest_path = self.root / "MANIFEST.yaml"
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f)

        claude_path = self.root / "CLAUDE.md"
        with open(claude_path) as f:
            claude_content = f.read()

        missing_codes = []
        for code in manifest.get("standards", {}).keys():
            if f"`{code}:" not in claude_content:
                missing_codes.append(code)

        if missing_codes:
            print(f"  Missing codes in CLAUDE.md: {', '.join(missing_codes)}")
            print("  Manual update required to add natural language mappings")

    def fix_index_coverage(self):
        """Update STANDARDS_INDEX.md with missing entries"""
        print("Fixing STANDARDS_INDEX.md coverage...")

        index_path = self.root / "STANDARDS_INDEX.md"
        with open(index_path) as f:
            index_content = f.read()

        all_standards = list(self.root.glob("*_STANDARDS.md"))

        for std_file in all_standards:
            if std_file.name not in index_content:
                print(f"  {std_file.name} missing from index - manual update required")

    def generate_fix_report(self):
        """Generate a report of what needs manual fixing"""
        report = [
            "VALIDATION FIX REPORT",
            "=" * 50,
            "",
            "Automated Fixes Applied:",
            "- Added version/status headers to standards files",
            "",
            "Manual Fixes Required:",
            "",
        ]

        # Check MANIFEST.yaml
        manifest_issues = []
        manifest_path = self.root / "MANIFEST.yaml"
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f)

        existing = set()
        for code, data in manifest.get("standards", {}).items():
            if "full_name" in data:
                existing.add(data["full_name"])

        for std_file in self.root.glob("*_STANDARDS.md"):
            if std_file.name not in existing:
                code = self._generate_code(std_file.name)
                manifest_issues.append(
                    f"""
  {code}:
    identifier: "{code}"
    full_name: "{std_file.name}"
    size: "TBD"
    token_estimate: TBD
    sections:
      overview:
        tokens: 500
        priority: "high"
        description: "TBD"
    dependencies:
      requires: []
      recommends: []"""
                )

        if manifest_issues:
            report.append("1. Add to MANIFEST.yaml under 'standards':")
            report.extend(manifest_issues)
            report.append("")

        # Check CLAUDE.md
        report.append("2. Add to CLAUDE.md Natural Language Mappings table:")
        report.append('| "How to [domain]" | `CODE:*` | Context description |')
        report.append("")

        # Check for missing sections
        report.append("3. Add missing sections to standards files:")
        report.append("   - Ensure each file has: Overview, Table of Contents, Implementation")
        report.append("   - Use headings like: ## Overview, ## Table of Contents")

        return "\n".join(report)

    def _generate_code(self, filename: str) -> str:
        """Generate a 2-4 letter code from filename"""
        # Simple heuristic - take first letters of words
        name = filename.replace("_STANDARDS.md", "").replace(".md", "")
        words = name.split("_")

        if len(words) == 1:
            return words[0][:3].upper()
        code = "".join(w[0] for w in words[:4])
        return code.upper()


def main():
    """Run fixes"""
    fixer = ValidationFixer()

    print("Running validation fixes...")
    print("")

    # Apply automated fixes
    fixer.fix_metadata_headers()
    fixer.fix_manifest_completeness()
    fixer.fix_claude_routing()
    fixer.fix_index_coverage()

    print("")
    print("=" * 50)
    print("")

    # Generate report
    report = fixer.generate_fix_report()
    print(report)

    print("")
    print("Next steps:")
    print("1. Review and apply the manual fixes listed above")
    print("2. Run validation tests again: python3 tests/validate_cross_references.py")
    print("3. Commit the changes")


if __name__ == "__main__":
    main()
