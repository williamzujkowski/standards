---
name: zero-trust-security
category: security
difficulty: advanced
estimated_time: "8-12 hours"
prerequisites:
  - Network security fundamentals
  - Container orchestration (Kubernetes)
  - PKI and certificate management
  - Identity and access management
nist_controls:
  - AC-4    # Information Flow Enforcement
  - SC-7    # Boundary Protection
  - SC-8    # Transmission Confidentiality and Integrity
related_skills:
  - secrets-management
  - secure-api-design
  - security-monitoring
version: "1.0.0"
---

# Zero-Trust Security

## Level 1: Quick Reference

### Core Principles

Zero-trust architecture operates on the principle: **"Never trust, always verify."** Unlike traditional perimeter-based security, zero-trust assumes breach and verifies every request regardless of origin.

**Fundamental Tenets:**

- No implicit trust based on network location
- Verify explicitly (authentication + authorization)
- Least privilege access (just-in-time, just-enough)
- Assume breach (limit blast radius, segment access)
- Inspect and log all traffic

### Common Zero-Trust Patterns

#### 1. Mutual TLS (mTLS)

```yaml
# Istio PeerAuthentication for strict mTLS
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
```

**When to use:** Service-to-service authentication, encrypted communication between microservices.

#### 2. Service Mesh

- **Istio/Linkerd:** Transparent mTLS, traffic encryption, identity management
- **Consul Connect:** Service identity and authorization
- **AWS App Mesh:** Cloud-native service mesh

**Key benefits:** Automatic encryption, fine-grained policies, observability.

#### 3. BeyondCorp Model

```yaml
# Identity-aware proxy configuration
apiVersion: v1
kind: Service
metadata:
  name: webapp
  annotations:
    cloud.google.com/neg: '{"ingress": true}'
    cloud.google.com/backend-config: '{"default": "beyondcorp-config"}'
spec:
  type: ClusterIP
  ports:
    - port: 8080
      targetPort: 8080
```

**Use case:** Remote access without VPN, identity-based access to applications.

### Essential Checklist

**Identity & Authentication:**

- [ ] Workload identities for all services (SPIFFE/SPIRE)
- [ ] mTLS enabled for service-to-service communication
- [ ] Strong authentication (MFA, certificates, tokens)
- [ ] Identity lifecycle management (rotation, revocation)

**Authorization:**

- [ ] Fine-grained access policies (attribute-based)
- [ ] Least privilege by default
- [ ] Just-in-time access provisioning
- [ ] Policy enforcement at every access point

**Network Security:**

- [ ] Microsegmentation (NetworkPolicies, security groups)
- [ ] Encrypted communication (TLS 1.3+)
- [ ] Traffic inspection and filtering
- [ ] No trust based on network location

**Monitoring & Verification:**

- [ ] Continuous monitoring of authentication events
- [ ] Anomaly detection on access patterns
- [ ] Centralized logging (who, what, when, where)
- [ ] Regular access reviews and audits

**Architecture:**

- [ ] Policy Decision Point (PDP) implemented
- [ ] Policy Enforcement Point (PEP) at critical paths
- [ ] Policy Administration Point (PAP) for management
- [ ] Data plane and control plane separation

### Quick Wins

1. **Enable mTLS in service mesh** (2-4 hours)
   - Deploy Istio/Linkerd
   - Configure strict mTLS mode
   - Verify with traffic inspection

2. **Implement Kubernetes NetworkPolicies** (1-2 hours)
   - Default deny all traffic
   - Explicit allow rules per service
   - Test connectivity

3. **Deploy workload identities** (3-4 hours)
   - Install SPIFFE/SPIRE
   - Configure workload attestation
   - Integrate with service mesh

---

## Level 2: Implementation Guide

### Zero-Trust Architecture Principles

Zero-trust architecture (ZTA) fundamentally reimagines security by eliminating implicit trust. Traditional castle-and-moat security assumes everything inside the perimeter is trustworthy, but ZTA treats every request as potentially hostile.

#### NIST 800-207 Zero Trust Tenets

1. **All data sources and computing services are considered resources**
   - Applications, services, databases, IoT devices, containers
   - Resources may be on-premises, cloud, edge, or hybrid

2. **All communication is secured regardless of network location**
   - Encrypt all traffic (mTLS, TLS 1.3)
   - No trust based on internal network position
   - Apply same security to internal and external traffic

3. **Access to resources is granted on a per-session basis**
   - Authentication and authorization for every request
   - Continuous verification throughout session
   - Short-lived credentials and tokens

4. **Access is determined by dynamic policy**
   - User identity, device health, behavior, risk score
   - Attribute-based access control (ABAC)
   - Context-aware decisions (time, location, sensitivity)

5. **Monitor and measure integrity and security posture**
   - Continuous monitoring of assets
   - Real-time threat detection
   - Security analytics and automation

