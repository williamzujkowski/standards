# Standards Index

This index provides a comprehensive directory of all security and compliance standards documented in this repository.

## NIST Standards

### Security and Privacy Controls

- [**SP 800-53 Rev. 5**](/standards/nist/sp800-53r5.md) - Comprehensive catalog of security and privacy controls for federal systems
- **SP 800-53B** - Control baselines for Low, Moderate, and High impact systems ([CSRC](https://csrc.nist.gov/pubs/sp/800/53/b/upd1/final))

### Specialized Frameworks

- [**SP 800-171 Rev. 3**](/standards/nist/sp800-171r3.md) - Requirements for protecting Controlled Unclassified Information (CUI)
- [**SP 800-218 SSDF v1.1**](/standards/nist/sp800-218-ssdf.md) - Secure Software Development Framework practices
- [**AI RMF 1.0**](/standards/nist/ai-rmf-1.0.md) - Risk management framework for artificial intelligence systems
- [**AI RMF GenAI Profile**](/standards/nist/ai-rmf-genai-profile.md) - Specific guidance for generative AI systems

## OWASP Standards

### Web Application Security

- [**Top 10 2021**](/standards/owasp/top10-2021.md) - Most critical web application security risks
- [**API Security Top 10 2023**](/standards/owasp/api-top10-2023.md) - Critical API security risks

## Supply Chain Security

### Software Supply Chain

- [**SLSA v1.0**](/standards/supply-chain/slsa-1.0.md) - Supply chain levels framework (Retired - historical reference)
- [**SLSA v1.1**](/standards/supply-chain/slsa-1.1.md) - Current supply chain security levels specification
- [**CycloneDX SBOM**](/standards/supply-chain/cyclonedx-sbom.md) - Software Bill of Materials standard (ECMA-424)
- [**in-toto**](/standards/supply-chain/in-toto.md) - Framework for supply chain integrity and attestations

## CISA Guidance

### Security Initiatives

- [**Secure by Design**](/standards/cisa/secure-by-design.md) - Principles for building secure products by default
- [**KEV Catalog**](/standards/cisa/kev-process.md) - Known Exploited Vulnerabilities tracking and remediation

## Quick Reference

### By Compliance Domain

- **Federal Systems**: SP 800-53, SP 800-171
- **Software Development**: SP 800-218 SSDF, Secure by Design
- **Web Applications**: OWASP Top 10, OWASP API Top 10
- **Supply Chain**: SLSA, CycloneDX, in-toto
- **AI Systems**: AI RMF 1.0, GenAI Profile
- **Vulnerability Management**: CISA KEV

### By Implementation Phase

- **Design**: Secure by Design, AI RMF, SSDF
- **Development**: OWASP standards, SSDF practices
- **Build/Deploy**: SLSA levels, in-toto attestations
- **Operations**: SP 800-53 controls, KEV remediation
- **Assessment**: SP 800-171 requirements, SBOM generation

## Machine-Readable Registry

A JSON registry of all standards is available at [`/standards/registry.json`](/standards/registry.json) for programmatic access.
