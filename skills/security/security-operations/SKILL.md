---
name: security-operations
category: security
difficulty: advanced
nist_controls: [IR-4, IR-5, IR-6, SI-4, AU-6]
description: Security Operations Center (SOC) practices, incident response, SIEM management, and threat hunting following NIST 800-61
version: 1.0.0
last_updated: 2025-01-17
prerequisites: [security-fundamentals, network-security, linux-security]
estimated_time: "8-12 hours"
tags: [soc, incident-response, siem, threat-hunting, forensics, nist-800-61]
---

# Security Operations

## Level 1: Quick Reference

### Incident Response Lifecycle (NIST 800-61 Rev 2)

```
┌──────────────────────────────────────────────────────────────┐
│                  INCIDENT RESPONSE PHASES                     │
├──────────────────────────────────────────────────────────────┤
│ 1. PREPARATION                                                │
│    └─ Policies, tools, training, communication plans          │
│ 2. DETECTION & ANALYSIS                                       │
│    └─ SIEM alerts, log analysis, threat intelligence          │
│ 3. CONTAINMENT, ERADICATION & RECOVERY                        │
│    └─ Isolate, remove threat, restore operations              │
│ 4. POST-INCIDENT ACTIVITY                                     │
│    └─ Lessons learned, documentation, process improvement     │
└──────────────────────────────────────────────────────────────┘
```

### SOC Processes Overview

**Tier 1 - Alert Triage:**
- Monitor SIEM dashboards
- Initial alert validation
- Basic incident categorization
- Escalate to Tier 2/3

**Tier 2 - Incident Response:**
- Deep dive investigation
- Threat analysis and correlation
- Containment actions
- Forensic evidence collection

**Tier 3 - Threat Hunting:**
- Proactive threat hunting
- Advanced malware analysis
- Complex incident coordination
- Strategic threat intelligence

### Essential Security Operations Checklist

**SIEM Configuration:**
- [ ] Log sources configured (firewalls, endpoints, servers, cloud)
- [ ] Correlation rules active (failed logins, data exfiltration, privilege escalation)
- [ ] Alert thresholds tuned (reduce false positives)
- [ ] Retention policy implemented (90-day hot, 1-year archive)

**Incident Response Readiness:**
- [ ] IR playbooks documented (phishing, malware, DDoS, breach)
- [ ] Communication plan established (internal, legal, PR, customers)
- [ ] Evidence collection tools ready (FTK Imager, dd, volatility)
- [ ] Backup verification (test restore monthly)

**Threat Intelligence:**
- [ ] Threat feeds integrated (MISP, AlienVault OTX, VirusTotal)
- [ ] IOC watchlists maintained (IPs, domains, file hashes)
- [ ] Vulnerability scanning scheduled (weekly internal, monthly external)

**Security Metrics (NIST IR-4):**
- [ ] MTTD - Mean Time To Detect (target: <1 hour for critical)
- [ ] MTTR - Mean Time To Respond (target: <4 hours for critical)
- [ ] Incident trends (weekly review)
- [ ] False positive rate (<10%)

### Quick SIEM Queries

**Failed Login Attempts (Splunk SPL):**
```spl
index=security sourcetype=auth action=failure
| stats count by user, src_ip
| where count > 5
```

**Suspicious Outbound Traffic (ELK KQL):**
```kql
destination.port:(4444 OR 8080 OR 1337) AND NOT destination.ip:(10.0.0.0/8 OR 172.16.0.0/12 OR 192.168.0.0/16)
```

**Privilege Escalation (Azure Sentinel KQL):**
```kql
SecurityEvent
| where EventID == 4672
| where AccountType == "User"
| summarize count() by Account, Computer
```

### Incident Severity Classification

| Severity | Impact | Response Time | Escalation |
|----------|--------|---------------|------------|
| **Critical** | Business-critical system compromised, active data exfiltration | <15 min | Immediate - CISO, Legal |
| **High** | Multiple systems affected, potential data breach | <1 hour | Tier 3, Management |
| **Medium** | Single system compromised, contained threat | <4 hours | Tier 2 |
| **Low** | Failed attack attempt, no system impact | <24 hours | Tier 1 |


---

## Level 2: Implementation Guide

### Security Operations Center (SOC) Structure

#### SOC Team Roles & Responsibilities

**SOC Manager:**
- Strategic planning and resource allocation
- Metrics reporting to executive leadership
- Policy and procedure development
- Vendor and tool management

