# SEC:auth - Authentication Micro Standard (500 tokens max)

## Quick Rules
- Use proven standards: OAuth2, JWT, SAML
- Never store plain passwords
- Implement MFA for sensitive operations
- Session timeout: 30 min activity, 8 hour absolute

## Password Requirements
- Min 12 characters
- Mix of uppercase, lowercase, numbers, symbols
- No common passwords (check against list)
- Bcrypt/Argon2 hashing

## JWT Implementation
```python
# Generate
payload = {
    "sub": user_id,
    "exp": datetime.utcnow() + timedelta(hours=1),
    "iat": datetime.utcnow(),
    "jti": str(uuid4())  # Unique token ID
}
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Verify
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
except jwt.ExpiredSignatureError:
    # Handle expiry
```

## OAuth2 Flow
1. Redirect to provider
2. User authorizes
3. Receive code
4. Exchange code for token
5. Use token for API calls

## Security Checklist
✓ HTTPS only
✓ Secure session cookies (HttpOnly, Secure, SameSite)
✓ CSRF protection
✓ Rate limit login attempts (5 failures = 15 min lockout)
✓ Log authentication events
✓ Rotate secrets regularly

## MFA Options
- TOTP (Google Authenticator)
- SMS (backup only)
- WebAuthn/FIDO2 (preferred)

## Session Management
```python
session.permanent = False  # Close on browser exit
session.cookie_httponly = True
session.cookie_secure = True  # HTTPS only
session.cookie_samesite = 'Lax'
```