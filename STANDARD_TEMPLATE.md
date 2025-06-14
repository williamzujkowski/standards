# [STANDARD_NAME] Standards

**Version:** 1.0.0
**Last Updated:** [DATE]
**Status:** Draft/Active/Deprecated
**Standard Code:** [XX] (2-4 letters for CLAUDE.md reference)

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Core Principles](#core-principles)
3. [Detailed Standards](#detailed-standards)
4. [Implementation Patterns](#implementation-patterns)
5. [Tool Recommendations](#tool-recommendations)
6. [Testing & Validation](#testing--validation)
7. [Security Considerations](#security-considerations)
8. [Performance Guidelines](#performance-guidelines)
9. [Migration Guide](#migration-guide)
10. [Implementation Checklist](#implementation-checklist)

---

## Overview

[Provide a clear, concise overview of what this standard covers and why it's important. Include the scope and target audience.]

### When to Use This Standard

- [Specific use case 1]
- [Specific use case 2]
- [Specific use case 3]

### Prerequisites

- [Required knowledge or standards]
- [Related standards that should be understood first]

---

## Core Principles

### 1. [Principle Name]

[Explain the principle and why it matters]

**Example:**
```[language]
// Good example
[code]

// Bad example
[code]
```

### 2. [Next Principle]

[Continue with 3-5 core principles]

---

## Detailed Standards

### [Category 1]

#### [REQUIRED] [Specific Standard]

[Detailed explanation of the standard]

**Implementation:**
```[language]
[code example]
```

**Configuration Example:**
```yaml
# Example configuration
[config]
```

#### [RECOMMENDED] [Another Standard]

[Explanation and examples]

### [Category 2]

[Continue with all categories]

---

## Implementation Patterns

### Pattern: [Pattern Name]

**Context:** [When to use this pattern]

**Solution:**
```[language]
[implementation code]
```

**Benefits:**
- [Benefit 1]
- [Benefit 2]

**Trade-offs:**
- [Trade-off 1]
- [Trade-off 2]

### Pattern: [Next Pattern]

[Continue with 3-5 key patterns]

---

## Tool Recommendations

### [REQUIRED] Essential Tools

| Tool | Purpose | Configuration |
|------|---------|--------------|
| [tool-name] | [what it does] | See `[config-file]` |
| [tool-name] | [what it does] | `[inline-config]` |

### [RECOMMENDED] Additional Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| [tool-name] | [what it does] | [specific scenarios] |

### Tool Configuration Examples

```toml
# pyproject.toml example
[tool.example]
setting = "value"
```

---

## Testing & Validation

### Testing Requirements

- **[REQUIRED]** [Test type 1]: [Description and target metrics]
- **[REQUIRED]** [Test type 2]: [Description and target metrics]
- **[RECOMMENDED]** [Test type 3]: [Description]

### Validation Examples

```[language]
// Example test
[test code]
```

### CI/CD Integration

```yaml
# .github/workflows/example.yml
[workflow configuration]
```

---

## Security Considerations

### [REQUIRED] Security Measures

1. **[Security Aspect]**: [How to implement]
   ```[language]
   [security code example]
   ```

2. **[Another Aspect]**: [Implementation details]

### Common Security Pitfalls

- **Pitfall**: [Description]
  **Solution**: [How to avoid]

---

## Performance Guidelines

### Performance Targets

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| [metric] | [target value] | [how to measure] |

### Optimization Strategies

1. **[Strategy Name]**
   - When to apply: [conditions]
   - Implementation: [approach]
   - Expected improvement: [metrics]

---

## Migration Guide

### Migrating from [Old Approach]

1. **Assessment Phase**
   - [Check current state]
   - [Identify gaps]

2. **Migration Steps**
   ```bash
   # Step 1: [Description]
   [commands]

   # Step 2: [Description]
   [commands]
   ```

3. **Validation**
   - [How to verify successful migration]

---

## Implementation Checklist

### Phase 1: Foundation (Week 1)
- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]

### Phase 2: Core Implementation (Week 2-3)
- [ ] [Task 4]
- [ ] [Task 5]
- [ ] [Task 6]

### Phase 3: Advanced Features (Week 4+)
- [ ] [Task 7]
- [ ] [Task 8]
- [ ] [Task 9]

### Validation Checklist
- [ ] All [REQUIRED] standards implemented
- [ ] Test coverage meets requirements
- [ ] Security measures in place
- [ ] Performance targets achieved
- [ ] Documentation updated

---

## References

- Add links to related standards here
- Include external resources and documentation
- Reference official documentation

---

## Appendix: Quick Reference

### Command Cheat Sheet
```bash
# Common commands
[command] - [description]
[command] - [description]
```

### Configuration Quick Reference
```
[KEY]: [value] - [description]
[KEY]: [value] - [description]
```

---

**Note:** This standard is a living document. Updates and improvements are welcome via pull requests to the [standards repository](https://github.com/williamzujkowski/standards).

## Related Standards

- [Knowledge Management Standards](./KNOWLEDGE_MANAGEMENT_STANDARDS.md) - Core documentation principles

- [CONTRIBUTING.md](./CONTRIBUTING.md) - How to contribute new standards
- [CLAUDE.md](./CLAUDE.md) - How standards integrate with LLMs
- [CREATING_STANDARDS_GUIDE.md](./CREATING_STANDARDS_GUIDE.md) - Guide for creating standards