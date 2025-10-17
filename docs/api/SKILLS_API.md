# Skills API Documentation

**Version**: 1.0.0
**Last Updated**: 2025-10-16
**API Type**: CLI, Programmatic, Configuration-based

---

## Table of Contents

1. [Overview](#overview)
2. [CLI API](#cli-api)
3. [Load Syntax](#load-syntax)
4. [Product Matrix API](#product-matrix-api)
5. [Skill Resolution](#skill-resolution)
6. [Progressive Loading](#progressive-loading)
7. [Validation API](#validation-api)
8. [Programmatic API](#programmatic-api)
9. [Configuration](#configuration)
10. [Examples](#examples)

---

## Overview

The Skills API provides multiple interfaces for loading, composing, and validating skills:

- **CLI**: Command-line tools for skill operations
- **Load Syntax**: `@load` directives for declarative loading
- **Configuration**: YAML-based product type mappings
- **Programmatic**: TypeScript/Python APIs for integration

---

## CLI API

### skill-loader

Main CLI tool for skill operations.

#### Synopsis

```bash
npm run skill-loader -- <command> [options]
```

#### Commands

##### `load`

Load one or more skills.

**Syntax:**

```bash
npm run skill-loader -- load <skill-spec> [options]
```

**Parameters:**

- `<skill-spec>`: Skill specifier (see [Load Syntax](#load-syntax))
- `--level <1|2|3>`: Load specific level (default: 1)
- `--output <file>`: Save output to file
- `--format <md|json|yaml>`: Output format (default: md)
- `--with-resources`: Include bundled resources

**Examples:**

```bash
# Load single skill
npm run skill-loader -- load skill:coding-standards

# Load multiple skills
npm run skill-loader -- load "skill:coding-standards + skill:testing"

# Load at specific level
npm run skill-loader -- load skill:coding-standards --level 2

# Load and save
npm run skill-loader -- load product:api --output .claude/skills.md
```

##### `recommend`

Analyze project and recommend skills.

**Syntax:**

```bash
npm run skill-loader -- recommend <project-path> [options]
```

**Parameters:**

- `<project-path>`: Path to project directory
- `--format <text|json>`: Output format (default: text)
- `--min-priority <low|medium|high|critical>`: Minimum priority filter

**Example:**

```bash
npm run skill-loader -- recommend ./my-project

# Output:
# 🔍 Analyzing project...
# 📂 Detected: REST API (Python/FastAPI)
#
# 📚 Recommended Skills:
#   - coding-standards (priority: high)
#   - security-practices (priority: critical)
#   - testing (priority: high)
#   - nist-compliance (priority: medium)
```

##### `compose`

Compose multiple skills into a bundle.

**Syntax:**

```bash
npm run skill-loader -- compose <skill1> <skill2> ... [options]
```

**Parameters:**

- `<skillN>`: Skill identifiers
- `--level <1|2|3>`: Level for all skills (default: 1)
- `--output <file>`: Output file (required)
- `--format <md|json>`: Output format (default: md)
- `--name <name>`: Bundle name

**Example:**

```bash
npm run skill-loader -- compose \
  skill:coding-standards \
  skill:security-practices \
  skill:testing \
  --level 1 \
  --output team-bundle.md \
  --name "Team Development Bundle"
```

##### `list`

List all available skills.

**Syntax:**

```bash
npm run skill-loader -- list [options]
```

**Parameters:**

- `--format <table|json|yaml>`: Output format (default: table)
- `--verbose`: Show detailed information

**Example:**

```bash
npm run skill-loader -- list --format table

# Output:
# Skill                 Description                              Level 1 Tokens
# ────────────────────────────────────────────────────────────────────────────
# coding-standards      Comprehensive coding standards...        336
# security-practices    Modern security standards...             409
# testing              Comprehensive testing standards...        430
# nist-compliance      NIST 800-53r5 control implementation...  580
# skill-loader         Meta-skill for loading skills...         328
```

##### `validate`

Validate skill structure and content.

**Syntax:**

```bash
npm run skill-loader -- validate <skill-path> [options]
```

**Parameters:**

- `<skill-path>`: Path to skill directory or SKILL.md
- `--check-tokens`: Validate token counts
- `--check-refs`: Validate cross-references
- `--max-level1 <n>`: Max tokens for Level 1 (default: 2000)
- `--verbose`: Show detailed output

**Example:**

```bash
npm run skill-loader -- validate skills/coding-standards/ --check-tokens --check-refs

# Output:
# ✅ YAML frontmatter valid
# ✅ Required fields present
# ✅ Level 1 section found (336 tokens)
# ✅ Level 2 section found
# ✅ Cross-references valid
# Overall: PASSED
```

##### `auto-load`

Auto-detect and load recommended skills.

**Syntax:**

```bash
npm run skill-loader -- auto-load <project-path> [options]
```

**Parameters:**

- `<project-path>`: Path to project
- `--level <1|2|3>`: Level to load (default: 1)
- `--yes`: Skip confirmation prompt
- `--output <file>`: Save loaded skills

**Example:**

```bash
npm run skill-loader -- auto-load ./ --level 1 --output .claude/skills.md

# Output:
# Detected: REST API (Node.js/Express)
# Load all recommended skills? [Y/n] y
# ✓ Loaded coding-standards (336 tokens)
# ✓ Loaded security-practices (409 tokens)
# ✓ Loaded testing (430 tokens)
# Total: 1,175 tokens
```

---

## Load Syntax

### Basic Load

```bash
# Load single skill
@load skill:<skill-name>

# Load with level
@load skill:<skill-name> --level <1|2|3>
```

### Composite Load

```bash
# Load multiple skills
@load [skill:<skill1> + skill:<skill2> + skill:<skill3>]

# With different levels
@load [
  skill:<skill1> --level 2 +
  skill:<skill2> --level 1 +
  skill:<skill3> --level 2
]
```

### Product Type Load

```bash
# Load by product type
@load product:<product-type>

# With language override
@load product:<product-type> --language <lang>

# With framework override
@load product:<product-type> --framework <framework>

# Combined
@load product:api --language python --framework fastapi
```

### Wildcard Load

```bash
# Load all matching skills
@load skill:security-*

# Expands to all skills starting with "security-"
# Example: security-practices, security-monitoring, etc.
```

### Conditional Load

```bash
# Load based on condition
@load skill:<skill-name> if <condition>

# Examples:
@load skill:nist-compliance if env === "production"
@load skill:testing if exists("tests/")
```

---

## Product Matrix API

### Configuration Format

**File**: `config/product-matrix.yaml`

```yaml
version: 1

defaults:
  include_nist_on_security: true
  auto_expand_wildcards: true

products:
  <product-type>:
    description: "<description>"
    standards:
      - <standard-code>
      - <standard-code>
      ...

wildcards:
  "<pattern>":
    description: "<description>"
    expands_to:
      - <standard-code>
      - <standard-code>

language_mappings:
  <language>:
    <category>: <standard-code>

framework_mappings:
  <framework>:
    <category>: <standard-code>
```

### Standard Codes

| Code | Category | Description |
|------|----------|-------------|
| `CS:*` | Coding Standards | Language-specific coding patterns |
| `TS:*` | Testing | Testing frameworks and strategies |
| `SEC:*` | Security | Security practices and patterns |
| `NIST-IG:base` | Compliance | NIST baseline controls |
| `DOP:*` | DevOps | CI/CD and infrastructure |
| `OBS:*` | Observability | Monitoring and logging |
| `FE:*` | Frontend | Frontend development patterns |
| `DE:*` | Data Engineering | Data pipeline patterns |

### Resolution Rules

1. **Product Type Lookup**: `product:<type>` → Standards list
2. **Wildcard Expansion**: `SEC:*` → All security standards
3. **Language Mapping**: `--language python` → `CS:python`, `TS:pytest`
4. **Framework Mapping**: `--framework fastapi` → `CS:fastapi`, `SEC:fastapi-security`
5. **Auto NIST Inclusion**: If any `SEC:*` present → Add `NIST-IG:base`
6. **Standard to Skill**: Map standard codes to skill directories

---

## Skill Resolution

### Resolution Algorithm

```typescript
interface SkillResolver {
  /**
   * Resolve skill request to skill paths
   */
  resolveSkills(request: string): Promise<string[]>

  /**
   * Parse load request
   */
  parseRequest(request: string): ParsedRequest

  /**
   * Resolve product type to skills
   */
  resolveProductSkills(product: string): Promise<string[]>

  /**
   * Expand wildcards
   */
  expandWildcard(pattern: string): Promise<string[]>

  /**
   * Map standard code to skill
   */
  standardCodeToSkill(stdCode: string): string | null
}
```

### Resolution Flow

```
Input: @load product:api --language python
  ↓
Parse Request
  product: api
  language: python
  ↓
Lookup Product Matrix
  product:api → [CS:language, TS:framework, SEC:auth, SEC:input-validation, ...]
  ↓
Apply Language Mapping
  --language python → CS:python, TS:pytest
  ↓
Expand Wildcards
  SEC:* → [SEC:auth, SEC:secrets, SEC:input-validation, ...]
  ↓
Auto-Include NIST
  SEC present → Add NIST-IG:base
  ↓
Map to Skills
  CS:python → skill:coding-standards
  TS:pytest → skill:testing
  SEC:auth → skill:security-practices
  NIST-IG:base → skill:nist-compliance
  ↓
Output: [coding-standards, testing, security-practices, nist-compliance]
```

---

## Progressive Loading

### Level Definitions

| Level | Time | Token Budget | Content |
|-------|------|--------------|---------|
| 1 | 5 min | <2,000 | Core principles, quick reference, checklist |
| 2 | 30 min | <5,000 total | Detailed patterns, examples, integration |
| 3 | Extended | Flexible | Advanced topics, resources, tools |

### Loading API

```typescript
interface ProgressiveLoader {
  /**
   * Load skill at specified level
   */
  loadSkill(
    skillPath: string,
    level: 1 | 2 | 3
  ): Promise<SkillContent>

  /**
   * Parse skill markdown
   */
  parseSkillMarkdown(content: string): ParsedSkill

  /**
   * Estimate token count
   */
  estimateTokens(content: string): number

  /**
   * Load bundled resources
   */
  loadBundledResources(skillPath: string): Promise<SkillResources>
}

interface SkillContent {
  name: string
  description: string
  content: string
  estimatedTime: string
  tokenCost: number
  resources?: SkillResources
}

interface ParsedSkill {
  frontmatter: {
    name: string
    description: string
    [key: string]: any
  }
  level1: string
  level2: string
  level3: string
  fullContent: string
}
```

---

## Validation API

### Validation Tool

```bash
python scripts/validate-skills.py <skill-path> [options]
```

### Validation Checks

```python
class SkillValidator:
    """Validates skill structure and content."""

    def validate_skill(self, skill_path: str) -> ValidationResult:
        """
        Validate skill structure and content.

        Checks:
        - YAML frontmatter presence and structure
        - Required fields (name, description)
        - Level 1, 2, 3 sections
        - Token count guidelines
        - Cross-reference validity
        - Directory structure

        Returns:
            ValidationResult with errors, warnings, and status
        """
        pass

    def validate_frontmatter(self, content: str) -> List[str]:
        """Validate YAML frontmatter."""
        pass

    def validate_levels(self, content: str) -> List[str]:
        """Validate Level 1, 2, 3 sections."""
        pass

    def check_token_counts(self, content: str) -> List[str]:
        """Check token counts against guidelines."""
        pass

    def validate_cross_references(self, skill_path: str) -> List[str]:
        """Validate cross-references to other skills."""
        pass

class ValidationResult:
    errors: List[str]
    warnings: List[str]
    valid: bool
    token_estimates: Dict[str, int]
```

### Validation Output

```json
{
  "skill": "coding-standards",
  "valid": true,
  "errors": [],
  "warnings": [
    "Level 3 section is short (may want to expand)"
  ],
  "token_estimates": {
    "level1": 336,
    "level2": 1245,
    "level3": 1342,
    "total": 2923
  },
  "sections": {
    "has_level1": true,
    "has_level2": true,
    "has_level3": true
  },
  "frontmatter": {
    "valid": true,
    "has_name": true,
    "has_description": true
  },
  "cross_references": {
    "valid": true,
    "broken_links": []
  }
}
```

---

## Programmatic API

### TypeScript API

```typescript
import { SkillLoader } from '@standards/skills'

// Initialize loader
const loader = new SkillLoader({
  skillsDir: './skills',
  productMatrix: './config/product-matrix.yaml'
})

// Load single skill
const skill = await loader.loadSkill('coding-standards', { level: 1 })
console.log(skill.content)
console.log(`Token cost: ${skill.tokenCost}`)

// Load by product type
const skills = await loader.loadProductType('api', {
  language: 'python',
  level: 1
})

// Get recommendations
const recommendations = await loader.recommend('./')
console.log(recommendations)

// Compose skills
const bundle = await loader.composeSkills(
  ['coding-standards', 'security-practices', 'testing'],
  { level: 1 }
)
await bundle.save('.claude/bundle.md')
```

### Python API

```python
from standards.skills import SkillLoader

# Initialize loader
loader = SkillLoader(
    skills_dir='./skills',
    product_matrix='./config/product-matrix.yaml'
)

# Load single skill
skill = loader.load_skill('coding-standards', level=1)
print(skill.content)
print(f"Token cost: {skill.token_cost}")

# Load by product type
skills = loader.load_product_type('api', language='python', level=1)

# Get recommendations
recommendations = loader.recommend('./')
print(recommendations)

# Compose skills
bundle = loader.compose_skills(
    ['coding-standards', 'security-practices', 'testing'],
    level=1
)
bundle.save('.claude/bundle.md')
```

---

## Configuration

### Environment Variables

```bash
# Skills directory
SKILLS_DIR=./skills

# Product matrix file
PRODUCT_MATRIX=./config/product-matrix.yaml

# Cache directory
SKILLS_CACHE_DIR=./.cache/skills

# Default level
SKILLS_DEFAULT_LEVEL=1

# Token limits
SKILLS_MAX_LEVEL1_TOKENS=2000
SKILLS_MAX_LEVEL2_TOKENS=5000
```

### Configuration File

**File**: `.skillsrc.yaml`

```yaml
# Skills configuration
version: 1

# Directories
skills_dir: ./skills
product_matrix: ./config/product-matrix.yaml
cache_dir: ./.cache/skills

# Defaults
default_level: 1
default_format: markdown

# Token limits
token_limits:
  level1: 2000
  level2: 5000
  level3: null  # No limit

# Validation
validation:
  strict: false
  check_tokens: true
  check_refs: true
  max_warnings: 10

# Caching
cache:
  enabled: true
  ttl: 3600  # 1 hour

# Auto-recommendations
recommendations:
  min_priority: medium
  auto_include_nist: true
```

---

## Examples

### Example 1: Basic CLI Usage

```bash
# List available skills
npm run skill-loader -- list

# Load a skill
npm run skill-loader -- load skill:coding-standards --level 1

# Get recommendations
npm run skill-loader -- recommend ./

# Auto-load recommended
npm run skill-loader -- auto-load ./ --yes
```

### Example 2: Product Type Loading

```bash
# Load API bundle
npm run skill-loader -- load product:api --language python --output .claude/api-skills.md

# Load frontend bundle
npm run skill-loader -- load product:frontend-web --framework react --output .claude/frontend-skills.md
```

### Example 3: Custom Composition

```bash
# Create custom bundle
npm run skill-loader -- compose \
  skill:coding-standards \
  skill:security-practices \
  skill:testing \
  skill:nist-compliance \
  --level 1 \
  --output .claude/compliance-bundle.md \
  --name "Compliance Development Bundle"
```

### Example 4: Validation

```bash
# Validate single skill
python scripts/validate-skills.py skills/coding-standards/

# Validate all skills
python scripts/validate-skills.py skills/ --check-tokens --check-refs

# Export validation report
python scripts/validate-skills.py skills/ --format json --output validation-report.json
```

### Example 5: Programmatic Usage (TypeScript)

```typescript
import { SkillLoader } from '@standards/skills'

async function loadProjectSkills() {
  const loader = new SkillLoader()

  // Get recommendations
  const recs = await loader.recommend('./')

  // Load recommended skills
  const skills = await Promise.all(
    recs.map(rec => loader.loadSkill(rec.skill, { level: 1 }))
  )

  // Calculate total tokens
  const totalTokens = skills.reduce((sum, skill) => sum + skill.tokenCost, 0)

  console.log(`Loaded ${skills.length} skills (${totalTokens} tokens)`)

  // Save bundle
  const bundle = await loader.composeSkills(
    skills.map(s => s.name),
    { level: 1 }
  )
  await bundle.save('.claude/project-skills.md')
}

loadProjectSkills()
```

---

## API Reference

### Types

```typescript
// Skill content
interface SkillContent {
  name: string
  description: string
  content: string
  estimatedTime: string
  tokenCost: number
  resources?: SkillResources
}

// Skill resources
interface SkillResources {
  templates: FileResource[]
  scripts: FileResource[]
  resources: FileResource[]
}

interface FileResource {
  path: string
  content: string
  type: string
}

// Recommendations
interface SkillRecommendation {
  skill: string
  priority: 'low' | 'medium' | 'high' | 'critical'
  reason: string
  tokenCost: number
}

// Validation
interface ValidationResult {
  valid: boolean
  errors: string[]
  warnings: string[]
  tokenEstimates: Record<string, number>
}

// Project analysis
interface ProjectAnalysis {
  hasTests: boolean
  isApi: boolean
  isWebService: boolean
  hasSecurityCode: boolean
  hasComplianceFiles: boolean
  languages: string[]
  frameworks: string[]
}
```

---

## Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `SKILL_NOT_FOUND` | Skill does not exist | Check spelling, run `list` command |
| `INVALID_LEVEL` | Invalid level specified | Use 1, 2, or 3 |
| `INVALID_PRODUCT_TYPE` | Unknown product type | Check product-matrix.yaml |
| `VALIDATION_FAILED` | Skill validation failed | Fix errors in SKILL.md |
| `TOKEN_LIMIT_EXCEEDED` | Token budget exceeded | Move content to higher level |
| `INVALID_CROSS_REF` | Broken cross-reference | Fix or remove reference |

---

## Rate Limits

**Note**: Currently no rate limits. Future API service may implement:

- 100 requests/minute per API key
- 1000 requests/hour per API key
- 10,000 requests/day per API key

---

## Changelog

### v1.0.0 (2025-10-16)

- Initial release
- CLI API with load, recommend, compose, list, validate commands
- Load syntax (@load directives)
- Product matrix configuration
- Skill resolution algorithm
- Progressive loading (Level 1, 2, 3)
- Validation API
- TypeScript/Python programmatic APIs

---

## Support

- **Documentation**: [Skills User Guide](../guides/SKILLS_USER_GUIDE.md)
- **GitHub Issues**: [Report bugs](https://github.com/williamzujkowski/standards/issues)
- **Discussions**: [Ask questions](https://github.com/williamzujkowski/standards/discussions)

---

*Last Updated: 2025-10-16*
*Version: 1.0.0*
*Maintained by: Standards Repository Team*
