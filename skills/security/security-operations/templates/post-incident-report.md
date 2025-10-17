# Post-Incident Report Template

**Incident ID:** [INC-YYYY-XXX]
**Report Date:** [YYYY-MM-DD]
**Prepared By:** [Name, Title]
**Classification:** [Confidential / Internal Use Only]

---

## Executive Summary

[2-3 sentence summary of the incident, impact, and resolution. Written for non-technical executive audience.]

**Example:**
> On January 17, 2025, our security team detected and responded to a ransomware attack that encrypted 500 files on a single workstation. The incident was contained within 90 minutes, with full recovery completed in 18 hours. No customer data was compromised, and business operations were not materially affected.

**Key Metrics:**

- **Detection Time (MTTD):** [X hours/minutes]
- **Response Time (MTTR):** [X hours]
- **Total Duration:** [Detection to full recovery]
- **Business Impact:** [Revenue loss, customer impact, SLA violations]
- **Systems Affected:** [Count and criticality]

---

## 1. Incident Details

### 1.1 Incident Overview

| Field | Value |
|-------|-------|
| **Incident ID** | INC-2025-001 |
| **Incident Type** | [Phishing / Malware / Data Breach / DDoS / Insider Threat] |
| **Severity** | [Critical / High / Medium / Low] |
| **Detection Date/Time** | [YYYY-MM-DD HH:MM UTC] |
| **Containment Date/Time** | [YYYY-MM-DD HH:MM UTC] |
| **Resolution Date/Time** | [YYYY-MM-DD HH:MM UTC] |
| **Incident Commander** | [Name] |
| **Response Team** | [List of responders] |

### 1.2 Discovery Method

[Describe how the incident was discovered]

**Options:**

- SIEM alert (specify rule/correlation)
- EDR behavioral detection
- User report
- External notification (security researcher, customer, law enforcement)
- Routine audit/log review

**Example:**
> The incident was detected by our EDR platform (CrowdStrike Falcon) at 10:20 AM UTC when behavioral analysis flagged mass file encryption activity on workstation WS-FIN-042. A Tier 1 SOC analyst received the alert within 2 minutes and escalated to Tier 2 incident response.

### 1.3 Systems and Data Affected

**Systems:**

- Workstation: WS-FIN-042 (Windows 10, Finance Department)
- File Server: [If applicable]
- Databases: [If applicable]
- Cloud Services: [If applicable]

**Data:**

- Files Encrypted: 500 files (finance spreadsheets, invoices)
- Data Classification: Internal - Confidential
- Customer Data: None
- PII/PHI: None
- Financial Data: Yes (internal financial records, non-customer facing)

**User Accounts:**

- Primary: john.doe@company.com
- Compromised: [List if credentials stolen]

---

## 2. Timeline of Events

| Date/Time (UTC) | Event | Actor/System | Action Taken |
|-----------------|-------|--------------|--------------|
| 2025-01-17 08:00 | Phishing email delivered to user inbox | External attacker | None (not yet detected) |
| 2025-01-17 09:30 | User opened malicious attachment (macro-enabled Excel) | john.doe@company.com | Email gateway did not block (bypassed SEG) |
| 2025-01-17 09:32 | Macro executed, downloaded ransomware payload | Malware: TrickBot | EDR behavioral analysis triggered |
| 2025-01-17 10:15 | Ransomware executed, began encrypting files | Malware: Ryuk ransomware | User reported "files locked" |
| 2025-01-17 10:20 | EDR alert: Mass file encryption detected | CrowdStrike Falcon | Alert sent to SOC |
| 2025-01-17 10:22 | Tier 1 SOC analyst reviewed alert, confirmed true positive | SOC Analyst A | Escalated to Tier 2 |
| 2025-01-17 10:35 | Tier 2 analyst initiated containment | SOC Analyst B | Isolated workstation from network |
| 2025-01-17 10:40 | Incident Commander assigned, war room established | Incident Commander | Stakeholder notification |
| 2025-01-17 11:00 | Forensic memory dump captured | Forensic Specialist | Evidence preserved |
| 2025-01-17 11:30 | Malware family identified: Ryuk ransomware | Malware Analyst | IOCs extracted, threat intel updated |
| 2025-01-17 14:00 | Backup integrity verified, restore initiated | IT Operations | 450 files restored from backup |
| 2025-01-17 16:00 | System rebuild from gold image | IT Operations | Fresh OS deployed |
| 2025-01-17 18:00 | User credential reset, MFA enforced | IT Security | Account secured |
| 2025-01-18 02:00 | Full recovery confirmed, system back in production | Incident Commander | Incident closed |

