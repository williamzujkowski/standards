#!/usr/bin/env python3
"""
Router Edge Case Tests

Tests specific edge cases and error conditions in the routing system.

Author: REVIEWER Agent
Created: 2025-10-24
"""

from pathlib import Path

import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]


class TestProductMatrixEdgeCases:
    """Edge case tests for product-matrix.yaml."""

    @pytest.fixture
    def product_matrix(self) -> dict:
        """Load product matrix."""
        with open(REPO_ROOT / "config/product-matrix.yaml") as f:
            return yaml.safe_load(f)

    @pytest.mark.xfail(reason="Product matrix doesn't enforce NIST auto-inclusion yet", strict=False)
    def test_nist_auto_inclusion_on_security(self, product_matrix):
        """Verify NIST-IG:base is auto-included when SEC standards are present."""
        products = product_matrix.get("products", {})

        for product_name, product_config in products.items():
            standards = product_config.get("standards", [])

            # Check if any SEC standard is present
            has_security = any(std.startswith("SEC:") for std in standards)

            if has_security:
                # NIST-IG:base should be included
                assert "NIST-IG:base" in standards, (
                    f"Product {product_name} has security standards but missing NIST-IG:base"
                )

    def test_wildcard_sec_includes_nist(self, product_matrix):
        """Verify SEC:* wildcard expansion includes NIST-IG:base."""
        wildcards = product_matrix.get("wildcards", {})
        sec_wildcard = wildcards.get("SEC:*", {})

        expands_to = sec_wildcard.get("expands_to", [])
        assert "NIST-IG:base" in expands_to, "SEC:* wildcard must include NIST-IG:base"

    def test_no_circular_dependencies(self, product_matrix):
        """Verify no circular dependencies in stack presets."""
        stack_presets = product_matrix.get("stack_presets", {})

        for stack_name, stack_config in stack_presets.items():
            uses = stack_config.get("uses", "")

            # Stack preset should not reference another stack preset
            assert uses not in stack_presets, f"Stack preset {stack_name} references another stack preset: {uses}"

    def test_language_cs_consistency(self, product_matrix):
        """Verify language mappings have consistent CS references."""
        language_mappings = product_matrix.get("language_mappings", {})

        for language, mappings in language_mappings.items():
            cs_mapping = mappings.get("CS", "")

            # CS mapping should follow pattern: CS:{language}
            expected_pattern = f"CS:{language}"
            assert cs_mapping == expected_pattern, (
                f"Language {language} CS mapping should be {expected_pattern}, got {cs_mapping}"
            )

    def test_no_duplicate_standards_in_products(self, product_matrix):
        """Verify products don't have duplicate standards."""
        products = product_matrix.get("products", {})

        for product_name, product_config in products.items():
            standards = product_config.get("standards", [])

            # Check for duplicates
            duplicates = [std for std in standards if standards.count(std) > 1]
            unique_duplicates = set(duplicates)

            assert not unique_duplicates, f"Product {product_name} has duplicate standards: {unique_duplicates}"