6. **All resource authentication and authorization are dynamic and strictly enforced**
   - No static rules or permanent access
   - Adaptive policies based on risk
   - Fail-secure by default

7. **Collect as much information as possible about current state**
   - Asset inventory and behavior
   - Network traffic analysis
   - Security telemetry and logs

**NIST Controls:**

- **AC-4:** Information Flow Enforcement - Control information flow between security domains
- **SC-7:** Boundary Protection - Monitor and control communications at managed interfaces
- **SC-8:** Transmission Confidentiality and Integrity - Protect information during transmission

### Mutual TLS (mTLS) Implementation

Mutual TLS provides bidirectional authentication where both client and server verify each other's identity using certificates.

#### Certificate Management

```bash
# Generate root CA
openssl genrsa -out root-ca-key.pem 4096
openssl req -new -x509 -days 3650 -key root-ca-key.pem \
  -out root-ca.pem -subj "/CN=Service Mesh Root CA"

# Generate service certificate
openssl genrsa -out service-key.pem 2048
openssl req -new -key service-key.pem -out service.csr \
  -subj "/CN=my-service.production.svc.cluster.local"
openssl x509 -req -days 365 -in service.csr -CA root-ca.pem \
  -CAkey root-ca-key.pem -CAcreateserial -out service-cert.pem

# Create Kubernetes secret
kubectl create secret tls my-service-tls \
  --cert=service-cert.pem \
  --key=service-key.pem \
  -n production
```

#### Istio mTLS Configuration

```yaml
# Global strict mTLS enforcement
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT

---
# Namespace-specific mTLS with permissive mode for migration
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: PERMISSIVE  # Allow both mTLS and plaintext during migration

---
# Workload-specific mTLS override
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: legacy-service
  namespace: production
spec:
  selector:
    matchLabels:
      app: legacy-api
  mtls:
    mode: DISABLE
  portLevelMtls:
    8080:
      mode: STRICT  # Require mTLS on specific port
```

#### Verification and Troubleshooting

```bash
# Verify mTLS is enabled
istioctl authn tls-check my-service.production.svc.cluster.local

# Check certificate validity
kubectl exec -it my-service-pod -n production -c istio-proxy -- \
  openssl s_client -showcerts -connect other-service:8080

# View mTLS metrics
kubectl exec -it my-service-pod -n production -c istio-proxy -- \
  curl http://localhost:15000/stats/prometheus | grep ssl

# Test mTLS connectivity
kubectl run test-pod --rm -it --image=nicolaka/netshoot -- \
  curl -v --cacert /etc/certs/root-ca.pem \
  --cert /etc/certs/client-cert.pem \
  --key /etc/certs/client-key.pem \
  https://my-service.production.svc.cluster.local:8080
```

### Service Mesh for Zero-Trust

Service meshes provide a dedicated infrastructure layer for service-to-service communication with built-in security, observability, and traffic management.

#### Istio Architecture

```yaml
# Install Istio with security features
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: zero-trust-istio
spec:
  profile: production
  components:
    pilot:
      k8s:
        resources:
          requests:
            cpu: 500m
            memory: 2048Mi
    ingressGateways:
      - name: istio-ingressgateway
        enabled: true
        k8s:
          service:
            type: LoadBalancer
  meshConfig:
    # Enable access logging
    accessLogFile: /dev/stdout
    accessLogEncoding: JSON

    # Default mTLS settings
    defaultConfig:
      proxyMetadata:
        ISTIO_META_TLS_AUTO: "true"

    # Enable tracing
    enableTracing: true
    defaultConfig:
      tracing:
        sampling: 100.0
        zipkin:
          address: zipkin.istio-system:9411

  values:
    global:
      # Enable strict mTLS by default
      mtls:
        enabled: true
        auto: true

      # Security settings
      controlPlaneSecurityEnabled: true

      # Enable SDS (Secret Discovery Service)
      sds:
        enabled: true
        udsPath: "unix:/var/run/sds/uds_path"
```

#### Authorization Policies

```yaml
# Deny all by default
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  {}

---
# Allow specific service-to-service communication
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend-api
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/frontend"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
    when:
    - key: request.headers[x-api-version]
      values: ["v2"]

---
# Attribute-based access control
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: admin-access-policy
  namespace: production
spec:
  selector:
    matchLabels:
      app: admin-panel
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/admin-service"]
        requestPrincipals: ["*"]
    when:
    - key: request.auth.claims[role]
      values: ["admin", "superuser"]
    - key: request.auth.claims[department]
      values: ["engineering", "security"]

---
# Custom deny action with detailed reason
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-external-access
  namespace: production
spec:
  selector:
    matchLabels:
      app: internal-api
  action: DENY
  rules:
  - from:
    - source:
        notNamespaces: ["production", "staging"]
```

