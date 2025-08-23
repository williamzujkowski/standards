#!/usr/bin/env python3
"""
Inject cross-references to UNIFIED_STANDARDS.md in all standards documents.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

# List of files that need UNIFIED_STANDARDS cross-reference
TARGETS = [
    'standards/compliance/ANNOTATION_FRAMEWORK.md',
    'standards/compliance/IMPLEMENTATION_SUMMARY.md',
    'docs/standards/EVENT_DRIVEN_STANDARDS.md',
    'docs/standards/OBSERVABILITY_STANDARDS.md',
    'docs/standards/FRONTEND_MOBILE_STANDARDS.md',
    'docs/standards/KNOWLEDGE_MANAGEMENT_STANDARDS.md',
    'docs/standards/WEB_DESIGN_UX_STANDARDS.md',
    'docs/standards/PROJECT_MANAGEMENT_STANDARDS.md',
    'docs/standards/COST_OPTIMIZATION_STANDARDS.md',
    'docs/standards/TESTING_STANDARDS.md',
    'docs/standards/DATABASE_STANDARDS.md',
    'docs/standards/SEO_WEB_MARKETING_STANDARDS.md',
    'docs/standards/TOOLCHAIN_STANDARDS.md',
    'docs/standards/MICROSERVICES_STANDARDS.md',
    'docs/standards/ML_AI_STANDARDS.md',
    'docs/standards/MODERN_SECURITY_STANDARDS.md',
    'docs/standards/CLOUD_NATIVE_STANDARDS.md',
    'docs/standards/MODEL_CONTEXT_PROTOCOL_STANDARDS.md',
    'docs/standards/DATA_ENGINEERING_STANDARDS.md',
    'docs/standards/CONTENT_STANDARDS.md',
    'docs/standards/LEGAL_COMPLIANCE_STANDARDS.md',
    'docs/standards/CODING_STANDARDS.md',
    'docs/standards/GITHUB_PLATFORM_STANDARDS.md',
    'docs/standards/DEVOPS_PLATFORM_STANDARDS.md',
]

def compute_relative_path(from_file: Path, to_file: Path) -> str:
    """Compute relative path from one file to another."""
    # Get the directory of the from_file
    from_dir = from_file.parent
    
    # For files in standards/compliance/
    if 'standards/compliance' in str(from_dir):
        return '../../docs/standards/UNIFIED_STANDARDS.md'
    
    # For files in docs/standards/
    if 'docs/standards' in str(from_dir):
        return './UNIFIED_STANDARDS.md'
    
    return './UNIFIED_STANDARDS.md'

def inject_crossref(filepath: Path) -> bool:
    """Inject cross-reference after the first heading."""
    if not filepath.exists():
        print(f"  ⚠️  File not found: {filepath}")
        return False
    
    try:
        content = filepath.read_text(encoding='utf-8')
        lines = content.splitlines()
        
        # Check if cross-ref already exists
        if 'UNIFIED_STANDARDS' in content:
            print(f"  ✓ Already has reference: {filepath.name}")
            return False
        
        # Find the first heading (line starting with #)
        insert_pos = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('#'):
                # Insert after the heading and any immediate metadata
                insert_pos = i + 1
                # Skip version/date metadata if present
                while insert_pos < len(lines) and lines[insert_pos].strip().startswith('**'):
                    insert_pos += 1
                break
        
        if insert_pos == -1:
            insert_pos = 0
        
        # Compute relative path
        rel_path = compute_relative_path(filepath, ROOT / 'docs/standards/UNIFIED_STANDARDS.md')
        
        # Create cross-reference line
        crossref = f"\n> 📚 See also: [Unified Software Development Standards]({rel_path})\n"
        
        # Insert the cross-reference
        lines.insert(insert_pos, crossref)
        
        # Write back
        filepath.write_text('\n'.join(lines), encoding='utf-8')
        print(f"  ✅ Added cross-reference: {filepath.name}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing {filepath}: {e}")
        return False

def main():
    """Add cross-references to all target files."""
    print("📝 Injecting UNIFIED_STANDARDS cross-references...")
    print(f"  Processing {len(TARGETS)} files...")
    
    added = 0
    for target in TARGETS:
        filepath = ROOT / target
        if inject_crossref(filepath):
            added += 1
    
    print(f"\n✅ Added {added} cross-references")
    return 0

if __name__ == '__main__':
    sys.exit(main())