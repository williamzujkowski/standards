# Zero-Trust Architecture Diagram and Explanation

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Zero-Trust Architecture                          │
└─────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────┐
                              │  User/Device │
                              └───────┬──────┘
                                      │
                         ┌────────────▼────────────┐
                         │ Identity-Aware Proxy    │
                         │  (BeyondCorp/IAP)       │
                         │  • Identity verification │
                         │  • Device trust check    │
                         │  • Context evaluation    │
                         └────────────┬────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        │        Policy Decision Point (PDP)                       │
        │        ┌─────────────────────────────────┐               │
        │        │  Trust Algorithm Engine          │               │
        │        │  • Risk calculation              │               │
        │        │  • Context analysis              │               │
        │        │  • Attribute aggregation         │               │
        │        └─────────┬───────────────────────┘               │
        │                  │                                        │
        │     ┌────────────┼────────────┐                         │
        │     ▼            ▼            ▼                         │
        │  ┌──────┐   ┌────────┐   ┌──────────┐                 │
        │  │ User │   │ Device │   │ Resource │                 │
        │  │ DB   │   │ Posture│   │ Policies │                 │
        │  └──────┘   └────────┘   └──────────┘                 │
        └──────────────────┬──────────────────────────────────────┘
                           │
                           │ Authorization Decision
                           │
        ┌──────────────────▼──────────────────────────────────────┐
        │        Policy Enforcement Point (PEP)                    │
        │        ┌────────────────────────────────┐               │
        │        │  Envoy Proxy / API Gateway     │               │
        │        │  • mTLS enforcement            │               │
        │        │  • Token validation            │               │
        │        │  • Traffic inspection          │               │
        │        └────────────┬───────────────────┘               │
        └─────────────────────┼───────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
       ┌──────────┐    ┌──────────┐    ┌──────────┐
       │ Service A│    │ Service B│    │ Service C│
       │          │    │          │    │          │
       │ ┌──────┐ │    │ ┌──────┐ │    │ ┌──────┐ │
       │ │SPIFFE│ │    │ │SPIFFE│ │    │ │SPIFFE│ │
       │ │  ID  │ │    │ │  ID  │ │    │ │  ID  │ │
       │ └──────┘ │    │ └──────┘ │    │ └──────┘ │
       │  mTLS ───┼────┼──► mTLS  │    │   mTLS   │
       └──────────┘    └──────────┘    └──────────┘
              │               │               │
              └───────────────┼───────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   Service Mesh     │
                    │   Control Plane    │
                    │   • Identity mgmt  │
                    │   • Policy sync    │
                    │   • Certificate CA │
                    └────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   Observability    │
                    │   • Metrics        │
                    │   • Logs           │
                    │   • Traces         │
                    │   • Alerts         │
                    └────────────────────┘
