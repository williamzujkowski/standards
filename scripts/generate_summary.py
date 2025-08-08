#!/usr/bin/env python3
"""
Generate Standards Summary

This script generates a summary of all standards documents.
It's used by the auto-summaries.yml workflow.
"""

import os
import yaml
import re
from datetime import datetime


def extract_summary(file_path, max_lines=3):
    """Extract first few meaningful lines from a standard."""
    with open(file_path, 'r') as f:
        lines = f.readlines()

    summary_lines = []
    in_code_block = False

    for line in lines[2:]:  # Skip title and blank line
        line = line.strip()
        if line.startswith('```'):
            in_code_block = not in_code_block
            continue

        if not in_code_block and line and not line.startswith('#'):
            summary_lines.append(line)
            if len(summary_lines) >= max_lines:
                break

    return ' '.join(summary_lines)


def generate_summary():
    summary = f"# Standards Summary\n"
    summary += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"

    # Load manifest for structure
    with open('config/MANIFEST.yaml', 'r') as f:
        manifest = yaml.safe_load(f)

    for std_code, std_info in manifest['standards'].items():
        file_name = std_info['full_name']
        file_path = f"docs/standards/{file_name}"
        if os.path.exists(file_path):
            excerpt = extract_summary(file_path)
            summary += f"## {std_code} - {file_name}\n"
            summary += f"{excerpt}\n\n"

    with open('STANDARDS_SUMMARY.md', 'w') as f:
        f.write(summary)


if __name__ == "__main__":
    generate_summary()