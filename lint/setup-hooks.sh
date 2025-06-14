#!/bin/bash
# Setup pre-commit hooks for the standards repository

set -euo pipefail

echo "Setting up pre-commit hooks for standards repository..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    echo "Installing pre-commit..."
    pip3 install --user pre-commit
    
    # Add to PATH if needed
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install Node.js dependencies for markdownlint
if command -v npm &> /dev/null; then
    echo "Installing Node.js dependencies..."
    npm install -g markdownlint-cli
else
    echo "Warning: npm not found. Markdownlint will be skipped."
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --user pyyaml

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

# Create secrets baseline if it doesn't exist
if [ ! -f .secrets.baseline ]; then
    echo "Creating secrets baseline..."
    detect-secrets scan > .secrets.baseline || true
fi

# Run hooks on all files to check current state
echo ""
echo "Running hooks on all files to check current compliance..."
echo "This may take a few minutes..."
pre-commit run --all-files || true

echo ""
echo "✓ Pre-commit hooks installed successfully!"
echo ""
echo "Hooks will now run automatically before each commit."
echo "To run manually: pre-commit run --all-files"
echo "To skip hooks: git commit --no-verify"
echo ""
echo "To update hooks: pre-commit autoupdate"