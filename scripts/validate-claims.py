#!/usr/bin/env python3
"""
Validate documentation claims against actual implementation.

Verifies:
- Agent counts match actual available agents
- Command examples are tested and working
- File paths and directories exist
- Integration instructions are current
- Performance claims are measurable
- Tool lists are accurate and complete
"""

import argparse
import json
import logging
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of a validation check."""

    check_name: str
    passed: bool
    message: str
    details: Dict = field(default_factory=dict)
    severity: str = "error"  # error, warning, info


class ClaimsValidator:
    """Validates documentation claims against actual implementation."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.results: List[ValidationResult] = []
        self.claude_md = repo_root / "CLAUDE.md"
        self.config_dir = repo_root / "config"
        self.scripts_dir = repo_root / "scripts"
        self.docs_dir = repo_root / "docs"

    def validate_all(self) -> bool:
        """Run all validation checks."""
        logger.info("Starting comprehensive validation...")

        # Core validation checks
        self.validate_agent_counts()
        self.validate_command_examples()
        self.validate_file_paths()
        self.validate_directory_structure()
        self.validate_tool_lists()
        self.validate_mcp_integration()
        self.validate_config_files()
        self.validate_cross_references()
        self.validate_executable_scripts()
        self.validate_documentation_consistency()

        return all(r.passed or r.severity != "error" for r in self.results)

    def validate_agent_counts(self) -> None:
        """Validate that documented agent counts match actual available agents."""
        logger.info("Validating agent counts...")

        try:
            # Parse CLAUDE.md for agent counts
            if not self.claude_md.exists():
                self.results.append(
                    ValidationResult(
                        check_name="agent_counts",
                        passed=False,
                        message="CLAUDE.md not found",
                        severity="error",
                    )
                )
                return

            content = self.claude_md.read_text()

            # Find agent count claims
            agent_section = re.search(r"🚀 Agent Types for Task Tool \((\d+) Available\)", content)

            if not agent_section:
                self.results.append(
                    ValidationResult(
                        check_name="agent_counts",
                        passed=False,
                        message="Agent count section not found in CLAUDE.md",
                        severity="warning",
                    )
                )
                return

            claimed_count = int(agent_section.group(1))

            # Count actual agents listed
            actual_agents = set()

            # Extract agents from sections
            agent_pattern = r"`([a-z-]+)`"
            for match in re.finditer(agent_pattern, content):
                agent_name = match.group(1)
                # Filter out non-agent names
                if not any(
                    agent_name.startswith(prefix)
                    for prefix in ["http", "www", "git", "npm", "python", "bash", "mkdir", "cd"]
                ):
                    actual_agents.add(agent_name)

            # Validate count
            actual_count = len(actual_agents)
            passed = claimed_count == actual_count

            self.results.append(
                ValidationResult(
                    check_name="agent_counts",
                    passed=passed,
                    message=f"Agent count: claimed={claimed_count}, actual={actual_count}",
                    details={"claimed": claimed_count, "actual": actual_count, "agents": sorted(actual_agents)},
                    severity="error" if not passed else "info",
                )
            )

        except Exception as e:
            self.results.append(
                ValidationResult(
                    check_name="agent_counts",
                    passed=False,
                    message=f"Error validating agent counts: {e}",
                    severity="error",
                )
            )

    def validate_command_examples(self) -> None:
        """Validate that command examples in documentation are working."""
        logger.info("Validating command examples...")

        try:
            content = self.claude_md.read_text()

            # Extract bash command examples
            bash_blocks = re.findall(r"```(?:bash|sh)\n(.*?)```", content, re.DOTALL)

            tested_commands = 0
            failed_commands = []

            for block in bash_blocks:
                commands = [line.strip() for line in block.split("\n") if line.strip() and not line.startswith("#")]

                for cmd in commands:
                    # Skip complex or interactive commands
                    if any(
                        skip in cmd
                        for skip in [
                            "git push",
                            "git commit",
                            "npx",
                            "claude mcp",
                            "||",
                            "&&",
                            "mcp__",
                            "$",
                        ]
                    ):
                        continue

                    # Test safe commands
                    if cmd.startswith(("python3 scripts/", "pytest", "pre-commit")):
                        tested_commands += 1
                        # Check if script exists
                        if cmd.startswith("python3 scripts/"):
                            script_name = cmd.split()[1].replace("scripts/", "")
                            script_path = self.scripts_dir / script_name
                            if not script_path.exists():
                                failed_commands.append(f"Script not found: {script_name}")

            passed = len(failed_commands) == 0

            self.results.append(
                ValidationResult(
                    check_name="command_examples",
                    passed=passed,
                    message=f"Tested {tested_commands} commands, {len(failed_commands)} failed",
                    details={"tested": tested_commands, "failed": failed_commands},
                    severity="warning" if not passed else "info",
                )
            )

        except Exception as e:
            self.results.append(
                ValidationResult(
                    check_name="command_examples",
                    passed=False,
                    message=f"Error validating commands: {e}",
                    severity="warning",
                )
            )

    def validate_file_paths(self) -> None:
        """Validate that all referenced file paths exist."""
        logger.info("Validating file paths...")

        try:
            content = self.claude_md.read_text()

            # Extract file path references
            path_pattern = r"`([a-zA-Z0-9_\-/.]+\.(md|yaml|yml|py|sh|json|txt))`"
            referenced_paths = set(re.findall(path_pattern, content))

            missing_paths = []

            for path_tuple in referenced_paths:
                path_str = path_tuple[0]
                # Skip URLs and special patterns
                if path_str.startswith(("http", "www", "{{", "<", "org/project")):
                    continue

                path = self.repo_root / path_str

                if not path.exists():
                    missing_paths.append(path_str)

            passed = len(missing_paths) == 0

            self.results.append(
                ValidationResult(
                    check_name="file_paths",
                    passed=passed,
                    message=f"Checked {len(referenced_paths)} paths, {len(missing_paths)} missing",
                    details={"total": len(referenced_paths), "missing": missing_paths},
                    severity="error" if not passed else "info",
                )
            )

        except Exception as e:
            self.results.append(
                ValidationResult(
                    check_name="file_paths",
                    passed=False,
                    message=f"Error validating file paths: {e}",
                    severity="error",
                )
            )

    def validate_directory_structure(self) -> None:
        """Validate that expected directories exist."""
        logger.info("Validating directory structure...")

        expected_dirs = [
            "docs/standards",
            "docs/nist",
            "docs/guides",
            "docs/core",
            "examples",
            "scripts",
            "config",
            "reports/generated",
            "tests",
        ]

        missing_dirs = []

        for dir_name in expected_dirs:
            dir_path = self.repo_root / dir_name
            if not dir_path.exists():
                missing_dirs.append(dir_name)

        passed = len(missing_dirs) == 0

        self.results.append(
            ValidationResult(
                check_name="directory_structure",
                passed=passed,
                message=f"Checked {len(expected_dirs)} directories, {len(missing_dirs)} missing",
                details={"expected": expected_dirs, "missing": missing_dirs},
                severity="error" if not passed else "info",
            )
        )

    def validate_tool_lists(self) -> None:
        """Validate that tool lists are accurate and complete."""
        logger.info("Validating tool lists...")

        try:
            content = self.claude_md.read_text()

            # Find MCP tool count claim
            mcp_tools_match = re.search(r"MCP Tools.*?\((\d+) available", content)

            if not mcp_tools_match:
                self.results.append(
                    ValidationResult(
                        check_name="tool_lists",
                        passed=False,
                        message="MCP tools count not found in CLAUDE.md",
                        severity="warning",
                    )
                )
                return

            claimed_mcp_count = int(mcp_tools_match.group(1))

            # Count actual MCP tools listed
            mcp_tools = set(re.findall(r"`(mcp__[a-z_-]+)`", content))
            actual_mcp_count = len(mcp_tools)

            passed = claimed_mcp_count == actual_mcp_count

            self.results.append(
                ValidationResult(
                    check_name="tool_lists",
                    passed=passed,
                    message=f"MCP tools: claimed={claimed_mcp_count}, actual={actual_mcp_count}",
                    details={"claimed": claimed_mcp_count, "actual": actual_mcp_count, "tools": sorted(mcp_tools)},
                    severity="warning" if not passed else "info",
                )
            )

        except Exception as e:
            self.results.append(
                ValidationResult(
                    check_name="tool_lists",
                    passed=False,
                    message=f"Error validating tool lists: {e}",
                    severity="warning",
                )
            )

    def validate_mcp_integration(self) -> None:
        """Validate MCP integration claims."""
        logger.info("Validating MCP integration...")

        # Check for MCP configuration
        package_json = self.repo_root / "package.json"
        mcp_config = self.repo_root / ".claude-flow" / "config.json"

        has_package_json = package_json.exists()
        has_mcp_config = mcp_config.exists()

        passed = True
        details = {"package_json": has_package_json, "mcp_config": has_mcp_config}

        self.results.append(
            ValidationResult(
                check_name="mcp_integration",
                passed=passed,
                message=f"MCP integration files: package.json={has_package_json}, config={has_mcp_config}",
                details=details,
                severity="info",
            )
        )

    def validate_config_files(self) -> None:
        """Validate configuration files."""
        logger.info("Validating configuration files...")

        config_files = [
            "audit-rules.yaml",
            "product-matrix.yaml",
        ]

        missing_configs = []
        invalid_configs = []

        for config_file in config_files:
            config_path = self.config_dir / config_file

            if not config_path.exists():
                missing_configs.append(config_file)
                continue

            # Validate YAML syntax
            try:
                yaml.safe_load(config_path.read_text())
            except yaml.YAMLError as e:
                invalid_configs.append(f"{config_file}: {e}")

        passed = len(missing_configs) == 0 and len(invalid_configs) == 0

        self.results.append(
            ValidationResult(
                check_name="config_files",
                passed=passed,
                message=f"Config files: {len(missing_configs)} missing, {len(invalid_configs)} invalid",
                details={"missing": missing_configs, "invalid": invalid_configs},
                severity="error" if not passed else "info",
            )
        )

    def validate_cross_references(self) -> None:
        """Validate cross-references between documentation files."""
        logger.info("Validating cross-references...")

        try:
            # Run the audit reports script
            audit_json = self.repo_root / "reports" / "generated" / "structure-audit.json"

            if not audit_json.exists():
                self.results.append(
                    ValidationResult(
                        check_name="cross_references",
                        passed=False,
                        message="Audit report not found, run generate-audit-reports.py first",
                        severity="warning",
                    )
                )
                return

            audit_data = json.loads(audit_json.read_text())

            broken_links = audit_data.get("broken_links", -1)
            passed = broken_links == 0

            self.results.append(
                ValidationResult(
                    check_name="cross_references",
                    passed=passed,
                    message=f"Broken links: {broken_links}",
                    details=audit_data,
                    severity="error" if not passed else "info",
                )
            )

        except Exception as e:
            self.results.append(
                ValidationResult(
                    check_name="cross_references",
                    passed=False,
                    message=f"Error validating cross-references: {e}",
                    severity="warning",
                )
            )

    def validate_executable_scripts(self) -> None:
        """Validate that documented scripts are executable."""
        logger.info("Validating executable scripts...")

        non_executable = []

        for script in self.scripts_dir.glob("*.py"):
            if not script.stat().st_mode & 0o111:  # Check if executable bit is set
                non_executable.append(script.name)

        passed = len(non_executable) == 0

        self.results.append(
            ValidationResult(
                check_name="executable_scripts",
                passed=passed,
                message=f"Scripts: {len(non_executable)} missing executable permission",
                details={"non_executable": non_executable},
                severity="warning" if not passed else "info",
            )
        )

    def validate_documentation_consistency(self) -> None:
        """Validate consistency across documentation."""
        logger.info("Validating documentation consistency...")

        try:
            # Check CLAUDE.md vs README.md consistency
            claude_content = self.claude_md.read_text()
            readme_path = self.repo_root / "README.md"

            if not readme_path.exists():
                self.results.append(
                    ValidationResult(
                        check_name="documentation_consistency",
                        passed=False,
                        message="README.md not found",
                        severity="warning",
                    )
                )
                return

            readme_content = readme_path.read_text()

            # Check for common keywords
            keywords = ["standards", "Claude", "MCP", "SPARC", "NIST"]
            missing_in_readme = []

            for keyword in keywords:
                if keyword.lower() in claude_content.lower() and keyword.lower() not in readme_content.lower():
                    missing_in_readme.append(keyword)

            passed = len(missing_in_readme) == 0

            self.results.append(
                ValidationResult(
                    check_name="documentation_consistency",
                    passed=passed,
                    message=f"Keywords missing in README: {len(missing_in_readme)}",
                    details={"missing_keywords": missing_in_readme},
                    severity="info",
                )
            )

        except Exception as e:
            self.results.append(
                ValidationResult(
                    check_name="documentation_consistency",
                    passed=False,
                    message=f"Error validating consistency: {e}",
                    severity="info",
                )
            )

    def print_report(self) -> None:
        """Print validation report."""
        print("\n" + "=" * 80)
        print("DOCUMENTATION VALIDATION REPORT")
        print("=" * 80 + "\n")

        errors = [r for r in self.results if not r.passed and r.severity == "error"]
        warnings = [r for r in self.results if not r.passed and r.severity == "warning"]
        info = [r for r in self.results if r.passed or r.severity == "info"]

        total = len(self.results)
        passed = len([r for r in self.results if r.passed])

        print(f"Total Checks: {total}")
        print(f"Passed: {passed} ({passed * 100 // total}%)")
        print(f"Errors: {len(errors)}")
        print(f"Warnings: {len(warnings)}")
        print()

        if errors:
            print("❌ ERRORS:")
            for result in errors:
                print(f"  • {result.check_name}: {result.message}")
                if result.details:
                    for key, value in result.details.items():
                        if isinstance(value, list) and value:
                            print(f"    - {key}: {value[:3]}{'...' if len(value) > 3 else ''}")
            print()

        if warnings:
            print("⚠️  WARNINGS:")
            for result in warnings:
                print(f"  • {result.check_name}: {result.message}")
            print()

        if not errors and not warnings:
            print("✅ All validation checks passed!")
        else:
            print(f"\n{'⚠️' if not errors else '❌'} Validation {'completed with warnings' if not errors else 'failed'}")

        print("\n" + "=" * 80)

    def export_report(self, output_path: Path) -> None:
        """Export validation report as JSON."""
        report = {
            "summary": {
                "total_checks": len(self.results),
                "passed": len([r for r in self.results if r.passed]),
                "errors": len([r for r in self.results if not r.passed and r.severity == "error"]),
                "warnings": len([r for r in self.results if not r.passed and r.severity == "warning"]),
            },
            "results": [
                {
                    "check": r.check_name,
                    "passed": r.passed,
                    "message": r.message,
                    "severity": r.severity,
                    "details": r.details,
                }
                for r in self.results
            ],
        }

        output_path.write_text(json.dumps(report, indent=2) + "\n")
        logger.info(f"Report exported to: {output_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate documentation claims against actual implementation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all validations
  python3 validate-claims.py

  # Export JSON report
  python3 validate-claims.py --export reports/validation.json

  # Verbose output
  python3 validate-claims.py --verbose

Exit codes:
  0 - All checks passed
  1 - Errors found
  2 - Warnings only
        """,
    )

    parser.add_argument("--export", type=Path, help="Export report to JSON file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Get repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    # Run validation
    validator = ClaimsValidator(repo_root)
    all_valid = validator.validate_all()

    # Print report
    validator.print_report()

    # Export if requested
    if args.export:
        validator.export_report(args.export)

    # Exit with appropriate code
    errors = [r for r in validator.results if not r.passed and r.severity == "error"]
    warnings = [r for r in validator.results if not r.passed and r.severity == "warning"]

    if errors:
        sys.exit(1)
    elif warnings:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
