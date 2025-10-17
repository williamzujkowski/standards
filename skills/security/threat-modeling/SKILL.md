---
name: threat-modeling
category: security
difficulty: intermediate
nist_controls: [RA-3, RA-5]
tags: [stride, risk-assessment, attack-trees, dfd, threat-analysis]
related_skills: [security-testing, secure-coding, vulnerability-management]
learning_path: security
estimated_time: 4-6 hours
prerequisites: [security-fundamentals, architecture-basics]
---

# Threat Modeling

> **Identify, prioritize, and mitigate security threats systematically using STRIDE methodology**

## Level 1: Quick Reference

### STRIDE Threat Categories

```yaml
threats:
  S_spoofing:
    description: Impersonating something or someone else
    targets: [authentication, identity]
    example: "Using stolen credentials to access system"
    
  T_tampering:
    description: Modifying data or code maliciously
    targets: [data_integrity, code_integrity]
    example: "Altering transaction amounts in transit"
    
  R_repudiation:
    description: Claiming to not have performed an action
    targets: [logging, audit_trails]
    example: "Denying fraudulent transaction was performed"
    
  I_information_disclosure:
    description: Exposing information to unauthorized parties
    targets: [confidentiality, data_protection]
    example: "Leaking customer PII through error messages"
    
  D_denial_of_service:
    description: Making system unavailable or degraded
    targets: [availability, performance]
    example: "Overwhelming API with requests"
    
  E_elevation_of_privilege:
    description: Gaining unauthorized higher access level
    targets: [authorization, access_control]
    example: "Exploiting bug to gain admin rights"
```

### Four Key Questions

1. **What are we building?**
   - System architecture, components, data flows
   - Trust boundaries, entry/exit points
   
2. **What can go wrong?**
   - Apply STRIDE to each component
   - Identify threat scenarios
   
3. **What should we do about it?**
   - Prioritize threats (DREAD scoring)
   - Design mitigations
   
4. **Did we do a good job?**
   - Review threat model coverage
   - Validate mitigations

### Essential Checklist

**Planning Phase:**
- [ ] Identify system scope and boundaries
- [ ] Document assets and data flows
- [ ] Define security objectives
- [ ] Assemble threat modeling team

**Analysis Phase:**
- [ ] Create data flow diagrams (DFD)
- [ ] Mark trust boundaries
- [ ] Apply STRIDE to each element
- [ ] Document threat scenarios
- [ ] Build attack trees

**Prioritization:**
- [ ] Score threats using DREAD
- [ ] Classify by impact and likelihood
- [ ] Map to security controls (NIST RA-3)

**Mitigation:**
- [ ] Design countermeasures
- [ ] Assign ownership and timeline
- [ ] Track implementation status
- [ ] Verify effectiveness (NIST RA-5)

**Documentation:**
- [ ] Maintain threat model repository
- [ ] Update for architecture changes
- [ ] Share findings with stakeholders
- [ ] Schedule periodic reviews

---

## Level 2: Implementation Guide

### STRIDE Methodology

#### Systematic Threat Identification

```yaml
# Apply STRIDE to each DFD element

processes:
  - name: "Authentication Service"
    threats:
      spoofing:
        - "Attacker uses stolen JWT token"
        - "Session hijacking via XSS"
      tampering:
        - "Modify auth response to elevate privileges"
      repudiation:
        - "No audit log of failed auth attempts"
      information_disclosure:
        - "Username enumeration via timing attack"
      denial_of_service:
        - "Brute force password attempts"
      elevation_of_privilege:
        - "JWT signature bypass"
        
data_stores:
  - name: "User Database"
    threats:
      spoofing: "N/A - data stores don't authenticate"
      tampering:
        - "SQL injection modifies user roles"
        - "Direct database access without encryption"
      repudiation:
        - "No change tracking on user records"
      information_disclosure:
        - "Database backup stored unencrypted"
        - "Weak access controls on database"
      denial_of_service:
        - "Resource exhaustion via complex queries"
      elevation_of_privilege:
        - "Privilege escalation via stored procedures"
        
data_flows:
  - name: "Login Request → Auth Service"
    threats:
      spoofing:
        - "Man-in-the-middle intercepts credentials"
      tampering:
        - "Modify request to bypass validation"
      repudiation: "N/A - flows don't take actions"
      information_disclosure:
        - "Credentials sent over unencrypted connection"
      denial_of_service:
        - "Flood authentication endpoint"
      elevation_of_privilege: "N/A - flows don't have privileges"
```

