---
name: api-security
category: security
difficulty: intermediate
nist_controls:
  - SC-8   # Transmission Confidentiality and Integrity
  - SC-13  # Cryptographic Protection
  - IA-5   # Authenticator Management
  - AC-7   # Unsuccessful Logon Attempts
related_skills:
  - authentication
  - tls-ssl
  - input-validation
  - threat-modeling
estimated_time: "4-6 hours"
prerequisites:
  - Basic understanding of REST APIs
  - Familiarity with HTTP protocol
  - Knowledge of authentication concepts
last_updated: "2025-10-17"
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

## Level 2: Implementation Guide

### 2.1 Authentication Mechanisms

#### API Key Authentication

**Use Case**: Server-to-server communication, simple client auth

**Implementation Best Practices**:

```python
# Python API Key Generation
import secrets
import hashlib
from datetime import datetime, timedelta

class APIKeyManager:
    def generate_api_key(self, user_id: str, expires_days: int = 365):
        """Generate cryptographically secure API key"""
        key = secrets.token_urlsafe(32)  # 256-bit key
        key_hash = hashlib.sha256(key.encode()).hexdigest()

        return {
            "key": key,  # Return to user once
            "hash": key_hash,  # Store in database
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=expires_days),
            "permissions": []
        }

    def validate_api_key(self, provided_key: str, stored_hash: str) -> bool:
        """Constant-time comparison to prevent timing attacks"""
        provided_hash = hashlib.sha256(provided_key.encode()).hexdigest()
        return secrets.compare_digest(provided_hash, stored_hash)

# Flask middleware
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if not key or not api_key_manager.validate_api_key(key):
            return jsonify({"error": "Invalid API key"}), 401
        return f(*args, **kwargs)
    return decorated
```

**Security Considerations**:

- Store only hashed keys in database (SHA-256 minimum)
- Use HTTPS exclusively
- Implement key rotation policy
- Support key revocation
- Log key usage for audit trails
- Consider key prefixes for identification (e.g., `sk_live_...`)

#### OAuth 2.0 with PKCE

**Use Case**: Third-party integrations, mobile/SPA clients

```javascript
// Node.js OAuth 2.0 Authorization Code + PKCE
const crypto = require('crypto');
const express = require('express');
const router = express.Router();

// Step 1: Generate PKCE challenge
function generatePKCE() {
  const verifier = crypto.randomBytes(32).toString('base64url');
  const challenge = crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url');

  return { verifier, challenge };
}

// Step 2: Authorization endpoint
router.get('/authorize', (req, res) => {
  const { client_id, redirect_uri, state, code_challenge, code_challenge_method } = req.query;

  // Validate client_id and redirect_uri
  if (!validateClient(client_id, redirect_uri)) {
    return res.status(400).json({ error: 'invalid_client' });
  }

  // Validate PKCE parameters
  if (code_challenge_method !== 'S256') {
    return res.status(400).json({ error: 'invalid_request',
                                  error_description: 'code_challenge_method must be S256' });
  }

  // Store code_challenge associated with authorization code
  const authCode = generateAuthCode();
  storePKCEChallenge(authCode, code_challenge);

  // Redirect with authorization code
  res.redirect(`${redirect_uri}?code=${authCode}&state=${state}`);
});

// Step 3: Token endpoint
router.post('/token', async (req, res) => {
  const { grant_type, code, redirect_uri, client_id, code_verifier } = req.body;

  if (grant_type !== 'authorization_code') {
    return res.status(400).json({ error: 'unsupported_grant_type' });
  }

  // Verify code_verifier against stored challenge
  const storedChallenge = getPKCEChallenge(code);
  const computedChallenge = crypto
    .createHash('sha256')
    .update(code_verifier)
    .digest('base64url');

  if (computedChallenge !== storedChallenge) {
    return res.status(400).json({ error: 'invalid_grant' });
  }

  // Issue tokens
  const accessToken = generateJWT({ client_id }, '15m');
  const refreshToken = generateRefreshToken();

  res.json({
    access_token: accessToken,
    token_type: 'Bearer',
    expires_in: 900,
    refresh_token: refreshToken
  });
});
```

#### JWT Token Management

**Best Practices**:

