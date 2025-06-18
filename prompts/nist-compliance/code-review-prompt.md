# NIST Code Review Prompt

## Purpose
Use this prompt to review code for NIST compliance issues and get specific recommendations.

## The Prompt

```
Perform a NIST 800-53r5 compliance review of the following code. I need a security-focused review that identifies:

1. Missing NIST control tags
2. Incorrect control mappings  
3. Incomplete control implementations
4. Security vulnerabilities related to NIST controls
5. Evidence collection gaps

Code to review:
```[LANGUAGE]
[INSERT YOUR CODE HERE]
```

Review Criteria:
- Baseline: [LOW/MODERATE/HIGH]
- Focus areas: [e.g., authentication, authorization, logging]
- Known issues: [any specific concerns]

For each finding, provide:
- **Location**: Line number or function name
- **Issue Type**: Missing tag / Incorrect tag / Incomplete implementation / Security gap
- **Severity**: CRITICAL / HIGH / MEDIUM / LOW
- **NIST Control**: Which control is affected
- **Current State**: What's currently implemented
- **Required State**: What should be implemented
- **Fix**: Specific code changes needed
- **Evidence Impact**: How this affects compliance evidence

Format the review as:
1. Executive Summary (counts and overall assessment)
2. Critical Findings (must fix)
3. Important Findings (should fix)
4. Minor Findings (nice to fix)
5. Positive Findings (what's done well)
6. Remediation Priority List
```

## Usage Examples

### Example 1: Authentication Module Review
```
Perform a NIST 800-53r5 compliance review of the following code.

Code to review:
```python
class AuthService:
    def login(self, username: str, password: str) -> dict:
        user = self.db.get_user(username)
        if not user:
            return {"success": False, "error": "Invalid credentials"}

        if bcrypt.checkpw(password.encode(), user.password_hash):
            token = jwt.encode(
                {"user_id": user.id, "exp": datetime.utcnow() + timedelta(hours=1)},
                self.secret_key,
                algorithm="HS256"
            )
            return {"success": True, "token": token}

        return {"success": False, "error": "Invalid credentials"}

    def change_password(self, user_id: str, old_password: str, new_password: str):
        user = self.db.get_user_by_id(user_id)
        if bcrypt.checkpw(old_password.encode(), user.password_hash):
            new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            self.db.update_password(user_id, new_hash)
            return True
        return False
```

Review Criteria:
- Baseline: MODERATE
- Focus areas: authentication, password management
```

### Expected Output Format

```markdown
## NIST 800-53r5 Compliance Review

### Executive Summary
- Total findings: 12
- Critical: 3
- High: 4
- Medium: 5
- Missing controls: ia-2, au-2, ac-7, si-10, ia-5.1
- Overall compliance: 40% (NEEDS SIGNIFICANT WORK)

### Critical Findings

#### 1. Missing Authentication Logging
- **Location**: Lines 2-14 (login function)
- **Issue Type**: Missing tag + Incomplete implementation
- **Severity**: CRITICAL
- **NIST Control**: au-2 (Audit Events)
- **Current State**: No logging of authentication attempts
- **Required State**: Must log all authentication attempts with outcome
- **Fix**:
```python
# @nist au-2 "Log authentication events"
def login(self, username: str, password: str) -> dict:
    try:
        user = self.db.get_user(username)
        if not user:
            # @nist au-2 "Log failed authentication - user not found"
            self.audit_log.warning(f"Failed login attempt for unknown user: {username}")
            return {"success": False, "error": "Invalid credentials"}

        # ... rest of implementation
```
- **Evidence Impact**: No audit trail for compliance verification

#### 2. No Account Lockout Mechanism
- **Location**: Entire login function
- **Issue Type**: Missing implementation
- **Severity**: CRITICAL
- **NIST Control**: ac-7 (Unsuccessful Login Attempts)
- **Current State**: Unlimited login attempts allowed
- **Required State**: Must limit failed attempts and lock accounts
- **Fix**: [Detailed implementation example]

### Important Findings

#### 3. Missing Input Validation
- **Location**: Lines 2, 16 (function parameters)
- **Issue Type**: Security gap
- **Severity**: HIGH
- **NIST Control**: si-10 (Information Input Validation)
[Rest of finding details...]

### Remediation Priority

1. **Week 1**: Critical findings
   - Add authentication logging (4 hours)
   - Implement account lockout (8 hours)
   - Add input validation (4 hours)

2. **Week 2**: High priority findings
   [List continues...]
```

## Variations

### For Pull Request Reviews
```
Review this pull request for NIST compliance impact:

Changed files:
[LIST FILES]

Diff:
[PASTE DIFF]

Specifically check:
1. Are new security features properly tagged?
2. Do modifications maintain existing control compliance?
3. Are removed features affecting any controls?
```

### For Specific Control Validation
```
Verify that this code correctly implements NIST control [CONTROL-ID]:

Expected requirements:
[LIST CONTROL REQUIREMENTS]

Code claiming to implement this control:
[PASTE CODE]
```

### For Security-Focused Review
```
Review this code for security vulnerabilities that would violate NIST controls:

Priority vulnerabilities to check:
- Injection flaws (violates si-10)
- Broken authentication (violates ia-2)
- Broken access control (violates ac-3)
- Security misconfiguration (violates cm-6)
- Sensitive data exposure (violates sc-8, sc-13)
```

## Best Practices

1. **Include Context**: Provide surrounding code if reviewing a snippet
2. **Specify Language**: Include the programming language for syntax-specific reviews
3. **Define Scope**: Clear about what type of review you need
4. **Provide Background**: Mention any existing security measures
5. **Request Priorities**: Ask for findings to be ranked by severity

## Follow-Up Prompts

After the review:

1. **Fix Generation**: "Generate the complete fixed version of [FUNCTION]"
2. **Test Creation**: "Create tests to verify the fixes for finding #X"
3. **Documentation**: "Create documentation for the security changes"
4. **Evidence**: "What evidence should I collect to prove these fixes work?"
