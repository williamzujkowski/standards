---
name: fintech-compliance
category: compliance
difficulty: advanced
compliance_standards: [PCI-DSS-v4.0.1, SOC2-Type-II]
description: Payment card security, SOC2 compliance, and financial services regulatory requirements
prerequisites: [security-fundamentals, api-security]
related_skills: [cloud-security, audit-logging]
version: 1.0.0
---

# FinTech Compliance Skill

## Overview

Master payment card industry security standards (PCI-DSS v4.0.1), SOC2 Type II compliance, and financial services regulatory requirements for secure payment processing and data protection.

---

## Level 1: Quick Reference (~800-1000 tokens)

### PCI-DSS 12 Requirements Overview

**Build and Maintain Secure Network and Systems**
1. Install and maintain network security controls
2. Apply secure configurations to all system components

**Protect Account Data**
3. Protect stored account data
4. Protect cardholder data with strong cryptography during transmission over open, public networks

**Maintain Vulnerability Management Program**
5. Protect all systems and networks from malicious software
6. Develop and maintain secure systems and software

**Implement Strong Access Control Measures**
7. Restrict access to system components and cardholder data by business need to know
8. Identify users and authenticate access to system components
9. Restrict physical access to cardholder data

**Regularly Monitor and Test Networks**
10. Log and monitor all access to system components and cardholder data
11. Test security of systems and networks regularly

**Maintain Information Security Policy**
12. Support information security with organizational policies and programs

### SOC2 Trust Service Criteria

**Security (Common Criteria)**
- Access controls (logical and physical)
- System operations and change management
- Risk mitigation

**Availability**
- System availability commitments
- Monitoring and incident response

**Confidentiality**
- Data classification and handling
- Confidential information protection

### Merchant Levels

| Level | Annual Transactions | Requirements |
|-------|---------------------|--------------|
| 1     | >6M                 | Annual onsite audit, quarterly network scans |
| 2     | 1M-6M               | Annual SAQ, quarterly network scans |
| 3     | 20K-1M (e-commerce) | Annual SAQ, quarterly network scans |
| 4     | <20K (e-commerce) or <1M (other) | Annual SAQ, quarterly network scans (recommended) |

### Essential Checklist

- [ ] **CDE Segmentation**: Isolate cardholder data environment from other networks
- [ ] **Encryption**: All cardholder data encrypted at rest (AES-256) and in transit (TLS 1.2+)
- [ ] **Tokenization**: Replace PANs with tokens for non-payment operations
- [ ] **Access Control**: Unique user IDs, MFA for all CDE access, least privilege
- [ ] **Logging**: Centralized logging with 90+ day retention, automated monitoring
- [ ] **Vulnerability Management**: Quarterly scans, patch management, secure SDLC
- [ ] **Incident Response**: Documented plan, tested annually, 24/7 monitoring
- [ ] **Physical Security**: Restricted access to data centers, visitor logs, camera surveillance

---

## Level 2: Implementation Guide (~4500-5500 tokens)

### PCI-DSS v4.0.1 Detailed Requirements

#### Requirement 1: Network Security Controls

**1.1 Processes and mechanisms for network security controls**
- 1.1.1 Document security policies and operational procedures
- 1.1.2 Define roles and responsibilities

**1.2 Network security controls (NSCs) configured and maintained**
- 1.2.1 Configuration standards defined and implemented
- 1.2.2 NSCs restrict connections between untrusted networks and CDE
- 1.2.3 NSCs restrict inbound traffic to necessary services
- 1.2.4 NSCs restrict outbound traffic from CDE
- 1.2.5 NSCs installed between wireless and CDE
- 1.2.6 Configuration standards for NSCs documented
- 1.2.7 NSC configurations reviewed at least once every six months
- 1.2.8 Configuration files for NSCs secured

**1.3 Network access to and from CDE restricted**
- 1.3.1 Inbound traffic to CDE restricted
- 1.3.2 Outbound traffic from CDE restricted
- 1.3.3 NSCs installed between all wireless and CDE

