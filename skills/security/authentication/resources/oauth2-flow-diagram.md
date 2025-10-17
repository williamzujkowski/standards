# OAuth2 Flow Diagrams

## Authorization Code Flow with PKCE (Proof Key for Code Exchange)

**Recommended for:** Single-Page Applications (SPAs), Mobile Apps

```
┌─────────────┐                                  ┌─────────────┐                          ┌─────────────┐
│   Client    │                                  │    User     │                          │   Auth      │
│   (SPA)     │                                  │   Browser   │                          │   Server    │
└──────┬──────┘                                  └──────┬──────┘                          └──────┬──────┘
       │                                                │                                         │
       │  1. Generate PKCE                              │                                         │
       │     code_verifier = random(32 bytes)           │                                         │
       │     code_challenge = SHA256(code_verifier)     │                                         │
       │                                                │                                         │
       │  2. Redirect to /authorize                     │                                         │
       │     + client_id                                │                                         │
       │     + redirect_uri                             │                                         │
       │     + code_challenge                           │                                         │
       │     + code_challenge_method=S256               │                                         │
       │     + state (CSRF token)                       │                                         │
       │────────────────────────────────────────────────>                                         │
       │                                                │                                         │
       │                                                │  3. User authenticates                  │
       │                                                │     (username + password)                │
       │                                                │─────────────────────────────────────────>
       │                                                │                                         │
       │                                                │  4. Authorization granted               │
       │                                                │<─────────────────────────────────────────
       │                                                │                                         │
       │  5. Redirect back with authorization code      │                                         │
       │     + code                                     │                                         │
       │     + state                                    │                                         │
       │<────────────────────────────────────────────────                                         │
       │                                                │                                         │
       │  6. Verify state matches                       │                                         │
       │                                                │                                         │
       │  7. Exchange code for tokens                   │                                         │
       │     POST /token                                │                                         │
       │     + code                                     │                                         │
       │     + code_verifier                            │                                         │
       │     + client_id                                │                                         │
       │     + redirect_uri                             │                                         │
       │─────────────────────────────────────────────────────────────────────────────────────────>
       │                                                │                                         │
       │                                                │          8. Verify code_challenge       │
       │                                                │             SHA256(code_verifier)       │
       │                                                │             == stored code_challenge    │
       │                                                │                                         │
       │  9. Return tokens                              │                                         │
       │     {                                          │                                         │
       │       access_token,                            │                                         │
       │       refresh_token,                           │                                         │
       │       id_token,                                │                                         │
       │       expires_in                               │                                         │
       │     }                                          │                                         │
       │<─────────────────────────────────────────────────────────────────────────────────────────
       │                                                │                                         │
       │  10. Use access_token for API calls            │                                         │
       │                                                │                                         │
```

**PKCE Security:** Prevents authorization code interception attacks by requiring the `code_verifier` that generated the `code_challenge`.

---

## Client Credentials Flow

**Recommended for:** Service-to-Service Authentication (Backend APIs, Microservices)

```
┌─────────────┐                                  ┌─────────────┐
│   Client    │                                  │   Auth      │
│  Service    │                                  │   Server    │
└──────┬──────┘                                  └──────┬──────┘
       │                                                │
       │  1. Request token with credentials             │
       │     POST /token                                │
       │     grant_type=client_credentials              │
       │     client_id=service-a                        │
       │     client_secret=<secret>                     │
       │     scope=api:read api:write                   │
       │─────────────────────────────────────────────────>
       │                                                │
       │                                      2. Verify │
       │                                       credentials
       │                                                │
       │  3. Return access token                        │
       │     {                                          │
       │       access_token: "eyJhbGc...",              │
       │       token_type: "Bearer",                    │
       │       expires_in: 3600,                        │
       │       scope: "api:read api:write"              │
       │     }                                          │
       │<─────────────────────────────────────────────────
       │                                                │
       │  4. Use token for API calls                    │
       │     Authorization: Bearer eyJhbGc...           │
       │                                                │
```

**Security Note:** `client_secret` must be stored securely (vault, environment variables). Never commit to version control.

---

## Refresh Token Flow

**Purpose:** Obtain new access token without re-authentication

```
┌─────────────┐                                  ┌─────────────┐
│   Client    │                                  │   Auth      │
│   (SPA)     │                                  │   Server    │
└──────┬──────┘                                  └──────┬──────┘
       │                                                │
       │  1. Access token expired (401 Unauthorized)    │
       │                                                │
       │  2. Request new access token                   │
       │     POST /token                                │
       │     grant_type=refresh_token                   │
       │     refresh_token=<refresh_token>              │
       │     client_id=<client_id>                      │
       │─────────────────────────────────────────────────>
       │                                                │
       │                                      3. Verify │
       │                                       refresh_token
       │                                       not revoked
       │                                                │
       │  4. Return new tokens                          │
       │     {                                          │
       │       access_token: "eyJhbGc...",              │
       │       refresh_token: "new_refresh_token",      │
       │       expires_in: 3600                         │
       │     }                                          │
       │<─────────────────────────────────────────────────
       │                                                │
       │  5. Invalidate old refresh token (rotation)    │
       │                                                │
```

