#!/usr/bin/env python3
"""Update all script paths to match new directory structure"""

from pathlib import Path


def update_file(file_path, replacements):
    """Update a file with the given replacements"""
    with open(file_path, "r") as f:
        content = f.read()

    original = content
    for old, new in replacements:
        content = content.replace(old, new)

    if content != original:
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Updated: {file_path}")
        return True
    return False


# Define replacements for each file type
badge_replacements = [
    # Update all GitHub URLs to include docs/standards/
    (
        "/blob/master/CODING_STANDARDS.md",
        "/blob/master/docs/standards/CODING_STANDARDS.md",
    ),
    (
        "/blob/master/TESTING_STANDARDS.md",
        "/blob/master/docs/standards/TESTING_STANDARDS.md",
    ),
    (
        "/blob/master/MODERN_SECURITY_STANDARDS.md",
        "/blob/master/docs/standards/MODERN_SECURITY_STANDARDS.md",
    ),
    (
        "/blob/master/SEO_WEB_MARKETING_STANDARDS.md",
        "/blob/master/docs/standards/SEO_WEB_MARKETING_STANDARDS.md",
    ),
    (
        "/blob/master/LEGAL_COMPLIANCE_STANDARDS.md",
        "/blob/master/docs/standards/LEGAL_COMPLIANCE_STANDARDS.md",
    ),
    (
        "/blob/master/PROJECT_MANAGEMENT_STANDARDS.md",
        "/blob/master/docs/standards/PROJECT_MANAGEMENT_STANDARDS.md",
    ),
    (
        "/blob/master/DEVOPS_PLATFORM_STANDARDS.md",
        "/blob/master/docs/standards/DEVOPS_PLATFORM_STANDARDS.md",
    ),
    (
        "/blob/master/OBSERVABILITY_STANDARDS.md",
        "/blob/master/docs/standards/OBSERVABILITY_STANDARDS.md",
    ),
    (
        "/blob/master/FRONTEND_MOBILE_STANDARDS.md",
        "/blob/master/docs/standards/FRONTEND_MOBILE_STANDARDS.md",
    ),
    (
        "/blob/master/CLOUD_NATIVE_STANDARDS.md",
        "/blob/master/docs/standards/CLOUD_NATIVE_STANDARDS.md",
    ),
    (
        "/blob/master/WEB_DESIGN_UX_STANDARDS.md",
        "/blob/master/docs/standards/WEB_DESIGN_UX_STANDARDS.md",
    ),
    (
        "/blob/master/DATA_ENGINEERING_STANDARDS.md",
        "/blob/master/docs/standards/DATA_ENGINEERING_STANDARDS.md",
    ),
    (
        "/blob/master/GITHUB_PLATFORM_STANDARDS.md",
        "/blob/master/docs/standards/GITHUB_PLATFORM_STANDARDS.md",
    ),
    (
        "/blob/master/COST_OPTIMIZATION_STANDARDS.md",
        "/blob/master/docs/standards/COST_OPTIMIZATION_STANDARDS.md",
    ),
    (
        "/blob/master/CONTENT_STANDARDS.md",
        "/blob/master/docs/standards/CONTENT_STANDARDS.md",
    ),
    (
        "/blob/master/EVENT_DRIVEN_STANDARDS.md",
        "/blob/master/docs/standards/EVENT_DRIVEN_STANDARDS.md",
    ),
    (
        "/blob/master/TOOLCHAIN_STANDARDS.md",
        "/blob/master/docs/standards/TOOLCHAIN_STANDARDS.md",
    ),
    (
        "/blob/master/COMPLIANCE_STANDARDS.md",
        "/blob/master/docs/standards/COMPLIANCE_STANDARDS.md",
    ),
    (
        "/blob/master/UNIFIED_STANDARDS.md",
        "/blob/master/docs/standards/UNIFIED_STANDARDS.md",
    ),
    (
        "/blob/master/KNOWLEDGE_MANAGEMENT_STANDARDS.md",
        "/blob/master/docs/standards/KNOWLEDGE_MANAGEMENT_STANDARDS.md",
    ),
    (
        "/blob/master/VALIDATION_PATTERNS.md",
        "/blob/master/docs/standards/VALIDATION_PATTERNS.md",
    ),
    # NIST files
    (
        "/blob/master/NIST_IMPLEMENTATION_GUIDE.md",
        "/blob/master/docs/nist/NIST_IMPLEMENTATION_GUIDE.md",
    ),
    # Core files
    ("/blob/master/CLAUDE.md", "/blob/master/docs/core/CLAUDE.md"),
    ("/blob/master/CONTRIBUTING.md", "/blob/master/docs/core/CONTRIBUTING.md"),
    # Guides
    ("/blob/master/STANDARDS_INDEX.md", "/blob/master/docs/guides/STANDARDS_INDEX.md"),
    ("/blob/master/STANDARDS_GRAPH.md", "/blob/master/docs/guides/STANDARDS_GRAPH.md"),
    (
        "/blob/master/ADOPTION_CHECKLIST.md",
        "/blob/master/docs/guides/ADOPTION_CHECKLIST.md",
    ),
]

test_replacements = [
    # Update file existence checks
    ("STANDARDS_INDEX.md", "docs/guides/STANDARDS_INDEX.md"),
    ("STANDARDS_GRAPH.md", "docs/guides/STANDARDS_GRAPH.md"),
]

script_replacements = [
    # Update script references
    ("./fix_trailing_whitespace.sh", "./scripts/fix_trailing_whitespace.sh"),
    ("'./fix_trailing_whitespace.sh'", "'./scripts/fix_trailing_whitespace.sh'"),
    ('"./fix_trailing_whitespace.sh"', '"./scripts/fix_trailing_whitespace.sh"'),
]

# Update scripts
print("Updating scripts...")
update_file("scripts/generate-badges.sh", badge_replacements)
update_file("scripts/check_whitespace.sh", script_replacements)
update_file("tests/validate_knowledge_management.sh", test_replacements)

# Update Python scripts
print("\nUpdating Python scripts...")
python_files = list(Path("scripts").glob("*.py")) + list(Path("tests").glob("*.py"))
for py_file in python_files:
    # Check if file references old paths
    with open(py_file, "r") as f:
        content = f.read()

    if any(term in content for term in ["STANDARDS.md", "MANIFEST.yaml", "CLAUDE.md"]):
        print(f"Checking: {py_file}")
        # You may need custom replacements for Python files

print("\nDone!")
