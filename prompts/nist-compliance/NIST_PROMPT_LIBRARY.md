# NIST Compliance LLM Prompt Library

A comprehensive collection of prompts for LLMs to assist with NIST 800-53r5 compliance implementation.

## Table of Contents

1. [Control Suggestion Prompts](#control-suggestion-prompts)
2. [Implementation Guidance Prompts](#implementation-guidance-prompts)
3. [Code Review Prompts](#code-review-prompts)
4. [Evidence Generation Prompts](#evidence-generation-prompts)
5. [Gap Analysis Prompts](#gap-analysis-prompts)
6. [Documentation Prompts](#documentation-prompts)

---

## Control Suggestion Prompts

### Basic Control Suggestion

```
Given the following code snippet, suggest relevant NIST 800-53r5 controls from the moderate baseline. For each suggested control, explain why it applies and where to add the @nist tag.

Code:
[INSERT CODE]

Output format:
- Control ID: Brief explanation
- Suggested tag location
```

### Pattern-Based Control Mapping

```
Analyze the following code for security patterns and map them to NIST 800-53r5 controls:

Patterns to look for:
- Authentication mechanisms → ia-2, ia-5
- Authorization checks → ac-3, ac-6
- Encryption usage → sc-8, sc-13
- Logging statements → au-2, au-3
- Input validation → si-10
- Error handling → si-11
- Session management → ac-12

Code:
[INSERT CODE]

For each pattern found, provide:
1. Line number
2. Pattern type
3. Recommended NIST control(s)
4. Tagging example
```

### Security Feature Detection

```
Review this code module and identify all security-relevant features that should be tagged with NIST controls:

[INSERT CODE]

For each security feature:
1. Feature description
2. NIST control mapping
3. Implementation completeness (full/partial/missing)
4. Suggested improvements
```

---

## Implementation Guidance Prompts

### Control Implementation Guide

```
Provide implementation guidance for NIST control [CONTROL-ID] in [LANGUAGE]:

Context:
- Application type: [WEB_APP/API/MICROSERVICE/etc]
- Current implementation: [DESCRIBE]
- Technology stack: [LIST TECHNOLOGIES]

Include:
1. Step-by-step implementation
2. Code examples with @nist tags
3. Common pitfalls to avoid
4. Testing approach
5. Evidence collection method
```

### Language-Specific Implementation

```
Show me how to implement [SECURITY_FEATURE] following NIST [CONTROL-ID] in [LANGUAGE]:

Requirements:
- Use idiomatic [LANGUAGE] patterns
- Include proper error handling
- Add comprehensive NIST annotations
- Show both basic and advanced implementations

Provide:
1. Basic implementation
2. Production-ready version
3. Unit test example
4. Integration points
```

### Multi-Control Implementation

```
I need to implement a [FEATURE] that satisfies these NIST controls:
- [CONTROL-1]: [DESCRIPTION]
- [CONTROL-2]: [DESCRIPTION]
- [CONTROL-3]: [DESCRIPTION]

Show me an implementation that:
1. Satisfies all controls
2. Properly tags each control
3. Avoids conflicts between controls
4. Includes necessary evidence markers
```

---

## Code Review Prompts

### Compliance Review

```
Review the following code for NIST 800-53r5 compliance:

[INSERT CODE]

Check for:
1. Missing NIST tags for security features
2. Incorrectly tagged controls
3. Incomplete implementations
4. Security vulnerabilities
5. Evidence collection gaps

Provide:
- Line-by-line analysis
- Severity rating for each issue
- Specific fix recommendations
```

### Control Validation

```
Validate that the following code correctly implements NIST control [CONTROL-ID]:

[INSERT CODE]

Verify:
1. All control requirements are met
2. Implementation is complete
3. Tags are accurate
4. Evidence is collectible
5. No security gaps

Output:
- Compliance status: [COMPLIANT/PARTIAL/NON-COMPLIANT]
- Specific issues found
- Required changes
```

### Security Pattern Analysis

```
Analyze this codebase for security patterns and their NIST control coverage:

[INSERT CODE OR FILE LIST]

Identify:
1. Security patterns present
2. Associated NIST controls
3. Coverage percentage
4. Missing patterns for moderate baseline
5. Over-engineering (unnecessary controls)
```

---

## Evidence Generation Prompts

### Evidence Documentation

```
Generate evidence documentation for NIST control [CONTROL-ID] based on this implementation:

[INSERT CODE]

Create:
1. Control narrative (how it's implemented)
2. Test procedures
3. Expected results
4. Artifact locations
5. Continuous monitoring approach
```

### Test Evidence Creation

```
Create test cases that demonstrate compliance with NIST control [CONTROL-ID]:

Implementation:
[INSERT CODE]

Generate:
1. Unit test cases with @evidence tags
2. Integration test scenarios
3. Security test cases
4. Performance/stress tests (if applicable)
5. Test documentation
```

### Configuration Evidence

```
Document configuration settings that implement NIST control [CONTROL-ID]:

System: [SYSTEM TYPE]
Current config:
[INSERT CONFIG]

Provide:
1. Security-relevant settings
2. NIST control mapping
3. Validation commands
4. Monitoring queries
5. Change management process
```

---

## Gap Analysis Prompts

### Baseline Gap Analysis

```
Perform a gap analysis against NIST 800-53r5 [LOW/MODERATE/HIGH] baseline:

Current implementations:
[LIST IMPLEMENTED CONTROLS OR INSERT CODE]

Identify:
1. Missing required controls
2. Partially implemented controls
3. Priority order for remediation
4. Effort estimates
5. Quick wins vs long-term projects
```

### Control Family Analysis

```
Analyze coverage for NIST control family [FAMILY-CODE] (e.g., AC, AU, IA):

Codebase summary:
[DESCRIBE APPLICATION]

Current controls:
[LIST CURRENT CONTROLS]

Provide:
1. Family coverage percentage
2. Missing critical controls
3. Implementation recommendations
4. Dependencies between controls
5. Phased implementation plan
```

### Risk-Based Gap Analysis

```
Identify high-risk gaps in NIST compliance for a [APPLICATION TYPE]:

Security requirements:
- Data sensitivity: [HIGH/MEDIUM/LOW]
- User base: [INTERNAL/EXTERNAL/MIXED]
- Deployment: [CLOUD/ON-PREM/HYBRID]

Current controls:
[LIST CONTROLS]

Prioritize gaps by:
1. Security risk
2. Compliance impact
3. Implementation complexity
4. Business criticality
```

---

## Documentation Prompts

### SSP Section Generation

```
Generate System Security Plan (SSP) content for NIST control [CONTROL-ID]:

Implementation details:
[DESCRIBE IMPLEMENTATION]

Code references:
[LIST FILES AND FUNCTIONS]

Create:
1. Control description
2. Implementation narrative
3. Responsible parties
4. Related controls
5. Continuous monitoring approach
```

### Control Mapping Documentation

```
Create a control mapping document for [APPLICATION/MODULE]:

Features:
[LIST SECURITY FEATURES]

Generate:
1. Feature-to-control mapping table
2. Implementation status
3. Evidence locations
4. Testing procedures
5. Maintenance requirements
```

### Developer Guide Creation

```
Write a developer guide for implementing NIST controls in our [PROJECT TYPE]:

Tech stack: [LIST TECHNOLOGIES]
Baseline: [LOW/MODERATE/HIGH]

Include:
1. Quick reference card
2. Common patterns
3. Tagging guidelines
4. Testing requirements
5. Code examples
```

---

## Usage Examples

### Example 1: Reviewing Authentication Code

```
Prompt:
Review the following authentication function for NIST compliance and suggest appropriate control tags:

```python
def login(username, password):
    user = db.get_user(username)
    if user and check_password(password, user.password_hash):
        session['user_id'] = user.id
        return redirect('/dashboard')
    return render_template('login.html', error='Invalid credentials')
```

Expected Output:

- Missing @nist ia-2 tag for authentication
- Missing @nist au-2 for audit logging
- Missing @nist ac-7 for failed attempt handling
- Missing @nist si-10 for input validation
- Suggested implementation improvements for each control

```

### Example 2: Implementation Guidance Request
```

Prompt:
Show me how to implement password complexity validation for NIST ia-5.1 in Python with proper annotations.

Expected Output:
[Complete implementation with regex patterns, error messages, and test cases]

```

### Example 3: Gap Analysis
```

Prompt:
My web application has the following NIST controls implemented:

- ia-2 (basic authentication)
- au-2 (some logging)
- sc-8 (HTTPS)

What controls am I missing for moderate baseline, and which should I prioritize?

Expected Output:
[Prioritized list with implementation effort and risk ratings]

```

---

## Best Practices for Using These Prompts

1. **Be Specific**: Include actual code, not descriptions
2. **Provide Context**: Mention language, framework, and environment
3. **Iterate**: Use follow-up prompts to refine suggestions
4. **Validate**: Always verify LLM suggestions against official NIST documentation
5. **Customize**: Adapt prompts to your specific technology stack

## Integration with Development Workflow

```bash
# Example: Pre-commit hook using LLM
#!/bin/bash
# Get changed files
files=$(git diff --cached --name-only)

# For each file, run compliance check
for file in $files; do
    if [[ $file == *.py ]] || [[ $file == *.js ]] || [[ $file == *.go ]]; then
        # Use LLM to check for missing NIST tags
        llm_response=$(curl -X POST https://api.llm.com/v1/chat \
            -H "Content-Type: application/json" \
            -d "{
                \"prompt\": \"Review this code for missing NIST tags: $(cat $file)\",
                \"model\": \"compliance-assistant\"
            }")

        # Parse and display suggestions
        echo "NIST suggestions for $file:"
        echo "$llm_response"
    fi
done
```

---

## Prompt Templates for CI/CD

### PR Review Template

```yaml
name: NIST Compliance Review
prompt: |
  Review this pull request for NIST 800-53r5 compliance:

  Changed files:
  ${{ github.event.pull_request.changed_files }}

  Diff:
  ${{ github.event.pull_request.diff }}

  Check for:
  1. New security features without NIST tags
  2. Modified security code with outdated tags
  3. Removed security controls
  4. Compliance impact

  Generate review comment with findings.
```

### Automated Documentation

```yaml
name: Generate Control Evidence
prompt: |
  Based on the NIST tags in this codebase:

  Files: ${{ inputs.files }}

  Generate:
  1. Control implementation summary
  2. Evidence inventory
  3. Test coverage report
  4. Missing evidence identification

  Format as markdown for SSP inclusion.
```

---

## Continuous Improvement

These prompts should be:

- Updated as NIST standards evolve
- Customized for your organization
- Refined based on LLM performance
- Extended for new use cases
- Validated against real implementations

Remember: LLMs are assistants, not authorities. Always verify suggestions against official NIST documentation and security best practices.
