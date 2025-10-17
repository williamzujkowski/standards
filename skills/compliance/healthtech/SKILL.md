---
name: healthtech-hipaa
category: compliance
difficulty: advanced
compliance_standards:
  - HIPAA
  - HITECH
  - HL7-v2
  - FHIR-R4
version: 1.0.0
last_updated: 2025-10-17
---

# HealthTech HIPAA Compliance Skill

> **LEGAL DISCLAIMER**: This document provides educational guidance on HIPAA compliance requirements and is not legal advice. Healthcare organizations must consult with qualified healthcare compliance attorneys and privacy officers to ensure full regulatory compliance. HIPAA regulations are complex and fact-specific; implementation must be tailored to your organization's specific circumstances.

## Level 1: Quick Reference (~1000 tokens)

### HIPAA Overview

**Health Insurance Portability and Accountability Act (HIPAA)** establishes national standards for protecting sensitive patient health information. Enforced by the Office for Civil Rights (OCR) within the U.S. Department of Health and Human Services (HHS).

#### Privacy Rule vs Security Rule

**Privacy Rule (45 CFR Part 160 and Subparts A and E of Part 164)**
- Establishes standards for PHI use and disclosure
- Patient rights: access, amendment, accounting of disclosures
- Minimum necessary standard
- Notice of Privacy Practices (NPP) requirement
- Applies to: health plans, healthcare clearinghouses, healthcare providers

**Security Rule (45 CFR Parts 160, 162, and 164)**
- Protects electronic PHI (ePHI) specifically
- Three safeguard categories: Administrative, Physical, Technical
- Risk analysis and management required
- Workforce security and training mandates
- Incident response procedures

### Protected Health Information (PHI)

**18 HIPAA Identifiers** that constitute PHI when linked to health information:

1. Names (full name, last name + initial)
2. Geographic subdivisions smaller than state
3. Dates (except year) - birth, admission, discharge, death
4. Telephone numbers
5. Fax numbers
6. Email addresses
7. Social Security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers (VINs, license plates)
13. Device identifiers and serial numbers
14. URLs
15. IP addresses
16. Biometric identifiers (fingerprints, voiceprints)
17. Full-face photographs
18. Any other unique identifying characteristic

**De-identification Methods:**
- **Safe Harbor**: Remove all 18 identifiers
- **Expert Determination**: Statistical/scientific analysis proving re-identification risk is very small

### Business Associate Agreement (BAA) Requirements

**When Required**: Any third party that creates, receives, maintains, or transmits PHI on behalf of a covered entity must sign a BAA.

**Essential BAA Clauses (45 CFR 164.504(e)):**
- Permitted uses and disclosures of PHI
- Prohibition on unauthorized use/disclosure
- Safeguard requirements (administrative, physical, technical)
- Subcontractor BAA requirement
- Individual access rights
- Breach notification obligations (60-day reporting)
- Return or destruction of PHI upon termination
- Audit, inspection, and documentation rights

### Essential Compliance Checklist

```
□ PHI Encryption
  □ Data at rest: AES-256 encryption
  □ Data in transit: TLS 1.2+ (preferably 1.3)
  □ Encrypted backups with key management
  
□ Access Control
  □ Unique user IDs for all personnel
  □ Role-based access control (RBAC)
  □ Multi-factor authentication (MFA) for ePHI access
  □ Emergency access procedures
  □ Automatic logoff after inactivity
  
□ Audit Logs
  □ Log all PHI access and modifications
  □ Retain logs for 6 years minimum
  □ Regular log review and monitoring
  □ Tamper-resistant log storage
  
□ Business Associates
  □ Identify all BAs with PHI access
  □ Execute BAAs before PHI disclosure
  □ Monitor BA compliance
  □ Include BAA termination rights
  
□ Breach Notification
  □ Breach detection and response procedures
  □ 60-day notification timeline to OCR
  □ Individual notification without unreasonable delay
  □ Media notification if >500 residents affected
  
□ Risk Assessment
  □ Annual risk analysis documented
  □ Risk management plan implemented
  □ Ongoing vulnerability scanning
  □ Penetration testing (annual minimum)
```

### Quick Implementation Path

1. **Designate Privacy & Security Officers** (can be same person for small organizations)
2. **Conduct Risk Assessment** - Document all systems containing ePHI
3. **Implement Technical Safeguards** - Encryption, MFA, audit logging
4. **Execute BAAs** - Before any PHI sharing with vendors
5. **Train Workforce** - Annual HIPAA training for all staff
6. **Create Policies & Procedures** - Privacy practices, security incident response
7. **Test & Monitor** - Regular compliance audits and security assessments

### Penalties for Non-Compliance

**HITECH Act Penalty Tiers (per violation):**
- Tier 1 (Unknowing): $100-$50,000
- Tier 2 (Reasonable cause): $1,000-$50,000
- Tier 3 (Willful neglect, corrected): $10,000-$50,000
- Tier 4 (Willful neglect, not corrected): $50,000 minimum

**Annual Maximum**: $1.5 million per violation category

---

## Level 2: Implementation Guide (~5200 tokens)

### HIPAA Privacy Rule (45 CFR Part 160 and Part 164, Subparts A and E)

#### Permitted Uses and Disclosures

**Treatment, Payment, Healthcare Operations (TPO)** - No authorization required:
- **Treatment**: Coordination of care, referrals, consultations
- **Payment**: Billing, claims processing, eligibility verification
- **Healthcare Operations**: Quality assessment, case management, business planning