```javascript
// JWT Token Structure
const jwt = require('jsonwebtoken');

function generateJWT(payload, expiresIn = '15m') {
  return jwt.sign(
    {
      sub: payload.user_id,
      iat: Math.floor(Date.now() / 1000),
      exp: Math.floor(Date.now() / 1000) + (15 * 60), // 15 minutes
      iss: 'api.example.com',
      aud: 'api.example.com',
      scope: payload.permissions.join(' ')
    },
    process.env.JWT_PRIVATE_KEY,
    { algorithm: 'RS256' } // Use asymmetric signing
  );
}

// Refresh Token Rotation
class TokenManager {
  async refreshAccessToken(refreshToken) {
    const storedToken = await db.refreshTokens.findOne({ token: refreshToken });

    if (!storedToken || storedToken.expiresAt < new Date()) {
      throw new Error('Invalid or expired refresh token');
    }

    // Rotate refresh token (one-time use)
    await db.refreshTokens.deleteOne({ token: refreshToken });

    const newAccessToken = generateJWT({ user_id: storedToken.userId });
    const newRefreshToken = crypto.randomBytes(40).toString('hex');

    await db.refreshTokens.insertOne({
      token: newRefreshToken,
      userId: storedToken.userId,
      expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) // 30 days
    });

    return { accessToken: newAccessToken, refreshToken: newRefreshToken };
  }
}
```

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

```javascript
// Express.js rate limiting with Redis
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');
const redis = require('redis');

const client = redis.createClient({ url: process.env.REDIS_URL });

// Tier 1: Global IP-based limit
const globalLimiter = rateLimit({
  store: new RedisStore({ client, prefix: 'rl:global:' }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 1000, // 1000 requests per 15 min per IP
  message: 'Too many requests from this IP'
});

// Tier 2: Authenticated user limit
const userLimiter = rateLimit({
  store: new RedisStore({ client, prefix: 'rl:user:' }),
  windowMs: 60 * 1000, // 1 minute
  max: 100, // 100 requests per minute per user
  keyGenerator: (req) => req.user?.id || req.ip,
  skip: (req) => !req.user // Skip for unauthenticated
});

// Tier 3: Endpoint-specific limit
const expensiveOperationLimiter = rateLimit({
  store: new RedisStore({ client, prefix: 'rl:expensive:' }),
  windowMs: 60 * 1000,
  max: 5, // 5 requests per minute
  keyGenerator: (req) => req.user.id
});

// Apply to routes
app.use('/api', globalLimiter);
app.use('/api', authenticateToken, userLimiter);
app.post('/api/generate-report', expensiveOperationLimiter, generateReport);
```

#### Adaptive Rate Limiting

```python
# Python adaptive rate limiter based on system load
import psutil
from flask import request, jsonify

class AdaptiveRateLimiter:
    def __init__(self, base_limit=100):
        self.base_limit = base_limit

    def get_current_limit(self):
        """Adjust rate limit based on CPU/memory usage"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent

        if cpu_percent > 80 or memory_percent > 80:
            return int(self.base_limit * 0.5)  # Reduce by 50%
        elif cpu_percent > 60 or memory_percent > 60:
            return int(self.base_limit * 0.75)  # Reduce by 25%
        else:
            return self.base_limit

    def check_limit(self, user_id):
        current_limit = self.get_current_limit()
        current_count = redis_client.incr(f"rate:{user_id}:{int(time.time() / 60)}")
        redis_client.expire(f"rate:{user_id}:{int(time.time() / 60)}", 60)

        if current_count > current_limit:
            return False, current_limit, current_count
        return True, current_limit, current_count

# Middleware
def adaptive_rate_limit():
    limiter = AdaptiveRateLimiter()
    user_id = get_current_user_id()

    allowed, limit, count = limiter.check_limit(user_id)

    if not allowed:
        return jsonify({
            "error": "Rate limit exceeded",
            "limit": limit,
            "current": count,
            "retry_after": 60
        }), 429
```

### 2.3 Input Validation and Sanitization

#### Schema-Based Validation

```python
# Pydantic models for request validation
from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List
from datetime import datetime

class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30, regex=r'^[a-zA-Z0-9_-]+$')
    age: Optional[int] = Field(None, ge=0, le=150)
    roles: List[str] = Field(default_factory=list, max_items=10)

    @validator('username')
    def username_no_profanity(cls, v):
        if contains_profanity(v):
            raise ValueError('Username contains inappropriate content')
        return v

    @validator('roles')
    def validate_roles(cls, v):
        allowed_roles = {'user', 'admin', 'moderator'}
        if not set(v).issubset(allowed_roles):
            raise ValueError(f'Invalid roles. Allowed: {allowed_roles}')
        return v

    class Config:
        # Reject extra fields
        extra = 'forbid'

# FastAPI integration
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/users")
async def create_user(user_data: CreateUserRequest):
    # Input is automatically validated
    # SQL injection prevented by ORM parameterization
    user = await db.users.create(**user_data.dict())
    return {"id": user.id, "username": user.username}
```

