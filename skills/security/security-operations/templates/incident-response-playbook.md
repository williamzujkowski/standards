# Incident Response Playbook

## Table of Contents

1. [Playbook 1: Phishing Response](#playbook-1-phishing-response)
2. [Playbook 2: Malware Outbreak](#playbook-2-malware-outbreak)
3. [Playbook 3: Data Breach](#playbook-3-data-breach)
4. [Playbook 4: DDoS Attack](#playbook-4-ddos-attack)
5. [Playbook 5: Insider Threat](#playbook-5-insider-threat)
6. [Communication Templates](#communication-templates)

---

## Playbook 1: Phishing Response

### Trigger

- User reports suspicious email via security@company.com
- Email security gateway flags malicious attachment/link
- EDR detects payload execution from email attachment

### Severity Assessment

- **Critical:** Credential compromise OR payload execution on critical systems
- **High:** Payload execution on standard endpoints
- **Medium:** Suspicious email with no execution confirmed
- **Low:** Obvious spam with no delivery

### Response Steps

#### Phase 1: Containment (Target: <5 minutes)

**1.1 Email Quarantine**

```powershell
# Exchange: Search and delete phishing email
$subject = "Urgent: Password Expiration"
Search-Mailbox -Identity * -SearchQuery "Subject:'$subject'" -DeleteContent -Confirm:$false

# Get count before deletion
$count = Search-Mailbox -Identity * -SearchQuery "Subject:'$subject'" -EstimateResultOnly
Write-Output "Emails found: $($count.ResultItemsCount)"
```

**1.2 Block Sender (NIST IR-4.a)**

```bash
# Postfix: Block sender domain
echo "example-phishing.com REJECT Phishing domain" >> /etc/postfix/sender_access
postmap /etc/postfix/sender_access
postfix reload
```

**1.3 Disable Compromised Accounts**

```powershell
# Azure AD: Revoke all sessions
Revoke-AzureADUserAllRefreshToken -ObjectId user@company.com
Set-AzureADUser -ObjectId user@company.com -AccountEnabled $false
```

#### Phase 2: Detection & Analysis (Target: <30 minutes)

**2.1 Email Header Analysis**

```bash
# Extract headers from .eml file
grep -E "(From|Reply-To|Return-Path|Received|X-Originating-IP)" phishing_email.eml

# Check SPF/DKIM/DMARC
grep -E "(spf=|dkim=|dmarc=)" phishing_email.eml
```

**2.2 Attachment Analysis (Sandbox)**

```bash
# Submit to VirusTotal
curl -X POST https://www.virustotal.com/api/v3/files \
  -H "x-apikey: $VT_API_KEY" \
  -F "file=@malicious_attachment.zip"

# Submit to ANY.RUN (interactive sandbox)
curl -X POST https://api.any.run/v1/analysis \
  -H "Authorization: Bearer $ANYRUN_API_KEY" \
  -F "file=@malicious_attachment.exe"
```

**2.3 Check for Payload Delivery (SIEM Query)**

```spl
# Splunk: Check if any users clicked link or executed attachment
index=security (sourcetype=proxy OR sourcetype=edr)
| eval indicator=coalesce(url, process_name)
| search indicator="*phishing-domain.com*" OR indicator="*malicious.exe"
| stats count by user, indicator, action
```

**2.4 IOC Extraction**

```yaml
# Document IOCs for threat intel
iocs:
  email_sender: phishing@malicious-domain.com
  sender_ip: 185.220.101.42
  malicious_url: http://phishing-domain.com/login.php
  attachment_hash: a5c2e5e7f8a9b1c3d4e5f6a7b8c9d0e1
  c2_domain: malware-c2.evil.com
  c2_ip: 192.0.2.100
```

#### Phase 3: Eradication (Target: <1 hour)

**3.1 Remove Malware (EDR)**

```bash
# CrowdStrike: Isolate and remediate host
falcon-cli contain -id HOST_ID
falcon-cli remediate -id DETECTION_ID -action kill_process
```

**3.2 Credential Reset**

```powershell
# Force password reset for affected users
$users = @("user1@company.com", "user2@company.com")
foreach ($user in $users) {
    Set-AzureADUserPassword -ObjectId $user -ForceChangePasswordNextSignIn $true
    Write-Output "Password reset enforced for $user"
}
```

#### Phase 4: Recovery (Target: <2 hours)

**4.1 Restore Files (if ransomware payload)**

```bash
# Restore from backup
veeam-cli restore -vm AFFECTED_VM -point BACKUP_TIMESTAMP
```

**4.2 Re-enable Accounts**

```powershell
# After credential reset
Set-AzureADUser -ObjectId user@company.com -AccountEnabled $true
```

#### Phase 5: Post-Incident (Within 24 hours)

**5.1 Update Threat Intelligence**

```bash
# Add IOCs to MISP
misp-cli add-attribute --event INCIDENT_ID --type domain --value phishing-domain.com
misp-cli add-attribute --event INCIDENT_ID --type ip-dst --value 185.220.101.42
```

**5.2 Email Security Tuning**

```yaml
# Update Proofpoint/Mimecast rules
email_security_rules:
  - rule: "Block sender domain pattern *-verify-account.com"
    action: quarantine
  - rule: "Flag emails with urgency keywords + external sender"
    keywords: ["urgent", "action required", "verify account"]
    action: banner_warning
```

**5.3 User Training**

- Send organization-wide phishing awareness email
- Schedule targeted training for affected users
- Update phishing simulation campaign

### Communication Templates

**Internal Notification (Critical Incidents)**

```
Subject: SECURITY INCIDENT - Phishing Campaign Detected

Team,

We are responding to an active phishing campaign targeting our organization.

What happened:
- Phishing emails with subject "Urgent: Password Expiration" delivered to ~50 employees
- 5 users clicked malicious link, credentials potentially compromised
- Affected accounts disabled, forced password reset initiated

Current status:
- Emails quarantined from all mailboxes
- Sender domain blocked at email gateway
- Investigation ongoing - expected resolution in 2 hours

Actions required:
- Do NOT click links in emails about password expiration
- Report suspicious emails to security@company.com
- Contact IT if you clicked the link in this email

Incident Commander: Jane Smith (jane.smith@company.com, x1234)
Next update: 2 hours
```

### NIST Control Mapping

- **IR-4 (Incident Handling):** Quarantine, block sender, disable accounts
- **IR-5 (Incident Monitoring):** SIEM queries, EDR alerts, email gateway logs
- **IR-6 (Incident Reporting):** Internal notification, management escalation
- **SI-4 (System Monitoring):** Email security gateway, EDR, proxy logs

---

## Playbook 2: Malware Outbreak

### Trigger

- EDR detects malicious process execution
- Antivirus quarantine alerts spike
- User reports ransomware note or system slowdown

### Severity Assessment

- **Critical:** Ransomware encrypting production systems OR wiper malware
- **High:** Malware with data exfiltration capability
- **Medium:** Commodity malware (Emotet, Qbot) contained to single host
- **Low:** Potentially unwanted program (PUP), no security impact

### Response Steps

#### Phase 1: Immediate Containment (<5 minutes)

**1.1 Network Isolation (NIST IR-4.a)**

```bash
# Linux: Drop all network traffic except to forensic server
sudo iptables -P INPUT DROP
sudo iptables -P OUTPUT DROP
sudo iptables -A OUTPUT -d 10.0.0.100 -j ACCEPT  # Forensic server
sudo iptables -A INPUT -s 10.0.0.100 -j ACCEPT

# Windows: Disable network adapter
Disable-NetAdapter -Name "Ethernet" -Confirm:$false
```

**1.2 Preserve Memory (Forensics)**

```bash
# Linux: Capture memory with LiME
sudo insmod lime-$(uname -r).ko "path=/mnt/evidence/memory-$(hostname)-$(date +%Y%m%d-%H%M%S).lime format=lime"

# Windows: Use Magnet RAM Capture
.\MagnetRAMCapture.exe -output C:\forensics\memory-$(hostname)-$(Get-Date -Format 'yyyyMMdd-HHmmss').dmp
```

**1.3 Identify Malware Variant**

```bash
# Check process tree
ps aux | grep -E "(suspicious|unusual)"
pstree -p

# Get file hash
sha256sum /path/to/suspicious_file

# Check VirusTotal
curl "https://www.virustotal.com/api/v3/files/$HASH" -H "x-apikey: $VT_API_KEY" | jq '.data.attributes.last_analysis_stats'
```

#### Phase 2: Scope Assessment (<30 minutes)

**2.1 SIEM Query - Find Other Infected Hosts**

```spl
# Splunk: Search for malware hash across all endpoints
index=edr sourcetype=sysmon EventCode=1
| eval file_hash=coalesce(Hashes, hash_sha256)
| search file_hash="a5c2e5e7f8a9b1c3d4e5f6a7b8c9d0e1"
| stats count by host, user, file_path
```

**2.2 Network IOC Search**

```spl
# Splunk: C2 communication detection
index=network sourcetype=firewall OR sourcetype=proxy
| search dest_ip IN ("192.0.2.100", "192.0.2.101") OR dest_domain="*.evil.com"
| stats count by src_ip, dest_ip, dest_port
```

**2.3 Timeline Analysis**

```bash
# Malware first seen timestamp
earliest_detection=$(grep -r "malware.exe" /var/log/syslog | head -1 | awk '{print $1" "$2" "$3}')
echo "First detection: $earliest_detection"

# Build timeline from forensic image
fls -r -m / /dev/sda1 > timeline.body
mactime -b timeline.body -d > timeline.csv
grep "$earliest_detection" timeline.csv
```

#### Phase 3: Eradication (<2 hours)

**3.1 Remove Malware & Persistence**

```bash
# Linux: Remove malware and persistence mechanisms
sudo systemctl stop malicious-service
sudo systemctl disable malicious-service
sudo rm -f /etc/systemd/system/malicious.service
sudo crontab -l | grep -v "malware" | sudo crontab -
sudo rm -f /usr/local/bin/malware.sh

# Windows: Remove scheduled tasks and registry keys
Get-ScheduledTask | Where-Object {$_.TaskPath -like "*malware*"} | Unregister-ScheduledTask -Confirm:$false
Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "MalwareStartup"
```

**3.2 Credential Rotation**

```powershell
# Assume all credentials on infected host compromised
$hostname = "INFECTED-HOST"
Get-ADComputer -Identity $hostname | Get-ADComputerServiceAccount | ForEach-Object {
    Set-ADServiceAccount $_.SamAccountName -Credential (Get-Credential)
    Write-Output "Rotated credential for $($_.SamAccountName)"
}
```

#### Phase 4: Recovery (<4 hours)

**4.1 System Rebuild (Gold Image)**

```bash
# Deploy fresh OS image via PXE boot
cobbler system edit --name=infected-host --netboot-enabled=1
cobbler sync
# Reboot host for network boot
ipmitool -I lanplus -H $IPMI_IP -U $USER -P $PASS power cycle
```

**4.2 Restore Data from Backup**

```bash
# Verify backup integrity before restore
sha256sum /backup/data.tar.gz
# Compare with known-good hash from before infection

# Restore
tar -xzf /backup/data.tar.gz -C /mnt/restored
```

**4.3 Enhanced Monitoring**

```yaml
# Deploy additional EDR sensors
edr_config:
  host: infected-host-restored
  monitoring_level: maximum
  behavioral_analysis: enabled
  network_capture: enabled
  retention_days: 180
```

#### Phase 5: Post-Incident (<1 week)

**5.1 Malware Analysis Report**

```markdown
# Malware Analysis - Incident INC-2025-001

## Executive Summary
- **Malware Family:** Emotet
- **Infection Vector:** Phishing email with malicious macro
- **Capability:** Credential theft, lateral movement, ransomware dropper
- **Systems Affected:** 3 Windows workstations
- **Data Impact:** No confirmed data loss

## Technical Details
- **File Hash (SHA256):** a5c2e5e7f8a9b1c3d4e5f6a7b8c9d0e1
- **C2 Domains:** evil[.]com, backup-c2[.]net
- **Persistence:** Registry Run key, scheduled task
- **Lateral Movement:** SMB with stolen credentials

## Recommendations
1. Implement application whitelisting (AppLocker/AppArmor)
2. Disable Office macros by default
3. Network segmentation to limit lateral movement
4. Enhanced EDR coverage on critical assets
```

**5.2 Lessons Learned**

See template: `post-incident-report.md`

### NIST Control Mapping

- **IR-4.a (Incident Handling - Preparation):** EDR deployment, forensic tools
- **IR-4.c (Incident Handling - Containment):** Network isolation, process termination
- **SI-4 (System Monitoring):** EDR alerts, SIEM correlation
- **CM-3 (Configuration Management):** Gold image rebuild

---

## Playbook 3: Data Breach

### Trigger

- SIEM alerts on large data download/upload
- External notification (security researcher, customer complaint)
- Database audit log shows unauthorized access

### Severity Assessment

- **Critical:** PII/PHI of >10,000 individuals OR financial data
- **High:** Confidential IP, customer data (<10,000 records)
- **Medium:** Internal documents, non-sensitive data
- **Low:** Publicly available data accessed by unauthorized party

### Response Steps

#### Phase 1: Containment (<15 minutes)

**1.1 Revoke Access Credentials (NIST IR-4.c)**

```bash
# Revoke API key
aws iam delete-access-key --access-key-id AKIAIOSFODNN7EXAMPLE --user-name compromised-user

# Revoke database user
mysql -e "REVOKE ALL PRIVILEGES ON database.* FROM 'compromised_user'@'%'; FLUSH PRIVILEGES;"
```

**1.2 Block Attacker IP**

```bash
# Firewall rule
sudo iptables -A INPUT -s 203.0.113.42 -j DROP
sudo iptables -A OUTPUT -d 203.0.113.42 -j DROP

# AWS Security Group
aws ec2 revoke-security-group-ingress --group-id sg-12345678 --protocol tcp --port 443 --cidr 203.0.113.42/32
```

**1.3 Enable Enhanced Logging**

```bash
# MySQL: Enable query audit log
SET GLOBAL general_log = 'ON';
SET GLOBAL log_output = 'FILE';

# PostgreSQL: Enable audit extension
ALTER SYSTEM SET pgaudit.log = 'all';
SELECT pg_reload_conf();
```

#### Phase 2: Scope Determination (<4 hours)

**2.1 Query Database Audit Logs**

```sql
-- PostgreSQL: Find unauthorized queries
SELECT
    event_time,
    user_name,
    client_addr,
    command_tag,
    substring(query, 1, 100) AS query_preview
FROM pg_audit_log
WHERE event_time BETWEEN '2025-01-17 08:00:00' AND '2025-01-17 12:00:00'
    AND user_name = 'compromised_user'
    AND command_tag IN ('SELECT', 'COPY')
ORDER BY event_time;

-- Count affected records
SELECT COUNT(*) FROM customers WHERE last_accessed BETWEEN '2025-01-17 08:00:00' AND '2025-01-17 12:00:00';
```

**2.2 Network Traffic Analysis**

```bash
# Extract large uploads from PCAP
tshark -r capture.pcap -Y "http.request.method==POST && frame.len>10000" \
    -T fields -e frame.time -e ip.src -e http.request.uri -e frame.len

# Calculate total data exfiltrated
tshark -r capture.pcap -Y "ip.dst==203.0.113.42" -z io,stat,1,"SUM(frame.len)frame.len"
```

**2.3 Affected Data Classification**

```yaml
breach_scope:
  records_accessed: 15,342
  data_types:
    - full_name
    - email_address
    - phone_number
    - date_of_birth
    - social_security_number: 1,203 records
  regulatory_impact:
    - GDPR: 8,500 EU residents
    - CCPA: 4,100 California residents
    - HIPAA: 0 PHI records
```

#### Phase 3: Legal & Regulatory Notification (<72 hours)

**3.1 Internal Escalation**

```
TO: Legal Counsel, CISO, CEO
SUBJECT: DATA BREACH - IMMEDIATE ATTENTION REQUIRED

A data breach has been confirmed:
- Date/Time: 2025-01-17 08:00 - 12:00 UTC
- Records Affected: 15,342 customer records
- Data Types: Names, emails, phones, DOB, SSN (1,203)
- Attacker: External, IP 203.0.113.42
- Access Method: Compromised API key

Regulatory obligations:
- GDPR: 72-hour notification to supervisory authority (deadline: 2025-01-20 12:00 UTC)
- CCPA: Notify California AG (4,100 residents affected)
- State laws: 47 states require notification

Next steps:
1. Legal review of notification language
2. Engage forensic firm for investigation
3. Notify cyber insurance carrier
4. Prepare customer communication

Incident Commander: [Name], [Contact]
```

**3.2 Regulatory Notification Templates**

See section: [Communication Templates](#communication-templates)

#### Phase 4: Remediation (<1 week)

**4.1 Fix Vulnerability**

```python
# Example: Add rate limiting to API
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/customers')
@limiter.limit("100 per hour")
def get_customers():
    # API logic
    pass
```

**4.2 Implement Additional Controls**

```yaml
# New security controls
controls_implemented:
  - data_loss_prevention:
      tool: "Microsoft Purview DLP"
      rules: ["Block large customer data exports", "Alert on sensitive data downloads"]
  - database_activity_monitoring:
      tool: "Imperva DAM"
      alerts: ["Unusual query patterns", "Access outside business hours"]
  - api_security:
      tool: "API Gateway with rate limiting"
      limits: "100 requests/hour per API key"
```

#### Phase 5: Customer Notification (<30 days)

**5.1 Notification Letter (Legal Review Required)**

See: [Communication Templates - Data Breach Notification](#data-breach-notification)

**5.2 Credit Monitoring Offer**

```yaml
credit_monitoring:
  provider: "Experian IdentityWorks"
  duration: 12 months
  services:
    - credit_monitoring: 3 bureaus
    - identity_theft_insurance: $1M coverage
    - fraud_resolution_support: 24/7 hotline
  enrollment: https://company.id protection.com
  enrollment_deadline: 90 days from notification
```

### NIST Control Mapping

- **IR-4.c (Incident Handling - Containment):** Revoke credentials, block IPs
- **IR-6.b (Incident Reporting - External):** Regulatory notification
- **AU-6 (Audit Review):** Database audit log analysis
- **SI-4 (System Monitoring):** DLP, database activity monitoring

---

## Playbook 4: DDoS Attack

### Trigger

- Network monitoring alerts on traffic spike
- Application performance degradation
- ISP notification of inbound DDoS

### Severity Assessment

- **Critical:** Multi-vector attack >100 Gbps, business-critical service offline
- **High:** Single-vector attack 10-100 Gbps, degraded performance
- **Medium:** <10 Gbps, intermittent service issues
- **Low:** Attack mitigated by existing defenses, no user impact

### Response Steps

#### Phase 1: Detection & Analysis (<15 minutes)

**1.1 Confirm DDoS (Not Legitimate Traffic Spike)**

```bash
# Check connection counts by IP
netstat -an | grep :80 | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr | head -20

# Top talkers analysis
tcpdump -i eth0 -nn -c 10000 | awk '{print $3}' | cut -d. -f1-4 | sort | uniq -c | sort -nr | head
```

**1.2 Identify Attack Vector**

```yaml
# Common DDoS attack types
attack_vectors:
  volumetric:
    - UDP flood: High packet rate, random source IPs
    - ICMP flood: Ping flood from botnet
    - DNS amplification: Small queries, large responses

  protocol:
    - SYN flood: Half-open TCP connections
    - ACK flood: TCP ACK packets to random ports

  application:
    - HTTP flood: Legitimate-looking HTTP GET/POST requests
    - Slowloris: Slow HTTP requests keeping connections open
```

**1.3 Measure Attack Size**

```bash
# Bandwidth utilization
iftop -i eth0 -n -P -t -s 10

# Packets per second
sar -n DEV 1 10 | grep eth0
```

#### Phase 2: Mitigation (<30 minutes)

**2.1 Enable DDoS Mitigation Service**

```bash
# Cloudflare: Enable "I'm Under Attack" mode
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/security_level" \
    -H "Authorization: Bearer $CF_API_TOKEN" \
    -d '{"value":"under_attack"}'

# AWS Shield Advanced: Emergency contact
aws shield describe-attack --attack-id $ATTACK_ID
```

**2.2 Rate Limiting (Application Layer)**

```nginx
# Nginx: Rate limiting config
http {
    limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;

    server {
        location / {
            limit_req zone=one burst=20 nodelay;
            proxy_pass http://backend;
        }
    }
}
```

**2.3 Geo-Blocking (If Attack from Specific Country)**

```bash
# iptables: Block traffic from country (using IP range)
curl http://www.ipdeny.com/ipblocks/data/countries/cn.zone -o /tmp/cn.zone
for ip in $(cat /tmp/cn.zone); do
    iptables -A INPUT -s $ip -j DROP
done
```

**2.4 ISP Blackhole/Scrubbing**

```
# Contact ISP NOC
Phone: 1-800-ISP-NOC-1
Email: noc@isp.com

Request:
- Blackhole routing for attack traffic (null route)
- OR scrubbing center redirect (clean traffic forwarding)
- Provide: Target IP, attack type, approximate volume
```

#### Phase 3: Monitoring & Adjustment (<2 hours)

**3.1 Traffic Analysis**

```bash
# Real-time traffic dashboard
watch -n 5 'netstat -an | grep :80 | wc -l; sar -n DEV 1 1 | grep eth0'

# Application response time
curl -o /dev/null -s -w "Time: %{time_total}s\n" https://company.com
```

**3.2 Adjust Mitigation**

```bash
# Tighten rate limits if attack persists
# Lower burst threshold
limit_req zone=one burst=5 nodelay;
```

#### Phase 4: Post-Attack Analysis

**4.1 Attack Attribution**

```bash
# Extract attacker IPs from logs
zcat /var/log/nginx/access.log.*.gz | awk '{print $1}' | sort | uniq -c | sort -nr | head -100 > attacker_ips.txt

# Check IP reputation
for ip in $(head -20 attacker_ips.txt | awk '{print $2}'); do
    curl -s "https://www.abuseipdb.com/check/$ip/json?key=$ABUSE_IPDB_KEY" | jq .
done
```

**4.2 Infrastructure Improvements**

```yaml
# DDoS resilience recommendations
improvements:
  - cdn: "Deploy Cloudflare/Akamai for L7 protection"
  - anycast: "Use anycast IP to distribute attack load"
  - auto_scaling: "AWS Auto Scaling to handle traffic spikes"
  - rate_limiting: "API Gateway with per-IP limits"
  - monitoring: "NetFlow analysis for early detection"
```

### NIST Control Mapping

- **IR-4 (Incident Handling):** DDoS mitigation activation, traffic filtering
- **SI-4 (System Monitoring):** Network traffic analysis, bandwidth monitoring
- **SC-5 (Denial of Service Protection):** Rate limiting, CDN, auto-scaling

---

## Playbook 5: Insider Threat

### Trigger

- DLP alert on large data transfer to personal cloud storage
- UEBA anomaly: User accessing unusual systems/data
- Manager reports suspicious employee behavior
- Exit interview: Departing employee with access to sensitive data

### Severity Assessment

- **Critical:** Active data exfiltration OR sabotage (deleted databases, malware deployment)
- **High:** Unauthorized access to trade secrets, customer data
- **Medium:** Policy violation (personal use of company resources)
- **Low:** Accidental data exposure (no malicious intent)

### Response Steps

#### Phase 1: Covert Investigation (<24 hours)

**IMPORTANT:** Do NOT alert the subject during investigation

**1.1 Preserve Evidence**

```bash
# IT: Create forensic copy of user's workstation (after hours)
sudo dd if=/dev/sda of=/mnt/evidence/insider-$(date +%Y%m%d).img bs=4M status=progress
sha256sum /mnt/evidence/insider-$(date +%Y%m%d).img > /mnt/evidence/insider-$(date +%Y%m%d).img.sha256
```

**1.2 Review User Activity (SIEM)**

```spl
# Splunk: User activity timeline
index=security user="insider@company.com"
| eval hour=strftime(_time, "%Y-%m-%d %H:00")
| stats count by hour, sourcetype, action
| sort hour
```

**1.3 Check Cloud Storage Uploads (DLP Logs)**

```spl
# Splunk: Data exfiltration to personal cloud
index=dlp user="insider@company.com" action=upload
| eval dest_domain=coalesce(destination_domain, url_domain)
| search dest_domain IN ("dropbox.com", "drive.google.com", "onedrive.live.com")
| stats sum(bytes) as total_bytes, count by dest_domain
```

**1.4 Database Access Audit**

```sql
-- PostgreSQL: Check what data user accessed
SELECT
    event_time,
    database_name,
    command_tag,
    object_name,
    substring(query, 1, 200) AS query_preview
FROM pg_audit_log
WHERE user_name = 'insider'
    AND event_time > NOW() - INTERVAL '30 days'
    AND (object_name LIKE '%customer%' OR object_name LIKE '%confidential%')
ORDER BY event_time DESC;
```

#### Phase 2: Coordinated Response (<1 hour)

**Coordinate with:** HR, Legal, Management, Physical Security

**2.1 Account Suspension (No Warning)**

```bash
# Disable all access immediately
# Active Directory
Disable-ADAccount -Identity insider

# VPN
sudo ./vpn-revoke.sh insider@company.com

# Badge access
curl -X POST https://badgesystem.company.com/api/revoke \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"employee_id":"12345"}'
```

**2.2 Escorted Exit (If On-Site)**

- Physical Security escorts employee from building
- Collect company assets (laptop, phone, badge)
- No access to personal workstation during exit

**2.3 Forensic Collection**

```bash
# Collect all user data
# Email
/opt/exchange/export-mailbox.sh insider@company.com > /evidence/email-export.pst

# File shares
rsync -av --log-file=/evidence/rsync.log /shares/users/insider/ /evidence/file-shares/

# Browser history (from forensic image)
sqlite3 /evidence/forensic-image/Users/insider/AppData/Local/Google/Chrome/History \
    "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC;"
```

#### Phase 3: Investigation & Legal Action (<1 week)

**3.1 Forensic Analysis**

```bash
# Search for keywords in files
grep -r -i -E "(confidential|secret|customer list)" /evidence/file-shares/ > keywords.txt

# Check USB device history (Windows Registry)
grep "USBSTOR" /evidence/forensic-image/Windows/System32/config/SYSTEM
```

**3.2 Document Timeline**

```markdown
# Insider Threat Timeline - Employee ID 12345

| Date/Time | Event | Source |
|-----------|-------|--------|
| 2025-01-10 14:30 | Submitted resignation | HR System |
| 2025-01-12 09:15 | Accessed customer database (unusual) | Database audit log |
| 2025-01-12 10:00 | Downloaded 500 customer records to CSV | DLP alert |
| 2025-01-12 10:30 | Uploaded files to personal Dropbox | DLP alert, proxy logs |
| 2025-01-12 16:00 | Accessed competitor job posting site | Proxy logs |
| 2025-01-13 08:00 | Account disabled by security team | AD logs |
| 2025-01-13 09:00 | Escorted exit from building | Physical security |
```

**3.3 Legal Consultation**

- Consult legal counsel on:
  - Civil action (injunction, damages)
  - Criminal referral (Computer Fraud and Abuse Act, trade secret theft)
  - Notification obligations (if PII exfiltrated)

#### Phase 4: Prevention (Ongoing)

**4.1 Enhanced Monitoring for At-Risk Employees**

```yaml
# UEBA policy for departing employees
ueba_policies:
  - trigger: "Resignation submitted"
    actions:
      - increase_logging: true
      - alert_threshold: "50% of normal activity"
      - restrict_access: ["confidential file shares", "database export functions"]
      - retention: "1 year post-departure"
```

**4.2 Offboarding Checklist**

```markdown
# Employee Offboarding - Security Checklist

- [ ] Disable accounts on resignation date (not last day)
- [ ] Revoke VPN, email, SSO access
- [ ] Remove from all security groups
- [ ] Collect company assets (laptop, phone, badge)
- [ ] Conduct exit interview (remind of confidentiality obligations)
- [ ] Review final 30 days of activity for anomalies
- [ ] Archive user data for 1 year
```

### NIST Control Mapping

- **IR-4 (Incident Handling):** Covert investigation, coordinated response
- **PS-4 (Personnel Termination):** Offboarding checklist, access revocation
- **AU-6 (Audit Review):** User activity monitoring, forensic analysis
- **SI-4 (System Monitoring):** DLP, UEBA, database audit logs

---

## Communication Templates

### Internal Notification (Critical Incidents)

```
TO: Executive Leadership, IT Operations, Legal
FROM: Security Operations Center
SUBJECT: SECURITY INCIDENT - [Type] - Severity [Critical/High]

SUMMARY
[1-2 sentence description of incident]

DETAILS
- Incident ID: INC-2025-XXX
- Detection Time: [YYYY-MM-DD HH:MM UTC]
- Incident Type: [Phishing / Malware / Data Breach / DDoS / Insider Threat]
- Severity: [Critical / High / Medium / Low]
- Systems Affected: [List of systems/users]

CURRENT STATUS
- Containment: [Complete / In Progress / Not Started]
- Investigation: [Complete / In Progress / Not Started]
- Recovery: [Complete / In Progress / Not Started]

IMPACT
- Business Operations: [Disrupted / Degraded / No Impact]
- Data: [Compromised / At Risk / Secure]
- Customer Impact: [Yes / No / Unknown]

ACTIONS TAKEN
1. [Action 1]
2. [Action 2]
3. [Action 3]

NEXT STEPS
1. [Next step 1]
2. [Next step 2]

INCIDENT COMMANDER
[Name], [Title]
[Email], [Phone]

NEXT UPDATE
[Time] or upon significant development
```

### Data Breach Notification (Customer-Facing)

**IMPORTANT:** Legal review required before sending

```
Subject: Important Security Notice - [Company Name]

Dear [Customer Name],

We are writing to inform you of a data security incident that may have affected your personal information.

WHAT HAPPENED
On [Date], we discovered that an unauthorized party gained access to our systems and accessed customer data. We immediately launched an investigation and engaged a leading cybersecurity firm to assist.

WHAT INFORMATION WAS AFFECTED
The accessed data may have included:
- Name
- Email address
- Phone number
- [Other data types - be specific]

Based on our investigation, the following information was NOT accessed:
- Credit card numbers
- Social Security numbers
- Financial account information

WHAT WE ARE DOING
- We have fixed the security vulnerability
- We have reported this incident to law enforcement
- We are implementing additional security measures to prevent future incidents
- We are offering you [12 months] of free credit monitoring and identity theft protection

WHAT YOU CAN DO
1. Enroll in credit monitoring: [Link] (enrollment code: [CODE])
2. Monitor your accounts for suspicious activity
3. Consider placing a fraud alert with credit bureaus
4. Change your password if you reused it on other sites

We take the security of your information very seriously and deeply regret this incident.

For questions, contact our dedicated hotline:
Phone: 1-800-XXX-XXXX (Mon-Fri 8AM-8PM ET)
Email: dataincident@company.com
Web: https://company.com/security-incident

Sincerely,
[Name], [Title]
[Company Name]

---
Additional Resources:
- Federal Trade Commission (Identity Theft): https://www.identitytheft.gov
- Credit Bureau Contact Information:
  * Equifax: 1-800-525-6285, https://www.equifax.com
  * Experian: 1-888-397-3742, https://www.experian.com
  * TransUnion: 1-800-680-7289, https://www.transunion.com
```

### Regulatory Notification (GDPR Example)

```
TO: [Supervisory Authority - e.g., ICO, CNIL]
FROM: [Company Data Protection Officer]
SUBJECT: Personal Data Breach Notification - [Company Name]

In accordance with Article 33 of the GDPR, we are notifying you of a personal data breach.

CONTROLLER DETAILS
Company Name: [Company Name]
Registration Number: [Number]
Address: [Address]
DPO Contact: [Name], [Email], [Phone]

BREACH DETAILS
Date/Time of Breach: [YYYY-MM-DD HH:MM UTC]
Date/Time of Discovery: [YYYY-MM-DD HH:MM UTC]
Nature of Breach: [Unauthorized access / Data loss / Other]

DATA SUBJECTS AFFECTED
Number of Data Subjects: [Number]
Categories: [Customers / Employees / Other]
Geographical Location: [Countries]

PERSONAL DATA CATEGORIES
- [Category 1 - e.g., Names]
- [Category 2 - e.g., Email addresses]
- [Special categories - if applicable]

LIKELY CONSEQUENCES
[Description of potential impact on data subjects]

MEASURES TAKEN
- Immediate: [Containment actions]
- Long-term: [Prevention measures]

NOTIFICATION TO DATA SUBJECTS
[Completed / In Progress / Not Required]
Justification: [If not completed]

CONTACT
[DPO Name]
[Email]
[Phone]

Attachments:
- Incident report
- Forensic analysis summary
```

---

## Appendix: Quick Reference

### Incident Severity Matrix

| Factor | Critical | High | Medium | Low |
|--------|----------|------|--------|-----|
| **Business Impact** | Critical system down | Important system degraded | Minor system affected | No business impact |
| **Data** | PII/PHI breach >10K | PII breach <10K | Internal data only | No data exposure |
| **Scope** | Multiple systems | Several systems | Single system | Isolated event |
| **Active Threat** | Yes, ongoing | Yes, contained | No, remnants | No threat |

### Response Time Targets (NIST IR-4)

| Severity | Detection → Analysis | Analysis → Containment | Containment → Recovery |
|----------|---------------------|------------------------|------------------------|
| **Critical** | <15 min | <15 min | <4 hours |
| **High** | <1 hour | <1 hour | <24 hours |
| **Medium** | <4 hours | <4 hours | <3 days |
| **Low** | <24 hours | <24 hours | <1 week |

### Evidence Collection Priority

1. **Volatile (collect first):**
   - Memory (RAM)
   - Network connections
   - Running processes

2. **Semi-Volatile:**
   - Logs (syslog, event logs)
   - Temporary files
   - Swap/page files

3. **Non-Volatile:**
   - Disk images
   - Configuration files
   - Backup data

### Chain of Custody Template

```
EVIDENCE ITEM: [Description]
ITEM NUMBER: [Unique ID]
INCIDENT: INC-2025-XXX

COLLECTION
Collected by: [Name, Title]
Date/Time: [YYYY-MM-DD HH:MM UTC]
Location: [Physical/Network location]
Method: [Tool/command used]
Hash (SHA256): [Hash value]

TRANSFER LOG
| Date/Time | From | To | Purpose | Signature |
|-----------|------|----|---------| ---------|
|           |      |    |         |          |
```

---

*Last Updated: 2025-01-17*
*Version: 1.0.0*
*Based on: NIST 800-61 Rev 2, ISO 27035*
