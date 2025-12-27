#!/usr/bin/env python3
"""
Unit tests for hub enforcement validation.
Tests that AUTO-LINKS sections are properly parsed and hub violations detected.
"""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


# Load generate-audit-reports.py module
spec = importlib.util.spec_from_file_location(
    "generate_audit_reports", Path(__file__).parent.parent / "generate-audit-reports.py"
)
generate_audit_reports = importlib.util.module_from_spec(spec)
sys.modules["generate_audit_reports"] = generate_audit_reports
spec.loader.exec_module(generate_audit_reports)

# Import functions
build_link_graph = generate_audit_reports.build_link_graph
enforce_hub_rules = generate_audit_reports.enforce_hub_rules
parse_autolinks_section = generate_audit_reports.parse_autolinks_section


class TestHubEnforcement(unittest.TestCase):
    """Test hub enforcement and AUTO-LINKS parsing."""

    def test_parse_autolinks_section(self):
        """Test deterministic AUTO-LINKS parsing."""
        content = """
# Test Document

Some content here.

<!-- AUTO-LINKS:docs/standards/** -->

- [Standard 1](docs/standards/FOO.md)
- [Standard 2](docs/standards/BAR.md)
- [External](https://example.com)

<!-- /AUTO-LINKS -->

More content with [regular link](other.md).

<!-- AUTO-LINKS:docs/guides/** -->

- [Guide 1](docs/guides/GUIDE.md)

<!-- /AUTO-LINKS -->
"""

        links = parse_autolinks_section(content)

        # Should find 4 links from AUTO-LINKS blocks
        self.assertEqual(len(links), 4)

        # Check specific links
        link_urls = [link[1] for link in links]
        self.assertIn("docs/standards/FOO.md", link_urls)
        self.assertIn("docs/standards/BAR.md", link_urls)
        self.assertIn("https://example.com", link_urls)
        self.assertIn("docs/guides/GUIDE.md", link_urls)

        # Should NOT include the regular link outside AUTO-LINKS
        self.assertNotIn("other.md", link_urls)

    def test_hub_graph_with_autolinks(self):
        """Test that AUTO-LINKS create proper inbound edges in graph."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)

            # Create directory structure
            (tmp / "docs" / "standards").mkdir(parents=True)

            # Create hub file with AUTO-LINKS
            hub_content = """# Unified Standards

This is the hub document.

<!-- AUTO-LINKS:docs/standards/** -->

- [Foo Standard](FOO.md)
- [Bar Standard](BAR.md)

<!-- /AUTO-LINKS -->
"""
            hub_path = tmp / "docs" / "standards" / "UNIFIED_STANDARDS.md"
            hub_path.write_text(hub_content)

            # Create target files
            foo_path = tmp / "docs" / "standards" / "FOO.md"
            foo_path.write_text("# Foo Standard\n\nContent here.")

            bar_path = tmp / "docs" / "standards" / "BAR.md"
            bar_path.write_text("# Bar Standard\n\nContent here.")

            # Create a file NOT in AUTO-LINKS
            orphan_path = tmp / "docs" / "standards" / "ORPHAN.md"
            orphan_path.write_text("# Orphan Standard\n\nNot linked from hub.")

            # Build graph with our test files
            all_md_files = list(tmp.rglob("*.md"))

            # Temporarily change ROOT for testing
            old_root = generate_audit_reports.ROOT
            generate_audit_reports.ROOT = tmp

            try:
                graph, _, _ = build_link_graph(all_md_files)

                # FOO.md should have hub as inbound
                foo_key = "docs/standards/FOO.md"
                self.assertIn(foo_key, graph)
                self.assertIn("docs/standards/UNIFIED_STANDARDS.md", graph[foo_key])

                # BAR.md should have hub as inbound
                bar_key = "docs/standards/BAR.md"
                self.assertIn(bar_key, graph)
                self.assertIn("docs/standards/UNIFIED_STANDARDS.md", graph[bar_key])

                # ORPHAN.md should NOT have hub as inbound
                orphan_key = "docs/standards/ORPHAN.md"
                if orphan_key in graph:
                    self.assertNotIn("docs/standards/UNIFIED_STANDARDS.md", graph.get(orphan_key, set()))

            finally:
                generate_audit_reports.ROOT = old_root

    def test_hub_violations_detection(self):
        """Test that hub violations are properly detected."""
        # Create a simple graph
        graph = {
            "docs/standards/FOO.md": {"docs/standards/UNIFIED_STANDARDS.md"},  # Linked from hub
            "docs/standards/BAR.md": set(),  # NOT linked from hub
            "docs/standards/UNIFIED_STANDARDS.md": set(),  # The hub itself
        }

        # Hub rules
        rules = {
            "orphans": {
                "exclude": [],
                "require_link_from": [
                    {"pattern": "docs/standards/**/*.md", "hubs": ["docs/standards/UNIFIED_STANDARDS.md"]}
                ],
            }
        }

        violations, matrix = enforce_hub_rules(graph, rules)

        # BAR.md should be a violation (not linked from hub)
        self.assertIn("docs/standards/BAR.md", violations)

        # FOO.md should NOT be a violation (linked from hub)
        self.assertNotIn("docs/standards/FOO.md", violations)

        # Hub itself should NOT be a violation
        self.assertNotIn("docs/standards/UNIFIED_STANDARDS.md", violations)

        # Check matrix
        self.assertTrue(matrix["docs/standards/FOO.md"]["docs/standards/UNIFIED_STANDARDS.md"])
        self.assertFalse(matrix["docs/standards/BAR.md"]["docs/standards/UNIFIED_STANDARDS.md"])


if __name__ == "__main__":
    unittest.main()