#### Content-Type Validation

```javascript
// Express middleware for strict content-type checking
function validateContentType(allowedTypes) {
  return (req, res, next) => {
    const contentType = req.headers['content-type'];

    if (!contentType) {
      return res.status(400).json({ error: 'Content-Type header required' });
    }

    const mediaType = contentType.split(';')[0].trim();

    if (!allowedTypes.includes(mediaType)) {
      return res.status(415).json({
        error: 'Unsupported Media Type',
        allowed: allowedTypes
      });
    }

    next();
  };
}

// Apply to routes
app.post('/api/data',
  validateContentType(['application/json']),
  parseJSON,
  handleData
);
```

#### SQL Injection Prevention

```python
# ALWAYS use parameterized queries
from sqlalchemy import text

# ✅ CORRECT: Parameterized query
def get_user_by_email(email: str):
    query = text("SELECT * FROM users WHERE email = :email")
    result = db.execute(query, {"email": email})
    return result.fetchone()

# ❌ WRONG: String concatenation (vulnerable!)
def get_user_by_email_UNSAFE(email: str):
    query = f"SELECT * FROM users WHERE email = '{email}'"
    result = db.execute(query)
    return result.fetchone()

# ✅ CORRECT: ORM usage
from sqlalchemy.orm import Session

def get_user_by_email_ORM(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
```


### 2.4 CORS Configuration

#### Secure CORS Setup

```javascript
// Express CORS configuration
const cors = require('cors');

const corsOptions = {
  origin: function (origin, callback) {
    // Allowlist specific origins
    const allowedOrigins = [
      'https://app.example.com',
      'https://admin.example.com'
    ];

    // Allow requests with no origin (mobile apps, Postman)
    if (!origin || allowedOrigins.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true, // Allow cookies
  optionsSuccessStatus: 200,
  maxAge: 86400, // Cache preflight for 24 hours
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Request-ID'],
  exposedHeaders: ['X-Total-Count', 'X-Page-Count']
};

app.use(cors(corsOptions));

// Public API endpoints (no credentials)
app.use('/api/public', cors({
  origin: '*',
  credentials: false
}));
```

**CORS Security Rules**:

- Never use `origin: '*'` with `credentials: true`
- Validate origin against allowlist (no regex if possible)
- Minimize `allowedHeaders` and `exposedHeaders`
- Set appropriate `maxAge` for preflight caching
- Consider CSRF tokens for state-changing operations

### 2.5 API Versioning

#### Version Management Strategy

```python
# FastAPI versioning with deprecation
from fastapi import FastAPI, Header, HTTPException, status
from datetime import datetime

app = FastAPI()

# Version 1 (deprecated)
@app.get("/v1/users", deprecated=True)
async def get_users_v1(x_api_version: str = Header(None)):
    # Add Sunset header (RFC 8594)
    return Response(
        content=json.dumps({"users": old_format()}),
        headers={
            "Sunset": "Sat, 31 Dec 2025 23:59:59 GMT",
            "Deprecation": "true",
            "Link": '<https://api.example.com/v2/users>; rel="successor-version"'
        }
    )

# Version 2 (current)
@app.get("/v2/users")
async def get_users_v2():
    return {"users": new_format(), "version": "2.0"}

# Version-agnostic endpoint with header-based routing
@app.get("/users")
async def get_users(accept_version: str = Header("2.0", alias="Accept-Version")):
    if accept_version == "1.0":
        return await get_users_v1()
    elif accept_version == "2.0":
        return await get_users_v2()
    else:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Version {accept_version} not supported. Available: 1.0, 2.0"
        )
```

### 2.6 OpenAPI Security Schemas

#### Defining Security in OpenAPI 3.0

