# NIST Quickstart Example

This quickstart demonstrates how to implement NIST 800-53r5 control tagging in a simple authentication service.

## Features Demonstrated

- **Authentication & Authorization** with NIST control tags
- **Password Management** following NIST guidelines
- **Session Management** with timeout controls
- **Audit Logging** for security events
- **Input Validation** to prevent injection attacks
- **Account Lockout** after failed attempts

## NIST Controls Implemented

| Control | Description | Implementation |
|---------|-------------|----------------|
| **AC-2** | Account Management | User creation and management |
| **AC-3** | Access Enforcement | Role-based authorization |
| **AC-6** | Least Privilege | Role-based access control |
| **AC-7** | Unsuccessful Login Attempts | Account lockout after 5 failures |
| **AC-12** | Session Termination | Automatic session expiration |
| **AC-12.1** | Session Timeout | 15-minute idle timeout |
| **AU-2** | Audit Events | Security event logging |
| **AU-3** | Content of Audit Records | Detailed audit logs |
| **IA-2** | User Authentication | Login functionality |
| **IA-5** | Authenticator Management | Password complexity rules |
| **IA-5.1** | Password-Based Authentication | PBKDF2 password hashing |
| **IA-8** | System User Identification | User identification system |
| **SC-13** | Cryptographic Protection | SHA-256 password hashing |
| **SI-10** | Information Input Validation | Input sanitization |
| **SI-11** | Error Handling | Safe error messages |

## Quick Start

### 1. Run the Example

```bash
# Run the authentication service demo
make run
```

### 2. Run Tests

```bash
# Run the test suite
make test
```

### 3. Check NIST Compliance

```bash
# Check for NIST control tags
make nist-check
```

### 4. Full Validation

```bash
# Run all checks (lint, test, NIST)
make validate
```

## File Structure

```
quickstart/
├── auth-service.py       # Main authentication service with NIST tags
├── test_auth_service.py  # Test suite validating NIST controls
├── Makefile             # Automation for testing and validation
└── README.md            # This file
```

## How to Add NIST Tags

### For Functions/Classes

```python
def authenticate(self, username: str, password: str):
    """
    Authenticate user and create session.

    @nist ia-2 "User authentication"
    @nist ac-7 "Unsuccessful login attempts"
    """
    # Implementation...
```

### For Inline Code

```python
# @nist sc-13 "Cryptographic protection"
password_hash = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
```

## CI/CD Integration

Add to your GitHub Actions workflow:

```yaml
- name: NIST Compliance Check
  run: |
    cd examples/nist-templates/quickstart
    make ci
```

## Local Development

1. **Install the Git Hook**:

   ```bash
   ./scripts/setup-nist-hooks.sh
   ```

2. **Enable VS Code Extension** (if available):
   - Install the NIST compliance extension
   - Get real-time control suggestions

3. **Run Pre-commit Checks**:

   ```bash
   git add auth-service.py
   git commit -m "Add authentication service"
   # Hook will check for NIST tags automatically
   ```

## Verification Steps

1. **Check Tag Coverage**:

   ```bash
   grep -o "@nist [a-z][a-z]-[0-9]\+" auth-service.py | sort -u
   ```

2. **Validate Format**:

   ```bash
   # Should match: @nist xx-# where xx is lowercase
   grep "@nist" auth-service.py | grep -v "@nist [a-z][a-z]-[0-9]"
   ```

3. **Run Security Tests**:

   ```bash
   python -m pytest test_auth_service.py -k security
   ```

## Best Practices

1. **Tag at the Right Level**: Add tags to functions/classes, not every line
2. **Use Descriptive Comments**: Include the control description after the tag
3. **Group Related Controls**: Keep related NIST controls together
4. **Test the Controls**: Write tests that validate each control works
5. **Document Compliance**: Maintain a control mapping (like the table above)

## Next Steps

1. Extend this example with your own security features
2. Add more NIST controls as needed
3. Integrate with your CI/CD pipeline
4. Generate compliance reports using the tags

## Resources

- [NIST 800-53r5 Controls](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [NIST Implementation Guide](../../../docs/nist/NIST_IMPLEMENTATION_GUIDE.md)
- [Compliance Standards](../../../docs/standards/COMPLIANCE_STANDARDS.md)
- [Security Standards](../../../docs/standards/MODERN_SECURITY_STANDARDS.md)
