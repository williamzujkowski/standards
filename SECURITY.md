# Security Policy

## Supported Versions

This repository maintains standards documentation. Security updates are applied to:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| Others  | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in this repository, please report it through one of the following channels:

### For Documentation Issues

If the vulnerability relates to incorrect or misleading security guidance in our standards documentation:

1. **DO NOT** create a public issue
2. Email: security@[domain] (replace with actual domain)
3. Include:
   - Affected document and section
   - Description of the incorrect information
   - Suggested correction with authoritative source
   - Potential impact if followed

### For Code/Infrastructure Issues

If the vulnerability relates to code examples, CI/CD workflows, or infrastructure:

1. **DO NOT** create a public issue
2. Use GitHub's Security Advisory feature (if enabled)
3. Or email: security@[domain]
4. Include:
   - Affected file(s)
   - Steps to reproduce
   - Potential impact
   - Suggested fix if available

## Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 5 business days
- **Resolution Target**:
  - Critical: 7 days
  - High: 14 days
  - Medium: 30 days
  - Low: Next regular update

## Security Standards

This repository follows security standards documented within:

- NIST SP 800-53 Rev. 5 for security controls
- NIST SP 800-171 Rev. 3 for CUI protection
- OWASP Top 10 2021 for web application security
- SLSA Level 3 for supply chain security

## Verification

All security-related content in this repository:

- MUST cite authoritative sources
- MUST be reviewed quarterly
- MUST be validated against primary sources
- MUST NOT contain unverified claims

## Dependencies

We regularly scan and update dependencies:

- GitHub Actions are pinned to specific versions
- Third-party actions are reviewed before use
- Automated dependency updates via Dependabot
- Weekly security scanning via GitHub Security

## Code of Conduct

Security researchers are expected to:

- Follow responsible disclosure practices
- Allow reasonable time for patches
- Not access or modify user data
- Not perform destructive actions
- Respect rate limits and resource constraints

## Recognition

We appreciate security researchers who help improve our standards. With your permission, we will acknowledge your contribution in our updates.

## Contact

- Security Issues: security@[domain]
- General Questions: @williamzujkowski
- Emergency: Use GitHub Security Advisory

## Related Documents

- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [README.md](README.md) - Project overview
- [CLAIMS.md](CLAIMS.md) - Normative claims registry
