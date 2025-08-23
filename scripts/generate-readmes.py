#!/usr/bin/env python3
"""
Generate README.md files for directories missing them.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Directories that need README files
MISSING_DIRS = [
    "memory",
    "reports",
    "standards",
    "ai-engine",
    "prompts",
    "catalogs",
    "profiles",
    "config",
    "scripts",
    "docs",
    "examples/project-templates",
    "examples/ai-generation-hints",
    "examples/nist-templates/typescript",
    "examples/nist-templates/python",
    "examples/nist-templates/go",
    "examples/project-templates/python-project",
    "examples/project-templates/javascript-project",
    "examples/project-templates/go-project",
    "examples/project-templates/terraform",
    "examples/project-templates/docker",
    "examples/project-templates/kubernetes",
    "standards/compliance/oscal",
    "standards/compliance/examples",
    "standards/compliance/src",
    "standards/compliance/semantic",
    "standards/compliance/scripts",
    "standards/compliance/automation",
    "standards/compliance/oscal/catalogs",
    "standards/compliance/oscal/profiles",
    "standards/compliance/oscal/types",
    "standards/compliance/src/parsers",
    "monitoring/config",
    "memory/sessions",
    "memory/agents",
    ".claude/agents",
    ".claude/commands",
    ".nist",
    ".vscode/nist-extension",
    ".github/PULL_REQUEST_TEMPLATE",
]

# Directory descriptions
DIR_DESCRIPTIONS = {
    "memory": "Persistent memory storage for agents and sessions",
    "reports": "Generated reports and audit outputs",
    "standards": "Standards documentation root",
    "ai-engine": "AI engine configuration and templates",
    "prompts": "LLM prompts for various tasks",
    "catalogs": "OSCAL catalogs for compliance",
    "profiles": "OSCAL profiles and configurations",
    "config": "Configuration files and matrices",
    "scripts": "Utility and automation scripts",
    "docs": "Documentation root",
    "examples/project-templates": "Project template examples",
    "examples/ai-generation-hints": "AI code generation hints",
    "examples/nist-templates/typescript": "TypeScript NIST compliance templates",
    "examples/nist-templates/python": "Python NIST compliance templates",
    "examples/nist-templates/go": "Go NIST compliance templates",
    "monitoring/config": "Monitoring configuration files",
    "memory/sessions": "Session memory storage",
    "memory/agents": "Agent memory storage",
    ".claude/agents": "Claude agent definitions",
    ".claude/commands": "Claude command definitions",
    ".nist": "NIST compliance metadata",
    ".vscode/nist-extension": "VS Code NIST extension",
    ".github/PULL_REQUEST_TEMPLATE": "GitHub PR templates",
}


def get_hub_link(dir_path: Path) -> str:
    """Get the appropriate hub link for a directory."""
    dir_str = str(dir_path)

    # Determine the best hub based on location
    if "standards" in dir_str:
        # Calculate relative path to UNIFIED_STANDARDS
        depth = len(dir_path.parts)
        return "../" * (depth - 1) + "docs/standards/UNIFIED_STANDARDS.md"
    elif "examples" in dir_str:
        depth = len(dir_path.parts)
        return "../" * depth + "README.md"
    elif "docs" in dir_str:
        return "../README.md"
    elif ".claude" in dir_str or ".nist" in dir_str or ".github" in dir_str:
        return "../../README.md"
    else:
        return "../README.md"


def generate_readme(dir_path: Path) -> bool:
    """Generate README for a directory."""
    full_path = ROOT / dir_path

    # Create directory if it doesn't exist
    full_path.mkdir(parents=True, exist_ok=True)

    readme_path = full_path / "README.md"

    # Skip if README already exists
    if readme_path.exists():
        print(f"  ✓ Already exists: {dir_path}/README.md")
        return False

    # Get description
    description = DIR_DESCRIPTIONS.get(str(dir_path), f'{full_path.name.replace("-", " ").title()} directory')

    # Start building README content
    lines = [
        f"# {full_path.name.replace('-', ' ').replace('_', ' ').title()}",
        "",
        description,
        "",
    ]

    # List child files/directories
    children = []

    # Add subdirectories
    for child in sorted(full_path.glob("*/")):
        if child.name not in [".git", "__pycache__", "node_modules"]:
            children.append(("dir", child.name, f"./{child.name}/"))

    # Add markdown files
    for child in sorted(full_path.glob("*.md")):
        if child.name != "README.md":
            children.append(("file", child.stem, f"./{child.name}"))

    # Add other relevant files
    for pattern in ["*.py", "*.sh", "*.yaml", "*.yml", "*.json"]:
        for child in sorted(full_path.glob(pattern)):
            children.append(("file", child.stem, f"./{child.name}"))

    if children:
        lines.append("## Contents")
        lines.append("")
        for typ, name, path in children:
            icon = "📁" if typ == "dir" else "📄"
            display_name = name.replace("_", " ").replace("-", " ").title()
            lines.append(f"- {icon} [{display_name}]({path})")
        lines.append("")

    # Add navigation link
    lines.append("---")
    lines.append("")
    hub_link = get_hub_link(dir_path)
    lines.append(f"← Back to [Main Repository]({hub_link})")
    lines.append("")

    # Write README
    try:
        readme_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"  ✅ Created: {dir_path}/README.md")
        return True
    except Exception as e:
        print(f"  ❌ Error creating {dir_path}/README.md: {e}")
        return False


def main():
    """Generate all missing READMEs."""
    print("📁 Generating missing README files...")
    print(f"  Processing {len(MISSING_DIRS)} directories...")

    created = 0
    for dir_path in MISSING_DIRS:
        if generate_readme(Path(dir_path)):
            created += 1

    print(f"\n✅ Created {created} README files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
