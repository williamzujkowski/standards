# Anthropic Compliance Fixer - User Guide

## Overview

The `fix-anthropic-compliance.py` script automatically fixes common compliance issues in SKILL.md files to meet Anthropic API requirements for custom knowledge integration.

**Location**: `/home/william/git/standards/scripts/fix-anthropic-compliance.py`

## What It Fixes

### 1. Missing YAML Frontmatter

**Problem**: Skills without `---` delimited frontmatter blocks
**Solution**: Creates proper YAML frontmatter with required fields

```yaml
---
name: skill-name
description: Auto-generated description
---
```

### 2. Malformed YAML Frontmatter

**Problem**: Frontmatter missing closing `---` delimiter
**Solution**: Automatically detects where YAML ends and Markdown begins

**Before**:
```
---
name: my-skill
description: Something
## Examples  ← Missing closing ---
```

**After**:
```yaml
---
name: my-skill
description: Something
---

## Examples
```

### 3. Missing `name` Field

**Problem**: Frontmatter lacks required `name` field
**Solution**: Derives name from directory path

- `skills/cloud-native/kubernetes/SKILL.md` → `name: kubernetes`
- `skills/testing/e2e-testing/SKILL.md` → `name: e2e-testing`

Ensures name is <64 characters (Anthropic API requirement).

### 4. Missing or Placeholder `description` Field

**Problem**: No description or contains "TODO"
**Solution**: Three-tier extraction strategy:

1. **Extract from Level 1 content**: Uses first meaningful paragraph from Quick Start section
2. **Extract from document**: Finds first non-template content line
3. **Generate contextual description**: Creates description based on skill category and path

**Examples**:

```yaml
# For skills/data-engineering/orchestration/SKILL.md
description: "Orchestration standards for data engineering in Data Engineering environments. Covers best practices, implementation patterns, and integration guidelines."

# For skills/testing/SKILL.md
description: "Testing standards and best practices for Testing. Includes implementation guidelines, common patterns, and testing strategies."
```

Ensures description is <1024 characters (Anthropic API requirement).

### 5. Token Count Overages (>5000 tokens)

**Problem**: Skill file exceeds 5000 token limit
**Solution**: Multi-strategy optimization:

1. **Move verbose examples**: Relocates detailed code examples from Level 2 to Level 3
2. **Condense whitespace**: Removes excessive blank lines
3. **Preserve all content**: Never deletes information, only reorganizes

**Example**:
```
Before: 5877 tokens (over limit)
After:  4821 tokens (under limit)

Changes:
- Moved 3 detailed code examples to Level 3: Additional Examples
- Condensed spacing between sections
- All content preserved in reorganized structure
```

## Usage

### Basic Commands

```bash
# Preview all changes (recommended first step)
python3 scripts/fix-anthropic-compliance.py --dry-run --all

# Fix a specific skill
python3 scripts/fix-anthropic-compliance.py --skill cloud-native/kubernetes

# Fix all non-compliant skills
python3 scripts/fix-anthropic-compliance.py --all

# Fix only frontmatter issues (skip token optimization)
python3 scripts/fix-anthropic-compliance.py --all --skip-token-optimization

# Verbose output for debugging
python3 scripts/fix-anthropic-compliance.py --dry-run --all --verbose
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--skill PATH` | Fix specific skill (path relative to `skills/`) |
| `--all` | Fix all non-compliant skills |
| `--dry-run` | Preview changes without modifying files |
| `--skip-token-optimization` | Only fix frontmatter, don't reorganize content |
| `--verbose` | Show detailed debug information |

## Safety Features

### Automatic Backups

Before modifying any file, the script:
1. Creates timestamped backup directory: `.backup/skill-fixes-YYYYMMDD-HHMMSS/`
2. Preserves original file with full directory structure
3. Maintains file permissions and metadata

**Restore from backup**:
```bash
cp .backup/skill-fixes-20251024-223000/skills/my-skill/SKILL.md skills/my-skill/SKILL.md
```

### Validation

- **YAML parsing**: Ensures frontmatter is valid YAML before writing
- **Field limits**: Enforces Anthropic API constraints (name <64, description <1024)
- **Token estimation**: Accurate token counting using 1 token ≈ 4 characters
- **Content preservation**: Never deletes content, only reorganizes

### Comprehensive Logging

All operations logged to: `reports/generated/skill-fixes.log`

**Log includes**:
- Timestamp for each operation
- Files processed and changes made
- Warnings for malformed frontmatter
- Token optimization details
- Error messages with context

## Output Examples

### Dry-Run Summary

```
================================================================================
SUMMARY REPORT
================================================================================

[DRY RUN MODE - No files were modified]

Total skills processed: 52
Skills that would be fixed: 43

Issues found:
  - Missing or placeholder 'description' field: 38
  - Token count exceeded (>5000): 5
  - Missing 'name' field: 3

Changes that would be made:
--------------------------------------------------------------------------------

skills/skill-loader/SKILL.md:
  - Added description: 'Skill-Loader standards and implementation best practices...'
  New frontmatter:
    name: skill-loader
    description: Skill-Loader standards and implementation best practices for software development.

skills/devops/ci-cd/SKILL.md:
  - Optimized content: 5877 → 4821 tokens
  New frontmatter:
    name: ci-cd
    description: CI/CD pipeline standards for GitHub Actions, GitLab CI, and deployment automation...

Example: First 3 files that would be fixed:
--------------------------------------------------------------------------------

1. skills/skill-loader/SKILL.md
   Issues: Missing or placeholder 'description' field

2. skills/data-engineering/orchestration/SKILL.md
   Issues: Missing or placeholder 'description' field

3. skills/devops/ci-cd/SKILL.md
   Issues: Token count exceeded (5877 > 5000)

Log file: /home/william/git/standards/reports/generated/skill-fixes.log

================================================================================
```

