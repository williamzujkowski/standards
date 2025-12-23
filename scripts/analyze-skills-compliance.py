#!/usr/bin/env python3
"""
Analyze all SKILL.md files for compliance with tiered learning standards.
Generate comprehensive report with violations and recommendations.
"""

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class SkillCompliance:
    """Compliance status for a single skill."""

    path: str
    name: str
    has_frontmatter: bool
    has_level1: bool
    has_level2: bool
    has_level3: bool
    has_examples: bool
    has_integration: bool
    has_pitfalls: bool
    total_tokens: int
    level1_tokens: int
    level2_tokens: int
    level3_tokens: int
    violations: List[str]
    missing_sections: List[str]
    token_violations: List[str]

    @property
    def compliance_score(self) -> float:
        """Calculate compliance score as percentage."""
        total_checks = 7
        passed = sum(
            [
                self.has_frontmatter,
                self.has_level1,
                self.has_level2,
                self.has_level3,
                self.has_examples,
                self.has_integration,
                self.has_pitfalls,
            ]
        )
        return (passed / total_checks) * 100

    @property
    def is_compliant(self) -> bool:
        """Check if skill meets all requirements."""
        return len(self.violations) == 0 and len(self.token_violations) == 0


def estimate_tokens(text: str) -> int:
    """Rough token estimation (words * 1.3)."""
    words = len(text.split())
    return int(words * 1.3)


def extract_section_content(content: str, header_pattern: str) -> Tuple[str, int, int]:
    """Extract content between header and next same-level header."""
    lines = content.split("\n")
    in_section = False
    section_lines = []
    start_line = 0

    for i, line in enumerate(lines):
        if re.match(header_pattern, line):
            if in_section:
                break
            in_section = True
            start_line = i
            continue

        if in_section:
            # Stop at next same-level or higher header
            if re.match(r"^#{1,2}\s+", line) and not re.match(r"^###", line):
                break
            section_lines.append(line)

    content = "\n".join(section_lines).strip()
    return content, start_line, estimate_tokens(content)


def analyze_skill(skill_path: Path) -> SkillCompliance:
    """Analyze a single SKILL.md file for compliance."""
    content = skill_path.read_text(encoding="utf-8")
    rel_path = str(skill_path.relative_to(Path("/home/william/git/standards")))
    skill_name = skill_path.parent.name

    violations = []
    missing_sections = []
    token_violations = []

    # Check frontmatter
    has_frontmatter = content.startswith("---")
    if not has_frontmatter:
        violations.append("Missing YAML frontmatter")
        missing_sections.append("YAML frontmatter with metadata")

    # Check Level 1: Quick Start
    level1_content, _, level1_tokens = extract_section_content(content, r"^##\s+Level 1:.*Quick Start")
    has_level1 = bool(level1_content)
    if not has_level1:
        violations.append("Missing Level 1: Quick Start")
        missing_sections.append("Level 1: Quick Start (100-150 tokens)")
    elif level1_tokens < 100 or level1_tokens > 200:
        token_violations.append(f"Level 1 tokens: {level1_tokens} (expected: 100-150)")

    # Check Level 2: Implementation
    level2_content, _, level2_tokens = extract_section_content(content, r"^##\s+Level 2:.*Implementation")
    has_level2 = bool(level2_content)
    if not has_level2:
        violations.append("Missing Level 2: Implementation")
        missing_sections.append("Level 2: Implementation (1,500-2,500 tokens)")
    elif level2_tokens < 1000 or level2_tokens > 3000:
        token_violations.append(f"Level 2 tokens: {level2_tokens} (expected: 1,500-2,500)")

    # Check Level 3: Mastery
    level3_content, _, level3_tokens = extract_section_content(content, r"^##\s+Level 3:.*Mastery")
    has_level3 = bool(level3_content)
    if not has_level3:
        violations.append("Missing Level 3: Mastery")
        missing_sections.append("Level 3: Mastery (filesystem references only)")
    elif level3_tokens > 100:  # Should mostly be links
        token_violations.append(f"Level 3 tokens: {level3_tokens} (expected: <100, mostly references)")

    # Check Examples
    has_examples = bool(re.search(r"^##\s+Examples?", content, re.MULTILINE))
    if not has_examples:
        violations.append("Missing Examples section")
        missing_sections.append("Examples section")

    # Check Integration
    has_integration = bool(re.search(r"^##\s+(Integration|Integration Points|Integrations)", content, re.MULTILINE))
    if not has_integration:
        violations.append("Missing Integration section")
        missing_sections.append("Integration points section")

    # Check Pitfalls
    has_pitfalls = bool(re.search(r"^##\s+(Common Pitfalls|Pitfalls|Common Issues)", content, re.MULTILINE))
    if not has_pitfalls:
        violations.append("Missing Common Pitfalls section")
        missing_sections.append("Common pitfalls section")

    total_tokens = estimate_tokens(content)

    return SkillCompliance(
        path=rel_path,
        name=skill_name,
        has_frontmatter=has_frontmatter,
        has_level1=has_level1,
        has_level2=has_level2,
        has_level3=has_level3,
        has_examples=has_examples,
        has_integration=has_integration,
        has_pitfalls=has_pitfalls,
        total_tokens=total_tokens,
        level1_tokens=level1_tokens,
        level2_tokens=level2_tokens,
        level3_tokens=level3_tokens,
        violations=violations,
        missing_sections=missing_sections,
        token_violations=token_violations,
    )


