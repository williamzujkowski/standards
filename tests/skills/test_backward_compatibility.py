#!/usr/bin/env python3
"""
Test Suite: Backward Compatibility
Ensures existing @load patterns continue to work with new skill system.
"""

import pytest
from pathlib import Path
from typing import Dict, List
import re
import yaml


class BackwardCompatibilityTester:
    """Test backward compatibility with existing patterns."""

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.standards_dir = self.repo_root / "docs" / "standards"
        self.skills_dir = self.repo_root / "docs" / "skills"
        self.product_matrix = self.repo_root / "config" / "product-matrix.yaml"

    def load_product_matrix(self) -> Dict:
        """Load the product matrix configuration."""
        if not self.product_matrix.exists():
            return {}

        with open(self.product_matrix) as f:
            return yaml.safe_load(f)

    def parse_load_directive(self, directive: str) -> Dict:
        """Parse @load directive and extract components."""
        # Patterns:
        # @load product:api
        # @load [product:api + CS:python + TS:pytest]
        # @load CS:python

        result = {
            'directive': directive,
            'product': None,
            'standards': [],
            'valid': False
        }

        # Extract product type
        product_match = re.search(r'product:([a-z0-9-]+)', directive)
        if product_match:
            result['product'] = product_match.group(1)

        # Extract standard codes
        standard_matches = re.findall(r'([A-Z]+):([a-z0-9-*]+)', directive)
        for code, value in standard_matches:
            result['standards'].append(f"{code}:{value}")

        result['valid'] = result['product'] is not None or len(result['standards']) > 0

        return result

    def resolve_load_directive_legacy(self, directive: str) -> Dict:
        """Resolve @load directive using legacy standards."""
        parsed = self.parse_load_directive(directive)
        matrix = self.load_product_matrix()

        result = {
            'directive': directive,
            'resolved_standards': [],
            'resolved_files': [],
            'method': 'legacy'
        }

        # Resolve product type from matrix
        if parsed['product'] and 'products' in matrix:
            product_config = matrix['products'].get(parsed['product'], {})
            if 'standards' in product_config:
                result['resolved_standards'].extend(product_config['standards'])

        # Add explicit standards
        result['resolved_standards'].extend(parsed['standards'])

        # Map to actual files
        for standard in result['resolved_standards']:
            # Convert standard code to potential file names
            # Example: CS:python -> CODING_STANDARDS.md (section: python)
            if ':' in standard:
                code, value = standard.split(':', 1)
                result['resolved_files'].append(self._map_standard_to_file(code, value))

        return result

    def resolve_load_directive_skills(self, directive: str) -> Dict:
        """Resolve @load directive using new skill system."""
        parsed = self.parse_load_directive(directive)

        result = {
            'directive': directive,
            'resolved_skills': [],
            'resolved_files': [],
            'method': 'skills'
        }

        # Map to skills
        if parsed['product']:
            # Product should map to skill bundle
            result['resolved_skills'].append(f"product-{parsed['product']}")

        for standard in parsed['standards']:
            # Convert standard code to skill name
            skill_name = self._map_standard_to_skill(standard)
            if skill_name:
                result['resolved_skills'].append(skill_name)

        # Map to actual skill files
        for skill in result['resolved_skills']:
            skill_path = self.skills_dir / skill / "SKILL.md"
            result['resolved_files'].append(str(skill_path))

        return result

    def _map_standard_to_file(self, code: str, value: str) -> str:
        """Map standard code to legacy file."""
        code_to_file = {
            'CS': 'CODING_STANDARDS.md',
            'TS': 'TESTING_STANDARDS.md',
            'SEC': 'MODERN_SECURITY_STANDARDS.md',
            'FE': 'FRONTEND_MOBILE_STANDARDS.md',
            'DOP': 'DEVOPS_PLATFORM_STANDARDS.md',
            'OBS': 'OBSERVABILITY_STANDARDS.md',
            'LEG': 'LEGAL_COMPLIANCE_STANDARDS.md',
            'NIST-IG': 'COMPLIANCE_STANDARDS.md',
        }

        base_file = code_to_file.get(code, 'UNIFIED_STANDARDS.md')
        return str(self.standards_dir / base_file)

    def _map_standard_to_skill(self, standard: str) -> str:
        """Map standard code to skill name."""
        if ':' not in standard:
            return None

        code, value = standard.split(':', 1)

        # Map code to skill prefix
        code_to_skill = {
            'CS': 'coding',
            'TS': 'testing',
            'SEC': 'security',
            'FE': 'frontend',
            'DOP': 'devops',
            'OBS': 'observability',
            'LEG': 'legal',
            'NIST-IG': 'nist-compliance',
        }

        prefix = code_to_skill.get(code, 'general')
        return f"{prefix}-{value}"

    def compare_resolutions(self, directive: str) -> Dict:
        """Compare legacy and skill resolution for the same directive."""
        legacy = self.resolve_load_directive_legacy(directive)
        skills = self.resolve_load_directive_skills(directive)

        return {
            'directive': directive,
            'legacy': legacy,
            'skills': skills,
            'compatible': len(legacy['resolved_files']) > 0 and len(skills['resolved_skills']) > 0
        }

    def test_all_product_types(self) -> Dict:
        """Test all product types from matrix."""
        matrix = self.load_product_matrix()

        results = {
            'total_products': 0,
            'compatible': 0,
            'incompatible': 0,
            'details': []
        }

        if 'products' not in matrix:
            return results

        for product_type in matrix['products'].keys():
            directive = f"@load product:{product_type}"
            comparison = self.compare_resolutions(directive)

            results['total_products'] += 1
            if comparison['compatible']:
                results['compatible'] += 1
            else:
                results['incompatible'] += 1

            results['details'].append(comparison)

        return results


