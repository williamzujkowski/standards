#\!/bin/bash
# Check for trailing whitespace in repository files

echo "Checking for trailing whitespace in markdown and YAML files..."

# Find files with trailing whitespace, excluding common directories
files_with_whitespace=$(find . -type f \( -name "*.md" -o -name "*.yml" -o -name "*.yaml" \) \
  -not -path "./.git/*" \
  -not -path "./node_modules/*" \
  -not -path "./standards/compliance/node_modules/*" \
  -not -path "./venv/*" \
  -not -path "./.venv/*" \
  -not -path "./dist/*" \
  -not -path "./build/*" \
  -exec grep -l '[[:space:]]$' {} \; 2>/dev/null)

if [ -n "$files_with_whitespace" ]; then
  echo "❌ Trailing whitespace found in the following files:"
  echo "$files_with_whitespace"
  echo ""
  echo "Total files with trailing whitespace: $(echo "$files_with_whitespace" | wc -l)"
  echo ""
  echo "To fix, run: find . -type f \\( -name \"*.md\" -o -name \"*.yml\" -o -name \"*.yaml\" \\) -not -path \"./.git/*\" -not -path \"./node_modules/*\" -not -path \"./standards/compliance/node_modules/*\" -exec sed -i 's/[[:space:]]*$//' {} \;"
  exit 1
else
  echo "✅ No trailing whitespace found in markdown or YAML files"
  exit 0
fi
