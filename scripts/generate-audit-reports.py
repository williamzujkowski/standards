#!/usr/bin/env python3
"""
Generate link check and structure audit reports for the standards repository.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from urllib.parse import urlparse

def check_links_in_file(filepath: str) -> Tuple[List[str], List[str], List[str]]:
    """Extract and categorize links from a markdown file."""
    internal_links = []
    external_links = []
    broken_links = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all markdown links
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(link_pattern, content)
        
        for text, link in matches:
            # Skip anchors
            if link.startswith('#'):
                continue
            
            # Check if external
            if link.startswith(('http://', 'https://')):
                external_links.append((text, link))
            else:
                # Internal link
                internal_links.append((text, link))
                
                # Check if file exists
                if not link.startswith('mailto:'):
                    # Resolve relative path
                    base_dir = Path(filepath).parent
                    target_path = base_dir / link
                    
                    # Remove anchor if present
                    if '#' in str(target_path):
                        target_path = Path(str(target_path).split('#')[0])
                    
                    # Check existence
                    if not target_path.exists():
                        broken_links.append((text, link, filepath))
    
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    
    return internal_links, external_links, broken_links

def analyze_repository_structure() -> Dict:
    """Analyze the repository structure for issues."""
    issues = {
        'orphaned_files': [],
        'missing_cross_refs': [],
        'non_conforming_names': [],
        'duplicate_content': [],
        'missing_readmes': [],
        'structure_violations': []
    }
    
    # Expected structure
    expected_dirs = {
        'docs/standards': 'Standard documents',
        'docs/nist': 'NIST compliance docs',
        'docs/guides': 'Implementation guides',
        'examples': 'Example code',
        'scripts': 'Utility scripts',
        'prompts': 'LLM prompts',
        'config': 'Configuration files',
        'reports/generated': 'Generated reports'
    }
    
    # Check for expected directories
    for dir_path, description in expected_dirs.items():
        if not Path(dir_path).exists():
            issues['structure_violations'].append(f"Missing expected directory: {dir_path} ({description})")
    
    # Find all markdown files
    all_md_files = list(Path('.').glob('**/*.md'))
    
    # Check for orphaned files (not linked from anywhere)
    linked_files = set()
    for md_file in all_md_files:
        internal, _, _ = check_links_in_file(str(md_file))
        for _, link in internal:
            if not link.startswith('#'):
                linked_files.add(link)
    
    # Check each file
    for md_file in all_md_files:
        rel_path = str(md_file)
        
        # Skip generated files
        if 'reports/generated' in rel_path or 'node_modules' in rel_path:
            continue
        
        # Check if orphaned
        is_linked = False
        for linked in linked_files:
            if rel_path in linked or linked in rel_path:
                is_linked = True
                break
        
        if not is_linked and rel_path not in ['README.md', 'CHANGELOG.md', 'LICENSE.md']:
            issues['orphaned_files'].append(rel_path)
        
        # Check naming conventions
        filename = md_file.name
        if 'standards' in str(md_file.parent).lower():
            # Check if filename follows UPPERCASE_WITH_UNDERSCORES.md pattern
            name_without_ext = filename.replace('.md', '').replace('.MD', '')
            if name_without_ext != 'README':
                # Should be all uppercase with underscores
                if not name_without_ext.replace('_', '').isupper():
                    issues['non_conforming_names'].append(f"{rel_path} - Standards should be UPPERCASE_WITH_UNDERSCORES.md")
        
        # Check for missing cross-references to UNIFIED_STANDARDS
        if 'standards' in str(md_file.parent) and filename != 'UNIFIED_STANDARDS.md':
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'UNIFIED_STANDARDS' not in content and filename != 'README.md':
                    issues['missing_cross_refs'].append(f"{rel_path} - No reference to UNIFIED_STANDARDS.md")
    
    # Check for directories without README
    for dir_path in Path('.').glob('**/'):
        if dir_path.is_dir() and not (dir_path / 'README.md').exists():
            rel_dir = str(dir_path)
            if not any(skip in rel_dir for skip in ['.git', '__pycache__', 'node_modules', '.', 'reports/generated']):
                if rel_dir and rel_dir != '.':
                    issues['missing_readmes'].append(rel_dir)
    
    return issues

def generate_linkcheck_report() -> str:
    """Generate a link check report."""
    report = []
    report.append("# Link Check Report")
    report.append(f"\nGenerated: 2025-08-23\n")
    
    all_broken = []
    all_external = []
    file_count = 0
    
    # Check all markdown files
    for md_file in Path('.').glob('**/*.md'):
        # Skip generated reports and node_modules
        if 'reports/generated' in str(md_file) or 'node_modules' in str(md_file):
            continue
        
        file_count += 1
        internal, external, broken = check_links_in_file(str(md_file))
        
        if broken:
            all_broken.extend(broken)
        if external:
            all_external.extend([(str(md_file), text, link) for text, link in external])
    
    # Report broken links
    report.append(f"\n## Broken Internal Links ({len(all_broken)} found)\n")
    if all_broken:
        for text, link, source in all_broken:
            report.append(f"- **{source}**: [{text}]({link})")
    else:
        report.append("✅ No broken internal links found!")
    
    # Report external links
    report.append(f"\n## External Links ({len(all_external)} found)\n")
    if all_external:
        # Group by domain
        by_domain = {}
        for source, text, link in all_external:
            domain = urlparse(link).netloc
            if domain not in by_domain:
                by_domain[domain] = []
            by_domain[domain].append((source, text, link))
        
        for domain, links in sorted(by_domain.items()):
            report.append(f"\n### {domain} ({len(links)} links)")
            for source, text, link in links[:5]:  # Show first 5
                report.append(f"- {source}: [{text}]({link})")
            if len(links) > 5:
                report.append(f"- ... and {len(links) - 5} more")
    
    report.append(f"\n## Summary\n")
    report.append(f"- Files checked: {file_count}")
    report.append(f"- Broken links: {len(all_broken)}")
    report.append(f"- External links: {len(all_external)}")
    
    return '\n'.join(report)

def generate_structure_audit_report(issues: Dict) -> str:
    """Generate a structure audit report."""
    report = []
    report.append("# Structure Audit Report")
    report.append(f"\nGenerated: 2025-08-23\n")
    
    total_issues = sum(len(v) for v in issues.values())
    report.append(f"## Summary\n")
    report.append(f"Total issues found: {total_issues}\n")
    
    # Orphaned files
    report.append(f"\n## Orphaned Files ({len(issues['orphaned_files'])})\n")
    report.append("Files not linked from any other document:\n")
    if issues['orphaned_files']:
        for file in issues['orphaned_files']:
            report.append(f"- {file}")
    else:
        report.append("✅ No orphaned files found")
    
    # Missing cross-references
    report.append(f"\n## Missing Cross-References ({len(issues['missing_cross_refs'])})\n")
    report.append("Standards documents not referencing UNIFIED_STANDARDS.md:\n")
    if issues['missing_cross_refs']:
        for issue in issues['missing_cross_refs']:
            report.append(f"- {issue}")
    else:
        report.append("✅ All standards properly cross-referenced")
    
    # Non-conforming filenames
    report.append(f"\n## Non-Conforming Filenames ({len(issues['non_conforming_names'])})\n")
    if issues['non_conforming_names']:
        for issue in issues['non_conforming_names']:
            report.append(f"- {issue}")
    else:
        report.append("✅ All filenames follow conventions")
    
    # Missing READMEs
    report.append(f"\n## Directories Missing README ({len(issues['missing_readmes'])})\n")
    if issues['missing_readmes']:
        for dir_path in issues['missing_readmes']:
            report.append(f"- {dir_path}/")
    else:
        report.append("✅ All directories have README files")
    
    # Structure violations
    report.append(f"\n## Structure Violations ({len(issues['structure_violations'])})\n")
    if issues['structure_violations']:
        for violation in issues['structure_violations']:
            report.append(f"- {violation}")
    else:
        report.append("✅ Repository structure follows standards")
    
    # Recommendations
    report.append("\n## Recommendations\n")
    if total_issues > 0:
        report.append("1. **Fix broken links**: Update or remove broken internal links")
        report.append("2. **Link orphaned files**: Add references to orphaned documents")
        report.append("3. **Add cross-references**: Link standards to UNIFIED_STANDARDS.md")
        report.append("4. **Standardize names**: Rename files to follow conventions")
        report.append("5. **Add READMEs**: Create README.md for directories lacking them")
    else:
        report.append("✅ Repository structure is well-organized and compliant!")
    
    return '\n'.join(report)

def main():
    """Generate audit reports."""
    print("🔍 Generating audit reports...")
    
    # Ensure output directory exists
    output_dir = Path('reports/generated')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate link check report
    print("Checking links...")
    linkcheck_report = generate_linkcheck_report()
    linkcheck_path = output_dir / 'linkcheck.txt'
    with open(linkcheck_path, 'w', encoding='utf-8') as f:
        f.write(linkcheck_report)
    print(f"✅ Link check report: {linkcheck_path}")
    
    # Generate structure audit report
    print("Auditing structure...")
    issues = analyze_repository_structure()
    structure_report = generate_structure_audit_report(issues)
    structure_path = output_dir / 'structure-audit.md'
    with open(structure_path, 'w', encoding='utf-8') as f:
        f.write(structure_report)
    print(f"✅ Structure audit: {structure_path}")
    
    # Summary
    total_issues = sum(len(v) for v in issues.values())
    print(f"\n📊 Audit Summary:")
    print(f"  - Structure issues: {total_issues}")
    print(f"  - Reports generated in: {output_dir}/")

if __name__ == '__main__':
    main()