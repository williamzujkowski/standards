# Data Flow Diagram (DFD) Template

## DFD Notation Guide

### Symbols

```
┌─────────────┐
│   Process   │  = Rounded rectangle (transforms data)
└─────────────┘

║            ║
║ Data Store ║  = Parallel lines (stores data)
║            ║

┌─────────────┐
│ External    │  = Rectangle (external entity)
│ Entity      │
└─────────────┘

─────────────>  = Data flow (arrow shows direction)

═══════════>    = Trusted/privileged data flow

- - - - - ->    = Out-of-scope data flow

╔══════════════╗
║ Trust        ║ = Trust boundary (encloses components)
║ Boundary     ║
╚══════════════╝
```

### Example DFD

```
Trust Boundary: Internet
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║  ┌──────────┐                                            ║
║  │  User    │                                            ║
║  │ (Mobile) │                                            ║
║  └────┬─────┘                                            ║
║       │                                                   ║
║       │ 1. HTTPS Request                                 ║
║       │ (Credentials)                                    ║
║       ↓                                                   ║
║  ┌─────────────┐                                         ║
║  │   API       │ 2. SQL Query                            ║
║  │  Gateway    │───────────────────>║                    ║
║  └──────┬──────┘                    ║  User Database ║   ║
║         │                           ║                ║   ║
║         │ 3. JWT                    ╚════════════════╝   ║
║         │ Validation                                     ║
║         ↓                                                 ║
║  ┌─────────────┐                                         ║
║  │   Auth      │ 4. Session Lookup                       ║
║  │  Service    │───────────────────>║                    ║
║  └─────────────┘                    ║ Session Store  ║   ║
║                                     ║                ║   ║
╚═══════════════════════════════════════════════════════════╝
         │
         │ 5. External OAuth
         │ (Out of scope)
         ↓
  ┌─────────────┐
  │   OAuth     │
  │  Provider   │
  └─────────────┘
```

## DFD Template for Your System

### Level 0: Context Diagram

```
[High-level view showing system and external entities]

Example:
┌──────────┐
│  Users   │──────> [Your System] <──────┌─────────────┐
└──────────┘                              │  External   │
                                          │  Services   │
                                          └─────────────┘
```

### Level 1: System Overview

```
[Main components and data flows]

Trust Boundary: ______________
╔════════════════════════════════════════════════════════╗
║                                                        ║
║  ┌──────────┐           ┌─────────────┐               ║
║  │ Component│ ───────> │  Component  │               ║
║  │    A     │   Data   │      B      │               ║
║  └──────────┘           └─────────────┘               ║
║       │                                                ║
║       │                                                ║
║       ↓                                                ║
║  ║              ║                                      ║
║  ║  Data Store  ║                                      ║
║  ║              ║                                      ║
╚════════════════════════════════════════════════════════╝
```

### Level 2: Detailed Component View

```
[Detailed view of specific component with all interactions]
```

## Data Flow Inventory

| Flow ID | Source | Destination | Data Type | Protocol | Encryption | Authentication | Trust Boundary Crossing |
|---------|--------|-------------|-----------|----------|------------|----------------|------------------------|
| DF-001 | _[Source]_ | _[Dest]_ | _[Data]_ | _[HTTP/TCP/etc]_ | _[TLS/None]_ | _[JWT/API Key/None]_ | _[Yes/No]_ |
| DF-002 |  |  |  |  |  |  |  |

## Process Inventory

| Process ID | Name | Description | Trust Level | Input Flows | Output Flows | Privilege Level |
|------------|------|-------------|-------------|-------------|--------------|-----------------|
| P-001 | _[Name]_ | _[Purpose]_ | _[0-10]_ | _[DF-IDs]_ | _[DF-IDs]_ | _[User/Admin/System]_ |
| P-002 |  |  |  |  |  |  |

## Data Store Inventory

| Store ID | Name | Data Type | Sensitivity | Encryption at Rest | Access Control | Backup Strategy |
|----------|------|-----------|-------------|-------------------|----------------|-----------------|
| DS-001 | _[Name]_ | _[Type]_ | _[High/Med/Low]_ | _[Yes/No]_ | _[RBAC/ACL]_ | _[Daily/Hourly]_ |
| DS-002 |  |  |  |  |  |  |

## External Entity Inventory

| Entity ID | Name | Relationship | Trust Level | Authentication Method | Data Exchanged |
|-----------|------|--------------|-------------|----------------------|----------------|
| EE-001 | _[Name]_ | _[Customer/Partner/3rd Party]_ | _[0-10]_ | _[OAuth/API Key/None]_ | _[Data types]_ |
| EE-002 |  |  |  |  |  |

## Trust Boundaries

