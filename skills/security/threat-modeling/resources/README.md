# Threat Modeling Resources

Additional learning materials and real-world examples.

## Available Resources

### stride-examples.md

Comprehensive collection of real-world STRIDE threat examples including:

**Spoofing Examples:**

- Session hijacking via XSS
- DNS spoofing attacks
- Email spoofing for BEC

**Tampering Examples:**

- E-commerce price manipulation
- Git repository tampering
- Client-side data modification

**Repudiation Examples:**

- Missing audit logs enabling insider threats
- Email spoofing without authentication

**Information Disclosure Examples:**

- API IDOR vulnerabilities
- S3 bucket misconfigurations
- Capital One breach case study

**Denial of Service Examples:**

- Slowloris attacks
- Database resource exhaustion
- Application-layer DDoS

**Elevation of Privilege Examples:**

- SQL injection to admin access
- Container escape attacks
- Privilege escalation chains

**Additional Content:**

- Combined attack chains
- Industry-specific examples (healthcare, financial)
- Detection patterns and log analysis
- Risk assessment calculations
- Before/after mitigation metrics

## Usage

### Learning

Review examples relevant to your technology stack:

- Web applications
- APIs and microservices
- Mobile applications
- Cloud infrastructure
- Containers and orchestration

### Threat Modeling

Reference examples when:

1. Identifying threats in your system
2. Explaining threats to stakeholders
3. Estimating DREAD scores
4. Designing mitigations
5. Creating detection rules

### Security Testing

Use examples to:

- Create test cases
- Guide penetration testing
- Validate security controls
- Measure mitigation effectiveness

## Example Application

**Scenario:** You're threat modeling a web API

**Steps:**

1. Review "API IDOR" example in Information Disclosure
2. Check if your API has similar patterns
3. Apply DREAD scoring methodology from example
4. Implement suggested mitigations
5. Create detection rules based on log patterns
6. Test effectiveness with before/after metrics

## Real-World Incident References

Examples include references to:

- CVE vulnerabilities
- Public breach disclosures
- Security research publications
- OWASP findings

## Contributing

To add new examples:

1. Document real-world incident or common vulnerability
2. Include complete attack scenario
3. Provide DREAD scoring
4. List practical mitigations with NIST controls
5. Add detection patterns
6. Reference authoritative sources

## Related Skills

- [security-testing] - Test for threats
- [secure-coding] - Prevent vulnerabilities
- [vulnerability-management] - Track and remediate
