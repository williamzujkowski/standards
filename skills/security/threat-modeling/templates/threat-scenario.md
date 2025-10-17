# Threat Scenario & Attack Tree Template

## Threat Scenario Overview

**Scenario ID:** _[TS-001]_  
**Scenario Name:** _[Brief descriptive name]_  
**Attack Goal:** _[What attacker wants to achieve]_  
**Affected System:** _[System or component]_  
**Threat Category:** _[STRIDE category]_  
**Risk Level:** _[Critical/High/Medium/Low]_

## Attack Tree

```
Goal: [Primary attack objective]
│
├─── AND [Required condition 1]
│    ├─── OR [Alternative method A]
│    │    ├─── [Specific technique A1]
│    │    │    Cost: [Low/Med/High]
│    │    │    Skill: [Low/Med/High]
│    │    │    Detection: [Easy/Med/Hard]
│    │    │
│    │    └─── [Specific technique A2]
│    │         Cost: [Low/Med/High]
│    │         Skill: [Low/Med/High]
│    │         Detection: [Easy/Med/Hard]
│    │
│    └─── OR [Alternative method B]
│         └─── [Specific technique B1]
│
└─── AND [Required condition 2]
     └─── [Technique C]
```

### Example: Account Takeover Attack Tree

```
Goal: Gain Unauthorized Access to User Account
│
├─── AND [Obtain Valid Credentials]
│    ├─── OR [Steal Credentials]
│    │    ├─── Phishing email
│    │    │    Cost: Low
│    │    │    Skill: Low
│    │    │    Detection: Medium
│    │    │    Mitigation: User training, email filtering
│    │    │
│    │    ├─── Credential stuffing
│    │    │    Cost: Low
│    │    │    Skill: Medium
│    │    │    Detection: Easy (rate limiting)
│    │    │    Mitigation: Rate limiting, CAPTCHA
│    │    │
│    │    └─── Keylogger malware
│    │         Cost: Medium
│    │         Skill: High
│    │         Detection: Medium
│    │         Mitigation: Endpoint protection, MFA
│    │
│    └─── OR [Exploit Auth Vulnerability]
│         ├─── SQL injection in login
│         │    Cost: Low
│         │    Skill: Medium
│         │    Detection: Easy (WAF)
│         │    Mitigation: Parameterized queries, input validation
│         │
│         └─── Session fixation
│              Cost: Low
│              Skill: High
│              Detection: Hard
│              Mitigation: Regenerate session IDs
│
└─── AND [Bypass Additional Security]
     ├─── OR [Defeat MFA]
     │    ├─── SIM swap attack
     │    │    Cost: Medium
     │    │    Skill: Medium
     │    │    Detection: Hard
     │    │    Mitigation: Hardware tokens, app-based MFA
     │    │
     │    └─── MFA fatigue attack
     │         Cost: Low
     │         Skill: Low
     │         Detection: Medium
     │         Mitigation: Number matching, rate limiting
     │
     └─── Social engineering support desk
          Cost: Low
          Skill: Low
          Detection: Medium
          Mitigation: Strict verification procedures
```

## Detailed Attack Scenario

### Step-by-Step Attack Path

**Step 1: Initial Access**
- **Attacker Action:** _[What attacker does]_
- **System Response:** _[How system reacts]_
- **Prerequisites:** _[What must be in place]_
- **Indicators:** _[Signs of attack]_

**Step 2: Privilege Escalation**
- **Attacker Action:** _[What attacker does]_
- **System Response:** _[How system reacts]_
- **Prerequisites:** _[What must be in place]_
- **Indicators:** _[Signs of attack]_

**Step 3: Goal Achievement**
- **Attacker Action:** _[What attacker does]_
- **System Response:** _[How system reacts]_
- **Impact:** _[What damage is done]_
- **Indicators:** _[Signs of attack]_

### Example: SQL Injection Attack Scenario

**Step 1: Reconnaissance**
- **Attacker Action:** Probe login form with `' OR 1=1--` in username field
- **System Response:** Error message reveals SQL syntax, confirming vulnerability
- **Prerequisites:** Unfiltered input, verbose error messages
- **Indicators:** Unusual characters in request logs, SQL errors in application logs

**Step 2: Exploitation**
- **Attacker Action:** Craft SQL injection payload to dump user table: `admin' UNION SELECT username,password,email FROM users--`
- **System Response:** Returns all user records including password hashes
- **Prerequisites:** Database connection with SELECT privileges
- **Indicators:** Complex queries in logs, unusually large responses, UNION keywords in requests

**Step 3: Privilege Escalation**
- **Attacker Action:** Crack admin password hash offline, login as admin
- **System Response:** Grants admin access to system
- **Impact:** Full control of application and data
- **Indicators:** Login from new IP, admin access from unusual location, mass data exports

## Attack Scenario Details

### Threat Actor Profile

**Actor Type:** _[Nation State / Organized Crime / Insider / Script Kiddie / Hacktivist]_  
**Motivation:** _[Financial / Espionage / Disruption / Ideology]_  
**Skill Level:** _[Expert / Advanced / Intermediate / Novice]_  
**Resources:** _[High / Medium / Low]_  
**Persistence:** _[High / Medium / Low]_

