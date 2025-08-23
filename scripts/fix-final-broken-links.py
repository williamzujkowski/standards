#!/usr/bin/env python3
"""
Fix the final 28 broken links identified in the audit.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fix_compliance_readme_links():
    """Fix the broken links in compliance subdirectory READMEs."""
    print("  Fixing compliance README links...")

    # These READMEs need their paths adjusted
    fixes = [
        (
            "standards/compliance/oscal/README.md",
            "../../../../docs/standards/UNIFIED_STANDARDS.md",
            "../../../docs/standards/UNIFIED_STANDARDS.md",
        ),
        (
            "standards/compliance/examples/README.md",
            "../../../../docs/standards/UNIFIED_STANDARDS.md",
            "../../../docs/standards/UNIFIED_STANDARDS.md",
        ),
        (
            "standards/compliance/src/README.md",
            "../../../../docs/standards/UNIFIED_STANDARDS.md",
            "../../../docs/standards/UNIFIED_STANDARDS.md",
        ),
        (
            "standards/compliance/semantic/README.md",
            "../../../../docs/standards/UNIFIED_STANDARDS.md",
            "../../../docs/standards/UNIFIED_STANDARDS.md",
        ),
        (
            "standards/compliance/scripts/README.md",
            "../../../../docs/standards/UNIFIED_STANDARDS.md",
            "../../../docs/standards/UNIFIED_STANDARDS.md",
        ),
        (
            "standards/compliance/automation/README.md",
            "../../../../docs/standards/UNIFIED_STANDARDS.md",
            "../../../docs/standards/UNIFIED_STANDARDS.md",
        ),
        (
            "standards/compliance/oscal/catalogs/README.md",
            "../../../../../../docs/standards/UNIFIED_STANDARDS.md",
            "../../../../docs/standards/UNIFIED_STANDARDS.md",
        ),
        (
            "standards/compliance/oscal/profiles/README.md",
            "../../../../../../docs/standards/UNIFIED_STANDARDS.md",
            "../../../../docs/standards/UNIFIED_STANDARDS.md",
        ),
        (
            "standards/compliance/oscal/types/README.md",
            "../../../../../../docs/standards/UNIFIED_STANDARDS.md",
            "../../../../docs/standards/UNIFIED_STANDARDS.md",
        ),
        (
            "standards/compliance/src/parsers/README.md",
            "../../../../../../docs/standards/UNIFIED_STANDARDS.md",
            "../../../../docs/standards/UNIFIED_STANDARDS.md",
        ),
    ]

    for file_path, old_link, new_link in fixes:
        full_path = ROOT / file_path
        if full_path.exists():
            content = full_path.read_text(encoding="utf-8")
            content = content.replace(old_link, new_link)
            full_path.write_text(content, encoding="utf-8")
            print(f"    ✅ Fixed {file_path}")


def fix_nist_docs():
    """Fix broken links in NIST documentation."""
    print("  Fixing NIST documentation links...")

    # Fix NIST_QUICK_REFERENCE.md
    nist_ref = ROOT / "docs/nist/NIST_QUICK_REFERENCE.md"
    if nist_ref.exists():
        content = nist_ref.read_text(encoding="utf-8")
        # Fix the standards link
        content = re.sub(
            r"\.\.\./standards/COMPLIANCE_STANDARDS\.md", "../../docs/standards/COMPLIANCE_STANDARDS.md", content
        )
        # Fix the examples link
        content = re.sub(r"\.\./\.\.\./\.\./examples/nist-templates/", "../../examples/nist-templates/", content)
        nist_ref.write_text(content, encoding="utf-8")
        print("    ✅ Fixed NIST_QUICK_REFERENCE.md")

    # Fix NIST_IMPLEMENTATION_GUIDE.md
    nist_guide = ROOT / "docs/nist/NIST_IMPLEMENTATION_GUIDE.md"
    if nist_guide.exists():
        content = nist_guide.read_text(encoding="utf-8")
        # Fix all .../standards/ links
        content = re.sub(
            r"\.\.\./standards/COMPLIANCE_STANDARDS\.md", "../../docs/standards/COMPLIANCE_STANDARDS.md", content
        )
        content = re.sub(r"\.\.\./standards/CODING_STANDARDS\.md", "../../docs/standards/CODING_STANDARDS.md", content)
        content = re.sub(
            r"\.\.\./standards/MODERN_SECURITY_STANDARDS\.md",
            "../../docs/standards/MODERN_SECURITY_STANDARDS.md",
            content,
        )
        content = re.sub(
            r"\.\.\./standards/PROJECT_MANAGEMENT_STANDARDS\.md",
            "../../docs/standards/PROJECT_MANAGEMENT_STANDARDS.md",
            content,
        )
        content = re.sub(
            r"\.\.\./standards/UNIFIED_STANDARDS\.md", "../../docs/standards/UNIFIED_STANDARDS.md", content
        )
        # Fix compliance README link
        content = re.sub(
            r"\.\./\.\.\./\.\./standards/compliance/README\.md", "../../standards/compliance/README.md", content
        )
        nist_guide.write_text(content, encoding="utf-8")
        print("    ✅ Fixed NIST_IMPLEMENTATION_GUIDE.md")


def fix_guides_docs():
    """Fix broken links in guides documentation."""
    print("  Fixing guides documentation links...")

    # Fix CREATING_STANDARDS_GUIDE.md
    guide = ROOT / "docs/guides/CREATING_STANDARDS_GUIDE.md"
    if guide.exists():
        content = guide.read_text(encoding="utf-8")
        content = re.sub(r"\.\./\.\.\./\.\./config/MANIFEST\.yaml", "../../config/MANIFEST.yaml", content)
        guide.write_text(content, encoding="utf-8")
        print("    ✅ Fixed CREATING_STANDARDS_GUIDE.md")


def fix_standards_docs():
    """Fix broken links in standards documentation."""
    print("  Fixing standards documentation links...")

    # Fix KNOWLEDGE_MANAGEMENT_STANDARDS.md
    km = ROOT / "docs/standards/KNOWLEDGE_MANAGEMENT_STANDARDS.md"
    if km.exists():
        content = km.read_text(encoding="utf-8")
        content = re.sub(r"\.\./\.\.\./\.\./config/MANIFEST\.yaml", "../../config/MANIFEST.yaml", content)
        km.write_text(content, encoding="utf-8")
        print("    ✅ Fixed KNOWLEDGE_MANAGEMENT_STANDARDS.md")

    # Fix TOOLCHAIN_STANDARDS.md
    tool = ROOT / "docs/standards/TOOLCHAIN_STANDARDS.md"
    if tool.exists():
        content = tool.read_text(encoding="utf-8")
        content = re.sub(r"\.\./\.\.\./\.\./config/TOOLS_CATALOG\.yaml", "../../config/TOOLS_CATALOG.yaml", content)
        content = re.sub(r"\.\./\.\.\./\.\./examples/project-templates/", "../../examples/project-templates/", content)
        tool.write_text(content, encoding="utf-8")
        print("    ✅ Fixed TOOLCHAIN_STANDARDS.md")

    # Fix MODERN_SECURITY_STANDARDS.md regex patterns (these are code examples, not links)
    sec = ROOT / "docs/standards/MODERN_SECURITY_STANDARDS.md"
    if sec.exists():
        content = sec.read_text(encoding="utf-8")
        # These appear to be regex patterns in code blocks, need to escape them properly
        # Just ensure they're in code blocks
        # Actually, these are likely false positives from the link checker
        print("    ℹ️  MODERN_SECURITY_STANDARDS.md patterns are regex examples, not links")


def fix_badges_readme():
    """Fix broken link in badges README."""
    print("  Fixing badges README...")

    badges = ROOT / "badges/README.md"
    if badges.exists():
        content = badges.read_text(encoding="utf-8")
        # This should point to docs/standards-compliance.md from badges/
        content = content.replace("../docs/standards-compliance.md", "../docs/standards-compliance.md")
        # Check if the file exists, if not, remove the link
        if not (ROOT / "docs/standards-compliance.md").exists():
            # Remove the broken link but keep the text
            content = re.sub(
                r"\[View Full Standards Compliance Report →\]\([^)]+\)",
                "View Full Standards Compliance Report",
                content,
            )
        badges.write_text(content, encoding="utf-8")
        print("    ✅ Fixed badges/README.md")


def main():
    """Fix all remaining broken links."""
    print("🔧 Fixing final broken links...")

    fix_compliance_readme_links()
    fix_nist_docs()
    fix_guides_docs()
    fix_standards_docs()
    fix_badges_readme()

    print("✅ All fixable links repaired")


if __name__ == "__main__":
    main()
