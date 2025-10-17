# Threat Modeling Scripts

Automation scripts for threat modeling workflows.

## Available Scripts

### threat-report-generator.py

Generate comprehensive threat model reports from YAML threat definitions.

**Features:**

- STRIDE threat analysis
- DREAD scoring and prioritization
- Mitigation tracking
- NIST control mapping
- Executive summaries
- Recommendations

**Usage:**

```bash
# Basic usage
python threat-report-generator.py --input threats.yaml --output report.md

# Generate to stdout
python threat-report-generator.py --input threats.yaml

# Summary only
python threat-report-generator.py --input threats.yaml --summary-only
```

**Input Format (threats.yaml):**

```yaml
system_name: "User Authentication Service"
version: "1.0"
date: "2025-10-17"
analyst: "Security Team"

threats:
  - id: "THREAT-001"
    category: "Spoofing"
    description: "JWT token theft and replay"
    attack_scenario: |
      1. Attacker steals JWT from local storage via XSS
      2. Uses token to impersonate user
    component: "Authentication Service"
    dread:
      damage: 8
      reproducibility: 9
      exploitability: 7
      affected_users: 8
      discoverability: 6
    mitigations:
      - control: "Use httpOnly cookies"
        nist_control: "SC-8"
        status: "Implemented"
        owner: "Backend Team"
        target_date: "2025-11-01"
    impact_confidentiality: "High"
    impact_integrity: "Medium"
    impact_availability: "Low"
```

**Output:**

- Markdown report with executive summary
- Threat breakdown by STRIDE category
- Critical and high priority threats detailed
- Mitigation status tracking
- NIST control mapping
- Recommendations

## Example Workflow

```bash
# 1. Create threat definitions
cat > my-threats.yaml << EOF
system_name: "My Application"
version: "1.0"
date: "2025-10-17"
analyst: "Me"
threats:
  # ... threat definitions
EOF

# 2. Generate report
python threat-report-generator.py -i my-threats.yaml -o threat-report.md

# 3. Review report
cat threat-report.md

# 4. Track in version control
git add my-threats.yaml threat-report.md
git commit -m "docs: add threat model"
```

## Integration with CI/CD

```yaml
# .github/workflows/threat-model.yml
name: Threat Model Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate threat report
        run: |
          python skills/security/threat-modeling/scripts/threat-report-generator.py \
            --input threat-model.yaml \
            --output threat-report.md
      - name: Check for critical threats
        run: |
          if grep -q "Critical: [1-9]" threat-report.md; then
            echo "❌ Critical threats found!"
            exit 1
          fi
```

## Requirements

- Python 3.7+
- PyYAML: `pip install pyyaml`

## Future Enhancements

- HTML output format
- JSON export
- Integration with threat modeling tools
- Automated DREAD calculation suggestions
- MITRE ATT&CK mapping
