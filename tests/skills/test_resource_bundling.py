#!/usr/bin/env python3
"""
Test Suite: Resource Bundling
Validates that resources are properly bundled within skills.
"""

import json
from pathlib import Path

import pytest


class ResourceBundlingValidator:
    """Validate resource bundling in skills."""

    EXPECTED_RESOURCE_DIRS = ["resources", "templates", "scripts", "examples"]
    VALID_RESOURCE_EXTENSIONS = [".md", ".txt", ".yaml", ".yml", ".json", ".sh", ".py", ".js", ".ts"]

    def __init__(self, skills_dir: Path):
        self.skills_dir = Path(skills_dir)

    def find_all_skills(self) -> list[Path]:
        """Find all skill directories."""
        if not self.skills_dir.exists():
            return []

        skills = []
        for item in self.skills_dir.iterdir():
            if item.is_dir() and (item / "SKILL.md").exists():
                skills.append(item)
        return skills

    def analyze_skill_resources(self, skill_dir: Path) -> dict:
        """Analyze resource structure for a skill."""
        result = {
            "skill_name": skill_dir.name,
            "has_skill_md": (skill_dir / "SKILL.md").exists(),
            "resource_dirs": {},
            "total_resources": 0,
            "resources_by_type": {},
            "issues": [],
        }

        # Check each expected resource directory
        for resource_dir_name in self.EXPECTED_RESOURCE_DIRS:
            resource_dir = skill_dir / resource_dir_name

            if resource_dir.exists() and resource_dir.is_dir():
                resources = self._scan_resource_dir(resource_dir)
                result["resource_dirs"][resource_dir_name] = resources
                result["total_resources"] += len(resources)

                # Categorize by extension
                for resource in resources:
                    ext = resource["extension"]
                    if ext not in result["resources_by_type"]:
                        result["resources_by_type"][ext] = 0
                    result["resources_by_type"][ext] += 1

        # Validate resource references in SKILL.md
        if result["has_skill_md"]:
            referenced, unreferenced = self._check_resource_references(skill_dir)
            result["referenced_resources"] = referenced
            result["unreferenced_resources"] = unreferenced

            if unreferenced:
                result["issues"].append(f"Unreferenced resources: {len(unreferenced)}")

        return result

    def _scan_resource_dir(self, resource_dir: Path) -> list[dict]:
        """Scan a resource directory for files."""
        resources = []

        for item in resource_dir.rglob("*"):
            if item.is_file():
                resources.append(
                    {
                        "path": str(item.relative_to(resource_dir)),
                        "full_path": str(item),
                        "extension": item.suffix,
                        "size_bytes": item.stat().st_size,
                    }
                )

        return resources

    def _check_resource_references(self, skill_dir: Path) -> tuple:
        """Check which resources are referenced in SKILL.md."""
        skill_md = skill_dir / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")

        # Find all resource references (./resources/, ./templates/, etc.)
        import re

        pattern = r"\./(resources|templates|scripts|examples)/([^\s\)]+)"
        references = re.findall(pattern, content)

        referenced = set()
        for resource_type, resource_path in references:
            referenced.add(f"{resource_type}/{resource_path}")

        # Find actual resources
        actual_resources = set()
        for resource_dir_name in self.EXPECTED_RESOURCE_DIRS:
            resource_dir = skill_dir / resource_dir_name
            if resource_dir.exists():
                for item in resource_dir.rglob("*"):
                    if item.is_file():
                        rel_path = f"{resource_dir_name}/{item.relative_to(resource_dir)}"
                        actual_resources.add(rel_path)

        unreferenced = actual_resources - referenced

        return list(referenced), list(unreferenced)

    def validate_resource_accessibility(self, skill_dir: Path) -> dict:
        """Validate that resources are accessible and valid."""
        result = {"skill_name": skill_dir.name, "accessible": True, "issues": []}

        for resource_dir_name in self.EXPECTED_RESOURCE_DIRS:
            resource_dir = skill_dir / resource_dir_name

            if not resource_dir.exists():
                continue

            for item in resource_dir.rglob("*"):
                if not item.is_file():
                    continue

                # Check file is readable
                try:
                    item.read_bytes()
                except Exception as e:
                    result["accessible"] = False
                    result["issues"].append(f"Cannot read {item}: {e}")

                # Check extension is valid
                if item.suffix not in self.VALID_RESOURCE_EXTENSIONS:
                    result["issues"].append(f"Unexpected file type: {item} ({item.suffix})")

                # Check for executable scripts
                if item.suffix in [".sh", ".py"]:
                    if not self._is_executable(item):
                        result["issues"].append(f"Script not executable: {item}")

        return result

    def _is_executable(self, file_path: Path) -> bool:
        """Check if file is executable."""
        import stat

        return bool(file_path.stat().st_mode & stat.S_IXUSR)

    def analyze_all_skills(self) -> dict:
        """Analyze resource bundling for all skills."""
        skills = self.find_all_skills()

        results = {
            "total_skills": len(skills),
            "skills_with_resources": 0,
            "total_resources": 0,
            "resource_breakdown": {},
            "skills": [],
        }

        for skill_dir in skills:
            analysis = self.analyze_skill_resources(skill_dir)
            results["skills"].append(analysis)

            if analysis["total_resources"] > 0:
                results["skills_with_resources"] += 1
                results["total_resources"] += analysis["total_resources"]

            # Aggregate resource types
            for ext, count in analysis["resources_by_type"].items():
                if ext not in results["resource_breakdown"]:
                    results["resource_breakdown"][ext] = 0
                results["resource_breakdown"][ext] += count

        return results