#### Linkerd Alternative

```yaml
# Linkerd authorization policy
apiVersion: policy.linkerd.io/v1beta1
kind: Server
metadata:
  name: backend-server
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend-api
  port: 8080
  proxyProtocol: HTTP/2

---
apiVersion: policy.linkerd.io/v1alpha1
kind: AuthorizationPolicy
metadata:
  name: frontend-can-call-backend
  namespace: production
spec:
  targetRef:
    group: policy.linkerd.io
    kind: Server
    name: backend-server
  requiredAuthenticationRefs:
  - name: frontend-sa
    kind: ServiceAccount
    namespace: production

---
# Linkerd ServerAuthorization with mTLS
apiVersion: policy.linkerd.io/v1beta1
kind: ServerAuthorization
metadata:
  name: backend-auth
  namespace: production
spec:
  server:
    selector:
      matchLabels:
        app: backend-api
  client:
    meshTLS:
      serviceAccounts:
      - name: frontend
        namespace: production
      - name: api-gateway
        namespace: ingress
```

### Identity-Based Access (Workload Identities)

#### SPIFFE/SPIRE Implementation

SPIFFE (Secure Production Identity Framework For Everyone) provides a universal identity framework for workloads in heterogeneous environments.

```bash
# Install SPIRE server
kubectl apply -f https://raw.githubusercontent.com/spiffe/spire-tutorials/main/k8s/quickstart/spire-server.yaml

# Install SPIRE agent
kubectl apply -f https://raw.githubusercontent.com/spiffe/spire-tutorials/main/k8s/quickstart/spire-agent.yaml

# Configure SPIRE server
kubectl exec -n spire spire-server-0 -- \
  /opt/spire/bin/spire-server entry create \
  -spiffeID spiffe://example.org/ns/production/sa/backend \
  -parentID spiffe://example.org/spire/agent/k8s_psat/cluster \
  -selector k8s:ns:production \
  -selector k8s:sa:backend \
  -dns backend.production.svc.cluster.local
```

**SPIRE Server Configuration:**

```hcl
# /etc/spire/server.conf
server {
  bind_address = "0.0.0.0"
  bind_port = "8081"
  trust_domain = "example.org"
  data_dir = "/run/spire/data"
  log_level = "INFO"
  ca_ttl = "24h"
  default_svid_ttl = "1h"
}

plugins {
  DataStore "sql" {
    plugin_data {
      database_type = "postgres"
      connection_string = "postgresql://spire:password@postgres:5432/spire"
    }
  }

  KeyManager "disk" {
    plugin_data {
      keys_path = "/run/spire/data/keys.json"
    }
  }

  NodeAttestor "k8s_psat" {
    plugin_data {
      clusters = {
        "production-cluster" = {
          service_account_allow_list = ["spire:spire-agent"]
        }
      }
    }
  }

  NodeResolver "noop" {
    plugin_data {}
  }

  Notifier "k8sbundle" {
    plugin_data {
      namespace = "spire"
      config_map = "spire-bundle"
    }
  }
}
```

**SPIRE Agent Configuration:**

```hcl
# /etc/spire/agent.conf
agent {
  data_dir = "/run/spire"
  log_level = "INFO"
  server_address = "spire-server.spire.svc.cluster.local"
  server_port = "8081"
  trust_domain = "example.org"
  socket_path = "/run/spire/sockets/agent.sock"
}

plugins {
  KeyManager "memory" {
    plugin_data {}
  }

  NodeAttestor "k8s_psat" {
    plugin_data {
      cluster = "production-cluster"
    }
  }

  WorkloadAttestor "k8s" {
    plugin_data {
      skip_kubelet_verification = true
    }
  }

  WorkloadAttestor "unix" {
    plugin_data {}
  }
}
```

#### Integrating SPIRE with Istio

```yaml
# Configure Istio to use SPIRE as CA
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-spire-integration
spec:
  profile: production
  meshConfig:
    trustDomain: example.org
    defaultConfig:
      proxyMetadata:
        SPIFFE_ENABLED: "true"

  values:
    global:
      # Use SPIRE for certificate management
      caAddress: spire-server.spire.svc.cluster.local:8081

    pilot:
      env:
        ENABLE_CA_SERVER: "false"
        EXTERNAL_CA: ISTIOD_RA_KUBERNETES_API
```

**Workload Identity Example:**

