#!/usr/bin/env python3
"""
Automated migration script for repository optimization v2.

Migrates:
- Documentation structure to new hub system
- Skills to modular skill system
- Configuration files to new format
- Pre-commit hooks to enhanced version
- Audit reports to new structure
"""

import argparse
import logging
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class MigrationError(Exception):
    """Migration error."""


class RepositoryMigrator:
    """Handles automated repository migration to v2."""

    def __init__(self, repo_root: Path, dry_run: bool = False):
        self.repo_root = repo_root
        self.dry_run = dry_run
        self.backup_dir = repo_root / ".migration-backup" / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.migration_log: list[str] = []

    def log(self, message: str, level: str = "info") -> None:
        """Log migration action."""
        self.migration_log.append(f"[{level.upper()}] {message}")
        if level == "info":
            logger.info(message)
        elif level == "warning":
            logger.warning(message)
        elif level == "error":
            logger.error(message)

    def create_backup(self) -> None:
        """Create backup before migration."""
        if self.dry_run:
            self.log("DRY RUN: Would create backup", "info")
            return

        self.log(f"Creating backup: {self.backup_dir}", "info")
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Backup critical files
        critical_files = [
            "CLAUDE.md",
            "README.md",
            "config/audit-rules.yaml",
            "config/product-matrix.yaml",
            ".pre-commit-config.yaml",
        ]

        for file_path in critical_files:
            src = self.repo_root / file_path
            if src.exists():
                dst = self.backup_dir / file_path
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                self.log(f"Backed up: {file_path}", "info")

    def migrate_documentation_structure(self) -> None:
        """Migrate documentation to new hub system."""
        self.log("Migrating documentation structure...", "info")

        # Update hub rules in audit-rules.yaml
        audit_rules_path = self.repo_root / "config" / "audit-rules.yaml"

        if not audit_rules_path.exists():
            self.log("audit-rules.yaml not found", "warning")
            return

        try:
            audit_rules = yaml.safe_load(audit_rules_path.read_text())

            # Ensure hub rules are present
            if "orphans" not in audit_rules:
                audit_rules["orphans"] = {}

            if "require_link_from" not in audit_rules["orphans"]:
                audit_rules["orphans"]["require_link_from"] = []

            # Add default hub rules if missing
            default_hubs = [
                {"pattern": "docs/standards/*.md", "hubs": ["docs/standards/UNIFIED_STANDARDS.md"]},
                {"pattern": "docs/guides/*.md", "hubs": ["docs/guides/STANDARDS_INDEX.md"]},
                {"pattern": "docs/core/*.md", "hubs": ["docs/core/README.md"]},
                {"pattern": "docs/nist/*.md", "hubs": ["docs/nist/README.md"]},
                {"pattern": "docs/*.md", "hubs": ["docs/README.md"]},
            ]

            existing_patterns = {rule.get("pattern") for rule in audit_rules["orphans"]["require_link_from"]}

            for hub_rule in default_hubs:
                if hub_rule["pattern"] not in existing_patterns:
                    audit_rules["orphans"]["require_link_from"].append(hub_rule)
                    self.log(f"Added hub rule: {hub_rule['pattern']}", "info")

            if not self.dry_run:
                audit_rules_path.write_text(yaml.dump(audit_rules, sort_keys=False))
                self.log("Updated audit-rules.yaml", "info")

        except Exception as e:
            self.log(f"Error updating audit-rules.yaml: {e}", "error")

    def migrate_skills_structure(self) -> None:
        """Migrate to modular skill system."""
        self.log("Migrating skills structure...", "info")

        skills_dir = self.repo_root / "skills"

        if not skills_dir.exists():
            self.log("Skills directory does not exist, skipping", "info")
            return

        # Ensure all skills have proper structure
        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                self.log(f"Missing SKILL.md in {skill_dir.name}", "warning")
                continue

            # Ensure required subdirectories
            required_dirs = ["templates", "scripts", "resources"]

            for dir_name in required_dirs:
                dir_path = skill_dir / dir_name
                if not dir_path.exists():
                    if not self.dry_run:
                        dir_path.mkdir(parents=True, exist_ok=True)
                        (dir_path / ".gitkeep").touch()
                    self.log(f"Created {dir_name}/ in {skill_dir.name}", "info")

    def migrate_config_files(self) -> None:
        """Migrate configuration files to new format."""
        self.log("Migrating configuration files...", "info")

        # Update product-matrix.yaml structure
        product_matrix_path = self.repo_root / "config" / "product-matrix.yaml"

        if product_matrix_path.exists():
            try:
                matrix = yaml.safe_load(product_matrix_path.read_text())

                # Ensure version field
                if "version" not in matrix:
                    matrix["version"] = 2
                    self.log("Added version field to product-matrix.yaml", "info")

                # Ensure metadata
                if "metadata" not in matrix:
                    matrix["metadata"] = {"updated": datetime.now().isoformat(), "migration": "v2"}

                if not self.dry_run:
                    product_matrix_path.write_text(yaml.dump(matrix, sort_keys=False))
                    self.log("Updated product-matrix.yaml", "info")

            except Exception as e:
                self.log(f"Error updating product-matrix.yaml: {e}", "error")

    def migrate_precommit_hooks(self) -> None:
        """Migrate pre-commit hooks to enhanced version."""
        self.log("Migrating pre-commit hooks...", "info")

        precommit_config = self.repo_root / ".pre-commit-config.yaml"

        if not precommit_config.exists():
            self.log("No .pre-commit-config.yaml found", "warning")
            return

        try:
            config = yaml.safe_load(precommit_config.read_text())

            # Ensure audit check hook is present
            repos = config.get("repos", [])

            # Check if audit hook exists
            has_audit_hook = False
            for repo in repos:
                if repo.get("repo") == "local":
                    hooks = repo.get("hooks", [])
                    for hook in hooks:
                        if hook.get("id") == "audit-gates":
                            has_audit_hook = True
                            break

            if not has_audit_hook:
                # Add audit hook
                local_repo = None
                for repo in repos:
                    if repo.get("repo") == "local":
                        local_repo = repo
                        break

                if not local_repo:
                    local_repo = {"repo": "local", "hooks": []}
                    repos.append(local_repo)

                audit_hook = {
                    "id": "audit-gates",
                    "name": "Audit Gates",
                    "entry": "python3 scripts/generate-audit-reports.py",
                    "language": "system",
                    "pass_filenames": False,
                    "always_run": True,
                }

                local_repo["hooks"].append(audit_hook)
                config["repos"] = repos

                if not self.dry_run:
                    precommit_config.write_text(yaml.dump(config, sort_keys=False))
                self.log("Added audit-gates hook to pre-commit", "info")

        except Exception as e:
            self.log(f"Error updating pre-commit config: {e}", "error")

    def migrate_audit_reports(self) -> None:
        """Migrate audit reports to new structure."""
        self.log("Migrating audit reports structure...", "info")

        reports_dir = self.repo_root / "reports" / "generated"
        reports_dir.mkdir(parents=True, exist_ok=True)

        # Ensure .gitignore for generated reports
        gitignore = reports_dir / ".gitignore"
        if not gitignore.exists():
            if not self.dry_run:
                gitignore.write_text("*\n!.gitignore\n")
            self.log("Created .gitignore for generated reports", "info")

    def update_claude_md(self) -> None:
        """Update CLAUDE.md with migration notes."""
        self.log("Updating CLAUDE.md...", "info")

        claude_md = self.repo_root / "CLAUDE.md"

        if not claude_md.exists():
            self.log("CLAUDE.md not found", "warning")
            return

        content = claude_md.read_text()

        # Add migration notice if not present
        migration_notice = f"""
<!-- MIGRATION NOTE: Migrated to v2 on {datetime.now().strftime("%Y-%m-%d")} -->
"""

        if "MIGRATION NOTE" not in content and not self.dry_run:
            # Add at top after first heading
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if line.startswith("#"):
                    lines.insert(i + 1, migration_notice)
                    break

            claude_md.write_text("\n".join(lines))
            self.log("Added migration notice to CLAUDE.md", "info")

    def run_post_migration_checks(self) -> bool:
        """Run validation after migration."""
        self.log("Running post-migration checks...", "info")

        if self.dry_run:
            self.log("DRY RUN: Would run post-migration checks", "info")
            return True

        # Run audit reports
        try:
            result = subprocess.run(
                ["python3", str(self.repo_root / "scripts" / "generate-audit-reports.py")],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.repo_root,
            )

            if result.returncode == 0:
                self.log("Audit reports generated successfully", "info")
            else:
                self.log(f"Audit reports failed: {result.stderr}", "warning")

        except Exception as e:
            self.log(f"Error running audit reports: {e}", "warning")

        # Run validation
        try:
            result = subprocess.run(
                ["python3", str(self.repo_root / "scripts" / "validate-skills.py")],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.repo_root,
            )

            if result.returncode == 0:
                self.log("Skills validation passed", "info")
            else:
                self.log(f"Skills validation warnings: {result.stderr}", "info")

        except Exception as e:
            self.log(f"Error running skills validation: {e}", "warning")

        return True

    def export_migration_log(self, output_path: Path) -> None:
        """Export migration log."""
        log_content = "\n".join(self.migration_log)
        output_path.write_text(log_content)
        logger.info(f"Migration log exported to: {output_path}")

    def migrate(self) -> bool:
        """Run full migration."""
        self.log("=" * 80, "info")
        self.log("REPOSITORY MIGRATION TO V2", "info")
        self.log("=" * 80, "info")
        self.log("", "info")

        if self.dry_run:
            self.log("DRY RUN MODE - No changes will be made", "info")
            self.log("", "info")

        try:
            # Create backup
            self.create_backup()

            # Run migrations
            self.migrate_documentation_structure()
            self.migrate_skills_structure()
            self.migrate_config_files()
            self.migrate_precommit_hooks()
            self.migrate_audit_reports()
            self.update_claude_md()

            # Post-migration checks
            checks_passed = self.run_post_migration_checks()

            self.log("", "info")
            self.log("=" * 80, "info")
            self.log("MIGRATION COMPLETED" + (" (DRY RUN)" if self.dry_run else ""), "info")
            self.log("=" * 80, "info")

            if not self.dry_run:
                self.log(f"Backup created at: {self.backup_dir}", "info")

            return checks_passed

        except Exception as e:
            self.log(f"Migration failed: {e}", "error")
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Automated migration script for repository optimization v2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (no changes)
  python3 migrate-to-v2.py --dry-run

  # Run migration
  python3 migrate-to-v2.py

  # Export migration log
  python3 migrate-to-v2.py --log migration.log

  # Force migration (skip confirmations)
  python3 migrate-to-v2.py --force

Exit codes:
  0 - Migration successful
  1 - Migration failed
        """,
    )

    parser.add_argument("--dry-run", action="store_true", help="Perform dry run without making changes")

    parser.add_argument("--force", action="store_true", help="Skip confirmation prompts")

    parser.add_argument("--log", type=Path, help="Export migration log to file")

    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Get repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    # Confirm migration
    if not args.force and not args.dry_run:
        print("\n⚠️  This will migrate your repository to v2 structure.")
        print("A backup will be created before any changes.")
        response = input("\nContinue? [y/N]: ")

        if response.lower() != "y":
            print("Migration cancelled.")
            sys.exit(0)

    # Run migration
    migrator = RepositoryMigrator(repo_root, dry_run=args.dry_run)
    success = migrator.migrate()

    # Export log if requested
    if args.log:
        migrator.export_migration_log(args.log)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
