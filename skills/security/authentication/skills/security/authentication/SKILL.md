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

# Authentication Security Standards


## Level 1: Quick Reference (5-10 minutes)

### Authentication Flows Cheat Sheet

```
┌─────────────────────────────────────────────────────────────┐
│ OAuth2 Authorization Code Flow with PKCE                    │
├─────────────────────────────────────────────────────────────┤
│ 1. Client generates code_verifier + code_challenge          │
│ 2. Redirect to /authorize with challenge                    │
│ 3. User authenticates, grants permission                     │
│ 4. Redirect back with authorization code                    │
│ 5. Exchange code + verifier for access token                │
│ 6. Use access token for API calls                           │
└─────────────────────────────────────────────────────────────┘
```

### JWT Structure

```
Header.Payload.Signature
{alg, typ}.{claims}.{signature}

Required Claims:
- iss: Issuer
- sub: Subject (user ID)
- exp: Expiration timestamp
- iat: Issued at timestamp
- aud: Audience
```

### MFA Methods (Ranked by Security)

1. **WebAuthn/FIDO2** (hardware keys, biometrics) - BEST
2. **TOTP** (authenticator apps like Google Authenticator)
3. **Email OTP** (backup only)
4. **SMS** (NOT recommended for primary MFA)

### Security Checklist

- [ ] Use OAuth2 with PKCE for SPAs
- [ ] Sign JWTs with RS256 (not HS256 for public clients)
- [ ] Set JWT expiration to 15-60 minutes
- [ ] Implement refresh token rotation
- [ ] Store tokens in httpOnly cookies (not localStorage)
- [ ] Enable TOTP or WebAuthn for MFA
- [ ] Implement account lockout after 5 failed attempts
- [ ] Use bcrypt/argon2 for password hashing
- [ ] Enforce HTTPS for all authentication endpoints
- [ ] Implement CSRF protection for session-based auth
- [ ] Set session timeout to 30 minutes
- [ ] Log all authentication events

### Common Vulnerabilities to Avoid

❌ **NEVER:**

- Store passwords in plain text
- Use MD5 or SHA-1 for password hashing
- Store JWTs in localStorage (XSS vulnerable)
- Use HS256 with public clients (secret exposure risk)
- Skip token expiration validation
- Trust client-side authentication checks
- Use SMS as primary MFA (SIM swapping attacks)


## Level 2: Implementation Guide (30-45 minutes)

### 1. OAuth2 Implementation

#### Authorization Code Flow with PKCE

**When to use:** Single-page applications, mobile apps

```javascript
// @nist ia-2 "User authentication"
// @nist sc-8 "Transmission confidentiality"
const crypto = require('crypto');

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

  // Step 2: Exchange code for tokens
  async exchangeCode(code, receivedState) {
    if (receivedState !== this.sessionStorage.state) {
      throw new Error('Invalid state parameter');
    }

    const response = await fetch(`${this.authServerUrl}/token`, {
      method: 'POST',
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code: code,
        redirect_uri: this.redirectUri,
        client_id: this.clientId,
        code_verifier: this.sessionStorage.codeVerifier
      })
    });

    return await response.json();
  }
}
```

**NIST 800-63B:** This flow meets **AAL2** (Authenticator Assurance Level 2) with PKCE. *(NIST:IA-2)*

#### Client Credentials Flow (Service-to-Service)

```python
# @nist ia-8 "Service authentication"
import requests

def get_service_token(client_id, client_secret):
    response = requests.post(
        'https://auth.example.com/token',
        auth=(client_id, client_secret),
        data={'grant_type': 'client_credentials', 'scope': 'api:read api:write'}
    )
    return response.json()['access_token']
```

### 2. JWT Best Practices

#### Token Structure and Validation

```javascript
// @nist sc-13 "Cryptographic protection"
// @nist ia-5 "Authenticator management"
const jwt = require('jsonwebtoken');
const fs = require('fs');

class JWTManager {
  constructor(privateKey, publicKey, issuer, audience) {
    this.privateKey = privateKey;
    this.publicKey = publicKey;
    this.issuer = issuer;
    this.audience = audience;
  }

  generateToken(userId, roles = [], expiresIn = '15m') {
    const now = Math.floor(Date.now() / 1000);
    return jwt.sign(
      {
        sub: userId,
        iss: this.issuer,
        aud: this.audience,
        iat: now,
        exp: now + 900,
        roles: roles,
        type: 'access'
      },
      this.privateKey,
      { algorithm: 'RS256' }
    );
  }

  verifyToken(token, expectedType = 'access') {
    try {
      const decoded = jwt.verify(token, this.publicKey, {
        algorithms: ['RS256'],
        issuer: this.issuer,
        audience: this.audience
      });

      if (decoded.type !== expectedType) {
        throw new Error('Invalid token type');
      }
      return decoded;
    } catch (err) {
      if (err.name === 'TokenExpiredError') {
        throw new Error('Token expired');
      }
      throw new Error('Invalid token');
    }
  }
}
```

#### Secure Token Storage

