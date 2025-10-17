# PCI-DSS v4.0.1 Complete Compliance Checklist

## Requirement 1: Network Security Controls (8 sub-requirements)

### 1.1 Processes and Mechanisms
- [ ] 1.1.1 Security policies and operational procedures documented
- [ ] 1.1.2 Roles and responsibilities for network security defined

### 1.2 Network Security Controls
- [ ] 1.2.1 Configuration standards for NSCs defined
- [ ] 1.2.2 NSCs restrict connections between untrusted and CDE
- [ ] 1.2.3 Inbound traffic restricted to necessary services only
- [ ] 1.2.4 Outbound traffic from CDE restricted
- [ ] 1.2.5 NSCs installed between wireless and CDE
- [ ] 1.2.6 NSC configuration standards documented
- [ ] 1.2.7 NSC configurations reviewed every six months
- [ ] 1.2.8 NSC configuration files secured

### 1.3 Network Access Restrictions
- [ ] 1.3.1 Inbound traffic to CDE restricted
- [ ] 1.3.2 Outbound traffic from CDE restricted
- [ ] 1.3.3 NSCs between all wireless and CDE

### 1.4 Trusted/Untrusted Network Controls
- [ ] 1.4.1 NSCs between trusted and untrusted networks
- [ ] 1.4.2 Inbound traffic from untrusted networks restricted
- [ ] 1.4.3 Anti-spoofing measures implemented
- [ ] 1.4.4 System components cannot directly access untrusted networks
- [ ] 1.4.5 Application-layer filtering for all traffic

### 1.5 Computing Device Management
- [ ] 1.5.1 Security policies for mobile and remote-access devices

## Requirement 2: Secure Configurations (7 sub-requirements)

### 2.1 Processes and Mechanisms
- [ ] 2.1.1 Security policies documented
- [ ] 2.1.2 Roles and responsibilities defined

### 2.2 System Component Security
- [ ] 2.2.1 Configuration standards developed
- [ ] 2.2.2 Vendor defaults changed before production
- [ ] 2.2.3 Primary functions on separate servers by security level
- [ ] 2.2.4 Only necessary services/protocols enabled
- [ ] 2.2.5 Security features documented and implemented
- [ ] 2.2.6 Security parameters configured to prevent misuse
- [ ] 2.2.7 All non-console admin access encrypted

### 2.3 Wireless Security
- [ ] 2.3.1 Strong cryptography for wireless auth and transmission
- [ ] 2.3.2 Wireless vendor defaults changed

## Requirement 3: Protect Stored Account Data (26 sub-requirements)

### 3.1 Processes and Mechanisms
- [ ] 3.1.1 Security policies documented
- [ ] 3.1.2 Roles and responsibilities defined

### 3.2 Storage Minimization
- [ ] 3.2.1 Account data storage kept to minimum
- [ ] 3.2.2 Sensitive authentication data (SAD) not stored post-authorization

### 3.3 Sensitive Authentication Data Protection
- [ ] 3.3.1 Full track data not retained
- [ ] 3.3.2 CAV2/CVC2/CVV2/CID not stored
- [ ] 3.3.3 PIN/PIN block not stored

### 3.4 PAN Display Restrictions
- [ ] 3.4.1 PAN masked when displayed (max first 6, last 4)
- [ ] 3.4.2 Technical controls restrict PAN display

### 3.5 PAN Protection
- [ ] 3.5.1 PAN rendered unreadable using:
  - [ ] One-way hash (keyed cryptographic)
  - [ ] Truncation (with hash unable to replace truncated segment)
  - [ ] Index tokens with secure storage
  - [ ] Strong cryptography with key management
- [ ] 3.5.2 Disk/partition encryption logical access managed independently

### 3.6 Cryptographic Key Security
- [ ] 3.6.1 Key management procedures implemented
- [ ] 3.6.2 KEKs at least as strong as DEKs
- [ ] 3.6.3 KEKs stored separately from DEKs
- [ ] 3.6.4 Keys stored in fewest possible locations
- [ ] 3.6.5 Key custodian responsibilities documented
- [ ] 3.6.6 Split knowledge and dual control implemented
- [ ] 3.6.7 Key changes for compromised keys
- [ ] 3.6.8 Key replacement when custodian leaves

### 3.7 Cryptography Standards
- [ ] 3.7.1 Keys generated using strong methods
- [ ] 3.7.2 Keys distributed securely
- [ ] 3.7.3 Keys stored securely
- [ ] 3.7.4 Keys changed at end of cryptoperiod
- [ ] 3.7.5 Keys retired/replaced when compromised
- [ ] 3.7.6 Split knowledge for manual clear-text operations
- [ ] 3.7.7 Prevention of unauthorized key substitution
- [ ] 3.7.8 Key custodians formally acknowledge responsibilities
- [ ] 3.7.9 Crypto modules hardened