**1.4 Network connections between trusted and untrusted networks controlled**
- 1.4.1 NSCs implemented between trusted and untrusted networks
- 1.4.2 Inbound traffic from untrusted networks restricted
- 1.4.3 Anti-spoofing measures implemented
- 1.4.4 System components cannot directly access untrusted networks
- 1.4.5 Application-layer filtering applied to all inbound/outbound traffic

**1.5 Risks to CDE from computing devices managed**
- 1.5.1 Security policies for mobile and remote-access devices

#### Requirement 2: Secure Configurations

**2.1 Processes and mechanisms for secure configurations**
- 2.1.1 Document security policies and operational procedures
- 2.1.2 Define roles and responsibilities

**2.2 System components configured and managed securely**
- 2.2.1 Configuration standards developed for all system components
- 2.2.2 Vendor-supplied defaults changed before production
- 2.2.3 Primary functions requiring different security levels on separate servers
- 2.2.4 Only necessary services, protocols, daemons enabled
- 2.2.5 Security features documented and implemented
- 2.2.6 System security parameters configured to prevent misuse
- 2.2.7 All non-console administrative access encrypted

**2.3 Wireless environments configured and managed securely**
- 2.3.1 Strong cryptography for wireless authentication and transmission
- 2.3.2 Vendor defaults for wireless changed (passwords, SNMP, etc.)

#### Requirement 3: Protect Stored Account Data

**3.1 Processes and mechanisms for protecting stored account data**
- 3.1.1 Document security policies and operational procedures
- 3.1.2 Define roles and responsibilities

**3.2 Storage of account data minimized**
- 3.2.1 Account data storage kept to minimum required
- 3.2.2 Sensitive authentication data not stored after authorization

**3.3 Sensitive authentication data (SAD) not stored after authorization**
- 3.3.1 Full track data not retained
- 3.3.2 CAV2/CVC2/CVV2/CID not stored
- 3.3.3 PIN/PIN block not stored

**3.4 Access to displays of full PAN restricted**
- 3.4.1 PAN masked when displayed (first 6 and last 4 digits max)
- 3.4.2 Technical controls restrict PAN display

**3.5 Primary account number (PAN) secured wherever stored**
- 3.5.1 PAN rendered unreadable using any of:
  - One-way hashes (keyed cryptographic hash)
  - Truncation (hashing cannot replace truncated segment)
  - Index tokens with secure token storage
  - Strong cryptography with key management
- 3.5.2 If disk-level or partition-level encryption used, logical access managed independently

**3.6 Cryptographic keys used to protect stored account data secured**
- 3.6.1 Key management procedures implemented
- 3.6.2 Key-encryption keys at least as strong as data-encryption keys
- 3.6.3 Key-encryption keys stored separately from data-encryption keys
- 3.6.4 Keys stored in fewest possible locations
- 3.6.5 Key custodian responsibilities documented
- 3.6.6 Split knowledge and dual control of keys
- 3.6.7 Cryptographic key changes for keys compromised or suspected
- 3.6.8 Cryptographic keys replaced when personnel with key knowledge leave

**3.7 Cryptography used according to industry standards**
- 3.7.1 Cryptographic keys generated using strong cryptographic methods
- 3.7.2 Keys distributed securely
- 3.7.3 Keys stored securely
- 3.7.4 Cryptographic key changes for keys reaching end of cryptoperiod
- 3.7.5 Cryptographic keys retired or replaced when compromised
- 3.7.6 Split knowledge and dual control used for manual clear-text key operations
- 3.7.7 Prevention of unauthorized substitution of cryptographic keys
- 3.7.8 Key custodians formally acknowledge key custodian responsibilities
- 3.7.9 Hardware and software cryptographic modules hardened

#### Requirement 4: Protect Cardholder Data with Strong Cryptography

**4.1 Processes and mechanisms for protecting in-transit data**
- 4.1.1 Document security policies and operational procedures
- 4.1.2 Define roles and responsibilities

**4.2 PAN protected with strong cryptography during transmission**
- 4.2.1 Strong cryptography and security protocols protect PAN during transmission
- 4.2.1.1 Industry-accepted strong cryptography implemented (TLS 1.2+)
- 4.2.1.2 Only trusted keys and certificates accepted
- 4.2.2 PAN not sent via end-user messaging technologies

#### Requirement 5: Protect from Malicious Software