**Security Analyst Tier 1 (Alert Triage):**
- 24/7 monitoring of SIEM alerts
- Initial alert validation and categorization
- Basic log analysis and correlation
- Ticket creation and escalation
- **NIST Controls:** SI-4 (Information System Monitoring)

**Security Analyst Tier 2 (Incident Response):**
- Deep-dive incident investigation
- Malware analysis and reverse engineering
- Forensic evidence collection
- Containment and eradication actions
- **NIST Controls:** IR-4 (Incident Handling), IR-6 (Incident Reporting)

**Security Analyst Tier 3 (Threat Hunter):**
- Proactive threat hunting campaigns
- Advanced persistent threat (APT) detection
- Threat intelligence analysis and dissemination
- Security tool development and automation
- **NIST Controls:** IR-5 (Incident Monitoring), AU-6 (Audit Review)

**Incident Commander:**
- Major incident coordination
- Stakeholder communication (legal, PR, management)
- Post-incident review facilitation

#### SOC Tools & Technologies

**SIEM Platforms:**
- **Splunk Enterprise Security:** Market leader, powerful SPL query language
- **Elastic Stack (ELK):** Open-source, KQL query language, cost-effective
- **Azure Sentinel:** Cloud-native, integrated with Microsoft ecosystem
- **IBM QRadar:** Enterprise-grade, strong compliance features

**Endpoint Detection & Response (EDR):**
- CrowdStrike Falcon, Microsoft Defender for Endpoint, Carbon Black
- Real-time process monitoring and behavioral analysis
- Automated threat remediation

**Threat Intelligence Platforms:**
- MISP (Malware Information Sharing Platform)
- ThreatConnect, Anomali, Recorded Future
- STIX/TAXII feeds integration

**Forensic Tools:**
- **Memory Analysis:** Volatility, Rekall
- **Disk Forensics:** Autopsy, FTK Imager, EnCase
- **Network Forensics:** Wireshark, NetworkMiner, Zeek

### Incident Response Lifecycle (NIST 800-61 Rev 2)

#### Phase 1: Preparation (IR-4)

**Organizational Readiness:**

```yaml
# IR Team Structure
incident_response_team:
  core_members:
    - security_analysts: 3-5
    - forensic_specialists: 1-2
    - legal_counsel: 1
    - public_relations: 1
    - executive_sponsor: CISO

  on_call_rotation:
    - tier_2_analyst: 24/7 coverage
    - tier_3_hunter: business hours + on-call
    - incident_commander: escalation only

# Communication Plan
communication_channels:
  - internal: Slack #security-incidents (P3-P4), Secure conference bridge (P1-P2)
  - external: Legal-approved PR templates, customer notification process
  - regulatory: 72-hour breach notification (GDPR), SEC reporting
```

**Tool Preparation:**
- SIEM with 90+ days of log retention
- Jump bag (USB drives with forensic tools, live Linux distros)
- Evidence storage (encrypted, chain-of-custody documented)
- Isolated malware analysis sandbox (Cuckoo, ANY.RUN)

**Training & Tabletop Exercises:**
- Quarterly incident response drills
- Annual red team/purple team exercises
- Phishing simulations monthly

#### Phase 2: Detection & Analysis (SI-4, AU-6)

**Detection Sources:**

```python
# SIEM Alert Sources Priority Matrix
detection_sources = {
    "high_fidelity": [
        "EDR behavioral alerts",           # 95% accuracy
        "IDS/IPS signature matches",       # 90% accuracy
        "Threat intel IOC hits",           # 85% accuracy
    ],
    "medium_fidelity": [
        "UEBA anomaly detection",          # 70% accuracy
        "DLP policy violations",           # 75% accuracy
        "Failed authentication spikes",    # 60% accuracy
    ],
    "low_fidelity": [
        "Generic firewall denies",         # 40% accuracy
        "Vulnerability scanner findings",  # 50% accuracy
    ]
}
```

**Alert Triage Process:**

1. **Initial Validation (5 minutes):**
   - Is this a true positive or false positive?
   - Quick OSINT lookup (IP reputation, domain age)
   - Check asset criticality (production vs. dev)

2. **Scoping (15-30 minutes):**
   - Timeline: When did activity start?
   - Scope: How many systems affected?
   - Impact: What data/systems at risk?
   - Persistence: Is threat still active?

3. **Categorization:**
   - **Incident Type:** Malware, phishing, DDoS, data breach, insider threat, account compromise
   - **Severity:** Critical, High, Medium, Low (see Quick Reference table)
   - **Confidence:** Confirmed, likely, suspected

