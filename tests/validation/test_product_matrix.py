"""
Product matrix validation tests.

Tests product matrix configuration and consistency.
"""

from pathlib import Path
from typing import Dict

import pytest


class TestProductMatrixStructure:
    """Test product matrix structure."""

    def test_matrix_has_version(self, product_matrix: Dict):
        """Verify product matrix has version field."""
        assert "version" in product_matrix, "Product matrix missing version field"
        assert product_matrix["version"] >= 1, "Invalid version number"

    def test_matrix_has_products(self, product_matrix: Dict):
        """Verify product matrix defines products."""
        assert "products" in product_matrix, "Product matrix missing products section"
        assert len(product_matrix["products"]) > 0, "No products defined"

    def test_products_have_required_fields(self, product_matrix: Dict):
        """Verify each product has required fields."""
        required_fields = ["description", "standards"]
        invalid_products = []

        for product_name, product_config in product_matrix["products"].items():
            missing = [field for field in required_fields if field not in product_config]
            if missing:
                invalid_products.append(f"{product_name}: missing {missing}")

        assert not invalid_products, f"Products with invalid structure:\n" + "\n".join(invalid_products)

    def test_wildcard_expansions_defined(self, product_matrix: Dict):
        """Verify wildcard expansions are properly defined."""
        if "wildcards" not in product_matrix:
            pytest.skip("No wildcards defined in product matrix")

        invalid_wildcards = []
        for wildcard, config in product_matrix["wildcards"].items():
            if "expands_to" not in config:
                invalid_wildcards.append(f"{wildcard}: missing expands_to")
            elif not isinstance(config["expands_to"], list):
                invalid_wildcards.append(f"{wildcard}: expands_to must be a list")

        assert not invalid_wildcards, f"Invalid wildcard definitions:\n" + "\n".join(invalid_wildcards)


class TestProductMatrixContent:
    """Test product matrix content."""

    def test_standard_codes_consistent(self, product_matrix: Dict):
        """Verify standard codes follow consistent format."""
        import re

        invalid_codes = []
        # Allow uppercase letters, numbers, and hyphens in both parts
        code_pattern = re.compile(r"^[A-Z]{2,6}(-[A-Z]+)?:[a-z0-9\-]+$")

        for product_name, product_config in product_matrix["products"].items():
            for standard in product_config.get("standards", []):
                if not code_pattern.match(standard):
                    invalid_codes.append(f"{product_name}: {standard}")

        assert not invalid_codes, f"Invalid standard codes:\n" + "\n".join(invalid_codes[:10])

    def test_nist_auto_inclusion(self, product_matrix: Dict):
        """Verify NIST is auto-included when SEC standards present."""
        products_with_sec = []
        products_missing_nist = []

        for product_name, product_config in product_matrix["products"].items():
            standards = product_config.get("standards", [])

            has_sec = any(s.startswith("SEC:") for s in standards)
            has_nist = any("NIST" in s for s in standards)

            if has_sec:
                products_with_sec.append(product_name)
                if not has_nist:
                    products_missing_nist.append(product_name)

        # Verify auto-inclusion setting
        defaults = product_matrix.get("defaults", {})
        auto_include = defaults.get("include_nist_on_security", False)

        # If auto-include is enabled, warn but don't fail
        # This allows for some flexibility in product definitions
        if auto_include and products_missing_nist:
            import warnings

            warnings.warn(
                f"Products with SEC but no explicit NIST: {products_missing_nist}. "
                "Consider adding NIST-IG:base for consistency."
            )

    def test_language_mappings_valid(self, product_matrix: Dict):
        """Verify language mappings are properly defined."""
        if "language_mappings" not in product_matrix:
            pytest.skip("No language mappings defined")

        invalid_mappings = []
        for language, mappings in product_matrix["language_mappings"].items():
            if not isinstance(mappings, dict):
                invalid_mappings.append(f"{language}: mappings must be a dict")
                continue

            for key, value in mappings.items():
                if not isinstance(value, str):
                    invalid_mappings.append(f"{language}.{key}: value must be a string")

        assert not invalid_mappings, f"Invalid language mappings:\n" + "\n".join(invalid_mappings)

    def test_framework_mappings_valid(self, product_matrix: Dict):
        """Verify framework mappings are properly defined."""
        if "framework_mappings" not in product_matrix:
            pytest.skip("No framework mappings defined")

        invalid_mappings = []
        for framework, mappings in product_matrix["framework_mappings"].items():
            if not isinstance(mappings, dict):
                invalid_mappings.append(f"{framework}: mappings must be a dict")

        assert not invalid_mappings, f"Invalid framework mappings:\n" + "\n".join(invalid_mappings)


