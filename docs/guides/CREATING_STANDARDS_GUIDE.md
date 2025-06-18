# Guide to Creating New Standards

This guide helps contributors and LLMs create standards that conform to our repository's approach.

---

## 🎯 Quick Start

1. **Use the template**: Copy [STANDARD_TEMPLATE.md](STANDARD_TEMPLATE.md)
2. **Follow the structure**: Keep all sections, remove those not applicable
3. **Add metadata**: Update MANIFEST.yaml and related files
4. **Submit PR**: Include rationale for the new standard

---

## 📋 Standard Requirements

### Document Structure

Every standard MUST include:

1. **Header Metadata**
   - Version (semantic versioning)
   - Last Updated date
   - Status (Draft/Active/Deprecated)
   - Standard Code (2-4 letters for CLAUDE.md)

2. **Core Sections**
   - Overview with clear scope
   - Core principles (3-5 key concepts)
   - Detailed standards with [REQUIRED]/[RECOMMENDED] tags
   - Implementation patterns with code examples
   - Tool recommendations
   - Implementation checklist

3. **Supporting Content**
   - Testing & validation approaches
   - Security considerations
   - Performance guidelines
   - Migration guides (if replacing existing practices)

### Writing Style

- **Be Prescriptive**: Tell users exactly what to do
- **Show, Don't Just Tell**: Include code examples for every concept
- **Multi-Language**: Provide examples in Python, JavaScript/TypeScript, and Go where applicable
- **Real-World Focus**: Use practical, production-ready examples
- **Progressive Disclosure**: Start simple, add complexity gradually

### Code Examples

```python
# Good: Clear, practical example with context
class UserService:
    """Service for managing user operations."""

    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def get_user(self, user_id: str) -> User:
        """Get user by ID with proper error handling."""
        if not user_id:
            raise ValueError("User ID is required")

        user = await self._repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User {user_id} not found")

        return user
```

```python
# Bad: Too abstract, no error handling
def get_user(id):
    return db.get(id)
```

### Using [REQUIRED] and [RECOMMENDED] Tags

- **[REQUIRED]**: Must be implemented for compliance
- **[RECOMMENDED]**: Should be implemented unless there's a good reason not to

Example:
```markdown
### [REQUIRED] Error Handling

All functions must handle errors explicitly...

### [RECOMMENDED] Logging

Functions should log significant operations...
```

---

## 🔧 Integration Steps

### 1. Create Your Standard

Use [STANDARD_TEMPLATE.md](STANDARD_TEMPLATE.md) as your starting point.

### 2. Update MANIFEST.yaml

Add your standard's metadata:

```yaml
YOUR_STANDARD_CODE:
  identifier: "YSC"
  filename: "YOUR_STANDARD_NAME.md"
  sections:
    overview:
      tokens: 500
      priority: "critical"
      description: "Introduction and scope"
    core-principles:
      tokens: 800
      priority: "high"
      description: "Fundamental concepts"
    # ... more sections
  dependencies:
    requires: ["CS"]  # Standards that must be loaded first
    recommends: ["TS", "SEC"]  # Helpful companion standards
```

### 3. Update STANDARDS_INDEX.md

Add a one-line summary:

```markdown
- **YOUR_STANDARD_NAME.md (YSC)**: Brief description of what the standard covers
```

### 4. Update CLAUDE.md

Add loading patterns:

```markdown
### Natural Language Mappings
| Query | Standards Loaded | Context |
|-------|------------------|---------|
| "How do I [your domain]?" | `YSC:* + [related]` | Your context |
```

### 5. Update STANDARDS_GRAPH.md

Add relationships:

```markdown
### YOUR_STANDARD_NAME.md
- **Depends on**: CODING_STANDARDS.md (core practices)
- **Related to**: [Related standards]
- **Recommended with**: [Companion standards]
```

### 6. Update README.md

Add to the appropriate category section.

---

## 📊 Quality Checklist

Before submitting your standard:

- [ ] Follows the template structure
- [ ] Includes practical code examples
- [ ] Has clear [REQUIRED] vs [RECOMMENDED] sections
- [ ] Provides tool configurations
- [ ] Includes implementation checklist
- [ ] Updates all integration files
- [ ] Passes YAML validation
- [ ] Under 3000 lines (split if larger)

---

## 💡 Best Practices

### 1. Focus on Practical Application

```markdown
# Good: Specific, actionable
### [REQUIRED] API Response Format

All APIs must return responses in this format:
{
  "data": {...},
  "meta": {...},
  "errors": [...]
}

# Bad: Vague, theoretical
APIs should have consistent response formats.
```

### 2. Provide Multiple Implementation Options

```markdown
### Database Connection Patterns

#### Option 1: Connection Pool (Recommended)
[Code example with connection pooling]

#### Option 2: Single Connection (Simple Use Cases)
[Code example with single connection]

#### When to Use Each
- Use Option 1 when: [specific scenarios]
- Use Option 2 when: [specific scenarios]
```

### 3. Include Anti-Patterns

```markdown
### Common Mistakes

#### Anti-Pattern: Global Database Connection
```python
# DON'T DO THIS
db = connect_to_database()  # Global connection

def get_user(id):
    return db.query(...)  # Shared state issues
```

#### Better Approach: Dependency Injection
```python
# DO THIS INSTEAD
class UserService:
    def __init__(self, db_connection):
        self.db = db_connection
```
```

### 4. Link to Related Standards

Always reference related standards:

```markdown
For error handling patterns, see [CODING_STANDARDS.md](./CODING_STANDARDS.md#error-handling).

For testing these patterns, refer to [TESTING_STANDARDS.md](./docs/standards/TESTING_STANDARDS.md).
```

---

## 🤖 For LLMs Creating Standards

When creating a new standard:

1. **Analyze Existing Standards**: Review 2-3 related standards for style consistency
2. **Identify Gaps**: Ensure the new standard fills a genuine need
3. **Cross-Reference**: Link to existing standards rather than duplicating content
4. **Validate Structure**: Ensure all required sections are present
5. **Generate Examples**: Create realistic, production-ready code examples
6. **Consider Token Efficiency**: Structure content for efficient progressive loading

### Prompt Template for LLMs

```
Create a new standard for [DOMAIN] following STANDARD_TEMPLATE.md.

Context:
- Target audience: [developers/architects/teams]
- Scope: [what this covers]
- Related standards: [existing standards to reference]

Requirements:
- Include examples in Python, JavaScript/TypeScript, and Go
- Mark sections as [REQUIRED] or [RECOMMENDED]
- Provide tool configurations
- Include migration guide from [current practice]
- Add implementation checklist with time estimates

The standard should help teams [specific goal].
```

---

## 📝 Review Process

New standards go through:

1. **Technical Review**: Accuracy and completeness
2. **Style Review**: Consistency with existing standards
3. **Integration Review**: Proper updates to all required files
4. **Community Feedback**: Open for comments period

---

## 🔗 Additional Resources

- [STANDARD_TEMPLATE.md](STANDARD_TEMPLATE.md) - The template to use
- [CLAUDE.md](./docs/core/CLAUDE.md) - How standards integrate with LLMs
- [MANIFEST.yaml](./config/MANIFEST.yaml) - Metadata structure
- [Contributing Guide](./docs/core/CONTRIBUTING.md) - General contribution guidelines

---

**Remember**: Standards should be practical, prescriptive, and production-ready. They should help teams implement best practices quickly and confidently.

## Related Standards

- [Knowledge Management Standards](./docs/standards/KNOWLEDGE_MANAGEMENT_STANDARDS.md) - Architecture principles