**SIEM Analysis Techniques:**

```spl
# Splunk: Detect lateral movement via SMB
index=security sourcetype=wineventlog EventCode=4624
| where LogonType=3 AND AuthenticationPackageName="NTLM"
| transaction src_ip maxspan=5m
| where eventcount > 10
| table _time, src_ip, dest_host, user
```

```kql
# Azure Sentinel: Detect credential dumping
SecurityEvent
| where EventID in (4672, 4673, 4674)
| where Process has_any ("lsass.exe", "mimikatz", "procdump")
| extend Timestamp, Computer, Account, Process
| summarize count() by bin(Timestamp, 5m), Computer, Account
```

**Threat Intelligence Integration:**

```bash
# Check IP against threat feeds
curl -s "https://otx.alienvault.com/api/v1/indicators/IPv4/$IP/general" | jq '.pulse_info.count'

# Check file hash against VirusTotal
curl -s "https://www.virustotal.com/api/v3/files/$HASH" \
  -H "x-apikey: $VT_API_KEY" | jq '.data.attributes.last_analysis_stats'
```

#### Phase 3: Containment, Eradication & Recovery (IR-4)

**Containment Strategies:**

**Short-Term Containment (Immediate - 15 minutes):**
- Isolate infected host from network (EDR quarantine, VLAN switch)
- Block malicious IPs/domains at firewall/proxy
- Disable compromised user accounts
- Preserve evidence (memory dump, disk image)

```bash
# Linux: Network isolation
sudo iptables -A INPUT -j DROP
sudo iptables -A OUTPUT -j DROP
sudo iptables -A OUTPUT -d 10.0.0.100 -j ACCEPT  # Allow forensic server

# Windows: Disable network adapter via PowerShell
Disable-NetAdapter -Name "Ethernet" -Confirm:$false
```

**Long-Term Containment (1-4 hours):**
- Implement network segmentation
- Apply emergency patches
- Enhanced monitoring on related systems
- Communication blackout (deny attacker intel)

**Eradication:**

```bash
# Remove malware persistence mechanisms
# Linux
sudo crontab -l | grep -v "malicious.sh" | crontab -
sudo systemctl disable malicious-service
sudo rm -f /etc/systemd/system/malicious.service

# Windows (PowerShell)
Get-ScheduledTask | Where-Object {$_.TaskPath -like "*malicious*"} | Unregister-ScheduledTask -Confirm:$false
Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "Malware"
```

**Recovery:**

1. **System Rebuild (Gold Image):**
   - Wipe and reinstall from known-good backup
   - Verify integrity (file hashes, AIDE/Tripwire)

2. **Credential Reset:**
   - Force password reset for affected accounts
   - Rotate service account credentials
   - Invalidate all active sessions

3. **Monitoring Enhancement:**
   - Deploy additional sensors on recovered systems
   - Create custom SIEM alerts for re-infection indicators

#### Phase 4: Post-Incident Activity (IR-5)

**Lessons Learned Meeting (Within 2 weeks):**

```markdown
# Post-Incident Review Template
## Incident Summary
- **Incident ID:** INC-2025-001
- **Date:** 2025-01-17
- **Type:** Ransomware
- **Severity:** Critical
- **Duration:** Detection to recovery = 18 hours

## Timeline
- 08:00: Initial phishing email delivered
- 09:30: User opened malicious attachment
- 10:15: Ransomware executed, encrypted 500 files
- 10:20: EDR alert triggered, Tier 1 analyst notified
- 10:35: Tier 2 escalation, containment initiated
- 11:00: Affected system isolated
- 14:00: Forensic analysis complete, IOCs identified
- 18:00: System rebuild from backup
- 02:00 (+1 day): Full recovery, business operations restored

## What Went Well
- EDR detected malware within 5 minutes of execution
- Incident response team mobilized quickly
- Backups were intact and restorable

## What Needs Improvement
- Phishing email bypassed SEG (Secure Email Gateway)
- User security awareness training needed
- Backup restore took 8 hours (target: <4 hours)

## Action Items
- [ ] Implement advanced email filtering (ASSIGNED: Security Team, DUE: 2025-02-01)
- [ ] Conduct phishing simulation training (ASSIGNED: HR, DUE: 2025-01-31)
- [ ] Optimize backup restore process (ASSIGNED: IT Ops, DUE: 2025-02-15)
- [ ] Add ransomware-specific SIEM alerts (ASSIGNED: SOC, DUE: 2025-01-24)
```

