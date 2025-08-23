#!/usr/bin/env python3
"""
Generate Weekly Digest

This script generates a weekly digest of changes to standards documents.
It's used by the auto-summaries.yml workflow.
"""

import subprocess
import re
from datetime import datetime, timedelta


def get_recent_changes():
    # Get commits from last week
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    cmd = f"git log --since='{week_ago}' --pretty=format:'%h|%s|%an|%ad' --date=short"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    changes = []
    for line in result.stdout.strip().split('\n'):
        if line:
            parts = line.split('|')
            if len(parts) == 4:
                changes.append({
                    'hash': parts[0],
                    'message': parts[1],
                    'author': parts[2],
                    'date': parts[3]
                })
    return changes


def get_changed_files():
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    cmd = f"git diff --name-only HEAD@{{'{week_ago}'}} HEAD"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return [f for f in result.stdout.strip().split('\n') if f.endswith('.md')]


def generate_digest():
    digest = f"# Weekly Standards Digest\n"
    digest += f"**Week of:** {datetime.now().strftime('%Y-%m-%d')}\n\n"

    # Recent changes
    changes = get_recent_changes()
    if changes:
        digest += "## Recent Updates\n\n"
        for change in changes[:10]:  # Top 10 changes
            digest += f"- **{change['date']}** - {change['message']} ({change['hash']})\n"
        digest += "\n"

    # Changed files
    files = get_changed_files()
    if files:
        digest += "## Updated Standards\n\n"
        for file in sorted(files):
            if file != 'WEEKLY_DIGEST.md':
                digest += f"- {file}\n"
        digest += "\n"

    # Quick stats
    digest += "## Repository Stats\n\n"
    digest += f"- Total standards documents: 21\n"
    digest += f"- Total updates this week: {len(changes)}\n"
    digest += f"- Files changed: {len(files)}\n"

    with open('WEEKLY_DIGEST.md', 'w') as f:
        f.write(digest)


if __name__ == "__main__":
    generate_digest()