**5.1 Processes and mechanisms for protecting from malware**
- 5.1.1 Document security policies and operational procedures
- 5.1.2 Define roles and responsibilities

**5.2 Malicious software prevented, detected, and addressed**
- 5.2.1 Anti-malware mechanisms deployed on all system components
- 5.2.2 Anti-malware mechanisms kept current
- 5.2.3 Anti-malware mechanisms actively running
- 5.2.3.1 Automatic updates enabled and periodic scans performed

**5.3 Anti-malware mechanisms and processes active and maintained**
- 5.3.1 Anti-malware mechanisms cannot be disabled or altered
- 5.3.2 Anti-malware mechanisms log events
- 5.3.3 Deployment of anti-malware solutions managed centrally
- 5.3.4 Anti-malware mechanisms detect all known malware
- 5.3.5 Administrator acknowledges anti-malware alerts

**5.4 Phishing attacks prevented**
- 5.4.1 Technical and automated controls prevent phishing attacks

#### Requirement 6: Develop and Maintain Secure Systems

**6.1 Processes and mechanisms for developing and maintaining secure systems**
- 6.1.1 Document security policies and operational procedures
- 6.1.2 Define roles and responsibilities

**6.2 Bespoke and custom software developed securely**
- 6.2.1 Threat modeling performed for bespoke/custom software
- 6.2.2 Secure coding techniques applied
- 6.2.3 Pre-production testing for custom software
- 6.2.4 Manual or automated security testing before release

**6.3 Security vulnerabilities identified and addressed**
- 6.3.1 Security vulnerabilities identified and prioritized
- 6.3.2 Software patches and updates installed promptly
- 6.3.3 Software inventory maintained

**6.4 Public-facing web applications protected**
- 6.4.1 Public-facing web applications protected by automated technical solution
- 6.4.2 Automated technical solution detects and prevents attacks
- 6.4.3 All payment page scripts managed

**6.5 Changes to system components managed securely**
- 6.5.1 Changes to system components managed using change control
- 6.5.2 Change control procedures documented
- 6.5.3 Security impact documented before implementation
- 6.5.4 Approval obtained before implementation
- 6.5.5 Functionality tested before production
- 6.5.6 Change implementation documented

#### Requirement 7: Restrict Access by Business Need to Know

**7.1 Processes and mechanisms for restricting access**
- 7.1.1 Document security policies and operational procedures
- 7.1.2 Define roles and responsibilities

**7.2 Access to system components and data limited by business need to know**
- 7.2.1 Access control model defined
- 7.2.2 Access assignments based on job function (least privilege)
- 7.2.3 Required privileges assigned based on personnel roles
- 7.2.4 Access granted based on approval by authorized personnel
- 7.2.5 All access reviewed and reconfirmed at least every six months
- 7.2.6 All access promptly revoked for terminated users

**7.3 Access to system components and data managed via access control systems**
- 7.3.1 Access control systems configured to enforce access requirements
- 7.3.2 Access control systems deny access by default
- 7.3.3 Access control systems include application and system accounts

#### Requirement 8: Identify Users and Authenticate Access

**8.1 Processes and mechanisms for identifying users and authenticating access**
- 8.1.1 Document security policies and operational procedures
- 8.1.2 Define roles and responsibilities

**8.2 User identification and authentication managed**
- 8.2.1 Unique user ID assigned before access allowed
- 8.2.2 Group, shared, or generic accounts disabled or removed
- 8.2.3 Additional authentication factors implemented for access to CDE
- 8.2.4 MFA implemented for all access to CDE
- 8.2.5 MFA systems configured to prevent misuse
- 8.2.6 Authentication factors periodically changed

**8.3 Strong authentication for users implemented**
- 8.3.1 All individual non-console administrative access uses MFA
- 8.3.2 Strong cryptography authenticates users
- 8.3.3 Strong cryptography for all remote access
- 8.3.4 MFA implemented for all access into CDE

**8.4 Multi-factor authentication (MFA) implemented**
- 8.4.1 MFA implemented for all access to CDE
- 8.4.2 MFA implemented for all remote network access
- 8.4.3 MFA implemented for application and system accounts

**8.5 Multi-factor authentication systems configured to prevent misuse**
- 8.5.1 MFA systems configured to prevent replay attacks

