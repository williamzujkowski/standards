---
title: "CISA Known Exploited Vulnerabilities (KEV) Catalog"
status: "authoritative-summary"
owner: "@williamzujkowski"
source:
  url: "https://www.cisa.gov/known-exploited-vulnerabilities-catalog"
  retrieved: "2025-08-22"
review:
  last_reviewed: "2025-08-22"
  next_review_due: "2026-02-22"
accuracy: "verified"
---

# CISA Known Exploited Vulnerabilities (KEV) Catalog

## Overview

The CISA Known Exploited Vulnerabilities (KEV) Catalog is a living list of vulnerabilities that are being actively exploited in the wild. Federal Civilian Executive Branch (FCEB) agencies are required to remediate KEV vulnerabilities within specified timeframes.

## KEV Inclusion Criteria

For a vulnerability to be added to the KEV catalog, it MUST meet ALL of the following criteria:

1. **Assigned CVE ID**: The vulnerability has a Common Vulnerabilities and Exposures (CVE) ID
2. **Active Exploitation**: There is reliable evidence the vulnerability is being actively exploited
3. **Clear Remediation**: There is a clear remediation action available (patch, mitigation, or workaround)

## Remediation Requirements

### Federal Agencies (Binding Operational Directive 22-01)

Federal Civilian Executive Branch agencies MUST:

- Remediate KEV vulnerabilities by the due date specified in the catalog
- Review the KEV catalog within 24 hours of publication
- Maintain automated vulnerability scanning capabilities
- Report compliance status as required

### Critical Infrastructure and Private Sector

Organizations SHOULD:

- Prioritize KEV vulnerabilities for immediate remediation
- Use the KEV catalog to inform patch management
- Monitor the KEV catalog regularly
- Integrate KEV data into vulnerability management programs

## KEV Catalog Data Fields

Each KEV entry includes:

- **CVE ID**: Unique vulnerability identifier
- **Vendor/Project**: Affected vendor or project
- **Product**: Affected product name
- **Vulnerability Name**: Brief description
- **Date Added**: When added to KEV catalog
- **Short Description**: Summary of vulnerability
- **Required Action**: Specific remediation required
- **Due Date**: Remediation deadline (for federal agencies)

## Using the KEV Catalog

### Integration Methods

- Direct catalog download (CSV/JSON)
- API access for automation
- RSS feed for updates
- Email subscription alerts

### Prioritization Strategy

1. Check KEV catalog FIRST
2. Remediate KEV vulnerabilities immediately
3. Use for risk-based decision making
4. Track remediation completion

## Implementation Requirements

Organizations MUST:

- Monitor the KEV catalog regularly
- Remediate KEV vulnerabilities within organizational SLAs
- Track KEV remediation status
- Report on KEV compliance

Organizations SHOULD:

- Automate KEV catalog consumption
- Integrate with vulnerability scanners
- Alert on new KEV additions
- Measure mean time to remediation

## References

- **Primary Source**: [CISA KEV Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- **BOD 22-01**: [Reducing the Significant Risk of Known Exploited Vulnerabilities](https://www.cisa.gov/binding-operational-directive-22-01)
- **KEV Methodology**: [Known Exploited Vulnerabilities](https://www.cisa.gov/known-exploited-vulnerabilities)
