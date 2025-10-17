# STRIDE Threat Model Template

## System Information

**System Name:** _[Your system name]_
**Version:** _[Version number]_
**Date:** _[Date of analysis]_
**Analyst:** _[Your name/team]_
**Status:** _[Draft / Under Review / Approved]_

## System Overview

**Purpose:** _[What does this system do?]_

**Key Assets:**
- _[List critical data, services, infrastructure]_

**Security Objectives:**
- Confidentiality: _[What must remain secret?]_
- Integrity: _[What must not be tampered with?]_
- Availability: _[What must remain accessible?]_

## System Architecture

### Components

| Component | Type | Description | Trust Level |
|-----------|------|-------------|-------------|
| _[Name]_ | _[Process/Data Store/External]_ | _[Purpose]_ | _[0-10]_ |

### Data Flow Diagram

```
[Paste or describe your DFD here]

Example:
(User) ──HTTPS──> [Web Server] ──SQL──> ||Database||
                        │
                        └──API──> [External Service]
```

### Trust Boundaries

| Boundary | Description | Crossing Points | Required Controls |
|----------|-------------|-----------------|-------------------|
| _[Name]_ | _[What separates]_ | _[Where data crosses]_ | _[Security measures]_ |

## STRIDE Analysis

### Component: _[Component Name]_

**Element Type:** _[Process / Data Store / Data Flow / External Entity]_

#### Spoofing

| ID | Threat Description | Attack Scenario | Impact | Likelihood | DREAD | Mitigation | NIST Control | Status |
|----|-------------------|-----------------|--------|------------|-------|------------|--------------|--------|
| S-001 | _[Threat]_ | _[How attacker would exploit]_ | _[H/M/L]_ | _[H/M/L]_ | _[Score]_ | _[Countermeasure]_ | _[Control ID]_ | _[Planned/Implemented/N/A]_ |

#### Tampering

| ID | Threat Description | Attack Scenario | Impact | Likelihood | DREAD | Mitigation | NIST Control | Status |
|----|-------------------|-----------------|--------|------------|-------|------------|--------------|--------|
| T-001 | _[Threat]_ | _[How attacker would exploit]_ | _[H/M/L]_ | _[H/M/L]_ | _[Score]_ | _[Countermeasure]_ | _[Control ID]_ | _[Planned/Implemented/N/A]_ |

#### Repudiation

| ID | Threat Description | Attack Scenario | Impact | Likelihood | DREAD | Mitigation | NIST Control | Status |
|----|-------------------|-----------------|--------|------------|-------|------------|--------------|--------|
| R-001 | _[Threat]_ | _[How attacker would exploit]_ | _[H/M/L]_ | _[H/M/L]_ | _[Score]_ | _[Countermeasure]_ | _[Control ID]_ | _[Planned/Implemented/N/A]_ |

#### Information Disclosure

| ID | Threat Description | Attack Scenario | Impact | Likelihood | DREAD | Mitigation | NIST Control | Status |
|----|-------------------|-----------------|--------|------------|-------|------------|--------------|--------|
| I-001 | _[Threat]_ | _[How attacker would exploit]_ | _[H/M/L]_ | _[H/M/L]_ | _[Score]_ | _[Countermeasure]_ | _[Control ID]_ | _[Planned/Implemented/N/A]_ |

#### Denial of Service

| ID | Threat Description | Attack Scenario | Impact | Likelihood | DREAD | Mitigation | NIST Control | Status |
|----|-------------------|-----------------|--------|------------|-------|------------|--------------|--------|
| D-001 | _[Threat]_ | _[How attacker would exploit]_ | _[H/M/L]_ | _[H/M/L]_ | _[Score]_ | _[Countermeasure]_ | _[Control ID]_ | _[Planned/Implemented/N/A]_ |

#### Elevation of Privilege

| ID | Threat Description | Attack Scenario | Impact | Likelihood | DREAD | Mitigation | NIST Control | Status |
|----|-------------------|-----------------|--------|------------|-------|------------|--------------|--------|
| E-001 | _[Threat]_ | _[How attacker would exploit]_ | _[H/M/L]_ | _[H/M/L]_ | _[Score]_ | _[Countermeasure]_ | _[Control ID]_ | _[Planned/Implemented/N/A]_ |

---

## Threat Summary

### Critical Threats (DREAD ≥ 7)

| ID | Category | Description | DREAD Score | Mitigation Status |
|----|----------|-------------|-------------|-------------------|
| _[ID]_ | _[STRIDE]_ | _[Brief description]_ | _[Score]_ | _[Status]_ |

### High Priority Threats (DREAD 4-6.9)

| ID | Category | Description | DREAD Score | Mitigation Status |
|----|----------|-------------|-------------|-------------------|
| _[ID]_ | _[STRIDE]_ | _[Brief description]_ | _[Score]_ | _[Status]_ |

## Risk Assessment (NIST RA-3)

**Overall Risk Level:** _[Critical / High / Medium / Low]_

**Key Findings:**
1. _[Major threat finding]_
2. _[Major threat finding]_
3. _[Major threat finding]_

**Risk Acceptance:**
- _[Which risks are accepted and why]_

## Mitigation Roadmap

### Immediate (0-30 days)

| ID | Mitigation | Owner | Target Date | NIST Control |
|----|------------|-------|-------------|--------------|
| _[ID]_ | _[Action]_ | _[Person/Team]_ | _[Date]_ | _[Control]_ |

### Short-term (1-3 months)

| ID | Mitigation | Owner | Target Date | NIST Control |
|----|------------|-------|-------------|--------------|
| _[ID]_ | _[Action]_ | _[Person/Team]_ | _[Date]_ | _[Control]_ |

### Long-term (3-12 months)

| ID | Mitigation | Owner | Target Date | NIST Control |
|----|------------|-------|-------------|--------------|
| _[ID]_ | _[Action]_ | _[Person/Team]_ | _[Date]_ | _[Control]_ |

## Assumptions and Dependencies

**Assumptions:**
- _[What we assume is true]_

**Dependencies:**
- _[What must be in place for this threat model to be valid]_

**Out of Scope:**
- _[What this threat model does not cover]_

## Review and Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Security Architect | _[Name]_ | _[Date]_ | _[Signature]_ |
| Development Lead | _[Name]_ | _[Date]_ | _[Signature]_ |
| Product Owner | _[Name]_ | _[Date]_ | _[Signature]_ |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | _[Date]_ | _[Name]_ | Initial threat model |

---

**Next Review Date:** _[Date for next threat model review]_