## Requirement 4: Protect In-Transit Data (4 sub-requirements)

### 4.1 Processes and Mechanisms
- [ ] 4.1.1 Security policies documented
- [ ] 4.1.2 Roles and responsibilities defined

### 4.2 Transmission Protection
- [ ] 4.2.1 Strong cryptography protects PAN during transmission
- [ ] 4.2.1.1 Industry-accepted strong cryptography (TLS 1.2+)
- [ ] 4.2.1.2 Only trusted keys and certificates accepted
- [ ] 4.2.2 PAN not sent via end-user messaging

## Requirement 5: Protect from Malware (12 sub-requirements)

### 5.1 Processes and Mechanisms
- [ ] 5.1.1 Security policies documented
- [ ] 5.1.2 Roles and responsibilities defined

### 5.2 Malware Prevention
- [ ] 5.2.1 Anti-malware on all system components
- [ ] 5.2.2 Anti-malware kept current
- [ ] 5.2.3 Anti-malware actively running
- [ ] 5.2.3.1 Automatic updates and periodic scans

### 5.3 Anti-malware Maintenance
- [ ] 5.3.1 Anti-malware cannot be disabled/altered
- [ ] 5.3.2 Anti-malware logs events
- [ ] 5.3.3 Centrally managed deployment
- [ ] 5.3.4 Detects all known malware
- [ ] 5.3.5 Administrator acknowledges alerts

### 5.4 Phishing Prevention
- [ ] 5.4.1 Technical controls prevent phishing

## Requirement 6: Secure Systems Development (18 sub-requirements)

### 6.1 Processes and Mechanisms
- [ ] 6.1.1 Security policies documented
- [ ] 6.1.2 Roles and responsibilities defined

### 6.2 Secure Software Development
- [ ] 6.2.1 Threat modeling performed
- [ ] 6.2.2 Secure coding techniques applied
- [ ] 6.2.3 Pre-production testing conducted
- [ ] 6.2.4 Security testing before release

### 6.3 Vulnerability Management
- [ ] 6.3.1 Security vulnerabilities identified and prioritized
- [ ] 6.3.2 Patches installed promptly
- [ ] 6.3.3 Software inventory maintained

### 6.4 Web Application Protection
- [ ] 6.4.1 Web apps protected by automated solution
- [ ] 6.4.2 Solution detects and prevents attacks
- [ ] 6.4.3 Payment page scripts managed

### 6.5 Change Management
- [ ] 6.5.1 Changes managed using change control
- [ ] 6.5.2 Change procedures documented
- [ ] 6.5.3 Security impact documented
- [ ] 6.5.4 Approval obtained before implementation
- [ ] 6.5.5 Functionality tested
- [ ] 6.5.6 Implementation documented

## Requirement 7: Restrict Access (9 sub-requirements)

### 7.1 Processes and Mechanisms
- [ ] 7.1.1 Security policies documented
- [ ] 7.1.2 Roles and responsibilities defined

### 7.2 Access Control
- [ ] 7.2.1 Access control model defined
- [ ] 7.2.2 Access based on job function (least privilege)
- [ ] 7.2.3 Privileges assigned based on roles
- [ ] 7.2.4 Access granted with approval
- [ ] 7.2.5 Access reviewed every six months
- [ ] 7.2.6 Access revoked promptly upon termination

### 7.3 Access Control Systems
- [ ] 7.3.1 Systems enforce access requirements
- [ ] 7.3.2 Systems deny access by default
- [ ] 7.3.3 Systems include app and system accounts

## Requirement 8: Identify and Authenticate Users (18 sub-requirements)

### 8.1 Processes and Mechanisms
- [ ] 8.1.1 Security policies documented
- [ ] 8.1.2 Roles and responsibilities defined

### 8.2 User Identification
- [ ] 8.2.1 Unique user ID assigned
- [ ] 8.2.2 Group/shared accounts disabled
- [ ] 8.2.3 Additional auth factors for CDE access
- [ ] 8.2.4 MFA for all CDE access
- [ ] 8.2.5 MFA systems prevent misuse
- [ ] 8.2.6 Auth factors periodically changed

### 8.3 Strong Authentication
- [ ] 8.3.1 All non-console admin access uses MFA
- [ ] 8.3.2 Strong cryptography authenticates users
- [ ] 8.3.3 Strong cryptography for remote access
- [ ] 8.3.4 MFA for all CDE access

