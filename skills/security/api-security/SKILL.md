---
name: api-security
category: security
difficulty: intermediate
nist_controls:
- SC-8
- SC-13
- IA-5
- AC-7
related_skills:
- authentication
- tls-ssl
- input-validation
- threat-modeling
estimated_time: 4-6 hours
prerequisites:
- Basic understanding of REST APIs
- Familiarity with HTTP protocol
- Knowledge of authentication concepts
last_updated: '2025-10-17'
description: 1. Broken Object Level Authorization (BOLA) - API fails to validate user
  access to objects 2. Broken Authentication - Weak or missing authentication mechanisms
  3. Broken Object Property Level Authorization - Missing field-level access control
  4. Unrestricted Resource Consumption - No rate limiting or throttling 5. Broken
  Function Level Authorization - Missing authorization checks on endpoints 6. Unrestricted
  Access to Sensitive Business Flows - Automated abuse of legitimate workflows 7.
  Server Side Request Forgery (SSRF) - API accepts URLs without validation 8. Security
  Misconfiguration - Insecure default configs, verbose errors 9. Improper Inventory
  Management - Undocumented/deprecated APIs in production 10. Unsafe Consumption of
  APIs - Trusting third-party API data without validation
---


# API Security

> **Level System**: Each skill contains three progressive levels
>
> - **Level 1**: Quick Reference (600-800 tokens) - Essential patterns and checklists
> - **Level 2**: Implementation Guide (3000-4500 tokens) - Detailed practices and examples
> - **Level 3**: Deep Dive - Additional resources and advanced topics

## Level 1: Quick Reference

### OWASP API Security Top 10 (2023)

1. **Broken Object Level Authorization (BOLA)** - API fails to validate user access to objects
2. **Broken Authentication** - Weak or missing authentication mechanisms
3. **Broken Object Property Level Authorization** - Missing field-level access control
4. **Unrestricted Resource Consumption** - No rate limiting or throttling
5. **Broken Function Level Authorization** - Missing authorization checks on endpoints
6. **Unrestricted Access to Sensitive Business Flows** - Automated abuse of legitimate workflows
7. **Server Side Request Forgery (SSRF)** - API accepts URLs without validation
8. **Security Misconfiguration** - Insecure default configs, verbose errors
9. **Improper Inventory Management** - Undocumented/deprecated APIs in production
10. **Unsafe Consumption of APIs** - Trusting third-party API data without validation

### Essential Security Checklist

```yaml
transport_security:
  - [ ] TLS 1.2+ enforced on all endpoints
  - [ ] HSTS headers configured
  - [ ] Certificate pinning for mobile clients

authentication:
  - [ ] API keys rotated regularly
  - [ ] OAuth 2.0 with PKCE for public clients
  - [ ] JWT tokens with short expiration (15-60 min)
  - [ ] Refresh token rotation implemented

authorization:
  - [ ] Object-level authorization on all resources
  - [ ] Field-level authorization for sensitive data
  - [ ] Role-based or attribute-based access control

input_validation:
  - [ ] Schema validation on all inputs
  - [ ] Content-Type verification
  - [ ] Request size limits enforced
  - [ ] SQL injection prevention (parameterized queries)

rate_limiting:
  - [ ] Per-user rate limits (e.g., 100 req/min)
  - [ ] Per-IP rate limits for unauthenticated endpoints
  - [ ] Exponential backoff on failed auth attempts
  - [ ] Resource-specific quotas

monitoring:
  - [ ] Authentication failures logged
  - [ ] Authorization failures alerted
  - [ ] Anomalous patterns detected (sudden spikes)
  - [ ] Security events centralized (SIEM)

cors_configuration:
  - [ ] Allowlist specific origins (no wildcards in prod)
  - [ ] Credentials flag set appropriately
  - [ ] Preflight cache configured

api_versioning:
  - [ ] Deprecated versions documented
  - [ ] Sunset headers on old versions
  - [ ] Security fixes backported to supported versions
```

### Quick Rate Limiting Pattern

```python
# Python with Flask-Limiter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="redis://localhost:6379"
)

@app.route("/api/resource")
@limiter.limit("10 per minute")
def api_resource():
    return {"data": "protected"}
```

### Quick JWT Validation Pattern