def generate_report(compliance_data: List[SkillCompliance]) -> str:
    """Generate comprehensive compliance report in Markdown."""
    total_skills = len(compliance_data)
    compliant_skills = [s for s in compliance_data if s.is_compliant]
    avg_compliance = sum(s.compliance_score for s in compliance_data) / total_skills

    # Sort by compliance score (worst first)
    compliance_data.sort(key=lambda x: (x.compliance_score, x.name))

    # Identify large skills
    large_skills = [s for s in compliance_data if s.total_tokens > 1500]

    # Count missing sections
    section_counts: Dict[str, int] = {}
    for skill in compliance_data:
        for section in skill.missing_sections:
            section_counts[section] = section_counts.get(section, 0) + 1

    report = f"""# Skills Compliance Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

- **Total Skills:** {total_skills}
- **Fully Compliant:** {len(compliant_skills)} ({len(compliant_skills)/total_skills*100:.1f}%)
- **Average Compliance:** {avg_compliance:.1f}%
- **Skills Needing Attention:** {total_skills - len(compliant_skills)}

## Compliance Gates

### ✅ PASSED
- Total skills analyzed: {total_skills}

### ⚠️  NEEDS ATTENTION
- **{total_skills - len(compliant_skills)} skills** below 100% compliance
- **{len(large_skills)} skills** exceed recommended token budget (>1,500 tokens)

## Overall Statistics

### Missing Sections (Most Common)
"""

    for section, count in sorted(section_counts.items(), key=lambda x: x[1], reverse=True):
        pct = (count / total_skills) * 100
        report += f"- **{section}**: {count} skills ({pct:.1f}%)\n"

    report += """
### Compliance Distribution

| Score Range | Count | Percentage |
|-------------|-------|------------|
"""

    ranges = [("100%", 100, 100), ("80-99%", 80, 99), ("60-79%", 60, 79), ("40-59%", 40, 59), ("<40%", 0, 39)]

    for label, min_score, max_score in ranges:
        count = len([s for s in compliance_data if min_score <= s.compliance_score <= max_score])
        pct = (count / total_skills) * 100 if total_skills > 0 else 0
        report += f"| {label} | {count} | {pct:.1f}% |\n"

    # Large skills section
    report += f"""
## Token Budget Violations

**{len(large_skills)} skills** exceed 1,500 token budget:

| Skill | Total Tokens | L1 Tokens | L2 Tokens | L3 Tokens |
|-------|--------------|-----------|-----------|-----------|
"""

    for skill in sorted(large_skills, key=lambda x: x.total_tokens, reverse=True)[:10]:
        report += f"| {skill.name} | {skill.total_tokens} | {skill.level1_tokens} | {skill.level2_tokens} | {skill.level3_tokens} |\n"

    # Detailed skill analysis
    report += """
## Detailed Skill Analysis

### Critical Priority (Compliance < 60%)

"""

    critical = [s for s in compliance_data if s.compliance_score < 60]
    if critical:
        for skill in critical:
            report += f"""#### {skill.name} ({skill.compliance_score:.0f}% compliant)

**Path:** `{skill.path}`

**Missing Sections:**
"""
            for section in skill.missing_sections:
                report += f"- {section}\n"

            if skill.token_violations:
                report += "\n**Token Violations:**\n"
                for violation in skill.token_violations:
                    report += f"- {violation}\n"

            report += "\n"
    else:
        report += "*No critical priority skills*\n\n"

    report += """### High Priority (Compliance 60-79%)

"""

    high = [s for s in compliance_data if 60 <= s.compliance_score < 80]
    if high:
        for skill in high:
            report += f"""#### {skill.name} ({skill.compliance_score:.0f}% compliant)

**Path:** `{skill.path}`

**Missing Sections:**
"""
            for section in skill.missing_sections:
                report += f"- {section}\n"

            if skill.token_violations:
                report += "\n**Token Violations:**\n"
                for violation in skill.token_violations:
                    report += f"- {violation}\n"

            report += "\n"
    else:
        report += "*No high priority skills*\n\n"

    report += """### Medium Priority (Compliance 80-99%)

"""

    medium = [s for s in compliance_data if 80 <= s.compliance_score < 100]
    if medium:
        for skill in medium:
            report += (
                f"- **{skill.name}** ({skill.compliance_score:.0f}%): Missing {', '.join(skill.missing_sections[:2])}"
            )
            if len(skill.missing_sections) > 2:
                report += f" and {len(skill.missing_sections) - 2} more"
            report += "\n"
    else:
        report += "*No medium priority skills*\n"

    report += """
### Fully Compliant ✅

"""

    if compliant_skills:
        for skill in sorted(compliant_skills, key=lambda x: x.name):
            report += f"- {skill.name}\n"
    else:
        report += "*No fully compliant skills yet*\n"

    # Templates section
    report += r"""
## Template Sections for Common Missing Content

### YAML Frontmatter Template

```yaml
---
skill_id: "category/skill-name"
version: "1.0.0"
category: "category-name"
complexity: "intermediate"  # beginner | intermediate | advanced
prerequisites:
  - "prerequisite-skill-1"
  - "prerequisite-skill-2"
estimated_time: "4-6 hours"
standards_alignment:
  - "standard-code-1"
  - "standard-code-2"
---
```

### Level 1: Quick Start Template

```markdown
## Level 1: Quick Start

**Target Audience:** Developers who need immediate, practical guidance.
**Token Budget:** 100-150 tokens

### What You'll Learn
- Core concept in one sentence
- Primary use case
- Key benefit

### Essential Commands
\`\`\`bash
# Critical command with brief explanation
command --flag value
\`\`\`

### When to Use
Brief decision criteria (2-3 sentences).
```

### Level 2: Implementation Template

```markdown
## Level 2: Implementation

**Target Audience:** Teams implementing in production.
**Token Budget:** 1,500-2,500 tokens

### Architecture Overview
High-level system design and component interaction.

### Implementation Steps

1. **Step One: Setup**
   - Configuration details
   - Environment preparation

2. **Step Two: Core Implementation**
   - Key code patterns
   - Best practices

3. **Step Three: Integration**
   - Connection points
   - API contracts

### Configuration Examples
\`\`\`yaml
# Production-ready configuration
key: value
\`\`\`

### Testing Strategy
- Unit test approach
- Integration test patterns
- Validation criteria
```

### Level 3: Mastery Template

```markdown
## Level 3: Mastery

**Target Audience:** Architects and specialists.
**Token Budget:** 0 inline tokens (references only)

For advanced topics, refer to:
- [Advanced Pattern Guide](./advanced/patterns.md)
- [Performance Optimization](./advanced/optimization.md)
- [Security Hardening](./advanced/security.md)
- [Troubleshooting Guide](./advanced/troubleshooting.md)
- [Case Studies](./case-studies/)
```

### Examples Section Template

```markdown
## Examples

### Basic Example
\`\`\`language
// Minimal working example
code here
\`\`\`

### Production Example
\`\`\`language
// Real-world implementation
code here
\`\`\`

### Integration Example
\`\`\`language
// How it connects to other systems
code here
\`\`\`
```

### Integration Points Template

```markdown
## Integration Points

### Upstream Dependencies
- **Service/Tool A**: Authentication and authorization
- **Service/Tool B**: Data persistence

### Downstream Consumers
- **Service/Tool C**: API client
- **Service/Tool D**: Event subscriber

### Related Skills
- [Related Skill 1](../category/skill1/SKILL.md)
- [Related Skill 2](../category/skill2/SKILL.md)
```

### Common Pitfalls Template

```markdown
## Common Pitfalls

### Pitfall 1: Issue Name
**Problem:** What goes wrong
**Solution:** How to fix it
**Prevention:** How to avoid it

### Pitfall 2: Issue Name
**Problem:** What goes wrong
**Solution:** How to fix it
**Prevention:** How to avoid it

### Pitfall 3: Issue Name
**Problem:** What goes wrong
**Solution:** How to fix it
**Prevention:** How to avoid it
```

## Recommended Remediation Order

1. **Phase 1: Critical (< 60% compliance)** - {len(critical)} skills
   - Fix all missing required sections
   - Add minimal frontmatter
   - Create basic Level 1-3 structure

2. **Phase 2: High Priority (60-79%)** - {len(high)} skills
   - Complete missing sections
   - Adjust token budgets
   - Add examples and integration points

3. **Phase 3: Medium Priority (80-99%)** - {len(medium)} skills
   - Polish remaining gaps
   - Refine token allocations
   - Enhance cross-references

4. **Phase 4: Token Budget Optimization** - {len(large_skills)} skills
   - Extract large Level 2 content to separate files
   - Move advanced content to Level 3 references
   - Create dedicated advanced/ subdirectories

## Success Metrics

- **Target Compliance:** 100%
- **Current Compliance:** {avg_compliance:.1f}%
- **Gap:** {100 - avg_compliance:.1f}%

**Estimated Effort:** {(total_skills - len(compliant_skills)) * 2} - {(total_skills - len(compliant_skills)) * 4} hours

## Next Steps

1. Review this report with development team
2. Assign skills to remediation agents based on priority
3. Use templates above for missing sections
4. Run validation script after fixes: `python3 scripts/validate-skills.py`
5. Iterate until 100% compliance achieved

---

*This report identifies issues only. Actual fixes will be implemented by remediation agents.*
"""

    return report