### 8.4 Multi-Factor Authentication
- [ ] 8.4.1 MFA for all CDE access
- [ ] 8.4.2 MFA for all remote network access
- [ ] 8.4.3 MFA for app and system accounts

### 8.5 MFA Configuration
- [ ] 8.5.1 MFA prevents replay attacks

### 8.6 Application and System Accounts
- [ ] 8.6.1 Accounts use strong authentication
- [ ] 8.6.2 Passwords changed periodically
- [ ] 8.6.3 Passwords protected

## Requirement 9: Restrict Physical Access (20 sub-requirements)

### 9.1 Processes and Mechanisms
- [ ] 9.1.1 Security policies documented
- [ ] 9.1.2 Roles and responsibilities defined

### 9.2 Physical Access Controls
- [ ] 9.2.1 Controls manage facility entry
- [ ] 9.2.2 Controls distinguish visitors from personnel
- [ ] 9.2.3 Personnel restricted to authorized areas
- [ ] 9.2.4 Visitors authorized and escorted
- [ ] 9.2.5 Visitors identified with badge
- [ ] 9.2.6 Controls for public network jacks
- [ ] 9.2.7 Network jack access restricted

### 9.3 Personnel and Visitor Access
- [ ] 9.3.1 Mechanisms distinguish personnel from visitors
- [ ] 9.3.2 Sensitive area access authorized
- [ ] 9.3.3 Access revoked upon termination
- [ ] 9.3.4 Visitor logs maintained

### 9.4 Media Access
- [ ] 9.4.1 All media physically secured
- [ ] 9.4.2 All media classified
- [ ] 9.4.3 External media shipments secured
- [ ] 9.4.4 Management approval for media removal
- [ ] 9.4.5 External media shipment logs maintained
- [ ] 9.4.6 Hard-copy media destroyed properly
- [ ] 9.4.7 Electronic media destroyed properly

### 9.5 POI Device Protection
- [ ] 9.5.1 POI devices protected from tampering
- [ ] 9.5.2 Periodic inspections for tampering
- [ ] 9.5.3 Personnel trained on tampering detection
- [ ] 9.5.4 POI devices inventoried

## Requirement 10: Log and Monitor (22 sub-requirements)

### 10.1 Processes and Mechanisms
- [ ] 10.1.1 Security policies documented
- [ ] 10.1.2 Roles and responsibilities defined

### 10.2 Audit Logs
- [ ] 10.2.1 Logs capture:
  - [ ] 10.2.1.1 User identification
  - [ ] 10.2.1.2 Type of event
  - [ ] 10.2.1.3 Date and time
  - [ ] 10.2.1.4 Success/failure indication
  - [ ] 10.2.1.5 Event origination
  - [ ] 10.2.1.6 Identity of affected resource
- [ ] 10.2.2 Logs record privileged user actions

### 10.3 Log Protection
- [ ] 10.3.1 Logs cannot be altered
- [ ] 10.3.2 Logs protected from unauthorized mods
- [ ] 10.3.3 Logs promptly backed up centrally
- [ ] 10.3.4 FIM or change detection on logs

### 10.4 Log Review
- [ ] 10.4.1 Logs reviewed daily
- [ ] 10.4.1.1 Automated mechanisms for reviews
- [ ] 10.4.2 Critical security control logs reviewed daily
- [ ] 10.4.3 Anomalies identified and responded to

### 10.5 Log History
- [ ] 10.5.1 Logs retained for 90+ days
- [ ] 10.5.2 Logs available for immediate analysis

### 10.6 Time Synchronization
- [ ] 10.6.1 Clocks synchronized using time-sync tech
- [ ] 10.6.2 Time from industry-accepted sources
- [ ] 10.6.3 Time-sync settings protected

### 10.7 Failure Detection
- [ ] 10.7.1 Security control failures detected
- [ ] 10.7.2 Failures responded to promptly
- [ ] 10.7.3 Critical control failures alerted

## Requirement 11: Test Security (24 sub-requirements)

### 11.1 Processes and Mechanisms
- [ ] 11.1.1 Security policies documented
- [ ] 11.1.2 Roles and responsibilities defined

### 11.2 Wireless Management
- [ ] 11.2.1 Wireless access points managed
- [ ] 11.2.2 Automated monitoring for unauthorized wireless

### 11.3 Vulnerability Scanning
- [ ] 11.3.1 Internal scans quarterly
- [ ] 11.3.1.1 High-risk/critical vulns resolved
- [ ] 11.3.1.2 Rescans verify resolution
- [ ] 11.3.1.3 Scan tools kept current
- [ ] 11.3.2 External scans quarterly
- [ ] 11.3.2.1 ASV scans quarterly