**Evidence Retention (IR-6):**
- Preserve all forensic images for 1 year minimum (legal hold: 7+ years)
- Document chain of custody
- Store in encrypted, access-controlled repository

### SIEM Integration & Log Management

#### Log Source Configuration

**Critical Log Sources (Priority 1):**

```yaml
# SIEM Log Source Inventory
log_sources:
  authentication:
    - Active Directory Domain Controllers (Event IDs: 4624, 4625, 4648, 4672, 4768, 4769)
    - VPN gateways (Cisco ASA, Palo Alto GlobalProtect)
    - SSO providers (Okta, Azure AD, Google Workspace)

  network:
    - Firewalls (allow/deny logs, IDS alerts)
    - Proxies (web traffic, SSL inspection)
    - DNS servers (query logs, sinkhole hits)

  endpoints:
    - EDR agents (process execution, file modifications, network connections)
    - Antivirus (detection logs, quarantine events)
    - Windows Event Logs (Security, System, Application)
    - Linux syslog (auth.log, secure, audit.log)

  cloud:
    - AWS CloudTrail (API calls, IAM changes)
    - Azure Activity Log (resource modifications)
    - Google Cloud Audit Logs
    - SaaS application logs (Salesforce, Workday)

  applications:
    - Web servers (Apache access/error logs, IIS logs)
    - Databases (login failures, schema changes)
    - Email gateways (spam/malware blocks, email flow)
```

**Log Parsing & Normalization:**

```python
# Splunk Common Information Model (CIM) Mapping
# Example: Firewall logs to CIM Authentication
[firewall_auth]
LOOKUP-action = firewall_action_lookup action OUTPUT action
EVAL-src = coalesce(src_ip, source_ip)
EVAL-dest = coalesce(dest_ip, destination_ip)
EVAL-user = coalesce(username, user_id)
FIELDALIAS-dest_port = dport AS dest_port
```

#### SIEM Correlation Rules

**Rule 1: Brute Force Attack Detection**

```spl
# Splunk: Failed logins followed by success
index=security sourcetype=auth action=failure
| stats count as failures by src_ip, user
| where failures > 10
| join type=inner src_ip, user [
    search index=security sourcetype=auth action=success
    | stats count by src_ip, user
  ]
| eval severity="high"
| table src_ip, user, failures
```

**Rule 2: Data Exfiltration Detection**

```kql
# Azure Sentinel: Large file upload to external cloud
CommonSecurityLog
| where DeviceAction == "upload"
| where DestinationIP !has "10." and DestinationIP !has "172.16." and DestinationIP !has "192.168."
| summarize TotalBytes = sum(SentBytes) by SourceIP, DestinationIP, bin(TimeGenerated, 5m)
| where TotalBytes > 100000000  // 100 MB
```

**Rule 3: Privilege Escalation**

```spl
# Splunk: User added to Domain Admins
index=security sourcetype=wineventlog EventCode=4728
| eval group_name=mvindex(split(TargetUserName, ","), 0)
| where group_name="Domain Admins" OR group_name="Enterprise Admins"
| table _time, SubjectUserName, TargetUserName, group_name
```

### Threat Hunting Methodologies

#### Hypothesis-Driven Hunting

**Process:**

1. **Formulate Hypothesis:**
   - "Attackers are using stolen credentials to access sensitive file shares"
   - Based on: Recent credential phishing campaign, increased SMB traffic

2. **Define Success Criteria:**
   - Identify unauthorized SMB access to finance file shares
   - Detect access outside business hours

3. **Data Collection:**

```spl
# Splunk: SMB access to sensitive shares
index=security sourcetype=wineventlog EventCode=5140
| eval share_path=lower(ShareName)
| where share_path="\\\\fileserver\\finance" OR share_path="\\\\fileserver\\hr"
| eval hour=strftime(_time, "%H")
| where (hour < 8 OR hour > 18) AND tonumber(hour) != null
| stats count by src_ip, user, share_path
```

4. **Analysis & Validation:**
   - Cross-reference user's normal access patterns (UEBA baseline)
   - Check if source IP is VPN or internal
   - Verify user's job role requires access

5. **Document Findings:**
   - Create IOCs for detected malicious activity
   - Update SIEM alerts
   - Brief SOC team

#### Data-Driven Hunting (Stack Counting)

**Technique: Rare Process Execution**

```spl
# Splunk: Find rare parent-child process relationships
index=security sourcetype=sysmon EventCode=1
| stats count by ParentImage, Image
| where count < 5
| sort count
```