def main():
    """Main analysis function."""
    skills_dir = Path("/home/william/git/standards/skills")
    skill_files = list(skills_dir.glob("*/*/SKILL.md"))
    skill_files.extend(list(skills_dir.glob("*/SKILL.md")))

    print(f"Analyzing {len(skill_files)} SKILL.md files...")

    compliance_data = []
    for skill_file in skill_files:
        print(f"  Analyzing {skill_file.relative_to(skills_dir.parent)}...")
        result = analyze_skill(skill_file)
        compliance_data.append(result)

    # Generate report
    report = generate_report(compliance_data)

    # Save report
    report_path = Path("/home/william/git/standards/reports/generated/skills-compliance-report.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    # Save JSON data
    json_path = Path("/home/william/git/standards/reports/generated/skills-compliance-data.json")
    json_data = {
        "generated": datetime.now().isoformat(),
        "total_skills": len(compliance_data),
        "compliant_skills": len([s for s in compliance_data if s.is_compliant]),
        "average_compliance": sum(s.compliance_score for s in compliance_data) / len(compliance_data),
        "skills": [asdict(s) for s in compliance_data],
    }
    json_path.write_text(json.dumps(json_data, indent=2), encoding="utf-8")

    print("\n✅ Analysis complete!")
    print(f"   Report: {report_path}")
    print(f"   Data: {json_path}")
    print("\n📊 Summary:")
    print(f"   Total skills: {len(compliance_data)}")
    print(f"   Compliant: {len([s for s in compliance_data if s.is_compliant])}")
    print(f"   Average compliance: {json_data['average_compliance']:.1f}%")


if __name__ == "__main__":
    main()