#### STRIDE-per-Element Pattern

```python
# threat_model.py

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class ThreatCategory(Enum):
    SPOOFING = "Spoofing"
    TAMPERING = "Tampering"
    REPUDIATION = "Repudiation"
    INFORMATION_DISCLOSURE = "Information Disclosure"
    DENIAL_OF_SERVICE = "Denial of Service"
    ELEVATION_OF_PRIVILEGE = "Elevation of Privilege"

class ElementType(Enum):
    PROCESS = "Process"
    DATA_STORE = "Data Store"
    DATA_FLOW = "Data Flow"
    EXTERNAL_ENTITY = "External Entity"

@dataclass
class Threat:
    category: ThreatCategory
    description: str
    attack_scenario: str
    impact: str
    likelihood: str
    mitigation: Optional[str] = None
    nist_control: Optional[str] = None

@dataclass
class ThreatModelElement:
    name: str
    element_type: ElementType
    threats: List[Threat]
    trust_boundary: Optional[str] = None
    
    def applicable_stride_categories(self) -> List[ThreatCategory]:
        """Return STRIDE categories applicable to this element type."""
        if self.element_type == ElementType.PROCESS:
            return list(ThreatCategory)  # All STRIDE applies
        elif self.element_type == ElementType.DATA_STORE:
            return [
                ThreatCategory.TAMPERING,
                ThreatCategory.REPUDIATION,
                ThreatCategory.INFORMATION_DISCLOSURE,
                ThreatCategory.DENIAL_OF_SERVICE
            ]
        elif self.element_type == ElementType.DATA_FLOW:
            return [
                ThreatCategory.SPOOFING,
                ThreatCategory.TAMPERING,
                ThreatCategory.INFORMATION_DISCLOSURE,
                ThreatCategory.DENIAL_OF_SERVICE
            ]
        elif self.element_type == ElementType.EXTERNAL_ENTITY:
            return [
                ThreatCategory.SPOOFING,
                ThreatCategory.REPUDIATION
            ]
        return []

# Example usage
auth_service = ThreatModelElement(
    name="Authentication Service",
    element_type=ElementType.PROCESS,
    trust_boundary="Internal Services",
    threats=[
        Threat(
            category=ThreatCategory.SPOOFING,
            description="JWT token theft and replay",
            attack_scenario="Attacker steals JWT from local storage via XSS",
            impact="High - Full account takeover",
            likelihood="Medium - Requires XSS vulnerability",
            mitigation="Use httpOnly cookies, implement token rotation",
            nist_control="IA-5(1) - Password-based authentication"
        )
    ]
)
```

### Attack Trees

#### Building Attack Trees

```
Goal: Gain Unauthorized Access to Admin Panel
│
├─── AND [Bypass Authentication]
│    ├─── OR [Steal Credentials]
│    │    ├─── Phishing attack
│    │    ├─── Credential stuffing
│    │    └─── Keylogger malware
│    └─── OR [Exploit Auth Vulnerability]
│         ├─── SQL injection in login
│         ├─── Session fixation
│         └─── JWT signature bypass
│
├─── AND [Exploit Authorization Flaw]
│    ├─── OR [Privilege Escalation]
│    │    ├─── IDOR vulnerability
│    │    ├─── Mass assignment
│    │    └─── Role confusion
│    └─── Direct URL access
│
└─── OR [Compromise Admin Account]
     ├─── Social engineering
     ├─── Insider threat
     └─── Weak password policy
```

#### Attack Tree Template