**Technique: Beaconing Detection**

```python
# Python: Detect C2 beaconing via statistical analysis
import pandas as pd
from scipy import stats

# Load network connection logs
df = pd.read_csv('network_connections.csv')
df['interval'] = df.groupby('dest_ip')['timestamp'].diff()

# Calculate coefficient of variation (CV) for each destination
cv_threshold = 0.1  # Low CV = consistent beaconing
for dest_ip in df['dest_ip'].unique():
    intervals = df[df['dest_ip'] == dest_ip]['interval'].dropna()
    if len(intervals) > 10:
        cv = stats.variation(intervals)
        if cv < cv_threshold:
            print(f"Potential beaconing to {dest_ip}, CV={cv:.3f}")
```

### Digital Forensics & Evidence Collection

#### Live System Forensics

**Linux Memory Capture:**

```bash
# Using LiME (Linux Memory Extractor)
sudo insmod lime-$(uname -r).ko "path=/tmp/memory.lime format=lime"

# Analyze with Volatility
volatility -f memory.lime --profile=LinuxUbuntu2004x64 linux_pslist
volatility -f memory.lime --profile=LinuxUbuntu2004x64 linux_netstat
```

**Windows Memory Capture:**

```powershell
# Using Magnet RAM Capture (free tool)
.\MagnetRAMCapture.exe -output C:\forensics\memory.dmp

# Using WinPmem
.\winpmem.exe memory.raw
```

#### Disk Forensics

**Evidence Collection (Forensically Sound):**

```bash
# Linux: Create dd image
sudo dd if=/dev/sda of=/mnt/evidence/disk.img bs=4M status=progress conv=noerror,sync

# Verify integrity
sha256sum /mnt/evidence/disk.img > /mnt/evidence/disk.img.sha256

# Mount as read-only
sudo mount -o ro,loop,noexec,noload /mnt/evidence/disk.img /mnt/analysis
```

**Timeline Analysis:**

```bash
# Generate filesystem timeline with fls + mactime
fls -r -m / /dev/sda1 > filesystem_timeline.body
mactime -b filesystem_timeline.body -d > timeline.csv

# Grep for suspicious activity
grep -i "2025-01-17" timeline.csv | grep -E "(bash|nc|wget|curl)"
```

#### Network Forensics

**PCAP Analysis:**

```bash
# Extract HTTP traffic
tshark -r capture.pcap -Y "http.request" -T fields -e frame.time -e ip.src -e http.request.full_uri

# Find large file downloads
tshark -r capture.pcap -qz io,stat,1,"SUM(frame.len)frame.len" -Y "tcp.port==80"

# Detect DNS tunneling (long subdomain queries)
tshark -r capture.pcap -Y "dns.qry.name" -T fields -e dns.qry.name | awk '{if(length > 50) print}'
```

### Security Metrics & KPIs (NIST IR-4, AU-6)

#### Primary Metrics

**Mean Time To Detect (MTTD):**

```python
# Calculate MTTD from incident data
import pandas as pd

incidents = pd.read_csv('incidents.csv')
incidents['detection_time'] = pd.to_datetime(incidents['detection_time'])
incidents['occurrence_time'] = pd.to_datetime(incidents['occurrence_time'])
incidents['ttd_hours'] = (incidents['detection_time'] - incidents['occurrence_time']).dt.total_seconds() / 3600

mttd = incidents['ttd_hours'].mean()
print(f"MTTD: {mttd:.2f} hours")

# By severity
print(incidents.groupby('severity')['ttd_hours'].mean())
```

**Mean Time To Respond (MTTR):**

```python
# MTTR from detection to containment
incidents['containment_time'] = pd.to_datetime(incidents['containment_time'])
incidents['ttr_hours'] = (incidents['containment_time'] - incidents['detection_time']).dt.total_seconds() / 3600

mttr = incidents['ttr_hours'].mean()
print(f"MTTR: {mttr:.2f} hours")
```

**Incident Trends:**

```python
# Monthly incident count by type
import matplotlib.pyplot as plt

incidents['month'] = incidents['detection_time'].dt.to_period('M')
incident_trends = incidents.groupby(['month', 'type']).size().unstack(fill_value=0)

incident_trends.plot(kind='bar', stacked=True)
plt.title('Incident Trends by Type')
plt.ylabel('Count')
plt.xlabel('Month')
plt.show()
```

**False Positive Rate:**

