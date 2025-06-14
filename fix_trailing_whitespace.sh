#!/bin/bash
# Script to remove trailing whitespace from all text files

echo "Fixing trailing whitespace in all files..."

# Fix trailing whitespace in markdown files
find . -name "*.md" -type f -not -path "./.git/*" -exec sed -i 's/[[:space:]]*$//' {} \;

# Fix trailing whitespace in YAML files
find . -name "*.yml" -o -name "*.yaml" -type f -not -path "./.git/*" -exec sed -i 's/[[:space:]]*$//' {} \;

# Fix trailing whitespace in Python files
find . -name "*.py" -type f -not -path "./.git/*" -exec sed -i 's/[[:space:]]*$//' {} \;

# Fix trailing whitespace in shell scripts
find . -name "*.sh" -type f -not -path "./.git/*" -exec sed -i 's/[[:space:]]*$//' {} \;

# Fix trailing whitespace in JSON files
find . -name "*.json" -type f -not -path "./.git/*" -exec sed -i 's/[[:space:]]*$//' {} \;

# Fix trailing whitespace in JavaScript files
find . -name "*.js" -type f -not -path "./.git/*" -exec sed -i 's/[[:space:]]*$//' {} \;

echo "✓ Trailing whitespace removed from all files"