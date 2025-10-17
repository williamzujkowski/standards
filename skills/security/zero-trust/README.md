# Zero-Trust Security Skill

**Advanced security skill for implementing zero-trust architecture in cloud-native environments**

## Overview

This skill provides comprehensive guidance for implementing zero-trust security architecture following NIST SP 800-207 guidelines. It covers mutual TLS (mTLS), service mesh security, workload identity management, network microsegmentation, and continuous verification.

## Skill Structure

```
skills/security/zero-trust/
├── SKILL.md                              # Main skill document (3 levels)
├── templates/                            # Configuration templates
│   ├── mtls-config.yaml                 # Istio mTLS configuration
│   ├── workload-identity.yaml           # SPIFFE/SPIRE setup
│   └── network-policy.yaml              # Kubernetes NetworkPolicies
├── resources/                            # Supporting documentation
│   ├── zero-trust-architecture.md       # Architecture diagrams and explanations
│   └── nist-800-207-checklist.md        # NIST compliance checklist
└── scripts/                              # Automation scripts
    └── setup-mtls.sh                    # mTLS certificate automation
```

## Learning Path

### Level 1: Quick Reference (15-30 minutes)
- Zero-trust principles and core tenets
- Common patterns (mTLS, service mesh, BeyondCorp)
- Essential implementation checklist
- Quick wins for immediate security improvements

**Target audience:** Developers, DevOps engineers, security practitioners

### Level 2: Implementation Guide (4-6 hours)
- Detailed zero-trust architecture principles
- Step-by-step mTLS implementation
- Service mesh deployment (Istio/Linkerd)
- Workload identity with SPIFFE/SPIRE
- Network microsegmentation strategies
- Continuous verification and monitoring
- BeyondCorp model implementation
- NIST 800-207 compliance guidance

**Target audience:** Security architects, platform engineers, DevSecOps teams

### Level 3: Deep Dive Resources
- Official NIST documentation
- Service mesh documentation (Istio, Linkerd)
- SPIFFE/SPIRE specifications
- Books, certifications, and training
- Community resources

**Target audience:** Security specialists, compliance officers, senior architects

## Quick Start

### Prerequisites
- Kubernetes cluster (1.20+)
- kubectl configured
- Basic understanding of:
  - Network security concepts
  - Container orchestration
  - PKI and certificates
  - Identity and access management

### 1. Set up mTLS with automated script

```bash
# Set environment variables
export NAMESPACE=production
export SERVICE_MESH=istio  # or linkerd
export CA_DIR=/tmp/mtls-ca

# Run setup
./scripts/setup-mtls.sh setup

# Generate service certificates
./scripts/setup-mtls.sh generate-cert frontend
./scripts/setup-mtls.sh generate-cert backend
./scripts/setup-mtls.sh generate-cert database

# Verify configuration
./scripts/setup-mtls.sh verify
```

### 2. Deploy Istio with strict mTLS

```bash
# Apply mTLS configuration
kubectl apply -f templates/mtls-config.yaml

# Verify mTLS status
istioctl proxy-status
istioctl authn tls-check
```

### 3. Implement workload identities

```bash
# Deploy SPIRE server and agents
kubectl apply -f templates/workload-identity.yaml

# Verify SPIRE deployment
kubectl exec -n spire spire-server-0 -- \
  /opt/spire/bin/spire-server healthcheck
```

### 4. Apply network segmentation

```bash
# Deploy NetworkPolicies
kubectl apply -f templates/network-policy.yaml

# Verify policies
kubectl get networkpolicies -n production
kubectl describe networkpolicy default-deny-all -n production
```

## Templates

### mTLS Configuration (`templates/mtls-config.yaml`)
- Global strict mTLS policy for Istio
- Namespace-level permissive mode for migration
- Workload-specific mTLS overrides
- DestinationRules for client-side mTLS
- Authorization policies for mTLS-authenticated services
- Gateway configuration with mTLS
- External service mTLS configuration

