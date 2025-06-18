#!/bin/bash

# Fetch official NIST 800-53r5 OSCAL catalog and profiles
# Source: https://github.com/usnistgov/oscal-content

echo "📥 Fetching official NIST OSCAL catalog and profiles..."

# Base URL for NIST OSCAL content
BASE_URL="https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json"

# Create directories if they don't exist
mkdir -p catalogs profiles

# Fetch NIST 800-53r5 catalog
echo "Downloading NIST 800-53r5 catalog..."
curl -s -o catalogs/nist-800-53r5-catalog.json \
  "${BASE_URL}/NIST_SP-800-53_rev5_catalog.json"

# Fetch baseline profiles
echo "Downloading baseline profiles..."

# Low baseline
curl -s -o profiles/low-baseline.json \
  "${BASE_URL}/NIST_SP-800-53_rev5_LOW-baseline_profile.json"

# Moderate baseline
curl -s -o profiles/moderate-baseline.json \
  "${BASE_URL}/NIST_SP-800-53_rev5_MODERATE-baseline_profile.json"

# High baseline
curl -s -o profiles/high-baseline.json \
  "${BASE_URL}/NIST_SP-800-53_rev5_HIGH-baseline_profile.json"

# Privacy baseline
curl -s -o profiles/privacy-baseline.json \
  "${BASE_URL}/NIST_SP-800-53_rev5_PRIVACY-baseline_profile.json"

echo "✅ OSCAL data download complete!"
echo ""
echo "Downloaded files:"
ls -la catalogs/*.json profiles/*.json