```

## Component Responsibilities

### 1. Identity-Aware Proxy (IAP)

**Function:** First point of contact for all requests, performs initial identity and device verification.

**Key Features:**

- User authentication (MFA, SSO, certificates)
- Device trust evaluation (managed, encrypted, compliant)
- Context extraction (location, time, IP reputation)
- Session management

**Technologies:**

- Google Cloud IAP
- Cloudflare Access
- Zscaler Private Access
- Custom Envoy + OIDC

### 2. Policy Decision Point (PDP)

**Function:** Evaluates access requests against policies and context to make authorization decisions.

**Inputs:**

- User identity and attributes
- Device health and compliance
- Resource sensitivity and requirements
- Network context (location, IP)
- Behavioral analytics (anomalies, patterns)

**Output:**

- ALLOW/DENY decision
- Session duration
- Additional authentication requirements
- Continuous verification interval

**Technologies:**

- Open Policy Agent (OPA)
- HashiCorp Sentinel
- AWS Verified Permissions
- Custom Trust Algorithm

### 3. Policy Enforcement Point (PEP)

**Function:** Enforces authorization decisions by controlling access to resources.

**Responsibilities:**

- Establish secure communication channels (mTLS)
- Validate authentication tokens
- Inspect and filter traffic
- Terminate unauthorized connections
- Collect telemetry

**Technologies:**

- Envoy Proxy
- Istio/Linkerd service mesh
- API Gateway (Kong, Tyk, AWS API Gateway)
- Cloud Load Balancers with WAF

### 4. Workload Identity (SPIFFE/SPIRE)

**Function:** Provides automatic, cryptographic identities for workloads.

**Features:**

- Automatic certificate issuance and rotation
- Workload attestation (proof of identity)
- Cross-platform identity framework
- Short-lived credentials (default 1 hour)

**Benefits:**

- No secrets in config files
- Strong authentication without passwords
- Platform-agnostic identity
- Audit trail of identity issuance

### 5. Service Mesh

**Function:** Handles service-to-service communication with built-in security.

**Capabilities:**

- Automatic mTLS between services
- Traffic encryption in transit
- Fine-grained authorization policies
- Traffic management (routing, retries, timeouts)
- Observability (metrics, logs, traces)

**Implementations:**

- Istio (feature-rich, complex)
- Linkerd (lightweight, simple)
- Consul Connect (HashiCorp ecosystem)
- AWS App Mesh (AWS-native)

### 6. Observability Stack

**Function:** Continuous monitoring and anomaly detection.

**Components:**

- **Metrics:** Prometheus, Grafana
- **Logging:** Fluentd, Elasticsearch, Loki
- **Tracing:** Jaeger, Zipkin, Tempo
- **SIEM:** Splunk, Elastic Security
- **Alerting:** Alertmanager, PagerDuty

## Data Flow Example

### Scenario: User accesses internal API

```
1. User Request
   ├─> HTTPS request to api.example.com
   └─> Includes authentication token (JWT)

2. Identity-Aware Proxy
   ├─> Validates JWT signature
   ├─> Checks user MFA status
   ├─> Evaluates device compliance
   ├─> Extracts context (IP, location, time)
   └─> Forwards to PDP with enriched context

3. Policy Decision Point (OPA)
   ├─> Queries user database (roles, permissions)
   ├─> Checks device posture (last scan, OS version)
   ├─> Calculates risk score (Trust Algorithm)
   │   ├─> User score: 85/100 (good history)
   │   ├─> Device score: 70/100 (managed but old OS)
   │   ├─> Network score: 90/100 (known location)
   │   ├─> Behavior score: 60/100 (unusual time)
   │   └─> Overall: 76/100 → ALLOW with conditions
   ├─> Determines session duration: 1 hour
   ├─> Requires re-verification every 5 minutes
   └─> Sends ALLOW decision to PEP

4. Policy Enforcement Point (Envoy)
   ├─> Receives ALLOW decision
   ├─> Establishes mTLS connection to backend
   ├─> Injects headers:
   │   ├─> X-User-ID: user-123
   │   ├─> X-Trust-Score: 76
   │   └─> X-Session-TTL: 3600
   ├─> Forwards request to backend service
   └─> Monitors connection (logs, metrics)

5. Backend Service
   ├─> Validates SPIFFE identity of caller
   ├─> Processes request
   ├─> Returns response
   └─> Logs access with user context

6. Continuous Verification (every 5 minutes)
   ├─> PEP queries PDP for session validity
   ├─> PDP re-evaluates context
   ├─> If risk increases → terminate session
   └─> If risk acceptable → extend session
```

## Network Segmentation

```
┌────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                       │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Namespace: ingress                                   │ │
│  │  ┌────────────────┐                                   │ │
│  │  │ Ingress Gateway│                                   │ │
│  │  │ (mTLS + WAF)   │                                   │ │
│  │  └───────┬────────┘                                   │ │
│  └──────────┼───────────────────────────────────────────┘ │
│             │                                              │
│  ┌──────────▼───────────────────────────────────────────┐ │
│  │  Namespace: production                                │ │
│  │  NetworkPolicy: deny-all (default)                    │ │
│  │                                                        │ │
│  │  ┌────────────┐      ┌────────────┐                  │ │
│  │  │  Frontend  │──────▶│  Backend   │                  │ │
│  │  │  (public)  │      │    API     │                  │ │
│  │  └────────────┘      └──────┬─────┘                  │ │
│  │                             │                         │ │
│  │                      ┌──────▼────────┐               │ │
│  │                      │   Database    │               │ │
│  │                      │  (isolated)   │               │ │
│  │                      └───────────────┘               │ │
│  │                                                        │ │
│  │  Allowed traffic:                                     │ │
│  │  ✓ Frontend → Backend:8080 (GET, POST)              │ │
│  │  ✓ Backend → Database:5432                           │ │
│  │  ✗ Frontend → Database (DENIED)                      │ │
│  │  ✗ Any → Any (DENIED)                                │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Namespace: monitoring                              │ │
│  │  NetworkPolicy: allow-scraping                      │ │
│  │                                                      │ │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐       │ │
│  │  │Prometheus│◀──│ Grafana  │◀──│ Exporter │       │ │
│  │  └──────────┘   └──────────┘   └──────────┘       │ │
│  │                                                      │ │
│  │  Can scrape metrics from all namespaces             │ │
│  │  on specific ports (9090, 9091)                     │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Trust Boundaries

