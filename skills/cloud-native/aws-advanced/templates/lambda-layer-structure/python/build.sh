#!/bin/bash
# Build Python Lambda Layer

set -e

echo "Building Python Lambda Layer..."

# Create directory structure
mkdir -p python/lib/python3.11/site-packages

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -t python/lib/python3.11/site-packages/

# Copy custom utilities
echo "Copying custom utilities..."
cp -r lib/* python/lib/

# Remove unnecessary files
echo "Cleaning up..."
find python -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find python -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
find python -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true

# Create zip file
echo "Creating layer package..."
zip -r layer.zip python/ -q

# Get zip size
SIZE=$(du -h layer.zip | cut -f1)
echo "Layer package created: layer.zip ($SIZE)"

# Publish to AWS (optional)
if [ "$1" == "--publish" ]; then
    echo "Publishing layer to AWS..."
    aws lambda publish-layer-version \
        --layer-name shared-python-dependencies \
        --description "Common Python dependencies and utilities" \
        --zip-file fileb://layer.zip \
        --compatible-runtimes python3.11 python3.12 \
        --compatible-architectures x86_64 arm64 \
        --license-info "MIT"
    echo "Layer published successfully!"
fi

echo "Done!"