**8.6 Use of application and system accounts strictly controlled**
- 8.6.1 Application and system accounts use strong authentication
- 8.6.2 Passwords for application and system accounts changed periodically
- 8.6.3 Passwords for application and system accounts protected

#### Requirement 9: Restrict Physical Access to Cardholder Data

**9.1 Processes and mechanisms for restricting physical access**
- 9.1.1 Document security policies and operational procedures
- 9.1.2 Define roles and responsibilities

**9.2 Physical access controls manage entry**
- 9.2.1 Physical access controls manage entry to facilities
- 9.2.2 Physical access controls distinguish visitors from personnel
- 9.2.3 Physical access controls for personnel restricted to authorized areas
- 9.2.4 Visitors authorized before entry and escorted
- 9.2.5 All visitors identified with badge
- 9.2.6 Physical access controls for publicly accessible network jacks
- 9.2.7 Access to network jacks restricted

**9.3 Physical access for personnel and visitors authorized and managed**
- 9.3.1 Personnel physical access mechanisms distinguish personnel from visitors
- 9.3.2 Physical access to sensitive areas authorized
- 9.3.3 Physical access revoked immediately upon termination
- 9.3.4 Visitor access logs maintained

**9.4 Media access restricted**
- 9.4.1 All media physically secured
- 9.4.2 All media classified
- 9.4.3 Media sent outside facility secured
- 9.4.4 Management approval obtained before media removal
- 9.4.5 Inventory logs maintained for external media shipments
- 9.4.6 Hard-copy media destroyed when no longer needed
- 9.4.7 Electronic media destroyed when no longer needed

**9.5 Point of interaction (POI) devices protected**
- 9.5.1 POI devices protected from tampering
- 9.5.2 Periodic inspections performed to detect tampering
- 9.5.3 Personnel trained to detect tampering attempts
- 9.5.4 POI devices inventoried and managed

#### Requirement 10: Log and Monitor All Access

**10.1 Processes and mechanisms for logging and monitoring access**
- 10.1.1 Document security policies and operational procedures
- 10.1.2 Define roles and responsibilities

**10.2 Audit logs implemented to support detection**
- 10.2.1 Audit logs capture required information
- 10.2.1.1 User identification
- 10.2.1.2 Type of event
- 10.2.1.3 Date and time
- 10.2.1.4 Success or failure indication
- 10.2.1.5 Origination of event
- 10.2.1.6 Identity or name of affected data/resource
- 10.2.2 Audit logs record all actions taken by privileged users

**10.3 Audit logs protected from destruction and unauthorized modifications**
- 10.3.1 Audit logs cannot be altered
- 10.3.2 Audit logs protected from unauthorized modifications
- 10.3.3 Audit logs promptly backed up to secure centralized location
- 10.3.4 File integrity monitoring or change-detection mechanisms on audit logs

**10.4 Audit logs reviewed to identify anomalies**
- 10.4.1 Audit logs reviewed at least daily
- 10.4.1.1 Automated mechanisms used for log reviews
- 10.4.2 Logs from critical security controls reviewed at least daily
- 10.4.3 Anomalies identified and responded to

**10.5 Audit log history retained and available**
- 10.5.1 Audit logs retained for at least 90 days
- 10.5.2 Audit logs available for immediate analysis

**10.6 Time-synchronization mechanisms support consistent time settings**
- 10.6.1 System clocks and time synchronized using time-synchronization technology
- 10.6.2 Systems acquire time from industry-accepted time sources
- 10.6.3 Time-synchronization settings and data protected

**10.7 Failures of critical security control systems detected and responded to**
- 10.7.1 Additional security control system failures detected
- 10.7.2 Security control failures responded to promptly
- 10.7.3 Failures of critical security controls detected and alerted

#### Requirement 11: Test Security of Systems and Networks

**11.1 Processes and mechanisms for regularly testing security**
- 11.1.1 Document security policies and operational procedures
- 11.1.2 Define roles and responsibilities

**11.2 Wireless access points managed and tested**
- 11.2.1 Authorized and unauthorized wireless access points managed
- 11.2.2 Automated monitoring implemented to detect unauthorized wireless

