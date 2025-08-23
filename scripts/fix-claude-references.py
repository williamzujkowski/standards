#!/usr/bin/env python3
"""
Fix references to CLAUDE.md - ensure they point to the right location.
Root CLAUDE.md is the router, docs/core/CLAUDE.md is legacy.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def fix_claude_refs():
    """Fix all references to CLAUDE.md to point correctly."""
    
    # Files that reference CLAUDE.md
    files_to_check = [
        'docs/nist/NIST_IMPLEMENTATION_GUIDE.md',
        'docs/guides/KICKSTART_PROMPT.md', 
        'docs/guides/CREATING_STANDARDS_GUIDE.md',
        'docs/standards/KNOWLEDGE_MANAGEMENT_STANDARDS.md',
        'README.md',
    ]
    
    for file_path in files_to_check:
        full_path = ROOT / file_path
        if not full_path.exists():
            continue
            
        content = full_path.read_text(encoding='utf-8')
        original = content
        
        # Fix references based on file location
        if 'docs/nist' in str(file_path):
            # From docs/nist -> ../../CLAUDE.md
            content = re.sub(r'\./docs/core/CLAUDE\.md', '../../CLAUDE.md', content)
            content = re.sub(r'docs/core/CLAUDE\.md', '../../CLAUDE.md', content)
            content = re.sub(r'\[CLAUDE\.md\]\(\.{0,2}/CLAUDE\.md\)', '[CLAUDE.md](../../CLAUDE.md)', content)
            
        elif 'docs/guides' in str(file_path):
            # From docs/guides -> ../../CLAUDE.md  
            content = re.sub(r'\./docs/core/CLAUDE\.md', '../../CLAUDE.md', content)
            content = re.sub(r'docs/core/CLAUDE\.md', '../../CLAUDE.md', content)
            
        elif 'docs/standards' in str(file_path):
            # From docs/standards -> ../../CLAUDE.md
            content = re.sub(r'\./docs/core/CLAUDE\.md', '../../CLAUDE.md', content)
            content = re.sub(r'docs/core/CLAUDE\.md', '../../CLAUDE.md', content)
            
        elif file_path == 'README.md':
            # From root -> ./CLAUDE.md
            content = re.sub(r'\./docs/core/CLAUDE\.md', './CLAUDE.md', content)
            content = re.sub(r'docs/core/CLAUDE\.md', 'CLAUDE.md', content)
        
        if content != original:
            full_path.write_text(content, encoding='utf-8')
            print(f"  ✅ Fixed CLAUDE.md references in {file_path}")

def main():
    print("🔧 Fixing CLAUDE.md references...")
    fix_claude_refs()
    print("✅ CLAUDE.md references fixed")

if __name__ == '__main__':
    main()