# NIST Incident Response Controls Mapping

Comprehensive mapping of NIST 800-61 (Incident Response Guide) and NIST 800-53 IR control family for security operations implementation.

---

## Table of Contents

1. [NIST 800-61 Rev 2 - Incident Response Guide](#nist-800-61-rev-2---incident-response-guide)
2. [NIST 800-53 Rev 5 - IR Control Family](#nist-800-53-rev-5---ir-control-family)
3. [Implementation Checklist](#implementation-checklist)
4. [Compliance Validation](#compliance-validation)

---

## NIST 800-61 Rev 2 - Incident Response Guide

### Phase 1: Preparation

**Objective:** Establish incident response capability before incidents occur

**Key Activities:**
- Develop incident response policy and procedures
- Establish incident response team (IRT) with defined roles
- Deploy incident detection and analysis tools (SIEM, EDR, IDS)
- Create communication plan (internal, external, legal, media)
- Conduct training and awareness programs
- Perform tabletop exercises and simulations

**SOC Implementation:**
```yaml
preparation_checklist:
  policies:
    - incident_response_policy: "Documented, approved by management"
    - escalation_matrix: "Critical: CISO within 15min, Board within 24h"
    - communication_plan: "Legal, PR, customers, regulators"

  team:
    - tier1_analysts: 3 (24/7 coverage)
    - tier2_responders: 2 (on-call)
    - tier3_hunters: 1 (business hours)
    - incident_commander: CISO designee

  tools:
    - siem: "Splunk Enterprise Security"
    - edr: "CrowdStrike Falcon"
    - forensics: "Volatility, Autopsy, FTK Imager"
    - threat_intel: "MISP, AlienVault OTX, VirusTotal"

  training:
    - frequency: Quarterly tabletop exercises
    - phishing_sims: Monthly
    - certifications: "GCIH, GCFA, GCIA for analysts"
```

**NIST 800-53 Controls Addressed:** IR-1, IR-2, IR-3, IR-8

---

### Phase 2: Detection and Analysis

**Objective:** Identify and validate security incidents, determine scope and impact

**Key Activities:**
- Monitor security alerts from SIEM, EDR, IDS/IPS
- Analyze indicators of compromise (IOCs)
- Correlate events across multiple data sources
- Prioritize incidents based on severity and business impact
- Document all findings

**SOC Implementation:**

**Detection Sources (Priority Order):**
1. **High Fidelity (>90% accuracy):**
   - EDR behavioral alerts
   - Threat intelligence IOC matches
   - IDS/IPS signature hits

2. **Medium Fidelity (60-80% accuracy):**
   - UEBA anomaly detection
   - DLP policy violations
   - Authentication failures (brute force, password spray)

3. **Low Fidelity (<60% accuracy):**
   - Generic firewall denies
   - Vulnerability scanner findings

**Alert Triage Process:**
```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Initial Validation (5 min)                          │
│   - True positive or false positive?                        │
│   - Asset criticality (production vs. dev)?                 │
│   - Quick OSINT lookup (IP reputation, domain age)          │
├─────────────────────────────────────────────────────────────┤
│ Step 2: Scoping (15-30 min)                                 │
│   - Timeline: When did activity start?                      │
│   - Scope: How many systems affected?                       │
│   - Impact: What data/systems at risk?                      │
│   - Persistence: Is threat still active?                    │
├─────────────────────────────────────────────────────────────┤
│ Step 3: Categorization                                      │
│   - Type: Malware, phishing, data breach, etc.              │
│   - Severity: Critical, High, Medium, Low                   │
│   - Confidence: Confirmed, Likely, Suspected                │
└─────────────────────────────────────────────────────────────┘
```

**NIST 800-53 Controls Addressed:** IR-4, IR-5, SI-4, AU-6

---

### Phase 3: Containment, Eradication, and Recovery

**Objective:** Limit damage, remove threat, restore operations

**Containment Strategies:**

**Short-Term Containment (Immediate - 15 minutes):**
- Isolate infected host from network (EDR quarantine, VLAN switch)
- Block malicious IPs/domains at firewall/proxy
- Disable compromised user accounts
- Preserve evidence (memory dump, disk image)

**Long-Term Containment (1-4 hours):**
- Implement network segmentation
- Apply emergency patches
- Enhanced monitoring on related systems
- Communication blackout (deny attacker intel)

**Eradication:**
- Remove malware and persistence mechanisms
- Patch vulnerabilities exploited by attacker
- Strengthen access controls
- Rotate credentials

**Recovery:**
- Restore systems from known-good backups
- Rebuild compromised systems from gold images
- Verify system integrity (file hashes, AIDE/Tripwire)
- Monitor for reinfection indicators

**NIST 800-53 Controls Addressed:** IR-4, CM-3, CP-10

---

### Phase 4: Post-Incident Activity

**Objective:** Learn from incidents, improve defenses, meet compliance obligations

**Key Activities:**
- Lessons learned meeting (within 2 weeks of incident closure)
- Root cause analysis (RCA)
- Document timeline, actions taken, evidence collected
- Update incident response procedures
- Implement corrective actions
- Evidence retention (1 year minimum, 7+ years for legal holds)

**Lessons Learned Meeting Agenda:**
```markdown
1. Incident Summary (5 min)
   - What happened? When? How detected?

2. Timeline Review (10 min)
   - Walk through incident timeline
   - Identify decision points

3. What Went Well (10 min)
   - Fast detection, effective containment, etc.

4. What Needs Improvement (15 min)
   - Gaps in detection, slow response, communication issues

5. Root Cause Analysis (10 min)
   - Why did incident occur?
   - Why was it not prevented/detected earlier?

6. Action Items (10 min)
   - Corrective actions with owners and due dates
   - Prioritize by impact and feasibility

7. Follow-Up (5 min)
   - Schedule next review to track action items
```

**NIST 800-53 Controls Addressed:** IR-4, IR-5, IR-6, IR-8

---

## NIST 800-53 Rev 5 - IR Control Family

### IR-1: Policy and Procedures

**Control Statement:**
Develop, document, and disseminate incident response policy and procedures

**Implementation:**
- **Policy:** Incident Response Policy (approved by CISO, reviewed annually)
- **Procedures:** Incident response playbooks for common scenarios
- **Distribution:** Accessible to all employees via intranet, mandatory training

**Evidence:**
- Incident Response Policy document (signed by CISO)
- Playbooks (phishing, malware, data breach, DDoS, insider threat)
- Training completion records

---

### IR-2: Incident Response Training

**Control Statement:**
Provide incident response training to system users consistent with assigned roles

**Implementation:**
```yaml
training_program:
  general_users:
    frequency: Annual
    content: "How to report incidents, phishing awareness"
    method: CBT (Computer-Based Training)

  it_staff:
    frequency: Quarterly
    content: "Incident detection, initial response, escalation"
    method: Instructor-led + hands-on labs

  ir_team:
    frequency: Monthly (tabletop) + Quarterly (full exercise)
    content: "Advanced forensics, malware analysis, legal considerations"
    certifications: "GCIH, GCFA, GCIA, OSCP"
```

**Evidence:**
- Training curriculum and materials
- Attendance records and completion certificates
- Exercise reports (tabletop, red team/purple team)

---

### IR-3: Incident Response Testing

**Control Statement:**
Test incident response capability using exercises and simulations

**Implementation:**
- **Tabletop Exercises:** Quarterly (discuss scenario, no hands-on)
- **Functional Exercises:** Semi-annually (test specific procedures, limited scope)
- **Full-Scale Exercises:** Annually (red team attack, full IR response)

**Example Tabletop Scenario:**
```
Scenario: Ransomware Outbreak

10:00 AM: EDR alerts on mass file encryption, 3 workstations affected
10:15 AM: Tier 1 analyst escalates to Tier 2
10:30 AM: Incident Commander assigned

Discussion Points:
- Who needs to be notified immediately?
- How do we contain spread to file servers?
- Are backups intact? How long to restore?
- Do we pay ransom? (Answer: No, per FBI/CISA guidance)
- When do we notify legal, customers, regulators?

Outcome: Identify gaps in backup restore process, improve communication plan
```

**Evidence:**
- Exercise plans and scenarios
- After-action reports with lessons learned
- Action item tracking (corrective actions implemented)

---

### IR-4: Incident Handling

**Control Statement:**
Implement incident handling capability for security incidents

**IR-4.a - Preparation:**
- Incident response plan documented and approved
- Tools deployed (SIEM, EDR, forensics, threat intel)
- Jump bags prepared (USB with tools, live boot media)

**IR-4.b - Detection and Analysis:**
- SIEM correlation rules configured
- Alert triage process documented
- Threat intelligence feeds integrated

**IR-4.c - Containment, Eradication, and Recovery:**
- Containment strategies defined (network isolation, account disablement)
- System rebuild procedures (gold images)
- Backup verification and restore process

**IR-4.d - Post-Incident Activity:**
- Lessons learned meeting scheduled within 2 weeks
- Root cause analysis performed
- Corrective actions tracked

**Implementation Metrics:**
```yaml
ir_4_metrics:
  mttd_target: "<1 hour for critical incidents"
  mttr_target: "<4 hours for critical incidents"
  false_positive_rate: "<10%"
  incident_resolution_rate: ">95% within SLA"
  lessons_learned_completion: "100% within 2 weeks"
```

**Evidence:**
- Incident response plan
- Incident tickets with full documentation
- Lessons learned reports
- MTTD/MTTR metrics dashboard

---

### IR-5: Incident Monitoring

**Control Statement:**
Track and document information system security incidents

**Implementation:**
- **Incident Tracking System:** ServiceNow, Jira Service Management, or custom
- **Metrics Collected:**
  - Incident count by type, severity, affected systems
  - MTTD (Mean Time To Detect)
  - MTTR (Mean Time To Respond)
  - False positive rate
  - Top attack vectors
  - Threat actor attribution (if known)

**Dashboard:**
See bundled resource: `templates/security-metrics-dashboard.json`

**Reporting:**
- **Daily:** SOC metrics email (active incidents, alerts triaged)
- **Weekly:** Trend analysis (incident types, targeted assets)
- **Monthly:** Executive report (MTTD/MTTR trends, top risks)
- **Quarterly:** Board of Directors briefing

**Evidence:**
- Incident tracking system screenshots
- Monthly/quarterly security metrics reports
- Executive briefing slides

---

### IR-6: Incident Reporting

**Control Statement:**
Require personnel to report suspected security incidents

**IR-6.a - Internal Reporting:**
```yaml
internal_reporting:
  users:
    method: "Email security@company.com, Intranet 'Report Incident' button"
    response_time: "Acknowledgment within 1 hour"

  soc_to_management:
    critical: "Phone call within 15 minutes"
    high: "Email within 1 hour"
    medium: "Email within 4 hours"

  management_to_board:
    critical: "Within 24 hours"
    high: "Monthly board report"
```

**IR-6.b - External Reporting:**
```yaml
external_reporting:
  law_enforcement:
    trigger: "Criminal activity (CFAA violation, financial fraud)"
    contact: "FBI Internet Crime Complaint Center (IC3), Secret Service"

  regulatory:
    gdpr: "72 hours to supervisory authority (DPO coordinates)"
    hipaa: "60 days to HHS for PHI breach >500 individuals"
    sec: "4 business days for material cybersecurity incident (8-K filing)"
    state_breach_laws: "Per state requirements (30-90 days typical)"

  cyber_insurance:
    timing: "Within 24-48 hours per policy terms"
    contact: "Insurance broker, claims hotline"

  isac_sharing:
    method: "STIX/TAXII, MISP"
    data: "Anonymized IOCs, TTPs (no PII)"
```

**Evidence:**
- Incident reporting procedures document
- Regulatory notification letters (GDPR, HIPAA, SEC)
- Law enforcement case numbers
- Cyber insurance claim confirmations

---

### IR-7: Incident Response Assistance

**Control Statement:**
Provide incident response support resources

**Implementation:**
- **Internal Resources:**
  - SOC hotline: 1-800-SOC-HELP (24/7)
  - Email: security@company.com
  - Intranet: Incident reporting portal, IR playbooks

- **External Resources:**
  - Forensic consultant (retainer agreement with Mandiant/CrowdStrike Services)
  - Legal counsel (data breach attorney on retainer)
  - Cyber insurance incident response services
  - CISA (Cybersecurity and Infrastructure Security Agency)
  - FBI Cyber Division

**Retainer Agreements:**
```yaml
external_support:
  forensic_firm:
    provider: "Mandiant"
    retainer: "$50,000/year (10 hours prepaid)"
    response_time: "4 hours for critical incidents"

  legal_counsel:
    provider: "Data Breach Law Firm"
    retainer: "$25,000/year"
    services: "Regulatory notification, class action defense"

  cyber_insurance:
    provider: "Chubb"
    coverage: "$5M cyber liability"
    services: "Forensics, PR, legal, credit monitoring"
```

**Evidence:**
- Retainer agreements with external consultants
- Contact list with 24/7 hotlines
- Incident response assistance guide

---

### IR-8: Incident Response Plan

**Control Statement:**
Develop and implement incident response plan

**IR-8.a - Plan Development:**
- Incident response policy and procedures
- Roles and responsibilities (IRT structure)
- Communication plan (internal and external)
- Playbooks for common incident types
- Evidence handling and chain of custody
- Legal and regulatory obligations

**IR-8.b - Plan Distribution:**
- All employees receive IR policy summary (annual training)
- IR team has full access to detailed playbooks
- Legal, PR, HR receive relevant sections

**IR-8.c - Plan Review:**
- Annual review (or after major incidents)
- Update based on lessons learned
- Approval by CISO and legal counsel

**IR-8.d - Plan Testing:**
- Quarterly tabletop exercises
- Annual full-scale exercise (red team)

**Evidence:**
- Incident Response Plan document (version control)
- Distribution records (email, intranet access logs)
- Annual review meeting notes
- Exercise after-action reports

---

## Implementation Checklist

### Phase 1: Foundation (Months 1-3)

- [ ] **IR-1: Policy and Procedures**
  - [ ] Develop Incident Response Policy (draft, review, approve)
  - [ ] Create incident response playbooks (phishing, malware, data breach)
  - [ ] Establish escalation matrix (who to notify, when)

- [ ] **IR-2: Team Formation**
  - [ ] Define IRT roles (Tier 1/2/3 analysts, Incident Commander)
  - [ ] Hire/train personnel (certifications: GCIH, GCFA)
  - [ ] Create on-call rotation schedule

- [ ] **IR-4: Tool Deployment**
  - [ ] Deploy SIEM (Splunk, ELK, Azure Sentinel)
  - [ ] Deploy EDR (CrowdStrike, Microsoft Defender)
  - [ ] Set up forensic workstation (Volatility, Autopsy, FTK)
  - [ ] Integrate threat intelligence feeds (MISP, AlienVault OTX)

- [ ] **IR-6: Reporting Mechanisms**
  - [ ] Create security@company.com email alias
  - [ ] Set up incident tracking system (ServiceNow, Jira)
  - [ ] Document regulatory reporting requirements (GDPR, HIPAA, SEC)

### Phase 2: Operationalization (Months 4-6)

- [ ] **IR-3: Testing**
  - [ ] Conduct first tabletop exercise
  - [ ] Review findings, update playbooks
  - [ ] Schedule quarterly exercises

- [ ] **IR-5: Monitoring and Metrics**
  - [ ] Define KPIs (MTTD, MTTR, false positive rate)
  - [ ] Create SOC metrics dashboard (Grafana)
  - [ ] Implement automated reporting (daily, weekly, monthly)

- [ ] **IR-7: External Support**
  - [ ] Negotiate retainer with forensic firm
  - [ ] Establish relationship with data breach attorney
  - [ ] Review cyber insurance incident response services

- [ ] **IR-8: Plan Maturity**
  - [ ] Conduct annual plan review
  - [ ] Update based on exercise findings
  - [ ] Distribute updated plan to stakeholders

### Phase 3: Continuous Improvement (Ongoing)

- [ ] **Post-Incident Reviews**
  - [ ] Lessons learned meeting after every P1/P2 incident
  - [ ] Root cause analysis, corrective actions
  - [ ] Update playbooks based on new TTPs

- [ ] **Threat Intelligence**
  - [ ] Subscribe to relevant ISAC feeds
  - [ ] Correlate internal incidents with global campaigns
  - [ ] Contribute anonymized IOCs to community (MISP)

- [ ] **Training and Awareness**
  - [ ] Monthly phishing simulations
  - [ ] Quarterly IR team training
  - [ ] Annual red team/purple team exercise

---

## Compliance Validation

### Audit Evidence Package

When auditors request evidence of IR control implementation, provide:

1. **Policies and Procedures (IR-1, IR-8):**
   - Incident Response Policy (signed, dated)
   - Incident Response Plan (version controlled)
   - Playbooks (phishing, malware, data breach, DDoS, insider threat)

2. **Training Records (IR-2):**
   - Training curriculum and materials
   - Attendance lists and completion certificates
   - Certification records (GCIH, GCFA, GCIA)

3. **Exercise Reports (IR-3):**
   - Tabletop exercise scenarios and after-action reports
   - Red team/purple team exercise findings
   - Corrective action tracking

4. **Incident Handling Evidence (IR-4):**
   - Sample incident tickets (redacted)
   - Lessons learned reports
   - MTTD/MTTR metrics dashboard

5. **Monitoring and Reporting (IR-5):**
   - Monthly security metrics reports (last 12 months)
   - Executive briefing slides
   - Trend analysis charts

6. **Regulatory Notifications (IR-6):**
   - GDPR notification letters (if applicable)
   - Cyber insurance claim confirmations
   - ISAC/MISP sharing evidence

7. **External Support Agreements (IR-7):**
   - Forensic firm retainer agreement
   - Legal counsel retainer agreement
   - Contact list with 24/7 hotlines

### Self-Assessment Questionnaire

Use this questionnaire for internal compliance checks:

| Control | Question | Evidence | Status |
|---------|----------|----------|--------|
| **IR-1** | Is there a documented Incident Response Policy approved by management? | Policy document with signatures | ✅ |
| **IR-2** | Are all IR team members trained and certified? | Training records, certifications | ✅ |
| **IR-3** | Are incident response exercises conducted quarterly? | Exercise reports (last 4 quarters) | ✅ |
| **IR-4.a** | Are incident detection tools deployed (SIEM, EDR)? | Tool inventory, configuration docs | ✅ |
| **IR-4.b** | Is MTTD <1 hour for critical incidents? | MTTD metrics dashboard | ✅ |
| **IR-4.c** | Are containment procedures documented? | Playbooks, incident tickets | ✅ |
| **IR-4.d** | Are lessons learned meetings held for all P1/P2 incidents? | Lessons learned reports | ✅ |
| **IR-5** | Are incident metrics tracked (MTTD, MTTR, count)? | Monthly metrics reports | ✅ |
| **IR-6.a** | Can employees easily report incidents? | Security email alias, intranet portal | ✅ |
| **IR-6.b** | Are regulatory notifications made within required timeframes? | Notification letters (GDPR 72h, HIPAA 60d) | ✅ |
| **IR-7** | Are external IR resources available (forensics, legal)? | Retainer agreements | ✅ |
| **IR-8** | Is the IR plan reviewed and updated annually? | Version history, review meeting notes | ✅ |

---

## Regulatory Mapping

### GDPR (General Data Protection Regulation)

- **Article 33 - Notification of Breach:** 72-hour notification to supervisory authority
- **Article 34 - Communication to Data Subjects:** Without undue delay for high-risk breaches
- **NIST Controls:** IR-6 (Incident Reporting), IR-4 (Incident Handling)

### HIPAA (Health Insurance Portability and Accountability Act)

- **Breach Notification Rule:** 60 days to HHS for PHI breach >500 individuals
- **Security Rule:** 164.308(a)(6) - Security incident procedures
- **NIST Controls:** IR-6 (Incident Reporting), IR-8 (Incident Response Plan)

### PCI-DSS (Payment Card Industry Data Security Standard)

- **Requirement 12.10:** Implement incident response plan
- **Requirement 12.10.1:** Test incident response plan annually
- **NIST Controls:** IR-8 (Incident Response Plan), IR-3 (Incident Response Testing)

### SOC 2 (System and Organization Controls)

- **CC7.3:** System security incidents are identified and managed
- **CC7.4:** System availability incidents are identified and managed
- **NIST Controls:** IR-4 (Incident Handling), IR-5 (Incident Monitoring)

### SEC Cyber Disclosure Rules

- **Form 8-K:** 4 business days for material cybersecurity incident
- **Form 10-K/10-Q:** Annual/quarterly disclosure of cybersecurity risk management
- **NIST Controls:** IR-6 (Incident Reporting), IR-5 (Incident Monitoring)

---

## References

- **NIST SP 800-61 Rev 2:** Computer Security Incident Handling Guide
  - <https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final>

- **NIST SP 800-53 Rev 5:** Security and Privacy Controls for Information Systems
  - <https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final>

- **NIST SP 800-86:** Guide to Integrating Forensic Techniques into Incident Response
  - <https://csrc.nist.gov/publications/detail/sp/800-86/final>

- **NIST Cybersecurity Framework:** Respond Function
  - <https://www.nist.gov/cyberframework>

- **ISO/IEC 27035:** Information Security Incident Management
  - <https://www.iso.org/standard/78973.html>

---

*Last Updated: 2025-01-17*
*Version: 1.0.0*
*Maintained by: Security Operations Team*