**Lines:** 233 | **Use cases:** Service mesh security, encrypted communication

### Workload Identity (`templates/workload-identity.yaml`)
- SPIRE server and agent configurations
- Kubernetes integration (k8s_psat attestation)
- Workload registration entries
- Istio + SPIRE integration
- Service account mapping
- Certificate management

**Lines:** 424 | **Use cases:** Zero-trust identity, mTLS with automatic certificates

### Network Policy (`templates/network-policy.yaml`)
- Default deny-all policies
- DNS resolution allowance
- Tier-based segmentation (frontend, backend, database)
- Layer 7 policies (Cilium)
- DNS-based egress policies
- Service mesh sidecar communication
- Monitoring and observability access

**Lines:** 483 | **Use cases:** Microsegmentation, east-west traffic control

## Resources

### Zero-Trust Architecture (`resources/zero-trust-architecture.md`)
Comprehensive architecture guide including:
- Component diagrams (PDP, PEP, PA)
- Data flow examples
- Network segmentation strategies
- Trust boundaries and levels
- Security controls mapping (NIST)
- Migration strategy (5 phases)
- Common pitfalls and solutions

**Lines:** 573 | **Key topics:** Architecture design, component integration

### NIST 800-207 Checklist (`resources/nist-800-207-checklist.md`)
Detailed compliance checklist covering:
- 7 zero-trust tenets (NIST)
- Architecture components (PE, PA, PEP)
- Trust algorithm implementation
- Identity and access management
- Network segmentation requirements
- Encryption and data protection
- Continuous monitoring
- Governance and compliance
- Automation and orchestration
- Maturity level assessment

**Lines:** 568 | **Use case:** Compliance assessment, implementation tracking

## Automation Scripts

### mTLS Setup (`scripts/setup-mtls.sh`)
Automated certificate management and mTLS configuration:

**Commands:**
```bash
setup-mtls.sh setup                  # Create CA and configure service mesh
setup-mtls.sh generate-cert <name>   # Generate service certificate
setup-mtls.sh rotate <name> ...      # Rotate certificates
setup-mtls.sh verify                 # Verify mTLS status
setup-mtls.sh info <name>            # Display certificate info
```

**Features:**
- Root and intermediate CA generation
- Service certificate creation with SAN
- Kubernetes secret management
- Istio/Linkerd integration
- Certificate rotation
- Validity verification

**Lines:** 387 | **Languages:** Bash, OpenSSL

## NIST Controls Coverage

This skill directly addresses the following NIST SP 800-53 controls:

| Control | Name | Implementation |
|---------|------|----------------|
| **AC-4** | Information Flow Enforcement | NetworkPolicies, service mesh authorization |
| **SC-7** | Boundary Protection | Microsegmentation, PEP at boundaries |
| **SC-8** | Transmission Confidentiality and Integrity | mTLS, TLS 1.3, encrypted channels |

## Use Cases

### 1. Microservices Security
- mTLS between all services
- Service-to-service authorization
- Workload identities without secrets
- Traffic encryption and inspection

### 2. Compliance Requirements
- NIST 800-207 compliance
- PCI-DSS segmentation
- HIPAA data protection
- SOC 2 access controls

### 3. Cloud-Native Security
- Kubernetes NetworkPolicies
- Service mesh integration
- Cloud-agnostic identity (SPIFFE)
- Multi-cluster security

### 4. Remote Access Security
- BeyondCorp model
- Identity-aware proxy
- Context-aware access
- Device trust verification

## Best Practices

### 1. Start with Visibility
- Deploy service mesh in permissive mode
- Enable comprehensive logging
- Map service dependencies
- Understand traffic patterns

### 2. Gradual Migration
- Phase 1: Visibility (weeks 1-4)
- Phase 2: Identity (weeks 5-8)
- Phase 3: Segmentation (weeks 9-12)
- Phase 4: Authorization (weeks 13-16)
- Phase 5: Continuous improvement

