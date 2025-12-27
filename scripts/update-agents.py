#!/usr/bin/env python3
"""
Update agent configurations for repository optimization.

Updates:
- Agent definitions in .claude/ directory
- Swarm coordination files
- Memory configurations
- Hive mind settings
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import yaml


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class AgentUpdater:
    """Updates agent configurations."""

    def __init__(self, repo_root: Path, dry_run: bool = False):
        self.repo_root = repo_root
        self.dry_run = dry_run
        self.claude_dir = repo_root / ".claude"
        self.updates_made: list[str] = []

    def log_update(self, message: str) -> None:
        """Log an update."""
        self.updates_made.append(message)
        logger.info(message)

    def ensure_directories(self) -> None:
        """Ensure required directories exist."""
        logger.info("Ensuring agent directories exist...")

        required_dirs = [
            ".claude",
            ".claude/agents",
            ".claude/swarms",
            ".claude/memory",
            ".hive-mind",
            ".hive-mind/sessions",
        ]

        for dir_path in required_dirs:
            full_path = self.repo_root / dir_path
            if not full_path.exists():
                if not self.dry_run:
                    full_path.mkdir(parents=True, exist_ok=True)
                    (full_path / ".gitkeep").touch()
                self.log_update(f"Created directory: {dir_path}")

    def update_agent_definitions(self) -> None:
        """Update agent definition files."""
        logger.info("Updating agent definitions...")

        # Standard agent types
        agent_types = {
            "coder": {
                "name": "Coder",
                "description": "Implements code following specifications and best practices",
                "capabilities": ["code-generation", "refactoring", "optimization", "testing"],
                "priority": "high",
            },
            "reviewer": {
                "name": "Reviewer",
                "description": "Reviews code for quality, security, and compliance",
                "capabilities": ["code-review", "security-audit", "quality-check", "documentation-review"],
                "priority": "high",
            },
            "tester": {
                "name": "Tester",
                "description": "Creates and executes tests, validates functionality",
                "capabilities": ["test-generation", "test-execution", "coverage-analysis", "regression-testing"],
                "priority": "high",
            },
            "researcher": {
                "name": "Researcher",
                "description": "Analyzes requirements and researches solutions",
                "capabilities": [
                    "requirements-analysis",
                    "solution-research",
                    "documentation-review",
                    "trend-analysis",
                ],
                "priority": "medium",
            },
            "planner": {
                "name": "Planner",
                "description": "Creates task plans and coordinates workflows",
                "capabilities": ["task-planning", "workflow-design", "resource-allocation", "dependency-mapping"],
                "priority": "high",
            },
            "architect": {
                "name": "Architect",
                "description": "Designs system architecture and technical solutions",
                "capabilities": [
                    "architecture-design",
                    "system-design",
                    "scalability-planning",
                    "technology-selection",
                ],
                "priority": "high",
            },
        }

        agents_dir = self.claude_dir / "agents"

        for agent_id, config in agent_types.items():
            agent_file = agents_dir / f"{agent_id}.yaml"

            # Add metadata
            full_config = {**config, "updated": datetime.now().isoformat(), "version": "2.0"}

            if not self.dry_run:
                if not agents_dir.exists():
                    agents_dir.mkdir(parents=True, exist_ok=True)
                agent_file.write_text(yaml.dump(full_config, sort_keys=False))

            self.log_update(f"Updated agent definition: {agent_id}")

    def update_swarm_configs(self) -> None:
        """Update swarm coordination configurations."""
        logger.info("Updating swarm configurations...")

        swarm_configs = {
            "default": {
                "topology": "mesh",
                "max_agents": 8,
                "strategy": "adaptive",
                "coordination": {"sync_interval": 30, "health_check_interval": 60, "timeout": 300},
            },
            "development": {
                "topology": "hierarchical",
                "max_agents": 6,
                "strategy": "sequential",
                "agents": ["planner", "architect", "coder", "tester", "reviewer"],
            },
            "analysis": {
                "topology": "star",
                "max_agents": 5,
                "strategy": "parallel",
                "agents": ["researcher", "analyst", "documenter"],
            },
        }

        swarms_dir = self.claude_dir / "swarms"

        for swarm_name, config in swarm_configs.items():
            swarm_file = swarms_dir / f"{swarm_name}.yaml"

            # Add metadata
            full_config = {**config, "updated": datetime.now().isoformat(), "version": "2.0"}

            if not self.dry_run:
                if not swarms_dir.exists():
                    swarms_dir.mkdir(parents=True, exist_ok=True)
                swarm_file.write_text(yaml.dump(full_config, sort_keys=False))

            self.log_update(f"Updated swarm configuration: {swarm_name}")

    def update_memory_configs(self) -> None:
        """Update memory configurations."""
        logger.info("Updating memory configurations...")

        memory_config = {
            "storage": {"type": "file", "path": ".claude/memory", "max_size_mb": 100},
            "namespaces": {
                "hive": {"description": "Hive mind coordination", "ttl": 86400},
                "swarm": {"description": "Swarm memory", "ttl": 43200},
                "agent": {"description": "Individual agent memory", "ttl": 21600},
                "task": {"description": "Task-specific memory", "ttl": 3600},
            },
            "persistence": {"enabled": True, "compression": True, "backup_interval": 3600},
        }

        memory_file = self.claude_dir / "memory-config.yaml"

        if not self.dry_run:
            memory_file.write_text(yaml.dump(memory_config, sort_keys=False))

        self.log_update("Updated memory configuration")

    def update_hive_mind_config(self) -> None:
        """Update hive mind configuration."""
        logger.info("Updating hive mind configuration...")

        hive_config = {
            "version": "2.0",
            "coordination": {
                "mode": "distributed",
                "consensus": "raft",
                "max_concurrent_tasks": 10,
                "task_timeout": 3600,
            },
            "agents": {"auto_spawn": True, "max_agents": 20, "resource_limits": {"memory_mb": 512, "cpu_percent": 50}},
            "memory": {
                "shared": True,
                "sync_interval": 30,
                "conflict_resolution": "last-write-wins",
            },
            "monitoring": {
                "enabled": True,
                "metrics_interval": 60,
                "log_level": "info",
            },
        }

        hive_file = self.repo_root / ".hive-mind" / "config.yaml"

        if not self.dry_run:
            hive_file.parent.mkdir(parents=True, exist_ok=True)
            hive_file.write_text(yaml.dump(hive_config, sort_keys=False))

        self.log_update("Updated hive mind configuration")

    def create_gitignore(self) -> None:
        """Create .gitignore for agent directories."""
        logger.info("Creating .gitignore files...")

        gitignore_content = """# Agent runtime files