```yaml
attack_tree:
  goal: "Primary attack objective"
  attack_id: "ATK-001"
  
  root_node:
    type: "AND" / "OR"
    description: "Attack step description"
    
    children:
      - id: "ATK-001-1"
        type: "OR"
        description: "Sub-attack vector"
        probability: "High" / "Medium" / "Low"
        impact: "Critical" / "High" / "Medium" / "Low"
        cost_to_attacker: "Low" / "Medium" / "High"
        detection_difficulty: "Easy" / "Medium" / "Hard"
        
        mitigations:
          - control: "Implement MFA"
            effectiveness: "High"
            nist_control: "IA-2(1)"
          - control: "Rate limiting on login"
            effectiveness: "Medium"
            nist_control: "AC-7"
            
        children:
          - id: "ATK-001-1-1"
            type: "LEAF"
            description: "Specific attack technique"
            prerequisites: ["Network access", "Valid username"]
            tools: ["Hydra", "Burp Suite"]
```

### Data Flow Diagrams (DFD)

#### DFD Notation

```
Components:
  [Process]     = Rounded rectangle (transforms data)
  ||Data Store||  = Parallel lines (stores data)
  (External)    = Rectangle (external entity)
  ─────>        = Data flow arrow
  ═══>          = Privileged/trusted data flow
  - - - >       = Out-of-scope flow
  ╔════╗        = Trust boundary
```

#### Example DFD: Web Application

```
Trust Boundary: Internet
╔═══════════════════════════════════════════════╗
║                                               ║
║  (User) ──1. HTTPS Request──> [Web Server]   ║
║              └──2. Query──> ||Database||      ║
║                             ||           ||   ║
║  (Admin) ══3. Admin API══> [Admin Panel]     ║
║              └──4. Commands──> [Backend]      ║
║                                 │             ║
║                                 │             ║
║                                 5. Logs       ║
║                                 ↓             ║
║                          ||Log Storage||      ║
╚═══════════════════════════════════════════════╝
   │
   6. External Auth
   ↓
(OAuth Provider)
```

#### DFD Analysis Checklist

```markdown
For each data flow:
- [ ] What data is transmitted?
- [ ] Is it encrypted in transit?
- [ ] Does it cross trust boundaries?
- [ ] What authentication is required?
- [ ] What validation occurs?
- [ ] Is it logged/audited?

For each process:
- [ ] What privilege level does it run at?
- [ ] What inputs does it accept?
- [ ] What outputs does it produce?
- [ ] What data stores does it access?
- [ ] What external services does it call?

For each data store:
- [ ] What sensitivity level is the data?
- [ ] Is it encrypted at rest?
- [ ] Who has access?
- [ ] Is access logged?
- [ ] What is the backup/recovery strategy?
```

### Trust Boundaries

#### Identifying Trust Boundaries

```yaml
trust_boundaries:
  internet_dmz:
    description: "Public internet to DMZ"
    crossing_points:
      - "Load balancer ingress"
      - "Web server endpoints"
    required_controls:
      - "TLS 1.3 encryption"
      - "Web application firewall"
      - "DDoS protection"
      - "Input validation"
    nist_controls: ["SC-8", "SC-5", "SI-10"]
    
  dmz_internal:
    description: "DMZ to internal network"
    crossing_points:
      - "Application server connections"
      - "Database connections"
    required_controls:
      - "Service authentication"
      - "Network segmentation"
      - "Least privilege access"
      - "Encrypted connections"
    nist_controls: ["AC-3", "SC-7", "IA-2"]
    
  application_database:
    description: "Application tier to data tier"
    crossing_points:
      - "Database queries"
      - "Stored procedure calls"
    required_controls:
      - "Parameterized queries"
      - "Database authentication"
      - "Connection pooling with auth"
      - "Query logging"
    nist_controls: ["SI-10", "IA-2", "AU-2"]
```

#### Boundary Crossing Analysis

