# NIST SP 800-207 Zero Trust Architecture Compliance Checklist

This checklist helps organizations assess their zero-trust implementation against NIST SP 800-207 guidelines.

## Legend

- ✅ Implemented
- ⚠️ Partially Implemented
- ❌ Not Implemented
- N/A Not Applicable

---

## 1. Zero Trust Tenets (Section 2.1)

### 1.1 All Data Sources and Computing Services are Resources

- [ ] All applications identified and inventoried
- [ ] All services catalogued with owners
- [ ] All data stores classified by sensitivity
- [ ] IoT/edge devices included in asset inventory
- [ ] Cloud resources tracked and monitored

### 1.2 All Communication is Secured

- [ ] mTLS enabled for service-to-service communication
- [ ] TLS 1.3 (or 1.2 minimum) for all external communication
- [ ] No unencrypted internal traffic
- [ ] Certificate rotation automated
- [ ] Strong cipher suites configured

### 1.3 Access Granted Per-Session Basis

- [ ] No persistent credentials or long-lived tokens
- [ ] Session tokens have defined TTL
- [ ] Re-authentication required after timeout
- [ ] Session revocation mechanism in place
- [ ] Continuous session validation implemented

### 1.4 Access Determined by Dynamic Policy

- [ ] Policy engine deployed (e.g., OPA)
- [ ] Policies include user identity, device health, risk score
- [ ] Context-aware authorization (location, time, behavior)
- [ ] Policies updated dynamically based on risk
- [ ] Policy versioning and audit trail maintained

### 1.5 Monitor and Measure Asset Security Posture

- [ ] Continuous monitoring of all assets
- [ ] Device health checks automated
- [ ] Security posture scoring implemented
- [ ] Compliance checks automated
- [ ] Real-time alerting on posture degradation

### 1.6 Dynamic and Strict Resource Authentication

- [ ] Strong authentication for all resource access
- [ ] Multi-factor authentication enforced
- [ ] Workload identities (SPIFFE/SPIRE) deployed
- [ ] Authentication logs centralized
- [ ] Failed authentication attempts monitored

### 1.7 Collect Information About Current State

- [ ] Comprehensive asset inventory
- [ ] Network traffic analysis enabled
- [ ] Security telemetry collected
- [ ] Behavioral analytics implemented
- [ ] Threat intelligence integration

---

## 2. Zero Trust Architecture Components (Section 3)

### 2.1 Policy Engine (PE)

- [ ] Policy engine deployed and operational
- [ ] Integrates with identity provider
- [ ] Accesses device posture data
- [ ] Considers resource sensitivity
- [ ] Calculates risk scores
- [ ] High availability configuration
- [ ] Performance monitoring enabled

**Policy Engine Location:** ___________________
**Technology Used:** ___________________

### 2.2 Policy Administrator (PA)

- [ ] Policy administrator deployed
- [ ] Generates session-specific tokens
- [ ] Communicates with policy engine
- [ ] Instructs policy enforcement points
- [ ] Logs all authorization decisions
- [ ] Session management implemented

**Policy Administrator Location:** ___________________
**Technology Used:** ___________________

### 2.3 Policy Enforcement Point (PEP)

- [ ] PEPs deployed at critical boundaries
- [ ] Enforces communication paths
- [ ] Validates authentication tokens
- [ ] Inspects traffic
- [ ] Terminates unauthorized connections
- [ ] Forwards requests to policy engine
- [ ] Logs all enforcement actions

**PEP Locations:** ___________________
**Technology Used:** ___________________

---

## 3. Trust Algorithm (Section 3.3)

### 3.1 Access Subject

- [ ] User identity verified
- [ ] User roles and attributes collected
- [ ] Historical behavior analyzed
- [ ] Access patterns monitored

### 3.2 Access Resource

- [ ] Resource classification implemented
- [ ] Sensitivity levels defined
- [ ] Resource ownership assigned
- [ ] Access requirements documented

### 3.3 Trust Scoring Inputs

#### User/Subject Attributes

- [ ] Authentication method strength
- [ ] MFA status
- [ ] Account age
- [ ] Previous security violations
- [ ] Role and clearance level

#### Device Attributes

- [ ] Device management status
- [ ] Operating system version
- [ ] Security software status
- [ ] Encryption status
- [ ] Compliance with baseline

#### Network Attributes

- [ ] Source IP reputation
- [ ] Geographic location
- [ ] Network type (corporate, public)
- [ ] VPN/proxy detection

#### Behavioral Attributes

- [ ] Time of access (normal/unusual)
- [ ] Frequency of access
- [ ] Data volume accessed
- [ ] Failed access attempts
- [ ] Anomaly detection

#### Resource Attributes

- [ ] Data classification level
- [ ] Regulatory requirements
- [ ] Business criticality
- [ ] Access history

### 3.4 Trust Score Calculation

