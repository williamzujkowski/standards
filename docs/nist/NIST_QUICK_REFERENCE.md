# NIST Compliance Quick Reference

**Version:** 1.0.0
**Last Updated:** 2025-01-18
**Status:** Active
**Standard Code:** NQR
**Tokens:** ~500
**Purpose:** Minimal context for quick lookups

---

## Essential Controls

| Pattern | Control | Tag |
|---------|---------|-----|
| Login/Auth | ia-2 | `@nist ia-2 "User authentication"` |
| Passwords | ia-5 | `@nist ia-5 "Password management"` |
| Permissions | ac-3 | `@nist ac-3 "Access enforcement"` |
| Logging | au-2 | `@nist au-2 "Audit events"` |
| Encryption | sc-13 | `@nist sc-13 "Cryptographic protection"` |
| Validation | si-10 | `@nist si-10 "Input validation"` |
| Errors | si-11 | `@nist si-11 "Error handling"` |
| Sessions | ac-12 | `@nist ac-12 "Session termination"` |
| Lockout | ac-7 | `@nist ac-7 "Failed login attempts"` |

## Quick Start

1. **Install**: `./scripts/setup-nist-hooks.sh`
2. **Tag code**: Add `@nist` comments above security features
3. **Validate**: `./scripts/nist-pre-commit.sh`
4. **CI/CD**: Already configured in `.github/workflows/nist-compliance.yml`

## Example

```python
# @nist ia-2 "User authentication"
# @nist au-2 "Log authentication events"
def login(username, password):
    # @nist si-10 "Validate inputs"
    if not validate_input(username):
        return error_response()

    # @nist ia-5 "Verify password"
    if verify_password(password, user.hash):
        # @nist au-2 "Log success"
        log_event("auth.success", user_id=user.id)
        return create_session(user)

    # @nist ac-7 "Track failed attempts"
    increment_failed_attempts(username)
    return error_response()
```

## Common Patterns

- **API Endpoint**: ia-2 + ac-3 + au-2 + si-10
- **Admin Function**: ac-3 + ac-6 + au-2
- **Data Storage**: sc-13 + ac-3 + au-9
- **File Upload**: si-10 + ac-3 + sc-8
- **Password Reset**: ia-5 + au-2 + ac-7

## Tools

- **VS Code Extension**: `.vscode/nist-extension/`
- **Scan Code**: `npm run scan-annotations`
- **Check Coverage**: `npm run nist-context suggest <file>`
- **Generate SSP**: `cd standards/compliance && npm run generate-ssp`

## Full Documentation

- **Complete Guide**: [NIST_IMPLEMENTATION_GUIDE.md](NIST_IMPLEMENTATION_GUIDE.md)
- **Detailed Standards**: [COMPLIANCE_STANDARDS.md](./docs/standards/COMPLIANCE_STANDARDS.md)
- **Templates**: [examples/nist-templates/](./examples/nist-templates/)