```go
// Go application using SPIFFE Workload API
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/spiffe/go-spiffe/v2/workloadapi"
)

func main() {
    ctx := context.Background()

    // Create X.509 source
    source, err := workloadapi.NewX509Source(ctx)
    if err != nil {
        log.Fatalf("Unable to create X.509 source: %v", err)
    }
    defer source.Close()

    // Get SVID (SPIFFE Verifiable Identity Document)
    svid, err := source.GetX509SVID()
    if err != nil {
        log.Fatalf("Unable to get X.509 SVID: %v", err)
    }

    fmt.Printf("SPIFFE ID: %s\n", svid.ID)
    fmt.Printf("Certificate: %v\n", svid.Certificates[0])

    // Use SVID for mTLS connections
    tlsConfig := source.GetX509SVIDConfig()

    // ... use tlsConfig with HTTP client or server
}
```

### Network Segmentation (Microsegmentation)

Microsegmentation divides networks into small, isolated segments to limit lateral movement and reduce blast radius.

#### Kubernetes NetworkPolicies

```yaml
# Default deny all ingress and egress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

---
# Allow DNS resolution
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53

---
# Frontend to backend communication
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend-api
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080

---
# Allow egress to external APIs with specific IPs
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-external-api
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api-consumer
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 203.0.113.0/24
        except:
        - 203.0.113.5/32
    ports:
    - protocol: TCP
      port: 443

---
# Multi-namespace access with labels
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-monitoring
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          monitoring: enabled
    - podSelector:
        matchLabels:
          app: prometheus
    ports:
    - protocol: TCP
      port: 9090
```

#### Cilium Network Policies (Advanced)

```yaml
# Layer 7 (HTTP) policy with Cilium
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: http-l7-policy
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: backend-api
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
    toPorts:
    - ports:
      - port: "8080"
        protocol: TCP
      rules:
        http:
        - method: "GET"
          path: "/api/users.*"
        - method: "POST"
          path: "/api/users"
          headers:
          - "Content-Type: application/json"

---
# DNS-based policy
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: dns-based-egress
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: external-api-client
  egress:
  - toFQDNs:
    - matchName: "api.stripe.com"
    - matchPattern: "*.googleapis.com"
  - toPorts:
    - ports:
      - port: "443"
        protocol: TCP

---
# Identity-based policy with SPIFFE
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: spiffe-identity-policy
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: secure-service
  ingress:
  - fromEndpoints:
    - matchExpressions:
      - key: io.cilium.k8s.policy.serviceaccount
        operator: In
        values:
        - "trusted-client"
    authentication:
      mode: required
    toPorts:
    - ports:
      - port: "8443"
        protocol: TCP
```

### Continuous Verification and Monitoring

Zero-trust requires continuous validation of security posture and real-time threat detection.

#### Security Monitoring Stack

```yaml
# Falco for runtime security
apiVersion: v1
kind: ConfigMap
metadata:
  name: falco-config
  namespace: security
data:
  falco.yaml: |
    rules_file:
      - /etc/falco/falco_rules.yaml
      - /etc/falco/k8s_audit_rules.yaml
      - /etc/falco/custom_rules.yaml

    json_output: true
    json_include_output_property: true
    log_stderr: true
    log_syslog: false
    log_level: info

    # Output channels
    file_output:
      enabled: true
      keep_alive: false
      filename: /var/log/falco/events.txt

    http_output:
      enabled: true
      url: http://falcosidekick:2801

    program_output:
      enabled: false

    # Rule matching
    priority: debug
    buffered_outputs: false

---
# Custom Falco rules for zero-trust violations
apiVersion: v1
kind: ConfigMap
metadata:
  name: falco-custom-rules
  namespace: security
data:
  custom_rules.yaml: |
    - rule: Unauthorized Network Connection
      desc: Detect network connections not matching zero-trust policies
      condition: >
        evt.type=connect and
        not proc.name in (allowed_binaries) and
        not fd.sip in (allowed_ips)
      output: >
        Unauthorized network connection
        (user=%user.name command=%proc.cmdline connection=%fd.name)
      priority: WARNING
      tags: [network, zero-trust]

    - rule: Process Running Without Identity
      desc: Detect processes without valid SPIFFE identity
      condition: >
        evt.type=execve and
        not proc.env contains "SPIFFE_ENDPOINT_SOCKET"
      output: >
        Process started without workload identity
        (user=%user.name command=%proc.cmdline container=%container.name)
      priority: ERROR
      tags: [identity, zero-trust]

    - rule: Suspicious Certificate Access
      desc: Detect unauthorized access to certificate files
      condition: >
        evt.type=open and
        fd.name glob "/etc/ssl/*" and
        not proc.name in (authorized_cert_readers)
      output: >
        Suspicious certificate file access
        (user=%user.name file=%fd.name process=%proc.name)
      priority: CRITICAL
      tags: [certificate, zero-trust]
```

#### Prometheus Metrics for Zero-Trust