```python
# boundary_analyzer.py

class TrustBoundary:
    def __init__(self, name, trust_level):
        self.name = name
        self.trust_level = trust_level  # 0-10, 0=untrusted
        
class BoundaryCrossing:
    def __init__(self, from_boundary, to_boundary, data_flow):
        self.from_boundary = from_boundary
        self.to_boundary = to_boundary
        self.data_flow = data_flow
        self.threats = []
        
    def analyze_threats(self):
        """Identify threats when crossing trust boundaries."""
        trust_decrease = self.from_boundary.trust_level - self.to_boundary.trust_level
        
        if trust_decrease > 0:
            # Data flowing to less trusted zone
            self.threats.append({
                'category': 'Information Disclosure',
                'description': f'Sensitive data exposed to {self.to_boundary.name}',
                'severity': 'High' if trust_decrease > 5 else 'Medium'
            })
            
        if trust_decrease < 0:
            # Data flowing from less trusted zone
            self.threats.extend([
                {
                    'category': 'Tampering',
                    'description': f'Unvalidated data from {self.from_boundary.name}',
                    'severity': 'High'
                },
                {
                    'category': 'Spoofing',
                    'description': f'Unauthenticated source in {self.from_boundary.name}',
                    'severity': 'High' if abs(trust_decrease) > 5 else 'Medium'
                }
            ])
            
        return self.threats

# Example
internet = TrustBoundary("Internet", 0)
dmz = TrustBoundary("DMZ", 5)
internal = TrustBoundary("Internal Network", 8)

crossing = BoundaryCrossing(
    from_boundary=internet,
    to_boundary=dmz,
    data_flow="User login request"
)

threats = crossing.analyze_threats()
```

### Threat Prioritization (DREAD)

#### DREAD Scoring System

```yaml
dread_scoring:
  damage_potential:
    0: "No damage"
    5: "Individual user data compromised"
    10: "Complete system compromise, data destruction"
    
  reproducibility:
    0: "Nearly impossible"
    5: "Requires specific conditions"
    10: "Trivial to reproduce"
    
  exploitability:
    0: "Requires expert, custom tools"
    5: "Skilled attacker with available tools"
    10: "Unskilled attacker, browser/publicly available"
    
  affected_users:
    0: "No users affected"
    5: "Some users affected"
    10: "All users affected"
    
  discoverability:
    0: "Hidden, requires source code"
    5: "Requires scanning/tool use"
    10: "Obvious, publicly known"

# DREAD Score = (D + R + E + A + D) / 5
# Priority: 0-3.9=Low, 4-6.9=Medium, 7-10=High
```

#### Threat Prioritization Example

```python
# dread_calculator.py

from dataclasses import dataclass

@dataclass
class DREADScore:
    damage: int  # 0-10
    reproducibility: int
    exploitability: int
    affected_users: int
    discoverability: int
    
    def calculate(self) -> float:
        return (
            self.damage + 
            self.reproducibility + 
            self.exploitability + 
            self.affected_users + 
            self.discoverability
        ) / 5
    
    def priority(self) -> str:
        score = self.calculate()
        if score >= 7:
            return "Critical"
        elif score >= 4:
            return "High"
        elif score >= 2:
            return "Medium"
        else:
            return "Low"

# Example: SQL Injection in login form
sql_injection = DREADScore(
    damage=10,              # Full database access
    reproducibility=10,     # Easy to reproduce
    exploitability=8,       # Requires moderate skill
    affected_users=10,      # All users affected
    discoverability=7       # Findable with automated scanners
)

print(f"DREAD Score: {sql_injection.calculate()}")  # 9.0
print(f"Priority: {sql_injection.priority()}")      # Critical
```

### Mitigation Strategies

#### Mitigation Pattern Catalog

