# Security Operations - Reference Implementation

This document contains detailed configuration examples and full code samples extracted from the main skill guide to keep the implementation guide concise.

## Table of Contents

- [Security Operations Center (SOC) Structure](#security-operations-center-(soc)-structure)
- [SOC Team Roles & Responsibilities](#soc-team-roles--responsibilities)
- [SOC Tools & Technologies](#soc-tools--technologies)
- [Incident Response Lifecycle (NIST 800-61 Rev 2)](#incident-response-lifecycle-(nist-800-61-rev-2))
- [Phase 1: Preparation (IR-4)](#phase-1:-preparation-(ir-4))
- [Phase 2: Detection & Analysis (SI-4, AU-6)](#phase-2:-detection--analysis-(si-4,-au-6))
- [Phase 3: Containment, Eradication & Recovery (IR-4)](#phase-3:-containment,-eradication--recovery-(ir-4))
- [Phase 4: Post-Incident Activity (IR-5)](#phase-4:-post-incident-activity-(ir-5))
- [SIEM Integration & Log Management](#siem-integration--log-management)
- [Log Source Configuration](#log-source-configuration)

---

## Code Examples

### Example 0

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

### Example 1

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

### Example 2

```spl
# Splunk: Detect lateral movement via SMB
index=security sourcetype=wineventlog EventCode=4624
| where LogonType=3 AND AuthenticationPackageName="NTLM"
| transaction src_ip maxspan=5m
| where eventcount > 10
| table _time, src_ip, dest_host, user
```

### Example 3

```kql
# Azure Sentinel: Detect credential dumping
SecurityEvent
| where EventID in (4672, 4673, 4674)
| where Process has_any ("lsass.exe", "mimikatz", "procdump")
| extend Timestamp, Computer, Account, Process
| summarize count() by bin(Timestamp, 5m), Computer, Account
```

### Example 4

```bash
# Check IP against threat feeds
curl -s "https://otx.alienvault.com/api/v1/indicators/IPv4/$IP/general" | jq '.pulse_info.count'

# Check file hash against VirusTotal
curl -s "https://www.virustotal.com/api/v3/files/$HASH" \
  -H "x-apikey: $VT_API_KEY" | jq '.data.attributes.last_analysis_stats'
```

### Example 5

```bash
# Linux: Network isolation
sudo iptables -A INPUT -j DROP
sudo iptables -A OUTPUT -j DROP
sudo iptables -A OUTPUT -d 10.0.0.100 -j ACCEPT  # Allow forensic server

# Windows: Disable network adapter via PowerShell
Disable-NetAdapter -Name "Ethernet" -Confirm:$false
```

### Example 6

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

### Example 7

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

### Example 8

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

### Example 9

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

### Example 10

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

### Example 11

```kql
# Azure Sentinel: Large file upload to external cloud
CommonSecurityLog
| where DeviceAction == "upload"
| where DestinationIP !has "10." and DestinationIP !has "172.16." and DestinationIP !has "192.168."
| summarize TotalBytes = sum(SentBytes) by SourceIP, DestinationIP, bin(TimeGenerated, 5m)
| where TotalBytes > 100000000  // 100 MB
```

### Example 12

```spl
# Splunk: User added to Domain Admins
index=security sourcetype=wineventlog EventCode=4728
| eval group_name=mvindex(split(TargetUserName, ","), 0)
| where group_name="Domain Admins" OR group_name="Enterprise Admins"
| table _time, SubjectUserName, TargetUserName, group_name
```

### Example 13

```spl
# Splunk: SMB access to sensitive shares
index=security sourcetype=wineventlog EventCode=5140
| eval share_path=lower(ShareName)
| where share_path="\\\\fileserver\\finance" OR share_path="\\\\fileserver\\hr"
| eval hour=strftime(_time, "%H")
| where (hour < 8 OR hour > 18) AND tonumber(hour) != null
| stats count by src_ip, user, share_path
```

### Example 15

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

### Example 16

```bash
# Using LiME (Linux Memory Extractor)
sudo insmod lime-$(uname -r).ko "path=/tmp/memory.lime format=lime"

# Analyze with Volatility
volatility -f memory.lime --profile=LinuxUbuntu2004x64 linux_pslist
volatility -f memory.lime --profile=LinuxUbuntu2004x64 linux_netstat
```

### Example 18

```bash
# Linux: Create dd image
sudo dd if=/dev/sda of=/mnt/evidence/disk.img bs=4M status=progress conv=noerror,sync

# Verify integrity
sha256sum /mnt/evidence/disk.img > /mnt/evidence/disk.img.sha256

# Mount as read-only
sudo mount -o ro,loop,noexec,noload /mnt/evidence/disk.img /mnt/analysis
```

### Example 19

```bash
# Generate filesystem timeline with fls + mactime
fls -r -m / /dev/sda1 > filesystem_timeline.body
mactime -b filesystem_timeline.body -d > timeline.csv

# Grep for suspicious activity
grep -i "2025-01-17" timeline.csv | grep -E "(bash|nc|wget|curl)"
```

### Example 20

```bash
# Extract HTTP traffic
tshark -r capture.pcap -Y "http.request" -T fields -e frame.time -e ip.src -e http.request.full_uri

# Find large file downloads
tshark -r capture.pcap -qz io,stat,1,"SUM(frame.len)frame.len" -Y "tcp.port==80"

# Detect DNS tunneling (long subdomain queries)
tshark -r capture.pcap -Y "dns.qry.name" -T fields -e dns.qry.name | awk '{if(length > 50) print}'
```

### Example 21

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

### Example 22

```python
# MTTR from detection to containment
incidents['containment_time'] = pd.to_datetime(incidents['containment_time'])
incidents['ttr_hours'] = (incidents['containment_time'] - incidents['detection_time']).dt.total_seconds() / 3600

mttr = incidents['ttr_hours'].mean()
print(f"MTTR: {mttr:.2f} hours")
```

### Example 23

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

### Example 26

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

### Example 27

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

### Example 28

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

### Example 29

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

### Example 30

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

---

## Additional Resources

See the main SKILL.md file for essential patterns and the official documentation for complete API references.