**11.3 External and internal vulnerabilities identified and addressed**
- 11.3.1 Internal vulnerability scans performed quarterly
- 11.3.1.1 High-risk and critical vulnerabilities resolved
- 11.3.1.2 Rescans performed to verify resolution
- 11.3.1.3 Scan tools kept up to date
- 11.3.2 External vulnerability scans performed quarterly
- 11.3.2.1 Quarterly external scans by PCI SSC Approved Scanning Vendor (ASV)

**11.4 External and internal penetration testing conducted**
- 11.4.1 Penetration testing methodology defined
- 11.4.2 Internal penetration testing performed annually
- 11.4.3 External penetration testing performed annually
- 11.4.4 Exploitable vulnerabilities corrected and testing repeated
- 11.4.5 Network segmentation verified annually
- 11.4.6 Penetration testing from within network performed
- 11.4.7 Additional testing for segmentation controls

**11.5 Network intrusions and unexpected activity detected**
- 11.5.1 Intrusion-detection and/or intrusion-prevention deployed
- 11.5.2 Mechanisms for intrusion detection kept current

**11.6 Unauthorized changes to system components detected**
- 11.6.1 Change-detection mechanism deployed
- 11.6.2 Critical files monitored using file-integrity monitoring (FIM)
- 11.6.3 Automated mechanisms used to perform comparisons
- 11.6.4 Change-detection solutions generate alerts
- 11.6.5 Change-detection mechanisms configured for CDE
- 11.6.6 Results from change-detection solution reviewed
- 11.6.7 Personnel respond appropriately to alerts

#### Requirement 12: Support Information Security with Organizational Policies

**12.1 Comprehensive information security policy established and maintained**
- 12.1.1 Security policy established and published
- 12.1.2 Security policy reviewed at least annually
- 12.1.3 Security policy defines roles and responsibilities
- 12.1.4 Executive management responsibility for information security assigned

**12.2 Acceptable use policies for end-user technologies defined**
- 12.2.1 Acceptable use policies defined for end-user technologies

**12.3 Risks to cardholder data formally identified and managed**
- 12.3.1 Targeted risk analysis performed annually
- 12.3.2 Targeted risk analysis considers impact on PCI DSS
- 12.3.3 Targeted risk analysis performed on documented frequency
- 12.3.4 Targeted risk analysis includes emerging threats

**12.4 PCI DSS compliance managed**
- 12.4.1 Service providers maintain PCI DSS compliance
- 12.4.2 Service providers acknowledge responsibility for CDE security

**12.5 PCI DSS scope documented and validated**
- 12.5.1 PCI DSS scope documented and confirmed annually
- 12.5.2 Scoping assessment performed annually
- 12.5.3 Additional supplemental analysis for sampling

**12.6 Security awareness education for personnel**
- 12.6.1 Security awareness program established
- 12.6.2 Security awareness training provided upon hire and annually
- 12.6.3 Personnel acknowledge reading and understanding security policy
- 12.6.3.1 Personnel trained on security policies and procedures

**12.7 Personnel screened to reduce risk**
- 12.7.1 Background checks conducted before hire for personnel with access to CDE

**12.8 Risk to service provider customers managed**
- 12.8.1 Service providers maintain list of PCI DSS requirements managed by each entity
- 12.8.2 Service providers support customers' compliance
- 12.8.3 Service providers implement processes for reporting failures
- 12.8.4 Service providers review and test PCI DSS controls quarterly
- 12.8.5 Service providers maintain documentation about PCI DSS requirements

**12.9 Service providers support their customers' PCI DSS compliance**
- 12.9.1 Service providers acknowledge responsibility in writing
- 12.9.2 Service providers support customers' requests for information

**12.10 Suspected and confirmed security incidents reported and responded to**
- 12.10.1 Incident response plan created and implemented
- 12.10.2 Specific personnel assigned for incident response 24/7
- 12.10.3 Personnel trained on incident response procedures
- 12.10.4 Incident response procedures tested annually
- 12.10.5 Intrusion detection/prevention monitored 24/7
- 12.10.6 Incident response plan updated based on lessons learned
- 12.10.7 Incident response procedures include:
  - Analysis and containment
  - Forensic evidence preservation
  - Root cause analysis
  - Incident documentation
  - Business continuity procedures

