# Skills Migration Quality Checklist

**Version**: 1.0.0
**Last Updated**: 2025-10-17
**Purpose**: Ensure consistent, high-quality skill implementation aligned with Anthropic's standards

---

## Pre-Implementation Checklist

### Planning Phase

- [x] Migration strategy document created
- [x] Skill mapping from existing standards defined
- [x] Directory structure planned
- [ ] Automation scripts designed
- [ ] Testing strategy defined
- [ ] Validation criteria established
- [ ] Timeline and milestones set
- [ ] Resource allocation confirmed

### Infrastructure Setup

- [x] `/skills` directory created
- [ ] All required skill subdirectories present
- [ ] Script directory structure (`/scripts/migration/`)
- [ ] Test framework directory (`/tests/skills/`)
- [ ] Documentation directory (`/docs/migration/`)
- [ ] CI/CD pipeline updated for skills validation

---

## Per-Skill Implementation Checklist

Use this checklist for each skill being created:

### 1. File Structure

**Directory Structure**:

- [ ] `SKILL.md` file created in skill root
- [ ] `/resources` subdirectory present
- [ ] `/scripts` subdirectory present (if applicable)
- [ ] `/templates` subdirectory present (if applicable)
- [ ] `/examples` subdirectory present

**File Naming**:

- [ ] Main file named exactly `SKILL.md` (case-sensitive)
- [ ] Resource files use descriptive kebab-case names
- [ ] Script files include `.sh` or `.py` extensions
- [ ] Template files clearly indicate purpose

### 2. YAML Frontmatter Validation

**Required Fields**:

```yaml
---
name: skill-name
description: Clear description text
---
```

**Checklist**:

- [ ] YAML frontmatter present at file start
- [ ] Opening and closing `---` delimiters present
- [ ] `name` field present and valid
- [ ] `description` field present
- [ ] Name uses kebab-case (lowercase with hyphens)
- [ ] Name matches directory name
- [ ] Description is clear and actionable
- [ ] Description length ≤ 1024 characters
- [ ] Description explains WHEN to use skill
- [ ] Description includes key capabilities
- [ ] No typos or grammatical errors in description

### 3. Description Quality Assessment

**Content Requirements**:

- [ ] Clearly states what the skill does
- [ ] Explains when Claude should use it
- [ ] Lists key capabilities (3-5 items)
- [ ] Uses active voice
- [ ] Avoids jargon or explains necessary terms
- [ ] Includes specific triggers/use cases

**Quality Metrics**:

- [ ] Character count: ____ / 1024 (must be ≤ 1024)
- [ ] Clarity score: Excellent / Good / Needs Improvement
- [ ] Completeness: All required elements present
- [ ] Actionability: Clear when to activate skill

**Example Good Description**:

```yaml
description: |
  Provides comprehensive coding standards and best practices for multiple
  programming languages including Python, JavaScript, TypeScript, and Go.
  Use this skill when reviewing code quality, establishing team conventions,
  or implementing language-specific patterns. Includes style guides, naming
  conventions, error handling patterns, and performance optimization techniques.
```

### 4. Content Structure Validation

**Required Sections**:

- [ ] `# [Skill Title]` - Main heading present
- [ ] `## Overview` - Brief introduction (Level 2)
- [ ] `## When to Use This Skill` - Clear triggers
- [ ] `## Core Instructions` - Main procedural knowledge
- [ ] `## Advanced Topics` - References to Level 3 resources
- [ ] `## Examples` - At least 2-3 concrete examples

**Content Quality**:

- [ ] Overview is concise (2-4 paragraphs)
- [ ] "When to Use" lists 3-5 specific scenarios
- [ ] Core Instructions are actionable and clear
- [ ] Advanced Topics reference external files, not embedded
- [ ] Examples are realistic and practical
- [ ] Code examples include proper formatting
- [ ] All internal links are valid

### 5. Progressive Disclosure Implementation

**Level 1 (Metadata - Always Loaded)**:

- [ ] YAML frontmatter only
- [ ] Name and description fields
- [ ] No additional metadata bloating

**Level 2 (Core Instructions - Loaded When Activated)**:

- [ ] Main SKILL.md body content
- [ ] Token count < 5,000 tokens
- [ ] Essential knowledge only
- [ ] No large code blocks embedded
- [ ] References to Level 3 resources

**Level 3 (Resources - Loaded On Demand)**:

- [ ] Additional markdown files in `/resources`
- [ ] Scripts in `/scripts` directory
- [ ] Templates in `/templates` directory
- [ ] Examples in `/examples` directory
- [ ] Each resource properly referenced from SKILL.md