**Required Disclosures** (only two scenarios):
1. To the individual when they request access to their PHI
2. To HHS for compliance investigation or review

**Permitted Without Authorization:**
- Public health activities (disease reporting, FDA, workplace medical surveillance)
- Victims of abuse, neglect, or domestic violence
- Judicial and administrative proceedings (pursuant to court order)
- Law enforcement purposes (court order, warrant, subpoena, administrative request)
- Decedents (to coroners, medical examiners, funeral directors)
- Cadaveric organ, eye, or tissue donation
- Research (IRB/Privacy Board waiver or de-identified data)
- Serious threat to health or safety
- Essential government functions (military, national security, correctional institutions)
- Workers' compensation

#### Individual Rights

**Right of Access (45 CFR 164.524)**
- Timely access within 30 days (one 30-day extension permitted)
- Reasonable fee for copies (labor, supplies, postage only - not retrieval fees)
- Form and format requested by individual (including electronic)
- Denial rights limited (psychotherapy notes, information compiled for legal proceedings)

**Right to Amend (45 CFR 164.526)**
- Request amendment within 60 days (one 30-day extension)
- Denial permitted if: created by another entity, not part of designated record set, not available for inspection, accurate and complete
- Append individual's statement of disagreement if denied

**Right to Accounting of Disclosures (45 CFR 164.528)**
- 6-year lookback period
- Exclude: TPO, individual-authorized, facility directory, national security
- First accounting free; reasonable fee for subsequent requests within 12 months

**Right to Request Restrictions (45 CFR 164.522)**
- Individual may request restrictions on uses/disclosures
- Covered entity not required to agree (except for self-pay restriction)
- **Self-Pay Restriction**: Must honor request to restrict disclosure to health plan if service paid out-of-pocket in full

**Right to Confidential Communications**
- Request communications by alternative means or locations
- Must accommodate reasonable requests

#### Minimum Necessary Standard

Use, disclose, or request only the minimum PHI necessary to accomplish intended purpose.