### Cardholder Data Environment (CDE) Segmentation

**Network Segmentation Strategy**

```
┌─────────────────────────────────────────────────┐
│           Corporate Network (Untrusted)         │
│  - Employee workstations                        │
│  - General business applications                │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────▼──────────┐
        │  Perimeter Firewall │
        └─────────┬──────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│              DMZ (Semi-Trusted)                  │
│  - Web application servers                       │
│  - API gateways                                  │
│  - Load balancers                                │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────▼──────────┐
        │   Internal Firewall │
        │   (CDE Boundary)    │
        └─────────┬──────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│    Cardholder Data Environment (CDE)            │
│                                                  │
│  ┌──────────────────┐  ┌──────────────────┐   │
│  │ Payment Gateway  │  │  Database Servers │   │
│  │ (Tokenization)   │  │  (Encrypted PAN)  │   │
│  └──────────────────┘  └──────────────────┘   │
│                                                  │
│  ┌──────────────────┐  ┌──────────────────┐   │
│  │   HSM/Key Mgmt   │  │  Logging/SIEM    │   │
│  └──────────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────┘
```

**Key Segmentation Controls:**
1. Firewall rules whitelist only required protocols (HTTPS, database ports)
2. Network ACLs deny by default, permit by exception
3. VLANs separate CDE from other networks
4. Jump boxes/bastion hosts for administrative access
5. No direct internet access from CDE
6. Annual penetration testing validates segmentation

### Payment Processing Security

**Tokenization Implementation**

```python
# Stripe tokenization (PCI SAQ A compliant)
import stripe
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

# Client-side: Card data never touches your server
# Stripe.js creates token from card details

# Server-side: Only handle token
def process_payment(token, amount):
    try:
        charge = stripe.Charge.create(
            amount=amount,  # Amount in cents
            currency="usd",
            source=token,  # Token from Stripe.js
            description="Product purchase"
        )
        # Store charge ID, never store card data
        return {"success": True, "charge_id": charge.id}
    except stripe.error.CardError as e:
        return {"success": False, "error": e.user_message}
```

**Encryption Requirements**

| Data State | Requirement | Algorithm | Key Length |
|------------|-------------|-----------|------------|
| At Rest    | PAN encrypted | AES | 256-bit minimum |
| In Transit | TLS 1.2+    | ECDHE-RSA-AES256-GCM-SHA384 | 2048-bit RSA minimum |
| Backups    | Encrypted   | AES-256 | 256-bit |
| Key Storage| Encrypted KEK | AES-256 | 256-bit |

**Key Management Lifecycle**

1. **Generation**: FIPS 140-2 Level 2+ HSM
2. **Distribution**: Encrypted channels, split knowledge
3. **Storage**: Separate from encrypted data, access logged
4. **Rotation**: Annual minimum, or upon compromise
5. **Destruction**: Secure deletion per NIST SP 800-88

### SOC2 Type II Compliance

**Trust Service Criteria Mapping**

**CC1: Control Environment**
- Board oversight of security and privacy
- Management philosophy and operating style
- Organizational structure and assignment of authority
- Commitment to competence
- Human resource policies

**CC2: Communication and Information**
- Internal communication channels
- External communication channels
- Information quality
- Management and board reporting

**CC3: Risk Assessment**
- Risk identification and assessment
- Fraud risk assessment
- Risk response and monitoring

**CC4: Monitoring Activities**
- Ongoing and separate evaluations
- Deficiency reporting and remediation

**CC5: Control Activities (Logical and Physical Access)**
- Selection and development of control activities
- Technology controls
- Policies and procedures deployment

**CC6: Logical and Physical Access Controls**
- Prior to issuing credentials, entity registers and authorizes new users
- Credentials and access are removed when access is no longer required
- Entity reviews credentials and access rights
- Physical access restricted to authorized personnel
- Logical access restricted based on least privilege

**CC7: System Operations**
- Change management procedures
- Configuration management
- Incident management
- Backup and recovery procedures

**CC8: Change Management**
- Change authorization and approval
- Testing procedures
- Deployment procedures
- Documentation requirements