| Boundary ID | Name | Inside | Outside | Security Controls |
|-------------|------|--------|---------|-------------------|
| TB-001 | _[Name]_ | _[Components inside]_ | _[Components outside]_ | _[Firewall/WAF/etc]_ |
| TB-002 |  |  |  |  |

## DFD Analysis Checklist

### For Each Data Flow:

- [ ] Source and destination clearly identified
- [ ] Data classification documented
- [ ] Encryption in transit specified
- [ ] Authentication mechanism defined
- [ ] Trust boundary crossings marked
- [ ] Protocol and port documented
- [ ] Input validation requirements noted
- [ ] Logging/auditing requirements defined

### For Each Process:

- [ ] Function and purpose documented
- [ ] Privilege level identified
- [ ] Input sources listed
- [ ] Output destinations listed
- [ ] Authentication requirements defined
- [ ] Authorization checks specified
- [ ] Error handling documented
- [ ] Logging requirements defined

### For Each Data Store:

- [ ] Data sensitivity classified
- [ ] Encryption at rest specified
- [ ] Access control mechanism defined
- [ ] Backup and recovery strategy documented
- [ ] Data retention policy specified
- [ ] PII/sensitive data handling noted
- [ ] Access logging enabled
- [ ] Integrity protection specified

### For Each External Entity:

- [ ] Entity type identified (user/system/service)
- [ ] Trust level assigned
- [ ] Authentication method documented
- [ ] Authorization scope defined
- [ ] Data exchange protocol specified
- [ ] Rate limiting requirements noted
- [ ] Monitoring requirements defined

### For Each Trust Boundary:

- [ ] Boundary clearly marked on DFD
- [ ] Security controls at boundary documented
- [ ] All crossing points identified
- [ ] Authentication at boundary defined
- [ ] Encryption requirements specified
- [ ] Monitoring and logging enabled
- [ ] Firewall/WAF rules documented

## Common DFD Patterns

### 1. Web Application Pattern

```
╔═══ Internet ══════════════════════════════════════════╗
║                                                       ║
║  (Users) ──HTTPS──> [Load Balancer]                  ║
║                          │                            ║
║                          ↓                            ║
║                     [Web Server]                      ║
║                          │                            ║
╚══════════════════════════┼════════════════════════════╝
                           │
╔═══ DMZ ═══════════════════┼════════════════════════════╗
║                          ↓                            ║
║                   [Application Server]                ║
║                          │                            ║
╚══════════════════════════┼════════════════════════════╝
                           │
╔═══ Internal Network ═════┼════════════════════════════╗
║                          ↓                            ║
║                   ║              ║                    ║
║                   ║   Database   ║                    ║
║                   ║              ║                    ║
╚═══════════════════════════════════════════════════════╝
```

### 2. Microservices Pattern

```
╔═══ Service Mesh ══════════════════════════════════════╗
║                                                       ║
║  [API Gateway] ──mTLS──> [Auth Service]              ║
║         │                                             ║
║         ├──mTLS──> [User Service] ──> ||Users DB||   ║
║         │                                             ║
║         └──mTLS──> [Order Service] ──> ||Orders DB|| ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
```

### 3. Mobile App Pattern

```
╔═══ Mobile Device ═════════════════════════════════════╗
║                                                       ║
║  [Mobile App] ──HTTPS+Certificate Pinning──>         ║
║                                                       ║
╚═══════════════════════════┼═══════════════════════════╝
                            │
╔═══ Cloud Backend ═════════┼═══════════════════════════╗
║                           ↓                           ║
║                    [API Gateway]                      ║
║                           │                           ║
║                           ├──> [Push Notification]    ║
║                           │                           ║
║                           └──> [Backend Services]     ║
╚═══════════════════════════════════════════════════════╝
```

## Tips for Effective DFDs

1. **Start Simple**: Begin with Level 0 (context), then drill down
2. **Be Consistent**: Use notation consistently throughout
3. **Mark Trust Boundaries**: Clearly show where trust changes
4. **Label Data Flows**: Specify what data is flowing
5. **Show Authentication**: Indicate auth points clearly
6. **Number Elements**: Use IDs for reference in threat analysis
7. **Keep Updated**: Revise DFD when architecture changes
8. **Version Control**: Track DFD changes over time

## Next Steps

1. Create your DFD using this template
2. Review with architecture team for accuracy
3. Identify all trust boundary crossings
4. Use DFD as input to STRIDE analysis
5. Update DFD when threats are discovered
6. Maintain DFD in version control alongside code

---

**Related Templates:**
- `stride-template.md` - Use this DFD for STRIDE analysis
- `threat-scenario.md` - Map attack paths to DFD elements