**Total Duration:** 16 hours (detection to full recovery)

---

## 3. Root Cause Analysis (RCA)

### 3.1 Primary Root Cause

[Identify the single most important factor that allowed the incident]

**Example:**
> **Inadequate email security filtering:** The phishing email bypassed our secure email gateway (SEG) because the macro-enabled Excel attachment was obfuscated with a password-protected ZIP file. The SEG did not inspect the ZIP contents, allowing the malicious payload to reach the user's inbox.

### 3.2 Contributing Factors

[List additional factors that contributed to the incident]

1. **User Security Awareness:** User opened attachment despite "unknown sender" warning
2. **Endpoint Configuration:** Macros were enabled by default on finance team workstations (business requirement for legacy Excel tools)
3. **Network Segmentation:** Finance workstations had access to file servers beyond necessary scope
4. **Backup Strategy:** Backup restore took 8 hours (exceeded target of 4 hours)

### 3.3 Why It Was Not Prevented

- **Email Security:** SEG did not inspect password-protected archives
- **User Training:** Last phishing simulation conducted 6 months ago (target: quarterly)
- **Application Whitelisting:** Not implemented on finance workstations (considered but deprioritized)
- **Detection Gap:** No SIEM alert for "Office application spawning suspicious processes" (added post-incident)

### 3.4 Why It Was Not Detected Earlier

- **Initial Payload Download:** TrickBot downloder evaded EDR signature detection (zero-day variant)
- **Lateral Movement:** None occurred (ransomware executed locally before network isolation)
- **C2 Communication:** Ransomware used HTTPS on port 443, appeared as legitimate traffic

---

## 4. Response Effectiveness

### 4.1 What Went Well

1. **Fast Detection:** EDR detected ransomware execution within 5 minutes (target: <15 min for critical)
2. **Effective Containment:** Network isolation completed in 15 minutes, preventing spread
3. **Team Coordination:** Incident response team mobilized quickly, clear communication
4. **Backup Integrity:** Backups were intact and restorable (regular testing paid off)
5. **Documentation:** All actions logged in incident ticket, evidence chain of custody maintained

### 4.2 What Needs Improvement

1. **Email Security:** Phishing email should have been blocked at gateway
2. **User Awareness:** User did not recognize phishing indicators (urgent language, unknown sender)
3. **Backup Restore Speed:** 8 hours to restore 450 files exceeded target (4 hours)
4. **SIEM Coverage:** No alert for "Office spawning suspicious processes" (gap identified)
5. **Communication:** Legal and PR teams notified 2 hours after detection (should be immediate for critical incidents)

### 4.3 Incident Response Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **MTTD (Mean Time To Detect)** | <15 min | 5 min | ✅ Exceeded target |
| **MTTR (Mean Time To Respond)** | <1 hour | 15 min | ✅ Exceeded target |
| **Containment Time** | <30 min | 15 min | ✅ Exceeded target |
| **Recovery Time** | <4 hours | 16 hours | ❌ Exceeded target |
| **Communication Delay** | Immediate | 2 hours | ❌ Missed target |

---

## 5. Impact Assessment

### 5.1 Business Impact

**Operational Impact:**

- **Downtime:** 1 workstation offline for 16 hours
- **Productivity Loss:** 1 employee unable to work for 16 hours (estimated $500 labor cost)
- **No customer-facing service disruption**

**Financial Impact:**

- Incident response labor: 40 hours (4 analysts × 10 hours) = $8,000
- Forensic analysis: $5,000 (external consultant)
- Total estimated cost: **$13,500**

**Data Impact:**

- **Confidentiality:** No data exfiltration detected (network logs reviewed)
- **Integrity:** 500 files encrypted, 450 restored from backup, 50 recreated by finance team
- **Availability:** 16 hours downtime for affected workstation

