# Real-World STRIDE Examples

## Overview

This document provides practical examples of STRIDE threats from real-world security incidents and common vulnerabilities.

---

## Spoofing Examples

### Example 1: Session Hijacking via XSS

**Incident:** Attacker steals session token through XSS vulnerability

**Attack Scenario:**
1. Application stores JWT in localStorage
2. XSS vulnerability allows script injection
3. Malicious script reads localStorage and exfiltrates JWT
4. Attacker uses stolen JWT to impersonate user

**DREAD Score:**
- Damage: 8 (Full account access)
- Reproducibility: 9 (Easy if XSS exists)
- Exploitability: 7 (Requires XSS vulnerability)
- Affected Users: 8 (Any user who visits malicious page)
- Discoverability: 6 (Common vulnerability)
- **Total: 7.6 (High Priority)**

**Mitigations:**
- Store tokens in httpOnly, secure cookies (NIST SC-8)
- Implement Content Security Policy (CSP)
- Sanitize all user input (NIST SI-10)
- Use X-XSS-Protection header
- Regular security testing (NIST RA-5)

### Example 2: DNS Spoofing

**Incident:** 2014 Venezuela internet censorship incident

**Attack Scenario:**
1. Attacker compromises DNS resolver
2. Redirects legitimate domain to malicious server
3. Users connect to fake server, provide credentials
4. Attacker harvests credentials

**Mitigations:**
- Implement DNSSEC validation
- Use certificate pinning in mobile apps
- Monitor DNS resolution anomalies (NIST SI-4)
- Educate users about certificate warnings

---

## Tampering Examples

### Example 3: Price Manipulation in E-commerce

**Incident:** Client-side price tampering vulnerability

**Attack Scenario:**
1. E-commerce site sends product price in hidden form field
2. Attacker intercepts request using proxy (Burp Suite)
3. Modifies price from $100 to $1
4. Submits modified request
5. Backend processes order at tampered price

**DREAD Score:**
- Damage: 9 (Direct financial loss)
- Reproducibility: 10 (Trivial to reproduce)
- Exploitability: 9 (No special skills needed)
- Affected Users: 2 (Limited to attackers)
- Discoverability: 8 (Easy to find with proxy)
- **Total: 7.6 (High Priority)**

**Mitigations:**
- Never trust client-side data (NIST SI-10)
- Store prices server-side, reference by ID
- Implement server-side validation
- Use HMAC to sign form data (NIST SC-8(1))
- Log price discrepancies for monitoring (NIST AU-2)

### Example 4: Git Repository Tampering

**Incident:** 2021 PHP Git Server Compromise

**Attack Scenario:**
1. Attackers compromised git.php.net server
2. Injected backdoor into PHP source code
3. Malicious commit pushed to official repository
4. Backdoor would have reached production systems

**Mitigations:**
- Require signed commits (GPG signatures)
- Implement code review for all changes
- Use branch protection rules
- Monitor for unauthorized commits (NIST AU-2)
- Maintain separate signing keys (NIST SC-12)

---

## Repudiation Examples

### Example 5: Missing Audit Logs

**Incident:** Insider threat without accountability

**Attack Scenario:**
1. Database admin has full access to user records
2. No logging of database queries or data exports
3. Admin exports customer PII for personal use
4. No evidence of data exfiltration
5. Admin denies any wrongdoing

**DREAD Score:**
- Damage: 7 (Data breach)
- Reproducibility: 10 (Always possible without logging)
- Exploitability: 8 (Requires privileged access)
- Affected Users: 8 (All customers)
- Discoverability: 2 (Hard to detect without logs)
- **Total: 7.0 (High Priority)**

**Mitigations:**
- Implement comprehensive audit logging (NIST AU-2)
- Protect log integrity (NIST AU-9)
- Centralize logs to SIEM (NIST AU-6)
- Monitor for data exfiltration (NIST SI-4)
- Require approval for bulk exports (NIST AC-3)

### Example 6: Email Spoofing for Social Engineering

**Incident:** Business Email Compromise (BEC)

**Attack Scenario:**
1. Attacker spoofs CEO's email address
2. Sends urgent wire transfer request to finance
3. Finance team complies, transfers funds
4. CEO denies sending email (no authentication)
5. No way to prove email origin

**Mitigations:**
- Implement DMARC, SPF, DKIM
- Require secondary verification for financial transactions
- Train employees on BEC tactics
- Log all email authentication failures (NIST AU-2)

---

## Information Disclosure Examples

### Example 7: API Exposure via IDOR

**Incident:** Insecure Direct Object Reference vulnerability

**Attack Scenario:**
1. API endpoint: `GET /api/users/{userId}/profile`
2. No authorization check beyond authentication
3. Attacker iterates userId from 1 to 10000
4. Downloads all user profiles, exposing PII
5. Data sold on dark web

