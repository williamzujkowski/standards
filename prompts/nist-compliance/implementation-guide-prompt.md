# NIST Implementation Guide Prompt

## Purpose
Use this prompt when you need detailed guidance on how to implement a specific NIST control in your codebase.

## The Prompt

```
I need to implement NIST 800-53r5 control [CONTROL-ID] in my application.

Context:
- Programming language: [LANGUAGE]
- Framework: [FRAMEWORK]
- Application type: [WEB_APP/API/MICROSERVICE/MOBILE/DESKTOP]
- Current security stack: [LIST ANY SECURITY LIBRARIES/TOOLS]
- Deployment environment: [CLOUD/ON-PREMISE/HYBRID]

Please provide:

1. **Control Overview**
   - What this control requires
   - Why it's important
   - Common implementation patterns

2. **Step-by-Step Implementation**
   - Prerequisites and dependencies
   - Code implementation with @nist tags
   - Configuration requirements
   - Integration points

3. **Code Examples**
   - Basic implementation
   - Production-ready version
   - Error handling
   - Edge cases

4. **Testing Approach**
   - Unit tests to verify the control
   - Integration tests
   - Security tests
   - How to mark tests as evidence

5. **Evidence Collection**
   - What evidence to collect
   - How to collect it automatically
   - Documentation requirements

6. **Common Mistakes**
   - What to avoid
   - Security anti-patterns
   - Performance considerations

7. **Related Controls**
   - Controls that work together
   - Dependencies
   - Potential conflicts
```

## Usage Examples

### Example 1: Implementing Authentication
```
I need to implement NIST 800-53r5 control ia-2 in my application.

Context:
- Programming language: Python
- Framework: FastAPI
- Application type: REST API
- Current security stack: JWT, bcrypt
- Deployment environment: AWS

[Rest of prompt...]
```

### Example 2: Implementing Audit Logging
```
I need to implement NIST 800-53r5 control au-2 and au-3 in my application.

Context:
- Programming language: Node.js
- Framework: Express
- Application type: Web application
- Current security stack: Winston logger, MongoDB
- Deployment environment: Kubernetes

[Rest of prompt...]
```

## Control-Specific Variations

### For Access Control (AC family)
```
Additional requirements:
- Show RBAC and ABAC implementation options
- Include privilege escalation prevention
- Demonstrate least privilege principle
```

### For Audit and Accountability (AU family)
```
Additional requirements:
- Show structured logging format
- Include log rotation and retention
- Demonstrate tamper protection
```

### For System and Communications Protection (SC family)
```
Additional requirements:
- Show encryption implementation
- Include key management
- Demonstrate secure communication patterns
```

## Expected Output Structure

The LLM should provide:

```markdown
## NIST Control [CONTROL-ID]: [CONTROL TITLE]

### Overview
[Brief description of what the control requires and why]

### Implementation in [LANGUAGE/FRAMEWORK]

#### Step 1: [First implementation step]
```language
# @nist [control-id] "[description]"
[CODE EXAMPLE]
```

#### Step 2: [Next step]
[Continue pattern...]

### Production Considerations
[Security hardening, performance, scalability]

### Testing Strategy
```language
# @nist [control-id] "Test evidence"
# @evidence test
[TEST CODE]
```

### Evidence Collection
[How to gather evidence for compliance]

### Common Pitfalls
1. [Pitfall 1]: [How to avoid]
2. [Pitfall 2]: [How to avoid]

### Related Controls
- [RELATED-CONTROL-1]: [How they work together]
- [RELATED-CONTROL-2]: [Dependencies]
```

## Tips for Better Results

1. **Be Specific**: Include actual technology versions
2. **Provide Context**: Describe your security requirements
3. **Ask for Alternatives**: Request multiple implementation approaches
4. **Request Best Practices**: Ask for industry-standard implementations
5. **Include Compliance Context**: Mention any additional compliance requirements
