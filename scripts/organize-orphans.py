#!/usr/bin/env python3
"""
Organize orphaned files by creating proper index entries.
Move reports to reports/generated and update indices.
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Files to move to reports/generated
MOVE_TO_REPORTS = [
    "ENHANCEMENT_IMPLEMENTATION_REPORT.md",
    "WORKFLOW_CLEANUP_REPORT.md",
    "REPOSITORY_REVIEW_FINAL_REPORT.md",
    "REORGANIZATION_SUMMARY.md",
    "STANDARDS_SUMMARY.md",
    "REPOSITORY_CLEANUP_RECOMMENDATIONS.md",
    "WEEKLY_DIGEST.md",
    "IMPLEMENTATION_REPORT_PHASE2.md",
    "COMPREHENSIVE_TESTING_REPORT.md",
    "FINAL_VALIDATION_REPORT.md",
    "CLEANUP_COMPLETION_REPORT.md",
    "IMPLEMENTATION_SUMMARY.md",
]


def move_reports():
    """Move report files to reports/generated."""
    moved = 0
    reports_dir = ROOT / "reports" / "generated"
    reports_dir.mkdir(parents=True, exist_ok=True)

    for filename in MOVE_TO_REPORTS:
        src = ROOT / filename
        if src.exists():
            dst = reports_dir / filename
            shutil.move(str(src), str(dst))
            print(f"  ✅ Moved {filename} to reports/generated/")
            moved += 1

    return moved


def create_orphan_index():
    """Create an index for remaining orphaned files."""
    # Create indices in key directories
    indices = {
        ".claude/agents/README.md": {
            "title": "Claude Agents",
            "files": [
                "analysis/code-analyzer.md",
                "github/*.md",
                "optimization/*.md",
                "sparc/*.md",
                "consensus/*.md",
                "templates/*.md",
                "swarm/*.md",
                "core/*.md",
            ],
        },
        "subagents/README.md": {
            "title": "Subagent Tasks",
            "files": [
                "completed/*.md",
                "reports/*.md",
            ],
        },
        "micro/README.md": {
            "title": "Micro Standards",
            "files": [
                "CS-api.micro.md",
                "SEC-auth.micro.md",
                "TS-unit.micro.md",
            ],
        },
    }

    for index_path, config in indices.items():
        full_path = ROOT / index_path
        if full_path.exists():
            # Read existing content
            content = full_path.read_text(encoding="utf-8")

            # Check if index section exists
            if "## Index" not in content:
                # Add index section
                lines = content.splitlines()

                # Find where to insert (after first heading)
                insert_pos = 0
                for i, line in enumerate(lines):
                    if line.startswith("# "):
                        insert_pos = i + 1
                        # Skip any immediate description
                        while (
                            insert_pos < len(lines)
                            and lines[insert_pos].strip()
                            and not lines[insert_pos].startswith("#")
                        ):
                            insert_pos += 1
                        break

                # Build index
                index_lines = ["", "## Index", ""]

                for pattern in config["files"]:
                    if "*" in pattern:
                        # Glob pattern
                        base_dir = full_path.parent
                        parts = pattern.split("/")
                        if len(parts) == 2 and parts[1] == "*.md":
                            subdir = base_dir / parts[0]
                            if subdir.exists():
                                index_lines.append(f"\n### {parts[0].title()}")
                                for file in sorted(subdir.glob("*.md")):
                                    if file.name != "README.md":
                                        rel_path = file.relative_to(base_dir)
                                        index_lines.append(f"- [{file.stem}]({rel_path})")
                    else:
                        # Direct file
                        file_path = full_path.parent / pattern
                        if file_path.exists():
                            index_lines.append(f"- [{file_path.stem}]({pattern})")

                # Insert index
                lines[insert_pos:insert_pos] = index_lines

                # Write back
                full_path.write_text("\n".join(lines), encoding="utf-8")
                print(f"  ✅ Updated index: {index_path}")


def update_main_readme():
    """Add section for archived reports in main README."""
    readme = ROOT / "README.md"
    if not readme.exists():
        return

    content = readme.read_text(encoding="utf-8")

    # Check if archived section exists
    if "## 📚 Archived Reports" not in content:
        # Find where to add (before contributing section or at end)
        lines = content.splitlines()
        insert_pos = len(lines)

        for i, line in enumerate(lines):
            if "## 🤝 Contributing" in line or "## Contributing" in line:
                insert_pos = i
                break

        # Add archived reports section
        archive_section = [
            "",
            "## 📚 Archived Reports",
            "",
            "Historical implementation and validation reports have been archived to `reports/generated/`:",
            "",
            "- Implementation reports",
            "- Validation reports",
            "- Cleanup summaries",
            "- Weekly digests",
            "",
            "See [reports/generated/](./reports/generated/) for full archive.",
            "",
        ]

        lines[insert_pos:insert_pos] = archive_section
        readme.write_text("\n".join(lines), encoding="utf-8")
        print("  ✅ Updated main README with archived reports section")


def main():
    """Organize orphaned files."""
    print("📂 Organizing orphaned files...")

    # Move reports
    moved = move_reports()
    print(f"  Moved {moved} reports to reports/generated/")

    # Create indices
    create_orphan_index()

    # Update main README
    update_main_readme()

    print("\n✅ Orphaned files organized")
    return 0


if __name__ == "__main__":
    sys.exit(main())
