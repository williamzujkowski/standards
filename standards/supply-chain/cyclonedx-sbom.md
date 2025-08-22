---
title: "CycloneDX SBOM - ECMA-424"
status: "authoritative-summary"
owner: "@williamzujkowski"
source:
  url: "https://ecma-international.org/publications-and-standards/standards/ecma-424/"
  retrieved: "2025-08-22"
review:
  last_reviewed: "2025-08-22"
  next_review_due: "2026-02-22"
accuracy: "verified"
---

# CycloneDX SBOM - ECMA-424

## Overview

CycloneDX is a modern standard for Software Bill of Materials (SBOM), standardized as ECMA-424 (1st edition, June 2024). CycloneDX v1.6 is a lightweight SBOM specification designed for use in application security contexts and supply chain component analysis.

## Key Features

- **Full-Stack Bill of Materials**: Supports software, hardware, services, and vulnerabilities
- **Machine and Human Readable**: JSON, XML, and Protocol Buffers formats
- **Vulnerability Exploitation Exchange (VEX)**: Native support for vulnerability disclosure
- **ECMA Standard**: Internationally recognized as ECMA-424 (1st edition, June 2024)

## Core Components

### Component Information

- Name, version, and supplier
- License and copyright
- Hashes for integrity verification
- Package URL (purl) for identification

### Dependency Graph

- Hierarchical component relationships
- Direct and transitive dependencies
- Dependency resolution metadata

### Vulnerability Information

- VEX (Vulnerability Exploitability eXchange)
- Security advisories
- Patch and remediation data

## Implementation Requirements

Organizations MUST:

- Generate SBOMs for all software releases
- Include all direct and transitive dependencies
- Provide accurate license information
- Update SBOMs when components change

Organizations SHOULD:

- Automate SBOM generation in CI/CD
- Validate SBOM completeness
- Sign SBOMs for authenticity
- Store SBOMs with artifacts

## References

- **Primary Standard**: [ECMA-424 (1st edition, June 2024)](https://ecma-international.org/publications-and-standards/standards/ecma-424/)
- **CycloneDX Project**: [cyclonedx.org](https://cyclonedx.org/)
- **Specification**: [CycloneDX v1.6](https://cyclonedx.org/specification/)