```javascript
// Node.js with jsonwebtoken
const jwt = require('jsonwebtoken');

function authenticateToken(req, res, next) {
  const token = req.headers['authorization']?.split(' ')[1];

  if (!token) return res.sendStatus(401);

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
}
```

---

## Level 2:
>
> **📚 Full Examples**: See [REFERENCE.md](./REFERENCE.md) for complete code samples, detailed configurations, and production-ready implementations.

 Implementation Guide

### 2.1 Authentication Mechanisms

#### API Key Authentication

**Use Case**: Server-to-server communication, simple client auth

**Implementation Best Practices**:


*See [REFERENCE.md](./REFERENCE.md#example-0) for complete implementation.*


**Security Considerations**:

- Store only hashed keys in database (SHA-256 minimum)
- Use HTTPS exclusively
- Implement key rotation policy
- Support key revocation
- Log key usage for audit trails
- Consider key prefixes for identification (e.g., `sk_live_...`)

#### OAuth 2.0 with PKCE

**Use Case**: Third-party integrations, mobile/SPA clients


*See [REFERENCE.md](./REFERENCE.md#example-1) for complete implementation.*


#### JWT Token Management

**Best Practices**:


*See [REFERENCE.md](./REFERENCE.md#example-2) for complete implementation.*


**JWT Security Checklist**:

- Use RS256 (asymmetric) for multi-service architectures
- Keep access tokens short-lived (15-60 minutes)
- Implement refresh token rotation
- Store refresh tokens securely (hashed in DB)
- Include `jti` (JWT ID) claim for revocation
- Validate `exp`, `iat`, `iss`, `aud` claims
- Never store sensitive data in JWT payload

### 2.2 Rate Limiting and Throttling

#### Multi-Tier Rate Limiting


*See [REFERENCE.md](./REFERENCE.md#example-3) for complete implementation.*


#### Adaptive Rate Limiting


*See [REFERENCE.md](./REFERENCE.md#example-4) for complete implementation.*


### 2.3 Input Validation and Sanitization

#### Schema-Based Validation


*See [REFERENCE.md](./REFERENCE.md#example-5) for complete implementation.*


#### Content-Type Validation


*See [REFERENCE.md](./REFERENCE.md#example-6) for complete implementation.*


#### SQL Injection Prevention


*See [REFERENCE.md](./REFERENCE.md#example-7) for complete implementation.*


### 2.4 CORS Configuration

#### Secure CORS Setup


*See [REFERENCE.md](./REFERENCE.md#example-8) for complete implementation.*


**CORS Security Rules**:

- Never use `origin: '*'` with `credentials: true`
- Validate origin against allowlist (no regex if possible)
- Minimize `allowedHeaders` and `exposedHeaders`
- Set appropriate `maxAge` for preflight caching
- Consider CSRF tokens for state-changing operations

### 2.5 API Versioning

#### Version Management Strategy


*See [REFERENCE.md](./REFERENCE.md#example-9) for complete implementation.*


### 2.6 OpenAPI Security Schemas

#### Defining Security in OpenAPI 3.0


*See [REFERENCE.md](./REFERENCE.md#example-10) for complete implementation.*


### 2.7 OWASP API Security Checklist

#### Complete Implementation Checklist


*See [REFERENCE.md](./REFERENCE.md#example-11) for complete implementation.*


### 2.8 Testing API Security

#### Automated Security Testing


*See [REFERENCE.md](./REFERENCE.md#example-12) for complete implementation.*


#### Security Test Cases


*See [REFERENCE.md](./REFERENCE.md#example-13) for complete implementation.*


### 2.9 API Security Anti-Patterns

#### Common Mistakes to Avoid


*See [REFERENCE.md](./REFERENCE.md#example-14) for complete implementation.*


---

## Level 3: Deep Dive Resources

### Official Documentation

- [OWASP API Security Project](https://owasp.org/www-project-api-security/)
- [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x00-header/)
- [OAuth 2.0 RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)
- [OAuth 2.0 for Native Apps (PKCE) - RFC 8252](https://datatracker.ietf.org/doc/html/rfc8252)
- [JSON Web Token (JWT) - RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519)
- [OpenAPI Specification - Security](https://swagger.io/specification/#security-scheme-object)

### Tools

- **Security Testing**: OWASP ZAP, Burp Suite, Postman/Newman
- **API Gateway**: Kong, AWS API Gateway, Azure API Management
- **Rate Limiting**: Redis, Nginx rate limiting, Cloud provider rate limiters
- **Secrets Management**: HashiCorp Vault, AWS Secrets Manager, Azure Key Vault

### Books & Guides

- "API Security in Action" by Neil Madden
- "OAuth 2.0 Simplified" by Aaron Parecki
- "Securing Microservices APIs" by Matt McLarty & Rob Brennan

### NIST Controls Deep Dive

#### SC-8: Transmission Confidentiality and Integrity

**Implementation**:

- TLS 1.2+ for all API traffic
- Perfect Forward Secrecy (PFS) cipher suites
- Certificate pinning for mobile clients
- Mutual TLS (mTLS) for service-to-service

**Validation**:

```bash
# Test TLS configuration
testssl.sh https://api.example.com

# Verify cipher suites
nmap --script ssl-enum-ciphers -p 443 api.example.com
```

#### SC-13: Cryptographic Protection

**Implementation**:

- AES-256-GCM for data at rest
- RSA-2048 or ECDSA P-256 for signatures
- Argon2id for password hashing
- HMAC-SHA256 for message authentication

#### IA-5: Authenticator Management

**Implementation**:

- API key rotation every 90 days
- JWT secret rotation on breach
- Password complexity requirements
- Account lockout after 5 failed attempts

#### AC-7: Unsuccessful Logon Attempts

**Implementation**:

```python
class LoginAttemptTracker:
    MAX_ATTEMPTS = 5
    LOCKOUT_DURATION = 900  # 15 minutes

    def record_failed_attempt(self, user_id: str):
        key = f"login_attempts:{user_id}"
        attempts = redis.incr(key)
        redis.expire(key, self.LOCKOUT_DURATION)

        if attempts >= self.MAX_ATTEMPTS:
            redis.setex(f"lockout:{user_id}", self.LOCKOUT_DURATION, "locked")
            alert_security_team(user_id, attempts)

    def is_locked_out(self, user_id: str) -> bool:
        return redis.exists(f"lockout:{user_id}")
```

### Bundled Resources

This skill includes the following resources in this directory:

1. **templates/openapi-security.yaml** - Complete OpenAPI 3.0 security schemas
2. **templates/rate-limiter.js** - Production-ready Express rate limiting middleware
3. **templates/input-validator.py** - Pydantic validation models for common use cases
4. **templates/api-gateway-config.yaml** - Kong/Nginx gateway configuration
5. **scripts/api-security-scan.sh** - Automated OWASP ZAP security scanning
6. **resources/owasp-api-top10.md** - Detailed OWASP API Security Top 10 guide

### Practice Exercises

1. **Implement JWT Authentication**: Build a complete JWT auth system with refresh tokens
2. **Rate Limiting Strategy**: Design multi-tier rate limiting for a SaaS API
3. **OWASP Top 10 Audit**: Scan an existing API against OWASP API Top 10
4. **Security Testing Suite**: Create Postman collection with 20+ security test cases
5. **API Gateway Configuration**: Set up Kong with OAuth2, rate limiting, and logging

### Continuous Learning

- Subscribe to [API Security Weekly](https://apisecurity.io/)
- Follow [@APIsecurity](https://twitter.com/APIsecurity) on Twitter
- Join OWASP API Security Slack channel
- Participate in bug bounty programs (HackerOne, Bugcrowd)

## Examples

### Basic Usage

```python
// TODO: Add basic example for api-security
// This example demonstrates core functionality
```

### Advanced Usage

```python
// TODO: Add advanced example for api-security
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how api-security
// works with other systems and services
```

See `examples/api-security/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Common development tools and frameworks
- **Prerequisites**: Basic understanding of general concepts

### Downstream Consumers

- **Applications**: Production systems requiring api-security functionality
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

- Follow established patterns and conventions for api-security
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

**Next Steps**: After mastering API security, explore related skills:

- **Threat Modeling** - Proactive security architecture design
- **Penetration Testing** - Offensive security testing techniques
- **Secure SDLC** - Integrating security throughout development lifecycle
- **Cloud Security** - AWS/Azure/GCP-specific API security patterns
