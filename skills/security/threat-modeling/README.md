# Threat Modeling Skill

> Systematically identify, prioritize, and mitigate security threats using STRIDE methodology

## Overview

This skill teaches comprehensive threat modeling for software systems, focusing on:

- STRIDE threat categorization
- Attack tree analysis
- Data flow diagrams (DFD)
- DREAD prioritization
- Mitigation planning
- NIST control integration (RA-3, RA-5)

## Skill Details

- **Category:** Security
- **Difficulty:** Intermediate
- **Learning Time:** 4-6 hours
- **Prerequisites:** security-fundamentals, architecture-basics

## Contents

### Main Skill Document

**`SKILL.md`** - Complete learning path with three levels:

1. **Level 1:** Quick reference (600-800 tokens)
   - STRIDE categories
   - Four key questions
   - Essential checklist
2. **Level 2:** Implementation guide (3000-4500 tokens)
   - Detailed STRIDE methodology
   - Attack trees
   - DFD creation
   - Trust boundaries
   - DREAD scoring
   - Mitigation strategies
   - PASTA methodology
   - Tools overview
   - NIST integration
3. **Level 3:** Deep dive resources

### Templates (`templates/`)

Ready-to-use templates for threat modeling:

- **`stride-template.md`** - Complete STRIDE threat model template
- **`data-flow-diagram.md`** - DFD creation with examples
- **`threat-scenario.md`** - Attack tree and scenario template
- **`mitigation-plan.md`** - Mitigation tracking and planning

### Scripts (`scripts/`)

Automation tools:

- **`threat-report-generator.py`** - Generate reports from YAML threat definitions

### Resources (`resources/`)

Learning materials:

- **`stride-examples.md`** - 15+ real-world STRIDE examples with:
  - Actual security incidents
  - DREAD scoring
  - Practical mitigations
  - Detection patterns

## Quick Start

### 1. Learn the Basics

```bash
# Read the quick reference (5-10 minutes)
head -n 200 SKILL.md
```

### 2. Create Your First Threat Model

```bash
# Copy STRIDE template
cp templates/stride-template.md my-threat-model.md

# Fill in your system details
# Apply STRIDE to each component
```

### 3. Build a Data Flow Diagram

```bash
# Use DFD template
cp templates/data-flow-diagram.md my-dfd.md

# Document your architecture
# Mark trust boundaries
# Identify data flows
```

### 4. Document Attack Scenarios

```bash
# Use scenario template
cp templates/threat-scenario.md my-scenario.md

# Build attack trees
# Calculate DREAD scores
# Plan mitigations
```

### 5. Generate Reports

```bash
# Install PyYAML
pip install pyyaml

# Create threat definitions (YAML)
cat > threats.yaml << 'EOF'
system_name: "My System"
version: "1.0"
date: "2025-10-17"
analyst: "Security Team"
threats:
  - id: "THREAT-001"
    category: "Spoofing"
    description: "JWT token theft"
    # ... more details
EOF

# Generate report
python scripts/threat-report-generator.py -i threats.yaml -o report.md
```

## Learning Path

### For Beginners

1. Read SKILL.md Level 1 (Quick Reference)
2. Study real-world examples in resources/stride-examples.md
3. Practice with stride-template.md on a simple system
4. Review example threat models

### For Intermediate

1. Read SKILL.md Level 2 (Implementation Guide)
2. Create DFDs with data-flow-diagram.md
3. Build attack trees with threat-scenario.md
4. Apply DREAD scoring methodology
5. Generate automated reports

### For Advanced

1. Read SKILL.md Level 3 (Deep Dive)
2. Implement PASTA methodology
3. Integrate with NIST framework (RA-3, RA-5)
4. Customize threat-report-generator.py
5. Conduct threat modeling workshops

## Use Cases

### Web Applications

- Identify authentication threats
- Map API attack surfaces
- Analyze session management
- Review data protection

### Cloud Infrastructure

- S3 bucket security
- IAM privilege escalation
- Container escape scenarios
- Network segmentation

### Mobile Applications

- Client-side tampering
- Certificate pinning
- Data storage security
- API authentication

### Microservices

- Service-to-service auth
- API gateway threats
- Data flow between services
- Distributed logging

## Integration

### With Development Workflow

```yaml
# .github/workflows/threat-model.yml
name: Threat Model Review
on:
  pull_request:
    paths:
      - 'architecture/**'
      - 'threat-model.yaml'
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate threat report
        run: python scripts/threat-report-generator.py -i threat-model.yaml
      - name: Check for critical threats
        run: |
          if grep -q "Critical" threat-report.md; then
            echo "Review required for critical threats"
          fi
```

### With Security Testing

- Use threat model to guide pen testing
- Create test cases from attack scenarios
- Validate mitigations with security scans
- Track vulnerability-to-threat mapping

### With Risk Management

- Link threats to risk register
- Map NIST controls to mitigations
- Track mitigation effectiveness
- Report to stakeholders

## NIST Controls

This skill addresses:

- **RA-3:** Risk Assessment - Systematic threat identification
- **RA-5:** Vulnerability Monitoring - Threat-informed scanning

## Metrics

Track your threat modeling effectiveness:

- Threats identified per system
- Average DREAD score
- Mitigation completion rate
- Time to detect new threats
- Coverage of attack surface

## Best Practices

1. **Start Early:** Threat model during design phase
2. **Iterate:** Update as architecture changes
3. **Collaborate:** Involve developers, architects, security
4. **Prioritize:** Focus on high DREAD threats first
5. **Validate:** Test threat scenarios with pen testing
6. **Document:** Maintain in version control
7. **Automate:** Generate reports, integrate with CI/CD

## Tools Mentioned

- Microsoft Threat Modeling Tool
- OWASP Threat Dragon
- PyTM (Python threat modeling)
- Custom: threat-report-generator.py

## Related Skills

- `security-fundamentals` - Security basics
- `secure-coding` - Prevent vulnerabilities
- `security-testing` - Test for threats
- `vulnerability-management` - Track and remediate
- `architecture-design` - System design

## Support

- Review examples in `resources/stride-examples.md`
- Use templates in `templates/`
- Generate reports with `scripts/threat-report-generator.py`
- Refer to SKILL.md for detailed methodology

## License

Part of the Standards Repository project.
