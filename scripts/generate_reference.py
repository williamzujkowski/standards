#!/usr/bin/env python3
"""
Generate Quick Reference JSON

This script generates a quick reference JSON file from standards documents.
It's used by the auto-summaries.yml workflow.
"""

import json
import yaml
import os
from datetime import datetime


def generate_reference():
    # Load index
    reference = {
        "version": "latest",
        "generated": datetime.now().isoformat(),
        "standards": {},
        "quick_answers": {}
    }

    # Parse STANDARDS_INDEX.md for quick lookups
    with open('docs/guides/STANDARDS_INDEX.md', 'r') as f:
        content = f.read()

    # Extract quick answers
    for line in content.split('\n'):
        if '|' in line and 'CS:' in line or 'SEC:' in line or 'TS:' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                code = parts[0].strip('`')
                if code and ':' in code:
                    reference['standards'][code] = {
                        'section': parts[1],
                        'summary': parts[2]
                    }

    # Add quick answers
    reference['quick_answers'] = {
        "python_naming": "snake_case for functions/variables, PascalCase for classes",
        "test_coverage": "85% overall, 95% critical paths, 90% new code",
        "api_versioning": "/api/v1/, /api/v2/ in URL path",
        "password_min": "12 characters minimum",
        "jwt_expiry": "1 hour for access tokens, 7 days for refresh"
    }

    with open('QUICK_REFERENCE.json', 'w') as f:
        json.dump(reference, f, indent=2)


if __name__ == "__main__":
    generate_reference()