```yaml
spoofing_mitigations:
  - pattern: "Strong Authentication"
    techniques:
      - Multi-factor authentication (MFA)
      - Certificate-based authentication
      - Biometric authentication
    nist_controls: ["IA-2(1)", "IA-2(2)"]
    
  - pattern: "Session Management"
    techniques:
      - Secure session tokens
      - Token rotation
      - Session timeout
    nist_controls: ["SC-23", "AC-12"]

tampering_mitigations:
  - pattern: "Data Integrity"
    techniques:
      - Digital signatures
      - HMAC validation
      - Cryptographic hashing
    nist_controls: ["SC-8(1)", "SI-7"]
    
  - pattern: "Input Validation"
    techniques:
      - Whitelist validation
      - Parameterized queries
      - Output encoding
    nist_controls: ["SI-10"]

repudiation_mitigations:
  - pattern: "Audit Logging"
    techniques:
      - Comprehensive logging
      - Log integrity protection
      - Time synchronization
    nist_controls: ["AU-2", "AU-9", "AU-8"]
    
information_disclosure_mitigations:
  - pattern: "Data Protection"
    techniques:
      - Encryption at rest
      - Encryption in transit
      - Data classification
      - Secure key management
    nist_controls: ["SC-28", "SC-8", "SC-12"]
    
  - pattern: "Access Control"
    techniques:
      - Least privilege
      - Role-based access control
      - Data loss prevention
    nist_controls: ["AC-3", "AC-6"]

denial_of_service_mitigations:
  - pattern: "Rate Limiting"
    techniques:
      - Request throttling
      - Resource quotas
      - Circuit breakers
    nist_controls: ["SC-5"]
    
  - pattern: "Resilience"
    techniques:
      - Load balancing
      - Auto-scaling
      - DDoS protection
    nist_controls: ["SC-5", "SC-6"]

elevation_of_privilege_mitigations:
  - pattern: "Authorization"
    techniques:
      - Principle of least privilege
      - Privilege separation
      - Secure defaults
    nist_controls: ["AC-6", "AC-3"]
    
  - pattern: "Validation"
    techniques:
      - Authorization checks
      - Path traversal prevention
      - Secure file handling
    nist_controls: ["AC-3", "SI-10"]
```

### PASTA Methodology

#### Process for Attack Simulation and Threat Analysis

```yaml
stage_1_define_objectives:
  description: "Define business objectives and security requirements"
  activities:
    - Identify business assets
    - Define security objectives
    - Establish risk tolerance
    - Document compliance requirements
  deliverables:
    - Business impact analysis
    - Security objectives document
    
stage_2_define_technical_scope:
  description: "Define technical scope of analysis"
  activities:
    - Identify system boundaries
    - Document architecture
    - List technologies and dependencies
    - Map data flows
  deliverables:
    - System architecture diagram
    - Technology inventory
    - Data flow diagrams
    
stage_3_application_decomposition:
  description: "Decompose application into components"
  activities:
    - Identify entry points
    - Map trust boundaries
    - Document interfaces
    - List actors and use cases
  deliverables:
    - Component diagram
    - Trust boundary map
    - Actor-use case matrix
    
stage_4_threat_analysis:
  description: "Analyze threats using intelligence"
  activities:
    - Review threat intelligence
    - Apply STRIDE methodology
    - Build attack trees
    - Map to MITRE ATT&CK
  deliverables:
    - Threat intelligence report
    - STRIDE analysis matrix
    - Attack trees
    
stage_5_vulnerability_analysis:
  description: "Identify vulnerabilities and weaknesses"
  activities:
    - Review security controls
    - Identify vulnerability gaps
    - Assess attack surface
    - Map to CWE/CVE
  deliverables:
    - Vulnerability assessment report
    - Control gap analysis (NIST RA-5)
    
stage_6_attack_modeling:
  description: "Model attack scenarios"
  activities:
    - Develop attack scenarios
    - Simulate attack paths
    - Assess exploitability
    - Estimate impact
  deliverables:
    - Attack scenario documentation
    - Attack path diagrams
    - Exploitability assessment
    
stage_7_risk_analysis:
  description: "Analyze and prioritize risks"
  activities:
    - Calculate risk scores
    - Prioritize threats
    - Recommend mitigations
    - Create remediation roadmap
  deliverables:
    - Risk assessment report (NIST RA-3)
    - Prioritized threat list
    - Mitigation recommendations
    - Security roadmap
```

### Tools

#### Microsoft Threat Modeling Tool