### Attack Surface

**Entry Points:**
- _[List all potential entry points]_

**Attack Vectors:**
- _[List attack vectors used]_

**Required Access:**
- _[Network access, physical access, credentials, etc.]_

### Technical Details

**Exploited Vulnerabilities:**
| CVE/CWE | Component | Description | CVSS Score |
|---------|-----------|-------------|------------|
| _[ID]_ | _[Component]_ | _[Description]_ | _[Score]_ |

**Tools & Techniques:**
| Tool | Purpose | MITRE ATT&CK Technique |
|------|---------|------------------------|
| _[Tool]_ | _[Usage]_ | _[Technique ID]_ |

**Payload Example:**
```
[Include actual payload or code snippet if relevant]
```

## Impact Analysis

### Confidentiality Impact

**Data Exposed:**
- _[List data types exposed]_

**Affected Records:** _[Number or scope]_  
**Sensitivity Level:** _[Public / Internal / Confidential / Secret]_

### Integrity Impact

**Modified Components:**
- _[List what could be altered]_

**Data Corruption Risk:** _[Describe potential corruption]_

### Availability Impact

**Affected Services:**
- _[List impacted services]_

**Downtime Estimate:** _[Duration]_  
**Recovery Complexity:** _[Simple / Moderate / Complex]_

### Business Impact

**Financial Impact:** $[Amount or range]  
**Reputational Impact:** _[Description]_  
**Regulatory Impact:** _[Compliance violations]_  
**Customer Impact:** _[Number affected]_

## Detection & Response

### Detection Mechanisms

**Preventive Controls:**
- [ ] _[Control 1]_ - NIST: _[Control ID]_
- [ ] _[Control 2]_ - NIST: _[Control ID]_

**Detective Controls:**
- [ ] _[Monitor/alert 1]_ - NIST: _[Control ID]_
- [ ] _[Monitor/alert 2]_ - NIST: _[Control ID]_

**Response Controls:**
- [ ] _[Response 1]_ - NIST: _[Control ID]_
- [ ] _[Response 2]_ - NIST: _[Control ID]_

### Indicators of Compromise (IOCs)

**Network Indicators:**
- _[Suspicious IP addresses, domains, URLs]_

**Host Indicators:**
- _[File hashes, registry keys, processes]_

**Application Indicators:**
- _[Error patterns, unusual queries, timing anomalies]_

**Behavioral Indicators:**
- _[Access patterns, data volume, timing]_

### Detection Rules

```yaml
# Example SIEM rule
rule: "SQL Injection Detection"
conditions:
  - field: "http.request.body"
    operator: "contains"
    values: ["UNION SELECT", "' OR 1=1", "'; DROP TABLE"]
  - field: "http.status"
    operator: "equals"
    value: 500
severity: High
action: Alert + Block
```

## Mitigation Strategy

### Immediate Actions (0-7 days)

| Action | Owner | Target Date | Status |
|--------|-------|-------------|--------|
| _[Action]_ | _[Team/Person]_ | _[Date]_ | _[Status]_ |

### Short-term Mitigations (1-3 months)

| Action | Owner | Target Date | NIST Control | Status |
|--------|-------|-------------|--------------|--------|
| _[Action]_ | _[Team/Person]_ | _[Date]_ | _[Control]_ | _[Status]_ |

### Long-term Security Improvements (3-12 months)

| Action | Owner | Target Date | NIST Control | Status |
|--------|-------|-------------|--------------|--------|
| _[Action]_ | _[Team/Person]_ | _[Date]_ | _[Control]_ | _[Status]_ |

### Compensating Controls

_[If mitigation cannot be fully implemented, describe compensating controls]_

## Validation & Testing

### Security Testing

- [ ] Penetration test conducted
- [ ] Vulnerability scan performed
- [ ] Code review completed
- [ ] Threat scenario validated
- [ ] Detection rules tested
- [ ] Response procedures exercised

### Test Results

**Test Date:** _[Date]_  
**Tester:** _[Name/Team]_  
**Outcome:** _[Vulnerability confirmed/mitigated]_  
**Evidence:** _[Reference to test report]_

## Related Threats

**Related Threat IDs:** _[List related threats from threat model]_  
**Attack Chain Dependencies:** _[What must succeed before this attack]_  
**Follow-on Attacks:** _[What attacks this enables]_

## References

- **MITRE ATT&CK:** _[Technique IDs]_
- **CWE:** _[Weakness IDs]_
- **CVE:** _[Vulnerability IDs]_
- **NIST Controls:** _[Control IDs]_
- **Industry Incidents:** _[Similar real-world attacks]_

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | _[Date]_ | _[Name]_ | Initial scenario |

---

**Next Steps:**
1. Review scenario with security team
2. Validate with penetration testing
3. Implement prioritized mitigations
4. Create detection rules
5. Document in threat model
6. Schedule periodic review
