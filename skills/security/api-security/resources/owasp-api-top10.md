# OWASP API Security Top 10 (2023) - Detailed Guide

## API1:2023 Broken Object Level Authorization (BOLA)

**Risk**: High
**Description**: APIs fail to validate that authenticated users have permission to access specific objects.

### Attack Example

```http
GET /api/users/123/profile
Authorization: Bearer user456_token
```

User 456's token is used to access user 123's profile without authorization check.

### Prevention

- Implement object-level authorization on every endpoint
- Use user-derived data (from token) not client-provided IDs
- Write tests for authorization logic

### Detection

- Review access control logic in code
- Test with different user roles
- Monitor for unusual data access patterns

---

## API2:2023 Broken Authentication

**Risk**: High
**Description**: Weak authentication mechanisms allow attackers to assume identities.

### Common Issues

- Weak password requirements
- No rate limiting on auth endpoints
- Credential stuffing vulnerabilities
- Missing MFA for sensitive operations

### Prevention

- Implement strong password policies (12+ chars, complexity)
- Add rate limiting to login endpoints (5 attempts per 15 min)
- Use OAuth 2.0 with PKCE for public clients
- Implement account lockout (NIST AC-7)
- Use short-lived JWT tokens (15-60 min)

---

## API3:2023 Broken Object Property Level Authorization

**Risk**: Medium
**Description**: Missing field-level authorization allows reading/writing sensitive fields.

### Attack Example

```json
PATCH /api/users/123
{
  "email": "attacker@evil.com",
  "is_admin": true
}
```

### Prevention

- Implement field-level authorization
- Use separate DTOs for input/output
- Never expose internal fields (is_admin, created_by)
- Validate writable fields based on user role

---

## API4:2023 Unrestricted Resource Consumption

**Risk**: Medium
**Description**: No limits on resource usage leads to DoS attacks.

### Issues

- No rate limiting
- Unlimited page size in pagination
- No timeout on expensive operations
- No request size limits

### Prevention

- Implement multi-tier rate limiting
- Enforce pagination (max 100 items per page)
- Set request timeouts (30s for normal, 5m for batch)
- Limit request body size (10MB default)
- Use circuit breakers for external APIs

---

## API5:2023 Broken Function Level Authorization

**Risk**: High
**Description**: Missing authorization checks on administrative functions.

### Attack Example

```http
DELETE /api/users/456
Authorization: Bearer regular_user_token
```

### Prevention

- Implement role-based access control (RBAC)
- Deny by default, allow explicitly
- Check permissions on every endpoint
- Separate admin routes with middleware
- Test with different user roles

---

## API6:2023 Unrestricted Access to Sensitive Business Flows

**Risk**: Medium
**Description**: Automated abuse of legitimate workflows (ticket buying, voting, etc).

### Examples

- Bot buying limited inventory
- Automated voting manipulation
- Mass account creation
- Scraping personal data

### Prevention

- Implement CAPTCHA for sensitive flows
- Add rate limiting per business flow
- Detect suspicious patterns (timing, IP clustering)
- Require additional verification for high-value transactions
- Monitor for anomalies

---

## API7:2023 Server Side Request Forgery (SSRF)

**Risk**: Medium
**Description**: API accepts URLs without validation, allowing internal network access.

### Attack Example

```json
POST /api/fetch-image
{
  "url": "http://169.254.169.254/latest/meta-data/"
}
```

### Prevention

- Never accept raw URLs from users
- Use allowlist of permitted domains
- Disable redirects in HTTP clients
- Block private IP ranges (10.0.0.0/8, 192.168.0.0/16)
- Use separate network for external requests

---

## API8:2023 Security Misconfiguration

**Risk**: Medium
**Description**: Insecure default configurations expose vulnerabilities.

### Common Issues

- Verbose error messages exposing stack traces
- Missing security headers
- CORS misconfiguration (wildcard origins)
- Default credentials
- Outdated dependencies

### Prevention

- Use secure defaults
- Harden production configurations
- Add security headers (HSTS, CSP, X-Frame-Options)
- Disable verbose errors in production
- Regular dependency updates
- Configuration as code with validation

---

## API9:2023 Improper Inventory Management

**Risk**: Low
**Description**: Undocumented or deprecated APIs running in production.

### Issues

- Old API versions exposed
- Debug endpoints in production
- Undocumented admin APIs
- Shadow APIs (forgotten endpoints)

### Prevention

- Maintain API inventory (OpenAPI specs)
- Version APIs explicitly
- Sunset old versions with proper notice
- Document all endpoints
- API discovery scanning

---

## API10:2023 Unsafe Consumption of APIs

**Risk**: Medium
**Description**: Trusting third-party API data without validation.

### Issues

- No input validation on third-party data
- Blindly trusting external API responses
- No timeout on external calls
- No error handling for API failures

### Prevention

- Validate all external API responses
- Set timeouts on external calls (5-10s)
- Implement circuit breakers
- Use allowlists for accepted values
- Handle API failures gracefully
- Log and monitor third-party API issues

---

## Testing for OWASP API Top 10

### Automated Tools

- OWASP ZAP API scan
- Burp Suite Pro
- Postman/Newman security tests
- API Fuzzing tools

### Manual Testing Checklist

1. Test authorization with different user roles
2. Attempt to access other users' resources
3. Modify request to access hidden fields
4. Send 1000+ requests to test rate limiting
5. Test CORS with evil.com origin
6. Send malformed inputs (SQL injection, XSS)
7. Attempt SSRF with internal IPs
8. Review error messages for information leakage
9. Test old API versions if available
10. Verify timeout and size limits
