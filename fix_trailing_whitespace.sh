#!/bin/bash
# Script to remove trailing whitespace from all text files
# Supports both standalone execution and pre-commit hook usage

set -euo pipefail

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Determine if running as pre-commit hook
IS_PRE_COMMIT="false"
if [[ "${PRE_COMMIT:-}" == "1" ]] || [[ -n "${PRE_COMMIT_FROM_REF:-}" ]] || [[ -n "${PRE_COMMIT_TO_REF:-}" ]]; then
    IS_PRE_COMMIT="true"
fi

# Function to fix trailing whitespace in a file
fix_file() {
    local file="$1"
    if [[ -f "$file" ]]; then
        # Create a backup for comparison
        cp "$file" "${file}.bak"

        # Remove trailing whitespace
        sed -i 's/[[:space:]]*$//' "$file"

        # Check if file was modified
        if ! cmp -s "$file" "${file}.bak"; then
            echo -e "${YELLOW}Fixed:${NC} $file"
            rm "${file}.bak"
            return 1  # File was modified
        else
            rm "${file}.bak"
            return 0  # File was not modified
        fi
    fi
}

# Main execution
main() {
    local files_modified=0
    local files_checked=0

    echo -e "${GREEN}Checking for trailing whitespace...${NC}"

    # Define file extensions to check
    local extensions=("md" "yml" "yaml" "py" "sh" "json" "js" "ts" "tsx" "jsx" "txt" "rst" "toml" "cfg" "ini" "xml" "html" "css" "scss" "sass")

    # If running as pre-commit, only check staged files
    if [[ "$IS_PRE_COMMIT" == "true" ]]; then
        # Get list of staged files
        while IFS= read -r file; do
            ((files_checked++))
            if fix_file "$file"; then
                :  # File was not modified
            else
                ((files_modified++))
                # Re-stage the file if it was modified
                git add "$file"
            fi
        done < <(git diff --cached --name-only --diff-filter=ACM | grep -E "\.($(IFS='|'; echo "${extensions[*]}"))$" || true)
    else
        # Run on all files in the repository
        for ext in "${extensions[@]}"; do
            while IFS= read -r file; do
                ((files_checked++))
                if fix_file "$file"; then
                    :  # File was not modified
                else
                    ((files_modified++))
                fi
            done < <(find . -name "*.${ext}" -type f -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./venv/*" -not -path "./.venv/*" -not -path "./vendor/*" 2>/dev/null || true)
        done
    fi

    # Summary
    echo -e "\n${GREEN}Summary:${NC}"
    echo -e "Files checked: $files_checked"
    echo -e "Files fixed: $files_modified"

    if [[ $files_modified -gt 0 ]]; then
        echo -e "\n${GREEN}✓${NC} Trailing whitespace removed from $files_modified file(s)"
        if [[ "$IS_PRE_COMMIT" == "true" ]]; then
            echo -e "${YELLOW}Note:${NC} Modified files have been re-staged"
        fi
    else
        echo -e "\n${GREEN}✓${NC} No trailing whitespace found"
    fi

    # Exit with appropriate code for pre-commit
    if [[ "$IS_PRE_COMMIT" == "true" ]]; then
        exit 0  # Always exit 0 in pre-commit mode
    fi
}

# Run main function
main