**CC9: Risk Mitigation**
- Vulnerability identification and assessment
- Threat protection mechanisms
- Security patch management
- Malware detection and prevention

**A1: Availability**
- Monitoring system capacity and performance
- Environmental protections (fire, flood, temperature)
- Redundancy and failover procedures
- Incident response for availability incidents

**C1: Confidentiality**
- Confidential information identified and classified
- Confidential information encrypted at rest and in transit
- Access to confidential information restricted
- Confidential information disposal procedures

### Audit Readiness and Evidence Collection

**Evidence Requirements by Control Category**

| Control Category | Evidence Types | Collection Frequency |
|------------------|----------------|----------------------|
| Access Control | User provisioning logs, access reviews, MFA configs | Quarterly |
| Change Management | Change tickets, approval records, test results | Per change |
| Encryption | Cipher configurations, key rotation logs, TLS scans | Monthly |
| Logging | Log retention verification, SIEM configurations | Monthly |
| Vulnerability Management | Scan reports, remediation tickets, patch schedules | Quarterly |
| Incident Response | Incident tickets, postmortem reports, tabletop exercises | Per incident |
| Physical Security | Badge logs, visitor logs, camera footage samples | Quarterly |
| Vendor Management | SOC2 reports, SLAs, due diligence assessments | Annually |

**Automated Evidence Collection**

```bash
# Example: Collect access review evidence
#!/bin/bash
EVIDENCE_DIR="/var/audit/evidence/$(date +%Y-%m)"
mkdir -p "$EVIDENCE_DIR"

# User access report
aws iam generate-credential-report
aws iam get-credential-report > "$EVIDENCE_DIR/iam-credentials.json"

# MFA enforcement status
aws iam get-account-summary > "$EVIDENCE_DIR/mfa-status.json"

# Firewall rules
aws ec2 describe-security-groups > "$EVIDENCE_DIR/security-groups.json"

# Encryption status
aws rds describe-db-instances --query 'DBInstances[*].[DBInstanceIdentifier,StorageEncrypted]' \
  > "$EVIDENCE_DIR/rds-encryption.json"

# Log retention verification
aws logs describe-log-groups --query 'logGroups[*].[logGroupName,retentionInDays]' \
  > "$EVIDENCE_DIR/log-retention.json"

# Generate timestamped hash
cd "$EVIDENCE_DIR" && sha256sum * > evidence-integrity.sha256
```

### Compliance Automation

**Continuous Compliance Monitoring Architecture**

```
┌─────────────────────────────────────────────────┐
│           Infrastructure as Code                 │
│  - Terraform/CloudFormation                      │
│  - Policy-as-Code (OPA, Sentinel)                │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────▼──────────┐
        │  CI/CD Pipeline     │
        │  - Compliance gates │
        │  - Security scans   │
        └─────────┬──────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│         Compliance Automation Tools              │
│  - AWS Config Rules                              │
│  - Azure Policy                                  │
│  - Cloud Custodian                               │
│  - Prowler/ScoutSuite                            │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────▼──────────┐
        │   SIEM/SOAR         │
        │   - Splunk          │
        │   - Elasticsearch   │
        │   - Sumo Logic      │
        └─────────┬──────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│          Compliance Dashboard                    │
│  - Real-time control status                      │
│  - Risk scoring                                  │
│  - Audit-ready reports                           │
└─────────────────────────────────────────────────┘
```

**Sample Compliance Rules (AWS Config)**

```python
# Require encryption for RDS instances
def evaluate_compliance(configuration_item):
    if configuration_item["resourceType"] != "AWS::RDS::DBInstance":
        return "NOT_APPLICABLE"
    
    storage_encrypted = configuration_item["configuration"].get("storageEncrypted", False)
    
    if storage_encrypted:
        return "COMPLIANT"
    else:
        return "NON_COMPLIANT"

# Require MFA for root account
def evaluate_mfa_compliance(configuration_item):
    if configuration_item["resourceType"] != "AWS::IAM::User":
        return "NOT_APPLICABLE"
    
    user_name = configuration_item["configuration"]["userName"]
    if user_name != "root":
        return "NOT_APPLICABLE"
    
    mfa_devices = configuration_item["configuration"].get("mfaDevices", [])
    
    if len(mfa_devices) > 0:
        return "COMPLIANT"
    else:
        return "NON_COMPLIANT"
```

