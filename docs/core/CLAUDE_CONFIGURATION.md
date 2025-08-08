# Claude Configuration Guide

## Overview

This document outlines the Claude-related configuration files in the standards repository, explaining which files are essential for version control and which should remain local.

## Configuration Files

### 1. Files to Version Control (Committed)

#### `/CLAUDE.md` ✅ **REQUIRED**

- **Purpose**: Main Claude configuration with project-specific instructions
- **Location**: Repository root
- **Status**: Already in repository
- **Contents**:
  - Project context and instructions
  - Code style guidelines
  - Tool usage patterns
  - Project-specific rules

#### `/docs/core/CLAUDE.md` ✅ **REQUIRED**

- **Purpose**: Detailed Claude development instructions
- **Location**: docs/core/
- **Status**: Already in repository
- **Contents**:
  - SPARC methodology details
  - Agent coordination protocols
  - MCP tool guidelines
  - Development workflows

### 2. Files to Ignore (Local Only)

#### `.claude/settings.local.json` ❌ **DO NOT COMMIT**

- **Purpose**: Personal Claude settings
- **Location**: .claude/
- **Status**: Ignored in .gitignore
- **Contents**: User-specific preferences

#### `.mcp.json` ❌ **DO NOT COMMIT**

- **Purpose**: MCP server configuration
- **Location**: Repository root
- **Status**: Ignored in .gitignore
- **Contents**: Local MCP server settings

#### `claude-flow.config.json` ❌ **DO NOT COMMIT**

- **Purpose**: Claude Flow local configuration
- **Location**: Repository root
- **Status**: Ignored in .gitignore
- **Contents**: Personal Claude Flow settings

#### `.claude-flow/` ❌ **DO NOT COMMIT**

- **Purpose**: Claude Flow runtime data
- **Location**: Repository root
- **Status**: Ignored in .gitignore
- **Contents**: Temporary swarm data, agent states

### 3. Optional Configuration Files

#### `.roomodes` 🔄 **OPTIONAL**

- **Purpose**: Roo tool configuration (legacy)
- **Location**: Repository root
- **Status**: Can be removed if not using Roo
- **Recommendation**: Remove if not actively using Roo

#### `memory/` 🔄 **OPTIONAL**

- **Purpose**: Claude Flow memory persistence
- **Location**: Repository root
- **Status**: Data ignored, README files kept
- **Structure**:

  ```
  memory/
  ├── sessions/       # Ignored except README
  │   └── README.md   # Kept
  ├── agents/        # Ignored except README
  │   └── README.md   # Kept
  └── claude-flow-data.json  # Ignored
  ```

## Environment Variables

### Required Variables

None required for basic Claude operation.

### Optional Variables

```bash
# For AI features (optional)
OPENAI_API_KEY=your_key_here

# For GitHub integration (optional)
GITHUB_TOKEN=your_token_here

# For monitoring (optional)
MONITORING_ENABLED=true
LOG_LEVEL=INFO
```

## Setup Instructions

### 1. Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd standards

# Run development setup
./scripts/setup-development.sh

# Copy environment example
cp .env.example .env
# Edit .env with your values
```

### 2. Claude Flow Setup (Optional)

```bash
# Install Claude Flow MCP server
claude mcp add claude-flow npx claude-flow@alpha mcp start

# This creates local configuration files that are gitignored
```

### 3. Verify Configuration

```bash
# Check that Claude files are properly configured
ls -la CLAUDE.md docs/core/CLAUDE.md

# Verify gitignore is working
git status --ignored
```

## Best Practices

### DO ✅

- Keep project instructions in `/CLAUDE.md`
- Document project-specific Claude patterns
- Share useful Claude prompts and workflows
- Update CLAUDE.md when project structure changes

### DON'T ❌

- Commit personal Claude settings
- Share API keys or tokens
- Commit Claude Flow runtime data
- Track memory/session files

## Troubleshooting

### Issue: Claude not following project rules

**Solution**: Ensure `/CLAUDE.md` is up-to-date and comprehensive

### Issue: Claude Flow data committed accidentally

**Solution**:

```bash
git rm -r --cached .claude-flow/
git rm -r --cached memory/claude-flow-data.json
git commit -m "Remove Claude Flow runtime data"
```

### Issue: Settings not persisting

**Solution**: Check that `.claude/settings.local.json` exists locally (not committed)

## Migration Guide

If upgrading from older Claude setup:

1. **Remove old files**:

   ```bash
   rm -rf .roo/ .roomodes  # If not using Roo
   rm update_script_paths.py  # One-time migration script
   ```

2. **Update .gitignore**:
   - Ensure latest .gitignore patterns are applied
   - Run: `git add .gitignore && git commit -m "Update .gitignore for Claude"`

3. **Verify clean status**:

   ```bash
   git status --ignored
   # Should show ignored Claude files
   ```

## Summary

- **Version Control**: Only `/CLAUDE.md` and `/docs/core/CLAUDE.md`
- **Local Only**: All `.claude*`, `.mcp.json`, memory data
- **Optional**: Remove Roo files if not using that tool
- **Security**: Never commit API keys or tokens
