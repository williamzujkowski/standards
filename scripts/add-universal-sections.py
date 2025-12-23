#!/usr/bin/env python3
"""Add universal sections (Examples, Integration Points, Common Pitfalls) to all skills."""

import os
import re
from pathlib import Path
from typing import Dict, Tuple

# Skill-specific content mappings
SKILL_CONTEXTS = {
    "authentication": {
        "category": "security",
        "tools": ["OAuth2", "JWT", "TOTP", "WebAuthn"],
        "related": ["authorization", "api-security", "secrets-management"],
    },
    "authorization": {
        "category": "security",
        "tools": ["RBAC", "ABAC", "ACL", "Policy engines"],
        "related": ["authentication", "api-security"],
    },
    "unit-testing": {
        "category": "testing",
        "tools": ["pytest", "Jest", "Go test", "unittest"],
        "related": ["integration-testing", "e2e-testing", "ci-cd"],
    },
    "ci-cd": {
        "category": "devops",
        "tools": ["GitHub Actions", "GitLab CI", "Jenkins", "CircleCI"],
        "related": ["infrastructure-as-code", "monitoring-observability"],
    },
    "kubernetes": {
        "category": "cloud-native",
        "tools": ["kubectl", "helm", "kustomize"],
        "related": ["containers", "service-mesh", "monitoring-observability"],
    },
    "react": {
        "category": "frontend",
        "tools": ["React", "Redux", "React Router", "Jest"],
        "related": ["typescript", "unit-testing", "e2e-testing"],
    },
    "sql": {
        "category": "database",
        "tools": ["PostgreSQL", "MySQL", "SQLite"],
        "related": ["nosql", "advanced-optimization"],
    },
    "graphql": {
        "category": "api",
        "tools": ["Apollo Server", "GraphQL Yoga", "Hasura"],
        "related": ["authentication", "authorization", "api-security"],
    },
    "secrets-management": {
        "category": "security",
        "tools": ["HashiCorp Vault", "AWS Secrets Manager", "Azure Key Vault"],
        "related": ["authentication", "ci-cd", "kubernetes"],
    },
}


def generate_examples_section(skill_name: str, skill_path: str) -> str:
    """Generate skill-specific Examples section."""
    # Extract language from path or content
    lang = "python"  # Default
    if "javascript" in skill_path or "typescript" in skill_path or "react" in skill_path:
        lang = "javascript"
    elif "go" in skill_path:
        lang = "go"
    elif "rust" in skill_path:
        lang = "rust"

    return f"""## Examples

### Basic Usage

```{lang}
// TODO: Add basic example for {skill_name}
// This example demonstrates core functionality
```

### Advanced Usage

```{lang}
// TODO: Add advanced example for {skill_name}
// This example shows production-ready patterns
```

### Integration Example

```{lang}
// TODO: Add integration example showing how {skill_name}
// works with other systems and services
```

See `examples/{skill_name}/` for complete working examples.
"""


def generate_integration_points_section(skill_name: str, context: Dict) -> str:
    """Generate skill-specific Integration Points section."""
    tools = ", ".join(context.get("tools", []))
    related = context.get("related", [])

    related_links = "\n".join([f"- [{r.replace('-', ' ').title()}](../../{r}/SKILL.md)" for r in related])

    return f"""## Integration Points

This skill integrates with:

### Upstream Dependencies
- **Tools**: {tools if tools else "Common development tools and frameworks"}
- **Prerequisites**: Basic understanding of {context.get('category', 'software development')} concepts

### Downstream Consumers
- **Applications**: Production systems requiring {skill_name} functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills
{related_links if related_links else "- See other skills in this category"}

### Common Integration Patterns
1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points
"""


def generate_common_pitfalls_section(skill_name: str) -> str:
    """Generate Common Pitfalls section template."""
    return f"""## Common Pitfalls

### Pitfall 1: Insufficient Testing
**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:
- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration
**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:
- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices
**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:
- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**
- Follow established patterns and conventions for {skill_name}
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts
"""


def check_section_exists(content: str, section_name: str) -> bool:
    """Check if a section already exists in the content."""
    pattern = f"^## {section_name}$"
    return bool(re.search(pattern, content, re.MULTILINE))


def find_insertion_point(content: str) -> int:
    """Find where to insert universal sections (before Validation or at end)."""
    # Look for ## Validation section
    validation_match = re.search(r"^## Validation$", content, re.MULTILINE)
    if validation_match:
        return validation_match.start()

    # Look for final --- separator before end
    last_separator = content.rfind("\n---\n")
    if last_separator > 0:
        return last_separator + 1

    # Insert at end
    return len(content)


def process_skill(skill_path: Path) -> Tuple[bool, str]:
    """Process a single skill file to add universal sections."""
    try:
        content = skill_path.read_text()
        skill_name = skill_path.parent.name

        # Check which sections are missing
        missing_sections = []
        if not check_section_exists(content, "Examples"):
            missing_sections.append("Examples")
        if not check_section_exists(content, "Integration Points"):
            missing_sections.append("Integration Points")
        if not check_section_exists(content, "Common Pitfalls"):
            missing_sections.append("Common Pitfalls")

        if not missing_sections:
            return False, f"Skipped (already has all sections): {skill_name}"

        # Get skill context
        context = SKILL_CONTEXTS.get(skill_name, {"category": "general", "tools": [], "related": []})

        # Generate missing sections
        new_sections = []
        if "Examples" in missing_sections:
            new_sections.append(generate_examples_section(skill_name, str(skill_path)))
        if "Integration Points" in missing_sections:
            new_sections.append(generate_integration_points_section(skill_name, context))
        if "Common Pitfalls" in missing_sections:
            new_sections.append(generate_common_pitfalls_section(skill_name))

        # Find insertion point
        insertion_point = find_insertion_point(content)

        # Insert new sections
        new_content = content[:insertion_point] + "\n".join(new_sections) + "\n---\n\n" + content[insertion_point:]

        # Write back
        skill_path.write_text(new_content)

        return True, f"✓ Updated {skill_name} (added {', '.join(missing_sections)})"

    except Exception as e:
        return False, f"✗ Error processing {skill_path}: {e}"


def main():
    """Main processing function."""
    repo_root = Path(__file__).parent.parent
    skills_dir = repo_root / "skills"

    # Find all SKILL.md files
    skill_files = list(skills_dir.rglob("SKILL.md"))

    print(f"Found {len(skill_files)} skill files")
    print("Processing skills...\n")

    updated_count = 0
    skipped_count = 0
    error_count = 0

    for skill_file in sorted(skill_files):
        updated, message = process_skill(skill_file)
        print(message)

        if updated:
            updated_count += 1
        elif "Error" in message:
            error_count += 1
        else:
            skipped_count += 1

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Updated: {updated_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total: {len(skill_files)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