```yaml
# ServiceMonitor for Istio mTLS metrics
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: istio-mtls-metrics
  namespace: istio-system
spec:
  selector:
    matchLabels:
      app: istiod
  endpoints:
  - port: http-monitoring
    interval: 30s
    path: /metrics
    relabelings:
    - sourceLabels: [__meta_kubernetes_pod_name]
      targetLabel: pod_name

---
# PrometheusRule for zero-trust alerts
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: zero-trust-alerts
  namespace: monitoring
spec:
  groups:
  - name: zero-trust
    interval: 30s
    rules:
    - alert: MTLSConnectionFailure
      expr: |
        rate(istio_tcp_connections_closed_total{response_flags="URX"}[5m]) > 0.1
      for: 5m
      labels:
        severity: critical
        category: zero-trust
      annotations:
        summary: "High rate of mTLS connection failures"
        description: "{{ $labels.destination_service }} is experiencing mTLS failures"

    - alert: UnauthorizedAccessAttempt
      expr: |
        rate(istio_requests_total{response_code="403"}[5m]) > 1
      for: 2m
      labels:
        severity: warning
        category: zero-trust
      annotations:
        summary: "Unauthorized access attempts detected"
        description: "{{ $labels.source_app }} attempting unauthorized access to {{ $labels.destination_service }}"

    - alert: CertificateExpirationWarning
      expr: |
        (x509_cert_not_after - time()) / 86400 < 7
      for: 1h
      labels:
        severity: warning
        category: certificate
      annotations:
        summary: "Certificate expiring soon"
        description: "Certificate {{ $labels.subject }} expires in {{ $value }} days"

    - alert: AnomalousTrafficPattern
      expr: |
        (
          rate(istio_requests_total[5m])
          /
          rate(istio_requests_total[5m] offset 1h)
        ) > 2
      for: 10m
      labels:
        severity: info
        category: anomaly
      annotations:
        summary: "Unusual traffic pattern detected"
        description: "Traffic to {{ $labels.destination_service }} is {{ $value }}x higher than usual"
```

### BeyondCorp Model

BeyondCorp removes the concept of a privileged corporate network, treating all access as potentially hostile.

#### Identity-Aware Proxy (IAP)

```yaml
# Google Cloud Identity-Aware Proxy configuration
apiVersion: cloud.google.com/v1
kind: BackendConfig
metadata:
  name: beyondcorp-backend
  namespace: production
spec:
  iap:
    enabled: true
    oauthclientCredentials:
      secretName: oauth-client-secret

  securityPolicy:
    name: "beyondcorp-security-policy"

  sessionAffinity:
    affinityType: "CLIENT_IP"
    affinityCookieTtlSec: 3600

---
# Application with IAP annotations
apiVersion: v1
kind: Service
metadata:
  name: webapp
  namespace: production
  annotations:
    cloud.google.com/backend-config: '{"default": "beyondcorp-backend"}'
    cloud.google.com/neg: '{"ingress": true}'
spec:
  type: ClusterIP
  selector:
    app: webapp
  ports:
  - port: 8080
    targetPort: 8080
    protocol: TCP
```

#### Open Policy Agent (OPA) for Context-Aware Access

```rego
# OPA policy for context-aware authorization
package beyondcorp.authz

import future.keywords.if
import future.keywords.in

default allow = false

# Allow if all conditions are met
allow if {
    valid_user
    valid_device
    valid_location
    valid_risk_score
    authorized_for_resource
}

# User identity verification
valid_user if {
    input.user.email
    input.user.email_verified
    not user_in_blocklist
}

user_in_blocklist if {
    input.user.email in data.blocklist.users
}

# Device trust verification
valid_device if {
    input.device.managed
    input.device.encrypted
    input.device.os_version in data.allowed_os_versions
    not device_compromised
}

device_compromised if {
    input.device.id in data.compromised_devices
}

# Location-based access
valid_location if {
    input.location.country in data.allowed_countries
}

valid_location if {
    input.resource.sensitivity == "low"
}

# Risk score calculation
valid_risk_score if {
    risk_score <= 30
}

risk_score = score if {
    base_score := 0
    user_score := user_risk_component
    device_score := device_risk_component
    behavior_score := behavior_risk_component
    score := base_score + user_score + device_score + behavior_score
}

user_risk_component = 10 if {
    input.user.new_account
} else = 0

device_risk_component = 15 if {
    not input.device.known
} else = 0

behavior_risk_component = 20 if {
    input.behavior.unusual_time
    input.behavior.unusual_location
} else = 10 if {
    input.behavior.unusual_time
} else = 0

# Resource-based authorization
authorized_for_resource if {
    required_role := data.resources[input.resource.path].required_role
    required_role in input.user.roles
}

# Additional constraints for sensitive resources
authorized_for_resource if {
    input.resource.sensitivity == "high"
    "admin" in input.user.roles
    input.device.managed
    input.user.mfa_verified
}
```

**OPA Integration with API Gateway:**

