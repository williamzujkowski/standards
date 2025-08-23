# Interactive Validation Patterns

**Version:** 1.0.0
**Last Updated:** 2025-01-13
**Status:** Active
**Standard Code:** VAL

---

## Overview

This standard provides comprehensive guidelines and best practices for the subject area.
It aims to ensure consistency, quality, and maintainability across all related implementations.

## Purpose

Real-time, interactive validation patterns for checking code and configuration compliance against standards.

## Real-time Code Validation

### Basic Validation Pattern

```
@validate code:
```python
def my_function(x):
    return x * 2
```

against:[CS:python + TS:docstring]

Output:

- ❌ Missing type hints (CS:3.1)
- ❌ Missing docstring (CS:3.2)
- ✅ Function under 50 lines (CS:3.1)
- ⚠️ Generic function name (CS:naming)

Suggested fix:
@generate compliant-version following:[identified-violations]

```

### Suggested Compliant Version
```python
def calculate_double_value(x: Union[int, float]) -> Union[int, float]:
    """Calculate double the input value.

    Args:
        x: Numeric value to double

    Returns:
        The input value multiplied by 2

    Raises:
        TypeError: If x is not numeric
    """
    if not isinstance(x, (int, float)):
        raise TypeError(f"Expected numeric input, got {type(x)}")
    return x * 2
```

## Validation Contexts

### API Endpoint Validation

```
@validate endpoint:
```python
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = db.query(f"SELECT * FROM users WHERE id = {id}")
    return jsonify(user)
```

against:[CS:api + SEC:api + TS:integration]

Critical Issues:

- 🚨 SQL Injection vulnerability (SEC:4.1)
- ❌ No authentication check (SEC:auth)
- ❌ No input validation (CS:validation)
- ❌ No error handling (CS:error-handling)
- ⚠️ No rate limiting (SEC:api)
- ⚠️ Missing OpenAPI documentation (CS:api)

```

### Frontend Component Validation
```

@validate component:

```jsx
function UserCard({user}) {
    return <div onClick={() => delete(user.id)}>
        <h1>{user.name}</h1>
        <img src={user.avatar} />
    </div>
}
```

against:[FE:react + WD:accessibility + SEC:frontend]

Issues:

- ❌ Missing prop types/TypeScript (FE:types)
- ❌ No accessible alt text (WD:accessibility)
- ❌ Unsafe delete operation (SEC:frontend)
- ⚠️ Missing error boundaries (FE:error-handling)
- ⚠️ No loading states (WD:ux)

```

## Validation Levels

### Quick Check
```

@validate-quick [code] check:[syntax + critical-security]

```

### Standard Check
```

@validate [code] against:[relevant-standards] output:[issues + suggestions]

```

### Deep Analysis
```

@validate-deep [code] analyze:[
    - Standards compliance
    - Performance implications
    - Security vulnerabilities
    - Test coverage gaps
    - Accessibility issues
    - Technical debt
]

```

## Batch Validation

### Project-Wide Validation
```

@validate project:[path]
    standards:[CS:* + TS:* + SEC:*]
    output:[report.md]
    ignore:[node_modules/, *.test.js]

Summary Report:

- Files analyzed: 147
- Standards compliance: 78%
- Critical issues: 12
- Warnings: 45
- Suggestions: 89

```

### Incremental Validation
```

@validate changes-since:[last-commit]
    standards:[enforced-only]
    fail-on:[critical]

```

## Fix Generation Patterns

### Single Fix
```

Issue: Missing error handling
@generate fix for:[specific-issue] in-context:[surrounding-code]

```

### Batch Fixes
```

@generate fixes for-all:[missing-docstrings]
    style:[google]
    include:[parameter-descriptions]

```

### Refactoring Suggestions
```

@suggest refactoring for:[complex-function]
    goals:[reduce-complexity + improve-testability]
    maintain:[functionality + performance]

```

## IDE Integration Patterns

### On-Save Validation
```

@validate on:[save]
    check:[style + critical-issues]
    auto-fix:[safe-formatting]
    warn:[other-issues]

```

### Inline Hints
```

@show hints while:[typing]
    for:[current-line]
    based-on:[relevant-standards]
    throttle:[300ms]

```

## CI/CD Validation

### Pre-Commit Hook
```

@validate staged:[files]
    enforce:[CS:style + SEC:secrets + TS:broken-tests]
    block-if:[violations]
    suggest:[quick-fixes]

```

### Pull Request Validation
```

@validate pr:[number]
    compare:[base...head]
    comment:[line-specific-issues]
    require:[85%-coverage + no-critical-issues]
    label:[compliance-status]

```

## Validation Output Formats

### Human-Readable
```

# Code Standards Validation Report

✅ Style: Compliant
❌ Security: 2 critical issues
⚠️ Testing: Coverage at 72% (required: 85%)
💡 Performance: 3 optimization opportunities

Action Items:

1. Fix SQL injection vulnerability (line 45)
2. Add authentication check (line 23)
3. Increase test coverage by 13%

```

### Machine-Readable
```json
{
  "validation": {
    "timestamp": "2025-01-10T10:30:00Z",
    "compliance_score": 0.78,
    "issues": [
      {
        "severity": "critical",
        "type": "security",
        "standard": "SEC:4.1",
        "file": "api/users.py",
        "line": 45,
        "message": "SQL injection vulnerability",
        "fix_available": true
      }
    ]
  }
}
```

### Actionable Report

```
## Immediate Actions Required

### 🚨 Critical (Fix Now)
1. **SQL Injection** - `api/users.py:45`
   ```python
   # Current (Vulnerable)
   query = f"SELECT * FROM users WHERE id = {id}"

   # Fixed (Safe)
   query = "SELECT * FROM users WHERE id = %s"
   cursor.execute(query, (id,))
   ```

### ⚠️ Important (Fix This Sprint)

1. **Missing Tests** - `services/auth.py`
   - Current coverage: 45%
   - Required: 85%
   - Add tests for: login(), logout(), refresh_token()

```

## Implementation

### Getting Started

1. Review the relevant sections of this standard for your use case
2. Identify which guidelines apply to your project
3. Implement the required practices and patterns
4. Validate compliance using the provided checklists

### Implementation Checklist

- [ ] Review and understand applicable standards
- [ ] Implement required practices
- [ ] Follow recommended patterns
- [ ] Validate implementation against guidelines
- [ ] Document any deviations with justification
