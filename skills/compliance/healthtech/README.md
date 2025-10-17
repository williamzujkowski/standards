# HealthTech HIPAA Compliance Skill

**Category**: Compliance
**Difficulty**: Advanced
**Standards**: HIPAA, HITECH, HL7-v2, FHIR-R4
**Version**: 1.0.0

## Overview

Comprehensive HIPAA compliance skill covering Privacy Rule, Security Rule, Breach Notification, HITECH Act enforcement, and healthcare interoperability standards (HL7/FHIR).

## Structure

```
healthtech/
├── SKILL.md                          # Main skill content (1,108 lines)
├── README.md                         # This file
├── resources/
│   ├── hipaa-compliance-checklist.md # Complete administrative/physical/technical safeguards checklist
│   └── breach-response-playbook.md   # Step-by-step breach notification procedures with templates
├── templates/
│   ├── baa-template.md               # Business Associate Agreement legal template
│   ├── fhir-resources.json           # FHIR R4 resource examples (Patient, Observation, Encounter, etc.)
│   └── phi-encryption.py             # AES-256 encryption implementation for PHI (executable Python)
└── scripts/
    └── audit-log-analyzer.py         # HIPAA audit log analysis and compliance reporting (executable Python)
```

## Skill Levels

### Level 1: Quick Reference (~1,000 tokens)

- HIPAA Privacy Rule vs Security Rule
- PHI identification (18 HIPAA identifiers)
- BAA requirements
- Essential compliance checklist
- Penalty tiers

### Level 2: Implementation Guide (~5,200 tokens)

- **Privacy Rule**: Individual rights, minimum necessary, permitted uses/disclosures
- **Security Rule**: 18 implementation specifications
  - 9 Administrative safeguards
  - 4 Physical safeguards
  - 5 Technical safeguards
- **HL7 v2 messaging**: ADT, ORM, ORU message types with security considerations
- **FHIR R4**: RESTful API standards, SMART on FHIR security
- **Audit logging**: Required events, retention, review procedures (45 CFR 164.312(b))
- **Breach notification**: Four-factor risk assessment, notification timelines (45 CFR 164.400-414)
- **HITECH Act**: Enforcement penalties, business associate liability
- **Compliance audit preparation**: OCR audit protocol, essential documentation

### Level 3: Deep Dive Resources

- Official HHS/OCR resources
- NIST SP 800-66 Rev. 2
- HL7 International and FHIR specifications
- HITRUST, EHNAC, CHIME organizations
- Certification programs (CHPS, CHP, CIPP/US)

## Bundled Resources

### 1. HIPAA Compliance Checklist

**File**: `resources/hipaa-compliance-checklist.md`

Comprehensive checklist covering:

- Administrative safeguards (9 standards)
- Physical safeguards (4 standards)
- Technical safeguards (5 standards)
- Privacy Rule requirements
- Breach notification procedures
- HITECH Act compliance

**Usage**: Print and use for internal compliance audits, gap analysis, and audit preparation.

### 2. Business Associate Agreement Template

**File**: `templates/baa-template.md`

Legally-structured BAA template with:

- All required HIPAA provisions (45 CFR 164.314(a)(2))
- Permitted uses and disclosures
- Safeguard requirements
- Breach notification obligations
- Subcontractor requirements
- Termination and PHI return/destruction clauses
- Indemnification provisions

**Usage**: Customize with legal counsel before execution. Review all bracketed placeholders.

### 3. FHIR R4 Resource Examples

**File**: `templates/fhir-resources.json`

Production-ready FHIR R4 resources:

- **Patient**: Demographics, identifiers, contact information
- **Observation**: Lab results (glucose) with LOINC codes
- **Encounter**: Outpatient visit with participants and location
- **Condition**: Diagnosis (hypertension) with ICD-10 and SNOMED codes
- **MedicationRequest**: Prescription with RxNorm codes and dosage instructions

**Usage**: Reference for FHIR API implementation, testing, and PHI security requirements.

### 4. PHI Encryption Implementation

**File**: `templates/phi-encryption.py`

Python implementation of HIPAA-compliant PHI encryption:

- **AES-256-GCM** authenticated encryption
- Unique IV per encryption
- PBKDF2 key derivation (600,000 iterations)
- Full-record and field-level encryption
- Key export/import utilities
- Example usage with 4 scenarios

**Requirements**: `pip install cryptography`

**Usage**:

```bash
python3 templates/phi-encryption.py  # Run examples
```

**Security Notes**:

- Store keys in HSM or KMS (never hardcode)
- Rotate keys annually
- Audit all encryption/decryption operations
- Implement key versioning for rotation

### 5. Audit Log Analyzer

**File**: `scripts/audit-log-analyzer.py`

Automated HIPAA compliance analysis:

- **Detection Rules**:
  - After-hours access by non-emergency personnel
  - Bulk record access (>50 records/hour)
  - VIP patient record access
  - Geographical anomalies (multiple IPs)
  - Terminated employee activity
  - Failed login patterns (brute-force)
  - Self-access by employees
  - Audit log tampering/gaps