```yaml
microsoft_tmt:
  description: "Official Microsoft tool for STRIDE-based threat modeling"
  features:
    - Built-in DFD editor
    - Automatic STRIDE threat generation
    - Threat templates library
    - Report generation
  usage:
    - Create DFD of system
    - Tool auto-generates threats per element
    - Review and customize threats
    - Add mitigations
    - Export reports
  download: "https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling"
  
owasp_threat_dragon:
  description: "Open-source threat modeling tool"
  features:
    - Web-based or desktop
    - STRIDE methodology support
    - Diagramming interface
    - Threat generation
    - Export to JSON/PDF
  usage:
    - Draw data flow diagram
    - Mark trust boundaries
    - Generate threats from template
    - Document mitigations
  repository: "https://github.com/OWASP/threat-dragon"
  
pytm:
  description: "Python-based threat modeling framework"
  features:
    - Code-as-threat-model
    - Automatic DFD generation
    - STRIDE threat rules
    - PlantUML/Graphviz output
  example: |
    from pytm import TM, Server, Datastore, Dataflow
    
    tm = TM("Web App Threat Model")
    web = Server("Web Server")
    db = Datastore("Database")
    flow = Dataflow(web, db, "SQL Query")
    tm.process()  # Generates threats
  repository: "https://github.com/izar/pytm"
```

#### Threat Modeling Workflow

```bash
# 1. Install OWASP Threat Dragon
npm install -g threat-dragon

# 2. Create new threat model
threat-dragon --new my-app-threats

# 3. Use pytm for code-based modeling
pip install pytm
python my_threat_model.py

# 4. Generate reports
python -m pytm.tm --report my_threat_model.py > threats.md

# 5. Integrate with CI/CD
cat > .github/workflows/threat-modeling.yml << 'EOF'
name: Threat Model Validation
on: [push]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install pytm
        run: pip install pytm
      - name: Generate threat model
        run: python threat_model.py
      - name: Check for new threats
        run: |
          if grep -q "Unmitigated" threats.md; then
            echo "Unmitigated threats found!"
            exit 1
          fi
EOF
```

### NIST Integration

#### NIST RA-3: Risk Assessment

```yaml
nist_ra_3:
  control: "RA-3: Risk Assessment"
  description: "Conduct risk assessments at regular intervals"
  
  threat_modeling_activities:
    - Identify threats to organizational operations
    - Identify threats to assets
    - Identify threats to individuals
    - Assess likelihood of threat occurrence
    - Assess impact of threat realization
    - Determine risk (likelihood × impact)
    - Document risk assessment results
    
  integration:
    - Use threat models as input to risk assessment
    - Map STRIDE threats to organizational risks
    - Include threat models in risk register
    - Update threat models when architecture changes
    
  frequency:
    - Initial system authorization
    - When significant changes occur
    - Annually (at minimum)
    - When new threats are identified
```

#### NIST RA-5: Vulnerability Monitoring and Scanning

```yaml
nist_ra_5:
  control: "RA-5: Vulnerability Monitoring and Scanning"
  description: "Monitor and scan for vulnerabilities"
  
  threat_modeling_integration:
    - Use threat models to focus scanning efforts
    - Prioritize scanning based on threat analysis
    - Map discovered vulnerabilities to threats
    - Validate threat model assumptions
    - Update threat models with new vulnerabilities
    
  process:
    1_threat_informed_scanning:
      - Review threat model for attack surfaces
      - Configure scanners for identified entry points
      - Focus on high-risk components
      
    2_vulnerability_analysis:
      - Map CVEs to threat model components
      - Assess exploitability in context
      - Update DREAD scores with real data
      
    3_remediation_prioritization:
      - Use threat model to prioritize fixes
      - Address threats with highest risk first
      - Validate mitigations against threat scenarios
      
    4_continuous_monitoring:
      - Automate vulnerability scanning
      - Integrate with CI/CD pipeline
      - Alert on new threats matching model
```

### Practical Examples

#### Example 1: Authentication Service Threat Model

