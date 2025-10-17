# Skill Authoring Guide

**Version**: 1.0.0
**Target Audience**: Contributors, Standards Authors
**Last Updated**: 2025-10-16

---

## Table of Contents

1. [Introduction](#introduction)
2. [Skill Structure](#skill-structure)
3. [Creating a New Skill](#creating-a-new-skill)
4. [Writing Skill Content](#writing-skill-content)
5. [Progressive Disclosure Guidelines](#progressive-disclosure-guidelines)
6. [YAML Frontmatter](#yaml-frontmatter)
7. [Bundled Resources](#bundled-resources)
8. [Cross-References](#cross-references)
9. [Validation](#validation)
10. [Publishing](#publishing)
11. [Best Practices](#best-practices)

---

## Introduction

### What Is a Skill?

A **skill** is a self-contained, modular standard that uses **progressive disclosure** to deliver information at three levels:

- **Level 1**: Quick Start (5 minutes, <2,000 tokens)
- **Level 2**: Implementation (30 minutes, <5,000 tokens)
- **Level 3**: Mastery (Extended, flexible tokens)

### Why Author Skills?

**Benefits of Skills Format:**
- ✅ **Modular**: Each skill is independent and versioned
- ✅ **Discoverable**: Auto-recommendations based on context
- ✅ **Efficient**: 90%+ token reduction through progressive loading
- ✅ **Maintainable**: Small, focused files instead of monolithic docs
- ✅ **Composable**: Skills work together seamlessly

---

## Skill Structure

### Directory Layout

```
skills/
└── your-skill-name/
    ├── SKILL.md              # Main skill content (required)
    ├── README.md             # Skill overview (optional but recommended)
    ├── templates/            # Implementation templates
    │   ├── template1.ext
    │   └── template2.ext
    ├── scripts/              # Automation scripts
    │   ├── validate.sh
    │   └── generate.py
    └── resources/            # Additional resources
        ├── reference.md
        └── examples/
```

### Required Files

1. **`SKILL.md`** (required)
   - Main skill content
   - YAML frontmatter
   - Level 1, 2, 3 sections

2. **`README.md`** (recommended)
   - Skill overview
   - When to use
   - Quick links

3. **Subdirectories** (optional)
   - `templates/` - Ready-to-use templates
   - `scripts/` - Automation tools
   - `resources/` - Additional references

---

## Creating a New Skill

### Step 1: Choose a Name

**Naming Conventions:**
- Use `kebab-case` for directory names
- Be descriptive and specific
- Avoid generic names

**Examples:**

```bash
# ✅ Good names
coding-standards
security-practices
nist-compliance
api-design-patterns

# ❌ Bad names
best-practices    # Too generic
coding            # Too broad
sec               # Too short, unclear
```

### Step 2: Use the Skill Generator

```bash
# Generate skill scaffold
python scripts/generate-skill.py \
  --name your-skill-name \
  --description "Brief description (max 1024 chars)" \
  --output skills/your-skill-name

# Output:
# ✓ Created skills/your-skill-name/SKILL.md
# ✓ Created skills/your-skill-name/README.md
# ✓ Created skills/your-skill-name/templates/
# ✓ Created skills/your-skill-name/scripts/
# ✓ Created skills/your-skill-name/resources/
```

### Step 3: Fill in the Template

The generator creates a template with placeholders:

```markdown
---
name: your-skill-name
description: [FILL IN: Brief description, max 1024 chars]
---

# [Skill Title]

## Level 1: Quick Start (5 minutes)

### What You'll Learn
[FILL IN: 2-3 sentence overview]

### Core Principles
[FILL IN: 3-5 key principles]

### Quick Reference
[FILL IN: Code snippet or checklist]

### Essential Checklist
- [ ] [Item 1]
- [ ] [Item 2]
- [ ] [Item 3]

### Common Pitfalls
[FILL IN: 3-5 common mistakes]

---

## Level 2: Implementation (30 minutes)

### Deep Dive Topics

#### 1. [Topic Name]
[FILL IN: Detailed explanation with code examples]

#### 2. [Topic Name]
[FILL IN: Implementation patterns]

### Integration Points
- Links to related skills (example: `[Another Skill](../another-skill/SKILL.md)`)

---

## Level 3: Mastery (Extended Learning)

### Advanced Topics

#### 1. [Advanced Topic]
[FILL IN: Advanced patterns and techniques]

### Resources
[FILL IN: External links, books, tools]

### Bundled Resources
- [Resource Name](./resources/file.md)
- Scripts in `./scripts/`
- Templates in `./templates/`
```

---

## Writing Skill Content

### Level 1: Quick Start

**Goal**: Get users productive in 5 minutes

**Structure:**

```markdown
## Level 1: Quick Start (5 minutes)

### What You'll Learn
[2-3 sentences: Clear value proposition]

### Core Principles
- **Principle 1**: One-line explanation
- **Principle 2**: One-line explanation
- **Principle 3**: One-line explanation
[3-5 principles maximum]

### Quick Reference
```language
# Minimal code example demonstrating core concept
[5-10 lines maximum]
```
```

### Essential Checklist
- [ ] Action item 1
- [ ] Action item 2
- [ ] Action item 3
[5-8 items maximum]

### Common Pitfalls
- Pitfall 1: Brief explanation + solution
- Pitfall 2: Brief explanation + solution
[3-5 items maximum]
```

**Token Budget**: <2,000 tokens

**Example: Good Level 1**

```markdown
## Level 1: Quick Start (5 minutes)

### What You'll Learn
Apply essential coding standards for clean, maintainable code that follows industry best practices.

### Core Principles
- **Consistency**: Follow established style guides (PEP 8, Airbnb, Google)
- **Readability**: Write self-documenting code with clear naming
- **Maintainability**: Keep functions small (<50 lines), files focused (<500 lines)
- **Quality**: Enforce standards with linters and formatters

### Quick Reference

```python
# ✅ Good: Clear naming, single responsibility
def calculate_user_discount(user: User, order: Order) -> Decimal:
    """Calculate discount based on user tier and order total."""
    if user.tier == "premium":
        return order.total * Decimal("0.15")
    return order.total * Decimal("0.05")

# ❌ Bad: Unclear naming, mixed concerns
def calc(u, o):
    d = 0.15 if u.t == "p" else 0.05
    save_to_db(u, o, d)  # Side effect!
    return o.t * d
```

### Essential Checklist
- [ ] Follow language-specific style guide
- [ ] Use meaningful, descriptive names
- [ ] Limit function complexity (cyclomatic < 10)
- [ ] Configure linter and formatter
- [ ] Add pre-commit hooks

### Common Pitfalls
- Inconsistent naming conventions within a project
- Functions that do too many things
- Missing or outdated documentation
- Skipping code reviews
```

**Why This Works:**
- ✅ Scannable structure
- ✅ Actionable content
- ✅ Concrete examples
- ✅ Clear next steps
- ✅ Under 2,000 tokens

### Level 2: Implementation

**Goal**: Provide comprehensive implementation guidance (30 minutes)

**Structure:**

```markdown
## Level 2: Implementation (30 minutes)

### Deep Dive Topics

#### 1. [Topic Name]

[Detailed explanation]

**[Subtopic]:**

```language
// Complete code example (20-30 lines)
```

[Analysis and explanation]

#### 2. [Topic Name]

[Detailed patterns with examples]

#### 3. [Topic Name]

[Integration points and best practices]

### Implementation Patterns

[Pattern 1: Description + example]
[Pattern 2: Description + example]

### Automation Tools

```json
// Tool configuration example
```

### Integration Points
- Links to related skills (example: `[Another Skill](../another-skill/SKILL.md)`) for specific aspects
- Links to related skills (example: `[Another Skill](../another-skill/SKILL.md)`) for integration patterns
```

**Token Budget**: <5,000 tokens (combined with Level 1)

**Example: Good Level 2 Section**

```markdown
#### 1. Code Style and Formatting

**Naming Conventions by Language:**

```typescript
// TypeScript/JavaScript
class UserService {}           // PascalCase for classes
const getUserById = () => {}   // camelCase for functions
const API_ENDPOINT = "..."     // UPPER_SNAKE_CASE for constants
```

```python
# Python
class UserService:              # PascalCase for classes
def get_user_by_id():          # snake_case for functions
API_ENDPOINT = "..."           # UPPER_SNAKE_CASE for constants
```

**File Organization:**
```
src/
├── models/           # Data models and types
├── services/         # Business logic (max 500 lines/file)
├── controllers/      # Request handlers
├── utils/           # Shared utilities
└── config/          # Configuration
```
```

**Why This Works:**
- ✅ Multiple languages covered
- ✅ Complete examples
- ✅ Practical file structure
- ✅ Actionable guidance

### Level 3: Mastery

**Goal**: Advanced topics, comprehensive resources, tooling

**Structure:**

```markdown
## Level 3: Mastery (Extended Learning)

### Advanced Topics

#### 1. [Advanced Topic Name]

[Deep dive into advanced patterns]

```language
// Advanced example (30-50 lines)
```

[Detailed analysis]

#### 2. [Advanced Topic Name]

[Expert-level guidance]

### Resources

#### Essential Reading
- Example: `[Book/Article Title](https://example.com)`
- Example: `[Documentation](https://docs.example.com)`

#### Tools and Frameworks
- **Category**: Tool 1, Tool 2, Tool 3
- **Category**: Tool 1, Tool 2, Tool 3

#### Language-Specific Style Guides
- Example: `[Python PEP 8](https://peps.python.org/pep-0008/)`
- Example: `[JavaScript Standard Style](https://standardjs.com/)`

### Templates

[Include template examples or link to ./templates/]

### Scripts

[Include script examples or link to ./scripts/]

---

## Bundled Resources

- Full original standard (if applicable): `../../docs/standards/ORIGINAL.md`
- Templates in `./templates/`
- Scripts in `./scripts/`
- Resources in `./resources/`
```

**Token Budget**: Flexible

---

## Progressive Disclosure Guidelines

### Token Budgets

| Level | Time | Token Budget | Use Case |
|-------|------|--------------|----------|
| 1 | 5 min | <2,000 | Quick reference, onboarding |
| 2 | 30 min | <5,000 total | Implementation, deep dive |
| 3 | Extended | Flexible | Mastery, tools, references |

### Content Allocation

**Level 1 (20% of content)**
- Core principles
- Essential checklist
- Quick examples
- Common pitfalls

**Level 2 (50% of content)**
- Detailed patterns
- Complete examples
- Integration points
- Implementation guidance

**Level 3 (30% of content)**
- Advanced topics
- Comprehensive resources
- External references
- Tools and templates

### Writing Guidelines

#### DO:
- ✅ Use concrete examples
- ✅ Provide actionable checklists
- ✅ Include code snippets
- ✅ Link related skills
- ✅ Use consistent formatting
- ✅ Add NIST mappings where relevant

#### DON'T:
- ❌ Include entire articles in Level 1
- ❌ Use vague language ("should", "might")
- ❌ Duplicate content across levels
- ❌ Omit examples
- ❌ Use inconsistent code style
- ❌ Create circular references

---

## YAML Frontmatter

### Required Fields

```yaml
---
name: skill-name
description: Brief description of what this skill provides, when to use it, and key capabilities (max 1024 chars)
---
```

### Optional Fields

```yaml
---
name: skill-name
description: [Brief description]
version: 1.0.0
author: Your Name
last_updated: 2025-10-16
tags:
  - coding
  - python
  - testing
prerequisites:
  - skill:coding-standards
dependencies:
  - skill:security-practices
estimated_time:
  level1: 5min
  level2: 30min
  level3: 2hr
---
```

### Description Guidelines

**Good Description:**
```yaml
description: Comprehensive coding standards and best practices for maintainable, consistent software development across multiple languages and paradigms. Load when starting projects, conducting code reviews, or establishing team conventions.
```

**Why It Works:**
- Clear scope (coding standards)
- Key benefits (maintainable, consistent)
- Coverage (multiple languages)
- Use cases (when to load)

**Bad Description:**
```yaml
description: Coding stuff.
```

**Why It Fails:**
- Too vague
- No use cases
- No scope

---

## Bundled Resources

### Templates

Create implementation templates in `templates/`:

```
templates/
├── linter-config.json
├── prettier.config.js
├── pre-commit-hooks.sh
└── README.md
```

**Template Example:**

```json
// templates/linter-config.json
{
  "extends": ["eslint:recommended"],
  "rules": {
    "complexity": ["error", 10],
    "max-lines-per-function": ["error", 50],
    "max-lines": ["error", 500]
  }
}
```

### Scripts

Add automation scripts in `scripts/`:

```
scripts/
├── check-complexity.py
├── validate-formatting.sh
└── README.md
```

**Script Example:**

```python
#!/usr/bin/env python3
"""Check cyclomatic complexity of Python files."""
import sys
from radon.complexity import cc_visit

def check_complexity(filename: str, max_complexity: int = 10) -> bool:
    """Check if file exceeds complexity threshold."""
    with open(filename) as f:
        code = f.read()

    results = cc_visit(code)
    violations = [r for r in results if r.complexity > max_complexity]

    if violations:
        print(f"❌ {filename}: Complexity violations found")
        for v in violations:
            print(f"  - {v.name}: complexity {v.complexity} (max {max_complexity})")
        return False

    print(f"✅ {filename}: All functions within complexity limit")
    return True

if __name__ == "__main__":
    passed = check_complexity(sys.argv[1])
    sys.exit(0 if passed else 1)
```

### Resources

Add supplementary content in `resources/`:

```
resources/
├── style-guides.md
├── tool-comparison.md
├── examples/
│   ├── good-example.py
│   └── bad-example.py
└── README.md
```

---

## Cross-References

### Linking to Other Skills

```markdown
### Integration Points
- Example: [Security Practices](../../skills/security/security-fundamentals/SKILL.md) for secure coding patterns
- Example: [Testing Standards](../../skills/testing/unit-testing/SKILL.md) for testable code design
- Example: [NIST Compliance](../../skills/compliance/nist/SKILL.md) for SI-10, SI-11 controls
```

### Linking to Original Standards

```markdown
## Bundled Resources
- [Full CODING_STANDARDS.md](../../docs/standards/CODING_STANDARDS.md)
- [UNIFIED_STANDARDS.md](../../docs/standards/UNIFIED_STANDARDS.md)
```

### NIST Control Mappings

```markdown
**NIST Mapping:**
- @nist-controls: [si-10, si-11, au-2, au-3]
```

---

## Validation

### Automated Validation

```bash
# Validate skill structure
python scripts/validate-skills.py skills/your-skill-name/

# Expected output:
# ✅ YAML frontmatter valid
# ✅ Required fields present (name, description)
# ✅ Level 1 section found
# ✅ Level 2 section found (recommended)
# ✅ Token count: Level 1 = 423 tokens (<2000 ✓)
# ✅ Cross-references valid
# ✅ Directory structure complete
#
# Overall: PASSED
```

### Manual Validation Checklist

- [ ] YAML frontmatter valid
- [ ] Name and description present
- [ ] Level 1 section exists
- [ ] Level 1 token count <2,000
- [ ] Level 2 section exists (recommended)
- [ ] Code examples work
- [ ] Cross-references valid
- [ ] Templates functional
- [ ] Scripts executable
- [ ] README.md present

### Token Count Verification

```bash
# Check token estimates
python scripts/validate-skills.py skills/your-skill-name/ --check-tokens

# Output:
# Level 1: 423 tokens ✓ (<2000)
# Level 2: 1,876 tokens ✓ (<5000 combined)
# Level 3: 892 tokens
# Total: 3,191 tokens
```

---

## Publishing

### Step 1: Final Validation

```bash
# Run full validation
python scripts/validate-skills.py skills/your-skill-name/ --verbose

# Validate cross-references
python scripts/validate-skills.py skills/your-skill-name/ --check-refs

# Test skill loading
npm run skill-loader -- load skill:your-skill-name --level 1
```

### Step 2: Documentation

Update skill catalog:

```bash
# Auto-generate catalog entry
python scripts/generate-catalog.py --add skills/your-skill-name/
```

### Step 3: Submit Pull Request

```bash
git checkout -b add-skill-your-skill-name
git add skills/your-skill-name/
git commit -m "feat: Add your-skill-name skill

- Level 1: Quick Start (423 tokens)
- Level 2: Implementation (1,876 tokens)
- Level 3: Mastery (892 tokens)
- Includes templates, scripts, resources
- Validated with 0 errors, 0 warnings"

git push origin add-skill-your-skill-name

# Open PR with template
gh pr create --title "Add your-skill-name skill" --body-file .github/PULL_REQUEST_TEMPLATE.md
```

### Step 4: Review Process

Your PR will be reviewed for:

1. **Structure**: Proper directory layout
2. **Content**: Level 1, 2, 3 sections present
3. **Validation**: Passes automated checks
4. **Token Budget**: Level 1 <2,000 tokens
5. **Examples**: Working code examples
6. **Cross-References**: Valid links
7. **Resources**: Templates, scripts functional

---

## Best Practices

### Content Writing

1. **Start with Level 1**
   - Write Level 1 first to clarify scope
   - Ensure <2,000 tokens
   - Test with target audience

2. **Expand to Level 2**
   - Add detailed patterns and examples
   - Keep combined (L1+L2) <5,000 tokens
   - Link to related skills

3. **Complete with Level 3**
   - Add advanced topics
   - Include comprehensive resources
   - Link to templates and scripts

### Code Examples

1. **Use Real-World Examples**
   - ✅ Production-ready code
   - ❌ Toy examples

2. **Show Good vs Bad**
   ```language
   // ✅ Good: Description
   [good example]

   // ❌ Bad: Description
   [bad example]
   ```

3. **Keep Examples Focused**
   - Level 1: 5-10 lines
   - Level 2: 20-30 lines
   - Level 3: 30-50 lines

### Maintenance

1. **Version Your Skill**
   ```yaml
   version: 1.0.0
   last_updated: 2025-10-16
   ```

2. **Update Dependencies**
   ```yaml
   dependencies:
     - skill:security-practices@1.0.0
   ```

3. **Deprecation Path**
   ```markdown
   > **Deprecated**: This skill is deprecated in favor of [New Skill](../new-skill/SKILL.md)
   ```

---

## Examples

### Example 1: Minimal Skill

```markdown
---
name: minimal-example
description: A minimal skill demonstrating required structure
---

# Minimal Example Skill

## Level 1: Quick Start (5 minutes)

### What You'll Learn
Core concept in 2-3 sentences.

### Core Principles
- **Principle 1**: Explanation
- **Principle 2**: Explanation

### Quick Reference
```language
// Minimal code example
```

### Essential Checklist
- [ ] Item 1
- [ ] Item 2

### Common Pitfalls
- Pitfall 1: Solution
```

### Example 2: Full Skill

See existing skills:
- `skills/coding-standards/SKILL.md`
- `skills/testing/SKILL.md`
- `skills/security-practices/SKILL.md`

---

## Get Help

### Resources
- **Validation Tool**: `python scripts/validate-skills.py --help`
- **Generator Tool**: `python scripts/generate-skill.py --help`
- **Examples**: Existing skills in `skills/` directory

### Support
- **GitHub Issues**: [Report issues](https://github.com/williamzujkowski/standards/issues)
- **Discussions**: [Ask questions](https://github.com/williamzujkowski/standards/discussions)

---

**Start Creating!** 🎨

Skills make standards more modular, discoverable, and maintainable. Follow these guidelines to create high-quality skills that benefit the entire community.

---

*Last Updated: 2025-10-16*
*Version: 1.0.0*
*Maintained by: Standards Repository Team*
