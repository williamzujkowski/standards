#!/bin/bash
# Script to check for trailing whitespace without modifying files
# Used for CI/CD validation

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to check for trailing whitespace in a file
check_file() {
    local file="$1"
    if [[ -f "$file" ]]; then
        if grep -q '[[:space:]]$' "$file"; then
            echo -e "${RED}Found trailing whitespace:${NC} $file"
            # Show lines with trailing whitespace
            grep -n '[[:space:]]$' "$file" | head -5
            return 1
        fi
    fi
    return 0
}

# Main execution
main() {
    local files_with_whitespace=0
    local files_checked=0
    local problematic_files=()

    echo -e "${GREEN}Checking for trailing whitespace...${NC}"

    # Define file extensions to check
    local extensions=("md" "yml" "yaml" "py" "sh" "json" "js" "ts" "tsx" "jsx" "txt" "rst" "toml" "cfg" "ini" "xml" "html" "css" "scss" "sass")

    # Check all files in the repository
    for ext in "${extensions[@]}"; do
        while IFS= read -r file; do
            ((files_checked++))
            if ! check_file "$file"; then
                ((files_with_whitespace++))
                problematic_files+=("$file")
            fi
        done < <(find . -name "*.${ext}" -type f -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./venv/*" -not -path "./.venv/*" -not -path "./vendor/*" 2>/dev/null || true)
    done

    # Summary
    echo -e "\n${GREEN}Summary:${NC}"
    echo -e "Files checked: $files_checked"
    echo -e "Files with trailing whitespace: $files_with_whitespace"

    if [[ $files_with_whitespace -gt 0 ]]; then
        echo -e "\n${RED}❌ Found trailing whitespace in $files_with_whitespace file(s)${NC}"
        echo -e "\n${YELLOW}Files with issues:${NC}"
        printf '%s\n' "${problematic_files[@]}"
        echo -e "\n${YELLOW}To fix these issues, run:${NC}"
        echo -e "  ./fix_trailing_whitespace.sh"
        exit 1
    else
        echo -e "\n${GREEN}✓ No trailing whitespace found${NC}"
        exit 0
    fi
}

# Run main function
main