```yaml
system: "User Authentication Service"
scope: "Login, registration, password reset"

components:
  - name: "Login API"
    type: process
    threats:
      - id: "THREAT-001"
        stride: Spoofing
        description: "Attacker uses stolen credentials"
        scenario: |
          1. User credentials leaked via phishing
          2. Attacker uses credentials to authenticate
          3. Gains access to user account
        dread:
          damage: 8
          reproducibility: 10
          exploitability: 9
          affected_users: 5
          discoverability: 8
          score: 8.0
          priority: Critical
        mitigations:
          - control: "Implement MFA"
            nist: "IA-2(1)"
            status: "Planned"
          - control: "Anomaly detection on login"
            nist: "SI-4"
            status: "Not Started"
            
  - name: "Password Reset Flow"
    type: process
    threats:
      - id: "THREAT-002"
        stride: Elevation of Privilege
        description: "Account takeover via password reset"
        scenario: |
          1. Attacker requests password reset for victim
          2. Intercepts reset token (weak token, email compromise)
          3. Resets victim's password
          4. Takes over account
        dread:
          damage: 9
          reproducibility: 5
          exploitability: 6
          affected_users: 5
          discoverability: 6
          score: 6.2
          priority: High
        mitigations:
          - control: "Short-lived reset tokens (15 min)"
            nist: "IA-5(1)"
            status: "Implemented"
          - control: "Require current password or additional verification"
            nist: "IA-2(1)"
            status: "Planned"
          - control: "Notify user of password reset request"
            nist: "AU-2"
            status: "Implemented"
```

#### Example 2: API Gateway Threat Model

```yaml
system: "API Gateway"
scope: "External API access, rate limiting, authentication"

trust_boundaries:
  - name: "Internet → DMZ"
    controls: ["TLS", "WAF", "DDoS Protection"]
  - name: "DMZ → Internal"
    controls: ["Service Authentication", "Network Segmentation"]

data_flows:
  - id: "DF-001"
    from: "Mobile App"
    to: "API Gateway"
    protocol: "HTTPS"
    data: "API requests with JWT"
    threats:
      - id: "THREAT-003"
        stride: Tampering
        description: "Request parameter manipulation"
        attack_tree: |
          Goal: Manipulate API request
          └─ OR
             ├─ Modify request body
             │  └─ Change product IDs in order
             ├─ Modify headers
             │  └─ Change Content-Type to bypass validation
             └─ Replay old requests
                └─ Resubmit successful transaction
        mitigation:
          - "Request signing with HMAC"
          - "Timestamp validation"
          - "Idempotency keys"
        nist: ["SC-8(1)", "SI-10"]
```

---

## Level 3: Deep Dive Resources

### Advanced Topics

- **Threat Intelligence Integration**: MITRE ATT&CK mapping, threat feeds
- **Automated Threat Modeling**: CI/CD integration, continuous threat modeling
- **Threat Model Maintenance**: Version control, change management
- **Quantitative Risk Analysis**: Monte Carlo simulations, risk metrics
- **Threat Modeling at Scale**: Enterprise architecture, microservices
- **Supply Chain Threat Modeling**: Third-party components, dependencies

### Tools & Frameworks

- **Commercial**: IriusRisk, ThreatModeler, SD Elements
- **Open Source**: OWASP Threat Dragon, PyTM, Threagile
- **Cloud-Native**: AWS Threat Composer, Azure Threat Modeling
- **Standards**: NIST SP 800-30 (Risk Assessment), ISO 27005

### References

- **OWASP Threat Modeling**: <https://owasp.org/www-community/Threat_Modeling>
- **Microsoft SDL**: <https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling>
- **NIST SP 800-30 Rev 1**: Risk Assessment Guide
- **NIST SP 800-154**: Data Integrity Guide
- **Adam Shostack's "Threat Modeling" Book**: Industry standard reference
- **MITRE ATT&CK**: <https://attack.mitre.org>

### Community

- **OWASP Threat Modeling Project**: Resources, templates, guidance
- **Threat Modeling Slack**: Community discussions
- **Security BSides**: Local threat modeling workshops

---

**Next Steps:**
1. Review bundled templates in `templates/`
2. Use `stride-template.md` for your first threat model
3. Generate DFDs with `data-flow-diagram.md`
4. Run `threat-report-generator.py` to create reports
5. Study real-world examples in `resources/stride-examples.md`

**Related Skills:** [security-testing] [secure-coding] [vulnerability-management]