**Refresh Token Rotation:** Each refresh request returns a new refresh token and invalidates the old one. Prevents replay attacks.

---

## Common Security Vulnerabilities

### ❌ Authorization Code Interception

**Attack:** Malicious app intercepts authorization code from redirect URI

**Mitigation:** Use PKCE (code_challenge + code_verifier). Even if code is intercepted, attacker cannot exchange it without the verifier.

### ❌ CSRF (Cross-Site Request Forgery)

**Attack:** Attacker tricks user into authorizing malicious app

**Mitigation:** Use `state` parameter with random token. Verify it matches on redirect.

```javascript
// Generate state
const state = crypto.randomBytes(16).toString('hex');
sessionStorage.setItem('oauth_state', state);

// Verify on callback
if (receivedState !== sessionStorage.getItem('oauth_state')) {
  throw new Error('Invalid state - possible CSRF attack');
}
```

### ❌ Redirect URI Manipulation

**Attack:** Attacker changes `redirect_uri` to steal authorization code

**Mitigation:** Whitelist exact redirect URIs in OAuth server configuration. Do not use wildcard matching.

```yaml
# Auth server config
clients:
  - client_id: "spa-app"
    redirect_uris:
      - "https://app.example.com/callback"  # Exact match only
      # ❌ NOT: "https://*.example.com/*"
```

### ❌ Token Leakage via Logs

**Attack:** Tokens exposed in application logs, browser history, or analytics

**Mitigation:**

- Never log tokens (access, refresh, or authorization codes)
- Use httpOnly cookies for token storage (prevents XSS)
- Avoid passing tokens in URL query parameters

### ❌ Refresh Token Theft

**Attack:** Long-lived refresh token stolen and used indefinitely

**Mitigation:**

- Implement refresh token rotation (new token on each refresh, old invalidated)
- Set maximum refresh token lifetime (e.g., 30 days)
- Revoke all refresh tokens on password change or logout
- Detect suspicious refresh patterns (multiple refresh tokens used simultaneously)

---

## Implementation Checklist

### Client-Side (SPA/Mobile)

- [ ] Generate cryptographically random `code_verifier` (32 bytes minimum)
- [ ] Compute `code_challenge` using SHA256
- [ ] Generate random `state` parameter (CSRF protection)
- [ ] Store `code_verifier` and `state` in session storage (not localStorage)
- [ ] Validate `state` on callback
- [ ] Exchange authorization code within 60 seconds (short-lived)
- [ ] Store access token in httpOnly cookie (not localStorage)
- [ ] Implement automatic token refresh before expiration
- [ ] Clear tokens on logout
- [ ] Handle token refresh failures (re-authenticate)

### Server-Side (Authorization Server)

- [ ] Whitelist exact redirect URIs (no wildcards)
- [ ] Enforce PKCE for public clients (SPAs, mobile apps)
- [ ] Validate `code_challenge` matches `code_verifier`
- [ ] Issue short-lived access tokens (15-60 minutes)
- [ ] Issue long-lived refresh tokens (optional, 7-30 days)
- [ ] Implement refresh token rotation
- [ ] Revoke refresh tokens on suspicious activity
- [ ] Log all authentication events (login, logout, token refresh)
- [ ] Rate limit token endpoints (prevent brute force)
- [ ] Use HTTPS for all endpoints (TLS 1.2+)

### Service-to-Service (Client Credentials)

- [ ] Store `client_secret` in vault or environment variables
- [ ] Use mutual TLS (mTLS) for high-security environments
- [ ] Rotate client secrets regularly (90 days)
- [ ] Scope tokens to minimum required permissions
- [ ] Monitor for unauthorized token usage
- [ ] Implement circuit breakers for token endpoint failures

---

## NIST 800-63B Alignment

| OAuth2 Flow | NIST AAL Level | Requirements |
|-------------|----------------|--------------|
| **Authorization Code + PKCE** | AAL2 | Multi-factor authentication, HTTPS, session timeouts |
| **Authorization Code + PKCE + WebAuthn** | AAL3 | Hardware-based authentication (FIDO2 keys), user verification |
| **Client Credentials** | AAL2 | Mutual TLS, client certificate validation |
| **Refresh Token** | AAL2 | Token rotation, revocation on suspicious activity |

**NIST Controls:**

- **IA-2:** User authentication (OAuth2 flows)
- **IA-5:** Authenticator management (PKCE, client secrets)
- **SC-8:** Transmission confidentiality (HTTPS enforcement)
- **AC-7:** Unsuccessful logon attempts (rate limiting)

---

## References

- [RFC 6749: OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749)
- [RFC 7636: PKCE for OAuth Public Clients](https://datatracker.ietf.org/doc/html/rfc7636)
- [OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [NIST 800-63B: Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
