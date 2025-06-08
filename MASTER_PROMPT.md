# Master Prompt for LLM-Optimized Standards Usage

**Purpose:** Efficient prompt templates that leverage the CLAUDE.md routing system
**Token Efficiency:** ~90% reduction through dynamic loading
**Last Updated:** January 2025

---

## 🎯 Core Master Prompt (Ultra-Compact)

```
You are an AI assistant following project standards defined in CLAUDE.md.

Project: Python, PEP8+Black(88), pytest(85%+), Google docstrings

For this task, load relevant standards using the @load syntax from CLAUDE.md.
Prioritize: correctness > security > performance > maintainability

Generate code that is production-ready and follows all loaded standards.
```

---

## 📋 Task-Specific Prompt Templates

### 1. Feature Development
```
Task: [DESCRIBE FEATURE]
Standards: @load [CS:style,arch,security + TS:unit,integration]
Context: [PROJECT CONTEXT]
Constraints: [SPECIFIC REQUIREMENTS]

Generate implementation following loaded standards.
Include: error handling, logging, tests
```

### 2. Bug Fix
```
Issue: [DESCRIBE BUG]
Standards: @load [TS:regression + CS:error-handling]
Context: [ERROR LOGS/STACK TRACE]

Fix the issue and create regression test.
Ensure: root cause addressed, not just symptoms
```

### 3. Performance Optimization
```
Problem: [PERFORMANCE ISSUE]
Standards: @load [CS:performance + OBS:metrics + COST:optimization]
Metrics: [CURRENT VS TARGET]

Optimize while maintaining functionality.
Profile before/after, document improvements.
```

### 4. Security Review
```
Component: [COMPONENT NAME]
Standards: @load [SEC:* + CS:security + TS:security]
Scope: [REVIEW SCOPE]

Perform security review against OWASP Top 10.
Fix vulnerabilities, add security tests.
```

### 5. API Development
```
Endpoint: [API DESCRIPTION]
Standards: @load [CS:api + SEC:api + TS:integration]
Spec: [OPENAPI/REQUIREMENTS]

Implement RESTful endpoint with:
- Input validation
- Error handling  
- Rate limiting
- Documentation
- Tests
```

---

## 🔧 Dynamic Context Loading

### Minimal Context
```
@load CS:style  # Just style guide
```

### Standard Context
```
@load [CS:style,arch + TS:core]  # Common development
```

### Full Domain Context
```
@load [CS:* + TS:* + SEC:relevant]  # Comprehensive
```

### Custom Context
```
@load [CS:3.1,3.4 + TS:4.1 + SEC:auth,crypto]  # Specific sections
```

---

## 🚀 Advanced Prompt Patterns

### 1. Progressive Enhancement
```
Start: @load CS:style
Then: @load CS:architecture (if complexity increases)
Finally: @load CS:performance (if optimization needed)
```

### 2. Domain-Specific Loading
```
If web: @load FE:*
If data: @load DE:*
If cloud: @load CN:*
If distributed: @load EVT:*
```

### 3. Quality Gates
```
Before commit: @load [CS:style + TS:coverage]
Before deploy: @load [SEC:checklist + OBS:monitoring]
Before release: @load [TS:regression + CS:documentation]
```

---

## 📊 Prompt Variables Reference

### Standard Variables
- `[FEATURE]` - Feature description
- `[CONTEXT]` - Project/module context
- `[CONSTRAINTS]` - Specific requirements
- `[METRICS]` - Performance targets

### Loading Variables
- `@load` - Load standards sections
- `:*` - Load entire document
- `:section` - Load specific section
- `[...]` - Load multiple sections

### Output Control
- `Include:` - Required elements
- `Focus:` - Priority areas
- `Skip:` - Exclude from scope
- `Format:` - Output structure

---

## 💡 Example Conversations

### Example 1: Microservice Development
```
Human: Create a user authentication microservice

AI: Loading @load [CS:arch,api + SEC:auth + CN:microservices + TS:integration]
[Generates service following loaded standards]
```

### Example 2: Data Pipeline
```
Human: Build ETL pipeline for customer data

AI: Loading @load [DE:pipelines,quality + CS:error + TS:data]
[Generates pipeline with data quality checks]
```

### Example 3: Frontend Component
```
Human: Create responsive dashboard component

AI: Loading @load [FE:react,performance + CS:style + TS:component]
[Generates React component with tests]
```

---

## 🔍 Quick Reference Mapping

| Task Type | Load Pattern | Focus Areas |
|-----------|--------------|-------------|
| New Feature | CS:all + TS:core | Architecture, tests |
| Bug Fix | TS:regression + CS:error | Root cause, testing |
| Refactor | CS:patterns + TS:* | Clean code, safety |
| Security | SEC:* + TS:security | Vulnerabilities |
| Performance | CS:perf + OBS:metrics | Bottlenecks, metrics |
| API | CS:api + SEC:api | REST, validation |
| Frontend | FE:* + TS:ui | Components, UX |
| Data | DE:* + TS:data | Quality, pipelines |
| Infrastructure | DOP:* + CN:k8s | Terraform, K8s |
| CI/CD | DOP:cicd + GH:* | Pipelines, GitOps |
| Platform | DOP:platform + CN:* | IDP, self-service |

---

## 🚨 Prompt Best Practices

### DO:
- Specify exact standards sections needed
- Include context about the project phase
- Define clear success criteria
- Request tests with implementation
- Ask for documentation updates

### DON'T:
- Load all standards unnecessarily
- Ignore project-specific context
- Skip security considerations
- Forget about error handling
- Omit performance targets

---

## 📝 Custom Organization Templates

For organization-specific standards:
```
@load ORG:security-policy  # Custom organization standards
@load TEAM:api-patterns    # Team-specific patterns
@load PROJECT:conventions  # Project-specific rules
```

---

**Token Usage:** This approach reduces prompt tokens from ~5000 to ~200-500 per request