# SIEM Query Library

Production-ready queries for Splunk SPL, ELK KQL, and Azure Sentinel KQL, organized by MITRE ATT&CK tactics.

## Table of Contents

1. [Initial Access (TA0001)](#initial-access-ta0001)
2. [Execution (TA0002)](#execution-ta0002)
3. [Persistence (TA0003)](#persistence-ta0003)
4. [Privilege Escalation (TA0004)](#privilege-escalation-ta0004)
5. [Defense Evasion (TA0005)](#defense-evasion-ta0005)
6. [Credential Access (TA0006)](#credential-access-ta0006)
7. [Discovery (TA0007)](#discovery-ta0007)
8. [Lateral Movement (TA0008)](#lateral-movement-ta0008)
9. [Collection (TA0009)](#collection-ta0009)
10. [Exfiltration (TA0010)](#exfiltration-ta0010)
11. [Command and Control (TA0011)](#command-and-control-ta0011)

---

## Initial Access (TA0001)

### Phishing - Suspicious Email Attachments

**Splunk SPL:**
```spl
index=email sourcetype=exchange
| eval attachment_ext=lower(mvindex(split(attachment_name, "."), -1))
| where attachment_ext IN ("exe", "scr", "bat", "cmd", "ps1", "vbs", "js", "jar", "zip")
| stats count by sender, recipient, subject, attachment_name, attachment_ext
| where count > 0
```

**ELK KQL:**
```kql
event.module: "o365" AND event.category: "email" AND
file.extension: (exe OR scr OR bat OR cmd OR ps1 OR vbs OR js OR jar OR zip)
```

**Azure Sentinel KQL:**
```kql
EmailAttachmentInfo
| where FileType in ("exe", "scr", "bat", "cmd", "ps1", "vbs", "js")
| join kind=inner (EmailEvents) on NetworkMessageId
| project Timestamp, SenderFromAddress, RecipientEmailAddress, Subject, FileName, FileType
```

### Brute Force - Failed Login Attempts

**Splunk SPL:**
```spl
index=security sourcetype=auth action=failure
| stats count as failures, values(src_ip) as source_ips by user
| where failures > 10
| join type=left user [
    search index=security sourcetype=auth action=success
    | stats count as successes, latest(_time) as success_time by user
  ]
| eval status=if(isnull(successes), "Failed only", "Succeeded after failures")
| table user, failures, successes, status, source_ips
```

**ELK KQL:**
```kql
event.category: "authentication" AND event.outcome: "failure"
| count BY user.name, source.ip
| WHERE count > 10
```

**Azure Sentinel KQL:**
```kql
SigninLogs
| where ResultType != 0  // 0 = success
| summarize FailureCount=count(), IPs=make_set(IPAddress) by UserPrincipalName
| where FailureCount > 10
| join kind=inner (
    SigninLogs
    | where ResultType == 0
    | summarize SuccessCount=count() by UserPrincipalName
  ) on UserPrincipalName
| project UserPrincipalName, FailureCount, SuccessCount, IPs
```

### Exploit Public-Facing Application

**Splunk SPL:**
```spl
index=web sourcetype=access_combined
| eval http_status=status
| where (http_status >= 400 AND http_status < 500) OR http_status == 500
| eval suspicious_pattern=if(match(uri, "(?i)(union|select|insert|drop|delete|exec|script|alert|onerror|javascript)"), 1, 0)
| where suspicious_pattern=1
| stats count by src_ip, uri, http_status
| where count > 5
| sort -count
```

**ELK KQL:**
```kql
http.response.status_code >= 400 AND
url.original: (*union* OR *select* OR *exec* OR *script* OR *alert*)
```

**Azure Sentinel KQL:**
```kql
W3CIISLog
| where scStatus >= 400
| where csUriQuery has_any ("union", "select", "exec", "script", "alert", "onload", "onerror")
| summarize Count=count() by cIP, csUriQuery, scStatus
| where Count > 5
```

---

## Execution (TA0002)

### PowerShell - Suspicious Command Execution

**Splunk SPL:**
```spl
index=edr sourcetype=sysmon EventCode=1
| eval process_lower=lower(CommandLine)
| where (match(process_lower, "(?i)(encodedcommand|invoke-expression|downloadstring|iex|webclient)"))
    OR (match(process_lower, "(?i)(bypass|noprofile|noninteractive)") AND match(process_lower, "(?i)(invoke|iex)"))
| table _time, host, user, ParentImage, Image, CommandLine
```

**ELK KQL:**
```kql
process.name: "powershell.exe" AND
process.args: (*EncodedCommand* OR *Invoke-Expression* OR *DownloadString* OR *IEX* OR *WebClient* OR *-nop* OR *-ep bypass*)
```

**Azure Sentinel KQL:**
```kql
DeviceProcessEvents
| where FileName =~ "powershell.exe"
| where ProcessCommandLine has_any (
    "EncodedCommand", "Invoke-Expression", "DownloadString", "IEX", "WebClient",
    "-nop", "-ep bypass", "-w hidden"
  )
| project Timestamp, DeviceName, AccountName, ProcessCommandLine, InitiatingProcessFileName
```

### Scripting - Malicious Script Execution

**Splunk SPL:**
```spl
index=edr sourcetype=sysmon EventCode=1
| eval script_ext=lower(mvindex(split(Image, "."), -1))
| where script_ext IN ("vbs", "js", "jse", "wsf", "wsh", "bat", "cmd", "ps1")
| eval suspicious_parent=if(match(ParentImage, "(?i)(winword|excel|outlook|acrord32)"), 1, 0)
| where suspicious_parent=1
| table _time, host, user, ParentImage, Image, CommandLine
```

**ELK KQL:**
```kql
process.parent.name: (*word.exe* OR *excel.exe* OR *outlook.exe* OR *acrord32.exe*) AND
process.name: (*.vbs OR *.js OR *.bat OR *.cmd OR *.ps1)
```

**Azure Sentinel KQL:**
```kql
DeviceProcessEvents
| where InitiatingProcessFileName in~ ("winword.exe", "excel.exe", "outlook.exe", "acrord32.exe")
| where FileName in~ ("wscript.exe", "cscript.exe", "cmd.exe", "powershell.exe")
| project Timestamp, DeviceName, AccountName, InitiatingProcessFileName, FileName, ProcessCommandLine
```

---

## Persistence (TA0003)

### Registry Run Keys / Startup Folder

**Splunk SPL:**
```spl
index=edr sourcetype=sysmon EventCode=13
| eval reg_path_lower=lower(TargetObject)
| where match(reg_path_lower, "(?i)(software\\\\microsoft\\\\windows\\\\currentversion\\\\run|software\\\\microsoft\\\\windows\\\\currentversion\\\\runonce)")
| table _time, host, user, EventType, TargetObject, Details, Image
```

**ELK KQL:**
```kql
event.code: "13" AND
registry.path: (*\\CurrentVersion\\Run* OR *\\CurrentVersion\\RunOnce*)
```

**Azure Sentinel KQL:**
```kql
DeviceRegistryEvents
| where RegistryKey has_any (
    @"\Microsoft\Windows\CurrentVersion\Run",
    @"\Microsoft\Windows\CurrentVersion\RunOnce"
  )
| project Timestamp, DeviceName, ActionType, RegistryKey, RegistryValueName, RegistryValueData
```

### Scheduled Task Creation

**Splunk SPL:**
```spl
index=security sourcetype=wineventlog EventCode=4698
| eval task_name=TaskName
| eval task_content=TaskContent
| table _time, host, user, task_name, task_content
```

**ELK KQL:**
```kql
event.code: "4698" AND event.action: "scheduled task created"
```

**Azure Sentinel KQL:**
```kql
SecurityEvent
| where EventID == 4698  // Scheduled task created
| extend TaskName = extract(@"Task Name:\s+(.+)", 1, EventData)
| project TimeGenerated, Computer, Account, TaskName, EventData
```

### Service Installation

**Splunk SPL:**
```spl
index=security sourcetype=wineventlog EventCode=7045
| eval service_name=ServiceName
| eval service_file=ImagePath
| eval suspicious_path=if(match(service_file, "(?i)(temp|appdata|programdata|users\\\\public)"), 1, 0)
| where suspicious_path=1
| table _time, host, user, service_name, service_file
```

**ELK KQL:**
```kql
event.code: "7045" AND
winlog.event_data.ImagePath: (*\\temp\\* OR *\\AppData\\* OR *\\ProgramData\\* OR *\\Users\\Public\\*)
```

**Azure Sentinel KQL:**
```kql
SecurityEvent
| where EventID == 7045  // New service installed
| extend ServiceName = extract(@"Service Name:\s+(.+)", 1, EventData),
         ImagePath = extract(@"Service File Name:\s+(.+)", 1, EventData)
| where ImagePath has_any ("\\temp\\", "\\AppData\\", "\\ProgramData\\", "\\Users\\Public\\")
| project TimeGenerated, Computer, ServiceName, ImagePath
```

---

## Privilege Escalation (TA0004)

### Access Token Manipulation - Privilege Escalation

**Splunk SPL:**
```spl
index=security sourcetype=wineventlog EventCode=4672
| eval privileges=PrivilegeList
| where match(privileges, "(?i)(SeDebugPrivilege|SeImpersonatePrivilege|SeAssignPrimaryTokenPrivilege)")
| where user!="SYSTEM" AND user!="LOCAL SERVICE" AND user!="NETWORK SERVICE"
| stats count by user, host, privileges
| where count > 5
```

**ELK KQL:**
```kql
event.code: "4672" AND
winlog.event_data.PrivilegeList: (*SeDebugPrivilege* OR *SeImpersonatePrivilege* OR *SeAssignPrimaryTokenPrivilege*) AND
NOT user.name: (SYSTEM OR "LOCAL SERVICE" OR "NETWORK SERVICE")
```

**Azure Sentinel KQL:**
```kql
SecurityEvent
| where EventID == 4672  // Special privileges assigned
| where PrivilegeList has_any ("SeDebugPrivilege", "SeImpersonatePrivilege", "SeAssignPrimaryTokenPrivilege")
| where Account !in ("SYSTEM", "LOCAL SERVICE", "NETWORK SERVICE")
| summarize Count=count() by Account, Computer, PrivilegeList
| where Count > 5
```

### Sudo/Su Usage (Linux)

**Splunk SPL:**
```spl
index=linux sourcetype=linux_secure
| eval cmd=lower(_raw)
| where match(cmd, "(?i)(sudo|su)")
| rex field=_raw "(?<command>sudo.*)"
| table _time, host, user, command
```

**ELK KQL:**
```kql
system.auth.sudo.command: * OR event.action: "executed" AND process.name: "sudo"
```

**Azure Sentinel KQL:**
```kql
Syslog
| where Facility == "auth" or Facility == "authpriv"
| where SyslogMessage has "sudo:" or SyslogMessage has "su:"
| extend Command = extract(@"COMMAND=(.+)", 1, SyslogMessage)
| project TimeGenerated, Computer, ProcessName, Command
```

---

## Defense Evasion (TA0005)

### Clear Windows Event Logs

**Splunk SPL:**
```spl
index=security sourcetype=wineventlog EventCode=1102
| table _time, host, user, EventCode, Message
```

**ELK KQL:**
```kql
event.code: "1102" AND event.action: "audit log cleared"
```

**Azure Sentinel KQL:**
```kql
SecurityEvent
| where EventID == 1102  // Audit log cleared
| project TimeGenerated, Computer, Account, Activity
```

### Indicator Removal - File Deletion

**Splunk SPL:**
```spl
index=edr sourcetype=sysmon EventCode=23
| eval file_lower=lower(TargetFilename)
| where match(file_lower, "(?i)(\.log$|\.evtx$|\.txt$)")
| table _time, host, user, TargetFilename, Image
```

**ELK KQL:**
```kql
event.code: "23" AND file.path: (*.log OR *.evtx OR *.txt)
```

**Azure Sentinel KQL:**
```kql
DeviceFileEvents
| where ActionType == "FileDeleted"
| where FileName endswith ".log" or FileName endswith ".evtx" or FileName endswith ".txt"
| project Timestamp, DeviceName, AccountName, FileName, FolderPath
```

### Timestomp - File Time Modification

**Splunk SPL:**
```spl
index=edr sourcetype=sysmon EventCode=2
| eval creation_time=CreationUtcTime
| eval previous_creation=PreviousCreationUtcTime
| where creation_time != previous_creation
| table _time, host, TargetFilename, creation_time, previous_creation
```

**ELK KQL:**
```kql
event.code: "2" AND file.ctime: * AND file.mtime: * AND file.ctime != file.mtime
```

**Azure Sentinel KQL:**
```kql
DeviceFileEvents
| where ActionType == "FileCreated" or ActionType == "FileModified"
| where FileCreationTime != FileModifiedTime
| project Timestamp, DeviceName, FileName, FolderPath, FileCreationTime, FileModifiedTime
```

---

## Credential Access (TA0006)

### Credential Dumping - LSASS Access

**Splunk SPL:**
```spl
index=edr sourcetype=sysmon EventCode=10
| eval target_image_lower=lower(TargetImage)
| where match(target_image_lower, "(?i)lsass\.exe")
| eval source_image_lower=lower(SourceImage)
| where NOT match(source_image_lower, "(?i)(svchost|csrss|wininit)")
| table _time, host, SourceImage, TargetImage, GrantedAccess, user
```

**ELK KQL:**
```kql
event.code: "10" AND
process.name: "lsass.exe" AND
NOT process.parent.name: (svchost.exe OR csrss.exe OR wininit.exe)
```

**Azure Sentinel KQL:**
```kql
DeviceEvents
| where ActionType == "ProcessAccess"
| where FileName =~ "lsass.exe"
| where InitiatingProcessFileName !in~ ("svchost.exe", "csrss.exe", "wininit.exe")
| project Timestamp, DeviceName, InitiatingProcessFileName, FileName, ProcessCommandLine
```

### Password Spraying

**Splunk SPL:**
```spl
index=security sourcetype=auth action=failure
| stats dc(user) as unique_users, count by src_ip
| where unique_users > 10 AND count > 20
| table src_ip, unique_users, count
```

**ELK KQL:**
```kql
event.category: "authentication" AND event.outcome: "failure"
| cardinality BY user.name, source.ip
| WHERE cardinality > 10
```

**Azure Sentinel KQL:**
```kql
SigninLogs
| where ResultType != 0  // Failed login
| summarize UniqueUsers=dcount(UserPrincipalName), TotalAttempts=count() by IPAddress
| where UniqueUsers > 10 and TotalAttempts > 20
| project IPAddress, UniqueUsers, TotalAttempts
```

---

## Discovery (TA0007)

### Network Service Scanning - Port Scanning

**Splunk SPL:**
```spl
index=network sourcetype=firewall action=deny
| stats dc(dest_port) as unique_ports, count by src_ip, dest_ip
| where unique_ports > 20 AND count > 50
| table src_ip, dest_ip, unique_ports, count
```

**ELK KQL:**
```kql
event.action: "deny" AND destination.port: *
| cardinality BY source.ip, destination.ip, destination.port
| WHERE cardinality > 20
```

**Azure Sentinel KQL:**
```kql
AzureNetworkAnalytics_CL
| where FlowStatus_s == "D"  // Denied
| summarize UniquePorts=dcount(DestPort_d), TotalAttempts=count() by SrcIP_s, DestIP_s
| where UniquePorts > 20 and TotalAttempts > 50
| project SrcIP_s, DestIP_s, UniquePorts, TotalAttempts
```

### System Information Discovery

**Splunk SPL:**
```spl
index=edr sourcetype=sysmon EventCode=1
| eval cmd_lower=lower(CommandLine)
| where match(cmd_lower, "(?i)(systeminfo|whoami|net user|net group|ipconfig|netstat)")
| stats count by host, user, Image, CommandLine
| where count > 3
```

**ELK KQL:**
```kql
process.name: (systeminfo.exe OR whoami.exe OR ipconfig.exe OR netstat.exe OR net.exe)
```

**Azure Sentinel KQL:**
```kql
DeviceProcessEvents
| where FileName in~ ("systeminfo.exe", "whoami.exe", "ipconfig.exe", "netstat.exe", "net.exe")
| summarize Count=count() by DeviceName, AccountName, FileName
| where Count > 3
```

---

## Lateral Movement (TA0008)

### Remote Services - RDP

**Splunk SPL:**
```spl
index=security sourcetype=wineventlog EventCode=4624
| where LogonType=10
| stats count, values(src_ip) as source_ips by user, dest_host
| where count > 5
```

**ELK KQL:**
```kql
event.code: "4624" AND winlog.event_data.LogonType: "10"
```

**Azure Sentinel KQL:**
```kql
SecurityEvent
| where EventID == 4624 and LogonType == 10  // RDP login
| summarize Count=count(), SourceIPs=make_set(IpAddress) by Account, Computer
| where Count > 5
```

### Pass the Hash - NTLM Authentication

**Splunk SPL:**
```spl
index=security sourcetype=wineventlog EventCode=4624
| where LogonType=3 AND AuthenticationPackageName="NTLM"
| eval logon_process_lower=lower(LogonProcessName)
| where logon_process_lower!="advapi"
| stats count, dc(dest_host) as unique_hosts by user, src_ip
| where unique_hosts > 3
```

**ELK KQL:**
```kql
event.code: "4624" AND
winlog.event_data.LogonType: "3" AND
winlog.event_data.AuthenticationPackageName: "NTLM"
```

**Azure Sentinel KQL:**
```kql
SecurityEvent
| where EventID == 4624
| where LogonType == 3 and AuthenticationPackageName == "NTLM"
| where LogonProcessName != "Advapi"
| summarize UniqueHosts=dcount(Computer), Count=count() by Account, IpAddress
| where UniqueHosts > 3
```

---

## Collection (TA0009)

### Data Staged - Large File Creation

**Splunk SPL:**
```spl
index=edr sourcetype=sysmon EventCode=11
| eval file_ext=lower(mvindex(split(TargetFilename, "."), -1))
| where file_ext IN ("zip", "rar", "7z", "tar", "gz")
| eval file_path_lower=lower(TargetFilename)
| where match(file_path_lower, "(?i)(temp|appdata|programdata)")
| table _time, host, user, TargetFilename, Image
```

**ELK KQL:**
```kql
event.code: "11" AND
file.extension: (zip OR rar OR 7z OR tar OR gz) AND
file.path: (*\\temp\\* OR *\\AppData\\* OR *\\ProgramData\\*)
```

**Azure Sentinel KQL:**
```kql
DeviceFileEvents
| where ActionType == "FileCreated"
| where FileName endswith ".zip" or FileName endswith ".rar" or FileName endswith ".7z"
| where FolderPath has_any ("\\temp\\", "\\AppData\\", "\\ProgramData\\")
| project Timestamp, DeviceName, AccountName, FileName, FolderPath, FileSize
```

### Screen Capture

**Splunk SPL:**
```spl
index=edr sourcetype=sysmon EventCode=1
| eval cmd_lower=lower(CommandLine)
| where match(cmd_lower, "(?i)(screenshot|screencapture|snippingtool)")
| table _time, host, user, Image, CommandLine
```

**ELK KQL:**
```kql
process.command_line: (*screenshot* OR *screencapture* OR *snippingtool*)
```

**Azure Sentinel KQL:**
```kql
DeviceProcessEvents
| where ProcessCommandLine has_any ("screenshot", "screencapture", "SnippingTool")
| project Timestamp, DeviceName, AccountName, FileName, ProcessCommandLine
```

---

## Exfiltration (TA0010)

### Exfiltration Over Web Service - Cloud Storage Upload

**Splunk SPL:**
```spl
index=proxy sourcetype=proxy
| eval url_lower=lower(url)
| where match(url_lower, "(?i)(dropbox|drive\.google|onedrive|box\.com|mega\.nz)")
| where http_method="POST" OR http_method="PUT"
| stats sum(bytes_out) as total_bytes by user, url, src_ip
| where total_bytes > 100000000  # 100 MB
```

**ELK KQL:**
```kql
http.request.method: (POST OR PUT) AND
url.domain: (dropbox.com OR drive.google.com OR onedrive.live.com OR box.com OR mega.nz) AND
http.request.bytes > 100000000
```

**Azure Sentinel KQL:**
```kql
CommonSecurityLog
| where RequestMethod in ("POST", "PUT")
| where RequestURL has_any ("dropbox.com", "drive.google.com", "onedrive.live.com", "box.com")
| summarize TotalBytes=sum(SentBytes) by SourceUserID, RequestURL, SourceIP
| where TotalBytes > 100000000  // 100 MB
```

### Data Transfer Size Limits - Large Outbound Transfer

**Splunk SPL:**
```spl
index=network sourcetype=firewall action=allow
| where dest_port IN (80, 443, 8080)
| stats sum(bytes_out) as total_bytes by src_ip, dest_ip, dest_port
| where total_bytes > 1000000000  # 1 GB
| sort -total_bytes
```

**ELK KQL:**
```kql
destination.port: (80 OR 443 OR 8080) AND
network.bytes > 1000000000
```

**Azure Sentinel KQL:**
```kql
AzureNetworkAnalytics_CL
| where DestPort_d in (80, 443, 8080)
| summarize TotalBytes=sum(OutboundBytes_d) by SrcIP_s, DestIP_s, DestPort_d
| where TotalBytes > 1000000000  // 1 GB
| top 20 by TotalBytes desc
```

---

## Command and Control (TA0011)

### DNS Tunneling Detection

**Splunk SPL:**
```spl
index=dns sourcetype=dns
| eval query_length=len(query)
| where query_length > 50
| stats count, avg(query_length) as avg_length by query, src_ip
| where count > 10 AND avg_length > 60
| sort -count
```

**ELK KQL:**
```kql
dns.question.name: * AND dns.question.name.length > 50
```

**Azure Sentinel KQL:**
```kql
DnsEvents
| extend QueryLength = strlen(Name)
| where QueryLength > 50
| summarize Count=count(), AvgLength=avg(QueryLength) by Name, ClientIP
| where Count > 10 and AvgLength > 60
| top 20 by Count desc
```

### Beaconing - Regular Outbound Connections

**Splunk SPL:**
```spl
index=network sourcetype=firewall action=allow
| eval hour=strftime(_time, "%H")
| stats count by src_ip, dest_ip, dest_port, hour
| eventstats avg(count) as avg_count, stdev(count) as stdev_count by src_ip, dest_ip, dest_port
| eval cv=stdev_count/avg_count
| where cv < 0.2  # Low coefficient of variation = consistent beaconing
| table src_ip, dest_ip, dest_port, avg_count, cv
```

**ELK KQL:**
```kql
event.action: "allow" AND destination.ip: * AND destination.port: *
| stats count by source.ip, destination.ip, destination.port, @timestamp.hour
```

**Azure Sentinel KQL:**
```kql
AzureNetworkAnalytics_CL
| extend Hour = hourofday(FlowStartTime_t)
| summarize Count=count() by SrcIP_s, DestIP_s, DestPort_d, Hour
| summarize AvgCount=avg(Count), StdevCount=stdev(Count) by SrcIP_s, DestIP_s, DestPort_d
| extend CV = StdevCount / AvgCount
| where CV < 0.2  // Consistent beaconing pattern
| project SrcIP_s, DestIP_s, DestPort_d, AvgCount, CV
```

### Non-Standard Port Usage

**Splunk SPL:**
```spl
index=network sourcetype=firewall action=allow
| where dest_port NOT IN (80, 443, 22, 3389, 445, 53, 123, 389, 636, 3268, 3269)
| stats sum(bytes_out) as total_bytes, count by src_ip, dest_ip, dest_port
| where total_bytes > 10000000 OR count > 100
| sort -total_bytes
```

**ELK KQL:**
```kql
NOT destination.port: (80 OR 443 OR 22 OR 3389 OR 445 OR 53 OR 123 OR 389 OR 636) AND
network.bytes > 10000000
```

**Azure Sentinel KQL:**
```kql
AzureNetworkAnalytics_CL
| where DestPort_d !in (80, 443, 22, 3389, 445, 53, 123, 389, 636, 3268, 3269)
| summarize TotalBytes=sum(OutboundBytes_d), Count=count() by SrcIP_s, DestIP_s, DestPort_d
| where TotalBytes > 10000000 or Count > 100
| top 20 by TotalBytes desc
```

---

## Bonus: Threat Hunting Queries

### Rare Parent-Child Process Relationships

**Splunk SPL:**
```spl
index=edr sourcetype=sysmon EventCode=1
| stats count by ParentImage, Image
| where count < 5
| sort count
```

**Azure Sentinel KQL:**
```kql
DeviceProcessEvents
| summarize Count=count() by InitiatingProcessFileName, FileName
| where Count < 5
| order by Count asc
```

### Anomalous User Behavior - Access Outside Business Hours

**Splunk SPL:**
```spl
index=security sourcetype=auth action=success
| eval hour=strftime(_time, "%H")
| eval is_after_hours=if(hour < 8 OR hour > 18, 1, 0)
| where is_after_hours=1
| stats count by user, src_ip, hour
| where count > 3
```

**Azure Sentinel KQL:**
```kql
SigninLogs
| extend Hour = hourofday(TimeGenerated)
| where Hour < 8 or Hour > 18
| summarize Count=count() by UserPrincipalName, IPAddress, Hour
| where Count > 3
```

### New Process Execution (Threat Hunting)

**Splunk SPL:**
```spl
index=edr sourcetype=sysmon EventCode=1
| stats earliest(_time) as first_seen by Image, hash
| where first_seen > relative_time(now(), "-7d")
| table first_seen, Image, hash
```

**Azure Sentinel KQL:**
```kql
DeviceProcessEvents
| summarize FirstSeen=min(Timestamp) by FileName, SHA256
| where FirstSeen > ago(7d)
| project FirstSeen, FileName, SHA256
```

---

## Performance Optimization Tips

### Splunk Optimization

1. **Use index and sourcetype filters first:**
   ```spl
   # Good
   index=security sourcetype=wineventlog EventCode=4624

   # Bad (slow)
   EventCode=4624 | search index=security sourcetype=wineventlog
   ```

2. **Limit time range:**
   ```spl
   earliest=-24h latest=now
   ```

3. **Use tstats for acceleration:**
   ```spl
   | tstats count where index=security by _time, user span=1h
   ```

### ELK Optimization

1. **Use index patterns:**
   ```kql
   # Target specific indices
   _index: "filebeat-*" AND event.code: "4624"
   ```

2. **Filter early:**
   ```kql
   # Apply filters before aggregations
   event.category: "authentication" AND event.outcome: "failure"
   | stats count by user.name
   ```

### Azure Sentinel Optimization

1. **Time filters first:**
   ```kql
   SigninLogs
   | where TimeGenerated > ago(1h)
   | where ResultType != 0
   ```

2. **Limit columns projected:**
   ```kql
   | project TimeGenerated, UserPrincipalName, IPAddress
   # Instead of returning all columns
   ```

---

*Last Updated: 2025-01-17*
*Version: 1.0.0*
*MITRE ATT&CK Framework: v14*