```python
# Calculate FP rate
total_alerts = 1000
true_positives = 150
false_positives = 850

fp_rate = false_positives / total_alerts * 100
print(f"False Positive Rate: {fp_rate:.1f}%")
# Target: <10%
```

#### Dashboard Visualization

**Grafana Dashboard (JSON Export):**

See bundled resource: `templates/security-metrics-dashboard.json`

**Key Panels:**
- MTTD/MTTR trend line graph
- Incident severity distribution (pie chart)
- Top 10 alert sources (bar chart)
- SOC analyst workload (heatmap)
- Threat actor attribution (world map)

### Incident Response Playbooks

#### Playbook 1: Phishing Response

**Trigger:** User reports suspicious email OR email security gateway flags malicious attachment

**Actions:**

1. **Containment (5 minutes):**
   - Quarantine email from all mailboxes (Exchange PowerShell)
   - Block sender domain at email gateway
   - Disable any compromised accounts

```powershell
# Exchange: Delete phishing email
Search-Mailbox -Identity * -SearchQuery 'Subject:"Urgent: Password Expiration"' -DeleteContent
```

2. **Analysis (30 minutes):**
   - Extract email headers (sender IP, SPF/DKIM/DMARC results)
   - Analyze attachments in sandbox (ANY.RUN, Hybrid Analysis)
   - Check for payload delivery (EDR alerts, web proxy logs)

3. **Eradication:**
   - Remove malware from infected endpoints (EDR remediation)
   - Reset passwords for affected users

4. **Recovery:**
   - Restore deleted files from backup
   - Re-enable accounts after credential reset

5. **Post-Incident:**
   - Update phishing training materials
   - Add IOCs to threat intelligence platform
   - Tune email security rules

#### Playbook 2: Ransomware Response

**Trigger:** EDR detects mass file encryption OR user reports encrypted files with ransom note

**Actions:**

1. **Immediate Containment (<5 minutes):**
   - Isolate infected host (network disconnect)
   - Identify ransomware variant (ransom note, file extensions)
   - Preserve memory image for forensics

2. **Impact Assessment (30 minutes):**
   - How many systems encrypted?
   - What data affected? (finance, PII, IP)
   - Are backups intact?

3. **Eradication:**
   - Do NOT pay ransom (FBI/CISA guidance)
   - Wipe infected systems
   - Remove ransomware from network shares

4. **Recovery:**
   - Restore from backups (test integrity first)
   - Rebuild systems from gold image
   - Verify decryption (if free tool available from No More Ransom)

5. **Post-Incident:**
   - Review backup strategy (offline/immutable backups)
   - Patch vulnerable systems
   - Implement application whitelisting

#### Playbook 3: Data Breach Response (IR-6)

**Trigger:** Unauthorized data access detected OR external notification of leaked data

**Actions:**

1. **Containment (15 minutes):**
   - Revoke API keys/credentials
   - Block attacker IP addresses
   - Enable enhanced logging

2. **Scope Determination (2-4 hours):**
   - What data was accessed? (query database audit logs)
   - How many records? What PII fields?
   - Timeline of unauthorized access

3. **Legal/Regulatory Notification:**
   - Notify legal counsel immediately
   - **GDPR:** 72-hour breach notification to supervisory authority
   - **CCPA:** Notify California Attorney General if >500 residents affected
   - **HIPAA:** Notify HHS within 60 days

4. **Customer Communication:**
   - Draft notification letter (legal review required)
   - Offer credit monitoring services
   - Set up dedicated support line

5. **Remediation:**
   - Fix vulnerability that led to breach
   - Implement additional access controls
   - Conduct third-party security audit

### NIST 800-53 IR Control Implementation

**IR-4: Incident Handling**

```yaml
# Incident Handling Capability
ir_4_implementation:
  incident_handling_capability:
    - automated_detection: SIEM correlation rules, EDR behavioral analysis
    - manual_reporting: Security hotline, email alias (security@company.com)
    - tracking_system: Jira Service Management, incident tickets

  incident_response_plan:
    - documented: Yes, last reviewed 2025-01-01
    - tested: Quarterly tabletop exercises
    - updated: After each major incident

  coordination:
    - internal: IT operations, legal, HR, executive leadership
    - external: Law enforcement (FBI IC3), cyber insurance, forensic vendors
```

**IR-5: Incident Monitoring**

```yaml
ir_5_implementation:
  tracking_metrics:
    - incidents_per_month: Trend analysis
    - mttd_mttr: By severity level
    - false_positive_rate: Weekly review

  reporting:
    - executive_dashboard: Monthly
    - board_of_directors: Quarterly
    - regulatory: As required (SEC 8-K for material breaches)
```