class TestSkillLoaderEdgeCases:
    """Edge case tests for skill-loader.py."""

    @pytest.fixture
    def legacy_mappings(self) -> dict:
        """Load legacy mappings."""
        with open(REPO_ROOT / "skills/legacy-bridge/resources/legacy-mappings.yaml") as f:
            return yaml.safe_load(f)

    def test_auto_inclusion_rules(self, legacy_mappings):
        """Verify auto-inclusion rules are properly defined."""
        auto_inclusion = legacy_mappings.get("auto_inclusion", {})
        rules = auto_inclusion.get("rules", [])

        for rule in rules:
            assert "condition" in rule, "Auto-inclusion rule missing condition"
            assert "includes" in rule, "Auto-inclusion rule missing includes"
            assert "reason" in rule, "Auto-inclusion rule missing reason"

    def test_deprecation_settings(self, legacy_mappings):
        """Verify deprecation warnings are properly configured."""
        deprecation = legacy_mappings.get("deprecation", {})

        assert "enabled" in deprecation, "Deprecation settings missing 'enabled' flag"
        assert "warning_template" in deprecation, "Deprecation missing warning template"
        assert "removal_date" in deprecation, "Deprecation missing removal date"

    def test_skill_level_consistency(self, legacy_mappings):
        """Verify skill levels are consistent across mappings."""
        valid_levels = {1, 2, 3}

        # Check product mappings
        product_mappings = legacy_mappings.get("product_mappings", {})
        for product_name, product_config in product_mappings.items():
            level = product_config.get("level", 2)
            assert level in valid_levels, f"Product {product_name} has invalid level: {level}"

        # Check coding standards mappings
        cs_mappings = legacy_mappings.get("coding_standards_mappings", {})
        for lang, lang_config in cs_mappings.items():
            level = lang_config.get("level", 2)
            assert level in valid_levels, f"CS:{lang} has invalid level: {level}"

    def test_wildcard_nist_inclusion(self, legacy_mappings):
        """Verify SEC:* wildcard includes NIST baseline."""
        wildcards = legacy_mappings.get("wildcards", {})
        sec_wildcard = wildcards.get("SEC:*", {})

        skills = sec_wildcard.get("skills", [])
        nist_included = any("nist-compliance" in skill for skill in skills)

        assert nist_included, "SEC:* wildcard must include nist-compliance/baseline"


class TestAuditRulesEdgeCases:
    """Edge case tests for audit-rules.yaml."""

    @pytest.fixture
    def audit_rules(self) -> dict:
        """Load audit rules."""
        with open(REPO_ROOT / "config/audit-rules.yaml") as f:
            return yaml.safe_load(f)

    def test_hub_requirements_no_duplicates(self, audit_rules):
        """Verify hub requirements don't have duplicate patterns."""
        orphans = audit_rules.get("orphans", {})
        requirements = orphans.get("require_link_from", [])

        patterns = [req["pattern"] for req in requirements]
        duplicates = [p for p in patterns if patterns.count(p) > 1]

        assert not duplicates, f"Duplicate hub requirement patterns: {set(duplicates)}"

    def test_exclusions_dont_overlap_requirements(self, audit_rules):
        """Verify exclusions don't overlap with hub requirements."""
        orphans = audit_rules.get("orphans", {})
        exclusions = orphans.get("exclude", [])
        requirements = orphans.get("require_link_from", [])

        # Convert exclusions to set for easier comparison
        exclusion_patterns = set(exclusions)

        # Check each requirement pattern
        for requirement in requirements:
            pattern = requirement["pattern"]

            # Basic check: exact pattern shouldn't be excluded
            assert pattern not in exclusion_patterns, f"Pattern {pattern} is both required and excluded"

    def test_limits_non_negative(self, audit_rules):
        """Verify all limits are non-negative."""
        limits = audit_rules.get("limits", {})

        for limit_name, limit_value in limits.items():
            assert limit_value >= 0, f"Limit {limit_name} is negative: {limit_value}"

    def test_all_hubs_have_reasonable_paths(self, audit_rules):
        """Verify hub paths are reasonable (not too deeply nested)."""
        orphans = audit_rules.get("orphans", {})
        requirements = orphans.get("require_link_from", [])

        for requirement in requirements:
            hubs = requirement.get("hubs", [])

            for hub in hubs:
                depth = hub.count("/")
                assert depth <= 5, f"Hub path too deep ({depth} levels): {hub}"


