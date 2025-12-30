#!/usr/bin/env python3
"""
Validate Standards Schema Consistency

This script validates that standards referenced in various files exist in the schema.
It's used by the standards-validation.yml workflow.
"""

import json
import sys

import yaml


def main():
    # Load standards schema
    with open("config/standards-schema.yaml") as f:
        schema = yaml.safe_load(f)

    # Load API rules
    with open("config/standards-api.json") as f:
        rules = json.load(f)

    # Validate all rule standards exist in schema
    standard_ids = {std["id"] for std in schema["standards"].values()}

    errors = []
    for rule in rules["rules"]:
        std_ref = rule["standard"].split(":")[0]
        if std_ref not in standard_ids:
            errors.append(f"Rule {rule['id']} references unknown standard: {std_ref}")

    if errors:
        print("Validation errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("All standards references are valid")


if __name__ == "__main__":
    main()