- [ ] Trust algorithm documented
- [ ] Weights assigned to each input
- [ ] Threshold values defined
- [ ] Algorithm regularly reviewed and updated
- [ ] Explainable decisions (audit trail)

**Trust Algorithm Version:** ___________________
**Last Review Date:** ___________________

---

## 4. Zero Trust Architecture Deployment Models (Section 4)

Select your deployment model(s):

### 4.1 Device Agent/Gateway-Based Deployment

- [ ] Agents installed on devices
- [ ] Gateway deployed for agentless devices
- [ ] Agent/gateway communicates with policy engine
- [ ] Certificate or token-based authentication
- [ ] Agent health monitoring

### 4.2 Enclave-Based Deployment

- [ ] Security enclaves defined
- [ ] Micro-perimeters established
- [ ] Gateway controls enclave access
- [ ] Internal enclave traffic monitored
- [ ] Least privilege access enforced

### 4.3 Resource Portal-Based Deployment

- [ ] Access portal deployed
- [ ] All resource access through portal
- [ ] Strong authentication enforced
- [ ] Session management implemented
- [ ] User activity logged

### 4.4 Device Application Sandboxing

- [ ] Applications sandboxed
- [ ] Sandbox policies enforced
- [ ] Communication controlled
- [ ] Data leakage prevention
- [ ] Monitoring and logging enabled

---

## 5. Identity and Access Management (IAM)

### 5.1 Identity Management

- [ ] Centralized identity provider
- [ ] Single Sign-On (SSO) implemented
- [ ] Identity lifecycle management
- [ ] Role-based access control (RBAC)
- [ ] Attribute-based access control (ABAC)

### 5.2 Multi-Factor Authentication

- [ ] MFA required for all users
- [ ] MFA for privileged accounts mandatory
- [ ] Multiple MFA methods supported
- [ ] MFA bypass prevention
- [ ] MFA enrollment monitored

### 5.3 Workload Identity

- [ ] SPIFFE/SPIRE deployed
- [ ] Service accounts managed
- [ ] Certificate-based authentication
- [ ] Automatic certificate rotation
- [ ] Identity attestation implemented

---

## 6. Network Segmentation and Microsegmentation

### 6.1 Network Segmentation

- [ ] Network zones defined
- [ ] Traffic between zones controlled
- [ ] Ingress/egress rules documented
- [ ] Segment isolation tested

### 6.2 Microsegmentation

- [ ] Kubernetes NetworkPolicies deployed
- [ ] Default deny policies in place
- [ ] Explicit allow rules documented
- [ ] Service-to-service communication controlled
- [ ] Layer 7 policies implemented (if applicable)

### 6.3 East-West Traffic Security

- [ ] Internal traffic encrypted (mTLS)
- [ ] Service mesh deployed
- [ ] Authorization policies enforced
- [ ] Traffic inspection enabled
- [ ] Anomaly detection on internal traffic

---

## 7. Encryption and Data Protection

### 7.1 Data in Transit

- [ ] All external traffic encrypted (TLS 1.3)
- [ ] All internal traffic encrypted (mTLS)
- [ ] Strong cipher suites enforced
- [ ] Certificate management automated
- [ ] Legacy protocols disabled

### 7.2 Data at Rest

- [ ] Database encryption enabled
- [ ] File system encryption enabled
- [ ] Backup encryption enabled
- [ ] Key management solution deployed
- [ ] Encryption key rotation automated

### 7.3 Key Management

- [ ] Centralized key management
- [ ] Hardware Security Module (HSM) used
- [ ] Key access controlled and logged
- [ ] Key rotation policy enforced
- [ ] Key recovery procedures documented

---

## 8. Continuous Monitoring and Analytics

### 8.1 Security Monitoring

- [ ] SIEM deployed
- [ ] All logs centralized
- [ ] Real-time alerting configured
- [ ] Security dashboards available
- [ ] Incident response plan documented

### 8.2 Behavioral Analytics

- [ ] User behavior analytics (UBA) implemented
- [ ] Entity behavior analytics (EBA) implemented
- [ ] Anomaly detection configured
- [ ] Machine learning models trained
- [ ] Baseline behavior established

### 8.3 Threat Detection

- [ ] Threat intelligence feeds integrated
- [ ] Indicators of Compromise (IoC) monitoring
- [ ] Automated threat response
- [ ] Threat hunting conducted regularly
- [ ] Vulnerability scanning automated

### 8.4 Metrics and KPIs

- [ ] Zero-trust metrics defined
- [ ] KPIs tracked and reported
- [ ] Policy effectiveness measured
- [ ] Security posture score calculated
- [ ] Continuous improvement process

**Key Metrics Tracked:**

- Authorization decision latency: _______
- Policy violations per day: _______
- Mean time to detect (MTTD): _______
- Mean time to respond (MTTR): _______
- Coverage percentage: _______

---

## 9. Governance and Compliance

### 9.1 Policy Management

- [ ] Zero-trust policies documented
- [ ] Policy ownership assigned
- [ ] Regular policy review scheduled
- [ ] Policy change management process
- [ ] Policy exceptions tracked and approved

