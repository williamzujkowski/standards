#!/usr/bin/env python3
"""
Calculate Standards Compliance Score

This script calculates the compliance score based on rules in standards-api.json.
It's used by the standards-validation.yml workflow.
"""

import json
import os


def main():
    # Check if we're in the right directory
    if os.path.exists('standards-api.json'):
        api_file = 'standards-api.json'
    elif os.path.exists('config/standards-api.json'):
        api_file = 'config/standards-api.json'
    else:
        print("Error: Cannot find standards-api.json")
        exit(1)

    with open(api_file, 'r') as f:
        rules = json.load(f)

    total_rules = len(rules['rules'])
    required_rules = len([r for r in rules['rules'] if r['severity'] == 'required'])

    score = (required_rules / total_rules) * 100 if total_rules > 0 else 0

    print(f'Compliance Score: {score:.1f}%')
    print(f'Total Rules: {total_rules}')
    print(f'Required Rules: {required_rules}')

    # Output for GitHub Actions using new format
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f'score={score:.1f}\n')
            f.write(f'total={total_rules}\n')
            f.write(f'required={required_rules}\n')


if __name__ == '__main__':
    main()