```javascript
// ✅ CORRECT: httpOnly cookie (XSS-safe)
app.post('/login', async (req, res) => {
  const token = createJWT(user.id);

  res.cookie('access_token', token, {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
    maxAge: 15 * 60 * 1000
  });

  res.json({ success: true });
});

// ❌ WRONG: localStorage (XSS vulnerable)
// localStorage.setItem('token', token);
```

**NIST 800-63B:** Tokens in httpOnly cookies meet **SC-8** (transmission confidentiality).

### 3. Multi-Factor Authentication

#### TOTP Implementation

```python
# @nist ia-2 "Multi-factor authentication"
import pyotp
import qrcode

class TOTPManager:
    def generate_secret(self, user_email: str) -> dict:
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)

        uri = totp.provisioning_uri(name=user_email, issuer_name='MyApp')

        qr = qrcode.make(uri)
        # Save QR code for user to scan

        return {'secret': secret, 'uri': uri}

    def verify_code(self, secret: str, code: str) -> bool:
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=1)
```

#### WebAuthn/FIDO2 (Hardware Keys)

```python
# @nist ia-2 "Hardware-based authentication"
from webauthn import generate_registration_options

class WebAuthnManager:
    def generate_registration_challenge(self, user_id, username):
        options = generate_registration_options(
            rp_id='example.com',
            rp_name='MyApp',
            user_id=user_id.encode(),
            user_name=username,
            authenticator_selection={
                'resident_key': 'preferred',
                'user_verification': 'preferred'
            }
        )
        return options
```

**NIST 800-63B:** WebAuthn with user verification meets **AAL3** (highest level).

### 4. Session Management

```javascript
// @nist sc-8 "Session security"
// @nist ac-7 "Account lockout"
const session = require('express-session');
const RedisStore = require('connect-redis').default;

class SessionManager {
  getSessionMiddleware() {
    return session({
      store: new RedisStore({ client: redisClient }),
      secret: process.env.SESSION_SECRET,
      resave: false,
      saveUninitialized: false,
      cookie: {
        secure: true,
        httpOnly: true,
        sameSite: 'strict',
        maxAge: 30 * 60 * 1000
      }
    });
  }

  enforceAbsoluteTimeout(req, res, next) {
    if (req.session.createdAt) {
      const maxAge = 8 * 60 * 60 * 1000;
      if (Date.now() - req.session.createdAt > maxAge) {
        req.session.destroy();
        return res.status(401).json({ error: 'Session expired' });
      }
    } else {
      req.session.createdAt = Date.now();
    }
    next();
  }
}
```

### 5. Passwordless Authentication

```python
# @nist ia-5 "Magic link authentication"
import secrets
from datetime import timedelta

class MagicLinkAuth:
    def generate_magic_link(self, user_email: str) -> str:
        token = secrets.token_urlsafe(32)
        redis.setex(f'magic_link:{token}', 15 * 60, user_email)
        return f'https://app.example.com/auth/verify?token={token}'

    def verify_magic_link(self, token: str) -> str:
        user_email = redis.get(f'magic_link:{token}')
        if not user_email:
            raise ValueError('Invalid or expired token')
        redis.delete(f'magic_link:{token}')
        return user_email.decode()
```

### 6. NIST 800-63B Compliance

#### Password Requirements

```python
# @nist ia-5 "Password management"
import argon2

class PasswordManager:
    def __init__(self):
        self.hasher = argon2.PasswordHasher(
            time_cost=2,
            memory_cost=65536,
            parallelism=2,
            hash_len=32
        )
        self.min_length = 8
        self.max_length = 64

    def validate_password(self, password: str):
        if len(password) < self.min_length:
            return False, f'Minimum {self.min_length} characters'
        if len(password) > self.max_length:
            return False, f'Maximum {self.max_length} characters'
        return True, 'Valid'

    def hash_password(self, password: str) -> str:
        return self.hasher.hash(password)

    def verify_password(self, password: str, hash: str) -> bool:
        try:
            self.hasher.verify(hash, password)
            return True
        except:
            return False
```

#### Account Lockout

```python
# @nist ac-7 "Unsuccessful logon attempts"
class AccountLockoutManager:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.max_attempts = 5
        self.lockout_duration = 30 * 60

    def record_failed_attempt(self, user_id: str):
        key = f'failed_attempts:{user_id}'
        attempts = self.redis.incr(key)

        if attempts == 1:
            self.redis.expire(key, 15 * 60)

        if attempts >= self.max_attempts:
            self.redis.setex(f'locked:{user_id}', self.lockout_duration, '1')
            return True
        return False

    def is_locked(self, user_id: str) -> bool:
        return self.redis.exists(f'locked:{user_id}') == 1
```


## Level 3: Deep Dive Resources

For production-ready implementations and advanced topics, see:

- **OAuth2 Flow Diagrams:** `resources/oauth2-flow-diagram.md`
- **JWT Validators:** `templates/jwt-validator.js`, `templates/jwt-validator.py`
- **OAuth2 Client:** `templates/oauth2-client.js`
- **Key Generation:** `scripts/generate-jwt-keys.sh`
- **NIST Compliance:** `resources/nist-800-63b-checklist.md`

## References

- [NIST 800-63B: Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [OAuth 2.0 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [WebAuthn Specification](https://www.w3.org/TR/webauthn-2/)