**DREAD Score:**
- Damage: 9 (Mass PII exposure)
- Reproducibility: 10 (Trivial script)
- Exploitability: 9 (No special tools needed)
- Affected Users: 10 (All users)
- Discoverability: 7 (Common vulnerability)
- **Total: 9.0 (Critical Priority)**

**Mitigations:**
- Implement authorization checks (NIST AC-3)
- Use UUIDs instead of sequential IDs
- Rate limit API endpoints (NIST SC-5)
- Monitor for enumeration patterns (NIST SI-4)
- Implement API authentication with scopes (NIST IA-2)

### Example 8: S3 Bucket Misconfiguration

**Incident:** 2019 Capital One breach (100M+ records)

**Attack Scenario:**
1. S3 bucket configured with public read access
2. Bucket contains customer data, backups
3. Attacker discovers bucket via scanning
4. Downloads all data
5. 100 million+ customer records exposed

**Mitigations:**
- Default deny for cloud storage (NIST AC-3)
- Use bucket policies to restrict access
- Enable encryption at rest (NIST SC-28)
- Monitor for public access (NIST SI-4)
- Regular access audits (NIST RA-5)

---

## Denial of Service Examples

### Example 9: Application-Layer DDoS

**Incident:** Slowloris attack on web server

**Attack Scenario:**
1. Attacker opens many connections to web server
2. Sends partial HTTP requests slowly
3. Server waits for complete requests
4. Connection pool exhausted
5. Legitimate users cannot connect

**DREAD Score:**
- Damage: 7 (Service unavailable)
- Reproducibility: 10 (Easy to reproduce)
- Exploitability: 8 (Simple tools available)
- Affected Users: 10 (All users)
- Discoverability: 9 (Well-known attack)
- **Total: 8.8 (Critical Priority)**

**Mitigations:**
- Implement connection timeouts (NIST SC-5)
- Use reverse proxy with rate limiting
- Deploy DDoS protection service (Cloudflare, AWS Shield)
- Monitor connection patterns (NIST SI-4)
- Increase timeout efficiency

### Example 10: Database Resource Exhaustion

**Incident:** Complex query DoS

**Attack Scenario:**
1. API allows user-defined search filters
2. Attacker crafts complex query with multiple JOINs
3. Query takes 60+ seconds to execute
4. Attacker submits 100 concurrent requests
5. Database becomes unresponsive
6. All application features fail

**Mitigations:**
- Implement query complexity limits
- Set database query timeout (NIST SC-5)
- Use read replicas for expensive queries
- Rate limit complex operations (NIST AC-7)
- Monitor query performance (NIST SI-4)

---

## Elevation of Privilege Examples

### Example 11: SQL Injection to Admin Access

**Incident:** Classic SQL injection vulnerability

**Attack Scenario:**
1. Login form vulnerable to SQL injection
2. Username field: `admin' OR 1=1--`
3. SQL query becomes: `SELECT * FROM users WHERE username='admin' OR 1=1--' AND password='...'`
4. Query always returns true
5. Attacker authenticated as admin

**DREAD Score:**
- Damage: 10 (Full system compromise)
- Reproducibility: 10 (100% reliable)
- Exploitability: 8 (Requires SQL knowledge)
- Affected Users: 10 (Entire system)
- Discoverability: 9 (Well-known vulnerability)
- **Total: 9.4 (Critical Priority)**

**Mitigations:**
- Use parameterized queries exclusively (NIST SI-10)
- Implement input validation with whitelist
- Use ORM frameworks properly
- Apply principle of least privilege (NIST AC-6)
- Regular security testing (NIST RA-5)
- Deploy Web Application Firewall

### Example 12: Container Escape via Misconfiguration

**Incident:** Docker container breakout

**Attack Scenario:**
1. Container runs with `--privileged` flag
2. Attacker compromises application in container
3. Exploits privileged mode to access host
4. Gains root access to host system
5. Pivots to other containers

**Mitigations:**
- Never use `--privileged` in production
- Implement security contexts (NIST AC-6)
- Use non-root containers
- Scan container images (NIST RA-5)
- Implement runtime security (Falco, Sysdig)
- Network segmentation for containers (NIST SC-7)

---

## Combined STRIDE Attacks

### Example 13: Full Attack Chain - Web Application

**Incident:** Multi-stage attack combining multiple STRIDE categories

**Attack Chain:**
1. **[I] Information Disclosure:** Directory traversal reveals source code
2. **[S] Spoofing:** Hardcoded API key found in code
3. **[T] Tampering:** Use API key to modify user roles
4. **[E] Elevation of Privilege:** Grant self admin privileges
5. **[R] Repudiation:** Delete audit logs to cover tracks
6. **[D] Denial of Service:** Deploy cryptominer, degrading service

