---
title: "SLSA 1.0 - Supply Chain Levels for Software Artifacts"
status: "authoritative-summary"
owner: "@williamzujkowski"
source:
  url: "https://slsa.dev/spec/v1.0/"
  retrieved: "2025-08-22"
review:
  last_reviewed: "2025-08-22"
  next_review_due: "2026-02-22"
accuracy: "verified"
---

# SLSA 1.0 - Supply Chain Levels for Software Artifacts

> **NOTE**: The SLSA v1.0 specification page is marked as "Status: Retired" as of this review. Version 1.1 is the current version. This document is maintained for historical reference and understanding of SLSA evolution. For current implementation, see [SLSA v1.1 documentation](https://slsa.dev/spec/v1.1/). Per [SLSA spec stages](https://slsa.dev/spec-stages), "Retired" indicates the specification is no longer maintained and has been rendered obsolete by a newer version.

## Overview

Supply chain Levels for Software Artifacts (SLSA, pronounced "salsa") is a security framework for ensuring the integrity of software artifacts throughout the software supply chain. The framework is designed to prevent tampering, improve integrity, and secure packages and infrastructure.

## SLSA Levels

SLSA v1.0 consists of three levels that progressively provide increased confidence in the software supply chain.

### SLSA Level 1 - Build Provenance

**Goal**: The build process produces provenance describing how the artifact was built.

**Requirements:**

- **Provenance exists**: Build MUST produce provenance in SLSA format
- **Provenance is authentic**: Provenance MUST be digitally signed
- **Provenance is complete**: Provenance MUST identify the builder and build instructions

**Benefits:**

- Basic documentation of build process
- Foundation for higher levels
- Enables downstream verification

### SLSA Level 2 - Hosted Build Platform

**Goal**: Builds run on a hosted platform that generates signed provenance.

**Requirements (includes Level 1 plus):**

- **Hosted build platform**: Build MUST run on infrastructure not controlled by the build's author
- **Signed provenance**: Platform MUST cryptographically sign the provenance
- **Provenance is service-generated**: Build service MUST generate provenance, not user-controlled process
- **Isolated builds**: Build service MUST ensure isolation between builds

**Benefits:**

- Tamper protection during build
- Increased confidence in provenance accuracy
- Protection against insider threats

### SLSA Level 3 - Hardened Builds

**Goal**: The build platform implements strong security controls to prevent tampering.

**Requirements (includes Level 2 plus):**

- **Non-falsifiable provenance**: Build platform MUST ensure provenance cannot be falsified
- **Isolated and ephemeral builds**: Each build MUST run in ephemeral, isolated environment
- **Parameterless builds**: Build definition MUST be fully specified in source
- **Hermetic builds**: All dependencies MUST be declared and immutable
- **Reproducible builds**: SHOULD be reproducible given same inputs
- **Two-party review**: All changes MUST be reviewed by trusted second party

**Benefits:**

- Strong tamper resistance
- Protection against sophisticated attacks
- High confidence in artifact integrity

## Provenance Format

SLSA provenance uses in-toto attestation format with specific predicates.

### Required Fields

```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [{
    "name": "artifact-name",
    "digest": {"sha256": "..."}
  }],
  "predicateType": "https://slsa.dev/provenance/v1",
  "predicate": {
    "buildDefinition": {
      "buildType": "...",
      "externalParameters": {...},
      "internalParameters": {...},
      "resolvedDependencies": [...]
    },
    "runDetails": {
      "builder": {
        "id": "...",
        "version": {...}
      },
      "metadata": {
        "invocationId": "...",
        "startedOn": "...",
        "finishedOn": "..."
      }
    }
  }
}
```

## Build Requirements by Level

| Requirement | Level 1 | Level 2 | Level 3 |
|------------|---------|---------|---------|
| Provenance exists | REQUIRED | REQUIRED | REQUIRED |
| Provenance signed | REQUIRED | REQUIRED | REQUIRED |
| Provenance authentic | REQUIRED | REQUIRED | REQUIRED |
| Service-generated | - | REQUIRED | REQUIRED |
| Non-falsifiable | - | - | REQUIRED |
| Isolated builds | - | REQUIRED | REQUIRED |
| Ephemeral environment | - | - | REQUIRED |
| Parameterless | - | - | REQUIRED |
| Hermetic | - | - | REQUIRED |
| Two-party review | - | - | REQUIRED |
| Reproducible | - | - | SHOULD |

## Source Requirements

### Version Control

- Source MUST be retained in version control system
- Source MUST have immutable references (tags, commits)
- Source MUST be available for verification

### Review Requirements (Level 3)

- All changes MUST undergo code review
- Review MUST be by trusted party
- Review MUST occur before integration
- Review history MUST be retained

## Implementation Guidance

Organizations MUST:

- Choose appropriate SLSA level based on risk assessment
- Implement provenance generation for all builds
- Verify provenance of consumed dependencies
- Maintain provenance throughout software lifecycle

Organizations SHOULD:

- Target SLSA Level 3 for critical software
- Automate provenance verification
- Integrate SLSA into CI/CD pipelines
- Use SLSA-compliant build platforms

## Verification Process

### Provenance Verification Steps

1. **Retrieve provenance**: Obtain attestation for artifact
2. **Verify signature**: Check cryptographic signature
3. **Check builder identity**: Verify trusted builder
4. **Validate content**: Ensure provenance matches expectations
5. **Apply policy**: Enforce organization's SLSA requirements

### Policy Examples

```yaml
# Minimum SLSA Level 2 for production
policy:
  - pattern: "prod/*"
    requirements:
      slsa_level: 2

# SLSA Level 3 for critical components  
  - pattern: "critical/*"
    requirements:
      slsa_level: 3
      builder_id: "https://github.com/slsa-framework/slsa-github-generator"
```

## Builder Requirements

### Level 1 Builders

- Generate provenance for builds
- Sign provenance statements
- Make provenance available

### Level 2 Builders

- Meet Level 1 requirements
- Run as hosted service
- Isolate individual builds
- Generate provenance in secure context

### Level 3 Builders

- Meet Level 2 requirements
- Implement non-falsifiable provenance
- Provide ephemeral, isolated environments
- Support hermetic builds
- Enable reproducible builds

## Threats Addressed

| Threat | Level 1 | Level 2 | Level 3 |
|--------|---------|---------|---------|
| Missing provenance | ✓ | ✓ | ✓ |
| Falsified provenance | Partial | ✓ | ✓ |
| Compromised build | - | Partial | ✓ |
| Compromised source | - | - | Partial |
| Compromised dependencies | - | Partial | ✓ |
| Build tampering | - | Partial | ✓ |
| Insider threats | - | Partial | ✓ |

## Ecosystem Support

### Build Platforms with SLSA Support

- GitHub Actions (via slsa-github-generator)
- Google Cloud Build
- GitLab CI (partial)
- Tekton Chains

### Package Registries

- npm (sigstore integration)
- Maven Central (planning)
- PyPI (planning)
- Container registries (via Cosign)

## Migration Path

1. **Start with Level 1**: Add basic provenance generation
2. **Move to Level 2**: Migrate to hosted build platform
3. **Achieve Level 3**: Implement full security controls
4. **Continuous improvement**: Regular assessment and updates

## References

- **Primary Source**: [SLSA v1.0 Specification](https://slsa.dev/spec/v1.0/)
- **Provenance Format**: [SLSA Provenance](https://slsa.dev/spec/v1.0/provenance)
- **Verification**: [SLSA Verification](https://slsa.dev/spec/v1.0/verification)
- **GitHub Generator**: [slsa-github-generator](https://github.com/slsa-framework/slsa-github-generator)
- **in-toto Framework**: [in-toto.io](https://in-toto.io/)
