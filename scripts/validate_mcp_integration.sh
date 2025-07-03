#!/bin/bash
# Validate MCP standards integration

echo "🔍 Validating MCP Standards Integration..."
echo "========================================"

ERRORS=0

# Check if MCP standard file exists
if [ ! -f "docs/standards/MODEL_CONTEXT_PROTOCOL_STANDARDS.md" ]; then
    echo "❌ MCP standards file not found"
    ((ERRORS++))
else
    echo "✅ MCP standards file exists"
fi

# Check CLAUDE.md for MCP patterns
if grep -q "MCP:server" docs/core/CLAUDE.md; then
    echo "✅ MCP loading patterns found in CLAUDE.md"
else
    echo "❌ MCP loading patterns missing from CLAUDE.md"
    ((ERRORS++))
fi

# Check MANIFEST.yaml for MCP metadata
if grep -q "identifier: \"MCP\"" config/MANIFEST.yaml; then
    echo "✅ MCP metadata found in MANIFEST.yaml"
else
    echo "❌ MCP metadata missing from MANIFEST.yaml"
    ((ERRORS++))
fi

# Check STANDARDS_GRAPH.md for MCP dependencies
if grep -q "MCP:server → requires" docs/guides/STANDARDS_GRAPH.md; then
    echo "✅ MCP dependencies found in STANDARDS_GRAPH.md"
else
    echo "❌ MCP dependencies missing from STANDARDS_GRAPH.md"
    ((ERRORS++))
fi

# Check README.md for MCP reference
if grep -q "MODEL_CONTEXT_PROTOCOL_STANDARDS.md" README.md; then
    echo "✅ MCP reference found in README.md"
else
    echo "❌ MCP reference missing from README.md"
    ((ERRORS++))
fi

# Check standards count in README
if grep -q "24 documents" README.md; then
    echo "✅ Standards count updated to 24"
else
    echo "❌ Standards count not updated"
    ((ERRORS++))
fi

# Check MCP standard structure
if grep -q "## 🎯 Micro Summary" docs/standards/MODEL_CONTEXT_PROTOCOL_STANDARDS.md; then
    echo "✅ MCP micro summary present"
else
    echo "❌ MCP micro summary missing"
    ((ERRORS++))
fi

# Summary
echo ""
echo "========================================"
if [ $ERRORS -eq 0 ]; then
    echo "✅ All MCP integration checks passed!"
else
    echo "❌ Found $ERRORS errors in MCP integration"
    exit 1
fi