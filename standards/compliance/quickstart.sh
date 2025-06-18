#!/bin/bash

echo "🚀 NIST 800-53r5 OSCAL-Native Compliance Platform Quick Start"
echo "============================================================"
echo ""

# Check if OSCAL data exists
if [ ! -f "oscal/catalogs/nist-800-53r5-catalog.json" ]; then
    echo "📥 Fetching OSCAL data..."
    cd oscal && ./fetch-oscal-data.sh && cd ..
    echo ""
fi

echo "✅ OSCAL data ready!"
echo ""

echo "📊 Platform Features:"
echo "  • OSCAL-native architecture with official NIST data"
echo "  • AI-powered semantic analysis for control mapping"
echo "  • Automatic repository standard tagging"
echo "  • Evidence harvesting from code and configs"
echo "  • System Security Plan (SSP) generation"
echo "  • Continuous compliance monitoring"
echo ""

echo "🔧 Available Commands (when CLI is implemented):"
echo "  nist-ai auto-tag              - Tag repository standards with NIST controls"
echo "  nist-ai analyze               - Perform compliance analysis"
echo "  nist-ai oscal generate-ssp    - Generate System Security Plan"
echo "  nist-ai ask '<question>'      - Natural language compliance queries"
echo ""

echo "📁 Key Directories:"
echo "  oscal/catalogs/   - NIST 800-53r5 control catalog"
echo "  oscal/profiles/   - Security baselines (low/moderate/high)"
echo "  oscal/types/      - TypeScript interfaces"
echo "  semantic/         - Knowledge graph and mappings"
echo "  automation/       - Core analysis engines"
echo ""

echo "🎯 Next Steps:"
echo "  1. Review the OSCAL catalog: oscal/catalogs/nist-800-53r5-catalog.json"
echo "  2. Check the demo: npm run demo"
echo "  3. Explore the TypeScript interfaces in oscal/types/"
echo "  4. See README.md for full documentation"
echo ""

echo "Phase 1 Complete ✅ - Foundation ready for SSP generation and CLI development!"