```yaml
# Envoy External Authorization with OPA
apiVersion: v1
kind: ConfigMap
metadata:
  name: envoy-config
  namespace: ingress
data:
  envoy.yaml: |
    static_resources:
      listeners:
      - name: main
        address:
          socket_address:
            address: 0.0.0.0
            port_value: 8000
        filter_chains:
        - filters:
          - name: envoy.filters.network.http_connection_manager
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
              stat_prefix: ingress_http
              codec_type: AUTO
              route_config:
                name: local_route
                virtual_hosts:
                - name: backend
                  domains: ["*"]
                  routes:
                  - match:
                      prefix: "/"
                    route:
                      cluster: backend_service
              http_filters:
              - name: envoy.filters.http.ext_authz
                typed_config:
                  "@type": type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz
                  grpc_service:
                    envoy_grpc:
                      cluster_name: opa_cluster
                    timeout: 0.5s
                  with_request_body:
                    max_request_bytes: 8192
                    allow_partial_message: true
              - name: envoy.filters.http.router
                typed_config:
                  "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router

      clusters:
      - name: backend_service
        connect_timeout: 0.25s
        type: STRICT_DNS
        lb_policy: ROUND_ROBIN
        load_assignment:
          cluster_name: backend_service
          endpoints:
          - lb_endpoints:
            - endpoint:
                address:
                  socket_address:
                    address: backend.production.svc.cluster.local
                    port_value: 8080

      - name: opa_cluster
        connect_timeout: 0.25s
        type: STRICT_DNS
        lb_policy: ROUND_ROBIN
        http2_protocol_options: {}
        load_assignment:
          cluster_name: opa_cluster
          endpoints:
          - lb_endpoints:
            - endpoint:
                address:
                  socket_address:
                    address: opa.security.svc.cluster.local
                    port_value: 9191
```

### NIST 800-207 Zero Trust Architecture

NIST SP 800-207 provides a comprehensive framework for implementing zero-trust architecture in federal and enterprise systems.

#### Zero Trust Architecture Components

**1. Policy Engine (PE):**

- Grants or denies access to resources
- Uses Policy Administrator to execute decisions
- Considers user, device, resource, and contextual attributes

**2. Policy Administrator (PA):**

- Establishes/shuts down communication paths
- Generates session-specific authentication tokens
- Instructs Policy Enforcement Points

**3. Policy Enforcement Point (PEP):**

- Enables, monitors, and terminates connections
- Forwards requests to Policy Engine
- Can be gateway, agent, or access proxy

**Implementation Example:**

```yaml
# Policy Engine (OPA) deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: policy-engine
  namespace: zero-trust
spec:
  replicas: 3
  selector:
    matchLabels:
      app: policy-engine
  template:
    metadata:
      labels:
        app: policy-engine
    spec:
      containers:
      - name: opa
        image: openpolicyagent/opa:latest
        args:
        - "run"
        - "--server"
        - "--addr=0.0.0.0:8181"
        - "--log-level=info"
        - "/policies"
        ports:
        - name: http
          containerPort: 8181
        volumeMounts:
        - name: policies
          mountPath: /policies
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8181
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health?ready=true
            port: 8181
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: policies
        configMap:
          name: opa-policies

---
# Policy Administrator (custom controller)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: policy-administrator
  namespace: zero-trust
spec:
  replicas: 2
  selector:
    matchLabels:
      app: policy-administrator
  template:
    metadata:
      labels:
        app: policy-administrator
    spec:
      serviceAccountName: policy-admin
      containers:
      - name: controller
        image: myorg/policy-admin-controller:v1.0
        env:
        - name: POLICY_ENGINE_URL
          value: "http://policy-engine.zero-trust.svc.cluster.local:8181"
        - name: TOKEN_ISSUER
          value: "https://auth.example.com"
        - name: SESSION_TTL
          value: "3600"
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: 200m
            memory: 256Mi

---
# Policy Enforcement Point (Envoy sidecar)
apiVersion: v1
kind: ConfigMap
metadata:
  name: pep-envoy-config
  namespace: zero-trust
data:
  envoy.yaml: |
    admin:
      address:
        socket_address:
          address: 127.0.0.1
          port_value: 9901

    static_resources:
      listeners:
      - name: pep_listener
        address:
          socket_address:
            address: 0.0.0.0
            port_value: 10000
        filter_chains:
        - filters:
          - name: envoy.filters.network.http_connection_manager
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
              stat_prefix: pep
              http_filters:
              - name: envoy.filters.http.ext_authz
                typed_config:
                  "@type": type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz
                  grpc_service:
                    envoy_grpc:
                      cluster_name: policy_engine
                    timeout: 1s
                  failure_mode_allow: false
              - name: envoy.filters.http.router
              route_config:
                name: local_route
                virtual_hosts:
                - name: backend
                  domains: ["*"]
                  routes:
                  - match: { prefix: "/" }
                    route:
                      cluster: backend

      clusters:
      - name: policy_engine
        connect_timeout: 0.5s
        type: STRICT_DNS
        http2_protocol_options: {}
        load_assignment:
          cluster_name: policy_engine
          endpoints:
          - lb_endpoints:
            - endpoint:
                address:
                  socket_address:
                    address: policy-engine.zero-trust.svc.cluster.local
                    port_value: 9191

      - name: backend
        connect_timeout: 0.5s
        type: STRICT_DNS
        load_assignment:
          cluster_name: backend
          endpoints:
          - lb_endpoints:
            - endpoint:
                address:
                  socket_address:
                    address: 127.0.0.1
                    port_value: 8080
```

