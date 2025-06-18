# NIST Gap Analysis Prompt

## Purpose
Use this prompt to identify missing NIST controls and prioritize implementation efforts.

## The Prompt

```
Perform a NIST 800-53r5 gap analysis for my application against the [MODERATE] baseline.

Application Overview:
- Type: [WEB_APPLICATION/API/MICROSERVICE/MOBILE_APP]
- Authentication: [DESCRIBE CURRENT AUTH]
- Authorization: [DESCRIBE CURRENT AUTHZ]
- Data Sensitivity: [PUBLIC/INTERNAL/CONFIDENTIAL/SECRET]
- User Base: [INTERNAL/EXTERNAL/MIXED]
- Deployment: [CLOUD/ON-PREMISE/HYBRID]

Currently Implemented Controls:
[LIST YOUR IMPLEMENTED CONTROLS OR PASTE SCAN RESULTS]
```
Example:
- ia-2: Basic username/password authentication
- sc-8: HTTPS for all communications
- au-2: Application logs to stdout
```

Security Features in Place:
- [LIST SECURITY FEATURES WITHOUT TAGS]

Please provide:

1. **Coverage Analysis**
   - Percentage of required controls implemented
   - Breakdown by control family (AC, AU, IA, SC, SI, etc.)
   - Visual representation (table or chart)

2. **Critical Gaps** (HIGH PRIORITY)
   - Missing controls that pose immediate risk
   - Why each is critical
   - Potential impact if not implemented
   - Effort estimate (LOW/MEDIUM/HIGH)

3. **Important Gaps** (MEDIUM PRIORITY)
   - Controls that should be implemented soon
   - Business justification
   - Dependencies on other controls
   - Effort estimate

4. **Nice-to-Have Gaps** (LOW PRIORITY)
   - Controls for defense in depth
   - Enhanced security posture
   - Future considerations

5. **Implementation Roadmap**
   - Phased approach (Phase 1, 2, 3)
   - Quick wins (< 1 day effort)
   - Dependencies between controls
   - Resource requirements

6. **Remediation Recommendations**
   For each missing control:
   - Specific implementation approach
   - Technology/library recommendations
   - Integration with existing systems
   - Testing requirements

7. **Risk Assessment**
   - Current risk level
   - Risk reduction after each phase
   - Acceptable risk considerations
```

## Usage Examples

### Example 1: Web Application
```
Perform a NIST 800-53r5 gap analysis for my application against the MODERATE baseline.

Application Overview:
- Type: WEB_APPLICATION
- Authentication: JWT with username/password
- Authorization: Role-based (admin, user)
- Data Sensitivity: CONFIDENTIAL (PII data)
- User Base: EXTERNAL customers
- Deployment: AWS Cloud

Currently Implemented Controls:
- ia-2: JWT authentication
- ac-3: RBAC implementation
- sc-8: TLS 1.3 for all connections
- si-10: Input validation on all forms

Security Features in Place:
- Password hashing with bcrypt
- Session timeout after 30 minutes
- Error messages don't leak information
- Database queries use parameterization
```

### Example 2: API Service
```
Perform a NIST 800-53r5 gap analysis for my application against the MODERATE baseline.

Application Overview:
- Type: REST API
- Authentication: API keys
- Authorization: Scope-based permissions
- Data Sensitivity: INTERNAL (business data)
- User Base: INTERNAL services only
- Deployment: Kubernetes on-premise

Currently Implemented Controls:
- ia-2: API key authentication
- au-2: Structured JSON logging
- sc-8: mTLS between services

Security Features in Place:
- Rate limiting per API key
- Request signing for webhooks
- Metric collection with Prometheus
```

## Expected Output Format

The LLM should provide:

```markdown
# NIST 800-53r5 Gap Analysis Report

## Executive Summary
- Current compliance: X%
- Critical gaps: N controls
- Estimated effort: X person-days
- Risk level: [HIGH/MEDIUM/LOW]

## Coverage Analysis

| Control Family | Required | Implemented | Coverage |
|---------------|----------|-------------|----------|
| AC - Access Control | 15 | 8 | 53% |
| AU - Audit | 8 | 2 | 25% |
| IA - Authentication | 6 | 4 | 67% |
| SC - System Protection | 10 | 7 | 70% |
| SI - System Integrity | 8 | 3 | 38% |

## Critical Gaps (Implement Immediately)

### 1. au-3: Content of Audit Records
- **Risk**: Cannot investigate security incidents
- **Impact**: HIGH - No forensic capability
- **Effort**: LOW (1-2 days)
- **Implementation**: Add structured logging with required fields

### 2. ac-7: Unsuccessful Login Attempts
- **Risk**: Brute force attacks possible
- **Impact**: HIGH - Account compromise
- **Effort**: MEDIUM (3-5 days)
- **Implementation**: Add rate limiting and account lockout

## Implementation Roadmap

### Phase 1: Critical Security (Week 1-2)
1. au-3: Implement structured audit logging
2. ac-7: Add account lockout mechanism
3. ia-5: Enhance password policy
4. si-11: Improve error handling

### Phase 2: Compliance Requirements (Week 3-4)
[Additional phases...]

## Quick Wins (< 1 day each)
1. Add @nist tags to existing security code
2. Enable security headers (X-Frame-Options, etc.)
3. Implement basic rate limiting
4. Add audit log for authentication events
```

## Customization Options

### For Different Baselines
```
Perform analysis against the [LOW/MODERATE/HIGH] baseline.
Note: MODERATE is typical for most applications.
```

### For Specific Industries
```
Include industry-specific requirements:
- Healthcare: HIPAA considerations
- Financial: PCI-DSS overlap
- Government: FISMA requirements
```

### For Resource Constraints
```
Constraints to consider:
- Team size: [NUMBER] developers
- Timeline: [TIMEFRAME]
- Budget: [CONSTRAINTS]
- Technical debt: [DESCRIBE]
```

## Follow-Up Prompts

After receiving the analysis, use these follow-ups:

1. **Deep Dive**: "Provide detailed implementation plan for [SPECIFIC CONTROL]"
2. **Priority Justification**: "Why is [CONTROL] marked as critical?"
3. **Alternative Approaches**: "What are alternative ways to satisfy [CONTROL]?"
4. **Tool Recommendations**: "What tools can help implement these controls?"
5. **Validation**: "How do I verify [CONTROL] is properly implemented?"
