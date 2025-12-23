#!/bin/bash
# sync-to-claude.sh - Make standards agents/skills auto-discoverable by Claude Code
#
# This script creates symlinks in ~/.claude/ pointing to the standards repo
# Run this once after cloning, or after adding new agents/skills
#
# Usage: ./scripts/sync-to-claude.sh [--uninstall]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
CLAUDE_DIR="$HOME/.claude"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }

# Uninstall mode
if [[ "$1" == "--uninstall" ]]; then
    echo "Removing standards symlinks from ~/.claude..."

    # Remove skill symlinks
    for link in "$CLAUDE_DIR/skills"/std-*; do
        if [[ -L "$link" ]]; then
            rm "$link"
            log_success "Removed $(basename "$link")"
        fi
    done

    # Remove agent symlinks
    for link in "$CLAUDE_DIR/agents"/std-*.md; do
        if [[ -L "$link" ]]; then
            rm "$link"
            log_success "Removed $(basename "$link")"
        fi
    done

    echo "Done! standards uninstalled from Claude."
    exit 0
fi

echo "Installing standards to Claude Code..."
echo "Repository: $REPO_ROOT"
echo ""

# Ensure Claude directories exist
mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents"

# === SKILLS ===
# Claude expects: ~/.claude/skills/<name>/SKILL.md
# We have: repo/skills/<category>/<name>/SKILL.md (nested structure)
# Solution: Find all SKILL.md files and symlink their parent directories

echo "Syncing skills..."
skill_count=0
while IFS= read -r skill_file; do
    skill_dir=$(dirname "$skill_file")
    skill_name=$(basename "$skill_dir")
    category=$(basename "$(dirname "$skill_dir")")

    # Use category-name format to avoid collisions
    target="$CLAUDE_DIR/skills/std-${category}-${skill_name}"

    if [[ -L "$target" ]]; then
        rm "$target"
    elif [[ -e "$target" ]]; then
        log_warn "Skipping $skill_name (non-symlink exists)"
        continue
    fi

    ln -s "$skill_dir" "$target"
    skill_count=$((skill_count + 1))
done < <(find "$REPO_ROOT/skills" -name "SKILL.md" -type f)
log_success "Linked $skill_count skills"

# === AGENTS ===
# Claude expects: ~/.claude/agents/<name>.md (single file with frontmatter)
# We have: repo/.claude/agents/<category>/<name>.md (nested structure)
# Solution: Find all .md files and symlink with std- prefix

echo "Syncing agents..."
agent_count=0
while IFS= read -r agent_file; do
    agent_name=$(basename "$agent_file" .md)

    # Skip README and other non-agent files
    if [[ "$agent_name" == "README" ]] || [[ "$agent_name" == "MIGRATION_SUMMARY" ]]; then
        continue
    fi

    target="$CLAUDE_DIR/agents/std-${agent_name}.md"

    if [[ -L "$target" ]]; then
        rm "$target"
    elif [[ -e "$target" ]]; then
        log_warn "Skipping $agent_name (non-symlink exists)"
        continue
    fi

    ln -s "$agent_file" "$target"
    agent_count=$((agent_count + 1))
done < <(find "$REPO_ROOT/.claude/agents" -name "*.md" -type f)
log_success "Linked $agent_count agents"

echo ""
echo "=== Installation Complete ==="
echo "Skills:  $skill_count linked to ~/.claude/skills/std-*"
echo "Agents:  $agent_count linked to ~/.claude/agents/std-*.md"
echo ""
echo "All standards items prefixed with 'std-' for easy identification."
echo ""
echo "Test with:"
echo "  ls ~/.claude/skills/std-* | head -5"
echo "  ls ~/.claude/agents/std-*.md | head -5"
echo ""
echo "To uninstall: $0 --uninstall"