**Token Budget**:

- [ ] Level 1: < 100 tokens (frontmatter)
- [ ] Level 2: < 5,000 tokens (main content)
- [ ] Level 3: Unlimited (lazy loaded)

### 6. Resource References Validation

**Reference Format**:

```markdown
For detailed Python standards, see `./resources/python-style-guide.md`
For linting configuration, access `./scripts/setup-linters.sh`
For boilerplate code, use `./templates/class-template.py`
```

**Checklist**:

- [ ] All resources use relative paths
- [ ] Paths start with `./resources/`, `./scripts/`, or `./templates/`
- [ ] Referenced files actually exist
- [ ] No absolute paths used
- [ ] No external URLs without fallback
- [ ] File extensions included in references
- [ ] Purpose of each resource is clear

### 7. Examples Quality

**Requirements**:

- [ ] Minimum 2 examples provided
- [ ] Maximum 5 examples (avoid bloat)
- [ ] Each example has clear context
- [ ] Examples show realistic use cases
- [ ] Code examples are properly formatted
- [ ] Examples demonstrate progressive complexity
- [ ] Each example is self-contained

**Example Format**:

```markdown
## Examples

### Example 1: Basic Code Review
```python
# When reviewing this code, apply Python naming conventions
def calcTotal(x, y):  # Issue: camelCase instead of snake_case
    return x + y
```

**Recommendation**:

```python
def calculate_total(amount_x: float, amount_y: float) -> float:
    """Calculate the sum of two amounts."""
    return amount_x + amount_y
```

```

### 8. Cross-Skill Dependencies

**Documentation**:
- [ ] Dependencies listed in a dedicated section
- [ ] Required skills explicitly named
- [ ] Optional complementary skills noted
- [ ] Composition patterns documented

**Example**:
```markdown
## Related Skills

**Required Dependencies**:
- `security-practices` - For security code review guidelines

**Complementary Skills**:
- `testing` - For test coverage standards
- `performance` - For optimization patterns
```

**Validation**:

- [ ] All referenced skills exist
- [ ] Circular dependencies avoided
- [ ] Dependency graph is acyclic
- [ ] Load order doesn't matter

### 9. Scripts and Automation

**If skill includes scripts**:

- [ ] Scripts have proper shebang (`#!/usr/bin/env python3`)
- [ ] Scripts are executable (`chmod +x`)
- [ ] Scripts include usage documentation
- [ ] Scripts handle errors gracefully
- [ ] Scripts validate inputs
- [ ] Scripts have exit codes
- [ ] Scripts are tested

**Script Documentation**:

```bash
#!/usr/bin/env bash
# Script: setup-linters.sh
# Purpose: Configure ESLint, Pylint, and other linters
# Usage: ./setup-linters.sh [language]
# Example: ./setup-linters.sh python
```

### 10. Templates Quality

**If skill includes templates**:

- [ ] Templates are complete and usable
- [ ] Placeholder syntax is consistent (`{{variable}}`)
- [ ] Templates include comments/documentation
- [ ] Templates follow skill standards
- [ ] Templates are language-appropriate
- [ ] Template usage is documented

### 11. Accessibility and Internationalization

**Content Accessibility**:

- [ ] Headings use proper hierarchy (H1 > H2 > H3)
- [ ] Lists use proper markdown syntax
- [ ] Code blocks specify language for syntax highlighting
- [ ] Links have descriptive text (not "click here")
- [ ] Images include alt text (if any)

**Language**:

- [ ] Uses clear, professional English
- [ ] Avoids idioms or colloquialisms
- [ ] Technical terms are defined on first use
- [ ] Suitable for non-native English speakers

### 12. Testing and Validation

**Automated Tests**:

- [ ] YAML frontmatter parses correctly
- [ ] All resource links resolve
- [ ] Token count within limits
- [ ] Description length within limits
- [ ] No broken markdown formatting
- [ ] Code examples are syntactically valid

**Manual Testing**:

- [ ] Loaded in Claude API successfully
- [ ] Progressive disclosure works correctly
- [ ] Examples are helpful and accurate
- [ ] Instructions are clear and actionable
- [ ] Resources load on demand
- [ ] Cross-skill composition works

**Test Script**:

```bash
# Validate skill format
python3 scripts/validate-skill.py skills/coding-standards/

# Test skill loading
python3 scripts/test-skill-load.py coding-standards

# Check token usage
python3 scripts/analyze-tokens.py skills/coding-standards/SKILL.md
```

### 13. Documentation Completeness

**Internal Documentation**:

