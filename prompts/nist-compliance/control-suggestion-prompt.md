# NIST Control Suggestion Prompt

## Purpose
Use this prompt when you have code that needs NIST control tagging but you're unsure which controls apply.

## The Prompt

```
You are a NIST 800-53r5 compliance expert. Analyze the following code and suggest appropriate security controls from the moderate baseline.

Code to analyze:
```
[INSERT YOUR CODE HERE]
```

For each security-relevant feature in the code:

1. **Identify the security pattern** (e.g., authentication, authorization, encryption, logging, validation)

2. **Map to NIST controls** using this reference:
   - Authentication → ia-2, ia-5
   - Authorization → ac-3, ac-6
   - Password handling → ia-5, ia-5.1
   - Session management → ac-12
   - Encryption → sc-8 (transit), sc-13 (at rest)
   - Audit/Logging → au-2, au-3
   - Input validation → si-10
   - Error handling → si-11
   - Rate limiting → ac-7

3. **Suggest tag placement** showing exactly where to add @nist annotations

4. **Explain the rationale** for each suggested control

5. **Identify missing security features** that should be implemented for moderate baseline compliance

Format your response as:
- Line X: [Description of feature]
  - Suggested control: @nist [control-id] "[description]"
  - Rationale: [Why this control applies]
  - Placement: [Where to add the tag]

Example output:
- Line 15-20: User authentication function
  - Suggested control: @nist ia-2 "User authentication"
  - Rationale: This function verifies user identity, which directly implements ia-2
  - Placement: Add above the function definition on line 15
```

## Usage Example

### Input:
```python
def login(username, password):
    user = get_user(username)
    if verify_password(password, user.password_hash):
        create_session(user.id)
        return {"success": True}
    return {"success": False}
```

### Expected Output:
```
- Line 1-6: User authentication function
  - Suggested control: @nist ia-2 "User authentication implementation"
  - Rationale: This function authenticates users by verifying credentials
  - Placement: Add above the function definition on line 1

- Line 3: Password verification
  - Suggested control: @nist ia-5 "Password-based authentication"
  - Rationale: Uses password as authenticator, implements ia-5 requirements
  - Placement: Add as comment above line 3

Missing security features for moderate baseline:
1. No audit logging (@nist au-2) - Should log authentication attempts
2. No account lockout (@nist ac-7) - Should track/limit failed attempts
3. No input validation (@nist si-10) - Should validate username/password format
4. No session timeout (@nist ac-12) - Should set session expiration
```

## Variations

### For Specific Languages
Add to the prompt:
```
The code is written in [LANGUAGE]. Use idiomatic comment syntax for @nist tags:
- Python: # @nist
- JavaScript/TypeScript: // @nist or /** @nist */
- Go: // @nist
- Java: // @nist or /** @nist */
```

### For Specific Baselines
Modify the prompt:
```
Suggest controls from the [LOW/MODERATE/HIGH] baseline only.
```

### For Specific Domains
Add context:
```
This is a [healthcare/financial/government] application that must comply with [HIPAA/PCI-DSS/FISMA].
```