### 5.2 Regulatory and Compliance

- **Data Breach Notification:** Not required (no PII/PHI exposed)
- **Regulatory Reporting:** Not required
- **Cyber Insurance:** Claim filed, pending approval (estimated $10,000 reimbursement)
- **Audit Impact:** Internal audit scheduled for next quarter (no external audit required)

### 5.3 Reputation Impact

- **Customer Communication:** None required (no customer data affected)
- **Media Coverage:** None
- **Employee Confidence:** Minor impact (internal email sent explaining incident and security improvements)

---

## 6. Lessons Learned

### 6.1 Key Takeaways

1. **Email Security is Critical First Line of Defense**
   - Phishing remains the #1 attack vector
   - Current SEG inadequate for advanced obfuscation techniques

2. **Backups Must Be Fast and Tested**
   - Backup restore speed directly impacts recovery time
   - Need to optimize backup infrastructure

3. **User Training Requires Continuous Reinforcement**
   - 6-month gap between simulations too long
   - Finance team needs targeted training (high-value targets)

4. **Defense in Depth Works**
   - EDR caught what SEG missed
   - Multiple layers prevented catastrophic damage

### 6.2 Corrective Actions

| Action Item | Priority | Owner | Due Date | Status |
|-------------|----------|-------|----------|--------|
| Deploy advanced email security (Proofpoint TAP) | High | Security Team | 2025-02-01 | In Progress |
| Implement monthly phishing simulations | High | HR / Security | 2025-01-31 | Not Started |
| Optimize backup restore process (target: <4h) | High | IT Operations | 2025-02-15 | Not Started |
| Add SIEM alert: "Office spawning suspicious processes" | High | SOC Team | 2025-01-24 | Completed |
| Disable macros by default (exceptions via GPO) | Medium | IT Operations | 2025-02-28 | Not Started |
| Implement application whitelisting (AppLocker) | Medium | Security Team | 2025-03-31 | Not Started |
| Network segmentation review (finance VLAN) | Low | Network Team | 2025-03-15 | Not Started |
| Update incident response playbook (ransomware) | Low | SOC Manager | 2025-02-10 | Not Started |

### 6.3 Preventative Measures

**Short-Term (1-3 months):**

- Enhanced email filtering (Proofpoint TAP, URL rewriting, sandbox analysis)
- Monthly phishing simulations with targeted training for clickers
- Disable Office macros by default, whitelist approved macros via GPO
- Add SIEM correlation rules for Office suspicious behavior

**Medium-Term (3-6 months):**

- Application whitelisting (AppLocker/AppArmor) on all endpoints
- Optimize backup/restore infrastructure (incremental backups, faster restore)
- Network segmentation review (limit lateral movement)
- EDR deployment to 100% of endpoints (currently 95%)

**Long-Term (6-12 months):**

- Zero Trust architecture (least privilege, MFA everywhere)
- Automated incident response (SOAR platform for common playbooks)
- Threat hunting program (proactive IOC searches)
- Annual red team/purple team exercises

---

## 7. Evidence and Forensics

### 7.1 Evidence Collected

- **Memory Dump:** `WS-FIN-042-memory-20250117.dmp` (8 GB)
- **Disk Image:** `WS-FIN-042-disk-20250117.img` (256 GB)
- **Logs:** EDR logs, Windows Event Logs, network traffic (PCAP)
- **Malware Samples:** TrickBot downloader, Ryuk ransomware
- **IOCs:** File hashes, C2 IPs/domains, registry keys

**Evidence Location:** `/forensic-storage/INC-2025-001/`
**Chain of Custody:** Maintained in incident ticket INC-2025-001
**Retention Period:** 1 year (extended to 7 years if legal hold required)

### 7.2 Indicators of Compromise (IOCs)

**File Hashes (SHA256):**

- TrickBot downloader: `a5c2e5e7f8a9b1c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7`
- Ryuk ransomware: `d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2`

**Network IOCs:**

- C2 Domain: `malware-c2.evil.com`
- C2 IP: `192.0.2.100`
- Bitcoin Wallet (ransom payment): `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` (not paid)

**Registry Keys:**

- `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\TrickBot`
- `HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce\Ryuk`

**Action Taken:**