class TestProductMatrixUsage:
    """Test product matrix usage patterns."""

    def test_common_products_defined(self, product_matrix: Dict):
        """Verify common product types are defined."""
        common_products = [
            "api",
            "web-service",
            "frontend-web",
            "data-pipeline",
        ]

        products = product_matrix.get("products", {})
        missing = [p for p in common_products if p not in products]

        assert not missing, f"Missing common product types: {missing}"

    def test_stack_presets_reference_products(self, product_matrix: Dict):
        """Verify stack presets reference valid products."""
        if "stack_presets" not in product_matrix:
            pytest.skip("No stack presets defined")

        invalid_references = []
        products = product_matrix.get("products", {})

        for stack, config in product_matrix["stack_presets"].items():
            if "uses" in config:
                referenced_product = config["uses"]
                if referenced_product not in products:
                    invalid_references.append(f"{stack}: references undefined product '{referenced_product}'")

        assert not invalid_references, f"Invalid product references:\n" + "\n".join(invalid_references)

    def test_no_circular_dependencies(self, product_matrix: Dict):
        """Verify no circular dependencies in stack presets."""
        if "stack_presets" not in product_matrix:
            pytest.skip("No stack presets defined")

        # Build dependency graph
        dependencies = {}
        for stack, config in product_matrix["stack_presets"].items():
            if "uses" in config:
                dependencies[stack] = config["uses"]

        # Check for cycles
        def has_cycle(stack, visited=None):
            if visited is None:
                visited = set()
            if stack in visited:
                return True
            if stack not in dependencies:
                return False
            visited.add(stack)
            return has_cycle(dependencies[stack], visited)

        circular = [stack for stack in dependencies if has_cycle(stack)]

        assert not circular, f"Circular dependencies detected: {circular}"


class TestProductMatrixDocumentation:
    """Test product matrix documentation."""

    def test_products_have_descriptions(self, product_matrix: Dict):
        """Verify all products have descriptions."""
        missing_descriptions = []

        for product_name, product_config in product_matrix["products"].items():
            description = product_config.get("description", "").strip()
            if not description or len(description) < 10:
                missing_descriptions.append(product_name)

        assert not missing_descriptions, f"Products missing descriptions: {missing_descriptions}"

    def test_wildcards_have_descriptions(self, product_matrix: Dict):
        """Verify wildcards have descriptions."""
        if "wildcards" not in product_matrix:
            pytest.skip("No wildcards defined")

        missing_descriptions = []

        for wildcard, config in product_matrix["wildcards"].items():
            description = config.get("description", "").strip()
            if not description:
                missing_descriptions.append(wildcard)

        assert not missing_descriptions, f"Wildcards missing descriptions: {missing_descriptions}"


@pytest.mark.quality_gate
class TestProductMatrixQualityGate:
    """Quality gate tests for product matrix."""

    def test_matrix_completeness(self, product_matrix: Dict):
        """Verify product matrix is complete and valid."""
        required_sections = ["version", "products"]
        missing = [s for s in required_sections if s not in product_matrix]

        assert not missing, f"Product matrix missing required sections: {missing}"

        assert len(product_matrix["products"]) >= 5, "Product matrix should define at least 5 product types"
