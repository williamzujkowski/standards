# NIST-Tagged Security Templates

Pre-built security components with NIST 800-53r5 control tags already applied. Use these templates as starting points for secure implementations.

## Available Templates

### TypeScript: Authentication Service

**File:** `typescript/auth-service.ts`

Features with NIST controls:

- User authentication (`@nist ia-2`)
- Password management (`@nist ia-5`)
- Multi-factor authentication (`@nist ia-2.1`)
- Account lockout (`@nist ac-7`)
- Session management (`@nist ac-12`)
- Audit logging (`@nist au-2, au-3`)
- Input validation (`@nist si-10`)
- Error handling (`@nist si-11`)

### Python: Secure API

**File:** `python/secure_api.py`

Features with NIST controls:

- JWT authentication (`@nist ia-2`)
- Role-based authorization (`@nist ac-3`)
- Rate limiting (`@nist ac-7`)
- Input validation (`@nist si-10`)
- Webhook signature validation (`@nist sc-8, sc-13`)
- Structured audit logging (`@nist au-2, au-3`)
- Security headers (`@nist sc-8`)
- Error handling (`@nist si-11`)

### Go: Secure Service

**File:** `go/secure_service.go`

Features with NIST controls:

- Authentication service (`@nist ia-2`)
- Password complexity validation (`@nist ia-5.1`)
- Permission-based authorization (`@nist ac-3, ac-6`)
- Account lockout (`@nist ac-7`)
- HTTPS enforcement (`@nist sc-8`)
- Request/response logging (`@nist au-2, au-3`)
- Webhook signature validation (`@nist sc-13`)
- Error recovery (`@nist si-11`)

## Usage

### 1. Copy Template

```bash
# For TypeScript
cp examples/nist-templates/typescript/auth-service.ts src/services/

# For Python
cp examples/nist-templates/python/secure_api.py src/api/

# For Go
cp examples/nist-templates/go/secure_service.go cmd/server/
```

### 2. Customize for Your Needs

- Replace placeholder implementations with your business logic
- Update configuration values (secrets, timeouts, etc.)
- Add additional NIST controls as needed
- Integrate with your existing infrastructure

### 3. Verify NIST Tags

```bash
# Navigate to compliance directory
cd standards/compliance

# Scan for NIST annotations
npm run scan-annotations scan src/

# Validate control coverage
npm run nist-context suggest src/services/auth-service.ts
```

## Key Security Patterns

### Authentication Pattern

```typescript
// @nist ia-2 "User authentication"
// @nist ia-5 "Credential management"
async function authenticate(username: string, password: string) {
    // Input validation
    // @nist si-10 "Validate inputs"
    if (!validateInput(username)) {
        return { error: 'Invalid input' };
    }

    // Verify credentials
    // @nist ia-5 "Password verification"
    const valid = await verifyPassword(password, user.passwordHash);

    // Audit log
    // @nist au-2 "Log authentication events"
    await auditLog('auth.attempt', { username, success: valid });
}
```

### Authorization Pattern

```python
# @nist ac-3 "Access enforcement"
# @nist ac-6 "Least privilege"
@require_auth(scopes=['admin'])
def admin_endpoint():
    # Only accessible with admin scope
    pass
```

### Input Validation Pattern

```go
// @nist si-10 "Input validation"
func validateInput(input string) error {
    if len(input) > 255 {
        return errors.New("input too long")
    }

    // Check for dangerous patterns
    // @nist si-10 "Prevent injection attacks"
    if containsSQLInjection(input) {
        return errors.New("invalid characters")
    }

    return nil
}
```

### Audit Logging Pattern

```typescript
// @nist au-2 "Audit event generation"
// @nist au-3 "Audit record content"
interface AuditLog {
    timestamp: Date;
    correlationId: string;
    userId?: string;
    action: string;
    result: 'success' | 'failure';
    details?: any;
}
```

## Control Coverage

These templates implement the following NIST controls:

### Access Control (AC)

- `ac-2`: Account Management
- `ac-3`: Access Enforcement
- `ac-6`: Least Privilege
- `ac-7`: Unsuccessful Login Attempts
- `ac-12`: Session Termination

### Audit and Accountability (AU)

- `au-2`: Audit Events
- `au-3`: Content of Audit Records
- `au-4`: Audit Storage Capacity
- `au-9`: Protection of Audit Information

### Identification and Authentication (IA)

- `ia-2`: User Authentication
- `ia-5`: Authenticator Management
- `ia-5.1`: Password Complexity

### System and Communications Protection (SC)

- `sc-8`: Transmission Confidentiality
- `sc-13`: Cryptographic Protection

### System and Information Integrity (SI)

- `si-10`: Information Input Validation
- `si-11`: Error Handling

## Testing Templates

Each template should have corresponding tests:

```typescript
// @nist test evidence for ia-2
describe('Authentication', () => {
    it('should reject invalid credentials', async () => {
        const result = await authService.authenticate('user', 'wrong');
        expect(result.success).toBe(false);
    });

    it('should lock account after 5 failed attempts', async () => {
        // @nist ac-7 "Test account lockout"
        for (let i = 0; i < 5; i++) {
            await authService.authenticate('user', 'wrong');
        }

        const result = await authService.authenticate('user', 'correct');
        expect(result.error).toBe('Account locked');
    });
});
```

## Extending Templates

To add new security features:

1. Identify the NIST control(s) that apply
2. Add the control tag above the implementation
3. Include implementation details with `@nist-implements`
4. Mark evidence types with `@evidence`
5. Update tests to verify the control

Example:

```python
# @nist cp-10 "Information system recovery"
# @nist-implements cp-10.2 "Transaction recovery"
# @evidence code, test, config
def recover_transaction(transaction_id: str) -> bool:
    """Recover failed transaction with rollback capability."""
    # Implementation here
    pass
```

## Compliance Verification

After using these templates:

1. Generate SSP with implemented controls:

   ```bash
   cd standards/compliance
   npm run generate-ssp
   ```

2. Check control coverage:

   ```bash
   npm run scan-annotations scan . -f markdown
   ```

3. Validate implementation:

   ```bash
   ./scripts/nist-pre-commit.sh
   ```