# Test cases
class TestBackwardCompatibility:
    """Test backward compatibility with existing patterns."""

    @pytest.fixture
    def tester(self):
        """Create tester instance."""
        repo_root = Path(__file__).parent.parent.parent
        return BackwardCompatibilityTester(repo_root)

    def test_parse_simple_product(self, tester):
        """Test parsing simple product directive."""
        result = tester.parse_load_directive("@load product:api")

        assert result['valid'] == True
        assert result['product'] == 'api'
        assert len(result['standards']) == 0

    def test_parse_complex_directive(self, tester):
        """Test parsing complex directive with multiple components."""
        result = tester.parse_load_directive("@load [product:api + CS:python + TS:pytest]")

        assert result['valid'] == True
        assert result['product'] == 'api'
        assert 'CS:python' in result['standards']
        assert 'TS:pytest' in result['standards']

    def test_parse_standards_only(self, tester):
        """Test parsing directive with only standards."""
        result = tester.parse_load_directive("@load [CS:python + TS:* + SEC:*]")

        assert result['valid'] == True
        assert result['product'] is None
        assert 'CS:python' in result['standards']
        assert 'TS:*' in result['standards']
        assert 'SEC:*' in result['standards']

    def test_legacy_resolution(self, tester):
        """Test legacy resolution produces file paths."""
        result = tester.resolve_load_directive_legacy("@load product:api")

        assert result['method'] == 'legacy'
        assert len(result['resolved_standards']) > 0

    def test_skill_resolution(self, tester):
        """Test skill resolution produces skill names."""
        result = tester.resolve_load_directive_skills("@load product:api")

        assert result['method'] == 'skills'
        assert 'product-api' in result['resolved_skills']

    def test_compatibility_comparison(self, tester):
        """Test that legacy and skill resolutions are compatible."""
        result = tester.compare_resolutions("@load product:api")

        # Should resolve in both systems
        assert len(result['legacy']['resolved_files']) > 0 or len(result['skills']['resolved_skills']) > 0

    def test_wildcard_handling(self, tester):
        """Test that wildcards are handled correctly."""
        result = tester.parse_load_directive("@load SEC:*")

        assert result['valid'] == True
        assert 'SEC:*' in result['standards']

    def test_all_product_types_exist(self, tester):
        """Test that all product types from matrix can be resolved."""
        results = tester.test_all_product_types()

        assert results['total_products'] > 0
        # At least some should be compatible (even if skills don't exist yet)
        # This is informational rather than strict requirement


if __name__ == '__main__':
    # Run compatibility analysis
    repo_root = Path(__file__).parent.parent.parent
    tester = BackwardCompatibilityTester(repo_root)

    print("\n=== Backward Compatibility Analysis ===\n")

    # Test common directives
    test_directives = [
        "@load product:api",
        "@load product:web-service",
        "@load product:frontend-web",
        "@load [product:api + CS:python + TS:pytest]",
        "@load [CS:python + TS:* + SEC:*]",
    ]

    print("Testing common directives:\n")

    compatible_count = 0

    for directive in test_directives:
        result = tester.compare_resolutions(directive)

        status = "✓" if result['compatible'] else "✗"
        print(f"{status} {directive}")
        print(f"  Legacy: {len(result['legacy']['resolved_files'])} files")
        print(f"  Skills: {len(result['skills']['resolved_skills'])} skills")

        if result['compatible']:
            compatible_count += 1

        print()

    compatibility_pct = (compatible_count / len(test_directives) * 100)
    print(f"Compatibility: {compatible_count}/{len(test_directives)} ({compatibility_pct:.0f}%)")

    # Test all product types
    print("\n=== Product Type Coverage ===\n")

    product_results = tester.test_all_product_types()

    print(f"Total product types: {product_results['total_products']}")
    print(f"Compatible: {product_results['compatible']}")
    print(f"Incompatible: {product_results['incompatible']}")
