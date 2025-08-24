#!/bin/bash
# Check for trailing whitespace in all text files

set -e

echo "Checking for trailing whitespace..."

# Find files with trailing whitespace
files_with_whitespace=$(find . -type f \
  -not -path "./.git/*" \
  -not -path "./node_modules/*" \
  -not -path "./__pycache__/*" \
  -not -path "./.venv/*" \
  -not -path "./venv/*" \
  -not -path "./.claude-flow/*" \
  -not -path "./reports/generated/*" \
  -not -path "./.hive-mind/*" \
  -not -path "./.ruff_cache/*" \
  -not -name "*.pyc" \
  -not -name "*.pyo" \
  -not -name "*.png" \
  -not -name "*.jpg" \
  -not -name "*.jpeg" \
  -not -name "*.gif" \
  -not -name "*.ico" \
  -not -name "*.svg" \
  -not -name "*.pdf" \
  -not -name "*.woff" \
  -not -name "*.woff2" \
  -not -name "*.ttf" \
  -not -name "*.otf" \
  -not -name "*.eot" \
  -not -name "*.min.js" \
  -not -name "*.min.css" \
  -exec grep -l '[[:space:]]$' {} + 2>/dev/null || true)

if [ -n "$files_with_whitespace" ]; then
  echo "❌ Files with trailing whitespace found:"
  echo "$files_with_whitespace"
  echo ""
  echo "Please remove trailing whitespace from these files."
  echo "You can use: sed -i 's/[[:space:]]*$//' <filename>"
  exit 1
else
  echo "✅ No trailing whitespace found"
  exit 0
fi
