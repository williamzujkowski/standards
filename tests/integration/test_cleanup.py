"""
Test suite for repository cleanup and __pycache__ exclusion.

London School TDD approach - testing cleanup behavior and exclusion rules.

RED PHASE: These tests will FAIL until cleanup is performed.
"""

import pytest
from pathlib import Path
from typing import List, Set, Dict
import json


class MockCleanupService:
    """Mock for cleanup service behavior"""

    def find_pycache_dirs(self, root: Path) -> List[Path]:
        """Mock method - will be replaced with real implementation"""
        raise NotImplementedError("Implementation required")

    def find_orphan_files(self, root: Path, exclusions: Set[str]) -> List[Path]:
        """Mock method - will be replaced with real implementation"""
        raise NotImplementedError("Implementation required")


class MockAuditService:
    """Mock for audit service behavior"""

    def generate_audit(self, root: Path) -> Dict:
        """Mock method - will be replaced with real implementation"""
        raise NotImplementedError("Implementation required")


class TestPycacheDetection:
    """Test detection of __pycache__ directories"""

    @pytest.fixture
    def cleanup_service(self):
        return MockCleanupService()

    @pytest.fixture
    def repo_root(self):
        return Path("/home/william/git/standards")

    def test_finds_pycache_directories(self, cleanup_service, repo_root):
        """Should find all __pycache__ directories"""
        # WHEN: Scanning for __pycache__
        pycache_dirs = cleanup_service.find_pycache_dirs(repo_root)

        # THEN: Should find any existing __pycache__ dirs
        # (This test will pass if none exist, which is desired state)
        for pycache_dir in pycache_dirs:
            assert pycache_dir.name == "__pycache__", f"Found directory is actually __pycache__: {pycache_dir}"

    def test_pycache_not_in_docs(self, repo_root):
        """__pycache__ should not exist in docs/ directory"""
        docs_dir = repo_root / "docs"

        if docs_dir.exists():
            pycache_in_docs = list(docs_dir.rglob("__pycache__"))
            assert len(pycache_in_docs) == 0, f"Found __pycache__ in docs/: {pycache_in_docs}"

    def test_pycache_not_in_config(self, repo_root):
        """__pycache__ should not exist in config/ directory"""
        config_dir = repo_root / "config"

        if config_dir.exists():
            pycache_in_config = list(config_dir.rglob("__pycache__"))
            assert len(pycache_in_config) == 0, f"Found __pycache__ in config/: {pycache_in_config}"

    def test_pycache_allowed_in_tests(self, repo_root):
        """__pycache__ is acceptable in tests/ directory"""
        # This is informational - tests may have __pycache__
        tests_dir = repo_root / "tests"

        # We don't fail if __pycache__ exists here, but we track it
        if tests_dir.exists():
            pycache_in_tests = list(tests_dir.rglob("__pycache__"))
            # Just log, don't assert
            print(f"Found {len(pycache_in_tests)} __pycache__ dirs in tests/ (acceptable)")


class TestGitignoreConfiguration:
    """Test .gitignore properly excludes __pycache__"""

    @pytest.fixture
    def repo_root(self):
        return Path("/home/william/git/standards")

    def test_gitignore_excludes_pycache(self, repo_root):
        """Gitignore should exclude __pycache__"""
        gitignore = repo_root / ".gitignore"

        assert gitignore.exists(), ".gitignore file should exist"

        content = gitignore.read_text()

        # Should have __pycache__ exclusion
        assert (
            "__pycache__" in content or "__pycache__/" in content or "**/__pycache__" in content
        ), ".gitignore should exclude __pycache__"

    def test_gitignore_excludes_pyc_files(self, repo_root):
        """Gitignore should exclude .pyc files"""
        gitignore = repo_root / ".gitignore"
        content = gitignore.read_text()

        assert "*.pyc" in content or ".pyc" in content, ".gitignore should exclude .pyc files"

    def test_gitignore_excludes_pyo_files(self, repo_root):
        """Gitignore should exclude .pyo files"""
        gitignore = repo_root / ".gitignore"
        content = gitignore.read_text()

        assert "*.pyo" in content or ".pyo" in content, ".gitignore should exclude .pyo files"


class TestAuditRulesConfiguration:
    """Test audit-rules.yaml properly excludes __pycache__"""

    @pytest.fixture
    def audit_rules_path(self):
        return Path("/home/william/git/standards/config/audit-rules.yaml")

    def test_audit_rules_exist(self, audit_rules_path):
        """Audit rules configuration should exist"""
        assert audit_rules_path.exists(), f"Audit rules not found at {audit_rules_path}"

    def test_audit_rules_exclude_pycache(self, audit_rules_path):
        """Audit rules should exclude __pycache__ from scans"""
        import yaml

        with open(audit_rules_path) as f:
            rules = yaml.safe_load(f)

        assert "exclusions" in rules or "exclude" in rules, "Audit rules should have exclusions section"

        exclusions = rules.get("exclusions", []) or rules.get("exclude", [])

        # Should exclude __pycache__
        pycache_excluded = any("__pycache__" in str(excl).lower() for excl in exclusions)

        assert pycache_excluded, "Audit rules should exclude __pycache__ directories"