### 9.2 Compliance

- [ ] Regulatory requirements mapped
- [ ] Compliance controls implemented
- [ ] Regular compliance audits conducted
- [ ] Compliance reporting automated
- [ ] Non-compliance remediation process

### 9.3 Risk Management

- [ ] Risk assessment conducted
- [ ] Residual risks documented
- [ ] Risk acceptance process
- [ ] Regular risk reviews
- [ ] Risk register maintained

---

## 10. Automation and Orchestration

### 10.1 Policy Automation

- [ ] Policy deployment automated
- [ ] Policy testing automated
- [ ] Policy rollback capability
- [ ] Infrastructure as Code (IaC) for policies
- [ ] GitOps workflow for policy management

### 10.2 Certificate Management

- [ ] Certificate issuance automated
- [ ] Certificate renewal automated
- [ ] Expiration monitoring
- [ ] Revocation process automated
- [ ] Certificate inventory maintained

### 10.3 Incident Response Automation

- [ ] Automated threat containment
- [ ] Automated evidence collection
- [ ] Automated notification
- [ ] Playbooks for common scenarios
- [ ] Post-incident analysis automated

---

## 11. User Experience and Adoption

### 11.1 User Experience

- [ ] Transparent authentication where possible
- [ ] Minimal user friction
- [ ] Clear error messages
- [ ] Self-service portal available
- [ ] User feedback collected

### 11.2 Training and Awareness

- [ ] Zero-trust training provided
- [ ] Security awareness program
- [ ] Role-specific training
- [ ] Regular refresher training
- [ ] Training effectiveness measured

### 11.3 Support

- [ ] Help desk trained on zero-trust
- [ ] Support documentation available
- [ ] Escalation process defined
- [ ] User satisfaction tracked
- [ ] Common issues documented

---

## 12. Resilience and Recovery

### 12.1 High Availability

- [ ] Policy engine redundancy
- [ ] Policy administrator redundancy
- [ ] PEP redundancy
- [ ] Disaster recovery plan
- [ ] Regular failover testing

### 12.2 Degradation Handling

- [ ] Fail-secure defaults configured
- [ ] Graceful degradation strategy
- [ ] Emergency access procedures
- [ ] Break-glass accounts secured
- [ ] Degradation monitoring

### 12.3 Backup and Recovery

- [ ] Configuration backup automated
- [ ] Policy backup automated
- [ ] Recovery procedures documented
- [ ] Recovery tested regularly
- [ ] Recovery time objectives (RTO) defined

---

## Summary Scorecard

| Category | Total Items | Implemented | Percentage |
|----------|-------------|-------------|------------|
| Zero Trust Tenets | ___ | ___ | ___% |
| Architecture Components | ___ | ___ | ___% |
| Trust Algorithm | ___ | ___ | ___% |
| IAM | ___ | ___ | ___% |
| Network Segmentation | ___ | ___ | ___% |
| Encryption | ___ | ___ | ___% |
| Monitoring | ___ | ___ | ___% |
| Governance | ___ | ___ | ___% |
| Automation | ___ | ___ | ___% |
| User Experience | ___ | ___ | ___% |
| Resilience | ___ | ___ | ___% |
| **TOTAL** | **___** | **___** | **___%** |

---

## Maturity Level Assessment

Based on your scorecard, assess your zero-trust maturity:

**Level 1: Traditional (0-25%)**

- Perimeter-based security
- Limited visibility
- Static policies

**Level 2: Initial (26-50%)**

- Some zero-trust components
- Basic encryption
- Manual processes

**Level 3: Intermediate (51-75%)**

- Core zero-trust implemented
- Good coverage
- Some automation

**Level 4: Advanced (76-90%)**

- Comprehensive zero-trust
- High automation
- Continuous improvement

**Level 5: Optimal (91-100%)**

- Full zero-trust coverage
- Mature processes
- Industry-leading practices

**Your Current Maturity Level:** ___________________

---

## Next Steps and Recommendations

1. **Immediate Actions (0-3 months):**
   - _______________________________________________
   - _______________________________________________
   - _______________________________________________

2. **Short-term Goals (3-6 months):**
   - _______________________________________________
   - _______________________________________________
   - _______________________________________________

3. **Long-term Goals (6-12 months):**
   - _______________________________________________
   - _______________________________________________
   - _______________________________________________

---

## Appendix: References

- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final)
- [NIST SP 800-53: Security and Privacy Controls](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [CISA Zero Trust Maturity Model](https://www.cisa.gov/zero-trust-maturity-model)
- [NSA Zero Trust Guidance](https://media.defense.gov/2021/Feb/25/2002588479/-1/-1/0/CSI_EMBRACING_ZT_SECURITY_MODEL_UOO115131-21.PDF)

**Assessment Completed By:** ___________________
**Date:** ___________________
**Next Review Date:** ___________________