### 11.4 Penetration Testing
- [ ] 11.4.1 Pen test methodology defined
- [ ] 11.4.2 Internal pen test annually
- [ ] 11.4.3 External pen test annually
- [ ] 11.4.4 Exploitable vulns corrected
- [ ] 11.4.5 Segmentation verified annually
- [ ] 11.4.6 Pen test from within network
- [ ] 11.4.7 Additional segmentation testing

### 11.5 Intrusion Detection
- [ ] 11.5.1 IDS/IPS deployed
- [ ] 11.5.2 Mechanisms kept current

### 11.6 Change Detection
- [ ] 11.6.1 Change-detection deployed
- [ ] 11.6.2 Critical files monitored (FIM)
- [ ] 11.6.3 Automated comparisons
- [ ] 11.6.4 Solutions generate alerts
- [ ] 11.6.5 Solutions configured for CDE
- [ ] 11.6.6 Results reviewed
- [ ] 11.6.7 Personnel respond to alerts

## Requirement 12: Information Security Policy (38 sub-requirements)

### 12.1 Security Policy
- [ ] 12.1.1 Policy established and published
- [ ] 12.1.2 Policy reviewed annually
- [ ] 12.1.3 Policy defines roles
- [ ] 12.1.4 Executive management assigned

### 12.2 Acceptable Use
- [ ] 12.2.1 Acceptable use policies defined

### 12.3 Risk Management
- [ ] 12.3.1 Risk analysis performed annually
- [ ] 12.3.2 Analysis considers PCI DSS impact
- [ ] 12.3.3 Analysis on documented frequency
- [ ] 12.3.4 Analysis includes emerging threats

### 12.4 Compliance Management
- [ ] 12.4.1 Service providers maintain compliance
- [ ] 12.4.2 Service providers acknowledge responsibility

### 12.5 Scope Documentation
- [ ] 12.5.1 Scope documented annually
- [ ] 12.5.2 Scoping assessment annually
- [ ] 12.5.3 Supplemental sampling analysis

### 12.6 Security Awareness
- [ ] 12.6.1 Awareness program established
- [ ] 12.6.2 Training upon hire and annually
- [ ] 12.6.3 Personnel acknowledge policy
- [ ] 12.6.3.1 Training on policies/procedures

### 12.7 Personnel Screening
- [ ] 12.7.1 Background checks before hire

### 12.8 Service Provider Risk Management
- [ ] 12.8.1 Service providers maintain requirement list
- [ ] 12.8.2 Support customer compliance
- [ ] 12.8.3 Processes for reporting failures
- [ ] 12.8.4 Review and test controls quarterly
- [ ] 12.8.5 Maintain PCI DSS documentation

### 12.9 Service Provider Support
- [ ] 12.9.1 Acknowledge responsibility in writing
- [ ] 12.9.2 Support customer info requests

### 12.10 Incident Response
- [ ] 12.10.1 IR plan created
- [ ] 12.10.2 24/7 personnel assigned
- [ ] 12.10.3 Personnel trained on IR
- [ ] 12.10.4 IR tested annually
- [ ] 12.10.5 IDS/IPS monitored 24/7
- [ ] 12.10.6 IR plan updated from lessons learned
- [ ] 12.10.7 IR includes:
  - [ ] Analysis and containment
  - [ ] Forensic preservation
  - [ ] Root cause analysis
  - [ ] Incident documentation
  - [ ] Business continuity

## Validation Procedures

### Monthly Tasks
- Review firewall rules (1.2.7 semi-annual, but monthly recommended)
- Review access logs (10.4.1)
- Verify anti-malware updates (5.2.2)
- Check backup integrity

### Quarterly Tasks
- Internal vulnerability scans (11.3.1)
- External vulnerability scans (11.3.2)
- Access reviews (7.2.5 semi-annual, but quarterly recommended)
- Service provider compliance validation (12.8.4)
- Network wireless scans (11.2.1)

### Annual Tasks
- Penetration testing internal (11.4.2)
- Penetration testing external (11.4.3)
- Security policy review (12.1.2)
- Risk analysis (12.3.1)
- Incident response testing (12.10.4)
- Security awareness training (12.6.2)
- Scope validation (12.5.1)

### Upon Change
- Change management documentation (6.5.1-6.5.6)
- Security impact analysis (6.5.3)
- Configuration updates (2.2.1)

---

**Total Sub-Requirements: 78+**
**Completion Rate Target: 100%**
**Next Audit Date: __________**
