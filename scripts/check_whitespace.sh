#!/bin/bash
# Script to check for trailing whitespace without modifying files
# Used for CI/CD validation

set -uo pipefail

# Add error handler
trap 'echo "Error on line $LINENO: Command failed with exit code $?"' ERR

# Color codes for output (disable in CI)
if [[ -n "${CI:-}" ]] || [[ -n "${GITHUB_ACTIONS:-}" ]]; then
    RED=''
    GREEN=''
    YELLOW=''
    NC=''
else
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    NC='\033[0m' # No Color
fi

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

    # Debug info in CI
    if [[ -n "${CI:-}" ]] || [[ -n "${GITHUB_ACTIONS:-}" ]]; then
        echo "Running in CI/GitHub Actions environment"
        echo "Current directory: $(pwd)"
        echo "Script location: $0"
    fi

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

    # Debug output for CI
    if [[ -n "${CI:-}" ]] || [[ -n "${GITHUB_ACTIONS:-}" ]]; then
        if [[ $files_checked -eq 0 ]]; then
            echo "WARNING: No files were checked. This might indicate an issue with the find command."
            echo "Trying alternative check..."
            # Run a simple grep to see if there are files with trailing whitespace
            if grep -r '[[:space:]]$' --include="*.md" --include="*.yml" --include="*.yaml" . 2>/dev/null; then
                echo "Found files with trailing whitespace using grep"
                exit 1
            fi
        fi
    fi

    if [[ $files_with_whitespace -gt 0 ]]; then
        echo -e "\n${RED}❌ Found trailing whitespace in $files_with_whitespace file(s)${NC}"
        echo -e "\n${YELLOW}Files with issues:${NC}"
        printf '%s\n' "${problematic_files[@]}"
        echo -e "\n${YELLOW}To fix these issues, run:${NC}"
        echo -e "  ./scripts/fix_trailing_whitespace.sh"
        exit 1
    else
        echo -e "\n${GREEN}✓ No trailing whitespace found${NC}"
        exit 0
    fi
}

# Run main function
main