### Actual Execution Summary

```
Total skills processed: 43
Skills fixed: 43

Backups saved to: .backup/skill-fixes-20251024-223000/
Log file: reports/generated/skill-fixes.log
```

## Workflow Recommendations

### First-Time Use

1. **Dry-run preview**:
   ```bash
   python3 scripts/fix-anthropic-compliance.py --dry-run --all > /tmp/preview.txt
   ```

2. **Review changes**:
   ```bash
   less /tmp/preview.txt
   ```

3. **Fix a test skill** (verify quality):
   ```bash
   python3 scripts/fix-anthropic-compliance.py --skill skill-loader
   git diff skills/skill-loader/SKILL.md
   ```

4. **If satisfied, fix all**:
   ```bash
   python3 scripts/fix-anthropic-compliance.py --all
   ```

5. **Verify results**:
   ```bash
   python3 scripts/analyze-skills-compliance.py
   ```

### Incremental Fixes

**Fix only frontmatter issues first**:
```bash
python3 scripts/fix-anthropic-compliance.py --all --skip-token-optimization
```

**Then optimize tokens separately**:
```bash
# Review which skills need optimization
python3 scripts/fix-anthropic-compliance.py --dry-run --all | grep "Token count"

# Fix specific token-heavy skills
python3 scripts/fix-anthropic-compliance.py --skill devops/ci-cd
python3 scripts/fix-anthropic-compliance.py --skill ml-ai/mlops
```

### Quality Assurance

After running fixes:

1. **Check YAML validity**:
   ```bash
   find skills -name "SKILL.md" -exec python3 -c "import yaml; yaml.safe_load(open('{}').read().split('---')[1])" \;
   ```

2. **Verify token counts**:
   ```bash
   python3 scripts/token-counter.py
   ```

3. **Review generated descriptions**:
   ```bash
   grep -h "^description:" skills/*/SKILL.md skills/*/*/SKILL.md
   ```

4. **Test git diff** (before committing):
   ```bash
   git diff --stat
   git diff skills/*/SKILL.md | less
   ```

## Technical Details

### Token Estimation

**Algorithm**: `tokens ≈ characters / 4`

This approximation is based on:
- English text averages ~4-5 characters per token
- Code averages ~3-4 characters per token
- Weighted average: ~4 characters per token

**Accuracy**: ±10% variance from actual Anthropic tokenization

### YAML Frontmatter Parsing

**Handles**:
- Standard format: `---\n...\n---\n`
- Missing closing delimiter (auto-detects Markdown start)
- Malformed YAML (salvages key-value pairs)
- Empty frontmatter (creates new)

**Detection logic**:
1. Look for closing `---`
2. If missing, scan for first `#` header or ` ```` code block
3. Everything before = YAML, everything after = Markdown

### Description Generation

**Priority order**:
1. Extract from Level 1 Quick Start section
2. Extract from first meaningful paragraph
3. Generate from skill path context

**Filters out**:
- TODO markers
- Code blocks
- Markdown formatting
- Template boilerplate

## Troubleshooting

### Issue: "Failed to parse YAML frontmatter"

**Cause**: Malformed YAML syntax
**Solution**: Script attempts to salvage; check log for details

```bash
# Check what was extracted
tail -20 reports/generated/skill-fixes.log
```

### Issue: Token optimization insufficient

**Cause**: Content still over 5000 tokens after optimization
**Solution**: Manual review required

```bash
# Identify problem skills
python3 scripts/fix-anthropic-compliance.py --dry-run --all | grep "over limit"
```

**Manual fixes**:
- Move more examples to external files
- Split large sections into separate documents
- Link to external resources instead of embedding

### Issue: Generated description too generic

**Cause**: No extractable content in skill file
**Solution**: Manually edit description after auto-generation

```bash
# Fix the skill first
python3 scripts/fix-anthropic-compliance.py --skill my-skill

# Then manually improve description
vim skills/my-skill/SKILL.md
```

## Integration with CI/CD

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check if any SKILL.md files changed
changed_skills=$(git diff --cached --name-only | grep 'SKILL.md$')

if [ -n "$changed_skills" ]; then
    echo "Checking SKILL.md compliance..."
    python3 scripts/fix-anthropic-compliance.py --dry-run --all | grep -q "No issues found"
    if [ $? -ne 0 ]; then
        echo "❌ SKILL.md files have compliance issues. Run:"
        echo "   python3 scripts/fix-anthropic-compliance.py --all"
        exit 1
    fi
fi
```

### GitHub Actions

```yaml
# .github/workflows/skills-compliance.yml
name: Skills Compliance Check

on:
  pull_request:
    paths:
      - 'skills/**/SKILL.md'

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check compliance
        run: |
          python3 scripts/fix-anthropic-compliance.py --dry-run --all
          if grep -q "Skills that would be fixed: 0"; then
            echo "✅ All skills compliant"
          else
            echo "❌ Compliance issues found"
            exit 1
          fi
```

## See Also

- **Validation**: `scripts/analyze-skills-compliance.py` - Audit current compliance status
- **Token counting**: `scripts/token-counter.py` - Detailed token analysis
- **Skills catalog**: `docs/SKILLS_CATALOG.md` - Complete skills inventory
