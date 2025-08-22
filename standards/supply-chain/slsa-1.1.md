---
title: "SLSA v1.1 - Supply Chain Levels for Software Artifacts"
status: "authoritative-summary"
owner: "@williamzujkowski"
source:
  url: "https://slsa.dev/spec/v1.1/"
  retrieved: "2025-08-22"
review:
  last_reviewed: "2025-08-22"
  next_review_due: "2026-02-22"
accuracy: "verified"
---

# SLSA v1.1 - Supply Chain Levels for Software Artifacts

## Overview

SLSA v1.1 is the current approved specification for Supply chain Levels for Software Artifacts. It provides a framework for incrementally improving supply chain security through a series of levels with increasing security guarantees.

## Key Features of v1.1

### Core Specification Structure

- **Understanding SLSA**: Supply chain threats and security model
- **Core Specification**: Technical requirements for artifact production
- **Attestation Formats**: Recommended formats including provenance

### Security Levels and Tracks

- Progressive security levels with specific requirements
- Different tracks for various aspects of supply chain security
- Clear requirements for each level within each track

### What's New in v1.1 (from v1.0)

- **Attestation Format Clarification**: Schemas are informative; specification text is canonical
- **VSA Improvements**: Added verification procedure and verifier metadata
- **Refined Threat Model**: Further refinement of supply chain threat understanding
- **Digest Recommendations**: Recommended setting digest field in VSA policy object

## Implementation Requirements

### Build Track Requirements

- Each level builds upon previous level requirements
- Focus on build integrity and provenance generation
- Progressive hardening of build environments

### Source Track Requirements  

- Version control requirements
- Code review and approval processes
- Source integrity protections

## Attestation and Verification

### Provenance Attestation

- Based on in-toto attestation framework
- Describes how artifacts were produced
- Cryptographically signed by build platform

### Verification Summary Attestation (VSA)

- Documents verification outcomes
- Includes verifier metadata (new in v1.1)
- Supports policy-based verification

## Migration from v1.0

Organizations using SLSA v1.0 SHOULD:

- Review the what's new documentation
- Update attestation generation to v1.1 formats
- Implement VSA verification procedures
- Adapt to refined threat model

## References

- **Primary Source**: [SLSA v1.1 Specification](https://slsa.dev/spec/v1.1/)
- **What's New**: [SLSA v1.1 Changes](https://slsa.dev/spec/v1.1/whats-new)
- **Previous Version**: [SLSA v1.0 (Retired)](https://slsa.dev/spec/v1.0/)
- **Blog Announcement**: [SLSA v1.1 Release](https://slsa.dev/blog/2025/04/slsa-v1.1)
