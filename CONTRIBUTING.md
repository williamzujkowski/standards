# Contributing to Standards Repository

Thank you for your interest in contributing to this standards repository! This document provides guidelines and instructions for contributions.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Standards for Standards](#standards-for-standards)
- [Submission Process](#submission-process)
- [Review Process](#review-process)
- [Style Guide](#style-guide)

## Code of Conduct

All contributors must adhere to professional conduct:

- Be respectful and inclusive
- Focus on factual, evidence-based contributions
- Cite authoritative sources
- Avoid unsubstantiated claims
- Respect intellectual property

## How to Contribute

### Reporting Issues

Before creating an issue, please:

1. Search existing issues to avoid duplicates
2. Use issue templates when available
3. Provide specific details:
   - Affected standard/document
   - Current content (if applicable)
   - Suggested improvement
   - Authoritative source for claim

### Types of Contributions

We welcome the following contributions:

#### 1. Content Corrections

- Fix factual errors
- Update outdated information
- Correct broken links
- Fix typos and formatting

#### 2. New Standards

- Add missing standards from authoritative sources
- Create summaries of new publications
- Add implementation guides

#### 3. Improvements

- Enhance clarity and readability
- Add examples and use cases
- Improve cross-references
- Add verification methods

#### 4. Tooling

- Automation scripts
- Validation tools
- CI/CD improvements
- Monitoring enhancements

## Standards for Standards

All contributed content MUST:

### 1. Include YAML Front Matter

```yaml
---
title: "Descriptive Title"
status: "authoritative-summary"
owner: "@githubusername"
source:
  url: "https://authoritative-source.org"
  retrieved: "YYYY-MM-DD"
review:
  last_reviewed: "YYYY-MM-DD"
  next_review_due: "YYYY-MM-DD"
accuracy: "verified|under-review|UNKNOWN"
---
```

### 2. Cite Authoritative Sources

Acceptable sources include:

- NIST publications (csrc.nist.gov)
- OWASP official documentation
- CISA official guidance
- ISO/IEC standards (when freely available)
- IETF RFCs
- OpenSSF projects
- CycloneDX specifications

### 3. Use Normative Language Correctly

- **MUST/SHALL/REQUIRED**: Absolute requirements
- **MUST NOT/SHALL NOT**: Absolute prohibitions
- **SHOULD/RECOMMENDED**: Strong recommendations
- **SHOULD NOT**: Strong discouragements
- **MAY/OPTIONAL**: Truly optional

### 4. Maintain Accuracy

- Verify all claims against primary sources
- Mark unverified claims as "UNKNOWN"
- Include retrieval dates for online sources
- Update content when sources change

## Submission Process

### 1. Fork and Clone

```bash
git clone https://github.com/williamzujkowski/standards.git
cd standards
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow the structure:

```
/standards/
  ├── nist/         # NIST standards
  ├── owasp/        # OWASP standards
  ├── supply-chain/ # Supply chain security
  ├── cisa/         # CISA guidance
  └── _templates/   # Templates
```

### 3. Validate Changes

Run validation before submitting:

```bash
# Check markdown formatting
npm run lint

# Validate links
npm run check-links

# Verify front matter
npm run validate-standards
```

### 4. Commit Changes

Use conventional commits:

```bash
git add .
git commit -m "type(scope): description"
```

Types:

- `feat`: New standard or feature
- `fix`: Correction to existing content
- `docs`: Documentation updates
- `refactor`: Restructuring without changing content
- `test`: Adding or updating tests
- `ci`: CI/CD changes

### 5. Submit Pull Request

1. Push to your fork
2. Create pull request against `main`
3. Fill out PR template completely
4. Link related issues

## Review Process

### Review Criteria

Pull requests are reviewed for:

1. **Accuracy**: Claims match authoritative sources
2. **Completeness**: Required metadata present
3. **Formatting**: Follows style guide
4. **Citations**: Proper source attribution
5. **Testing**: Passes automated checks

### Review Timeline

- Initial review: 3-5 business days
- Revision review: 2-3 business days
- Merge decision: Within 7 business days of approval

### Review Outcomes

- **Approved**: Ready to merge
- **Changes Requested**: Minor adjustments needed
- **Declined**: Does not meet standards (with explanation)

## Style Guide

### Markdown Formatting

- Use ATX headers (`#` not underlines)
- Limit lines to 120 characters (except URLs)
- Use fenced code blocks with language identifiers
- Include alt text for images

### File Naming

- Use lowercase with hyphens: `nist-sp800-53r5.md`
- Include version numbers: `owasp-top10-2021.md`
- Be descriptive but concise

### Content Structure

1. YAML front matter
2. Main heading matching title
3. Overview section
4. Detailed content with clear sections
5. Implementation guidance (MUST/SHOULD)
6. References section

### Code Examples

When including code:

```javascript
// GOOD: Includes context and explanation
// Parameterized query prevents SQL injection (OWASP A03:2021)
const query = 'SELECT * FROM users WHERE id = ?';
db.execute(query, [userId]);
```

### Cross-References

Link to other standards:

```markdown
See [NIST SP 800-53 Rev. 5](../nist/sp800-53r5.md) for detailed controls.
```

## Questions?

- Create a [Discussion](https://github.com/williamzujkowski/standards/discussions)
- Review existing [Issues](https://github.com/williamzujkowski/standards/issues)
- Contact: @williamzujkowski

## License

By contributing, you agree that your contributions will be licensed under the same license as this repository.

## Recognition

Contributors are recognized in:

- Git commit history
- GitHub contributors page
- Quarterly acknowledgments (with permission)

Thank you for helping improve security standards documentation!