- IOCs added to threat intelligence platform (MISP)
- Firewall rules updated to block C2 IPs/domains
- EDR signatures updated to detect file hashes

---

## 8. Communication Summary

### 8.1 Internal Communication

| Audience | Method | Timing | Content |
|----------|--------|--------|---------|
| SOC Team | Slack #security-incidents | 10:22 AM | Alert escalation, investigation updates |
| Incident Commander | Phone call | 10:35 AM | Incident briefing, war room activation |
| IT Operations | Email + conference call | 10:45 AM | System isolation, backup restore coordination |
| Executive Leadership | Email | 12:00 PM | Executive summary, no customer impact |
| Finance Department | Email | 14:00 PM | Workstation offline, ETA for recovery |
| All Employees | Company-wide email | 2025-01-18 | Phishing awareness reminder, security tips |

### 8.2 External Communication

| Entity | Required? | Timing | Status |
|--------|-----------|--------|--------|
| Law Enforcement (FBI IC3) | No | N/A | Not required (no criminal investigation) |
| Cyber Insurance | Yes | 12 hours | Claim filed, approved |
| Customers | No | N/A | No customer data affected |
| Regulatory Bodies | No | N/A | No PII/PHI breach |
| Media | No | N/A | No public disclosure required |

---

## 9. Recommendations

### 9.1 Immediate Actions (Next 30 Days)

1. **Deploy Advanced Email Security (Priority: High)**
   - Replace current SEG with Proofpoint Targeted Attack Protection (TAP)
   - Enable URL rewriting, attachment sandboxing, impersonation protection
   - Budget: $50,000/year

2. **Accelerate Phishing Simulations (Priority: High)**
   - Increase frequency from quarterly to monthly
   - Target high-risk departments (finance, HR, executive assistants)
   - Track click rates, provide immediate training to clickers

3. **Optimize Backup Infrastructure (Priority: High)**
   - Upgrade backup hardware (faster disk I/O)
   - Implement incremental forever backup strategy
   - Test restore process monthly (currently quarterly)

### 9.2 Strategic Recommendations (6-12 Months)

1. **Zero Trust Architecture**
   - Implement least privilege access (RBAC)
   - MFA enforcement for all applications (currently 80% coverage)
   - Network microsegmentation

2. **Security Orchestration, Automation, Response (SOAR)**
   - Automate common incident response playbooks (phishing, malware)
   - Reduce analyst workload, improve response time
   - Evaluate: Palo Alto XSOAR, Splunk SOAR

3. **Threat Hunting Program**
   - Hire dedicated threat hunter (Tier 3 analyst)
   - Proactive IOC searches, hypothesis-driven hunting
   - Quarterly threat hunting campaigns

---

## 10. Approval and Sign-Off

### 10.1 Report Prepared By

**Name:** [John Smith]
**Title:** Senior Security Analyst
**Date:** 2025-01-18
**Signature:** _______________________

### 10.2 Reviewed By

**Name:** [Jane Doe]
**Title:** SOC Manager
**Date:** 2025-01-19
**Signature:** _______________________

### 10.3 Approved By

**Name:** [Bob Johnson]
**Title:** Chief Information Security Officer (CISO)
**Date:** 2025-01-20
**Signature:** _______________________

---

## 11. Appendices

### Appendix A: Technical Details

[Include detailed forensic analysis, malware analysis report, network traffic analysis]

### Appendix B: SIEM Queries Used

[Include Splunk/ELK queries that detected or investigated the incident]

### Appendix C: Stakeholder Communication Logs

[Include email threads, meeting notes, conference call summaries]

### Appendix D: Incident Response Playbook Used

[Reference to specific playbook, note any deviations]

---

## 12. Distribution List

**Internal:**

- Chief Information Security Officer (CISO)
- Chief Information Officer (CIO)
- SOC Manager
- Incident Response Team
- IT Operations Manager
- Legal Counsel
- Risk Management

**External:**

- Cyber Insurance Provider
- External Forensic Consultant (if engaged)
- [Board of Directors - if critical incident]

**Retention:** 7 years (legal requirement for financial records)

---

*Report Classification: Confidential - Internal Use Only*
*Document Version: 1.0*
*Last Updated: 2025-01-20*
