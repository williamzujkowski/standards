#!/usr/bin/env python3
"""
Generate READMEs for the final 4 directories missing them.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def create_readme(dir_path: Path, title: str, description: str):
    """Create a README for a directory."""
    readme_path = dir_path / "README.md"
    if readme_path.exists():
        print(f"  ⚠️  README already exists: {dir_path}")
        return

    # Get relative path to root
    depth = len(dir_path.relative_to(ROOT).parts)
    back_to_root = "../" * depth

    # List contents
    contents = []
    for item in sorted(dir_path.iterdir()):
        if item.name == "README.md":
            continue
        if item.is_file() and item.suffix == ".md":
            contents.append(f"- [{item.stem.replace('_', ' ').title()}](./{item.name})")
        elif item.is_dir() and not item.name.startswith("."):
            contents.append(f"- [{item.name}/](./{item.name}/)")

    # Build README content
    lines = [f"# {title}", "", description, ""]

    if contents:
        lines.extend(["## Contents", "", *contents, ""])

    lines.extend(["## Navigation", "", f"← Back to [Main Repository]({back_to_root}README.md)", ""])

    readme_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✅ Created README for {dir_path.relative_to(ROOT)}")


def main():
    """Create READMEs for final directories."""
    print("📝 Generating READMEs for final directories...")

    directories = [
        (
            ROOT / "docs/nist",
            "NIST 800-53r5 Compliance Documentation",
            "Complete NIST 800-53r5 compliance implementation guides, templates, and control mappings for software development projects.",
        ),
        (
            ROOT / "docs/guides",
            "Implementation Guides",
            "Comprehensive guides for adopting standards, creating new standards, and leveraging AI-powered tools for project kickstart.",
        ),
        (
            ROOT / "docs/standards",
            "Software Development Standards",
            "Complete collection of software development standards covering all aspects of modern development from coding to deployment.",
        ),
        (
            ROOT / "docs/core",
            "Core Documentation",
            "Essential documentation for repository structure, integration strategies, and workflow configurations.",
        ),
    ]

    for dir_path, title, description in directories:
        if dir_path.exists():
            create_readme(dir_path, title, description)
        else:
            print(f"  ⚠️  Directory does not exist: {dir_path}")

    print("✅ README generation complete")


if __name__ == "__main__":
    main()
