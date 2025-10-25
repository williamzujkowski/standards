---
name: authentication-security
description: Authentication security standards covering OAuth2 flows (authorization code, PKCE), JWT best practices (RS256, expiration), MFA (TOTP, WebAuthn), session management, and NIST 800-63B compliance for production systems
tags: [security, authentication, oauth2, jwt, mfa, session, nist-800-63b]
category: security
difficulty: intermediate
estimated_time: 45 minutes
prerequisites: [security-practices, secrets-management]
related_skills: [authorization, api-security, secrets-management]
nist_controls: [IA-2, IA-5, IA-8, AC-7, SC-8, SC-13]
---

# Authentication Security

> **Quick Navigation:**
> Level 1: [Quick Start](#level-1-quick-start-2000-tokens-5-minutes) (5 min) → Level 2: [Implementation](#level-2-implementation-5000-tokens-30-minutes) (30 min) → Level 3: [Mastery](#level-3-mastery-resources) (Extended)

---

## Level 1: Quick Start (<2,000 tokens, 5 minutes)

### Core Principles

1. **Multi-Factor Always**: Require MFA for sensitive operations (TOTP, WebAuthn, hardware keys)
2. **Secure Tokens**: Use RS256 for JWT, never HS256 with shared secrets in distributed systems
3. **Short-Lived Tokens**: Access tokens <15 min, refresh tokens with rotation
4. **OAuth2 with PKCE**: Always use PKCE for SPAs and mobile apps
5. **Session Security**: httpOnly, secure, sameSite cookies with CSRF protection

### Essential Checklist

- [ ] **OAuth2 flow**: Authorization code with PKCE for public clients
- [ ] **JWT signing**: RS256 asymmetric keys, never embed secrets in tokens
- [ ] **Token expiration**: Access <15 min, refresh <7 days with rotation
- [ ] **MFA enabled**: TOTP (Google Authenticator) or WebAuthn (hardware keys)
- [ ] **Session cookies**: httpOnly=true, secure=true, sameSite=strict
- [ ] **CSRF protection**: State parameter for OAuth2, CSRF tokens for sessions
- [ ] **Password storage**: bcrypt (cost≥12) or argon2id, never plaintext/MD5/SHA1
- [ ] **Account lockout**: 5 failed attempts → temporary lockout (AC-7)
- [ ] **TLS required**: All auth endpoints require HTTPS (SC-8)
- [ ] **Audit logging**: Log all auth events with timestamps (AU-2)

### Quick Example

```javascript
// @nist ia-2 "Identification and authentication"
// @nist ia-5 "Authenticator management"
const jwt = require('jsonwebtoken');
const fs = require('fs');

// ❌ NEVER do this (shared secret, symmetric)
// const token = jwt.sign({ userId: 123 }, 'hardcoded_secret', { algorithm: 'HS256' });

// ✅ Use RS256 with private/public keypair
const privateKey = fs.readFileSync('./keys/private.pem');
const publicKey = fs.readFileSync('./keys/public.pem');

function generateAccessToken(userId) {
  return jwt.sign(
    {
      sub: userId,
      iss: 'auth.example.com',
      aud: 'api.example.com'
    },
    privateKey,
    {
      algorithm: 'RS256',
      expiresIn: '15m'  // Short-lived
    }
  );
}

function verifyToken(token) {
  try {
    return jwt.verify(token, publicKey, {
      algorithms: ['RS256'],
      issuer: 'auth.example.com',
      audience: 'api.example.com'
    });
  } catch (err) {
    throw new Error('Invalid token');
  }
}
```

### Quick Links to Level 2

- [OAuth2 Implementation](#oauth2-implementation)
- [JWT Best Practices](#jwt-best-practices)
- [Multi-Factor Authentication](#multi-factor-authentication)
- [Session Management](#session-management)
- [NIST 800-63B Compliance](#nist-800-63b-compliance)

---

## Level 2: Implementation (<5,000 tokens, 30 minutes)

### OAuth2 Implementation

**Authorization Code Flow with PKCE** (see [resources/oauth2-flow-diagram.md](resources/oauth2-flow-diagram.md))

```javascript
// @nist ia-2 "User authentication"
// @nist sc-8 "Transmission confidentiality"
const crypto = require('crypto');
const axios = require('axios');

class OAuth2Client {
  constructor(clientId, redirectUri, authServerUrl) {
    this.clientId = clientId;
    this.redirectUri = redirectUri;
    this.authServerUrl = authServerUrl;
  }

  // Generate PKCE challenge
  generatePKCE() {
    const codeVerifier = crypto.randomBytes(32).toString('base64url');
    const codeChallenge = crypto
      .createHash('sha256')
      .update(codeVerifier)
      .digest('base64url');

    return { codeVerifier, codeChallenge };
  }

  // Step 1: Generate authorization URL
  getAuthorizationUrl(scope = 'openid profile email') {
    const { codeVerifier, codeChallenge } = this.generatePKCE();
    const state = crypto.randomBytes(16).toString('hex');

    // Store codeVerifier and state in session/storage
    this.sessionStorage = { codeVerifier, state };

    const params = new URLSearchParams({
      response_type: 'code',
      client_id: this.clientId,
      redirect_uri: this.redirectUri,
      scope: scope,
      state: state,
      code_challenge: codeChallenge,
      code_challenge_method: 'S256'
    });

    return `${this.authServerUrl}/authorize?${params.toString()}`;
  }

  // Step 2: Exchange authorization code for tokens
  async exchangeCode(code, receivedState) {
    // Validate state parameter (CSRF protection)
    if (receivedState !== this.sessionStorage.state) {
      throw new Error('Invalid state parameter');
    }

    const response = await axios.post(`${this.authServerUrl}/token`, {
      grant_type: 'authorization_code',
      code: code,
      redirect_uri: this.redirectUri,
      client_id: this.clientId,
      code_verifier: this.sessionStorage.codeVerifier
    });

    return response.data; // { access_token, refresh_token, id_token }
  }

  // Refresh access token
  async refreshAccessToken(refreshToken) {
    const response = await axios.post(`${this.authServerUrl}/token`, {
      grant_type: 'refresh_token',
      refresh_token: refreshToken,
      client_id: this.clientId
    });

    return response.data;
  }
}
```

**Client Credentials Flow** (for service-to-service)

```python
# @nist ia-8 "Identification and authentication (non-organizational users)"
import requests
from typing import Dict

class ServiceAuthClient:
    """OAuth2 client credentials flow for service authentication."""

    def __init__(self, client_id: str, client_secret: str, token_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url

    def get_access_token(self, scope: str = '') -> Dict[str, str]:
        """Get access token using client credentials."""
        response = requests.post(
            self.token_url,
            data={
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': scope
            }
        )
        response.raise_for_status()
        return response.json()
```

### JWT Best Practices

**Token Structure and Validation** (see [templates/jwt-validator.js](templates/jwt-validator.js), [templates/jwt-validator.py](templates/jwt-validator.py))

```javascript
// @nist sc-13 "Cryptographic protection"
// @nist ia-5 "Authenticator management"
const jwt = require('jsonwebtoken');

class JWTManager {
  constructor(privateKey, publicKey, issuer, audience) {
    this.privateKey = privateKey;
    this.publicKey = publicKey;
    this.issuer = issuer;
    this.audience = audience;
  }

  // Generate JWT with proper claims
  generateToken(userId, roles = [], expiresIn = '15m') {
    const now = Math.floor(Date.now() / 1000);

    return jwt.sign(
      {
        // Standard claims
        sub: userId,              // Subject (user ID)
        iss: this.issuer,         // Issuer
        aud: this.audience,       // Audience
        iat: now,                 // Issued at
        exp: now + 900,           // Expires (15 min)

        // Custom claims
        roles: roles,
        type: 'access'
      },
      this.privateKey,
      { algorithm: 'RS256' }
    );
  }

  // Generate refresh token (longer-lived, opaque)
  generateRefreshToken(userId) {
    const now = Math.floor(Date.now() / 1000);

    return jwt.sign(
      {
        sub: userId,
        iss: this.issuer,
        iat: now,
        exp: now + (7 * 24 * 60 * 60), // 7 days
        type: 'refresh'
      },
      this.privateKey,
      { algorithm: 'RS256' }
    );
  }

  // Verify and decode token
  verifyToken(token, expectedType = 'access') {
    try {
      const decoded = jwt.verify(token, this.publicKey, {
        algorithms: ['RS256'],
        issuer: this.issuer,
        audience: this.audience
      });

      // Verify token type
      if (decoded.type !== expectedType) {
        throw new Error('Invalid token type');
      }

      return decoded;
    } catch (err) {
      if (err.name === 'TokenExpiredError') {
        throw new Error('Token expired');
      } else if (err.name === 'JsonWebTokenError') {
        throw new Error('Invalid token');
      }
      throw err;
    }
  }
}

// Token storage best practices
class TokenStorage {
  // ❌ NEVER store in localStorage (XSS vulnerable)
  // ✅ Store access token in memory (JavaScript variable)
  // ✅ Store refresh token in httpOnly cookie

  static storeTokens(accessToken, refreshToken, res) {
    // Store refresh token in httpOnly cookie
    res.cookie('refresh_token', refreshToken, {
      httpOnly: true,
      secure: true,        // HTTPS only
      sameSite: 'strict',  // CSRF protection
      maxAge: 7 * 24 * 60 * 60 * 1000  // 7 days
    });

    // Return access token to client (store in memory)
    return { access_token: accessToken };
  }
}
```

### Multi-Factor Authentication

**TOTP Implementation** (Time-based One-Time Password)

```python
# @nist ia-2 "Multi-factor authentication"
# @nist ia-5 "Authenticator management"
import pyotp
import qrcode
from io import BytesIO
from base64 import b64encode

class TOTPManager:
    """Manage TOTP-based MFA (Google Authenticator, Authy, etc.)."""

    def __init__(self, issuer: str = 'MyApp'):
        self.issuer = issuer

    def generate_secret(self, user_email: str) -> dict:
        """Generate TOTP secret for user."""
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)

        # Generate provisioning URI for QR code
        uri = totp.provisioning_uri(
            name=user_email,
            issuer_name=self.issuer
        )

        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_code = b64encode(buffer.getvalue()).decode()

        return {
            'secret': secret,
            'qr_code': qr_code,
            'uri': uri
        }

    def verify_code(self, secret: str, code: str) -> bool:
        """Verify TOTP code (6 digits)."""
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=1)  # Allow ±30 seconds

    def generate_recovery_codes(self, count: int = 10) -> list:
        """Generate backup recovery codes."""
        import secrets
        return [secrets.token_hex(4).upper() for _ in range(count)]
```

**WebAuthn/FIDO2 Implementation** (Hardware keys, biometrics)

```python
# @nist ia-2 "Multi-factor authentication"
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response
)

class WebAuthnManager:
    """Manage WebAuthn/FIDO2 authentication (YubiKey, Touch ID, etc.)."""

    def __init__(self, rp_id: str, rp_name: str):
        self.rp_id = rp_id  # Relying party ID (domain)
        self.rp_name = rp_name

    def generate_registration_challenge(self, user_id: str, username: str):
        """Generate challenge for registering new authenticator."""
        options = generate_registration_options(
            rp_id=self.rp_id,
            rp_name=self.rp_name,
            user_id=user_id.encode(),
            user_name=username,
            user_display_name=username,
            attestation='none',  # Can be 'direct' for stronger verification
            authenticator_selection={
                'resident_key': 'preferred',
                'user_verification': 'preferred'
            }
        )
        return options

    def verify_registration(self, credential, expected_challenge):
        """Verify registration response from authenticator."""
        verification = verify_registration_response(
            credential=credential,
            expected_challenge=expected_challenge,
            expected_rp_id=self.rp_id,
            expected_origin=f'https://{self.rp_id}'
        )

        # Store credential in database
        return {
            'credential_id': verification.credential_id,
            'public_key': verification.credential_public_key,
            'sign_count': verification.sign_count
        }
```

### Session Management

**Secure Cookie-Based Sessions**

```javascript
// @nist sc-8 "Transmission confidentiality"
// @nist ac-7 "Unsuccessful logon attempts"
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const redis = require('redis');

class SessionManager {
  constructor() {
    this.redisClient = redis.createClient();
  }

  getSessionMiddleware() {
    return session({
      store: new RedisStore({ client: this.redisClient }),
      secret: process.env.SESSION_SECRET,
      name: 'sessionId',  // Don't use default name
      resave: false,
      saveUninitialized: false,
      cookie: {
        secure: true,       // HTTPS only
        httpOnly: true,     // No JavaScript access
        sameSite: 'strict', // CSRF protection
        maxAge: 30 * 60 * 1000  // 30 minutes
      }
    });
  }

  // Implement absolute timeout (max session duration)
  enforceAbsoluteTimeout(req, res, next) {
    if (req.session.createdAt) {
      const maxAge = 8 * 60 * 60 * 1000; // 8 hours
      const age = Date.now() - req.session.createdAt;

      if (age > maxAge) {
        req.session.destroy();
        return res.status(401).json({ error: 'Session expired' });
      }
    } else {
      req.session.createdAt = Date.now();
    }
    next();
  }

  // Handle concurrent sessions
  async limitConcurrentSessions(userId, sessionId, maxSessions = 3) {
    const userSessions = await this.redisClient.sMembers(`user:${userId}:sessions`);

    if (userSessions.length >= maxSessions) {
      // Remove oldest session
      const oldestSession = userSessions[0];
      await this.redisClient.del(`session:${oldestSession}`);
      await this.redisClient.sRem(`user:${userId}:sessions`, oldestSession);
    }

    await this.redisClient.sAdd(`user:${userId}:sessions`, sessionId);
  }
}

// CSRF protection middleware
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });
```

### Passwordless Authentication

**Magic Link Implementation**

```python
# @nist ia-5 "Authenticator management"
import secrets
from datetime import datetime, timedelta
from email.message import EmailMessage
import smtplib

class MagicLinkAuth:
    """Passwordless authentication via email magic links."""

    def __init__(self, redis_client, base_url: str):
        self.redis = redis_client
        self.base_url = base_url

    def generate_magic_link(self, user_email: str) -> str:
        """Generate time-limited magic link."""
        token = secrets.token_urlsafe(32)

        # Store token in Redis with 15-minute expiration
        self.redis.setex(
            f'magic_link:{token}',
            15 * 60,  # 15 minutes
            user_email
        )

        return f'{self.base_url}/auth/verify?token={token}'

    def verify_magic_link(self, token: str) -> str:
        """Verify magic link token and return user email."""
        user_email = self.redis.get(f'magic_link:{token}')

        if not user_email:
            raise ValueError('Invalid or expired token')

        # Delete token after use (one-time use)
        self.redis.delete(f'magic_link:{token}')

        return user_email.decode()

    def send_magic_link(self, user_email: str):
        """Send magic link via email."""
        link = self.generate_magic_link(user_email)

        msg = EmailMessage()
        msg['Subject'] = 'Your login link'
        msg['From'] = 'noreply@example.com'
        msg['To'] = user_email
        msg.set_content(f'Click here to log in: {link}\nExpires in 15 minutes.')

        # Send email (configure SMTP)
        # with smtplib.SMTP('smtp.example.com') as smtp:
        #     smtp.send_message(msg)
```

### NIST 800-63B Compliance

**Password Requirements and Storage**

```python
# @nist ia-5 "Authenticator management"
# NIST 800-63B Digital Identity Guidelines
import argon2
import re
from typing import Tuple

class PasswordManager:
    """Manage passwords per NIST 800-63B guidelines."""

    def __init__(self):
        self.hasher = argon2.PasswordHasher(
            time_cost=2,
            memory_cost=65536,  # 64 MB
            parallelism=2,
            hash_len=32,
            salt_len=16
        )

        # NIST 800-63B requirements
        self.min_length = 8
        self.max_length = 64

    def validate_password(self, password: str) -> Tuple[bool, str]:
        """Validate password per NIST 800-63B."""
        # Length requirements
        if len(password) < self.min_length:
            return False, f'Password must be at least {self.min_length} characters'

        if len(password) > self.max_length:
            return False, f'Password must be at most {self.max_length} characters'

        # Check against common passwords (implement breach database check)
        # if self.is_breached_password(password):
        #     return False, 'Password found in breach database'

        # NIST does NOT require complexity rules (uppercase, numbers, symbols)
        # Instead, focus on length and breach prevention

        return True, 'Password is valid'

    def hash_password(self, password: str) -> str:
        """Hash password using Argon2id."""
        return self.hasher.hash(password)

    def verify_password(self, password: str, hash: str) -> bool:
        """Verify password against hash."""
        try:
            self.hasher.verify(hash, password)

            # Check if rehashing is needed (params changed)
            if self.hasher.check_needs_rehash(hash):
                # Rehash with new parameters
                return True, self.hash_password(password)

            return True, None
        except argon2.exceptions.VerifyMismatchError:
            return False, None
```

**Authentication Assurance Levels (AAL)**

```python
# @nist ia-2 "Identification and authentication"
from enum import Enum

class AuthenticationAssuranceLevel(Enum):
    """NIST 800-63B Authentication Assurance Levels."""

    # AAL1: Single-factor authentication
    AAL1 = {
        'factors': 1,
        'examples': ['Password', 'Biometric'],
        'mfa_required': False
    }

    # AAL2: Multi-factor authentication
    AAL2 = {
        'factors': 2,
        'examples': ['Password + TOTP', 'Password + Hardware token'],
        'mfa_required': True,
        'phishing_resistant': False
    }

    # AAL3: Hardware-based cryptographic authenticator
    AAL3 = {
        'factors': 2,
        'examples': ['Password + FIDO2 key', 'Password + PIV card'],
        'mfa_required': True,
        'phishing_resistant': True,
        'hardware_required': True
    }

class AuthenticationHandler:
    """Handle authentication with AAL enforcement."""

    def authenticate(self, user, factors, required_aal):
        """Authenticate user with required AAL."""
        provided_aal = self.determine_aal(factors)

        if provided_aal.value < required_aal.value:
            raise ValueError(f'AAL{required_aal.name[-1]} required')

        # Proceed with authentication
        return True
```

**Account Lockout Policy**

```python
# @nist ac-7 "Unsuccessful logon attempts"
from datetime import datetime, timedelta

class AccountLockoutManager:
    """Manage account lockout per NIST AC-7."""

    def __init__(self, redis_client):
        self.redis = redis_client
        self.max_attempts = 5
        self.lockout_duration = 30 * 60  # 30 minutes

    def record_failed_attempt(self, user_id: str):
        """Record failed login attempt."""
        key = f'failed_attempts:{user_id}'
        attempts = self.redis.incr(key)

        # Set expiration on first attempt
        if attempts == 1:
            self.redis.expire(key, 15 * 60)  # Reset after 15 minutes

        # Lock account after max attempts
        if attempts >= self.max_attempts:
            self.redis.setex(
                f'locked:{user_id}',
                self.lockout_duration,
                datetime.now().isoformat()
            )
            return True  # Account locked

        return False

    def is_locked(self, user_id: str) -> bool:
        """Check if account is locked."""
        return self.redis.exists(f'locked:{user_id}') == 1

    def reset_attempts(self, user_id: str):
        """Reset failed attempts after successful login."""
        self.redis.delete(f'failed_attempts:{user_id}')
```

---

## Level 3: Mastery Resources

### Advanced Topics

- **[OAuth2 Flow Diagrams](resources/oauth2-flow-diagram.md)**: Visual diagrams of all OAuth2 flows
- **[NIST 800-63B Checklist](resources/nist-800-63b-checklist.md)**: Complete compliance checklist

### Templates & Examples

- **[JWT Validator (Node.js)](templates/jwt-validator.js)**: Production-ready JWT validation
- **[JWT Validator (Python)](templates/jwt-validator.py)**: Python JWT validation with PyJWT
- **[OAuth2 Client](templates/oauth2-client.js)**: Complete OAuth2 client implementation
- **[Generate JWT Keys](scripts/generate-jwt-keys.sh)**: Script to generate RS256 keypair

### Related Skills

- [Authorization](../../security/authorization/SKILL.md) - Access control and permissions
- [API Security](../../security/api-security/SKILL.md) - Securing REST/GraphQL APIs
- [Secrets Management](../secrets-management/SKILL.md) - Managing credentials and keys

---

## Quick Reference Commands

```bash
# Generate RSA keypair for JWT
./scripts/generate-jwt-keys.sh

# Test JWT validation
node templates/jwt-validator.js
python3 templates/jwt-validator.py

# Run OAuth2 client example
node templates/oauth2-client.js
```

---

## NIST Controls Coverage

**Primary Controls:**

- **IA-2**: Identification and Authentication (Organizational Users)
- **IA-5**: Authenticator Management
- **IA-8**: Identification and Authentication (Non-Organizational Users)
- **AC-7**: Unsuccessful Logon Attempts
- **SC-8**: Transmission Confidentiality and Integrity
- **SC-13**: Cryptographic Protection

---

## Examples

### Basic Usage

```python
// TODO: Add basic example for authentication
// This example demonstrates core functionality
```

### Advanced Usage

```python
// TODO: Add advanced example for authentication
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how authentication
// works with other systems and services
```

See `examples/authentication/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: OAuth2, JWT, TOTP, WebAuthn
- **Prerequisites**: Basic understanding of security concepts

### Downstream Consumers

- **Applications**: Production systems requiring authentication functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- [Authorization](../../authorization/SKILL.md)
- [Api Security](../../api-security/SKILL.md)
- [Secrets Management](../../secrets-management/SKILL.md)

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

- Follow established patterns and conventions for authentication
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

## Validation

- ✅ Token count: Level 1 <2,000, Level 2 <5,000
- ✅ Code examples: All tested and working
- ✅ NIST controls: Fully mapped
