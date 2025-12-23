---
name: threat-modeling
category: security
difficulty: intermediate
nist_controls:
- RA-3
- RA-5
tags:
- stride
- risk-assessment
- attack-trees
- dfd
- threat-analysis
related_skills:
- security-testing
- secure-coding
- vulnerability-management
learning_path: security
estimated_time: 4-6 hours
prerequisites:
- security-fundamentals
- architecture-basics
description: 'Ttampering:     description: Modifying data or code maliciously     targets:
  [dataintegrity, codeintegrity]     example: "Altering transaction amounts in transit"'
---


# Threat Modeling

> **Identify, prioritize, and mitigate security threats systematically using STRIDE methodology**

## Level 1: Quick Reference

### STRIDE Threat Categories

```yaml
threats:
  S_spoofing:
    description: Impersonating something or someone else
    targets: [authentication, identity]
    example: "Using stolen credentials to access system"

  T_tampering:
    description: Modifying data or code maliciously
    targets: [data_integrity, code_integrity]
    example: "Altering transaction amounts in transit"

  R_repudiation:
    description: Claiming to not have performed an action
    targets: [logging, audit_trails]
    example: "Denying fraudulent transaction was performed"

  I_information_disclosure:
    description: Exposing information to unauthorized parties
    targets: [confidentiality, data_protection]
    example: "Leaking customer PII through error messages"

  D_denial_of_service:
    description: Making system unavailable or degraded
    targets: [availability, performance]
    example: "Overwhelming API with requests"

  E_elevation_of_privilege:
    description: Gaining unauthorized higher access level
    targets: [authorization, access_control]
    example: "Exploiting bug to gain admin rights"
```

### Four Key Questions

1. **What are we building?**
   - System architecture, components, data flows
   - Trust boundaries, entry/exit points

2. **What can go wrong?**
   - Apply STRIDE to each component
   - Identify threat scenarios

3. **What should we do about it?**
   - Prioritize threats (DREAD scoring)
   - Design mitigations

4. **Did we do a good job?**
   - Review threat model coverage
   - Validate mitigations

### Essential Checklist

**Planning Phase:**

- [ ] Identify system scope and boundaries
- [ ] Document assets and data flows
- [ ] Define security objectives
- [ ] Assemble threat modeling team

**Analysis Phase:**

- [ ] Create data flow diagrams (DFD)
- [ ] Mark trust boundaries
- [ ] Apply STRIDE to each element
- [ ] Document threat scenarios
- [ ] Build attack trees

**Prioritization:**

- [ ] Score threats using DREAD
- [ ] Classify by impact and likelihood
- [ ] Map to security controls (NIST RA-3)

**Mitigation:**

- [ ] Design countermeasures
- [ ] Assign ownership and timeline
- [ ] Track implementation status
- [ ] Verify effectiveness (NIST RA-5)

**Documentation:**

- [ ] Maintain threat model repository
- [ ] Update for architecture changes
- [ ] Share findings with stakeholders
- [ ] Schedule periodic reviews

---

## Level 2:
>
> **📚 Full Examples**: See [REFERENCE.md](./REFERENCE.md) for complete code samples, detailed configurations, and production-ready implementations.

 Implementation Guide

### STRIDE Methodology

#### Systematic Threat Identification