class TestOrphanFileResolution:
    """Test detection and resolution of orphan files"""

    @pytest.fixture
    def cleanup_service(self):
        return MockCleanupService()

    @pytest.fixture
    def repo_root(self):
        return Path("/home/william/git/standards")

    @pytest.fixture
    def standard_exclusions(self):
        """Standard directories to exclude from orphan detection"""
        return {
            ".claude",
            "subagents",
            "memory",
            "prompts",
            "reports/generated",
            ".vscode",
            ".git",
            "node_modules",
            "__pycache__",
            ".github",
        }

    def test_identifies_orphan_markdown_files(self, cleanup_service, repo_root, standard_exclusions):
        """Should identify markdown files not linked from hubs"""
        # WHEN: Scanning for orphans
        orphans = cleanup_service.find_orphan_files(repo_root, standard_exclusions)

        # THEN: Orphans should be outside hub coverage
        for orphan in orphans:
            assert orphan.suffix == ".md", f"Orphan should be markdown: {orphan}"

    def test_orphan_count_within_limit(self, cleanup_service, repo_root, standard_exclusions):
        """Orphan count should be within acceptable limit"""
        # GIVEN: Orphan limit from configuration
        orphan_limit = 5  # From CLAUDE.md gatekeeper

        # WHEN: Counting orphans
        orphans = cleanup_service.find_orphan_files(repo_root, standard_exclusions)

        # THEN: Should be at or below limit
        assert len(orphans) <= orphan_limit, f"Found {len(orphans)} orphans, limit is {orphan_limit}: {orphans}"

    def test_excluded_directories_not_scanned(self, cleanup_service, repo_root, standard_exclusions):
        """Excluded directories should not be scanned for orphans"""
        # WHEN: Finding orphans
        orphans = cleanup_service.find_orphan_files(repo_root, standard_exclusions)

        # THEN: No orphans should be in excluded directories
        for orphan in orphans:
            orphan_parts = orphan.parts
            for exclusion in standard_exclusions:
                assert exclusion not in orphan_parts, f"Orphan found in excluded directory {exclusion}: {orphan}"


class TestAuditReportGeneration:
    """Test audit report generation and validation"""

    @pytest.fixture
    def audit_service(self):
        return MockAuditService()

    @pytest.fixture
    def repo_root(self):
        return Path("/home/william/git/standards")

    @pytest.fixture
    def audit_report_path(self):
        return Path("/home/william/git/standards/reports/generated/structure-audit.json")

    def test_generates_audit_report(self, audit_service, repo_root):
        """Should generate structured audit report"""
        # WHEN: Generating audit
        audit = audit_service.generate_audit(repo_root)

        # THEN: Should have required sections
        assert "broken_links" in audit, "Audit should track broken links"
        assert "hub_violations" in audit, "Audit should track hub violations"
        assert "orphans" in audit, "Audit should track orphans"

    def test_audit_report_json_valid(self, audit_report_path):
        """Audit report should be valid JSON"""
        if audit_report_path.exists():
            try:
                with open(audit_report_path) as f:
                    audit = json.load(f)
                assert isinstance(audit, dict), "Audit report should be JSON object"
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON in audit report: {e}")

    def test_audit_gates_enforced(self, audit_report_path):
        """Audit gates should be enforced"""
        if audit_report_path.exists():
            with open(audit_report_path) as f:
                audit = json.load(f)

            # GATE 1: No broken links
            broken_links = audit.get("broken_links", 0)
            assert broken_links == 0, f"GATE FAILURE: {broken_links} broken links found"

            # GATE 2: No hub violations
            hub_violations = audit.get("hub_violations", 0)
            assert hub_violations == 0, f"GATE FAILURE: {hub_violations} hub violations found"

            # GATE 3: Orphans within limit
            orphan_limit = 5
            orphans = audit.get("orphans", 0)
            assert orphans <= orphan_limit, f"GATE FAILURE: {orphans} orphans found, limit is {orphan_limit}"


class TestCleanupIntegration:
    """Integration tests for cleanup operations"""

    @pytest.fixture
    def repo_root(self):
        return Path("/home/william/git/standards")

    def test_no_pycache_in_tracked_dirs(self, repo_root):
        """No __pycache__ should exist in version-controlled directories"""
        tracked_dirs = ["docs", "config", "examples", "monitoring", "tools-config"]

        for dir_name in tracked_dirs:
            dir_path = repo_root / dir_name
            if dir_path.exists():
                pycache_dirs = list(dir_path.rglob("__pycache__"))
                assert len(pycache_dirs) == 0, f"Found __pycache__ in {dir_name}/: {pycache_dirs}"

    def test_no_pyc_files_in_tracked_dirs(self, repo_root):
        """No .pyc files should exist in version-controlled directories"""
        tracked_dirs = ["docs", "config", "examples", "monitoring", "tools-config"]

        for dir_name in tracked_dirs:
            dir_path = repo_root / dir_name
            if dir_path.exists():
                pyc_files = list(dir_path.rglob("*.pyc"))
                assert len(pyc_files) == 0, f"Found .pyc files in {dir_name}/: {pyc_files}"

    def test_cleanup_is_idempotent(self):
        """Running cleanup multiple times should produce same result"""
        # GIVEN: Initial cleanup
        # cleanup_service.cleanup()
        # initial_state = get_directory_state()

        # WHEN: Running cleanup again
        # cleanup_service.cleanup()
        # final_state = get_directory_state()

        # THEN: State should be identical
        # assert initial_state == final_state
        pass  # Will implement with cleanup service


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
