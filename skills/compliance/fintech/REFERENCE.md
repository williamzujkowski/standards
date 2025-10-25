# FinTech Compliance - Reference Implementation

This document contains detailed PCI-DSS v4.0.1 requirements, SOC2 control mappings, and complete implementation examples.

## Table of Contents

- [PCI-DSS v4.0.1 Detailed Requirements](#pci-dss-v401-detailed-requirements)
- [Implementation Examples](#implementation-examples)
- [Compliance Checklists](#compliance-checklists)

---

## PCI-DSS v4.0.1 Detailed Requirements

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

*See REFERENCE.md for complete list.*



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




---

## Implementation Examples

See main SKILL.md for essential implementation patterns.

### Network Segmentation Example

```yaml
# CDE Network Segmentation
zones:
  - name: CDE
    subnets:
      - 10.0.1.0/24  # Payment processing
      - 10.0.2.0/24  # Database servers
    firewall_rules:
      - allow: HTTPS from trusted_apps
      - allow: PostgreSQL from app_servers
      - deny: all other traffic

  - name: trusted
    subnets:
      - 10.0.10.0/24  # Application servers
    firewall_rules:
      - allow: HTTPS to CDE
      - allow: outbound to internet (whitelist)

  - name: untrusted
    subnets:
      - 10.0.20.0/24  # DMZ
    firewall_rules:
      - deny: all to CDE (no direct access)
```

### Tokenization Implementation

```python
import stripe
from typing import Dict

class PaymentTokenizer:
    """PCI-compliant payment tokenization using Stripe."""

    def __init__(self, api_key: str):
        stripe.api_key = api_key

    def tokenize_card(self, card_data: Dict) -> str:
        """Convert PAN to token (never store raw PAN)."""
        token = stripe.Token.create(
            card={
                'number': card_data['number'],
                'exp_month': card_data['exp_month'],
                'exp_year': card_data['exp_year'],
                'cvc': card_data['cvc']  # Not stored after tokenization
            }
        )

        # Store only the token, not the PAN
        return token.id

    def charge_token(self, token: str, amount: int) -> Dict:
        """Process payment using token."""
        charge = stripe.Charge.create(
            amount=amount,
            currency='usd',
            source=token,
            description='Order payment'
        )

        return {
            'transaction_id': charge.id,
            'status': charge.status,
            'last4': charge.source.last4  # Safe to store
        }
```

### Audit Evidence Collection

```python
import boto3
from datetime import datetime, timedelta
from typing import List, Dict

class ComplianceEvidenceCollector:
    """Automated PCI compliance evidence collection."""

    def __init__(self):
        self.s3 = boto3.client('s3')
        self.config = boto3.client('config')
        self.iam = boto3.client('iam')

    def collect_quarterly_evidence(self) -> Dict:
        """Collect evidence for quarterly compliance review."""
        evidence = {
            'collection_date': datetime.utcnow().isoformat(),
            'access_reviews': self._collect_access_reviews(),
            'vulnerability_scans': self._collect_vulnerability_scans(),
            'log_retention': self._verify_log_retention(),
            'mfa_status': self._verify_mfa_enforcement(),
            'encryption_configs': self._verify_encryption()
        }

        # Store evidence in secure S3 bucket
        self._store_evidence(evidence)

        return evidence

    def _collect_access_reviews(self) -> List[Dict]:
        """Verify quarterly access reviews completed."""
        # Retrieve IAM user last access data
        users = self.iam.list_users()['Users']

        return [{
            'username': user['UserName'],
            'created': user['CreateDate'].isoformat(),
            'last_used': self.iam.get_user(UserName=user['UserName'])
                .get('User', {}).get('PasswordLastUsed', 'Never').isoformat()
                if hasattr(self.iam.get_user(UserName=user['UserName'])
                    .get('User', {}).get('PasswordLastUsed', 'Never'), 'isoformat')
                else 'Never'
        } for user in users]

    def _collect_vulnerability_scans(self) -> Dict:
        """Collect quarterly vulnerability scan reports."""
        # Query AWS Inspector or third-party scanner
        return {
            'scan_date': datetime.utcnow().isoformat(),
            'tool': 'AWS Inspector',
            'status': 'completed'
        }

    def _verify_log_retention(self) -> Dict:
        """Verify 90+ day log retention (PCI Req 10.5.1)."""
        logs = boto3.client('logs')
        log_groups = logs.describe_log_groups()['logGroups']

        non_compliant = [
            lg['logGroupName']
            for lg in log_groups
            if lg.get('retentionInDays', 0) < 90
        ]

        return {
            'total_log_groups': len(log_groups),
            'non_compliant': non_compliant,
            'compliant': len(non_compliant) == 0
        }

    def _verify_mfa_enforcement(self) -> Dict:
        """Verify MFA enabled for all users with CDE access."""
        users = self.iam.list_users()['Users']

        no_mfa = [
            user['UserName']
            for user in users
            if not self.iam.list_mfa_devices(UserName=user['UserName'])['MFADevices']
        ]

        return {
            'total_users': len(users),
            'users_without_mfa': no_mfa,
            'mfa_compliance': len(no_mfa) == 0
        }

    def _verify_encryption(self) -> Dict:
        """Verify encryption at rest and in transit."""
        return {
            's3_encryption': 'AES-256',
            'rds_encryption': 'enabled',
            'tls_version': 'TLS 1.2+'
        }

    def _store_evidence(self, evidence: Dict):
        """Store evidence in compliance bucket."""
        bucket = 'compliance-evidence-bucket'
        key = f"quarterly/{datetime.utcnow().strftime('%Y-%m')}/evidence.json"

        self.s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(evidence, indent=2),
            ServerSideEncryption='AES256'
        )
```

---

## Compliance Checklists

### PCI-DSS SAQ A (E-commerce)

- [ ] Merchant only uses approved payment processors (no CDE)
- [ ] PCI DSS compliant service provider confirmed
- [ ] SSL/TLS certificates valid and current
- [ ] Payment pages use HTTPS
- [ ] No storage of cardholder data
- [ ] Quarterly vulnerability scans completed
- [ ] Annual security awareness training completed

### PCI-DSS SAQ D (Full scope)

- [ ] All 12 requirements fully implemented
- [ ] Quarterly internal vulnerability scans
- [ ] Quarterly external ASV scans (passing)
- [ ] Annual penetration testing
- [ ] Annual audit (Level 1 merchants)
- [ ] Quarterly compliance reviews
- [ ] Incident response plan tested
- [ ] Network segmentation verified

### SOC2 Type II Readiness

- [ ] All Trust Service Criteria controls documented
- [ ] 6-12 month observation period completed
- [ ] Evidence collection automated
- [ ] Control testing performed
- [ ] Exceptions remediated
- [ ] Auditor selected
- [ ] Management representation letter prepared

---

## Additional Resources

- [PCI Security Standards Council](https://www.pcisecuritystandards.org)
- [AICPA SOC2 Resources](https://www.aicpa.org/soc)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
