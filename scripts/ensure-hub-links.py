#!/usr/bin/env python3
"""
Ensure hub files contain AUTO-LINKS sections pointing to all documents under their pattern.
"""

import re
import yaml
from pathlib import Path
from typing import List, Dict, Tuple

ROOT = Path(__file__).resolve().parents[1]

def load_audit_rules() -> Dict:
    """Load audit rules configuration."""
    config_path = ROOT / 'config/audit-rules.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def find_files_matching_pattern(pattern: str) -> List[Path]:
    """Find all files matching a glob pattern."""
    files = []
    glob_pattern = pattern.replace('**', '*')

    # Convert pattern to Path glob
    if '**' in pattern:
        # Recursive glob
        base_parts = pattern.split('**')[0].rstrip('/')
        suffix = pattern.split('**')[1].lstrip('/')
        base_path = ROOT / base_parts if base_parts else ROOT

        if base_path.exists():
            for file_path in base_path.rglob(suffix):
                if file_path.is_file():
                    files.append(file_path)
    else:
        # Simple glob
        for file_path in ROOT.glob(pattern):
            if file_path.is_file():
                files.append(file_path)

    return sorted(files)

def generate_auto_links_section(files: List[Path], hub_path: Path) -> str:
    """Generate AUTO-LINKS section content."""
    if not files:
        return "_(no documents found)_"

    lines = []
    hub_dir = hub_path.parent

    for file_path in files:
        # Skip the hub file itself
        if file_path == hub_path:
            continue

        # Calculate relative path from hub to file
        try:
            rel_path = file_path.relative_to(hub_dir)
        except ValueError:
            # File is not in a subdirectory of hub
            rel_path = Path('../') * len(hub_dir.relative_to(ROOT).parts) / file_path.relative_to(ROOT)

        # Create link
        title = file_path.stem.replace('_', ' ').replace('-', ' ').title()
        link = f"- [{title}]({rel_path})"
        lines.append(link)

    return '\n'.join(lines) if lines else "_(no documents found)_"

def update_hub_file(hub_path: Path, pattern: str, files: List[Path]):
    """Update or create hub file with AUTO-LINKS section."""
    auto_links_marker = f"<!-- AUTO-LINKS:{pattern} -->"
    auto_links_end = "<!-- /AUTO-LINKS -->"

    # Read existing content or create new
    if hub_path.exists():
        content = hub_path.read_text(encoding='utf-8')
    else:
        # Create minimal README
        hub_name = hub_path.parent.name.replace('-', ' ').replace('_', ' ').title()
        content = f"""# {hub_name}

This is the hub page for {hub_name.lower()} documentation.

## Contents

{auto_links_marker}

{auto_links_end}

---

← Back to [Main Repository]({"../" * len(hub_path.relative_to(ROOT).parts)}README.md)
"""
        hub_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate links section
    links_content = generate_auto_links_section(files, hub_path)

    # Check if AUTO-LINKS section exists
    if auto_links_marker in content:
        # Replace existing section
        pattern_escaped = re.escape(auto_links_marker)
        end_escaped = re.escape(auto_links_end)
        regex = f"{pattern_escaped}.*?{end_escaped}"
        replacement = f"{auto_links_marker}\n\n{links_content}\n\n{auto_links_end}"
        content = re.sub(regex, replacement, content, flags=re.DOTALL)
    else:
        # Add new section at appropriate location
        if "## Contents" in content:
            # Add after Contents heading
            content = content.replace(
                "## Contents",
                f"## Contents\n\n{auto_links_marker}\n\n{links_content}\n\n{auto_links_end}"
            )
        else:
            # Add before navigation or at end
            if "## Navigation" in content:
                content = content.replace(
                    "## Navigation",
                    f"{auto_links_marker}\n\n{links_content}\n\n{auto_links_end}\n\n## Navigation"
                )
            elif "---" in content:
                # Add before first horizontal rule
                parts = content.split("---", 1)
                content = f"{parts[0]}{auto_links_marker}\n\n{links_content}\n\n{auto_links_end}\n\n---{parts[1]}"
            else:
                # Add at end
                content += f"\n\n{auto_links_marker}\n\n{links_content}\n\n{auto_links_end}\n"

    # Write updated content
    hub_path.write_text(content, encoding='utf-8')
    print(f"  ✅ Updated hub: {hub_path.relative_to(ROOT)}")

def main():
    """Main execution."""
    print("🔗 Ensuring hub links...")

    # Load audit rules
    rules = load_audit_rules()

    if 'require_link_from' not in rules.get('orphans', {}):
        print("  ⚠️  No hub requirements found in audit rules")
        return

    hub_requirements = rules['orphans']['require_link_from']

    for requirement in hub_requirements:
        pattern = requirement['pattern']
        hubs = requirement.get('hubs', [])

        if not hubs:
            continue

        # Find all files matching pattern
        files = find_files_matching_pattern(pattern)

        print(f"\n  Pattern: {pattern}")
        print(f"  Found {len(files)} files")

        # Update each hub
        for hub in hubs:
            hub_path = ROOT / hub
            update_hub_file(hub_path, pattern, files)

    print("\n✅ Hub links ensured")

if __name__ == '__main__':
    main()