- [ ] All sections have content (no TODOs)
- [ ] Code examples include comments
- [ ] Complex concepts are explained
- [ ] Acronyms defined on first use
- [ ] Version history maintained

**External Documentation**:

- [ ] Skill listed in skills catalog
- [ ] Dependencies documented in mapping
- [ ] Migration notes updated
- [ ] API integration guide includes skill

---

## Post-Implementation Checklist

### Integration Testing

- [ ] Skill loads in Claude API
- [ ] Skill activates on appropriate triggers
- [ ] Progressive disclosure functions correctly
- [ ] Resources load on demand
- [ ] Cross-skill composition works
- [ ] No token budget exceeded
- [ ] Performance acceptable

### Quality Assurance

- [ ] Peer review completed
- [ ] Security review passed (if applicable)
- [ ] Compliance check passed (if applicable)
- [ ] User acceptance testing done
- [ ] Feedback incorporated

### Documentation

- [ ] Skills catalog updated
- [ ] Migration guide updated
- [ ] API integration examples added
- [ ] Changelog entry created
- [ ] Version number incremented

### Deployment

- [ ] CI/CD pipeline passes
- [ ] Validation gates pass
- [ ] Backward compatibility verified
- [ ] Rollback plan documented
- [ ] Monitoring configured

---

## Repository-Wide Validation

### Consistency Checks

- [ ] All skills follow same structure
- [ ] Naming conventions consistent
- [ ] YAML frontmatter format uniform
- [ ] Directory structure consistent
- [ ] Resource organization standardized

### Dependency Analysis

- [ ] Dependency graph generated
- [ ] No circular dependencies
- [ ] All dependencies valid
- [ ] Load order documented
- [ ] Optional vs required clear

### Performance Validation

- [ ] Token efficiency maintained
- [ ] Load times acceptable
- [ ] Memory usage reasonable
- [ ] Caching effective
- [ ] No performance regressions

### Compliance

- [ ] Anthropic Skills format followed
- [ ] License compliance verified
- [ ] Security standards met
- [ ] Privacy requirements satisfied
- [ ] Accessibility guidelines followed

---

## Continuous Improvement

### Metrics to Track

- [ ] Skill usage frequency
- [ ] User satisfaction scores
- [ ] Error rates
- [ ] Token efficiency
- [ ] Load times
- [ ] Composition patterns

### Review Schedule

- [ ] Weekly: Usage metrics
- [ ] Monthly: Quality assessment
- [ ] Quarterly: Comprehensive audit
- [ ] Annually: Major updates

### Feedback Loop

- [ ] User feedback mechanism
- [ ] Issue tracking system
- [ ] Feature request process
- [ ] Community contributions
- [ ] Regular updates

---

## Severity Levels for Issues

**Critical (Must Fix)**:

- YAML frontmatter invalid
- SKILL.md file missing
- Description > 1024 chars
- Broken resource links
- Security vulnerabilities

**Major (Should Fix)**:

- Missing required sections
- Token count > 5000 for Level 2
- Poor quality examples
- Missing documentation
- Inconsistent formatting

**Minor (Nice to Have)**:

- Typos or grammar issues
- Suboptimal organization
- Additional examples desired
- Better descriptions possible
- Improved resource references

---

## Sign-Off Requirements

**Before marking skill as complete**:

- [ ] All critical issues resolved
- [ ] All major issues resolved or documented
- [ ] Checklist completed 100%
- [ ] Tests passing
- [ ] Peer review approved
- [ ] Documentation updated

**Reviewers**:

- [ ] Technical Lead Sign-off: ________________
- [ ] Quality Assurance Sign-off: ________________
- [ ] Product Owner Sign-off: ________________

**Deployment Approval**:

- [ ] Staging deployment successful
- [ ] Production deployment approved
- [ ] Rollback plan confirmed
- [ ] Monitoring active

---

## Appendix: Validation Scripts

### Quick Validation Command

```bash
# Run all validation checks
./scripts/validate-all-skills.sh

# Validate specific skill
./scripts/validate-skill.sh coding-standards

# Generate quality report
./scripts/quality-report.sh > reports/quality-$(date +%Y%m%d).md
```

### Expected Output

```
✅ YAML Frontmatter Valid
✅ Description Length: 512/1024 chars
✅ Token Count: 3,847/5,000 tokens
✅ All Resources Exist
✅ No Broken Links
✅ Examples Valid
✅ Tests Passing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OVERALL: PASS (7/7 checks)
```

---

**Checklist Version**: 1.0.0
**Last Updated**: 2025-10-17
**Maintained By**: Standards Review Team
