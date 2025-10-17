# NIST 800-63B Digital Identity Guidelines Compliance Checklist

## Overview

NIST Special Publication 800-63B provides guidance on digital identity authentication and lifecycle management. This checklist covers the key requirements for implementing NIST 800-63B compliant authentication.

**Document Reference**: [NIST SP 800-63B Revision 3](https://pages.nist.gov/800-63-3/sp800-63b.html)

---

## Authentication Assurance Levels (AAL)

### AAL1: Single-Factor Authentication

- [ ] **Memorized secret** (password) meets requirements:
  - [ ] Minimum 8 characters (no maximum)
  - [ ] No composition rules (uppercase, numbers, symbols) required
  - [ ] Check against breach databases (Have I Been Pwned, etc.)
  - [ ] No password hints allowed
  - [ ] No knowledge-based authentication (security questions)
  - [ ] No SMS as sole authentication factor

- [ ] **Password storage** compliant:
  - [ ] Use approved hash function (bcrypt, PBKDF2, scrypt, or Argon2)
  - [ ] Minimum 10,000 iterations for PBKDF2
  - [ ] Bcrypt cost factor ≥ 10 (recommended ≥ 12)
  - [ ] Unique salt per password
  - [ ] Never store plaintext passwords

- [ ] **Throttling** implemented:
  - [ ] Rate limiting on authentication attempts
  - [ ] Account lockout after repeated failures
  - [ ] Exponential backoff for failed attempts

### AAL2: Multi-Factor Authentication

All AAL1 requirements PLUS:

- [ ] **Second factor** required:
  - [ ] TOTP (Time-based One-Time Password)
  - [ ] Push notification with biometric confirmation
  - [ ] SMS OTP (acceptable but not recommended)
  - [ ] Email OTP (acceptable for low-risk scenarios)
  - [ ] Hardware OTP token

- [ ] **Cryptographic authenticator** characteristics:
  - [ ] Something you have (phone, hardware token)
  - [ ] Proof of possession required
  - [ ] Resistant to replay attacks

- [ ] **Out-of-band authenticator**:
  - [ ] Separate communication channel
  - [ ] Time-limited (typically 5-10 minutes)
  - [ ] Random value with sufficient entropy (≥64 bits)

### AAL3: Hardware-Based Cryptographic Authentication

All AAL2 requirements PLUS:

- [ ] **Hardware cryptographic authenticator** required:
  - [ ] FIDO2/WebAuthn security key (YubiKey, etc.)
  - [ ] PIV/CAC smart card
  - [ ] Platform authenticator (Touch ID, Face ID, Windows Hello)

- [ ] **Verifier impersonation resistance**:
  - [ ] Public key cryptography
  - [ ] Challenge-response protocol
  - [ ] Phishing-resistant

- [ ] **Key storage**:
  - [ ] Private key stored in hardware
  - [ ] Key extraction not possible
  - [ ] FIPS 140-2 Level 1 or higher (recommended Level 2+)

---

## Password Requirements (Section 5.1.1)

### Memorized Secret (Password) Policies

- [ ] **Length requirements**:
  - [ ] Minimum 8 characters for user-chosen passwords
  - [ ] Minimum 6 characters for machine-generated passwords
  - [ ] At least 64 characters maximum (no arbitrary limits)
  - [ ] All printable ASCII characters allowed
  - [ ] Unicode characters (including emojis) allowed

- [ ] **Prohibited requirements** (DO NOT implement):
  - [ ] ❌ Composition rules (e.g., "must have uppercase, number, symbol")
  - [ ] ❌ Periodic password rotation without indication of compromise
  - [ ] ❌ Password hints
  - [ ] ❌ Security questions (knowledge-based authentication)
  - [ ] ❌ Password complexity requirements

- [ ] **Required checks**:
  - [ ] Compare against breach databases (HaveIBeenPwned API)
  - [ ] Check against common passwords list (top 100,000)
  - [ ] Verify not identical to username
  - [ ] Check for repetitive or sequential characters

- [ ] **Password change policy**:
  - [ ] Allow user-initiated password changes anytime
  - [ ] Force password change only on evidence of compromise
  - [ ] No arbitrary expiration periods

---

## Multi-Factor Authentication (Section 5.1.3-5.1.6)

### TOTP (Time-Based One-Time Password)

- [ ] **Implementation**:
  - [ ] RFC 6238 compliant
  - [ ] 6-digit OTP minimum
  - [ ] 30-second time window
  - [ ] Shared secret ≥128 bits entropy
  - [ ] Allow ±1 time step for clock skew

- [ ] **Registration**:
  - [ ] Generate secure random secret
  - [ ] Provide QR code for easy enrollment
  - [ ] Verify OTP before enabling MFA
  - [ ] Provide recovery codes

### WebAuthn/FIDO2

- [ ] **Authenticator requirements**:
  - [ ] Support FIDO2/WebAuthn protocol
  - [ ] Attestation verification (for high-security scenarios)
  - [ ] User verification (PIN or biometric)
  - [ ] Credential management (allow multiple keys)

- [ ] **Server-side validation**:
  - [ ] Verify authenticator data signature
  - [ ] Check challenge matches
  - [ ] Verify origin matches relying party ID
  - [ ] Store credential ID and public key
  - [ ] Increment signature counter on each use

### SMS OTP (Acceptable but not recommended)

- [ ] **If using SMS OTP**:
  - [ ] ≥6 random digits
  - [ ] 10-minute expiration maximum
  - [ ] Rate limiting to prevent enumeration
  - [ ] Single-use codes
  - [ ] Inform users of risks (SIM swapping)

---

## Session Management (Section 7)

### Session Requirements

- [ ] **Session binding**:
  - [ ] Bind session to user agent
  - [ ] Bind session to IP address (optional, consider mobile users)
  - [ ] Session token ≥64 bits entropy
  - [ ] Cryptographically random session IDs

- [ ] **Session timeout**:
  - [ ] Idle timeout: 30 minutes for AAL1
  - [ ] Idle timeout: 15 minutes for AAL2
  - [ ] Idle timeout: 15 minutes for AAL3
  - [ ] Absolute timeout: 12 hours maximum (AAL2/AAL3)
  - [ ] Reauthentication required after absolute timeout

- [ ] **Session termination**:
  - [ ] User-initiated logout invalidates session
  - [ ] Server-side session revocation
  - [ ] Clear session data on logout

### Cookie Security

- [ ] **Secure cookie attributes**:
  - [ ] `HttpOnly` flag set (prevent XSS)
  - [ ] `Secure` flag set (HTTPS only)
  - [ ] `SameSite=Strict` or `SameSite=Lax`
  - [ ] Appropriate domain and path scope
  - [ ] Expiration matches session timeout

---

## Credential Storage (Section 5.1.1.2)

### Password Hashing

- [ ] **Approved algorithms** (use one):
  - [ ] **Argon2id** (recommended)
    - [ ] Memory cost: 15 MB minimum
    - [ ] Time cost: 2 iterations minimum
  - [ ] **bcrypt**
    - [ ] Cost factor ≥12 (adjust for ~1 second computation)
  - [ ] **PBKDF2**
    - [ ] 10,000 iterations minimum (SHA-256 or SHA-512)
    - [ ] 100,000+ iterations recommended
  - [ ] **scrypt**
    - [ ] N=2^16, r=8, p=1 minimum

- [ ] **Salt requirements**:
  - [ ] ≥32 bits minimum (128 bits recommended)
  - [ ] Cryptographically random
  - [ ] Unique per password
  - [ ] Stored with hash

### Biometric Storage

- [ ] **Biometric data protection**:
  - [ ] Never store raw biometric data
  - [ ] Use one-way feature extraction
  - [ ] Store templates on secure hardware
  - [ ] Biometric matching on device (not server)

---

## Threat Model Protection

### Phishing Resistance

- [ ] **Phishing protection measures**:
  - [ ] FIDO2/WebAuthn for AAL3
  - [ ] Verify origin/domain in authentication flow
  - [ ] User education on phishing indicators
  - [ ] Monitor for domain spoofing

### Replay Attacks

- [ ] **Replay protection**:
  - [ ] Challenge-response for authenticators
  - [ ] Nonces for one-time use
  - [ ] Time-limited tokens
  - [ ] Signature counters for FIDO2

### Man-in-the-Middle (MITM)

- [ ] **MITM protection**:
  - [ ] TLS 1.2+ for all authentication traffic
  - [ ] Certificate pinning (mobile apps)
  - [ ] HSTS (HTTP Strict Transport Security)
  - [ ] Strong cipher suites

### Brute Force

- [ ] **Brute force protection**:
  - [ ] Rate limiting (account and IP-based)
  - [ ] CAPTCHA after failed attempts
  - [ ] Account lockout with increasing delays
  - [ ] Monitoring and alerting on attack patterns

---

## Account Recovery (Section 6.1.2.3)

### Password Reset

- [ ] **Secure reset process**:
  - [ ] Email-based reset link
  - [ ] Time-limited reset token (15-30 minutes)
  - [ ] Cryptographically random token (≥128 bits)
  - [ ] Single-use tokens
  - [ ] Notify user of password change

### Account Recovery Codes

- [ ] **Recovery code requirements**:
  - [ ] Generate 8-10 recovery codes
  - [ ] Minimum 8 characters each
  - [ ] Cryptographically random
  - [ ] One-time use
  - [ ] Secure storage (hashed like passwords)
  - [ ] Allow user to regenerate

---

## Privacy Considerations (Section 9)

### Data Minimization

- [ ] **Minimize PII collection**:
  - [ ] Collect only necessary authentication data
  - [ ] No unnecessary linkage to other identities
  - [ ] Pseudonymous identifiers when possible

### Consent and Notice

- [ ] **User awareness**:
  - [ ] Clear notice of authentication methods
  - [ ] Inform of biometric data usage
  - [ ] Consent for MFA enrollment
  - [ ] Privacy policy accessible

---

## Audit and Logging (Section 8)

### Authentication Events

- [ ] **Log authentication events**:
  - [ ] Successful authentications
  - [ ] Failed authentication attempts
  - [ ] Account lockouts
  - [ ] Password changes
  - [ ] MFA enrollments/changes
  - [ ] Session creation and termination

- [ ] **Log data requirements**:
  - [ ] Timestamp (UTC)
  - [ ] User identifier
  - [ ] IP address
  - [ ] User agent
  - [ ] Authentication method
  - [ ] Outcome (success/failure)

- [ ] **Log protection**:
  - [ ] No passwords or secrets in logs
  - [ ] Tamper-evident storage
  - [ ] Retention per security policy
  - [ ] Regular review and monitoring

---

## Implementation Checklist

### Pre-Launch

- [ ] Security review of authentication flow
- [ ] Penetration testing (OWASP Top 10)
- [ ] Code review of authentication logic
- [ ] Breach database integration tested
- [ ] MFA enrollment tested
- [ ] Account recovery tested
- [ ] Session management tested
- [ ] Rate limiting verified

### Post-Launch

- [ ] Monitor authentication logs
- [ ] Track failed authentication rates
- [ ] Review account lockouts
- [ ] Update breach databases regularly
- [ ] Conduct periodic security audits
- [ ] Review and update authentication policies
- [ ] Test account recovery procedures
- [ ] Conduct user education on security

---

## Resources

- **NIST 800-63B Full Specification**: https://pages.nist.gov/800-63-3/sp800-63b.html
- **OWASP Authentication Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- **HaveIBeenPwned API**: https://haveibeenpwned.com/API/v3
- **FIDO Alliance**: https://fidoalliance.org/
- **WebAuthn Specification**: https://www.w3.org/TR/webauthn/

---

## Compliance Summary

| Requirement | AAL1 | AAL2 | AAL3 |
|-------------|------|------|------|
| Password minimum 8 chars | ✓ | ✓ | ✓ |
| No composition rules | ✓ | ✓ | ✓ |
| Breach database check | ✓ | ✓ | ✓ |
| Rate limiting | ✓ | ✓ | ✓ |
| Multi-factor required | ✗ | ✓ | ✓ |
| Hardware authenticator | ✗ | ✗ | ✓ |
| Phishing-resistant | ✗ | ✗ | ✓ |
| Session timeout (idle) | 30 min | 15 min | 15 min |
| Session timeout (absolute) | 12 hr | 12 hr | 12 hr |

---

**Note**: This checklist is based on NIST SP 800-63B Revision 3. Always refer to the latest version of the specification for authoritative guidance.