```yaml
# openapi-security.yaml
openapi: 3.0.3
info:
  title: Secure API
  version: 2.0.0

# Define security schemes
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key for server-to-server communication

    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token for user authentication

    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/oauth/authorize
          tokenUrl: https://auth.example.com/oauth/token
          scopes:
            read:users: Read user data
            write:users: Modify user data
            admin: Administrative access

# Apply security globally
security:
  - BearerAuth: []

paths:
  /public/health:
    get:
      summary: Health check
      security: []  # Override: no auth required
      responses:
        '200':
          description: Service healthy

  /users:
    get:
      summary: List users
      security:
        - OAuth2: [read:users]
      responses:
        '200':
          description: User list
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '403':
          $ref: '#/components/responses/ForbiddenError'

  /admin/users:
    post:
      summary: Create user (admin only)
      security:
        - OAuth2: [admin]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '403':
          $ref: '#/components/responses/ForbiddenError'
        '422':
          description: Validation error

components:
  responses:
    UnauthorizedError:
      description: Authentication required
      headers:
        WWW-Authenticate:
          schema:
            type: string
            example: Bearer realm="api"

    ForbiddenError:
      description: Insufficient permissions
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                example: Forbidden
              required_scope:
                type: string
                example: admin
```

### 2.7 OWASP API Security Checklist

#### Complete Implementation Checklist

```markdown
## API Security Implementation Checklist

### Authentication & Authorization

- [ ] **Strong Authentication**
  - [ ] Multi-factor authentication for sensitive operations
  - [ ] Account lockout after N failed attempts (AC-7)
  - [ ] Password policies enforced (IA-5)
  - [ ] Secure password reset flow (email verification)

- [ ] **Token Security**
  - [ ] Short-lived access tokens (15-60 min)
  - [ ] Refresh token rotation on each use
  - [ ] Token revocation mechanism implemented
  - [ ] Token binding to client (if applicable)

- [ ] **Authorization**
  - [ ] Object-level authorization (check user owns resource)
  - [ ] Field-level authorization (redact sensitive fields)
  - [ ] Function-level authorization (check endpoint permissions)
  - [ ] Principle of least privilege applied

### Data Protection

- [ ] **Transport Security** (SC-8)
  - [ ] TLS 1.2+ enforced
  - [ ] Strong cipher suites only
  - [ ] HSTS header set (max-age=31536000; includeSubDomains)
  - [ ] Certificate pinning for mobile apps

- [ ] **Cryptography** (SC-13)
  - [ ] Sensitive data encrypted at rest (AES-256)
  - [ ] Cryptographic keys rotated regularly
  - [ ] Use authenticated encryption (GCM mode)
  - [ ] No deprecated algorithms (MD5, SHA-1, DES)

- [ ] **Data Handling**
  - [ ] PII minimized in logs
  - [ ] Sensitive data masked in responses
  - [ ] No secrets in version control
  - [ ] Secure deletion of sensitive data

### Input Validation

- [ ] **Request Validation**
  - [ ] Schema validation on all inputs
  - [ ] Content-Type verification
  - [ ] Request size limits (prevent DoS)
  - [ ] File upload validation (type, size, content)

- [ ] **Injection Prevention**
  - [ ] Parameterized queries (SQL injection)
  - [ ] Output encoding (XSS prevention)
  - [ ] Command injection prevention
  - [ ] LDAP injection prevention

### Rate Limiting & Resource Management

- [ ] **Rate Limiting**
  - [ ] Per-user rate limits
  - [ ] Per-IP rate limits (unauthenticated)
  - [ ] Endpoint-specific limits (expensive operations)
  - [ ] Proper 429 responses with Retry-After

- [ ] **Resource Quotas**
  - [ ] Maximum request body size
  - [ ] Maximum response size
  - [ ] Pagination enforced on list endpoints
  - [ ] Connection pooling configured

### Monitoring & Logging

- [ ] **Security Logging**
  - [ ] Authentication attempts logged
  - [ ] Authorization failures logged
  - [ ] Input validation failures logged
  - [ ] Rate limit violations logged

- [ ] **Monitoring**
  - [ ] Real-time alerting for anomalies
  - [ ] Failed auth spike detection
  - [ ] Unusual traffic pattern detection
  - [ ] Security dashboard implemented

### API Design

- [ ] **Error Handling**
  - [ ] No sensitive data in error messages
  - [ ] No stack traces in production
  - [ ] Consistent error format
  - [ ] Proper HTTP status codes

- [ ] **Versioning**
  - [ ] API versioning strategy implemented
  - [ ] Deprecated versions documented
  - [ ] Sunset headers on old versions
  - [ ] Migration guide published

- [ ] **Documentation**
  - [ ] OpenAPI specification maintained
  - [ ] Security requirements documented
  - [ ] Rate limits documented
  - [ ] Example requests/responses

### Infrastructure

- [ ] **Deployment Security**
  - [ ] API gateway/proxy implemented
  - [ ] DDoS protection enabled
  - [ ] WAF rules configured
  - [ ] Regular security scans

- [ ] **Secrets Management**
  - [ ] Secrets in vault (not env vars)
  - [ ] Automatic secret rotation
  - [ ] Least privilege for service accounts
  - [ ] Audit trail for secret access
```