### Incident Response for Payment Security

**Critical Incident Types**

1. **Suspected PAN Exposure**
   - Immediate containment: Isolate affected systems
   - Forensic preservation: Snapshot VMs, preserve logs
   - Notification: Payment brands within 72 hours
   - PFI (Payment Forensic Investigator) engagement

2. **CDE Breach**
   - Activate IR team 24/7
   - Preserve evidence (RAM dumps, disk images)
   - Engage legal counsel
   - Notify acquiring bank and card brands
   - Retain PFI for investigation

3. **Authentication Bypass**
   - Immediately revoke compromised credentials
   - Force password resets for affected accounts
   - Review and enhance MFA controls
   - Audit access logs for unauthorized activity

4. **Malware in CDE**
   - Isolate infected systems (network segmentation)
   - Deploy anti-malware tools
   - Scan all CDE components
   - Rebuild compromised systems from known-good images
   - Enhance monitoring for persistence mechanisms

**Compliance Reporting Timeline**

| Incident Type | Notification Deadline | Recipient |
|---------------|----------------------|-----------|
| PAN compromise | 72 hours | Payment brands, acquirer |
| CDE breach | 72 hours | Payment brands, PFI |
| SOC2 control failure | Next report period | Auditor, customers |
| GDPR breach (EU) | 72 hours | Data Protection Authority |
| State breach laws (US) | 30-90 days (varies) | State AG, affected individuals |

---

## Level 3: Deep Dive Resources

### Bundled Resources

1. **`resources/pci-dss-checklist.md`** - Complete 78-sub-requirement checklist with validation procedures
2. **`templates/soc2-control-mappings.yaml`** - SOC2 TSC to implementation control mappings
3. **`templates/tokenization-implementation.py`** - Production-ready Stripe/Braintree tokenization
4. **`templates/network-segmentation.yaml`** - CDE network architecture and firewall rules
5. **`scripts/audit-evidence-collector.sh`** - Automated evidence collection for quarterly audits
6. **`templates/compliance-dashboard.json`** - Grafana dashboard for real-time compliance monitoring

### Official Standards References

- **PCI DSS v4.0.1**: <https://www.pcisecuritystandards.org/document_library>
- **PCI SAQ**: Self-Assessment Questionnaires for merchant levels
- **PA-DSS**: Payment Application Data Security Standard
- **SOC2**: <https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report.html>
- **NIST Cybersecurity Framework**: <https://www.nist.gov/cyberframework>

### Industry Resources

- **PCI SSC**: <https://www.pcisecuritystandards.org>
- **Cloud Security Alliance (CSA)**: <https://cloudsecurityalliance.org>
- **ISACA**: <https://www.isaca.org> (CISA, CRISC certifications)
- **SANS Institute**: Payment card security courses

### Complementary Skills

- **security-fundamentals**: Foundational security principles
- **api-security**: Secure API design for payment endpoints
- **cloud-security**: Cloud-specific compliance (AWS, Azure, GCP)
- **audit-logging**: Centralized logging and SIEM implementation

---

## Quick Win: 30-Minute Compliance Assessment

```bash
# Run automated compliance scan
git clone https://github.com/prowler-cloud/prowler
cd prowler
./prowler aws --compliance pci_dss_v4.0.1

# Check TLS configurations
nmap --script ssl-enum-ciphers -p 443 payment-api.example.com

# Verify log retention
aws logs describe-log-groups | jq '.logGroups[] | select(.retentionInDays < 90)'

# Review IAM MFA enforcement
aws iam get-account-summary | jq '.SummaryMap | {MFADevices, AccountMFAEnabled}'

# Scan for exposed secrets
trufflehog git https://github.com/yourorg/payment-service --json
```

**Expected Outcomes:**
- PCI compliance posture report (automated scan)
- TLS cipher suite compliance verification
- Log retention gap analysis
- MFA enforcement status
- Secret exposure detection

---

*Version: 1.0.0*
*Last Updated: 2025-10-17*
*Compliance Standards: PCI-DSS v4.0.1, SOC2 Type II*
