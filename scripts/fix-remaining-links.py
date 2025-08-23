#!/usr/bin/env python3
"""
Fix remaining broken links in NIST docs and other files.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def fix_nist_links():
    """Fix broken links in NIST documentation."""
    
    # Fix NIST_IMPLEMENTATION_GUIDE.md
    nist_guide = ROOT / 'docs/nist/NIST_IMPLEMENTATION_GUIDE.md'
    if nist_guide.exists():
        content = nist_guide.read_text(encoding='utf-8')
        
        # Fix relative paths - these files are in docs/nist/
        content = re.sub(r'\.\.?/\.\.?/standards/COMPLIANCE_STANDARDS\.md', '../standards/COMPLIANCE_STANDARDS.md', content)
        content = re.sub(r'\.\.?/\.\.?/\.\.?/standards/compliance/README\.md', '../../standards/compliance/README.md', content)
        content = re.sub(r'\.\.?/\.\.?/standards/CODING_STANDARDS\.md', '../standards/CODING_STANDARDS.md', content)
        content = re.sub(r'\.\.?/\.\.?/standards/MODERN_SECURITY_STANDARDS\.md', '../standards/MODERN_SECURITY_STANDARDS.md', content)
        content = re.sub(r'\.\.?/\.\.?/standards/PROJECT_MANAGEMENT_STANDARDS\.md', '../standards/PROJECT_MANAGEMENT_STANDARDS.md', content)
        content = re.sub(r'\.\.?/\.\.?/standards/UNIFIED_STANDARDS\.md', '../standards/UNIFIED_STANDARDS.md', content)
        
        nist_guide.write_text(content, encoding='utf-8')
        print("  ✅ Fixed NIST_IMPLEMENTATION_GUIDE.md links")
    
    # Fix NIST_QUICK_REFERENCE.md
    nist_ref = ROOT / 'docs/nist/NIST_QUICK_REFERENCE.md'
    if nist_ref.exists():
        content = nist_ref.read_text(encoding='utf-8')
        
        content = re.sub(r'\.\.?/\.\.?/standards/COMPLIANCE_STANDARDS\.md', '../standards/COMPLIANCE_STANDARDS.md', content)
        content = re.sub(r'\.\.?/\.\.?/\.\.?/examples/nist-templates/', '../../examples/nist-templates/', content)
        
        nist_ref.write_text(content, encoding='utf-8')
        print("  ✅ Fixed NIST_QUICK_REFERENCE.md links")

def fix_readme_links():
    """Fix links in generated README files."""
    
    # Fix standards/README.md
    std_readme = ROOT / 'standards/README.md'
    if std_readme.exists():
        content = std_readme.read_text(encoding='utf-8')
        content = re.sub(r'docs/standards/UNIFIED_STANDARDS\.md', '../docs/standards/UNIFIED_STANDARDS.md', content)
        std_readme.write_text(content, encoding='utf-8')
        print("  ✅ Fixed standards/README.md")
    
    # Fix links in compliance subdirectory READMEs
    compliance_dirs = [
        'standards/compliance/oscal',
        'standards/compliance/examples',
        'standards/compliance/src',
        'standards/compliance/semantic',
        'standards/compliance/scripts',
        'standards/compliance/automation',
        'standards/compliance/oscal/catalogs',
        'standards/compliance/oscal/profiles',
        'standards/compliance/oscal/types',
        'standards/compliance/src/parsers',
    ]
    
    for dir_path in compliance_dirs:
        readme = ROOT / dir_path / 'README.md'
        if readme.exists():
            content = readme.read_text(encoding='utf-8')
            depth = len(Path(dir_path).parts)
            unified_path = '../' * depth + 'docs/standards/UNIFIED_STANDARDS.md'
            content = re.sub(r'\.\./+docs/standards/UNIFIED_STANDARDS\.md', unified_path, content)
            readme.write_text(content, encoding='utf-8')
            print(f"  ✅ Fixed {dir_path}/README.md")

def fix_other_links():
    """Fix remaining misc broken links."""
    
    # Fix CREATING_STANDARDS_GUIDE.md
    guide = ROOT / 'docs/guides/CREATING_STANDARDS_GUIDE.md'
    if guide.exists():
        content = guide.read_text(encoding='utf-8')
        content = re.sub(r'\.\.?/\.\.?/\.\.?/config/MANIFEST\.yaml', '../../config/MANIFEST.yaml', content)
        content = re.sub(r'\./docs/core/CONTRIBUTING\.md', '../core/CONTRIBUTING.md', content)
        content = re.sub(r'../../CONTRIBUTING\.md', '../core/CONTRIBUTING.md', content)
        guide.write_text(content, encoding='utf-8')
        print("  ✅ Fixed CREATING_STANDARDS_GUIDE.md")
    
    # Fix KNOWLEDGE_MANAGEMENT_STANDARDS.md  
    km = ROOT / 'docs/standards/KNOWLEDGE_MANAGEMENT_STANDARDS.md'
    if km.exists():
        content = km.read_text(encoding='utf-8')
        content = re.sub(r'\.\.?/\.\.?/\.\.?/config/MANIFEST\.yaml', '../../config/MANIFEST.yaml', content)
        km.write_text(content, encoding='utf-8')
        print("  ✅ Fixed KNOWLEDGE_MANAGEMENT_STANDARDS.md")
    
    # Fix TOOLCHAIN_STANDARDS.md
    tool = ROOT / 'docs/standards/TOOLCHAIN_STANDARDS.md'
    if tool.exists():
        content = tool.read_text(encoding='utf-8')
        content = re.sub(r'\.\.?/\.\.?/\.\.?/config/TOOLS_CATALOG\.yaml', '../../config/TOOLS_CATALOG.yaml', content)
        content = re.sub(r'\.\.?/\.\.?/\.\.?/examples/project-templates/', '../../examples/project-templates/', content)
        tool.write_text(content, encoding='utf-8')
        print("  ✅ Fixed TOOLCHAIN_STANDARDS.md")
    
    # Fix badges/README.md
    badges = ROOT / 'badges/README.md'
    if badges.exists():
        content = badges.read_text(encoding='utf-8')
        content = re.sub(r'\./docs/standards-compliance\.md', '../docs/standards-compliance.md', content)
        badges.write_text(content, encoding='utf-8')
        print("  ✅ Fixed badges/README.md")

def main():
    print("🔧 Fixing remaining broken links...")
    fix_nist_links()
    fix_readme_links()
    fix_other_links()
    print("✅ Remaining links fixed")

if __name__ == '__main__':
    main()