#### Trust Algorithm (TA)

The Trust Algorithm computes trust scores based on multiple inputs:

```python
# Trust Algorithm implementation
from dataclasses import dataclass
from typing import Dict, List
from enum import Enum

class TrustLevel(Enum):
    DENY = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

@dataclass
class TrustScore:
    user_score: float
    device_score: float
    network_score: float
    behavior_score: float
    resource_sensitivity: float

    def compute_overall(self) -> float:
        weights = {
            'user': 0.25,
            'device': 0.25,
            'network': 0.15,
            'behavior': 0.20,
            'resource': 0.15
        }

        total = (
            self.user_score * weights['user'] +
            self.device_score * weights['device'] +
            self.network_score * weights['network'] +
            self.behavior_score * weights['behavior'] +
            self.resource_sensitivity * weights['resource']
        )

        return min(max(total, 0.0), 100.0)

    def get_trust_level(self) -> TrustLevel:
        score = self.compute_overall()

        if score < 40:
            return TrustLevel.DENY
        elif score < 60:
            return TrustLevel.LOW
        elif score < 80:
            return TrustLevel.MEDIUM
        else:
            return TrustLevel.HIGH

class TrustAlgorithm:
    def __init__(self, config: Dict):
        self.config = config
        self.anomaly_threshold = config.get('anomaly_threshold', 0.7)

    def evaluate_user(self, user_data: Dict) -> float:
        score = 100.0

        # Authentication strength
        if not user_data.get('mfa_enabled'):
            score -= 30

        # Account age and activity
        if user_data.get('account_age_days', 0) < 30:
            score -= 20

        # Past violations
        violations = user_data.get('security_violations', 0)
        score -= min(violations * 10, 40)

        return max(score, 0.0)

    def evaluate_device(self, device_data: Dict) -> float:
        score = 100.0

        # Device management
        if not device_data.get('managed'):
            score -= 40

        # Encryption
        if not device_data.get('encrypted'):
            score -= 30

        # Security posture
        if not device_data.get('firewall_enabled'):
            score -= 15
        if not device_data.get('antivirus_updated'):
            score -= 15

        # Known device
        if not device_data.get('previously_seen'):
            score -= 20

        return max(score, 0.0)

    def evaluate_network(self, network_data: Dict) -> float:
        score = 100.0

        # Location
        if network_data.get('country') not in self.config.get('allowed_countries', []):
            score -= 40

        # IP reputation
        if network_data.get('ip_reputation') == 'bad':
            score -= 50

        # VPN/Proxy
        if network_data.get('using_vpn') and not network_data.get('corporate_vpn'):
            score -= 20

        return max(score, 0.0)

    def evaluate_behavior(self, behavior_data: Dict) -> float:
        score = 100.0

        # Time-based anomalies
        if behavior_data.get('unusual_time'):
            score -= 25

        # Access patterns
        if behavior_data.get('unusual_resource'):
            score -= 30

        # Volume anomalies
        if behavior_data.get('excessive_requests'):
            score -= 20

        # Failed attempts
        failed_attempts = behavior_data.get('recent_failed_attempts', 0)
        score -= min(failed_attempts * 15, 45)

        return max(score, 0.0)

    def evaluate_resource(self, resource_data: Dict) -> float:
        sensitivity_map = {
            'public': 100.0,
            'internal': 70.0,
            'confidential': 40.0,
            'restricted': 20.0
        }

        sensitivity = resource_data.get('classification', 'internal')
        return sensitivity_map.get(sensitivity, 50.0)

    def compute_trust_score(self, context: Dict) -> TrustScore:
        return TrustScore(
            user_score=self.evaluate_user(context.get('user', {})),
            device_score=self.evaluate_device(context.get('device', {})),
            network_score=self.evaluate_network(context.get('network', {})),
            behavior_score=self.evaluate_behavior(context.get('behavior', {})),
            resource_sensitivity=self.evaluate_resource(context.get('resource', {}))
        )

    def make_decision(self, context: Dict) -> Dict:
        trust_score = self.compute_trust_score(context)
        overall_score = trust_score.compute_overall()
        trust_level = trust_score.get_trust_level()

        # Determine access decision
        allow = trust_level != TrustLevel.DENY

        # Determine additional requirements
        additional_auth = trust_level in [TrustLevel.LOW, TrustLevel.MEDIUM]

        # Calculate session duration
        session_duration = self._calculate_session_duration(trust_level)

        return {
            'allow': allow,
            'trust_level': trust_level.name,
            'overall_score': overall_score,
            'component_scores': {
                'user': trust_score.user_score,
                'device': trust_score.device_score,
                'network': trust_score.network_score,
                'behavior': trust_score.behavior_score,
                'resource': trust_score.resource_sensitivity
            },
            'additional_auth_required': additional_auth,
            'session_duration_seconds': session_duration,
            'continuous_verification_interval': 300 if allow else 0
        }

    def _calculate_session_duration(self, trust_level: TrustLevel) -> int:
        duration_map = {
            TrustLevel.DENY: 0,
            TrustLevel.LOW: 1800,    # 30 minutes
            TrustLevel.MEDIUM: 3600,  # 1 hour
            TrustLevel.HIGH: 7200     # 2 hours
        }
        return duration_map.get(trust_level, 0)

# Example usage
trust_algo = TrustAlgorithm({
    'allowed_countries': ['US', 'CA', 'GB'],
    'anomaly_threshold': 0.7
})

context = {
    'user': {
        'mfa_enabled': True,
        'account_age_days': 365,
        'security_violations': 0
    },
    'device': {
        'managed': True,
        'encrypted': True,
        'firewall_enabled': True,
        'antivirus_updated': True,
        'previously_seen': True
    },
    'network': {
        'country': 'US',
        'ip_reputation': 'good',
        'using_vpn': False
    },
    'behavior': {
        'unusual_time': False,
        'unusual_resource': False,
        'excessive_requests': False,
        'recent_failed_attempts': 0
    },
    'resource': {
        'classification': 'confidential'
    }
}

decision = trust_algo.make_decision(context)
print(f"Access: {'ALLOWED' if decision['allow'] else 'DENIED'}")
print(f"Trust Level: {decision['trust_level']}")
print(f"Overall Score: {decision['overall_score']:.2f}")
print(f"Session Duration: {decision['session_duration_seconds']} seconds")
```