# Test cases
class TestResourceBundling:
    """Test resource bundling in skills."""

    @pytest.fixture
    def validator(self, tmp_path):
        """Create validator with sample skills."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        # Create skill with resources
        skill_dir = skills_dir / "test-skill"
        skill_dir.mkdir()

        # Create SKILL.md with resource references
        (skill_dir / "SKILL.md").write_text(
            """---
name: test-skill
description: Test skill with resources
---

# Test Skill

See ./resources/guide.md for details.
Use ./templates/config.yaml as template.
Run ./scripts/setup.sh to configure.
"""
        )

        # Create resource directories
        (skill_dir / "resources").mkdir()
        (skill_dir / "resources" / "guide.md").write_text("# Guide\n\nDetailed guide.")

        (skill_dir / "templates").mkdir()
        (skill_dir / "templates" / "config.yaml").write_text("key: value")

        (skill_dir / "scripts").mkdir()
        (skill_dir / "scripts" / "setup.sh").write_text("#!/bin/bash\necho 'Setup'")

        return ResourceBundlingValidator(skills_dir)

    def test_skill_has_resources(self, validator):
        """Test that skill with resources is detected."""
        skills = validator.find_all_skills()
        assert len(skills) > 0

        analysis = validator.analyze_skill_resources(skills[0])
        assert analysis["total_resources"] > 0
        assert len(analysis["resource_dirs"]) > 0

    def test_resource_directories_detected(self, validator):
        """Test that resource directories are properly detected."""
        skills = validator.find_all_skills()
        analysis = validator.analyze_skill_resources(skills[0])

        assert "resources" in analysis["resource_dirs"]
        assert "templates" in analysis["resource_dirs"]
        assert "scripts" in analysis["resource_dirs"]

    def test_resource_types_categorized(self, validator):
        """Test that resources are categorized by type."""
        skills = validator.find_all_skills()
        analysis = validator.analyze_skill_resources(skills[0])

        assert ".md" in analysis["resources_by_type"]
        assert ".yaml" in analysis["resources_by_type"]
        assert ".sh" in analysis["resources_by_type"]

    def test_referenced_resources_detected(self, validator):
        """Test that referenced resources are detected."""
        skills = validator.find_all_skills()
        analysis = validator.analyze_skill_resources(skills[0])

        assert len(analysis["referenced_resources"]) > 0
        assert any("guide.md" in ref for ref in analysis["referenced_resources"])

    def test_unreferenced_resources_detected(self, tmp_path):
        """Test detection of unreferenced resources."""
        skills_dir = tmp_path / "skills" / "unreferenced-skill"
        skills_dir.mkdir(parents=True)

        # Create SKILL.md without references
        (skills_dir / "SKILL.md").write_text(
            """---
name: unreferenced-skill
description: Skill with unreferenced resources
---

# Skill

No resource references here.
"""
        )

        # Create unreferenced resource
        (skills_dir / "resources").mkdir()
        (skills_dir / "resources" / "orphan.md").write_text("# Orphan")

        validator = ResourceBundlingValidator(tmp_path / "skills")
        analysis = validator.analyze_skill_resources(skills_dir)

        assert len(analysis["unreferenced_resources"]) > 0
        assert any("orphan.md" in unref for unref in analysis["unreferenced_resources"])

    def test_resource_accessibility(self, validator):
        """Test that resources are accessible."""
        skills = validator.find_all_skills()
        validation = validator.validate_resource_accessibility(skills[0])

        assert validation["accessible"] == True

    def test_aggregate_analysis(self, validator):
        """Test aggregate analysis of all skills."""
        results = validator.analyze_all_skills()

        assert results["total_skills"] > 0
        assert results["skills_with_resources"] > 0
        assert results["total_resources"] > 0
        assert len(results["resource_breakdown"]) > 0


if __name__ == "__main__":
    # Run resource bundling analysis
    repo_root = Path(__file__).parent.parent.parent
    skills_dir = repo_root / "docs" / "skills"

    print("\n=== Resource Bundling Analysis ===\n")

    if skills_dir.exists():
        validator = ResourceBundlingValidator(skills_dir)
        results = validator.analyze_all_skills()

        print(f"Total skills: {results['total_skills']}")
        print(f"Skills with resources: {results['skills_with_resources']}")
        print(f"Total resources: {results['total_resources']}")

        print("\nResource breakdown by type:")
        for ext, count in sorted(results["resource_breakdown"].items()):
            print(f"  {ext}: {count}")

        print("\nPer-skill details:")
        for skill in results["skills"]:
            print(f"\n{skill['skill_name']}:")
            print(f"  Resources: {skill['total_resources']}")

            if skill["issues"]:
                print("  Issues:")
                for issue in skill["issues"]:
                    print(f"    - {issue}")

        # Save report
        report_path = repo_root / "reports" / "generated" / "resource-bundling.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\nDetailed report saved to: {report_path}")
    else:
        print(f"Skills directory not found: {skills_dir}")
        print("Run pytest to execute unit tests.")