Zero-trust architecture eliminates the concept of trusted networks but establishes trust boundaries at different levels:

### Level 1: Identity Trust

- Strong authentication (certificates, MFA)
- Identity lifecycle management
- Attribute-based trust (roles, claims)

### Level 2: Device Trust

- Device registration and attestation
- Health and compliance checks
- Encryption and security posture

### Level 3: Network Trust

- No implicit trust
- Encrypted communication (mTLS, TLS 1.3)
- Microsegmentation with NetworkPolicies

### Level 4: Application Trust

- Workload identity (SPIFFE)
- Least privilege access
- Runtime security monitoring

### Level 5: Data Trust

- Data classification and labeling
- Encryption at rest and in transit
- Access logging and auditing

## Security Controls Mapping

| NIST Control | Zero-Trust Implementation |
|--------------|---------------------------|
| AC-4: Information Flow Enforcement | NetworkPolicies, Service mesh authorization |
| SC-7: Boundary Protection | Microsegmentation, PEP at every boundary |
| SC-8: Transmission Confidentiality | mTLS, TLS 1.3, encrypted channels |
| IA-2: Identification and Authentication | SPIFFE, workload identity, mTLS |
| AC-3: Access Enforcement | OPA policies, authorization policies |
| AU-2: Audit Events | Comprehensive logging, SIEM integration |
| SI-4: Information System Monitoring | Continuous monitoring, anomaly detection |

## Benefits of Zero-Trust

1. **Reduced Attack Surface:** Microsegmentation limits lateral movement
2. **Strong Authentication:** Every request verified with cryptographic identity
3. **Least Privilege:** Default deny, explicit allow
4. **Visibility:** All traffic logged and monitored
5. **Adaptability:** Context-aware policies adjust to risk
6. **Defense in Depth:** Multiple layers of security controls
7. **Cloud-Native:** Works across on-premises, cloud, and hybrid environments

## Common Pitfalls

1. **Incomplete Coverage:** Not applying zero-trust to all resources
2. **Static Policies:** Not adapting to changing risk
3. **Poor Visibility:** Insufficient logging and monitoring
4. **Complex Operations:** Over-complicating initial implementation
5. **Certificate Management:** Not automating certificate lifecycle
6. **Legacy Systems:** Difficulty integrating legacy applications
7. **User Experience:** Too restrictive policies frustrating users

## Migration Strategy

### Phase 1: Visibility (Weeks 1-4)

- Deploy service mesh in permissive mode
- Enable comprehensive logging
- Map all service dependencies
- Identify high-value assets

### Phase 2: Identity (Weeks 5-8)

- Deploy SPIFFE/SPIRE
- Enable workload identities
- Implement mTLS in permissive mode
- Validate certificate issuance

### Phase 3: Segmentation (Weeks 9-12)

- Deploy NetworkPolicies in audit mode
- Create microsegmentation plan
- Test connectivity with policies
- Gradually enforce policies

### Phase 4: Authorization (Weeks 13-16)

- Deploy OPA/policy engine
- Define authorization policies
- Implement PEP at ingress points
- Enable policy enforcement

### Phase 5: Continuous Improvement (Ongoing)

- Monitor and tune policies
- Respond to anomalies
- Update trust algorithms
- Expand coverage to new services