---

## Level 3: Deep Dive Resources

### Official Documentation

**NIST Standards:**

- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final)
- [NIST SP 800-53: Security and Privacy Controls](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)

**SPIFFE/SPIRE:**

- [SPIFFE Specification](https://github.com/spiffe/spiffe)
- [SPIRE Documentation](https://spiffe.io/docs/latest/spire-about/)

**Service Mesh:**

- [Istio Security](https://istio.io/latest/docs/concepts/security/)
- [Linkerd Security](https://linkerd.io/2/features/automatic-mtls/)

**BeyondCorp:**

- [BeyondCorp Research Papers](https://cloud.google.com/beyondcorp)
- [Identity-Aware Proxy](https://cloud.google.com/iap/docs)

### Books & Guides

- **"Zero Trust Networks"** by Evan Gilman & Doug Barth (O'Reilly)
- **"BeyondCorp: Design Your Own Zero Trust Network"** by Juana A. & Neal M.
- **"Zero Trust Security: An Enterprise Guide"** by Jason Garbis & Jerry Chapman

### Tools & Projects

**Zero-Trust Platforms:**

- Palo Alto Prisma Access
- Zscaler Private Access
- Cloudflare Access
- Google BeyondCorp

**Open Source:**

- Open Policy Agent (OPA)
- Envoy Proxy
- Istio Service Mesh
- SPIFFE/SPIRE

### Training & Certifications

- **SANS SEC530:** Defensible Security Architecture and Engineering
- **Cloud Security Alliance:** CCSK (Certificate of Cloud Security Knowledge)
- **Kubernetes Security Specialist (CKS)**

### Related Skills

Deepen your zero-trust expertise with these complementary skills:

- **Secrets Management:** Vault, sealed secrets, external secrets operator
- **Secure API Design:** OAuth2, OIDC, API gateways
- **Security Monitoring:** SIEM, threat detection, incident response

### Community Resources

- [r/netsec](https://reddit.com/r/netsec)
- [Cloud Native Security Day](https://events.linuxfoundation.org/cloud-native-security-day-north-america/)
- [OWASP](https://owasp.org/)

---

## Bundled Resources

See `templates/`, `resources/`, and `scripts/` directories for:

- mTLS configuration examples
- SPIFFE workload identity templates
- NetworkPolicy examples
- Zero-trust architecture diagrams
- Automation scripts
- NIST 800-207 compliance checklist
