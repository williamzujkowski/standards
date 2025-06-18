#!/bin/bash
# NIST 800-53r5 Control Tagging Pre-Commit Hook
#
# This hook validates NIST control tags and suggests missing ones
# for security-related code changes.

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Configuration
MIN_CONFIDENCE=0.7
SUGGEST_TAGS=${SUGGEST_TAGS:-true}
BLOCK_ON_MISSING=${BLOCK_ON_MISSING:-false}

echo "🔍 NIST 800-53r5 Compliance Check"
echo "================================="

# Function to check if file contains security patterns
contains_security_patterns() {
    local file=$1
    local patterns=(
        "auth.*\|login\|signin"
        "password\|credential\|secret"
        "encrypt\|decrypt\|crypto\|hash"
        "permission\|role\|access.*control\|rbac"
        "session\|token\|jwt\|cookie"
        "audit\|log.*security\|log.*event"
        "validate.*input\|sanitize\|escape"
        "tls\|ssl\|https\|certificate"
    )

    for pattern in "${patterns[@]}"; do
        if grep -i -q "$pattern" "$file" 2>/dev/null; then
            return 0
        fi
    done
    return 1
}

# Function to check if file has NIST tags
has_nist_tags() {
    local file=$1
    grep -q "@nist\s\+[a-z][a-z]-[0-9]" "$file" 2>/dev/null
}

# Function to suggest NIST controls based on content
suggest_nist_controls() {
    local file=$1
    local suggestions=""

    # Authentication patterns
    if grep -i -q "auth\|login\|signin" "$file" 2>/dev/null; then
        suggestions+="  - @nist ia-2 \"User authentication\"\n"
        suggestions+="  - @nist ia-8 \"System user identification\"\n"
    fi

    # Password patterns
    if grep -i -q "password\|credential" "$file" 2>/dev/null; then
        suggestions+="  - @nist ia-5 \"Authenticator management\"\n"
        suggestions+="  - @nist ia-5.1 \"Password-based authentication\"\n"
    fi

    # Encryption patterns
    if grep -i -q "encrypt\|decrypt\|crypto\|tls\|ssl" "$file" 2>/dev/null; then
        suggestions+="  - @nist sc-13 \"Cryptographic protection\"\n"
        suggestions+="  - @nist sc-8 \"Transmission confidentiality\"\n"
    fi

    # Access control patterns
    if grep -i -q "permission\|role\|rbac\|access.*control" "$file" 2>/dev/null; then
        suggestions+="  - @nist ac-3 \"Access enforcement\"\n"
        suggestions+="  - @nist ac-2 \"Account management\"\n"
        suggestions+="  - @nist ac-6 \"Least privilege\"\n"
    fi

    # Session patterns
    if grep -i -q "session\|timeout\|expire" "$file" 2>/dev/null; then
        suggestions+="  - @nist ac-12 \"Session termination\"\n"
        suggestions+="  - @nist ac-12.1 \"Session timeout\"\n"
    fi

    # Audit/logging patterns
    if grep -i -q "audit\|log.*security\|log.*event" "$file" 2>/dev/null; then
        suggestions+="  - @nist au-2 \"Audit events\"\n"
        suggestions+="  - @nist au-3 \"Content of audit records\"\n"
    fi

    # Input validation patterns
    if grep -i -q "validate.*input\|sanitize\|escape" "$file" 2>/dev/null; then
        suggestions+="  - @nist si-10 \"Information input validation\"\n"
        suggestions+="  - @nist si-11 \"Error handling\"\n"
    fi

    echo -e "$suggestions"
}

# Get staged files
staged_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(ts|js|py|go|java|rs|yaml|yml|json)$' || true)

if [ -z "$staged_files" ]; then
    echo "✅ No relevant files to check"
    exit 0
fi

# Track findings
warnings=0
errors=0
files_checked=0
files_with_security=0
files_missing_tags=0

# Check each staged file
for file in $staged_files; do
    if [ ! -f "$file" ]; then
        continue
    fi

    files_checked=$((files_checked + 1))

    # Check if file contains security patterns
    if contains_security_patterns "$file"; then
        files_with_security=$((files_with_security + 1))

        # Check if it has NIST tags
        if ! has_nist_tags "$file"; then
            files_missing_tags=$((files_missing_tags + 1))
            echo -e "\n${YELLOW}⚠️  Security code without NIST tags: $file${NC}"

            if [ "$SUGGEST_TAGS" = "true" ]; then
                echo -e "  Suggested NIST controls:"
                suggest_nist_controls "$file"
            fi

            warnings=$((warnings + 1))
        else
            echo -e "${GREEN}✓${NC} $file (has NIST tags)"
        fi
    fi
done

# Validate existing NIST tags format
echo -e "\n📋 Validating NIST tag format..."
for file in $staged_files; do
    if has_nist_tags "$file"; then
        # Check for invalid formats
        invalid_tags=$(grep -o "@nist\s\+[^[:space:]]*" "$file" | grep -v "@nist\s\+[a-z][a-z]-[0-9]" || true)

        if [ -n "$invalid_tags" ]; then
            echo -e "${RED}❌ Invalid NIST tag format in $file:${NC}"
            echo "$invalid_tags"
            echo "  Expected format: @nist xx-# where xx is lowercase family code"
            errors=$((errors + 1))
        fi
    fi
done

# Summary
echo -e "\n📊 Summary"
echo "=========="
echo "Files checked: $files_checked"
echo "Files with security code: $files_with_security"
echo "Files missing NIST tags: $files_missing_tags"
echo "Warnings: $warnings"
echo "Errors: $errors"

# Provide guidance
if [ $files_missing_tags -gt 0 ]; then
    echo -e "\n${YELLOW}💡 How to add NIST tags:${NC}"
    echo "  For functions/classes:"
    echo "    /**"
    echo "     * @nist ac-2 \"Account management\""
    echo "     * @nist ia-5 \"Authenticator management\""
    echo "     */"
    echo ""
    echo "  For inline code:"
    echo "    // @nist sc-13 \"Cryptographic protection\""
    echo ""
    echo "  See COMPLIANCE_STANDARDS.md for complete guidelines."
fi

# Determine exit status
if [ $errors -gt 0 ]; then
    echo -e "\n${RED}❌ Commit blocked due to NIST tag errors${NC}"
    exit 1
elif [ $warnings -gt 0 ] && [ "$BLOCK_ON_MISSING" = "true" ]; then
    echo -e "\n${RED}❌ Commit blocked: Security code requires NIST tags${NC}"
    echo "  Set BLOCK_ON_MISSING=false to allow commit with warnings"
    exit 1
elif [ $warnings -gt 0 ]; then
    echo -e "\n${YELLOW}⚠️  Proceeding with warnings${NC}"
    echo "  Consider adding NIST tags to security-related code"
    exit 0
else
    echo -e "\n${GREEN}✅ All NIST compliance checks passed${NC}"
    exit 0
fi