### 2.8 Testing API Security

#### Automated Security Testing

```bash
# OWASP ZAP automated scan
docker run -v $(pwd):/zap/wrk/:rw -t owasp/zap2docker-stable \
  zap-api-scan.py \
  -t https://api.example.com/openapi.json \
  -f openapi \
  -r zap-report.html \
  -J zap-report.json

# Postman security tests
newman run api-security-tests.json \
  --environment production.json \
  --reporters cli,json \
  --reporter-json-export security-test-results.json
```

#### Security Test Cases

```javascript
// Postman/Newman security test collection
{
  "info": {
    "name": "API Security Tests"
  },
  "item": [
    {
      "name": "SQL Injection Test",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/users?email=' OR '1'='1"
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test('Should not be vulnerable to SQL injection', function() {",
              "  pm.response.to.have.status(400);",
              "  pm.expect(pm.response.json()).to.not.have.property('users');",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "Rate Limit Test",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/users"
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "// Send 100 requests rapidly",
              "for (let i = 0; i < 100; i++) {",
              "  pm.sendRequest(pm.request.url, (err, res) => {",
              "    if (res.code === 429) {",
              "      pm.test('Rate limiting is enforced', function() {",
              "        pm.expect(res.headers.get('Retry-After')).to.exist;",
              "      });",
              "    }",
              "  });",
              "}"
            ]
          }
        }
      ]
    },
    {
      "name": "CORS Policy Test",
      "request": {
        "method": "OPTIONS",
        "url": "{{base_url}}/users",
        "header": [
          {
            "key": "Origin",
            "value": "https://evil.com"
          }
        ]
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test('Should reject unauthorized origins', function() {",
              "  const allowOrigin = pm.response.headers.get('Access-Control-Allow-Origin');",
              "  pm.expect(allowOrigin).to.not.equal('https://evil.com');",
              "});"
            ]
          }
        }
      ]
    }
  ]
}
```

### 2.9 API Security Anti-Patterns

#### Common Mistakes to Avoid

```python
# ❌ ANTI-PATTERN 1: Trusting client-side data
@app.post("/transfer")
def transfer_money(request: TransferRequest):
    # Client sends: {"from": "user123", "to": "user456", "amount": 100}
    # Attacker changes "from" to another user's account!
    transfer_funds(request.from_account, request.to_account, request.amount)

# ✅ CORRECT: Use authenticated user context
@app.post("/transfer")
def transfer_money(request: TransferRequest, current_user: User = Depends(get_current_user)):
    # Validate user owns the source account
    if not current_user.owns_account(request.from_account):
        raise HTTPException(status_code=403, detail="Unauthorized")
    transfer_funds(request.from_account, request.to_account, request.amount)

# ❌ ANTI-PATTERN 2: Exposing internal IDs
@app.get("/users/{user_id}")
def get_user(user_id: int):
    # Sequential IDs allow enumeration attacks
    return db.users.get(user_id)

# ✅ CORRECT: Use UUIDs or enforce authorization
@app.get("/users/{user_uuid}")
def get_user(user_uuid: str, current_user: User = Depends(get_current_user)):
    user = db.users.get_by_uuid(user_uuid)
    if not current_user.can_view(user):
        raise HTTPException(status_code=403)
    return user

# ❌ ANTI-PATTERN 3: Detailed error messages
@app.post("/login")
def login(email: str, password: str):
    user = db.users.get_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="Email not found")  # Info leak!
    if not check_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")  # Info leak!

# ✅ CORRECT: Generic error messages
@app.post("/login")
def login(email: str, password: str):
    user = db.users.get_by_email(email)
    if not user or not check_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return generate_token(user)
```

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

---

**Next Steps**: After mastering API security, explore related skills:

- **Threat Modeling** - Proactive security architecture design
- **Penetration Testing** - Offensive security testing techniques
- **Secure SDLC** - Integrating security throughout development lifecycle
- **Cloud Security** - AWS/Azure/GCP-specific API security patterns