**Mitigations (Defense in Depth):**
- Disable directory listing (NIST CM-7)
- Never hardcode secrets, use secret manager (NIST SC-12)
- Implement robust authorization (NIST AC-3)
- Protect log integrity, centralize logs (NIST AU-9)
- Monitor for anomalous behavior (NIST SI-4)
- Implement resource quotas (NIST SC-5)

---

## Industry-Specific Examples

### Example 14: Healthcare - HIPAA Violation via API

**Scenario:** Patient health records exposed via API

**Attack:**
1. Mobile app API endpoint: `GET /api/patients/{id}/records`
2. No authorization check beyond valid session
3. Attacker uses their own session, iterates patient IDs
4. Downloads 50,000 patient health records

**Impact:**
- HIPAA violation: $100K-$1.5M fine per incident
- Patient privacy compromised
- Reputational damage
- Legal liability

**NIST Controls:**
- AC-3: Access control enforcement
- AC-6: Least privilege
- AU-2: Audit logging
- RA-5: Vulnerability scanning

### Example 15: Financial - Transaction Tampering

**Scenario:** Payment amount manipulation

**Attack:**
1. Mobile banking app sends transaction details in request
2. Attacker intercepts, modifies amount from $1000 to $10
3. Backend processes transaction at tampered amount
4. Attacker steals $990

**Mitigations:**
- Server-side transaction validation
- Transaction signing with HMAC
- Anomaly detection for unusual amounts
- Two-factor authentication for transactions

---

## Detection Patterns

### Log Patterns for STRIDE Threats

**Spoofing Detection:**
```
# Multiple failed auth attempts followed by success from different IP
[ALERT] User: alice, Failed logins: 15, Source: 192.168.1.1
[ALERT] User: alice, Successful login, Source: 10.0.0.5
```

**Tampering Detection:**
```
# Unexpected changes to critical data
[ALERT] User role changed: user_id=123, old=user, new=admin, actor=user_id:456
[ALERT] Price modified in order: order_id=789, old=$100, new=$1
```

**Repudiation Detection:**
```
# Gap in audit logs
[ALERT] Audit log gap detected: missing entries from 14:00-15:30
[ALERT] Log file modified: /var/log/audit.log, modification_time > create_time
```

**Information Disclosure Detection:**
```
# Enumeration attempts
[ALERT] Sequential ID access: user_id 1-1000 accessed in 60 seconds
[ALERT] Large data export: user=admin, records=50000, table=customers
```

**Denial of Service Detection:**
```
# Abnormal resource consumption
[ALERT] Connection surge: 10000 connections from 203.0.113.1 in 10 seconds
[ALERT] Query timeout: query_duration > 30s, concurrent_queries=50
```

**Elevation of Privilege Detection:**
```
# Privilege escalation
[ALERT] User privilege changed: user_id=123, from=user to=admin
[ALERT] Unauthorized access attempt: user=guest, resource=/admin/panel
```

---

## Risk Assessment Examples

### Example 16: Risk Calculation

**Threat:** SQL Injection in authentication

**DREAD Breakdown:**
- **D** (Damage): 10 - Complete database compromise
- **R** (Reproducibility): 10 - 100% reliable exploit
- **E** (Exploitability): 7 - Requires SQL knowledge but tools available
- **A** (Affected Users): 10 - All users and data affected
- **D** (Discoverability): 9 - Automated scanners find it easily

**DREAD Score:** (10+10+7+10+9)/5 = **9.2 (Critical)**

**Risk Level:** Critical  
**Action Required:** Immediate remediation (0-7 days)  
**NIST Controls:** SI-10, RA-3, RA-5

---

## Mitigation Effectiveness

### Example 17: Before and After Metrics

**Threat:** Account takeover via credential stuffing

**Before Mitigations:**
- Successful attacks: 50/month
- Compromised accounts: 200/month
- Detection time: 48 hours average

**Mitigations Implemented:**
- Multi-factor authentication (MFA)
- Rate limiting (10 attempts/minute)
- CAPTCHA after 3 failures
- Anomaly detection

**After Mitigations:**
- Successful attacks: 2/month (-96%)
- Compromised accounts: 5/month (-97.5%)
- Detection time: 5 minutes average (-99.8%)
- MFA adoption: 85% of users

**NIST Controls Satisfied:**
- IA-2(1): Multi-factor authentication
- AC-7: Unsuccessful login attempts
- SI-4: Information system monitoring

---

## Next Steps

1. Review examples relevant to your system architecture
2. Identify similar threats in your threat model
3. Apply appropriate mitigations from examples
4. Implement detection patterns for monitoring
5. Conduct security testing to validate mitigations

**Related Resources:**
- `stride-template.md` - Use these examples in your threat model
- `threat-scenario.md` - Document attack chains
- `mitigation-plan.md` - Track mitigation implementation