*.log
*.tmp
*.cache

# Session files
sessions/
active-sessions.json

# Generated reports
reports/

# Memory snapshots
snapshots/

# Keep structure
!.gitkeep
"""

        gitignore_paths = [
            self.claude_dir / ".gitignore",
            self.repo_root / ".hive-mind" / ".gitignore",
        ]

        for gitignore_path in gitignore_paths:
            if not gitignore_path.exists():
                if not self.dry_run:
                    gitignore_path.parent.mkdir(parents=True, exist_ok=True)
                    gitignore_path.write_text(gitignore_content)
                self.log_update(f"Created .gitignore: {gitignore_path.relative_to(self.repo_root)}")

    def validate_configurations(self) -> bool:
        """Validate all configuration files."""
        logger.info("Validating configurations...")

        if self.dry_run:
            logger.info("DRY RUN: Skipping validation")
            return True

        validation_passed = True

        # Validate agent configs
        agents_dir = self.claude_dir / "agents"
        if agents_dir.exists():
            for agent_file in agents_dir.glob("*.yaml"):
                try:
                    yaml.safe_load(agent_file.read_text())
                    logger.debug(f"Valid: {agent_file.name}")
                except yaml.YAMLError as e:
                    logger.error(f"Invalid YAML in {agent_file.name}: {e}")
                    validation_passed = False

        # Validate swarm configs
        swarms_dir = self.claude_dir / "swarms"
        if swarms_dir.exists():
            for swarm_file in swarms_dir.glob("*.yaml"):
                try:
                    yaml.safe_load(swarm_file.read_text())
                    logger.debug(f"Valid: {swarm_file.name}")
                except yaml.YAMLError as e:
                    logger.error(f"Invalid YAML in {swarm_file.name}: {e}")
                    validation_passed = False

        return validation_passed

    def print_summary(self) -> None:
        """Print update summary."""
        print("\n" + "=" * 80)
        print("AGENT CONFIGURATION UPDATE SUMMARY")
        print("=" * 80)
        print(f"\nTotal updates: {len(self.updates_made)}")

        if self.dry_run:
            print("\n⚠️  DRY RUN - No changes were made")

        print("\nUpdates made:")
        for update in self.updates_made:
            print(f"  ✓ {update}")

        print("\n" + "=" * 80)

    def export_summary(self, output_path: Path) -> None:
        """Export update summary to file."""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": self.dry_run,
            "updates": self.updates_made,
            "total_updates": len(self.updates_made),
        }

        output_path.write_text(json.dumps(summary, indent=2) + "\n")
        logger.info(f"Summary exported to: {output_path}")

    def update_all(self) -> bool:
        """Run all updates."""
        logger.info("Starting agent configuration updates...")

        try:
            self.ensure_directories()
            self.update_agent_definitions()
            self.update_swarm_configs()
            self.update_memory_configs()
            self.update_hive_mind_config()
            self.create_gitignore()

            validation_passed = self.validate_configurations()

            self.print_summary()

            return validation_passed

        except Exception as e:
            logger.error(f"Update failed: {e}")
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Update agent configurations for repository optimization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (no changes)
  python3 update-agents.py --dry-run

  # Update all configurations
  python3 update-agents.py

  # Export summary
  python3 update-agents.py --summary updates.json

  # Verbose output
  python3 update-agents.py --verbose

Exit codes:
  0 - Update successful
  1 - Update failed
        """,
    )

    parser.add_argument("--dry-run", action="store_true", help="Perform dry run without making changes")

    parser.add_argument("--summary", type=Path, help="Export update summary to JSON file")

    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Get repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    # Run updates
    updater = AgentUpdater(repo_root, dry_run=args.dry_run)
    success = updater.update_all()

    # Export summary if requested
    if args.summary:
        updater.export_summary(args.summary)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
