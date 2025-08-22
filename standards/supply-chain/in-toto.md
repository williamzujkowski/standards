---
title: "in-toto - Supply Chain Security Framework"
status: "authoritative-summary"
owner: "@williamzujkowski"
source:
  url: "https://in-toto.io/docs/specs/"
  retrieved: "2025-08-22"
review:
  last_reviewed: "2025-08-22"
  next_review_due: "2026-02-22"
accuracy: "verified"
---

# in-toto - Supply Chain Security Framework

## Overview

in-toto is a framework designed to secure software supply chains by providing authentication, integrity, and auditability for software artifacts and the processes that produce them.

## Core Specifications

### in-toto Specification v1.0

- **Purpose**: Define supply chain layout and verification
- **Components**: Layout files describing expected steps and link metadata
- **Status**: Stable version for production use

### in-toto Attestation Framework v1.0

- **Purpose**: Express software supply chain claims in a standard format
- **Structure**: Statement/predicate model for attestations
- **Integration**: Will be incorporated into future in-toto specification

## Key Components

### Statement Format

- Envelope for cryptographically binding subjects to predicates
- Supports multiple signature schemes
- Enables cross-system interoperability

### Predicate Types

- **Provenance**: How an artifact was produced (used by SLSA)
- **Link**: Traditional in-toto link metadata
- **SPDX**: Software bill of materials information
- **Custom**: Organization-specific predicates

### Layout and Verification

- Define expected supply chain steps
- Specify authorized functionaries
- Set artifact flow rules
- Enable end-to-end verification

## Relationship with SLSA

### SLSA Provenance as in-toto Predicate

- SLSA provenance follows in-toto attestation format
- Uses in-toto statement structure
- Enables verification using in-toto tooling

### Integration Points

- Common attestation format
- Shared verification model
- Compatible signature schemes

## Implementation Requirements

Organizations MUST:

- Define supply chain layout
- Generate link metadata for each step
- Sign attestations cryptographically
- Verify complete supply chain before use

Organizations SHOULD:

- Use in-toto attestation format for new systems
- Integrate with existing CI/CD pipelines
- Automate verification processes
- Store attestations with artifacts

## References

- **Specifications Index**: [in-toto Specs](https://in-toto.io/docs/specs/)
- **Attestation Framework**: [in-toto Attestation](https://github.com/in-toto/attestation)
- **Main Specification**: [in-toto v1.0](https://github.com/in-toto/docs/blob/v1.0/in-toto-spec.md)
- **ITE-5 (Attestation Layers)**: [ITE-5 Specification](https://github.com/in-toto/ITE/tree/master/ITE/5)
