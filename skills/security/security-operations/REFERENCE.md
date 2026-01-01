# Security Operations - Complete Reference

This document contains detailed configuration examples, full code samples, and production-ready implementations for Security Operations. Use this as a companion to the main [SKILL.md](./SKILL.md).

## Table of Contents

- [SOC Team Structure](#soc-team-structure)
- [Detection Sources](#detection-sources)
- [SIEM Analysis Queries](#siem-analysis-queries)
- [Threat Intelligence Integration](#threat-intelligence-integration)
- [Containment Procedures](#containment-procedures)
- [Eradication Steps](#eradication-steps)
- [Post-Incident Report Template](#post-incident-report-template)
- [Log Source Configuration](#log-source-configuration)
- [Log Parsing & Normalization](#log-parsing--normalization)
- [SIEM Correlation Rules](#siem-correlation-rules)
- [Threat Hunting Queries](#threat-hunting-queries)
- [Forensics Procedures](#forensics-procedures)
- [Security Metrics Scripts](#security-metrics-scripts)
- [NIST Control Implementation](#nist-control-implementation)
- [Additional Playbook Details](#additional-playbook-details)

---

## SOC Team Structure

<a id="example-0"></a>

### Example 0: IR Team Structure Template

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

# Escalation Matrix
escalation_matrix:
  critical:
    notify_within: 15_minutes
    contacts: [CISO, CTO, Legal, CEO]
    communication: phone_call
  high:
    notify_within: 1_hour
    contacts: [SOC_Manager, IT_Director]
    communication: slack_and_email
  medium:
    notify_within: 4_hours
    contacts: [Tier_3_Lead]
    communication: ticket_update
  low:
    notify_within: 24_hours
    contacts: [Tier_2_Lead]
    communication: daily_standup
```

---

## Detection Sources

<a id="example-1"></a>

### Example 1: Detection Source Priority Matrix

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

# Priority scoring for alert triage
def calculate_alert_priority(alert):
    """Calculate priority score for SIEM alerts."""
    base_score = 0

    # Source fidelity
    if alert.source in detection_sources["high_fidelity"]:
        base_score += 80
    elif alert.source in detection_sources["medium_fidelity"]:
        base_score += 50
    else:
        base_score += 20

    # Asset criticality
    asset_scores = {"critical": 20, "high": 15, "medium": 10, "low": 5}
    base_score += asset_scores.get(alert.asset_criticality, 5)

    # Threat intel correlation
    if alert.has_threat_intel_match:
        base_score += 30

    return min(base_score, 100)
```

---

## SIEM Analysis Queries

<a id="example-2"></a>

### Example 2: Lateral Movement Detection (Splunk)

```spl
# Splunk: Detect lateral movement via SMB
index=security sourcetype=wineventlog EventCode=4624
| where LogonType=3 AND AuthenticationPackageName="NTLM"
| transaction src_ip maxspan=5m
| where eventcount > 10
| table _time, src_ip, dest_host, user
| sort -eventcount
```

<a id="example-3"></a>

### Example 3: Credential Dumping Detection (Azure Sentinel)

```kql
# Azure Sentinel: Detect credential dumping
SecurityEvent
| where EventID in (4672, 4673, 4674)
| where Process has_any ("lsass.exe", "mimikatz", "procdump")
| extend Timestamp, Computer, Account, Process
| summarize count() by bin(Timestamp, 5m), Computer, Account

# Additional: Detect Mimikatz-like activity
SecurityEvent
| where EventID == 10
| where TargetImage has "lsass.exe"
| where SourceImage !has "csrss.exe" and SourceImage !has "wininit.exe"
| project TimeGenerated, Computer, SourceImage, TargetImage
```

### Example: Suspicious PowerShell Execution

```spl
# Splunk: Detect encoded PowerShell commands
index=security sourcetype=wineventlog EventCode=4104
| eval decoded=base64decode(ScriptBlockText)
| where decoded LIKE "%Invoke-Mimikatz%" OR decoded LIKE "%Get-Credential%"
   OR decoded LIKE "%DownloadString%" OR decoded LIKE "%IEX%"
| table _time, Computer, User, ScriptBlockText

# Splunk: PowerShell download cradles
index=security sourcetype=sysmon EventCode=1
| where Image="*\\powershell.exe" OR Image="*\\pwsh.exe"
| where CommandLine LIKE "*WebClient*" OR CommandLine LIKE "*curl*"
   OR CommandLine LIKE "*wget*" OR CommandLine LIKE "*Invoke-WebRequest*"
| stats count by Computer, User, CommandLine
```

---

## Threat Intelligence Integration

<a id="example-4"></a>

### Example 4: Threat Feed Lookup Scripts

```bash
#!/bin/bash
# Threat intelligence lookup script

# Check IP against threat feeds
check_ip_reputation() {
    IP=$1

    # AlienVault OTX
    echo "=== AlienVault OTX ==="
    curl -s "https://otx.alienvault.com/api/v1/indicators/IPv4/$IP/general" \
        -H "X-OTX-API-KEY: $OTX_API_KEY" | jq '.pulse_info.count'

    # AbuseIPDB
    echo "=== AbuseIPDB ==="
    curl -s "https://api.abuseipdb.com/api/v2/check" \
        -H "Key: $ABUSEIPDB_KEY" \
        -d "ipAddress=$IP" | jq '.data.abuseConfidenceScore'

    # VirusTotal (if you have API access)
    echo "=== VirusTotal ==="
    curl -s "https://www.virustotal.com/api/v3/ip_addresses/$IP" \
        -H "x-apikey: $VT_API_KEY" | jq '.data.attributes.last_analysis_stats'
}

# Check file hash against VirusTotal
check_hash() {
    HASH=$1
    curl -s "https://www.virustotal.com/api/v3/files/$HASH" \
        -H "x-apikey: $VT_API_KEY" | jq '.data.attributes.last_analysis_stats'
}

# Check domain reputation
check_domain() {
    DOMAIN=$1

    # Whois age check
    CREATED=$(whois "$DOMAIN" | grep -i "creation date" | head -1)
    echo "Domain created: $CREATED"

    # URLhaus check
    curl -s "https://urlhaus-api.abuse.ch/v1/host/" \
        -d "host=$DOMAIN" | jq '.query_status, .urls[0].threat'
}

# Usage
check_ip_reputation "192.0.2.100"
check_hash "44d88612fea8a8f36de82e1278abb02f"
check_domain "suspicious-domain.xyz"
```

### Python MISP Integration

```python
from pymisp import PyMISP

class ThreatIntelManager:
    def __init__(self, misp_url, misp_key):
        self.misp = PyMISP(misp_url, misp_key, ssl=True)

    def search_ioc(self, ioc_value, ioc_type="ip-dst"):
        """Search for an IOC in MISP."""
        result = self.misp.search(value=ioc_value, type=ioc_type)
        return result

    def add_event_from_incident(self, incident):
        """Create MISP event from incident findings."""
        event = self.misp.new_event(
            distribution=0,  # Organization only
            threat_level_id=2,  # Medium
            analysis=1,  # Ongoing
            info=f"Incident {incident['id']}: {incident['title']}"
        )

        for ioc in incident.get('iocs', []):
            self.misp.add_attribute(
                event,
                type=ioc['type'],
                value=ioc['value'],
                comment=ioc.get('comment', '')
            )

        return event
```

---

## Containment Procedures

<a id="example-5"></a>

### Example 5: Network Isolation Commands

```bash
#!/bin/bash
# Emergency containment script for Linux hosts

# Immediate network isolation (allow only forensic server)
isolate_host() {
    FORENSIC_SERVER="10.0.0.100"

    # Backup current rules
    iptables-save > /tmp/iptables-backup-$(date +%Y%m%d_%H%M%S)

    # Drop all traffic
    sudo iptables -F
    sudo iptables -P INPUT DROP
    sudo iptables -P OUTPUT DROP
    sudo iptables -P FORWARD DROP

    # Allow loopback
    sudo iptables -A INPUT -i lo -j ACCEPT
    sudo iptables -A OUTPUT -o lo -j ACCEPT

    # Allow forensic server only
    sudo iptables -A OUTPUT -d $FORENSIC_SERVER -j ACCEPT
    sudo iptables -A INPUT -s $FORENSIC_SERVER -j ACCEPT

    echo "Host isolated. Only $FORENSIC_SERVER allowed."
}

# Windows: Disable network adapter via PowerShell
# Disable-NetAdapter -Name "Ethernet" -Confirm:$false
# Alternative: Use Windows Firewall
# netsh advfirewall set allprofiles firewallpolicy blockinbound,blockoutbound

# For cloud instances (AWS)
isolate_ec2_instance() {
    INSTANCE_ID=$1
    ISOLATION_SG="sg-isolation-only-ssh"

    aws ec2 modify-instance-attribute \
        --instance-id $INSTANCE_ID \
        --groups $ISOLATION_SG

    echo "EC2 instance $INSTANCE_ID moved to isolation security group"
}
```

### EDR Containment Commands

```powershell
# CrowdStrike Falcon containment
# Via API
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}
$body = @{
    "ids" = @("device_id_here")
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.crowdstrike.com/devices/entities/devices-actions/v2?action_name=contain" `
    -Method POST -Headers $headers -Body $body

# Microsoft Defender ATP isolation
$machineId = "machine_id_here"
Invoke-WebRequest -Uri "https://api.securitycenter.microsoft.com/api/machines/$machineId/isolate" `
    -Method POST -Headers $headers -Body '{"Comment": "Isolated for IR", "IsolationType": "Full"}'
```

---

## Eradication Steps

<a id="example-6"></a>

### Example 6: Malware Removal Procedures

```bash
#!/bin/bash
# Linux malware eradication script

# Remove persistence mechanisms
remove_persistence() {
    echo "=== Checking cron jobs ==="
    for user in $(cut -f1 -d: /etc/passwd); do
        crontab -l -u $user 2>/dev/null | grep -v "^#"
    done

    echo "=== Checking systemd services ==="
    systemctl list-unit-files --type=service | grep -E "enabled|bad"

    echo "=== Checking /etc/rc.local ==="
    cat /etc/rc.local 2>/dev/null

    echo "=== Checking init.d ==="
    ls -la /etc/init.d/

    # Remove specific malicious entries (customize as needed)
    sudo crontab -l | grep -v "malicious.sh" | crontab -
    sudo systemctl disable malicious-service
    sudo rm -f /etc/systemd/system/malicious.service
    sudo systemctl daemon-reload
}

# Remove malicious files
remove_malware_files() {
    # Common malware locations
    LOCATIONS=(
        "/tmp/.hidden"
        "/var/tmp/.cache"
        "/dev/shm/.x"
        "$HOME/.local/share/."
    )

    for loc in "${LOCATIONS[@]}"; do
        if [ -e "$loc" ]; then
            echo "Found suspicious: $loc"
            # Archive before deletion
            tar czf /evidence/$(date +%Y%m%d)_$(basename $loc).tar.gz "$loc"
            rm -rf "$loc"
        fi
    done
}

# Verify clean state
verify_clean() {
    # Check for common backdoor indicators
    netstat -tulpn | grep -E ":4444|:1337|:8080"
    ps aux | grep -E "nc|ncat|netcat|.hidden"
    find / -name "*.php" -mtime -1 2>/dev/null
}
```

```powershell
# Windows malware eradication script

# Remove scheduled task persistence
Get-ScheduledTask | Where-Object {$_.TaskPath -like "*suspicious*"} | Unregister-ScheduledTask -Confirm:$false

# Remove registry run keys
$runKeys = @(
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run",
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce"
)

foreach ($key in $runKeys) {
    Get-ItemProperty -Path $key | ForEach-Object {
        $_.PSObject.Properties | Where-Object {$_.Value -like "*suspicious*"} | ForEach-Object {
            Remove-ItemProperty -Path $key -Name $_.Name -Force
            Write-Host "Removed: $($_.Name) from $key"
        }
    }
}

# Remove malicious services
Get-Service | Where-Object {$_.DisplayName -like "*backdoor*"} | ForEach-Object {
    Stop-Service $_.Name -Force
    sc.exe delete $_.Name
}

# Remove WMI persistence
Get-WMIObject -Namespace root\subscription -Class __EventFilter | Where-Object {$_.Name -like "*malicious*"} | Remove-WMIObject
Get-WMIObject -Namespace root\subscription -Class __EventConsumer | Where-Object {$_.Name -like "*malicious*"} | Remove-WMIObject
```

---

## Post-Incident Report Template

<a id="example-7"></a>

### Example 7: Complete Post-Incident Report

```markdown
# Post-Incident Review Report

## Executive Summary
- **Incident ID:** INC-2025-001
- **Date:** 2025-01-17
- **Type:** Ransomware
- **Severity:** Critical
- **Duration:** Detection to recovery = 18 hours
- **Business Impact:** Finance department offline for 8 hours, $50K estimated loss

## Incident Timeline

| Time | Event | Actor |
|------|-------|-------|
| 08:00 | Initial phishing email delivered to user@company.com | Attacker |
| 09:30 | User opened malicious attachment (Invoice.xlsm) | User |
| 09:32 | Macro executed, PowerShell download initiated | Malware |
| 09:35 | Cobalt Strike beacon established to 203.0.113.50 | Malware |
| 10:15 | Ransomware payload deployed, 500 files encrypted | Malware |
| 10:20 | EDR alert triggered, Tier 1 analyst notified | SOC |
| 10:25 | Tier 1 validated alert, escalated to Tier 2 | SOC |
| 10:35 | Tier 2 initiated containment (host isolated) | SOC |
| 11:00 | Affected system network isolated | IT Ops |
| 14:00 | Forensic analysis complete, IOCs identified | Tier 3 |
| 18:00 | System rebuild from backup initiated | IT Ops |
| 02:00 (+1 day) | Full recovery, business operations restored | IT Ops |

## Attack Analysis

### Initial Access
- **Vector:** Spear phishing email with malicious Excel attachment
- **Sender:** spoofed internal user (invoice@company-corp.com)
- **Email bypassed SEG:** Yes (DMARC not enforced)

### Execution
- **Technique:** Excel macro → PowerShell download cradle
- **Payload URL:** https://cdn-update[.]net/patch.exe
- **Malware family:** LockBit 3.0

### Indicators of Compromise (IOCs)
| Type | Value | Context |
|------|-------|---------|
| IP | 203.0.113.50 | C2 server |
| Domain | cdn-update[.]net | Payload hosting |
| Hash (SHA256) | a1b2c3d4... | patch.exe (LockBit) |
| Hash (SHA256) | e5f6g7h8... | Invoice.xlsm |
| Email | invoice@company-corp.com | Sender |

## What Went Well
1. EDR detected malware within 5 minutes of execution
2. Incident response team mobilized quickly (<15 min)
3. Backups were intact and restorable
4. No lateral movement detected (single host contained)
5. Customer data not exfiltrated (based on network analysis)

## What Needs Improvement
1. Phishing email bypassed Secure Email Gateway (SEG)
   - **Root Cause:** DMARC not enforced, lookalike domain not blocked
2. User clicked despite recent training
   - **Root Cause:** Highly targeted spear phish, no visual warning
3. Backup restore took 8 hours (target: <4 hours)
   - **Root Cause:** Large dataset, single restore stream

## Action Items

| ID | Action | Owner | Due Date | Status |
|----|--------|-------|----------|--------|
| 1 | Implement DMARC enforcement (p=reject) | Email Admin | 2025-02-01 | In Progress |
| 2 | Block lookalike domains at email gateway | Security | 2025-01-24 | Open |
| 3 | Conduct targeted phishing simulation | HR/Security | 2025-01-31 | Open |
| 4 | Optimize backup restore (parallel streams) | IT Ops | 2025-02-15 | Open |
| 5 | Add LockBit-specific SIEM detection rules | SOC | 2025-01-24 | Open |
| 6 | Enable macro blocking for external Office docs | Desktop Eng | 2025-02-01 | Open |

## Lessons Learned
1. Email security is first line of defense - requires continuous tuning
2. User awareness training must be ongoing and scenario-based
3. Backup restore capability should be tested monthly
4. EDR + network isolation prevented catastrophic outcome

## Cost Summary
- Downtime cost: $50,000 (estimated)
- Forensics vendor: $15,000
- Remediation labor: $10,000
- **Total:** $75,000

## Appendices
- A: Forensic timeline (detailed)
- B: Network traffic analysis
- C: Malware reverse engineering report
- D: Communication log

---
**Report prepared by:** SOC Team Lead
**Date:** 2025-01-20
**Distribution:** CISO, IT Director, Legal, HR
```

---

## Log Source Configuration

<a id="example-8"></a>

### Example 8: SIEM Log Source Inventory

```yaml
# SIEM Log Source Inventory
log_sources:
  authentication:
    - name: Active Directory Domain Controllers
      events: [4624, 4625, 4648, 4672, 4768, 4769, 4771]
      priority: critical
      retention: 1_year
    - name: VPN gateways
      types: [Cisco ASA, Palo Alto GlobalProtect]
      priority: critical
    - name: SSO providers
      types: [Okta, Azure AD, Google Workspace]
      priority: critical

  network:
    - name: Firewalls
      data: [allow/deny logs, IDS alerts]
      priority: critical
    - name: Proxies
      data: [web traffic, SSL inspection]
      priority: high
    - name: DNS servers
      data: [query logs, sinkhole hits]
      priority: high

  endpoints:
    - name: EDR agents
      data: [process execution, file modifications, network connections]
      priority: critical
    - name: Antivirus
      data: [detection logs, quarantine events]
      priority: high
    - name: Windows Event Logs
      channels: [Security, System, Application, Sysmon]
      priority: critical
    - name: Linux syslog
      files: [auth.log, secure, audit.log, messages]
      priority: critical

  cloud:
    - name: AWS CloudTrail
      data: [API calls, IAM changes, S3 access]
      priority: critical
    - name: Azure Activity Log
      data: [resource modifications, sign-ins]
      priority: critical
    - name: Google Cloud Audit Logs
      priority: critical
    - name: SaaS applications
      types: [Salesforce, Workday, Office 365]
      priority: high

  applications:
    - name: Web servers
      types: [Apache access/error, IIS, Nginx]
      priority: high
    - name: Databases
      data: [login failures, schema changes, privileged queries]
      priority: high
    - name: Email gateways
      data: [spam/malware blocks, email flow, DLP alerts]
      priority: critical
```

---

## Log Parsing & Normalization

<a id="example-9"></a>

### Example 9: Splunk CIM Mapping

```conf
# Splunk Common Information Model (CIM) Mapping
# props.conf for firewall logs

[firewall_auth]
SHOULD_LINEMERGE = false
TIME_FORMAT = %Y-%m-%d %H:%M:%S
MAX_TIMESTAMP_LOOKAHEAD = 25

# Field extractions
EXTRACT-src_ip = src_ip=(?<src_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
EXTRACT-dest_ip = dest_ip=(?<dest_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
EXTRACT-action = action=(?<action>\w+)

# CIM field aliases
FIELDALIAS-src = src_ip AS src
FIELDALIAS-dest = dest_ip AS dest
FIELDALIAS-dest_port = dport AS dest_port

# Lookups for action normalization
LOOKUP-action = firewall_action_lookup action OUTPUT action

# Calculated fields
EVAL-src = coalesce(src_ip, source_ip)
EVAL-dest = coalesce(dest_ip, destination_ip)
EVAL-user = coalesce(username, user_id)
EVAL-vendor_product = "Custom Firewall"
```

### ELK Logstash Pipeline

```ruby
# logstash.conf - Windows Security Event parsing
input {
  beats {
    port => 5044
  }
}

filter {
  if [type] == "wineventlog" {
    # Parse Windows Security events
    grok {
      match => { "message" => "%{GREEDYDATA:event_data}" }
    }

    # Map to ECS (Elastic Common Schema)
    mutate {
      rename => {
        "EventID" => "event.code"
        "SourceName" => "event.provider"
        "Computer" => "host.name"
      }
    }

    # Normalize authentication events
    if [event.code] in [4624, 4625] {
      mutate {
        add_field => { "event.category" => "authentication" }
      }

      if [event.code] == 4624 {
        mutate { add_field => { "event.outcome" => "success" } }
      } else {
        mutate { add_field => { "event.outcome" => "failure" } }
      }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "security-events-%{+YYYY.MM.dd}"
  }
}
```

---

## SIEM Correlation Rules

<a id="example-10"></a>

### Example 10: Brute Force Attack Detection

```spl
# Splunk: Failed logins followed by success (potential brute force)
index=security sourcetype=auth action=failure
| stats count as failures, latest(_time) as last_failure by src_ip, user
| where failures > 10
| join type=inner src_ip, user [
    search index=security sourcetype=auth action=success
    | stats count, earliest(_time) as first_success by src_ip, user
  ]
| where first_success > last_failure
| eval severity="high"
| eval description="Brute force attack detected: ".failures." failures before success"
| table _time, src_ip, user, failures, severity, description
```

<a id="example-11"></a>

### Example 11: Data Exfiltration Detection

```kql
# Azure Sentinel: Large file upload to external cloud storage
CommonSecurityLog
| where DeviceAction == "upload"
| where DestinationIP !startswith "10."
    and DestinationIP !startswith "172.16."
    and DestinationIP !startswith "192.168."
| summarize TotalBytes = sum(SentBytes) by SourceIP, DestinationIP, bin(TimeGenerated, 5m)
| where TotalBytes > 100000000  // 100 MB
| extend AlertSeverity = case(
    TotalBytes > 1000000000, "Critical",  // 1 GB
    TotalBytes > 500000000, "High",       // 500 MB
    "Medium"
)

# Alternative: DNS exfiltration detection
DnsEvents
| where QueryType == "TXT" or strlen(Name) > 100
| extend SubdomainLength = strlen(split(Name, ".")[0])
| where SubdomainLength > 50
| summarize Count = count() by ClientIP, bin(TimeGenerated, 1h)
| where Count > 100
```

<a id="example-12"></a>

### Example 12: Privilege Escalation Detection

```spl
# Splunk: User added to privileged groups
index=security sourcetype=wineventlog EventCode=4728 OR EventCode=4732 OR EventCode=4756
| eval group_name=mvindex(split(TargetUserName, ","), 0)
| where group_name IN ("Domain Admins", "Enterprise Admins", "Administrators", "Schema Admins")
| table _time, SubjectUserName, MemberSid, TargetUserName, group_name
| rename SubjectUserName as "Added By", TargetUserName as "Group", MemberSid as "New Member"

# Detect sudo abuse on Linux
index=linux sourcetype=syslog sudo
| rex "user=(?<user>\w+).*command=(?<command>.*)"
| where command LIKE "%chmod%777%" OR command LIKE "%passwd%" OR command LIKE "%adduser%"
| stats count by user, command, host
```

---

## Threat Hunting Queries

<a id="example-13"></a>

### Example 13: Sensitive File Share Access

```spl
# Splunk: SMB access to sensitive shares outside business hours
index=security sourcetype=wineventlog EventCode=5140
| eval share_path=lower(ShareName)
| where share_path="\\\\fileserver\\finance" OR share_path="\\\\fileserver\\hr"
    OR share_path="\\\\fileserver\\executive"
| eval hour=strftime(_time, "%H")
| where (hour < 8 OR hour > 18) AND tonumber(hour) != null
| stats count by src_ip, user, share_path, hour
| where count > 0
| eval risk="High - After hours access to sensitive share"
```

<a id="example-15"></a>

### Example 15: C2 Beaconing Detection

```python
#!/usr/bin/env python3
"""
C2 Beaconing Detection Script
Detects consistent connection intervals indicative of C2 communication.
"""

import pandas as pd
from scipy import stats
import numpy as np

def detect_beaconing(connection_log, cv_threshold=0.1, min_connections=10):
    """
    Detect potential C2 beaconing via statistical analysis.

    Args:
        connection_log: CSV file with columns [timestamp, src_ip, dest_ip, dest_port]
        cv_threshold: Coefficient of variation threshold (lower = more consistent)
        min_connections: Minimum connections to analyze

    Returns:
        DataFrame of suspected beaconing destinations
    """
    df = pd.read_csv(connection_log)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(['dest_ip', 'timestamp'])

    # Calculate intervals between connections
    df['interval'] = df.groupby('dest_ip')['timestamp'].diff().dt.total_seconds()

    results = []

    for dest_ip in df['dest_ip'].unique():
        ip_data = df[df['dest_ip'] == dest_ip]
        intervals = ip_data['interval'].dropna()

        if len(intervals) < min_connections:
            continue

        # Calculate coefficient of variation
        cv = stats.variation(intervals)
        mean_interval = intervals.mean()
        std_interval = intervals.std()

        if cv < cv_threshold:
            results.append({
                'dest_ip': dest_ip,
                'connection_count': len(intervals),
                'mean_interval_sec': mean_interval,
                'std_interval_sec': std_interval,
                'cv': cv,
                'risk': 'HIGH' if cv < 0.05 else 'MEDIUM'
            })
            print(f"[!] Potential beaconing to {dest_ip}")
            print(f"    Connections: {len(intervals)}, Mean interval: {mean_interval:.2f}s, CV: {cv:.4f}")

    return pd.DataFrame(results)

# Example usage
if __name__ == "__main__":
    suspects = detect_beaconing('network_connections.csv')
    suspects.to_csv('beaconing_suspects.csv', index=False)
```

### Rare Parent-Child Process Detection

```spl
# Splunk: Find rare parent-child process relationships
index=security sourcetype=sysmon EventCode=1
| stats count by ParentImage, Image
| where count < 5
| sort count
| head 100
| eval suspicion = case(
    Image LIKE "%cmd.exe%" AND ParentImage LIKE "%excel.exe%", "HIGH",
    Image LIKE "%powershell.exe%" AND ParentImage LIKE "%winword.exe%", "HIGH",
    Image LIKE "%wscript.exe%" AND ParentImage LIKE "%outlook.exe%", "HIGH",
    1=1, "LOW"
)
| where suspicion != "LOW"
```

---

## Forensics Procedures

<a id="example-16"></a>

### Example 16: Linux Memory Capture

```bash
#!/bin/bash
# Linux memory forensics script

# Using LiME (Linux Memory Extractor)
capture_memory_lime() {
    EVIDENCE_DIR="/mnt/evidence/$(hostname)_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$EVIDENCE_DIR"

    # Load LiME module
    sudo insmod /opt/forensics/lime-$(uname -r).ko \
        "path=$EVIDENCE_DIR/memory.lime format=lime"

    # Generate hash for integrity
    sha256sum "$EVIDENCE_DIR/memory.lime" > "$EVIDENCE_DIR/memory.lime.sha256"

    echo "Memory captured to $EVIDENCE_DIR/memory.lime"
}

# Analyze with Volatility 3
analyze_memory() {
    MEMORY_FILE=$1

    echo "=== Process List ==="
    vol3 -f "$MEMORY_FILE" linux.pslist

    echo "=== Network Connections ==="
    vol3 -f "$MEMORY_FILE" linux.netstat

    echo "=== Bash History ==="
    vol3 -f "$MEMORY_FILE" linux.bash

    echo "=== Suspicious Processes ==="
    vol3 -f "$MEMORY_FILE" linux.malfind
}
```

<a id="example-18"></a>

### Example 18: Forensically Sound Disk Imaging

```bash
#!/bin/bash
# Forensically sound disk imaging script

create_disk_image() {
    SOURCE_DEVICE=$1
    EVIDENCE_DIR=$2
    CASE_ID=$3

    # Verify write blocker (if hardware) or mount read-only
    mount -o ro,noexec "$SOURCE_DEVICE" /mnt/suspect 2>/dev/null || true

    # Create evidence directory
    mkdir -p "$EVIDENCE_DIR"

    # Capture device info
    hdparm -I "$SOURCE_DEVICE" > "$EVIDENCE_DIR/device_info.txt"
    fdisk -l "$SOURCE_DEVICE" >> "$EVIDENCE_DIR/device_info.txt"

    # Create bit-for-bit copy with dd
    echo "Starting disk imaging at $(date)"
    dd if="$SOURCE_DEVICE" of="$EVIDENCE_DIR/disk_${CASE_ID}.img" \
        bs=4M status=progress conv=noerror,sync 2>&1 | tee "$EVIDENCE_DIR/dd_log.txt"

    # Generate hashes
    echo "Generating hashes..."
    md5sum "$EVIDENCE_DIR/disk_${CASE_ID}.img" > "$EVIDENCE_DIR/disk.md5"
    sha256sum "$EVIDENCE_DIR/disk_${CASE_ID}.img" > "$EVIDENCE_DIR/disk.sha256"

    # Verify source hash matches
    md5sum "$SOURCE_DEVICE" >> "$EVIDENCE_DIR/source.md5"

    # Document chain of custody
    cat > "$EVIDENCE_DIR/chain_of_custody.txt" << EOF
Case ID: $CASE_ID
Source Device: $SOURCE_DEVICE
Image File: disk_${CASE_ID}.img
Acquired By: $(whoami)
Acquisition Date: $(date -Iseconds)
Acquisition Tool: dd (GNU coreutils)
MD5: $(cat $EVIDENCE_DIR/disk.md5 | cut -d' ' -f1)
SHA256: $(cat $EVIDENCE_DIR/disk.sha256 | cut -d' ' -f1)
EOF

    echo "Imaging complete. Evidence at $EVIDENCE_DIR"
}

# Usage: create_disk_image /dev/sdb /mnt/evidence INC-2025-001
```

<a id="example-19"></a>

### Example 19: Timeline Analysis

```bash
#!/bin/bash
# Filesystem timeline generation

generate_timeline() {
    DISK_IMAGE=$1
    OUTPUT_DIR=$2

    # Generate body file with fls (The Sleuth Kit)
    echo "Generating filesystem timeline..."
    fls -r -m / "$DISK_IMAGE" > "$OUTPUT_DIR/filesystem.body"

    # Convert to human-readable timeline
    mactime -b "$OUTPUT_DIR/filesystem.body" -d > "$OUTPUT_DIR/timeline.csv"

    # Find activity around incident date
    INCIDENT_DATE="2025-01-17"
    grep "$INCIDENT_DATE" "$OUTPUT_DIR/timeline.csv" > "$OUTPUT_DIR/incident_day.csv"

    # Look for suspicious activity
    echo "=== Suspicious files modified on incident day ==="
    grep -E "(bash|nc|wget|curl|\.php|\.ps1|\.exe)" "$OUTPUT_DIR/incident_day.csv"

    echo "=== Files with suspicious extensions ==="
    grep -E "\.(encrypted|locked|locky|cryptolocker)" "$OUTPUT_DIR/timeline.csv"
}

# Super timeline with log2timeline (Plaso)
generate_super_timeline() {
    DISK_IMAGE=$1
    OUTPUT_DIR=$2

    # Parse all artifact types
    log2timeline.py "$OUTPUT_DIR/plaso.dump" "$DISK_IMAGE"

    # Filter and output
    psort.py -w "$OUTPUT_DIR/supertimeline.csv" "$OUTPUT_DIR/plaso.dump"
}
```

<a id="example-20"></a>

### Example 20: Network Forensics - PCAP Analysis

```bash
#!/bin/bash
# Network forensics script

analyze_pcap() {
    PCAP_FILE=$1
    OUTPUT_DIR=$2

    mkdir -p "$OUTPUT_DIR"

    # Extract HTTP traffic
    echo "=== HTTP Requests ==="
    tshark -r "$PCAP_FILE" -Y "http.request" \
        -T fields -e frame.time -e ip.src -e http.host -e http.request.full_uri \
        > "$OUTPUT_DIR/http_requests.txt"

    # Find large file transfers
    echo "=== Large Transfers (>1MB) ==="
    tshark -r "$PCAP_FILE" -qz io,stat,0 2>&1 | head -20

    # Detect DNS tunneling
    echo "=== Potential DNS Tunneling ==="
    tshark -r "$PCAP_FILE" -Y "dns.qry.name" \
        -T fields -e dns.qry.name 2>/dev/null | \
        awk 'length > 50 {print}' > "$OUTPUT_DIR/dns_tunneling.txt"

    # Extract files from HTTP
    echo "=== Extracting HTTP Objects ==="
    tshark -r "$PCAP_FILE" --export-objects http,"$OUTPUT_DIR/http_objects"

    # Find C2 beaconing patterns
    echo "=== Potential Beaconing ==="
    tshark -r "$PCAP_FILE" -Y "tcp" \
        -T fields -e frame.time_relative -e ip.dst -e tcp.dstport | \
        sort | uniq -c | sort -rn | head -20 > "$OUTPUT_DIR/connection_frequency.txt"

    # Zeek analysis (if available)
    if command -v zeek &> /dev/null; then
        echo "=== Running Zeek Analysis ==="
        zeek -r "$PCAP_FILE" -C "$OUTPUT_DIR/zeek/"
    fi
}
```

---

## Security Metrics Scripts

<a id="example-21"></a>

### Example 21: MTTD Calculation

```python
#!/usr/bin/env python3
"""Security metrics calculation scripts."""

import pandas as pd
from datetime import datetime

def calculate_mttd(incidents_file):
    """Calculate Mean Time To Detect from incident data."""
    incidents = pd.read_csv(incidents_file)
    incidents['detection_time'] = pd.to_datetime(incidents['detection_time'])
    incidents['occurrence_time'] = pd.to_datetime(incidents['occurrence_time'])

    # Calculate time to detect in hours
    incidents['ttd_hours'] = (
        incidents['detection_time'] - incidents['occurrence_time']
    ).dt.total_seconds() / 3600

    # Overall MTTD
    mttd = incidents['ttd_hours'].mean()
    print(f"Overall MTTD: {mttd:.2f} hours")

    # MTTD by severity
    print("\nMTTD by Severity:")
    print(incidents.groupby('severity')['ttd_hours'].mean().round(2))

    # MTTD by incident type
    print("\nMTTD by Type:")
    print(incidents.groupby('type')['ttd_hours'].mean().round(2))

    return mttd

# Sample incidents.csv format:
# incident_id,occurrence_time,detection_time,containment_time,severity,type
# INC-001,2025-01-17 09:30,2025-01-17 10:20,2025-01-17 11:00,critical,ransomware
```

<a id="example-22"></a>

### Example 22: MTTR Calculation

```python
def calculate_mttr(incidents_file):
    """Calculate Mean Time To Respond (detection to containment)."""
    incidents = pd.read_csv(incidents_file)
    incidents['detection_time'] = pd.to_datetime(incidents['detection_time'])
    incidents['containment_time'] = pd.to_datetime(incidents['containment_time'])

    incidents['ttr_hours'] = (
        incidents['containment_time'] - incidents['detection_time']
    ).dt.total_seconds() / 3600

    mttr = incidents['ttr_hours'].mean()
    print(f"Overall MTTR: {mttr:.2f} hours")

    # Check against SLA
    sla_critical = 1  # 1 hour
    sla_high = 4      # 4 hours

    critical = incidents[incidents['severity'] == 'critical']
    critical_breaches = critical[critical['ttr_hours'] > sla_critical]
    print(f"\nCritical SLA breaches: {len(critical_breaches)}/{len(critical)}")

    return mttr
```

<a id="example-23"></a>

### Example 23: Incident Trend Analysis

```python
import matplotlib.pyplot as plt

def analyze_trends(incidents_file, output_dir):
    """Generate incident trend visualizations."""
    incidents = pd.read_csv(incidents_file)
    incidents['detection_time'] = pd.to_datetime(incidents['detection_time'])
    incidents['month'] = incidents['detection_time'].dt.to_period('M')

    # Monthly incident count by type
    trends = incidents.groupby(['month', 'type']).size().unstack(fill_value=0)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Trend over time
    trends.plot(kind='bar', stacked=True, ax=axes[0, 0])
    axes[0, 0].set_title('Incident Trends by Type')
    axes[0, 0].set_ylabel('Count')

    # Severity distribution
    incidents['severity'].value_counts().plot(kind='pie', ax=axes[0, 1], autopct='%1.1f%%')
    axes[0, 1].set_title('Incident Severity Distribution')

    # MTTD trend
    monthly_mttd = incidents.groupby('month')['ttd_hours'].mean()
    monthly_mttd.plot(ax=axes[1, 0], marker='o')
    axes[1, 0].set_title('MTTD Trend')
    axes[1, 0].set_ylabel('Hours')
    axes[1, 0].axhline(y=1, color='r', linestyle='--', label='Target (1hr)')
    axes[1, 0].legend()

    # Top attack vectors
    incidents['type'].value_counts().head(10).plot(kind='barh', ax=axes[1, 1])
    axes[1, 1].set_title('Top Incident Types')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/incident_trends.png', dpi=150)
    print(f"Charts saved to {output_dir}/incident_trends.png")
```

---

## NIST Control Implementation

<a id="example-26"></a>

### Example 26: IR-4 Incident Handling

```yaml
# IR-4: Incident Handling Implementation
ir_4_implementation:
  incident_handling_capability:
    automated_detection:
      - SIEM correlation rules (500+ active)
      - EDR behavioral analysis
      - DLP policy enforcement
      - Network anomaly detection (UEBA)
    manual_reporting:
      - Security hotline: 1-800-SEC-HELP
      - Email alias: security@company.com
      - Internal chat: #security-urgent
    tracking_system:
      - Platform: Jira Service Management
      - Ticket prefix: INC-
      - SLA tracking: Built-in

  incident_response_plan:
    documented: true
    last_reviewed: 2025-01-01
    review_frequency: annual
    testing:
      tabletop: quarterly
      functional: semi-annually
      full_scale: annually
    update_triggers:
      - After major incidents
      - Regulatory changes
      - Tool/process changes

  incident_categories:
    - malware_infection
    - phishing_attack
    - data_breach
    - ddos_attack
    - insider_threat
    - account_compromise
    - ransomware
    - supply_chain_attack

  coordination:
    internal:
      - IT Operations
      - Legal
      - Human Resources
      - Executive Leadership
      - Communications/PR
    external:
      - Law enforcement (FBI IC3)
      - Cyber insurance carrier
      - Forensic vendors (retainer)
      - Sector ISAC
```

<a id="example-27"></a>

### Example 27: IR-5 Incident Monitoring

```yaml
# IR-5: Incident Monitoring Implementation
ir_5_implementation:
  tracking_metrics:
    mttd:
      definition: "Time from occurrence to detection"
      target:
        critical: 15_minutes
        high: 1_hour
        medium: 4_hours
      reporting: weekly
    mttr:
      definition: "Time from detection to containment"
      target:
        critical: 1_hour
        high: 4_hours
        medium: 24_hours
      reporting: weekly
    false_positive_rate:
      target: less_than_10_percent
      review: weekly
    incidents_per_month:
      trend_analysis: true
      baseline: established

  reporting:
    soc_daily:
      content: [alert_count, incident_count, open_tickets]
      audience: SOC Team
    management_weekly:
      content: [metrics_summary, notable_incidents, trend_analysis]
      audience: IT Director, CISO
    executive_monthly:
      content: [risk_posture, major_incidents, improvement_initiatives]
      audience: C-Suite, Board
    regulatory:
      frequency: as_required
      types: [SEC_8K, GDPR, HIPAA, state_breach_notification]
```

<a id="example-28"></a>

### Example 28: IR-6 Incident Reporting

```yaml
# IR-6: Incident Reporting Implementation
ir_6_implementation:
  internal_reporting:
    soc_to_management:
      critical: within_15_minutes
      high: within_1_hour
      medium: next_business_day
    management_to_board:
      material_breach: within_24_hours
      quarterly_summary: board_meeting

  external_reporting:
    law_enforcement:
      triggers: [criminal_activity, nation_state_attack, significant_loss]
      contacts: [FBI_IC3, Secret_Service, local_PD]
    regulatory:
      GDPR:
        deadline: 72_hours
        authority: supervisory_authority
        threshold: any_breach_affecting_EU_residents
      HIPAA:
        deadline: 60_days
        authority: HHS_OCR
        threshold: 500_or_more_individuals
      SEC:
        deadline: 4_business_days
        form: 8-K
        threshold: material_cybersecurity_incident
      state_breach:
        varies_by_state: true
        common_threshold: 500_residents
    cyber_insurance:
      deadline: 24_to_48_hours
      contact: claims_adjuster
      documentation_required: true

  information_sharing:
    isac_participation:
      sector_isacs: [FS-ISAC, H-ISAC, IT-ISAC]
      sharing_level: TLP_AMBER
    threat_intel:
      platforms: [MISP, STIX/TAXII]
      contribution: anonymized_IOCs
```

<a id="example-29"></a>

### Example 29: SI-4 System Monitoring

```yaml
# SI-4: Information System Monitoring Implementation
si_4_implementation:
  monitoring_tools:
    siem: Splunk Enterprise Security
    ids_ips:
      network: Snort, Suricata
      host: OSSEC
    edr: CrowdStrike Falcon
    ndr: Zeek, Corelight
    full_packet_capture:
      tool: Moloch/Arkime
      retention: 90_days

  monitoring_coverage:
    network_perimeter:
      coverage: 100_percent
      tools: [firewall_logs, IDS, proxy]
    internal_segments:
      coverage: 95_percent
      segments: [DMZ, production, corporate, guest]
    endpoints:
      coverage: 98_percent
      types: [servers, workstations, laptops]
      gap: legacy_systems
    cloud_assets:
      coverage: 90_percent
      platforms: [AWS, Azure, GCP]

  alert_escalation:
    critical:
      method: phone_call
      target: on_call_analyst
      response_time: 15_minutes
    high:
      method: email_and_slack
      target: tier_2_queue
      response_time: 1_hour
    medium:
      method: ticket_creation
      target: tier_1_queue
      response_time: 4_hours
    low:
      method: log_only
      target: weekly_review
```

<a id="example-30"></a>

### Example 30: AU-6 Audit Review

```yaml
# AU-6: Audit Review, Analysis, and Reporting Implementation
au_6_implementation:
  log_review_frequency:
    real_time:
      method: SIEM_automated_correlation
      scope: all_high_fidelity_sources
    daily:
      method: SOC_analyst_review
      scope: high_fidelity_alerts, failed_authentications
    weekly:
      method: threat_hunting
      scope: trend_analysis, false_positive_tuning
    monthly:
      method: compliance_reporting
      scope: full_audit_log_review

  analysis_techniques:
    signature_based:
      tools: [IDS_signatures, AV_definitions, YARA_rules]
      update_frequency: daily
    anomaly_based:
      tools: [UEBA, statistical_analysis, ML_models]
      baseline_period: 30_days
    threat_intelligence:
      tools: [IOC_matching, TTP_correlation, MITRE_mapping]
      feeds: [MISP, OTX, commercial_intel]

  reporting:
    automated:
      daily_soc_metrics: email_to_soc_team
      weekly_threat_summary: dashboard_update
    manual:
      monthly_security_posture: executive_report
      quarterly_compliance: audit_committee
    ad_hoc:
      incident_reports: per_incident
      board_briefings: as_requested
```

---

## Additional Playbook Details

### Phishing Response - Detailed Steps

```yaml
phishing_playbook:
  trigger:
    - User reports suspicious email
    - Email gateway flags malicious attachment/link
    - EDR detects payload execution

  immediate_actions:
    timeline: 5_minutes
    steps:
      - Quarantine email from all mailboxes
      - Block sender domain at email gateway
      - Disable any accounts that clicked link

  analysis:
    timeline: 30_minutes
    steps:
      - Extract email headers (sender IP, path, SPF/DKIM/DMARC)
      - Submit attachments to sandbox (ANY.RUN, Hybrid Analysis)
      - Check web proxy for payload delivery attempts
      - Identify all recipients who received email
      - Check EDR for execution on any endpoints

  containment_commands:
    exchange_online: |
      # Find and delete phishing email
      $searchQuery = "Subject:'Urgent: Password Expiration' Received:01/17/2025"
      $complianceSearch = New-ComplianceSearch -Name "PhishHunt" -ExchangeLocation All -ContentMatchQuery $searchQuery
      Start-ComplianceSearch -Identity "PhishHunt"
      # After review, delete
      New-ComplianceSearchAction -SearchName "PhishHunt" -Purge -PurgeType SoftDelete

    on_prem_exchange: |
      Search-Mailbox -Identity * -SearchQuery 'Subject:"Urgent: Password Expiration"' -DeleteContent -Force

  eradication:
    - Remove malware from infected endpoints (EDR remediation)
    - Reset passwords for users who entered credentials
    - Revoke OAuth tokens if attacker gained access
    - Clear browser cached credentials

  recovery:
    - Restore any deleted/encrypted files from backup
    - Re-enable accounts after credential reset
    - Verify no persistence mechanisms remain

  post_incident:
    - Update phishing training with new examples
    - Add IOCs to threat intelligence platform
    - Tune email security rules to catch variants
    - Create SIEM alerts for similar patterns
```

### Ransomware Response - Detailed Steps

```yaml
ransomware_playbook:
  trigger:
    - EDR detects mass file encryption
    - User reports encrypted files with ransom note
    - File server alerts on unusual file activity

  immediate_actions:
    timeline: 5_minutes
    steps:
      - Disconnect infected system from network (pull cable/disable WiFi)
      - Identify ransomware variant from ransom note/extension
      - Preserve memory image before shutdown
      - Alert incident commander

  impact_assessment:
    timeline: 30_minutes
    questions:
      - How many systems are encrypted?
      - What data is affected (PII, financial, IP)?
      - Are backups intact and air-gapped?
      - What is the backup age (RPO)?
      - Is the ransomware still spreading?

  containment:
    - Isolate network segment containing infected systems
    - Block C2 domains/IPs at firewall
    - Disable shared drives if ransomware spreads via SMB
    - Create forensic images of infected systems

  eradication:
    critical_decision: DO_NOT_PAY_RANSOM (FBI/CISA guidance)
    steps:
      - Wipe infected systems completely
      - Remove ransomware from network shares
      - Scan all systems with updated signatures
      - Check for lateral movement/additional infections

  recovery:
    - Test backup integrity before restore
    - Restore systems from known-good backups
    - Rebuild from gold image if backup unavailable
    - Check No More Ransom project for decryption tools
    - Implement additional monitoring on recovered systems

  post_incident:
    - Review backup strategy (add offline/immutable backups)
    - Patch systems that allowed initial access
    - Implement application whitelisting
    - Add behavioral detection for file encryption patterns
    - Conduct employee awareness training on ransomware
```

---

## Additional Resources

- [NIST 800-61 Rev 2](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final) - Computer Security Incident Handling Guide
- [NIST 800-53 Rev 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final) - Security Controls
- [MITRE ATT&CK](https://attack.mitre.org) - Adversary Tactics and Techniques
- [SANS Incident Response](https://www.sans.org/blog/the-importance-of-incident-response-planning/) - IR Planning Guide

---

*This reference document complements the main SKILL.md. Return to [SKILL.md](./SKILL.md) for the core implementation guide.*