**IR-6: Incident Reporting**

```yaml
ir_6_implementation:
  internal_reporting:
    - soc_to_management: Within 1 hour for critical incidents
    - management_to_board: Within 24 hours

  external_reporting:
    - law_enforcement: For criminal activity (FBI, Secret Service)
    - regulatory: GDPR (72h), HIPAA (60d), SEC (4 business days)
    - cyber_insurance: Within policy timeframe (typically 24-48h)

  information_sharing:
    - isac_participation: FS-ISAC, H-ISAC (sector-specific)
    - ttp_sharing: MISP, STIX/TAXII feeds
```

**SI-4: Information System Monitoring**

```yaml
si_4_implementation:
  monitoring_tools:
    - siem: Splunk Enterprise Security
    - ids_ips: Snort, Suricata
    - edr: CrowdStrike Falcon
    - network_tap: Full packet capture (90 days retention)

  monitoring_coverage:
    - network_perimeter: 100%
    - internal_segments: 95% (DMZ, production, corporate)
    - endpoints: 98% (servers, workstations)
    - cloud_assets: 90% (AWS, Azure)

  alert_escalation:
    - critical: Immediate phone call
    - high: Email + Slack within 15 min
    - medium: Ticket creation within 1 hour
```

**AU-6: Audit Review, Analysis, and Reporting**

```yaml
au_6_implementation:
  log_review_frequency:
    - real_time: SIEM automated correlation
    - daily: SOC analyst review of high-fidelity alerts
    - weekly: Trend analysis, false positive tuning
    - monthly: Executive report, compliance reporting

  analysis_techniques:
    - signature_based: Known malware, exploits
    - anomaly_based: UEBA, statistical outlier detection
    - threat_intelligence: IOC matching, TTP correlation

  reporting:
    - automated: Daily SOC metrics email
    - manual: Monthly security posture report
    - adhoc: Incident-specific reports for management
```

### Security Operations Best Practices

**SOC Efficiency Tips:**

1. **Automate Tier 1 Tasks:**
   - Use SOAR (Security Orchestration, Automation, Response) for common playbooks
   - Auto-enrich alerts with threat intel (IP reputation, domain age)
   - Automated containment for high-confidence alerts

2. **Reduce Alert Fatigue:**
   - Tune SIEM rules quarterly (disable low-value alerts)
   - Implement alert grouping/deduplication
   - Use risk-based alerting (asset criticality × threat severity)

3. **Continuous Improvement:**
   - Post-incident reviews for every P1/P2 incident
   - Track false positive sources, fix root cause
   - Share lessons learned across team (monthly knowledge sharing)

4. **Threat Intelligence Integration:**
   - Subscribe to relevant ISAC feeds
   - Correlate internal incidents with global campaigns
   - Contribute anonymized IOCs back to community

5. **Training & Development:**
   - Certifications: GCIH, GCFA, GCIA, OSCP
   - Hands-on labs: TryHackMe, HackTheBox, CyberDefenders
   - Conference attendance: DEF CON, Black Hat, BSides

**Common Pitfalls to Avoid:**

- **Alert Overload:** Tune, don't just forward all logs to SIEM
- **Inadequate Documentation:** Every incident must have a ticket
- **Poor Communication:** Keep stakeholders updated (no surprises)
- **Neglecting Backups:** Test restore process regularly
- **Single Point of Failure:** Redundant SIEM collectors, analysts on-call


---

## Level 3: Deep Dive Resources

### Bundled Resources

This skill includes 6 ready-to-use templates and scripts:

1. **`templates/incident-response-playbook.md`**
   - Complete IR playbooks for phishing, malware, DDoS, data breach
   - Step-by-step checklists with NIST control mappings
   - Communication templates (internal, external, regulatory)

2. **`templates/siem-queries.md`**
   - 50+ production-ready SIEM queries
   - Splunk SPL, ELK KQL, Azure Sentinel KQL
   - Categorized by MITRE ATT&CK tactics

3. **`scripts/forensics-collection.sh`**
   - Automated Linux forensics evidence collection
   - Memory dump, disk imaging, log preservation
   - Chain-of-custody documentation

4. **`templates/post-incident-report.md`**
   - Post-incident report template with root cause analysis
   - Lessons learned framework
   - Action item tracking

5. **`templates/security-metrics-dashboard.json`**
   - Grafana dashboard for security metrics
   - MTTD, MTTR, incident trends, SOC workload
   - Ready to import