**Exceptions** (minimum necessary doesn't apply):
- Disclosures to/requests by healthcare providers for treatment
- Uses/disclosures to the individual
- Uses/disclosures authorized by individual
- Disclosures to HHS for compliance review
- Uses/disclosures required by law

**Implementation:**
- Role-based access controls limiting PHI access by job function
- Routine/recurring disclosures: standard protocols limiting PHI
- Non-routine disclosures: individual review and limitation
- Reasonable reliance on requests from public officials, researchers with documentation

#### Notice of Privacy Practices (NPP)

**Required Content:**
- How PHI may be used and disclosed
- Individual's rights
- Covered entity's duties
- Complaint procedures
- Contact information for privacy officer
- Effective date

**Distribution Requirements:**
- Healthcare providers: provide at first service delivery, good faith effort to obtain written acknowledgment
- Health plans: provide at enrollment, every 3 years thereafter
- Electronic notice: conspicuous posting on website
- Post physical notice in facility

### HIPAA Security Rule (45 CFR Parts 160, 162, and 164)

#### Administrative Safeguards (9 Standards)

**1. Security Management Process (§164.308(a)(1))**

*Required Implementation Specifications:*
- **Risk Analysis**: Regularly assess potential risks and vulnerabilities to ePHI confidentiality, integrity, availability
- **Risk Management**: Implement security measures sufficient to reduce risks to reasonable and appropriate level
- **Sanction Policy**: Apply appropriate sanctions against workforce members who violate security policies
- **Information System Activity Review**: Regularly review audit logs, access reports, security incident tracking

*Risk Analysis Framework:*
```
1. Scope Definition
   - Identify all systems containing ePHI
   - Document data flows (creation, receipt, maintenance, transmission)
   - Map network architecture and access points
   
2. Threat Identification
   - Natural disasters (fire, flood, earthquake)
   - Human threats (malicious insiders, hackers, social engineering)
   - Technical failures (hardware failure, software bugs, power outages)
   
3. Vulnerability Assessment
   - Technical vulnerabilities (unpatched systems, weak authentication)
   - Physical vulnerabilities (unsecured facilities, lost devices)
   - Administrative vulnerabilities (inadequate policies, insufficient training)
   
4. Risk Determination
   - Likelihood: Low, Medium, High
   - Impact: Low, Medium, High
   - Risk Level = Likelihood × Impact
   
5. Control Recommendations
   - Prioritize by risk level
   - Document implementation plan with timelines
   - Assign ownership for each control
```

**2. Assigned Security Responsibility (§164.308(a)(2))**

Designate a Security Official responsible for developing and implementing security policies.

*Typical Responsibilities:*
- Oversee risk assessment and management activities
- Develop, implement, and maintain security policies and procedures
- Coordinate security training programs
- Manage security incident response
- Serve as liaison with Privacy Officer and Compliance Officer
- Report security metrics to executive leadership

**3. Workforce Security (§164.308(a)(3))**

*Required Implementation Specifications:*
- **Authorization and/or Supervision**: Appropriate authorization and supervision of workforce members accessing ePHI

*Addressable Implementation Specifications:*
- **Workforce Clearance**: Determine access authorization based on role
- **Termination Procedures**: Immediately terminate ePHI access upon workforce member departure

*Best Practices:*
- Background checks for positions with ePHI access
- Access authorization forms documenting role and justification
- Termination checklist (disable accounts, retrieve devices, revoke credentials)
- Regular access reviews (quarterly or semi-annually)

**4. Information Access Management (§164.308(a)(4))**

*Required Implementation Specifications:*
- **Isolate Healthcare Clearinghouse Functions**: If entity is a clearinghouse, separate clearinghouse functions from rest of organization

*Addressable Implementation Specifications:*
- **Access Authorization**: Implement policies/procedures for granting access to ePHI
- **Access Establishment and Modification**: Establish, document, review, modify user access rights

*Implementation via RBAC:*
```
Roles by Function:
- Physician: Full patient clinical records, billing read-only
- Nurse: Patient clinical records (assigned patients), no billing
- Billing Staff: Demographics, insurance, billing info - no clinical notes
- Admin Staff: Scheduling, demographics - no clinical or billing
- IT Admin: System access logs, technical data - audited PHI access
- Compliance Officer: Full read access - all access logged and justified
```

**5. Security Awareness and Training (§164.308(a)(5))**

*Addressable Implementation Specifications:*
- **Security Reminders**: Periodic security updates and reminders
- **Protection from Malicious Software**: Procedures for detecting and reporting malware
- **Log-in Monitoring**: Procedures for monitoring log-in attempts and reporting discrepancies
- **Password Management**: Procedures for creating, changing, safeguarding passwords

*Training Requirements:*
- Initial training before ePHI access granted
- Annual refresher training
- Training upon policy changes or new system implementation
- Document completion with signed acknowledgments

*Training Content:*
- HIPAA basics and organizational policies
- PHI identification and handling
- Minimum necessary principle
- Secure email and messaging
- Device security (laptops, smartphones, USB drives)
- Social engineering and phishing recognition
- Incident reporting procedures
- Sanctions for violations

**6. Security Incident Procedures (§164.308(a)(6))**

*Required Implementation Specifications:*
- **Response and Reporting**: Identify and respond to suspected/known security incidents; mitigate harmful effects; document incidents and outcomes

*Incident Categories:*
- **Tier 1 (Critical)**: Confirmed breach of unsecured PHI, ransomware encryption, unauthorized PHI disclosure
- **Tier 2 (High)**: Malware infection, suspected breach, lost/stolen device, unauthorized access attempt
- **Tier 3 (Medium)**: Policy violation, failed access attempt, phishing email received
- **Tier 4 (Low)**: Security question, suspected vulnerability, policy clarification

*Incident Response Process:*
```
1. Detection & Reporting
   - Workforce reports via incident hotline/email
   - Automated alerts from security tools
   - Initial report within 1 hour of discovery
   
2. Containment
   - Isolate affected systems
   - Disable compromised accounts
   - Preserve evidence
   
3. Assessment
   - Determine if PHI was acquired, accessed, used, or disclosed
   - Identify individuals affected
   - Assess risk of harm
   
4. Notification (if breach)
   - Individuals: without unreasonable delay, max 60 days
   - OCR: within 60 days if ≥500 individuals
   - Media: if ≥500 residents of state/jurisdiction
   
5. Mitigation & Remediation
   - Implement corrective actions
   - Update policies/procedures
   - Additional training if needed
   
6. Documentation
   - Incident report with timeline
   - Risk assessment justification if notification not required
   - Remediation actions and outcomes
```

**7. Contingency Plan (§164.308(a)(7))**

*Required Implementation Specifications:*
- **Data Backup Plan**: Establish procedures for creating and maintaining retrievable exact copies of ePHI
- **Disaster Recovery Plan**: Establish procedures to restore lost data
- **Emergency Mode Operation Plan**: Establish procedures to enable continuation of critical business processes while operating in emergency mode

*Addressable Implementation Specifications:*
- **Testing and Revision**: Periodically test and revise contingency plan
- **Applications and Data Criticality Analysis**: Assess criticality of applications and data

*Backup Requirements:*
- **Frequency**: Daily incremental, weekly full backup minimum
- **Scope**: All ePHI systems and databases
- **Storage**: Off-site secure location or encrypted cloud storage
- **Retention**: Align with legal record retention requirements (typically 6+ years)
- **Testing**: Quarterly restore tests from backup media

*Business Continuity Priorities:*
1. **Critical (RTO <4 hours)**: EHR access, pharmacy systems, emergency department systems
2. **Important (RTO <24 hours)**: Lab systems, radiology, scheduling
3. **Normal (RTO <72 hours)**: Billing, administrative systems, reporting

**8. Evaluation (§164.308(a)(8))**

Perform periodic technical and non-technical evaluation in response to environmental or operational changes.

*Evaluation Frequency:*
- Annual comprehensive evaluation minimum
- After significant system changes (new EHR, network redesign)
- After security incidents
- Following risk assessment updates

*Evaluation Components:*
- Review security policies and procedures
- Assess security control effectiveness
- Vulnerability scanning and penetration testing
- Audit log review
- Workforce compliance assessment
- Business associate oversight

**9. Business Associate Contracts (§164.308(b)(1))**

*Required Implementation Specifications:*
- **Written Contract or Other Arrangement**: BAA must document satisfactory assurances that BA will appropriately safeguard PHI

*BAA Required Provisions (45 CFR 164.314(a)(2))* - See BAA template in bundled resources.

#### Physical Safeguards (4 Standards)

**1. Facility Access Controls (§164.310(a)(1))**

*Required Implementation Specifications:*
- **Contingency Operations**: Establish procedures allowing facility access in support of data restoration under contingency plan

*Addressable Implementation Specifications:*
- **Facility Security Plan**: Implement policies/procedures to safeguard facility and equipment from unauthorized physical access
- **Access Control and Validation**: Implement procedures to control and validate access based on role or function
- **Maintenance Records**: Document repairs and modifications to physical components of facility

*Implementation Examples:*
- Controlled access via badge readers or biometric authentication
- Visitor sign-in with escort requirements
- Security cameras in data center and PHI storage areas
- Intrusion detection alarms on data center doors
- Separate locked room for server equipment
- Escort procedures for vendors and contractors

**2. Workstation Use (§164.310(b))**

Implement policies specifying proper workstation functions, manner of performance, physical attributes of surroundings.

*Workstation Security Controls:*
- Privacy screens to prevent visual eavesdropping
- Automatic screen lock after inactivity (5-10 minutes)
- Prohibition of PHI storage on local workstation drives
- Clear desk policy for PHI documents
- Positioning workstations away from public view
- Separate workstations for public-facing areas

**3. Workstation Security (§164.310(c))**

Implement physical safeguards for all workstations accessing ePHI to restrict access to authorized users.

*Technical Implementations:*
- Cable locks for laptops in semi-public areas
- Locked workstations in unoccupied offices
- Prohibition of ePHI access on personal devices (unless MDM-managed)
- Secure destruction of workstations before disposal
- Asset inventory and tracking

**4. Device and Media Controls (§164.310(d)(1))**

*Required Implementation Specifications:*
- **Disposal**: Implement policies/procedures for final disposition of ePHI and hardware/media containing ePHI
- **Media Re-use**: Remove ePHI before re-using media

*Addressable Implementation Specifications:*
- **Accountability**: Maintain record of movements of hardware/media containing ePHI
- **Data Backup and Storage**: Create retrievable, exact copy of ePHI before equipment movement

*Secure Disposal Methods:*
- **Hard Drives**: DoD 5220.22-M wiping (7-pass), degaussing, or physical destruction (shredding)
- **Solid State Drives**: Cryptographic erasure (if encrypted), physical destruction (pulverizing)
- **Optical Media**: Shredding, pulverizing, incinerating
- **Paper Records**: Cross-cut shredding (P-4 standard minimum), pulping, incineration
- **Mobile Devices**: Factory reset + encryption + physical destruction for high-sensitivity devices

*Media Tracking:*
- Asset tag on all portable media devices
- Checkout log for USB drives, external hard drives, backup tapes
- Courier receipts for off-site transport
- Certificate of destruction from disposal vendors

#### Technical Safeguards (5 Standards)

**1. Access Control (§164.312(a)(1))**

*Required Implementation Specifications:*
- **Unique User Identification**: Assign unique identifier for user identity tracking
- **Emergency Access Procedure**: Establish procedure for obtaining ePHI during emergency

*Addressable Implementation Specifications:*
- **Automatic Logoff**: Electronic procedure terminating session after predetermined inactivity
- **Encryption and Decryption**: Mechanism to encrypt/decrypt ePHI

*Access Control Implementation:*

**Unique User IDs:**
- No shared accounts (exception: emergency "break glass" account with full audit logging)
- Username format: firstname.lastname or employee ID
- Prohibition of generic IDs (admin, user, reception)

**Emergency Access:**
- "Break glass" account with elevated privileges
- Requires two-factor authentication
- All access fully logged and reviewed within 24 hours
- Justification documented for each use

**Automatic Logoff:**
- Clinical workstations: 5-10 minutes inactivity
- Administrative workstations: 15 minutes inactivity
- Server/privileged sessions: 5 minutes inactivity
- Screen lock vs. full logoff based on session type

**Encryption:**
- **At Rest**: AES-256 encryption for all ePHI storage (databases, file systems, backups)
- **In Transit**: TLS 1.2+ for all ePHI transmissions (TLS 1.3 preferred)
- **Mobile Devices**: Full-disk encryption (BitLocker, FileVault, native iOS/Android encryption)
- **Email**: S/MIME or PGP for PHI-containing emails (or encrypted portal)
- **Key Management**: Hardware Security Module (HSM) or cloud KMS; key rotation annually

**2. Audit Controls (§164.312(b))**

Implement hardware, software, and/or procedural mechanisms to record and examine activity in information systems containing ePHI.

*Required Audit Log Events:*
- **Authentication**: Login success/failure, logout, password changes
- **Authorization**: Access attempts (successful and denied), permission changes
- **PHI Access**: Record views, searches, retrievals, reports generated
- **PHI Modifications**: Creates, updates, deletes (with before/after values)
- **Administrative Actions**: User account changes, policy updates, configuration changes
- **Security Events**: Malware detection, intrusion attempts, firewall blocks

*Audit Log Fields (minimum):*
- Date and timestamp (synchronized to authoritative time source)
- User ID performing action
- Event type (login, view record, modify data, etc.)
- Success or failure indication
- Resource accessed (patient ID, record type, system component)
- Source IP address or workstation identifier
- Query details (for database access)

*Audit Log Management:*
- **Retention**: 6 years minimum (align with HIPAA record retention requirements)
- **Protection**: Read-only access for audit logs; tamper-evident storage
- **Review**: Regular review by security officer (weekly for high-risk systems, monthly for others)
- **Automated Monitoring**: SIEM rules for anomalies (after-hours access, bulk downloads, terminated user activity)
- **Secure Storage**: Centralized logging server with restricted access; encrypted transmission

**3. Integrity (§164.312(c)(1))**

Implement policies/procedures to protect ePHI from improper alteration or destruction.

*Addressable Implementation Specifications:*
- **Mechanism to Authenticate ePHI**: Implement electronic mechanisms to corroborate ePHI has not been altered or destroyed

*Integrity Controls:*
- Checksums and hash values for critical ePHI datasets
- Version control for ePHI records with change tracking
- Digital signatures for authentication of document integrity
- Audit logs tracking all modifications (who, what, when)
- Database transaction logging with rollback capability
- Regular integrity verification scans

**4. Person or Entity Authentication (§164.312(d))**

Implement procedures to verify person or entity seeking ePHI access is who they claim to be.

*Authentication Methods (in order of strength):*

1. **Multi-Factor Authentication (MFA)** - Required for remote access, recommended for all ePHI access
   - Something you know (password)
   - Something you have (smartphone app, hardware token, smart card)
   - Something you are (biometric: fingerprint, facial recognition)

2. **Single Sign-On (SSO)** with strong authentication
   - SAML 2.0 or OAuth 2.0/OIDC federation
   - Centralized identity provider with MFA
   - Session timeout and re-authentication policies

3. **Password Authentication** (minimum if MFA not feasible)
   - Minimum 12 characters (14+ preferred)
   - Complexity: uppercase, lowercase, number, special character
   - Password expiration: 90 days (or passphrase-based with no expiration if 20+ characters)
   - Password history: prevent reuse of last 10 passwords
   - Account lockout: 5 failed attempts, 30-minute lockout duration

*Entity Authentication:*
- Certificate-based authentication for system-to-system communication
- API keys with secure generation, storage, and rotation
- Service accounts with unique identifiers and restricted privileges

**5. Transmission Security (§164.312(e)(1))**

*Addressable Implementation Specifications:*
- **Integrity Controls**: Implement security measures to ensure ePHI transmission is not improperly modified
- **Encryption**: Implement mechanism to encrypt ePHI during transmission

*Transmission Protection:*

**Network Transmission:**
- TLS 1.2+ for all ePHI transmissions (TLS 1.3 preferred)
- Disable SSLv3, TLS 1.0, TLS 1.1 (known vulnerabilities)
- VPN (IPsec or SSL/TLS) for remote access
- Encrypted email gateway for PHI-containing emails

**Email Security:**
- Do not send unencrypted PHI via standard email
- Options: S/MIME encryption, PGP encryption, secure portal with download link, encrypted email gateway
- Training on identifying PHI in email subject lines (common violation)

**Mobile Devices:**
- Mobile Device Management (MDM) for organization-owned devices
- Encrypted containerization for PHI access on mobile devices
- Remote wipe capability for lost/stolen devices
- Prohibition of PHI in SMS/text messages

**Fax Transmission:**
- Dedicated fax machines in secure locations
- Cover sheet warning about confidential content
- Verification of recipient fax number before transmission
- Confirmation receipt for critical PHI transmissions
- eFax solutions with encryption and secure delivery

### HL7 v2 Messaging Standards

**HL7 v2** (Health Level 7 Version 2) is the most widely used healthcare messaging standard for electronic data exchange between healthcare systems.

#### Common HL7 v2 Message Types

- **ADT (Admission, Discharge, Transfer)**: Patient demographics, encounter management
  - A01: Admit/Visit Notification
  - A03: Discharge/End Visit
  - A04: Register a Patient
  - A08: Update Patient Information
  
- **ORM (Order)**: Orders for medications, labs, procedures
  - O01: Order Message
  
- **ORU (Observation Result)**: Lab results, diagnostic reports
  - R01: Unsolicited Observation Message
  
- **SIU (Scheduling)**: Appointment scheduling and updates
  - S12: Notification of New Appointment
  - S13: Notification of Appointment Rescheduling
  
- **DFT (Detailed Financial Transaction)**: Billing and charges
  - P03: Post Detail Financial Transaction

#### HL7 v2 Security Considerations

**PHI in HL7 Messages:**
- Patient Identification (PID segment): Name, DOB, SSN, MRN, address
- Next of Kin (NK1 segment): Family member information
- Diagnosis (DG1 segment): Diagnosis codes and descriptions
- Observation Results (OBX segment): Lab values, clinical observations

**Security Controls:**
- **Encryption**: TLS for HL7 message transmission over MLLP (Minimal Lower Layer Protocol)
- **Authentication**: Certificate-based authentication for HL7 interface connections
- **Access Control**: Restrict HL7 interface access to authorized systems only
- **Audit Logging**: Log all HL7 message transmissions with sender/receiver identification
- **Message Validation**: Schema validation and business rule validation before processing
- **Error Handling**: Secure error messages without exposing PHI in logs

### FHIR R4 (Fast Healthcare Interoperability Resources)

**FHIR** (pronounced "fire") is a modern RESTful API standard for healthcare data exchange, developed by HL7 International. FHIR R4 is the current normative version.

#### FHIR Core Resources (PHI-containing)

**Patient Resource**: Demographics and patient identity
```json
{
  "resourceType": "Patient",
  "id": "example",
  "identifier": [{"system": "http://hospital.example.org/mrn", "value": "12345"}],
  "name": [{"family": "Smith", "given": ["John"]}],
  "gender": "male",
  "birthDate": "1970-01-01",
  "address": [{"line": ["123 Main St"], "city": "Anytown", "state": "CA", "postalCode": "12345"}]
}
```

**Observation Resource**: Clinical findings and measurements
```json
{
  "resourceType": "Observation",
  "id": "glucose",
  "status": "final",
  "code": {"coding": [{"system": "http://loinc.org", "code": "15074-8", "display": "Glucose"}]},
  "subject": {"reference": "Patient/example"},
  "effectiveDateTime": "2025-10-17T09:30:00Z",
  "valueQuantity": {"value": 95, "unit": "mg/dL", "system": "http://unitsofmeasure.org", "code": "mg/dL"}
}
```

**Encounter Resource**: Patient care event
**Condition Resource**: Patient conditions and diagnoses
**MedicationRequest Resource**: Prescription orders
**DiagnosticReport Resource**: Lab and imaging reports

#### FHIR Security (SMART on FHIR)

**SMART on FHIR** - Security framework combining OAuth 2.0 and OpenID Connect

**Authentication Flow:**
1. App registers with FHIR server (client ID, redirect URI)
2. User authorizes app via OAuth 2.0 authorization code flow
3. App receives access token with granted scopes
4. App accesses FHIR resources with Bearer token

**FHIR Scopes (patient/user access):**
- `patient/Patient.read` - Read patient demographics
- `patient/Observation.read` - Read patient observations
- `user/Patient.read` - Provider reads any patient
- `user/*.read` - Provider reads all resource types

**HIPAA Compliance for FHIR APIs:**
- **TLS 1.2+ Required**: All FHIR API calls over HTTPS
- **Access Control**: OAuth 2.0 scopes enforcing minimum necessary
- **Audit Logging**: Log all FHIR API requests (user, resource, timestamp, IP)
- **Rate Limiting**: Prevent bulk data extraction abuse
- **BAA Required**: Execute BAA with any app developers accessing FHIR APIs
- **Bulk Data Export**: $export operation with secure delivery and access controls

### Audit Logging Requirements (45 CFR 164.312(b))

#### Required Audit Events

Comprehensive audit logging is critical for HIPAA compliance, breach investigation, and forensic analysis.

**Authentication & Authorization:**
- User login (success/failure, timestamp, source IP)
- User logout or session timeout
- Failed authentication attempts (with lockout triggers)
- Password changes
- MFA enrollment/changes
- Privilege escalation
- Role/permission changes

**PHI Access:**
- Record views (patient ID, user, timestamp, access method)
- Search queries (especially broad searches)
- Report generation (report type, parameters, data included)
- Data exports (CSV, PDF, bulk extracts)
- API calls accessing PHI (endpoint, requester, response code)

**PHI Modifications:**
- Create new records (with initial values)
- Update existing records (with before/after values)
- Delete records (soft delete preferred with audit trail)
- Merge/unmerge patient records

**Administrative Actions:**
- User account creation/modification/deletion
- Security policy changes
- System configuration changes
- Audit log access or export
- Backup/restore operations

**Security Events:**
- Intrusion detection alerts
- Malware detection
- Firewall denials for suspicious traffic
- Unauthorized access attempts
- Data loss prevention (DLP) triggers

#### Audit Log Review Process

**Regular Review Schedule:**
- **Daily**: Critical system logs (authentication failures, administrative actions)
- **Weekly**: High-risk user activity (privileged accounts, terminated employees)
- **Monthly**: Comprehensive review of all PHI access patterns
- **Quarterly**: Statistical analysis for anomaly detection

**Automated Monitoring with SIEM:**
- After-hours PHI access by non-emergency personnel
- Bulk record access (>50 records in single session)
- Access to VIP patient records (executives, celebrities)
- Geographical anomalies (login from unusual location)
- Terminated employee account activity
- Failed login patterns indicating brute-force attacks

**Investigation Triggers:**
- Multiple failed authentication attempts (potential breach)
- PHI access by users without legitimate treatment relationship
- Unusual access patterns (time, volume, or resource type)
- Access to own medical record by employee
- Modifications to audit logs (tampering attempt)

### Breach Notification Requirements (45 CFR 164.400-414)

#### Breach Definition

**Breach**: Acquisition, access, use, or disclosure of unsecured PHI that compromises security or privacy, in a manner not permitted under Privacy Rule.

**Exclusions (not a breach if):**
1. **Unintentional Acquisition/Access** by workforce member acting in good faith, within scope of authority, with no further impermissible use/disclosure
2. **Inadvertent Disclosure** from authorized person to another authorized person at same organization, with no further impermissible use/disclosure
3. **Unable to Retain** - Recipient unable to retain PHI (e.g., wrong fax number but not answered)

#### Breach Risk Assessment

Four-factor analysis to determine if breach notification is required:

1. **Nature and Extent of PHI**
   - Types of identifiers involved (SSN, financial data more sensitive)
   - Clinical information sensitivity (mental health, HIV status, substance abuse)
   
2. **Unauthorized Person**
   - Who gained access? (insider vs. external hacker)
   - Likelihood of re-disclosure or misuse
   
3. **Was PHI Actually Acquired or Viewed?**
   - Evidence of actual viewing vs. potential access
   - Forensic analysis results
   
4. **Risk of Harm Mitigation**
   - Was PHI encrypted, rendered unusable?
   - Were other safeguards in place limiting risk?

**Presumption**: Impermissible use/disclosure is a breach unless low probability that PHI was compromised (burden on covered entity to demonstrate).

#### Notification Timelines

**Individual Notification:**
- **Timeline**: Without unreasonable delay, no later than 60 days after breach discovery
- **Method**: First-class mail or email (if individual agreed to electronic notice)
- **Substitute Notice** (if contact info insufficient for <10 individuals, conspicuous posting on homepage for 90 days + media notice if available)

**Required Content:**
- Brief description of what happened
- Types of PHI involved
- Steps individuals should take to protect themselves
- What organization is doing to investigate, mitigate harm, protect against future breaches
- Contact information for questions

**OCR Notification:**
- **≥500 Individuals**: Notify HHS Office for Civil Rights within 60 days of breach discovery (concurrent with individual notification)
- **<500 Individuals**: Maintain log, submit annually to OCR (within 60 days of calendar year end)

**Media Notification:**
- **≥500 Residents of State/Jurisdiction**: Notice to prominent media outlet serving area (same timeline as individual notification)

**Business Associate Notification:**
- BA must notify covered entity within 60 days of discovering breach of unsecured PHI
- Covered entity responsible for notifications to individuals, OCR, and media

#### Breach Notification Template

See `resources/breach-response-playbook.md` for detailed breach notification procedures and templates.

### HITECH Act Enforcement and Penalties

**Health Information Technology for Economic and Clinical Health (HITECH) Act** (2009) strengthened HIPAA enforcement and expanded breach notification requirements.

#### Key HITECH Provisions

**Direct Business Associate Liability:**
- Business associates directly liable for HIPAA compliance (before HITECH, liability was indirect via contracts)
- OCR may investigate and penalize BAs directly

**Expanded Breach Notification:**
- Mandatory breach notification for unsecured PHI
- "Harm threshold" replaced with "low probability" standard
- Wall of Shame: OCR posts breaches ≥500 individuals on public website

**Increased Penalties:**
- Four-tier penalty structure based on culpability
- Mandatory penalties for willful neglect
- State attorneys general may enforce HIPAA

**Meaningful Use Incentives:**
- Electronic health record (EHR) adoption incentives
- Security requirements tied to funding

#### Penalty Tiers (per 45 CFR 160.404)

**Tier 1: Unknowing**
- Individual/entity did not know (and exercising reasonable diligence would not have known) of violation
- Minimum: $100 per violation
- Maximum: $50,000 per violation
- Annual Cap: $25,000 per violation type (updated to $1.5M after regulations aligned)

**Tier 2: Reasonable Cause**
- Violation due to reasonable cause, not willful neglect
- Minimum: $1,000 per violation
- Maximum: $50,000 per violation
- Annual Cap: $1.5 million per violation type

**Tier 3: Willful Neglect (Corrected)**
- Violation due to willful neglect, but corrected within 30 days
- Minimum: $10,000 per violation
- Maximum: $50,000 per violation
- Annual Cap: $1.5 million per violation type

**Tier 4: Willful Neglect (Not Corrected)**
- Violation due to willful neglect, not corrected within 30 days
- Minimum: $50,000 per violation
- Maximum: $50,000 per violation
- Annual Cap: $1.5 million per violation type

**Additional Considerations:**
- Each individual's PHI improperly accessed can constitute a separate violation
- Breaches can result in penalties across multiple categories (Privacy Rule, Security Rule, Breach Notification)
- Criminal penalties possible under HIPAA: $50,000-$250,000 fines and 1-10 years imprisonment for knowing violations

#### Notable HIPAA Settlements

- **Anthem Inc. (2018)**: $16 million - 78.8 million individual breach, lack of encryption
- **Premera Blue Cross (2020)**: $6.85 million - 10.4 million individual breach
- **University of Texas MD Anderson Cancer Center (2018)**: $4.3 million - unencrypted devices
- **Memorial Healthcare System (2017)**: $5.5 million - impermissible disclosures to media
- **Cottage Health (2018)**: $3 million - unauthorized PHI disclosure to outside parties

### Compliance Audit Preparation

#### OCR Audit Protocol Phases

**Phase 1: Desk Audit (Remote)**
- Document requests (policies, procedures, risk assessments, training records)
- Review submitted documentation
- May resolve at this phase or escalate to Phase 2

**Phase 2: On-Site Investigation**
- In-person site visit
- Interview workforce members
- Technical security assessment
- Review systems and physical security
- Evidence collection

#### Audit Readiness Documentation

**Essential Documents to Maintain:**

1. **Security Risk Assessment**
   - Current risk assessment (annual updates minimum)
   - Risk management plan with implementation tracking
   - Historical risk assessments showing progression

2. **Policies and Procedures**
   - HIPAA Privacy and Security policies (comprehensive coverage of all standards)
   - Incident response procedures
   - Breach notification procedures
   - Contingency plan (backup, disaster recovery, emergency mode)
   - Sanction policy

3. **Business Associate Agreements**
   - Executed BAAs for all business associates
   - BA tracking log (BA name, services provided, BAA execution date)
   - BA compliance oversight documentation (audits, reviews, assessments)

4. **Training Records**
   - Training materials and curricula
   - Attendance records with signatures and dates
   - New hire training within 30 days of hire
   - Annual refresher training for all workforce

5. **Access Controls**
   - User access authorization forms (role, justification, approval)
   - Access review logs (quarterly or semi-annual reviews)
   - Termination access revocation documentation

6. **Audit Logs**
   - 6 years of audit log retention
   - Regular audit log review documentation
   - Incident investigation reports

7. **Physical Security**
   - Facility access controls (badge systems, visitor logs)
   - Workstation security controls
   - Device and media disposal records (certificates of destruction)

8. **Breach Notification**
   - Breach log (all incidents assessed, even if notification not required)
   - Risk assessment documentation for each incident
   - Notification letters sent to individuals, OCR, and media (if applicable)
   - Remediation actions taken post-breach

#### Common Audit Findings

**Privacy Rule Violations:**
- Failure to provide timely access to records (30-day requirement)
- No Notice of Privacy Practices or outdated NPP
- Minimum necessary standard not implemented
- Inadequate authorization forms for disclosures

**Security Rule Violations:**
- No risk assessment or outdated risk assessment
- Inadequate access controls (shared passwords, no unique user IDs)
- Missing or incomplete audit logs
- No encryption for ePHI (addressable, but requires documentation if not implemented)
- Inadequate workforce training
- Missing or non-compliant BAAs

**Breach Notification Violations:**
- Late notification (>60 days)
- Failure to conduct proper risk assessment
- Incomplete notification letters
- Failure to report to OCR (especially <500 individual breaches in annual log)

#### Audit Response Best Practices

1. **Designate Audit Coordinator** - Single point of contact for OCR
2. **Assemble Audit Team** - Privacy Officer, Security Officer, Legal Counsel, IT Director, Compliance Officer
3. **Document Review** - Organize all requested documents; create index
4. **Gap Analysis** - Identify deficiencies before OCR does; begin remediation immediately
5. **Honesty** - Never misrepresent facts; OCR values transparency and good faith efforts
6. **Corrective Action Plan (CAP)** - If violations found, propose comprehensive CAP with timelines and milestones
7. **Follow-Up** - Implement CAP; provide regular progress reports to OCR

---

## Level 3: Deep Dive Resources

### Official HIPAA Resources

- **HHS Office for Civil Rights (OCR)**: <https://www.hhs.gov/ocr/privacy/index.html>
- **HIPAA Privacy Rule**: <https://www.hhs.gov/hipaa/for-professionals/privacy/index.html>
- **HIPAA Security Rule**: <https://www.hhs.gov/hipaa/for-professionals/security/index.html>
- **Breach Notification Rule**: <https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html>
- **HITECH Act**: <https://www.hhs.gov/hipaa/for-professionals/special-topics/hitech-act-enforcement-interim-final-rule/index.html>

### Technical Standards

- **NIST SP 800-66 Rev. 2**: *Implementing the HIPAA Security Rule* - <https://csrc.nist.gov/publications/detail/sp/800-66/rev-2/final>
- **NIST Cybersecurity Framework**: Healthcare sector implementation
- **HL7 International**: <https://www.hl7.org/>
- **FHIR Specification**: <https://hl7.org/fhir/R4/>
- **SMART on FHIR**: <https://docs.smarthealthit.org/>

### Industry Organizations

- **HITRUST Alliance**: <https://hitrustalliance.net/> - HITRUST CSF (Common Security Framework)
- **EHNAC**: <https://www.ehnac.org/> - Electronic Healthcare Network Accreditation Commission
- **CHIME**: <https://chimecentral.org/> - College of Healthcare Information Management Executives

### Certification Programs

- **Certified in Healthcare Privacy and Security (CHPS)**: AHIMA certification
- **Certified HIPAA Professional (CHP)**: AAPC certification
- **Certified Information Privacy Professional (CIPP/US)**: IAPP certification with healthcare specialization

### Bundled Resources

This skill includes 6 ready-to-use templates and tools:

1. **`resources/hipaa-compliance-checklist.md`** - Comprehensive checklist covering all HIPAA standards
2. **`templates/baa-template.md`** - Legally-structured Business Associate Agreement template
3. **`templates/fhir-resources.json`** - FHIR R4 resource examples (Patient, Observation, Encounter)
4. **`templates/phi-encryption.py`** - AES-256 encryption implementation for PHI
5. **`scripts/audit-log-analyzer.py`** - Automated HIPAA audit log analysis and compliance reporting
6. **`resources/breach-response-playbook.md`** - Step-by-step breach notification playbook with templates

### Skill Progression Path

**Mastery Levels:**

1. **Foundation** (Level 1): Understand HIPAA basics, PHI identification, essential safeguards
2. **Implementation** (Level 2): Implement technical, administrative, and physical safeguards; conduct risk assessments
3. **Expertise** (Level 3): Lead organizational compliance programs; conduct audits; respond to breaches; integrate HL7/FHIR with security

**Related Skills:**
- `security/OWASP` - Web application security (complementary for healthcare apps)
- `security/NIST-CSF` - NIST Cybersecurity Framework (broader security posture)
- `governance/SOC2` - SOC 2 compliance (often pursued alongside HIPAA)
- `data-privacy/GDPR` - GDPR compliance (for international healthcare data)

---

## Updates and Maintenance

**Last Updated**: 2025-10-17

**Change Log:**
- v1.0.0 (2025-10-17): Initial comprehensive HIPAA compliance skill with HITECH Act updates, HL7/FHIR standards integration, and bundled resources

**Regulatory Monitoring:**
HIPAA regulations are subject to updates and guidance changes. Monitor:
- HHS OCR website for new guidance and enforcement actions
- Federal Register for proposed rule changes
- OCR Cybersecurity Newsletter (monthly)

**Skill Maintenance:**
- Review annually for regulatory updates
- Update penalty amounts per inflation adjustments (published annually)
- Incorporate new OCR guidance and audit protocols
- Update technical standards (TLS versions, encryption standards) per evolving best practices

---

**Remember**: HIPAA compliance is an ongoing process, not a one-time project. Establish continuous monitoring, regular training, and periodic assessments to maintain compliance posture.
