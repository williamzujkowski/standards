#!/usr/bin/env python3
"""
Validate Markdown Standards Links

This script checks that all markdown files referenced in CLAUDE.md exist.
It's used by the standards-validation.yml workflow.
"""

import re
import os
import sys


def main():
    errors = []

    with open('CLAUDE.md', 'r') as f:
        content = f.read()

    # Find all .md file references
    md_files = re.findall(r'`([A-Z_]+\.md)`', content)

    for md_file in md_files:
        if not os.path.exists(md_file):
            errors.append(f'Referenced file does not exist: {md_file}')

    if errors:
        print('Missing files:')
        for error in errors:
            print(f'  - {error}')
        sys.exit(1)
    else:
        print('All referenced markdown files exist')


if __name__ == '__main__':
    main()
