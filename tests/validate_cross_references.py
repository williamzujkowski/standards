#!/usr/bin/env python3
"""
Cross-Reference Validation Test Suite
Ensures all standards are properly cross-referenced according to KNOWLEDGE_MANAGEMENT_STANDARDS.md
"""

import os
import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class ValidationResult:
    """Stores validation test results"""
    passed: bool
    message: str
    details: List[str] = None


class StandardsValidator:
    """Validates cross-references and completeness of standards documentation"""
    
    def __init__(self, root_path: str = "."):
        self.root = Path(root_path)
        self.standards_files = self._find_standards_files()
        self.errors = []
        self.warnings = []
        
    def _find_standards_files(self) -> List[Path]:
        """Find all standards markdown files"""
        patterns = ["*_STANDARDS.md", "UNIFIED_STANDARDS.md"]
        files = []
        for pattern in patterns:
            files.extend(self.root.glob(pattern))
        return sorted(files)
    
    def run_all_tests(self) -> Dict[str, ValidationResult]:
        """Run all validation tests"""
        results = {
            "manifest_completeness": self.test_manifest_completeness(),
            "claude_routing": self.test_claude_routing_coverage(),
            "bidirectional_links": self.test_bidirectional_links(),
            "metadata_consistency": self.test_metadata_consistency(),
            "required_sections": self.test_required_sections(),
            "version_info": self.test_version_information(),
            "cross_references": self.test_cross_references(),
            "index_coverage": self.test_index_coverage(),
            "graph_relationships": self.test_graph_relationships(),
            "readme_references": self.test_readme_references()
        }
        return results
    
    def test_manifest_completeness(self) -> ValidationResult:
        """Test: All standards have entries in MANIFEST.yaml"""
        manifest_path = self.root / "MANIFEST.yaml"
        if not manifest_path.exists():
            return ValidationResult(False, "MANIFEST.yaml not found")
        
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f)
        
        standards_in_manifest = set()
        for code, data in manifest.get('standards', {}).items():
            if 'full_name' in data:
                standards_in_manifest.add(data['full_name'])
            elif 'filename' in data:
                standards_in_manifest.add(data['filename'])
        
        missing = []
        for std_file in self.standards_files:
            if std_file.name not in standards_in_manifest:
                missing.append(std_file.name)
        
        if missing:
            return ValidationResult(
                False, 
                f"Missing {len(missing)} standards in MANIFEST.yaml",
                missing
            )
        return ValidationResult(True, "All standards present in MANIFEST.yaml")
    
    def test_claude_routing_coverage(self) -> ValidationResult:
        """Test: CLAUDE.md covers all major standard categories"""
        claude_path = self.root / "CLAUDE.md"
        if not claude_path.exists():
            return ValidationResult(False, "CLAUDE.md not found")
        
        with open(claude_path) as f:
            claude_content = f.read()
        
        # Extract standard codes from natural language mappings
        codes_in_claude = set()
        code_pattern = r'`([A-Z]{2,7}):[^`]*`'
        for match in re.finditer(code_pattern, claude_content):
            codes_in_claude.add(match.group(1))
        
        # Check against MANIFEST.yaml codes
        manifest_path = self.root / "MANIFEST.yaml"
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f)
        
        manifest_codes = set(manifest.get('standards', {}).keys())
        missing_codes = manifest_codes - codes_in_claude
        
        if missing_codes:
            return ValidationResult(
                False,
                f"Missing {len(missing_codes)} standard codes in CLAUDE.md routing",
                list(missing_codes)
            )
        return ValidationResult(True, "All standard codes covered in CLAUDE.md")
    
    def test_bidirectional_links(self) -> ValidationResult:
        """Test: Cross-references are bidirectional"""
        link_pattern = r'\[([^\]]+)\]\(\.\/([^)]+\.md)(?:#[^)]+)?\)'
        unidirectional = []
        
        # Build link map - include all relevant files
        all_files = list(self.standards_files)
        # Add other important files that can have bidirectional links
        other_files = [
            "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "CLAUDE.md",
            "STANDARD_TEMPLATE.md", "CREATING_STANDARDS_GUIDE.md",
            "KICKSTART_PROMPT.md", "KICKSTART_ADVANCED.md"
        ]
        for fname in other_files:
            fpath = self.root / fname
            if fpath.exists():
                all_files.append(fpath)
        
        links = defaultdict(set)
        for std_file in all_files:
            with open(std_file) as f:
                content = f.read()
            
            for match in re.finditer(link_pattern, content):
                target = match.group(2)
                if target != std_file.name:
                    links[std_file.name].add(target)
        
        # Check bidirectionality
        for source, targets in links.items():
            for target in targets:
                if source not in links.get(target, set()):
                    unidirectional.append(f"{source} -> {target}")
        
        if unidirectional:
            return ValidationResult(
                False,
                f"Found {len(unidirectional)} unidirectional links",
                unidirectional[:10]  # Show first 10
            )
        return ValidationResult(True, "All cross-references are bidirectional")
    
    def test_metadata_consistency(self) -> ValidationResult:
        """Test: All standards have consistent metadata headers"""
        missing_metadata = []
        required_fields = ['Version:', 'Last Updated:', 'Status:']
        
        for std_file in self.standards_files:
            with open(std_file) as f:
                content = f.read()
            
            missing_fields = []
            for field in required_fields:
                if field not in content[:500]:  # Check header area
                    missing_fields.append(field)
            
            if missing_fields:
                missing_metadata.append(f"{std_file.name}: {', '.join(missing_fields)}")
        
        if missing_metadata:
            return ValidationResult(
                False,
                f"Found {len(missing_metadata)} files with missing metadata",
                missing_metadata
            )
        return ValidationResult(True, "All standards have consistent metadata")
    
    def test_required_sections(self) -> ValidationResult:
        """Test: Standards follow required structure from KNOWLEDGE_MANAGEMENT_STANDARDS.md"""
        required_sections = [
            "Table of Contents",
            "Overview",
            "Implementation"
        ]
        missing_sections = []
        
        for std_file in self.standards_files:
            with open(std_file) as f:
                content = f.read()
            
            missing = []
            for section in required_sections:
                if f"## {section}" not in content and f"# {section}" not in content:
                    missing.append(section)
            
            if missing:
                missing_sections.append(f"{std_file.name}: {', '.join(missing)}")
        
        if missing_sections:
            return ValidationResult(
                False,
                f"Found {len(missing_sections)} files missing required sections",
                missing_sections[:10]
            )
        return ValidationResult(True, "All standards follow required structure")
    
    def test_version_information(self) -> ValidationResult:
        """Test: Version numbers follow semantic versioning"""
        invalid_versions = []
        version_pattern = r'\*?\*?Version:\*?\*?\s*(\d+\.\d+\.\d+)'
        
        for std_file in self.standards_files:
            with open(std_file) as f:
                content = f.read()
            
            match = re.search(version_pattern, content)
            if not match:
                invalid_versions.append(f"{std_file.name}: No valid version found")
        
        if invalid_versions:
            return ValidationResult(
                False,
                f"Found {len(invalid_versions)} files with invalid versions",
                invalid_versions
            )
        return ValidationResult(True, "All version numbers are valid")
    
    def test_cross_references(self) -> ValidationResult:
        """Test: All file references point to existing files"""
        broken_links = []
        link_pattern = r'\[([^\]]+)\]\(\.\/([^)]+)\)'
        
        for std_file in self.standards_files:
            with open(std_file) as f:
                content = f.read()
            
            for match in re.finditer(link_pattern, content):
                target_path = match.group(2).split('#')[0]  # Remove anchors
                full_path = self.root / target_path
                
                if not full_path.exists():
                    broken_links.append(f"{std_file.name} -> {target_path}")
        
        if broken_links:
            return ValidationResult(
                False,
                f"Found {len(broken_links)} broken links",
                broken_links[:10]
            )
        return ValidationResult(True, "All cross-references are valid")
    
    def test_index_coverage(self) -> ValidationResult:
        """Test: STANDARDS_INDEX.md covers all standards"""
        index_path = self.root / "STANDARDS_INDEX.md"
        if not index_path.exists():
            return ValidationResult(False, "STANDARDS_INDEX.md not found")
        
        with open(index_path) as f:
            index_content = f.read()
        
        missing = []
        for std_file in self.standards_files:
            if std_file.name not in index_content:
                missing.append(std_file.name)
        
        if missing:
            return ValidationResult(
                False,
                f"Missing {len(missing)} standards in STANDARDS_INDEX.md",
                missing
            )
        return ValidationResult(True, "All standards indexed")
    
    def test_graph_relationships(self) -> ValidationResult:
        """Test: STANDARDS_GRAPH.md contains all key relationships"""
        graph_path = self.root / "STANDARDS_GRAPH.md"
        if not graph_path.exists():
            return ValidationResult(False, "STANDARDS_GRAPH.md not found")
        
        with open(graph_path) as f:
            graph_content = f.read()
        
        # Check for dependency definitions
        required_patterns = [
            "requires",
            "recommends",
            "enhances",
            "conflicts"
        ]
        
        missing = []
        for pattern in required_patterns:
            if pattern not in graph_content:
                missing.append(pattern)
        
        if missing:
            return ValidationResult(
                False,
                f"Missing relationship types in STANDARDS_GRAPH.md",
                missing
            )
        return ValidationResult(True, "All relationship types defined")
    
    def test_readme_references(self) -> ValidationResult:
        """Test: README.md references all major standards"""
        readme_path = self.root / "README.md"
        if not readme_path.exists():
            return ValidationResult(False, "README.md not found")
        
        with open(readme_path) as f:
            readme_content = f.read()
        
        # Major standards that should be in README
        major_standards = [
            "CODING_STANDARDS.md",
            "TESTING_STANDARDS.md",
            "MODERN_SECURITY_STANDARDS.md",
            "CLAUDE.md",
            "KNOWLEDGE_MANAGEMENT_STANDARDS.md"
        ]
        
        missing = []
        for std in major_standards:
            if std not in readme_content:
                missing.append(std)
        
        if missing:
            return ValidationResult(
                False,
                f"Missing {len(missing)} major standards in README.md",
                missing
            )
        return ValidationResult(True, "All major standards referenced in README")


def format_results(results: Dict[str, ValidationResult]) -> str:
    """Format test results for display"""
    output = ["=" * 60]
    output.append("KNOWLEDGE MANAGEMENT VALIDATION RESULTS")
    output.append("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results.items():
        status = "✓ PASS" if result.passed else "✗ FAIL"
        output.append(f"\n{status} - {test_name.replace('_', ' ').title()}")
        output.append(f"  {result.message}")
        
        if result.details and not result.passed:
            output.append("  Details:")
            for detail in result.details[:5]:  # Show first 5
                output.append(f"    - {detail}")
            if len(result.details) > 5:
                output.append(f"    ... and {len(result.details) - 5} more")
        
        if result.passed:
            passed += 1
        else:
            failed += 1
    
    output.append("\n" + "=" * 60)
    output.append(f"SUMMARY: {passed} passed, {failed} failed")
    output.append("=" * 60)
    
    return "\n".join(output)


if __name__ == "__main__":
    validator = StandardsValidator()
    results = validator.run_all_tests()
    print(format_results(results))
    
    # Exit with error code if any tests failed
    exit(0 if all(r.passed for r in results.values()) else 1)