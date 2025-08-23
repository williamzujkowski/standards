#!/usr/bin/env python3
"""
Fix hub violations by ensuring all hub files properly link to their documents.
This is a companion to ensure-hub-links.py that verifies the links are recognized.
"""

import re
from pathlib import Path
from typing import Dict, Set

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_audit_rules() -> Dict:
    """Load audit rules configuration."""
    config_path = ROOT / "config/audit-rules.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def extract_links_from_auto_sections(content: str) -> Set[str]:
    """Extract file paths from AUTO-LINKS sections."""
    links = set()

    # Find all AUTO-LINKS sections
    auto_pattern = r"<!-- AUTO-LINKS:.*? -->(.*?)<!-- /AUTO-LINKS -->"
    matches = re.findall(auto_pattern, content, re.DOTALL)

    for match in matches:
        # Extract markdown links
        link_pattern = r"\[.*?\]\((.*?)\)"
        for link in re.findall(link_pattern, match):
            # Clean and normalize the link
            link = link.strip()
            if not link.startswith(("http://", "https://", "#", "mailto:")):
                links.add(link)

    return links


def verify_hub_links():
    """Verify that hub files link to all required documents."""
    rules = load_audit_rules()
    hub_requirements = rules.get("orphans", {}).get("require_link_from", [])

    issues = []
    fixed = []

    for requirement in hub_requirements:
        pattern = requirement["pattern"]
        hubs = requirement.get("hubs", [])

        for hub_path_str in hubs:
            hub_path = ROOT / hub_path_str
            if not hub_path.exists():
                print(f"  ⚠️  Hub file missing: {hub_path_str}")
                continue

            content = hub_path.read_text(encoding="utf-8")

            # Check if AUTO-LINKS sections exist
            if "<!-- AUTO-LINKS:" not in content:
                print(f"  ⚠️  No AUTO-LINKS section in {hub_path_str}")
                continue

            # Extract links from AUTO-LINKS sections
            auto_links = extract_links_from_auto_sections(content)

            # Also extract regular markdown links
            regular_links = set()
            link_pattern = r"\[.*?\]\((.*?)\)"
            for link in re.findall(link_pattern, content):
                link = link.strip()
                if not link.startswith(("http://", "https://", "#", "mailto:")):
                    regular_links.add(link)

            all_links = auto_links | regular_links

            print(f"\n  Hub: {hub_path_str}")
            print(f"    AUTO-LINKS: {len(auto_links)} links")
            print(f"    Regular links: {len(regular_links)} links")
            print(f"    Total: {len(all_links)} links")

            # Find files that should be linked from this hub
            if "**" in pattern:
                base_parts = pattern.split("**")[0].rstrip("/")
                suffix = pattern.split("**")[1].lstrip("/")
                base_path = ROOT / base_parts if base_parts else ROOT

                expected_files = []
                if base_path.exists():
                    for file_path in base_path.rglob(suffix):
                        if file_path.is_file() and file_path != hub_path:
                            expected_files.append(file_path)
            else:
                expected_files = list(ROOT.glob(pattern))
                expected_files = [f for f in expected_files if f.is_file() and f != hub_path]

            print(f"    Expected to link: {len(expected_files)} files")

            # Check if all expected files are linked
            missing = 0
            for expected in expected_files:
                # Calculate relative path from hub to expected file
                try:
                    rel_path = expected.relative_to(hub_path.parent)
                    rel_str = rel_path.as_posix()
                except ValueError:
                    # File is not in subdirectory of hub
                    rel_parts = [".."] * len(hub_path.parent.relative_to(ROOT).parts)
                    rel_parts.extend(expected.relative_to(ROOT).parts)
                    rel_str = "/".join(rel_parts)

                # Check if this file is linked (in any form)
                found = False
                for link in all_links:
                    # Normalize both paths for comparison
                    link_normalized = Path(link).as_posix()
                    if link_normalized == rel_str or link_normalized.endswith("/" + expected.name):
                        found = True
                        break

                if not found:
                    missing += 1
                    issues.append(f"      Missing link: {expected.relative_to(ROOT)}")

            if missing == 0:
                fixed.append(hub_path_str)
                print("    ✅ All expected files are linked")
            else:
                print(f"    ⚠️  Missing {missing} links")

    return issues, fixed


def main():
    """Main execution."""
    print("🔍 Verifying hub links...")

    issues, fixed = verify_hub_links()

    print("\n" + "=" * 60)
    if issues:
        print(f"\n⚠️  Found {len(issues)} missing links:")
        for issue in issues[:10]:  # Show first 10
            print(issue)
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")
    else:
        print("\n✅ All hub links verified")

    if fixed:
        print(f"\n✅ Verified hubs: {', '.join(fixed)}")


if __name__ == "__main__":
    main()
