#!/usr/bin/env python3
"""
Test script to detect redundancy and ensure DRY principles in the standards repository.
Run this as part of CI/CD to prevent future redundancy.
"""

import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml


class RedundancyChecker:
    def __init__(self, repo_path="."):
        self.repo_path = Path(repo_path)
        self.errors = []
        self.warnings = []

    def check_all(self):
        """Run all redundancy checks"""
        print("🔍 Running redundancy checks...")

        self.check_duplicate_content()
        self.check_cross_references()
        self.check_manifest_sync()
        self.check_index_freshness()
        self.check_api_completeness()

        return self.report_results()

    def check_duplicate_content(self):
        """Check for duplicate content across files"""
        print("\n📄 Checking for duplicate content...")

        # Read all markdown files
        content_hashes = defaultdict(list)

        # Check all markdown files in various directories
        md_files = list(self.repo_path.glob("*.md"))
        md_files.extend(self.repo_path.glob("docs/**/*.md"))

        for md_file in md_files:
            if md_file.name in ["README.md", "CLAUDE.md"]:  # Skip main files
                continue

            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extract sections
                sections = re.split(r"^##\s+", content, flags=re.MULTILINE)

                for section in sections[1:]:  # Skip header
                    if len(section) > 500:  # Only check substantial sections
                        # Normalize whitespace for comparison
                        normalized = re.sub(r"\s+", " ", section.strip())

                        # Skip generic boilerplate sections
                        if any(
                            generic in normalized
                            for generic in [
                                "This standard provides comprehensive guidelines and best practices",
                                "Review the relevant sections of this standard for your use case",
                                "Identify which guidelines apply to your project",
                            ]
                        ):
                            continue

                        section_hash = hashlib.md5(normalized.encode()).hexdigest()

                        content_hashes[section_hash].append(
                            {
                                "file": md_file.name,
                                "section": section.split("\n")[0][:50],
                            }
                        )
            except Exception as e:
                self.warnings.append(f"Could not read {md_file.name}: {e}")

        # Report duplicates
        for hash_val, locations in content_hashes.items():
            if len(locations) > 1:
                self.errors.append(
                    f"Duplicate content found in: {[loc['file'] for loc in locations]}"
                )

    def check_cross_references(self):
        """Check that all referenced files exist"""
        print("\n🔗 Checking cross-references...")

        # Check all markdown files in various directories
        md_files = list(self.repo_path.glob("*.md"))
        md_files.extend(self.repo_path.glob("docs/**/*.md"))

        for md_file in md_files:
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Find markdown links
                links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)

                for link_text, link_url in links:
                    if link_url.startswith("./") or (
                        link_url.endswith(".md") and not link_url.startswith("http")
                    ):
                        # Remove anchor references
                        clean_url = link_url.split("#")[0]
                        if clean_url:  # Skip pure anchors like #section
                            # First try resolving relative to the file's location
                            try:
                                relative_path = (md_file.parent / clean_url).resolve()
                                if relative_path.exists():
                                    continue
                            except Exception:
                                # Path resolution failed, continue with other checks
                                pass

                            # Local file reference - check multiple possible locations
                            clean_path = clean_url.lstrip("./")

                            # Then try multiple possible locations
                            possible_paths = [
                                self.repo_path / clean_path,
                                self.repo_path / "docs/standards" / clean_path,
                                self.repo_path / "docs/nist" / clean_path,
                                self.repo_path / "docs/guides" / clean_path,
                                self.repo_path / "docs/core" / clean_path,
                                self.repo_path / "config" / clean_path,
                                self.repo_path / "scripts" / clean_path,
                            ]

                            file_found = any(path.exists() for path in possible_paths)

                            if not file_found:
                                # Special case for .vscode extensions
                                if ".vscode" in clean_path and clean_path.endswith("/"):
                                    # This is likely a directory reference, skip it
                                    continue
                                self.errors.append(
                                    f"{md_file.name} references non-existent file: {link_url}"
                                )
            except Exception as e:
                self.warnings.append(
                    f"Could not check references in {md_file.name}: {e}"
                )

    def check_manifest_sync(self):
        """Check that MANIFEST.yaml is in sync with actual files"""
        print("\n📋 Checking MANIFEST.yaml sync...")

        try:
            with open(self.repo_path / "config/MANIFEST.yaml", "r") as f:
                manifest = yaml.safe_load(f)

            # Check each standard in manifest exists
            for code, standard in manifest.get("standards", {}).items():
                filename = standard.get("full_name")
                if filename:
                    # Check in multiple possible locations
                    possible_paths = [
                        self.repo_path / "docs/standards" / filename,
                        self.repo_path / "docs/nist" / filename,
                        self.repo_path / "docs/guides" / filename,
                        self.repo_path / "docs/core" / filename,
                    ]

                    file_found = any(path.exists() for path in possible_paths)

                    if not file_found:
                        self.errors.append(
                            f"MANIFEST.yaml references non-existent file: {filename}"
                        )

            # Check all _STANDARDS.md files are in manifest
            standards_dir = self.repo_path / "docs/standards"
            for std_file in standards_dir.glob("*_STANDARDS.md"):
                if std_file.name != "UNIFIED_STANDARDS.md":
                    found = False
                    for code, standard in manifest.get("standards", {}).items():
                        if standard.get("full_name") == std_file.name:
                            found = True
                            break
                    if not found:
                        self.warnings.append(
                            f"{std_file.name} not referenced in MANIFEST.yaml"
                        )

        except Exception as e:
            self.errors.append(f"Could not check MANIFEST.yaml: {e}")

    def check_index_freshness(self):
        """Check if STANDARDS_INDEX.md needs regeneration"""
        print("\n📑 Checking STANDARDS_INDEX.md freshness...")

        try:
            # Get modification times
            index_path = self.repo_path / "docs/guides/STANDARDS_INDEX.md"
            if not index_path.exists():
                self.errors.append("STANDARDS_INDEX.md is missing")
                return

            index_mtime = index_path.stat().st_mtime

            # Check if any standards file is newer
            standards_dir = self.repo_path / "docs/standards"
            for std_file in standards_dir.glob("*_STANDARDS.md"):
                if std_file.stat().st_mtime > index_mtime:
                    self.warnings.append(
                        f"STANDARDS_INDEX.md is out of date - {std_file.name} was modified more recently"
                    )
                    break

        except Exception as e:
            self.warnings.append(f"Could not check index freshness: {e}")

    def check_api_completeness(self):
        """Check that standards-api.json is complete"""
        print("\n🔌 Checking API completeness...")

        try:
            api_path = self.repo_path / "config/standards-api.json"
            if not api_path.exists():
                # Try old location
                api_path = self.repo_path / "standards-api.json"

            with open(api_path, "r") as f:
                api_data = json.load(f)

            # Check that all remote commands have endpoints
            for cmd, details in api_data.get("remote_commands", {}).items():
                if "endpoint" not in details and "uses" not in details:
                    self.warnings.append(
                        f"Remote command {cmd} missing endpoint or uses reference"
                    )

            # Check that direct_access section exists
            if "direct_access" not in api_data:
                self.errors.append("standards-api.json missing direct_access section")

        except Exception as e:
            self.errors.append(f"Could not check standards-api.json: {e}")

    def report_results(self):
        """Report test results"""
        print("\n" + "=" * 60)
        print("📊 REDUNDANCY CHECK RESULTS")
        print("=" * 60)

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ All checks passed! No redundancy detected.")

        print("\n" + "=" * 60)

        # Return exit code
        if self.errors:
            return 1  # Critical errors
        elif self.warnings:
            return 2  # Non-critical warnings
        else:
            return 0  # All good


def main():
    """Run redundancy checks"""
    checker = RedundancyChecker()
    exit_code = checker.check_all()

    # Additional checks that can be run
    print("\n💡 Additional manual checks to consider:")
    print("  - Run generate_standards_index.py to update the index")
    print("  - Review MANIFEST.yaml for accuracy")
    print("  - Check for overlapping content between standards")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
