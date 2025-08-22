#!/bin/bash
# check-claim-anchors.sh - Verify all claims in CLAIMS.md have specific anchors

set -e

CLAIMS_FILE="CLAIMS.md"
FAILED=0

# Check if CLAIMS.md exists
if [ ! -f "$CLAIMS_FILE" ]; then
    echo "ERROR: $CLAIMS_FILE not found"
    exit 1
fi

echo "Checking claim anchors in $CLAIMS_FILE..."

# Skip header lines, look for table rows with claims
# A proper anchor should contain: §, Section [0-9], p., Control ID pattern, or similar
while IFS='|' read -r _num claim _source section _status _rest; do
    # Skip empty lines and headers
    if [[ -z "$claim" ]] || [[ "$claim" == *"Claim"* ]] || [[ "$claim" == *"---"* ]] || [[ "$claim" == *"**"* ]]; then
        continue
    fi

    # Trim whitespace
    claim=$(echo "$claim" | xargs)
    section=$(echo "$section" | xargs)

    # Check if section contains specific anchor patterns
    if [[ -z "$section" ]]; then
        echo "ERROR: No section specified for claim: $claim"
        FAILED=1
    elif [[ "$section" == "UNKNOWN" ]]; then
        echo "WARNING: UNKNOWN anchor for claim: $claim"
        FAILED=1
    elif ! [[ "$section" =~ (§|Section\ [0-9]|p\.|[A-Z]{2}-[0-9]|[0-9]\.[0-9]|\#|Chapter|Appendix) ]]; then
        echo "WARNING: Vague anchor '$section' for claim: $claim"
        echo "  Consider adding specific section/page reference (§, p., #, etc.)"
    fi
done < "$CLAIMS_FILE"

if [ $FAILED -eq 0 ]; then
    echo "✓ All claims have proper anchors"
    exit 0
else
    echo "✗ Some claims lack specific anchors"
    exit 1
fi