6. **`resources/nist-ir-controls.md`**
   - NIST 800-61 incident response guide mapping
   - NIST 800-53 IR control implementation details
   - Compliance checklist

### Advanced Training Paths

**Incident Response Certifications:**
- **GCIH (GIAC Certified Incident Handler):** Industry-standard IR certification
- **GCFA (GIAC Certified Forensic Analyst):** Advanced forensics
- **GCIA (GIAC Certified Intrusion Analyst):** Network traffic analysis
- **OSCP (Offensive Security Certified Professional):** Penetration testing (know the attacker mindset)

**Hands-On Labs:**
- **TryHackMe:** "SOC Level 1" and "Cyber Defense" paths
- **CyberDefenders:** Blue team challenges with real incident data
- **SANS NetWars:** Capture-the-flag style incident response

**Recommended Reading:**
- *Incident Response & Computer Forensics* by Jason Luttgens (McGraw-Hill)
- *The Art of Memory Forensics* by Michael Hale Ligh (Wiley)
- *Blue Team Handbook: SOC, SIEM, and Threat Hunting* by Don Murdoch (CreateSpace)

### NIST Framework References

- **NIST 800-61 Rev 2:** Computer Security Incident Handling Guide
  - <https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final>
- **NIST 800-53 Rev 5:** Security and Privacy Controls (IR Family)
  - <https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final>
- **NIST 800-86:** Guide to Integrating Forensic Techniques into Incident Response
  - <https://csrc.nist.gov/publications/detail/sp/800-86/final>

### Tools & Resources

**Open-Source SIEM:**
- Wazuh: <https://wazuh.com>
- Elastic Security: <https://www.elastic.co/security>
- Graylog: <https://www.graylog.org>

**Threat Intelligence Platforms:**
- MISP (Open Source): <https://www.misp-project.org>
- AlienVault OTX: <https://otx.alienvault.com>
- STIX/TAXII: <https://oasis-open.github.io/cti-documentation/>

**Forensic Tools:**
- Volatility (Memory Analysis): <https://www.volatilityfoundation.org>
- Autopsy (Disk Forensics): <https://www.autopsy.com>
- Wireshark (Network Analysis): <https://www.wireshark.org>

**Incident Response Frameworks:**
- MITRE ATT&CK: <https://attack.mitre.org>
- NIST Cybersecurity Framework: <https://www.nist.gov/cyberframework>
- SANS Incident Response Process: <https://www.sans.org/blog/the-importance-of-incident-response-planning/>

### Community & Collaboration

**ISACs (Information Sharing and Analysis Centers):**
- FS-ISAC (Financial Services)
- H-ISAC (Healthcare)
- MS-ISAC (Multi-State, government)
- ICS-ISAC (Industrial Control Systems)

**Conferences:**
- DEF CON (Las Vegas, August)
- Black Hat (multiple locations)
- RSA Conference (San Francisco, April)
- BSides (local chapters worldwide)

**Online Communities:**
- Reddit: r/AskNetsec, r/blueteamsec
- Discord: SANS Cyber Defense Initiative, TryHackMe
- Twitter: #infosec, #threatintel, #dfir

---

## Summary & Next Steps

You've learned:
- Security Operations Center structure and processes
- Incident response lifecycle (NIST 800-61 Rev 2)
- SIEM integration and log analysis
- Threat hunting methodologies
- Digital forensics and evidence collection
- Security metrics and KPIs
- NIST 800-53 IR control implementation

**Validation Exercise:**

Set up a mini SOC lab:
1. Deploy Wazuh SIEM (Docker or VM)
2. Forward logs from 3 systems (Linux, Windows, network device)
3. Create 5 custom correlation rules
4. Simulate an incident (Metasploit attack)
5. Respond using IR playbook
6. Write post-incident report

**Time estimate:** 8-12 hours

**Related Skills:**
- [Security Fundamentals](../security-fundamentals/SKILL.md)
- [Network Security](../network-security/SKILL.md)
- [Linux Security](../linux-security/SKILL.md)
- [Cloud Security](../cloud-security/SKILL.md)

**Compliance Mapping:**
- NIST IR-4, IR-5, IR-6, SI-4, AU-6
- ISO 27001: A.16.1 (Incident Management)
- PCI-DSS: Requirement 12.10 (Incident Response Plan)
- SOC 2: CC7.3 (Security Incidents)

---

*Last Updated: 2025-01-17*
*Version: 1.0.0*
*Maintained by: Security Operations Team*