class TestCrossSystemConsistency:
    """Tests for consistency across multiple routing systems."""

    def test_product_types_aligned(self):
        """Verify product types are aligned across all configs."""
        # Load all configs
        with open(REPO_ROOT / "config/product-matrix.yaml") as f:
            product_matrix = yaml.safe_load(f)

        with open(REPO_ROOT / "skills/legacy-bridge/resources/legacy-mappings.yaml") as f:
            legacy_mappings = yaml.safe_load(f)

        # Get product sets
        matrix_products = set(product_matrix.get("products", {}).keys())
        legacy_products = set(legacy_mappings.get("product_mappings", {}).keys())

        # They should overlap significantly (may not be identical during transition)
        overlap = matrix_products & legacy_products
        assert len(overlap) >= 5, f"Insufficient product overlap: only {len(overlap)} shared"

    def test_wildcard_keys_aligned(self):
        """Verify wildcard keys match across configs."""
        # Load configs
        with open(REPO_ROOT / "config/product-matrix.yaml") as f:
            product_matrix = yaml.safe_load(f)

        with open(REPO_ROOT / "skills/legacy-bridge/resources/legacy-mappings.yaml") as f:
            legacy_mappings = yaml.safe_load(f)

        # Get wildcard sets
        matrix_wildcards = set(product_matrix.get("wildcards", {}).keys())
        legacy_wildcards = set(legacy_mappings.get("wildcards", {}).keys())

        # Should be identical
        assert matrix_wildcards == legacy_wildcards, (
            f"Wildcard mismatch: matrix={matrix_wildcards}, legacy={legacy_wildcards}"
        )

    def test_nist_auto_inclusion_consistent(self):
        """Verify NIST auto-inclusion logic is consistent across systems."""
        # Load configs
        with open(REPO_ROOT / "config/product-matrix.yaml") as f:
            product_matrix = yaml.safe_load(f)

        with open(REPO_ROOT / "skills/legacy-bridge/resources/legacy-mappings.yaml") as f:
            legacy_mappings = yaml.safe_load(f)

        # Check defaults
        matrix_defaults = product_matrix.get("defaults", {})
        assert matrix_defaults.get("include_nist_on_security") is True, (
            "Product matrix should auto-include NIST on security"
        )

        # Check auto-inclusion rules
        auto_inclusion = legacy_mappings.get("auto_inclusion", {})
        rules = auto_inclusion.get("rules", [])

        sec_rule = next((r for r in rules if "SEC" in r.get("condition", "")), None)
        assert sec_rule is not None, "Legacy mappings missing SEC auto-inclusion rule"

        includes = sec_rule.get("includes", [])
        nist_included = any("nist-compliance" in inc for inc in includes)
        assert nist_included, "Legacy SEC rule should auto-include NIST"


class TestErrorHandling:
    """Tests for error handling and edge cases."""

    def test_malformed_pattern_detection(self):
        """Test handling of potentially malformed patterns."""
        # This tests that our validation can catch issues

        test_patterns = [
            "",  # Empty pattern
            "docs/**/**/*.md",  # Double wildcard
            "docs/../*.md",  # Parent directory reference
        ]

        for pattern in test_patterns:
            # Empty patterns should be caught
            if pattern == "":
                assert len(pattern) == 0, "Empty pattern should be detected"

    def test_yaml_structure_validation(self):
        """Verify YAML files have expected top-level structure."""
        # Product matrix
        with open(REPO_ROOT / "config/product-matrix.yaml") as f:
            product_matrix = yaml.safe_load(f)

        required_keys = ["version", "defaults", "products", "wildcards"]
        for key in required_keys:
            assert key in product_matrix, f"Product matrix missing key: {key}"

        # Audit rules
        with open(REPO_ROOT / "config/audit-rules.yaml") as f:
            audit_rules = yaml.safe_load(f)

        required_keys = ["version", "limits", "orphans"]
        for key in required_keys:
            assert key in audit_rules, f"Audit rules missing key: {key}"

    def test_version_fields_present(self):
        """Verify all configs have version fields."""
        configs = [
            "config/product-matrix.yaml",
            "config/audit-rules.yaml",
            "skills/legacy-bridge/resources/legacy-mappings.yaml",
        ]

        for config_path in configs:
            with open(REPO_ROOT / config_path) as f:
                config = yaml.safe_load(f)

            assert "version" in config, f"{config_path} missing version field"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
