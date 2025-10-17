# HIPAA Breach Response Playbook

> **LEGAL DISCLAIMER**: This playbook provides guidance for HIPAA breach response procedures. It is not legal advice. Organizations must consult with qualified legal counsel, privacy officers, and compliance professionals when responding to actual breaches.

## Table of Contents

1. [Breach Definition](#breach-definition)
2. [Immediate Response Actions](#immediate-response-actions)
3. [Breach Risk Assessment](#breach-risk-assessment)
4. [Notification Requirements](#notification-requirements)
5. [Notification Templates](#notification-templates)
6. [Post-Breach Activities](#post-breach-activities)
7. [Common Breach Scenarios](#common-breach-scenarios)

---

## Breach Definition

**HIPAA Breach (45 CFR 164.402)**: Acquisition, access, use, or disclosure of unsecured Protected Health Information (PHI) in a manner not permitted under the Privacy Rule that compromises the security or privacy of the PHI.

### What is NOT a Breach

**Three Exceptions** (notification not required):

1. **Unintentional Acquisition/Access** by workforce member acting in good faith, within scope of authority, with no further impermissible use/disclosure

2. **Inadvertent Disclosure** from authorized person to another authorized person at same organization, with no further impermissible use/disclosure

3. **Unable to Retain** - Recipient unable to retain PHI (e.g., wrong fax number but not answered)

### Presumption of Breach

Unless the covered entity or business associate demonstrates a **low probability that PHI was compromised** through the four-factor risk assessment, an impermissible use or disclosure is presumed to be a breach.

---

## Immediate Response Actions

**Timeline: Within 1 Hour of Discovery**

### 1. Activate Incident Response Team

**Core Team Members:**
- Privacy Officer (lead coordinator)
- Security Officer
- Legal Counsel
- IT Security
- Compliance Officer
- Public Relations (if media notification required)
- Executive Leadership (for significant breaches)

**Immediate Actions:**
- Convene emergency meeting (in-person or conference call)
- Brief team on known facts
- Assign roles and responsibilities
- Establish communication protocols

### 2. Contain the Breach

**Technical Containment:**
- Isolate affected systems
- Disable compromised accounts immediately
- Revoke access credentials
- Block unauthorized network connections
- Preserve evidence (do not delete logs or data)

**Physical Containment:**
- Secure physical location where breach occurred
- Retrieve stolen/lost devices if possible
- Lock down areas with PHI exposure
- Control access to breach scene

**Administrative Containment:**
- Notify affected departments
- Implement additional monitoring
- Brief workforce on situation (need-to-know basis)
- Document all containment actions taken

### 3. Preserve Evidence

**Critical Evidence:**
- System logs (authentication, access, modifications)
- Network traffic logs
- Physical security logs (badge access, cameras)
- Email communications
- Device forensics (if device involved)
- Witness statements
- Timeline of events

**Evidence Handling:**
- Create forensic copies of affected systems
- Document chain of custody
- Store evidence securely
- Do not modify original evidence
- Photograph physical evidence
- Record all investigative actions

### 4. Initial Assessment

**Determine:**
- What PHI was involved?
- How many individuals affected?
- Who had unauthorized access?
- When did breach occur?
- How did breach occur?
- Has PHI been acquired or just accessed?
- Is PHI encrypted or otherwise secured?

**Document:**
- Date and time of discovery
- Who discovered the breach
- Initial facts and circumstances
- Systems/locations affected
- Preliminary estimate of individuals affected

---

## Breach Risk Assessment

**Requirement**: Conduct four-factor risk assessment to determine if notification is required (45 CFR 164.402(2)).

### Four-Factor Analysis

**Factor 1: Nature and Extent of PHI Involved**

Assess **types of identifiers**:
- High sensitivity: SSN, financial information, genetic data, mental health records, HIV status, substance abuse treatment
- Medium sensitivity: Medical record number, diagnosis codes, treatment information
- Lower sensitivity: Demographic information only (name, address, date of birth)

Questions:
- What specific PHI elements were involved?
- How sensitive is the clinical information?
- Could the PHI be used for identity theft or fraud?
- Does PHI include highly sensitive diagnoses?

**Factor 2: Unauthorized Person Who Used or Received PHI**

Assess **identity and intent of recipient**:
- Known malicious actor (hacker, identity thief): Higher risk
- Unknown/unintentional recipient (wrong fax, misdirected email): Lower risk
- Business associate or other HIPAA-covered entity: Lower risk
- General public/media: Higher risk

Questions:
- Who is the unauthorized person/entity?
- What is their likely intent (malicious vs. inadvertent)?
- What is the likelihood they will further disclose or misuse PHI?
- Can the recipient be contacted and PHI retrieved?

**Factor 3: Was PHI Actually Acquired or Viewed?**

Assess **evidence of acquisition**:
- Confirmed viewing/download: Higher risk
- Potential access only (no evidence of viewing): Lower risk
- Encrypted PHI accessed without decryption key: Lower risk
- Clear evidence PHI was not accessed: Lower risk

Questions:
- Is there forensic evidence PHI was accessed?
- Can access logs confirm or rule out viewing?
- Was PHI downloaded, printed, or copied?
- Did unauthorized person have opportunity to view PHI?

**Factor 4: Extent to Which Risk Has Been Mitigated**

Assess **mitigation measures**:
- PHI encrypted and key not compromised: Significant mitigation
- Devices remotely wiped after loss: Significant mitigation
- PHI retrieved and destroyed: Significant mitigation
- Business associate agreement in place with recipient: Some mitigation

Questions:
- Was PHI encrypted with strong encryption (AES-256)?
- Was encryption key compromised?
- Has PHI been retrieved or destroyed?
- What safeguards were in place that limited exposure?
- What additional safeguards have been implemented?

### Risk Assessment Conclusion

**Low Probability of Compromise → Breach Notification NOT Required**

Document **detailed justification** for conclusion, addressing all four factors.

**Cannot Demonstrate Low Probability → Breach Notification REQUIRED**

Proceed with notification requirements (Section 4).

### Risk Assessment Documentation Template

```
HIPAA BREACH RISK ASSESSMENT

Incident ID: [Incident Number]
Assessment Date: [Date]
Assessor: [Name, Title]

INCIDENT SUMMARY:
[Brief description of incident]

FOUR-FACTOR ANALYSIS:

Factor 1: Nature and Extent of PHI Involved
PHI Elements: [List specific PHI elements]
Number of Individuals: [Count]
Sensitivity Rating: [High/Medium/Low]
Analysis: [Detailed assessment]

Factor 2: Unauthorized Person
Identity: [Description of unauthorized person/entity]
Intent: [Malicious/Inadvertent/Unknown]
Disclosure Risk: [High/Medium/Low]
Analysis: [Detailed assessment]

Factor 3: PHI Acquisition/Viewing
Evidence of Access: [Yes/No/Unknown]
Forensic Findings: [Summary]
Acquisition Confirmed: [Yes/No/Unknown]
Analysis: [Detailed assessment]

Factor 4: Risk Mitigation
Encryption: [Yes/No - Algorithm, Key Status]
Retrieval: [Yes/No - Details]
Other Safeguards: [Description]
Mitigation Rating: [Significant/Moderate/Minimal/None]
Analysis: [Detailed assessment]

CONCLUSION:
Breach Notification Required: [YES / NO]

Rationale: [Detailed justification for conclusion, synthesizing all four factors]

Approved By:
Privacy Officer: _________________ Date: _______
Legal Counsel: ___________________ Date: _______
```

---

## Notification Requirements

### Timeline Summary

| Notification To | Timeline | Method |
|-----------------|----------|--------|
| Individuals (≥500 affected) | Within 60 days of discovery | First-class mail or email (if agreed) |
| Individuals (<500 affected) | Within 60 days of discovery | First-class mail or email (if agreed) |
| HHS OCR (≥500 affected) | Within 60 days of discovery | OCR Breach Portal |
| HHS OCR (<500 affected) | Within 60 days of calendar year end | OCR Breach Portal (annual log) |
| Media (≥500 in state/jurisdiction) | Within 60 days of discovery | Prominent media outlet |
| Covered Entity (by BA) | Within 60 days of discovery | As specified in BAA |

### Individual Notification Requirements

**Required Content (45 CFR 164.404(c)):**

1. **Brief Description** of what happened, including date of breach and date of discovery

2. **Types of PHI Involved** (e.g., name, SSN, date of birth, medical record number, diagnosis)

3. **Steps Individuals Should Take** to protect themselves from potential harm

4. **What Organization is Doing** to investigate, mitigate harm, and protect against future breaches

5. **Contact Information** for questions (toll-free phone number, email, website, or postal address)

**Plain Language Requirement**: Written at 6th-8th grade reading level, avoiding technical jargon.

**Method:**
- **First-class mail** to last known address
- **Email** if individual agreed to electronic notice AND has not withdrawn consent
- **Substitute notice** if insufficient contact information:
  - <10 individuals: Telephone or other written means
  - ≥10 individuals: Conspicuous posting on homepage for 90 days + notice to media (if available)

### HHS OCR Notification

**≥500 Individuals Affected:**
- Submit via **OCR Breach Reporting Portal**: <https://ocrportal.hhs.gov/ocr/breach/wizard_breach.jsf>
- **Within 60 days** of breach discovery
- **Concurrent** with individual notification

**<500 Individuals Affected:**
- Maintain **breach log** internally
- Submit **annual log** to OCR within 60 days of calendar year end (by March 1)

**Information Required:**
- Organization details (name, address, contact)
- Date of breach and date of discovery
- Number of individuals affected
- Description of breach
- Types of PHI involved
- Brief summary of incident
- Actions taken in response

### Media Notification

**Requirement**: If breach affects **≥500 residents of a state or jurisdiction**

**Method:**
- Notice to **prominent media outlet** serving the state or jurisdiction
- Press release or media advisory

**Timeline**: Within 60 days of breach discovery (same timeline as individual notification)

**Content**: Similar to individual notification (description, PHI types, steps, contact info)

### Business Associate Notification to Covered Entity

**Requirement**: BA must notify CE within **60 days of discovery**

**Content:**
- Identification of each individual whose PHI was breached (or reasonably believed to be breached)
- Date of breach and date of discovery
- Description of breach
- Types of PHI involved
- Any other information CE needs for notification

**Responsibility**: Covered entity remains responsible for individual, OCR, and media notifications (BA notifications are to CE, not directly to individuals/OCR)

---

## Notification Templates

### Template 1: Individual Notification Letter (Mail/Email)

```
[Organization Letterhead]

[Date]

[Individual Name]
[Address]
[City, State ZIP]

Re: Notice of Data Breach

Dear [Individual Name]:

We are writing to inform you of a data breach that may have affected the security of your protected health information (PHI). [Organization Name] takes the privacy and security of your information very seriously. This letter explains the breach, the information involved, what we are doing in response, and steps you can take to protect yourself.

WHAT HAPPENED

On [Date of Breach], [brief description of what happened - e.g., "an unauthorized individual gained access to our computer system" or "a laptop containing patient information was stolen from an employee's vehicle"]. We discovered the breach on [Date of Discovery] when [how breach was discovered].

WHAT INFORMATION WAS INVOLVED

The information that may have been accessed includes:
- [List specific PHI elements: name, date of birth, Social Security number, medical record number, diagnosis, treatment information, etc.]

[If applicable: "At this time, we have no evidence that your information has been misused."]

WHAT WE ARE DOING

We have taken the following steps in response:
- [Action 1 - e.g., "We immediately disabled the compromised accounts and reset all passwords"]
- [Action 2 - e.g., "We notified law enforcement and are cooperating with their investigation"]
- [Action 3 - e.g., "We have implemented additional security measures including enhanced access controls and monitoring"]
- [Action 4 - e.g., "We are offering complimentary credit monitoring and identity theft protection services for [duration]"]

We have also notified the U.S. Department of Health and Human Services as required by federal law.

WHAT YOU CAN DO

We recommend you take the following steps to protect yourself:

1. **Review your credit reports** for any suspicious activity. You are entitled to a free credit report annually from each of the three major credit bureaus. Visit www.annualcreditreport.com or call 1-877-322-8228.

2. **Monitor your medical records and Explanation of Benefits (EOB) statements** from your health insurance for any unfamiliar medical services or charges. Report any discrepancies to your health plan immediately.

3. **Place a fraud alert** on your credit file. Contact one of the three credit bureaus below (contacting one will notify the other two):
   - Equifax: 1-800-525-6285, www.equifax.com
   - Experian: 1-888-397-3742, www.experian.com
   - TransUnion: 1-800-680-7289, www.transunion.com

4. **Consider placing a security freeze** on your credit file, which prevents new credit accounts from being opened in your name without your permission. Contact each credit bureau directly.

5. [If SSN involved: "**Review your Social Security earnings statement** annually to ensure all earnings are accurate and authorized. Visit www.ssa.gov/myaccount/."]

6. [If credit monitoring offered: "**Enroll in complimentary credit monitoring and identity theft protection services** by [date] using the instructions enclosed."]

FOR MORE INFORMATION

We sincerely apologize for this incident and any inconvenience or concern it may cause. If you have questions or would like additional information, please contact us:

- **Phone**: [Toll-free number] ([Hours of operation, Time zone])
- **Email**: [Dedicated breach response email]
- **Website**: [Website with FAQs]
- **Mail**: [Mailing address]

We are committed to protecting the privacy and security of your health information and have taken additional steps to prevent similar incidents in the future.

Sincerely,

[Name]
[Title]
[Organization Name]

Enclosures: [If applicable - credit monitoring enrollment instructions, identity theft resources]
```

### Template 2: Media Notice / Press Release

```
FOR IMMEDIATE RELEASE

[Organization Name] Announces Data Breach Affecting Patient Information

[City, State] – [Date] – [Organization Name] is notifying patients that [brief description of breach - e.g., "a data breach involving unauthorized access to our electronic health records system occurred on [Date of Breach]"].

The breach was discovered on [Date of Discovery] when [how breach was discovered]. [Organization Name] immediately [containment actions taken].

Our investigation determined that the following types of patient information may have been affected: [list PHI types - name, date of birth, medical record number, diagnosis, etc.]. Approximately [number] individuals may have been affected.

[If applicable: "At this time, we have no evidence that patient information has been misused."]

[Organization Name] takes the privacy and security of patient information seriously and deeply regrets this incident. We have [summary of response actions - e.g., "implemented enhanced security measures, provided additional workforce training, and engaged a cybersecurity firm to conduct a comprehensive security assessment"].

Affected individuals are being notified by mail and are encouraged to [key protective actions - e.g., "monitor their credit reports and Explanation of Benefits statements for any suspicious activity"]. [If applicable: "[Organization Name] is offering complimentary credit monitoring and identity theft protection services to affected individuals."]

[Organization Name] has notified the U.S. Department of Health and Human Services and [if applicable] "law enforcement" as required by federal law.

Patients with questions may contact our dedicated helpline at [toll-free number] ([hours of operation, time zone]) or visit [website] for more information.

ABOUT [ORGANIZATION NAME]
[Brief organizational description]

MEDIA CONTACT:
[Name]
[Title]
[Phone]
[Email]

###
```

### Template 3: Substitute Notice (Insufficient Contact Info)

**Homepage Notice (Conspicuous Posting for 90 Days)**

```
NOTICE OF DATA BREACH

[Organization Name] experienced a data breach on [Date] that may have affected the protected health information of some individuals. If you were a patient at [Organization Name] between [date range], your information may have been affected.

We attempted to notify affected individuals by mail, but do not have current contact information for some individuals.

INFORMATION INVOLVED: [List PHI types]

WHAT YOU SHOULD DO:
- Monitor your credit reports and medical statements
- Contact us if you believe you may be affected

FOR MORE INFORMATION:
Phone: [Toll-free number]
Email: [Email address]
Mail: [Mailing address]

This notice will remain posted for 90 days from [Date].
```

---

## Post-Breach Activities

### 1. Root Cause Analysis

**Conduct thorough investigation:**
- What vulnerabilities were exploited?
- How did security controls fail?
- Were policies and procedures followed?
- What human factors contributed?
- Could the breach have been detected earlier?

**Document findings** in detailed incident report.

### 2. Corrective Action Plan (CAP)

**Develop comprehensive CAP addressing:**
- Technical vulnerabilities (patch systems, implement encryption, enhance access controls)
- Policy gaps (update policies, create new procedures)
- Training deficiencies (provide additional workforce training)
- Physical security weaknesses (improve facility security)
- Third-party oversight (enhance business associate monitoring)

**Assign responsibilities and timelines** for each corrective action.

**Track implementation** and report progress to executive leadership.

### 3. Regulatory Compliance

**Cooperate with HHS OCR investigation:**
- Respond to requests for information promptly
- Provide requested documentation
- Allow on-site inspection if requested
- Be transparent and honest

**Prepare for potential penalties:**
- Review penalty tiers (Tier 1-4 based on culpability)
- Engage legal counsel
- Consider settlement negotiations if appropriate

### 4. Stakeholder Communication

**Internal communication:**
- Brief workforce on incident and lessons learned
- Reinforce security awareness
- Recognize individuals who detected/responded to breach

**External communication:**
- Update affected individuals on corrective actions
- Maintain dedicated communication channel for questions
- Issue follow-up communications as appropriate

**Board/executive reporting:**
- Present incident report to board of directors
- Report on CAP implementation
- Provide ongoing risk updates

### 5. Continuous Improvement

**Update security program:**
- Revise risk assessment based on incident findings
- Implement enhanced monitoring and detection
- Conduct additional security assessments
- Test incident response plan

**Lessons learned session:**
- Convene incident response team debrief
- Identify what worked well and what needs improvement
- Update incident response plan
- Document lessons learned for future reference

---

## Common Breach Scenarios

### Scenario 1: Lost/Stolen Unencrypted Device

**Facts:**
- Laptop stolen from employee vehicle
- Contains ePHI of 500 patients
- Laptop not encrypted
- Password-protected but not encrypted

**Risk Assessment:**
- Factor 1: Names, DOB, MRN, diagnoses (Medium-High sensitivity)
- Factor 2: Unknown/potentially malicious (Higher risk)
- Factor 3: Unable to confirm if accessed, but opportunity existed (Higher risk)
- Factor 4: Password protection only, not encrypted (Minimal mitigation)

**Conclusion**: **Breach notification REQUIRED**

**Actions:**
- Notify 500 individuals within 60 days
- Notify HHS OCR within 60 days via Breach Portal
- Notify media (≥500 affected)
- Offer credit monitoring services
- Implement full-disk encryption on all devices (CAP)

---

### Scenario 2: Misdirected Fax

**Facts:**
- Fax with patient information sent to wrong fax number
- 1 patient affected
- Recipient: another medical office (covered entity)
- Recipient notified immediately, confirmed PHI destroyed

**Risk Assessment:**
- Factor 1: Name, DOB, diagnosis, treatment (Medium sensitivity)
- Factor 2: Healthcare provider (covered entity), bound by HIPAA (Lower risk)
- Factor 3: Likely viewed, but no evidence of retention (Medium risk)
- Factor 4: PHI retrieved and destroyed, recipient is HIPAA-covered entity (Significant mitigation)

**Conclusion**: **Low probability of compromise - Breach notification NOT required**

**Documentation**: Detailed risk assessment justification; confirmation of destruction from recipient

**Actions:**
- Document incident in breach log (for annual OCR submission if <500 total for year)
- Implement fax verification procedures (CAP)
- Train workforce on fax security

---

### Scenario 3: Hacking Incident with Encryption

**Facts:**
- Hacker gained access to database server
- Database contains ePHI of 10,000 patients
- Database encrypted with AES-256
- Encryption keys stored on separate, secured system
- No evidence encryption keys were compromised
- Forensic analysis confirms hacker accessed encrypted database files but not keys

**Risk Assessment:**
- Factor 1: Full patient records (High sensitivity)
- Factor 2: Malicious actor (hacker) (Higher risk)
- Factor 3: Encrypted files acquired, but no decryption capability (Lower risk)
- Factor 4: Strong encryption (AES-256), keys not compromised (Significant mitigation)

**Conclusion**: **Low probability of compromise - Breach notification NOT required** (if forensic analysis conclusively shows keys were not compromised)

**Documentation**: Detailed forensic report; encryption strength documentation; key management evidence

**Actions:**
- Document incident in breach log
- Notify HHS OCR if cannot demonstrate low probability
- Enhanced monitoring for unusual activity
- Security vulnerability remediation (CAP)
- Incident response plan testing

---

### Scenario 4: Insider Snooping

**Facts:**
- Employee accessed records of 50 patients without legitimate treatment relationship
- Employee not assigned to care for these patients
- Detected through routine audit log review
- PHI viewed but not printed, downloaded, or disclosed further
- Employee terminated immediately

**Risk Assessment:**
- Factor 1: Full patient records viewed (High sensitivity)
- Factor 2: Former employee, likely curiosity, not malicious intent (Medium risk)
- Factor 3: Confirmed viewing, but no evidence of further disclosure (Higher risk)
- Factor 4: Employee terminated, no evidence of external disclosure (Moderate mitigation)

**Conclusion**: **Breach notification REQUIRED**

**Actions:**
- Notify 50 individuals within 60 days
- Notify HHS OCR (annual log, <500 total for year)
- Disciplinary action (termination) documented
- Enhanced access controls and monitoring (CAP)
- Workforce training on snooping prohibitions

---

## Appendix: Breach Response Checklist

### Phase 1: Immediate Response (0-24 hours)

- [ ] Convene incident response team
- [ ] Contain the breach (technical, physical, administrative)
- [ ] Preserve evidence (logs, devices, documentation)
- [ ] Conduct initial assessment (what, who, when, how)
- [ ] Document all actions taken

### Phase 2: Investigation (1-7 days)

- [ ] Conduct four-factor risk assessment
- [ ] Determine number of individuals affected
- [ ] Identify types of PHI involved
- [ ] Interview witnesses
- [ ] Review forensic evidence
- [ ] Consult with legal counsel

### Phase 3: Notification (8-60 days)

- [ ] Draft individual notification letters
- [ ] Prepare media notice (if ≥500 affected)
- [ ] Submit HHS OCR notification (if ≥500 affected)
- [ ] Mail individual notifications
- [ ] Issue media notice
- [ ] Establish dedicated communication channel (hotline, email, website)
- [ ] Document all notifications sent

### Phase 4: Remediation (Ongoing)

- [ ] Conduct root cause analysis
- [ ] Develop corrective action plan
- [ ] Implement corrective actions
- [ ] Update policies and procedures
- [ ] Provide additional workforce training
- [ ] Enhance security controls
- [ ] Monitor for ongoing issues

### Phase 5: Reporting and Documentation (Ongoing)

- [ ] Prepare incident report for executive leadership
- [ ] Maintain breach log
- [ ] Submit annual breach log to OCR (if <500 total for year)
- [ ] Cooperate with HHS OCR investigation (if applicable)
- [ ] Document lessons learned
- [ ] Update incident response plan

---

**END OF HIPAA BREACH RESPONSE PLAYBOOK**

For questions or support during an actual breach, contact:
- HHS OCR: <https://www.hhs.gov/ocr>
- OCR Hotline: 1-800-368-1019
- OCR Breach Portal: <https://ocrportal.hhs.gov/ocr/breach/wizard_breach.jsf>
