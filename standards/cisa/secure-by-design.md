---
title: "CISA Secure by Design Principles"
status: "authoritative-summary"
owner: "@williamzujkowski"
source:
  url: "https://www.cisa.gov/resources-tools/resources/secure-by-design"
  retrieved: "2025-08-22"
review:
  last_reviewed: "2025-08-22"
  next_review_due: "2026-02-22"
accuracy: "verified"
---

# CISA Secure by Design Principles

## Overview

CISA's Secure by Design initiative shifts security responsibility to technology manufacturers, encouraging them to build products with security as a core business requirement, not just a technical feature.

## Core Principles

### Take Ownership of Customer Security Outcomes

Manufacturers MUST:

- Build products secure by default
- Eliminate entire classes of vulnerabilities
- Provide secure configuration templates
- Make security features available at no additional charge

### Embrace Radical Transparency and Accountability

Organizations SHOULD:

- Publish vulnerability disclosure policies
- Provide Software Bills of Materials (SBOMs)
- Share aggregate security metrics
- Document security practices publicly

### Lead from the Top

Leadership MUST:

- Prioritize security in business decisions
- Allocate resources for secure development
- Create accountability for security outcomes
- Incentivize security improvements

## Secure by Default Requirements

Products MUST:

- Ship with secure configurations enabled
- Require opt-in for less secure modes
- Implement secure authentication by default
- Enable logging and security features automatically

Products MUST NOT:

- Use default passwords
- Require additional purchases for security
- Ship with known vulnerabilities
- Enable unnecessary services by default

## Key Practices

### Memory Safe Languages

- Use memory safe languages for new development
- Create roadmaps to eliminate memory unsafe code
- Measure and report memory safety progress

### Security Development Lifecycle

- Implement threat modeling
- Conduct security testing throughout development
- Perform security reviews before release
- Monitor and patch vulnerabilities post-release

### Vulnerability Management

- Establish coordinated vulnerability disclosure
- Remediate vulnerabilities within defined SLAs
- Provide security advisories and updates
- Support products throughout lifecycle

## References

- **Primary Source**: [CISA Secure by Design](https://www.cisa.gov/resources-tools/resources/secure-by-design)
- **Guidance Document**: [Secure by Design Principles (PDF)](https://www.cisa.gov/sites/default/files/2023-04/principles_approaches_for_security-by-design-default_508_0.pdf)
- **Secure by Design Pledge**: [CISA Secure by Design Pledge](https://www.cisa.gov/securebydesign/pledge)