- **Compliance Reporting**: JSON and human-readable summary reports
- **Violation Severity**: Critical, High, Medium, Low

**Usage**:

```bash
# Generate sample audit log and analyze
python3 scripts/audit-log-analyzer.py

# Analyze your audit logs
python3 scripts/audit-log-analyzer.py
# Then modify to load your log file:
# analyzer.load_audit_log('your_audit_log.jsonl', format='json')
```

**Output**:

- `compliance_report.json`: Detailed violation data
- Console summary: Executive-level compliance report

### 6. Breach Response Playbook

**File**: `resources/breach-response-playbook.md`

Complete breach notification procedures:

- **Breach definition** and three exceptions
- **Immediate response** actions (1-hour timeline)
- **Four-factor risk assessment** framework with documentation template
- **Notification requirements** (individuals, OCR, media, business associates)
- **Notification templates**:
  - Individual notification letter
  - Media notice/press release
  - Substitute notice (homepage posting)
- **Post-breach activities**: Root cause analysis, corrective action plan
- **Common breach scenarios** with risk assessment examples:
  - Lost/stolen unencrypted device
  - Misdirected fax
  - Hacking incident with encryption
  - Insider snooping

**Usage**: Reference during actual breach incidents. Consult with legal counsel.

## Quick Start

### 1. Initial Compliance Assessment

```bash
# Print the compliance checklist
cd skills/compliance/healthtech/resources
cat hipaa-compliance-checklist.md
```

Review all sections and identify gaps in your current compliance posture.

### 2. Execute Business Associate Agreements

```bash
cd skills/compliance/healthtech/templates
cat baa-template.md
```

Customize BAA template with legal counsel and execute with all business associates.

### 3. Implement PHI Encryption

```bash
cd skills/compliance/healthtech/templates
python3 phi-encryption.py  # Review examples
```

Integrate PHI encryption into your application using the provided implementation patterns.

### 4. Enable Audit Logging

Review audit logging requirements in Level 2 of SKILL.md. Configure your systems to log:

- Authentication events (login/logout/failures)
- PHI access (views/searches/exports)
- Modifications (creates/updates/deletes)
- Administrative actions (user changes, config changes)

### 5. Analyze Audit Logs

```bash
cd skills/compliance/healthtech/scripts
python3 audit-log-analyzer.py  # Run demo with sample data
```

Schedule regular audit log analysis (weekly for high-risk systems, monthly for others).

### 6. Prepare for Breaches

```bash
cd skills/compliance/healthtech/resources
cat breach-response-playbook.md
```

Establish incident response team, review breach notification procedures, and conduct tabletop exercises.

## Legal Disclaimer

**IMPORTANT**: This skill provides educational guidance on HIPAA compliance requirements and is **not legal advice**. Healthcare organizations must consult with qualified healthcare compliance attorneys and privacy officers to ensure full regulatory compliance. HIPAA regulations are complex and fact-specific; implementation must be tailored to your organization's specific circumstances.

All templates, checklists, and tools provided are reference implementations and must be reviewed, customized, and validated by legal and compliance professionals before use in production environments.

## Compliance Standards Covered

- **HIPAA Privacy Rule** (45 CFR Part 160 and Subparts A and E of Part 164)
- **HIPAA Security Rule** (45 CFR Parts 160, 162, and 164)
- **HIPAA Breach Notification Rule** (45 CFR Part 164, Subpart D)
- **HITECH Act** (2009) - Enhanced enforcement and penalties
- **HL7 v2** - Healthcare messaging standards (ADT, ORM, ORU, SIU, DFT)
- **FHIR R4** - Fast Healthcare Interoperability Resources (RESTful APIs)
- **SMART on FHIR** - OAuth 2.0 security framework for FHIR APIs

## Related Skills

- `security/OWASP` - Web application security (complementary for healthcare apps)
- `security/NIST-CSF` - NIST Cybersecurity Framework (broader security posture)
- `governance/SOC2` - SOC 2 compliance (often pursued alongside HIPAA)
- `data-privacy/GDPR` - GDPR compliance (for international healthcare data)

## Updates and Maintenance

**Last Updated**: 2025-10-17

**Regulatory Monitoring**: HIPAA regulations are subject to updates and guidance changes. Monitor:

- HHS OCR website: <https://www.hhs.gov/ocr/privacy/>
- Federal Register for proposed rule changes
- OCR Cybersecurity Newsletter (monthly): <https://www.hhs.gov/about/agencies/asa/ocio/cybersecurity/newsletter/>

**Skill Maintenance**: Review annually for regulatory updates, penalty adjustments, and technical standards evolution.

## Support and Resources

- **HHS Office for Civil Rights**: <https://www.hhs.gov/ocr>
- **OCR Hotline**: 1-800-368-1019
- **OCR Breach Portal**: <https://ocrportal.hhs.gov/ocr/breach/>
- **HL7 International**: <https://www.hl7.org/>
- **FHIR Specification**: <https://hl7.org/fhir/R4/>

---

**Skill Progression**: Foundation (Level 1) → Implementation (Level 2) → Expertise (Level 3) → Lead organizational compliance programs