### 3. Automate Everything
- Certificate lifecycle management
- Policy deployment and testing
- Monitoring and alerting
- Incident response

### 4. Measure and Improve
- Track key metrics (authorization latency, policy violations)
- Regular security assessments
- Policy effectiveness reviews
- Continuous tuning

## Common Pitfalls

1. **Incomplete Coverage:** Apply zero-trust to ALL resources, not just critical ones
2. **Static Policies:** Policies must adapt to changing risk
3. **Poor Visibility:** Insufficient logging makes troubleshooting impossible
4. **Over-Complexity:** Start simple, iterate
5. **Certificate Management:** Automate or face operational burden
6. **Legacy Systems:** Plan for gradual migration
7. **User Experience:** Balance security with usability

## Troubleshooting

### mTLS Issues
```bash
# Check mTLS status
istioctl proxy-status
istioctl authn tls-check <service>

# View certificate details
kubectl exec <pod> -c istio-proxy -- \
  openssl s_client -showcerts -connect <service>:8080

# Check mTLS metrics
kubectl exec <pod> -c istio-proxy -- \
  curl http://localhost:15000/stats/prometheus | grep ssl
```

### NetworkPolicy Issues
```bash
# Test connectivity
kubectl run test-pod --rm -it --image=nicolaka/netshoot -- \
  curl -v <service>:<port>

# Check policy application
kubectl describe networkpolicy <policy-name>

# View policy logs (Cilium)
kubectl logs -n kube-system -l k8s-app=cilium --tail=50
```

### SPIRE Issues
```bash
# Check SPIRE server health
kubectl exec -n spire spire-server-0 -- \
  /opt/spire/bin/spire-server healthcheck

# List registered workloads
kubectl exec -n spire spire-server-0 -- \
  /opt/spire/bin/spire-server entry show

# Check agent status
kubectl logs -n spire -l app=spire-agent --tail=50
```

## Related Skills

- **Secrets Management:** Vault, sealed secrets, external secrets operator
- **Secure API Design:** OAuth2, OIDC, API gateway security
- **Security Monitoring:** SIEM, threat detection, incident response
- **Container Security:** Image scanning, runtime security, admission control

## Additional Resources

### Documentation
- [NIST SP 800-207](https://csrc.nist.gov/publications/detail/sp/800-207/final)
- [Istio Security](https://istio.io/latest/docs/concepts/security/)
- [SPIFFE/SPIRE](https://spiffe.io/docs/latest/)
- [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

### Tools
- Service Meshes: Istio, Linkerd, Consul Connect
- Policy Engines: OPA, Kyverno, Gatekeeper
- Identity: SPIFFE/SPIRE, Keycloak, Dex
- Monitoring: Prometheus, Grafana, Falco

### Training
- SANS SEC530: Defensible Security Architecture
- Kubernetes Security Specialist (CKS)
- Cloud Security Alliance CCSK
- Istio Fundamentals (by Tetrate)

## Metrics and KPIs

Track these metrics to measure zero-trust effectiveness:

- **Authorization Decision Latency:** < 100ms (target)
- **Policy Violations:** Trend down over time
- **Mean Time to Detect (MTTD):** < 5 minutes
- **Mean Time to Respond (MTTR):** < 15 minutes
- **Coverage Percentage:** > 95% of services
- **Certificate Rotation Success Rate:** 100%
- **Failed Authentication Attempts:** Monitor for anomalies

## Contributing

To improve this skill:
1. Test configurations in your environment
2. Document edge cases and solutions
3. Share automation scripts
4. Report issues or gaps
5. Contribute examples and use cases

## Version History

- **v1.0.0** (2025-01-17): Initial release
  - Complete SKILL.md with 3 levels
  - 6 bundled resources (templates, scripts, docs)
  - NIST 800-207 compliance checklist
  - mTLS automation script

## License

This skill is part of the Standards Repository and follows the repository's license terms.
