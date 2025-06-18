#!/bin/bash
# Setup NIST compliance git hooks

set -e

REPO_ROOT=$(git rev-parse --show-toplevel)
HOOKS_DIR="$REPO_ROOT/.git/hooks"
SCRIPTS_DIR="$REPO_ROOT/scripts"

echo "🔧 Setting up NIST compliance git hooks..."

# Create hooks directory if it doesn't exist
mkdir -p "$HOOKS_DIR"

# Install pre-commit hook
echo "Installing pre-commit hook..."
cat > "$HOOKS_DIR/pre-commit" << 'EOF'
#!/bin/bash
# NIST compliance pre-commit hook

# Run the NIST validation script
if [ -f "$REPO_ROOT/scripts/nist-pre-commit.sh" ]; then
    "$REPO_ROOT/scripts/nist-pre-commit.sh"
else
    echo "⚠️  NIST pre-commit script not found"
    exit 0
fi
EOF

# Replace $REPO_ROOT with actual path
sed -i "s|\$REPO_ROOT|$REPO_ROOT|g" "$HOOKS_DIR/pre-commit"

# Make hook executable
chmod +x "$HOOKS_DIR/pre-commit"

# Setup commit message template
echo "Setting up commit message template..."
git config --local commit.template .gitmessage

# Install optional prepare-commit-msg hook
cat > "$HOOKS_DIR/prepare-commit-msg" << 'EOF'
#!/bin/bash
# Add NIST control hints to commit message

COMMIT_MSG_FILE=$1
COMMIT_SOURCE=$2

# Only add hints for new commits (not amends, merges, etc.)
if [ -z "$COMMIT_SOURCE" ]; then
    # Check if any staged files have NIST tags
    nist_controls=$(git diff --cached | grep "@nist" | grep -o "@nist [a-z][a-z]-[0-9]\+" | sed 's/@nist //' | sort -u | tr '\n' ', ' | sed 's/,$//')

    if [ -n "$nist_controls" ]; then
        # Add NIST controls to commit message
        echo "" >> "$COMMIT_MSG_FILE"
        echo "# NIST Controls in this commit: $nist_controls" >> "$COMMIT_MSG_FILE"
    fi
fi
EOF

chmod +x "$HOOKS_DIR/prepare-commit-msg"

echo "✅ NIST compliance hooks installed successfully!"
echo ""
echo "Configuration options:"
echo "  - To make warnings block commits: export BLOCK_ON_MISSING=true"
echo "  - To disable tag suggestions: export SUGGEST_TAGS=false"
echo ""
echo "To uninstall hooks, run:"
echo "  rm $HOOKS_DIR/pre-commit $HOOKS_DIR/prepare-commit-msg"
echo "  git config --local --unset commit.template"