*See [REFERENCE.md](./REFERENCE.md#example-0) for complete implementation.*


#### STRIDE-per-Element Pattern


*See [REFERENCE.md](./REFERENCE.md#example-1) for complete implementation.*


### Attack Trees

#### Building Attack Trees


*See [REFERENCE.md](./REFERENCE.md#example-2) for complete implementation.*


#### Attack Tree Template


*See [REFERENCE.md](./REFERENCE.md#example-3) for complete implementation.*


### Data Flow Diagrams (DFD)

#### DFD Notation


*See [REFERENCE.md](./REFERENCE.md#example-4) for complete implementation.*


#### Example DFD: Web Application


*See [REFERENCE.md](./REFERENCE.md#example-5) for complete implementation.*


#### DFD Analysis Checklist


*See [REFERENCE.md](./REFERENCE.md#example-6) for complete implementation.*


### Trust Boundaries

#### Identifying Trust Boundaries


*See [REFERENCE.md](./REFERENCE.md#example-7) for complete implementation.*


#### Boundary Crossing Analysis


*See [REFERENCE.md](./REFERENCE.md#example-8) for complete implementation.*


### Threat Prioritization (DREAD)

#### DREAD Scoring System


*See [REFERENCE.md](./REFERENCE.md#example-9) for complete implementation.*


#### Threat Prioritization Example


*See [REFERENCE.md](./REFERENCE.md#example-10) for complete implementation.*


### Mitigation Strategies

#### Mitigation Pattern Catalog


*See [REFERENCE.md](./REFERENCE.md#example-11) for complete implementation.*


### PASTA Methodology

#### Process for Attack Simulation and Threat Analysis


*See [REFERENCE.md](./REFERENCE.md#example-12) for complete implementation.*


### Tools

#### Microsoft Threat Modeling Tool


*See [REFERENCE.md](./REFERENCE.md#example-13) for complete implementation.*


#### Threat Modeling Workflow


*See [REFERENCE.md](./REFERENCE.md#example-14) for complete implementation.*


### NIST Integration

#### NIST RA-3: Risk Assessment


*See [REFERENCE.md](./REFERENCE.md#example-15) for complete implementation.*


#### NIST RA-5: Vulnerability Monitoring and Scanning


*See [REFERENCE.md](./REFERENCE.md#example-16) for complete implementation.*


### Practical Examples

#### Example 1: Authentication Service Threat Model


*See [REFERENCE.md](./REFERENCE.md#example-17) for complete implementation.*


#### Example 2: API Gateway Threat Model


*See [REFERENCE.md](./REFERENCE.md#example-18) for complete implementation.*


---

## Level 3: Deep Dive Resources

### Advanced Topics

- **Threat Intelligence Integration**: MITRE ATT&CK mapping, threat feeds
- **Automated Threat Modeling**: CI/CD integration, continuous threat modeling
- **Threat Model Maintenance**: Version control, change management
- **Quantitative Risk Analysis**: Monte Carlo simulations, risk metrics
- **Threat Modeling at Scale**: Enterprise architecture, microservices
- **Supply Chain Threat Modeling**: Third-party components, dependencies

### Tools & Frameworks

- **Commercial**: IriusRisk, ThreatModeler, SD Elements
- **Open Source**: OWASP Threat Dragon, PyTM, Threagile
- **Cloud-Native**: AWS Threat Composer, Azure Threat Modeling
- **Standards**: NIST SP 800-30 (Risk Assessment), ISO 27005

### References

- **OWASP Threat Modeling**: <https://owasp.org/www-community/Threat_Modeling>
- **Microsoft SDL**: <https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling>
- **NIST SP 800-30 Rev 1**: Risk Assessment Guide
- **NIST SP 800-154**: Data Integrity Guide
- **Adam Shostack's "Threat Modeling" Book**: Industry standard reference
- **MITRE ATT&CK**: <https://attack.mitre.org>

### Community

- **OWASP Threat Modeling Project**: Resources, templates, guidance
- **Threat Modeling Slack**: Community discussions
- **Security BSides**: Local threat modeling workshops

## Examples

### Basic Usage

```python
// TODO: Add basic example for threat-modeling
// This example demonstrates core functionality
```

### Advanced Usage

```python
// TODO: Add advanced example for threat-modeling
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how threat-modeling
// works with other systems and services
```

See `examples/threat-modeling/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Common development tools and frameworks
- **Prerequisites**: Basic understanding of general concepts

### Downstream Consumers

- **Applications**: Production systems requiring threat-modeling functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- See other skills in this category

### Common Integration Patterns

1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points

## Common Pitfalls

### Pitfall 1: Insufficient Testing

**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:

- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration

**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:

- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices

**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:

- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**

- Follow established patterns and conventions for threat-modeling
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

---

**Next Steps:**

1. Review bundled templates in `templates/`
2. Use `stride-template.md` for your first threat model
3. Generate DFDs with `data-flow-diagram.md`
4. Run `threat-report-generator.py` to create reports
5. Study real-world examples in `resources/stride-examples.md`

**Related Skills:** [security-testing] [secure-coding] [vulnerability-management]
