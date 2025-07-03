# Modern Security Standards

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active
**Standard Code:** SEC

---

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active

## Table of Contents

1. [Zero Trust Architecture](#1-zero-trust-architecture)
2. [Supply Chain Security](#2-supply-chain-security)
3. [Container and Kubernetes Security](#3-container-and-kubernetes-security)
4. [API Security](#4-api-security)
5. [DevSecOps Integration](#5-devsecops-integration)
6. [Cloud Security](#6-cloud-security)
7. [Identity and Access Management](#7-identity-and-access-management)
8. [Incident Response and Forensics](#8-incident-response-and-forensics)

---

## Overview

This standard provides comprehensive guidelines and best practices for the subject area.
It aims to ensure consistency, quality, and maintainability across all related implementations.

## NIST Compliance Integration

This standard is fully mapped to NIST 800-53r5 controls. Look for `@nist` tags throughout.

For implementation guidance:

- **Quick Start**: [NIST_IMPLEMENTATION_GUIDE.md](../nist/NIST_IMPLEMENTATION_GUIDE.md)
- **Detailed Standards**: [COMPLIANCE_STANDARDS.md](COMPLIANCE_STANDARDS.md)
- **Control Reference**:
  [Quick Reference](../nist/NIST_IMPLEMENTATION_GUIDE.md#tagging-quick-reference)

## 1. Zero Trust Architecture

<!-- @nist-controls: [ac-2, ac-3, ac-6, ia-2, ia-5, au-2, sc-8] -->

### 1.1 Zero Trust Principles

#### Core Tenets **[REQUIRED]**

```yaml
# Zero Trust Policy Configuration
zero_trust_policy:
  principles:
    - "Never trust, always verify"
    - "Assume breach"
    - "Verify explicitly"
    - "Use least privilege access"
    - "Monitor and log everything"

  implementation:
    identity_verification:
      - Multi-factor authentication required  # @nist ia-2 "Multi-factor authentication"
      - Continuous authentication  # @nist ia-2 "Continuous verification"
      - Risk-based authentication  # @nist ia-5 "Risk-based authenticator management"
      - Device compliance verification  # @nist ia-2 "Device authentication"

    network_segmentation:
      - Micro-segmentation  # @nist ac-3 "Access enforcement through segmentation"
      - Software-defined perimeters  # @nist ac-3 "Dynamic access control"
      - Encrypted communications  # @nist sc-8 "Transmission confidentiality"
      - Network monitoring  # @nist au-2 "Network audit events"

    data_protection:
      - Data classification  # @nist ac-3 "Classification-based access"
      - Encryption at rest and in transit  # @nist sc-13 "Cryptographic protection"
      - Data loss prevention  # @nist ac-3 "Data access enforcement"
      - Rights management  # @nist ac-6 "Least privilege data access"
```

#### Implementation Framework **[REQUIRED]**

```python
# Zero Trust Access Control Framework
# @nist ac-3 "Access enforcement implementation"
# @nist ac-6 "Least privilege access control"
# @nist au-2 "Audit access decisions"
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import time
import jwt
from cryptography.fernet import Fernet

class TrustLevel(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    FULL = 4

@dataclass
class SecurityContext:
    user_id: str
    device_id: str
    location: str
    ip_address: str
    user_agent: str
    risk_score: float
    trust_level: TrustLevel
    authentication_time: float
    session_id: str

@dataclass
class AccessRequest:
    resource: str
    action: str
    context: SecurityContext
    requested_time: float

class PolicyEngine(ABC):
    @abstractmethod
    def evaluate(self, request: AccessRequest) -> bool:
        pass

class ZeroTrustAccessControl:
    # @nist ac-3 "Zero trust access control implementation"
    def __init__(self):
        self.policies: List[PolicyEngine] = []
        self.audit_logger = AuditLogger()  # @nist au-2 "Audit logger initialization"
        self.risk_engine = RiskEngine()  # @nist ia-2 "Risk-based authentication"

    def add_policy(self, policy: PolicyEngine):
        """Add a policy to the evaluation chain."""
        self.policies.append(policy)

    def evaluate_access(self, request: AccessRequest) -> Dict[str, Any]:
        """Evaluate access request against all policies.
        @nist ac-3 "Policy-based access enforcement"
        @nist au-3 "Generate detailed audit records"
        """
        start_time = time.time()

        # Update risk score
        request.context.risk_score = self.risk_engine.calculate_risk(request.context)

        # Evaluate all policies
        decisions = []
        for policy in self.policies:
            try:
                decision = policy.evaluate(request)
                decisions.append({
                    'policy': policy.__class__.__name__,
                    'decision': decision,
                    'timestamp': time.time()
                })
            except Exception as e:
                decisions.append({
                    'policy': policy.__class__.__name__,
                    'decision': False,
                    'error': str(e),
                    'timestamp': time.time()
                })

        # Final decision - all policies must pass
        final_decision = all(d['decision'] for d in decisions)

        result = {
            'access_granted': final_decision,
            'user_id': request.context.user_id,
            'resource': request.resource,
            'action': request.action,
            'risk_score': request.context.risk_score,
            'trust_level': request.context.trust_level.name,
            'policies_evaluated': len(decisions),
            'evaluation_time_ms': (time.time() - start_time) * 1000,
            'policy_decisions': decisions
        }

        # Audit log
        # @nist au-2 "Log all access decisions"
        # @nist au-3 "Include all relevant details in audit log"
        self.audit_logger.log_access_decision(result)

        return result

class IdentityVerificationPolicy(PolicyEngine):
    def __init__(self, mfa_required: bool = True, max_session_age: int = 3600):
        self.mfa_required = mfa_required
        self.max_session_age = max_session_age

    def evaluate(self, request: AccessRequest) -> bool:
        context = request.context

        # Check session age
        session_age = time.time() - context.authentication_time
        if session_age > self.max_session_age:
            return False

        # Check MFA requirement
        if self.mfa_required and context.trust_level < TrustLevel.MEDIUM:
            return False

        return True

class LocationPolicy(PolicyEngine):
    def __init__(self, allowed_countries: List[str], allowed_ip_ranges: List[str]):
        self.allowed_countries = allowed_countries
        self.allowed_ip_ranges = allowed_ip_ranges

    def evaluate(self, request: AccessRequest) -> bool:
        context = request.context

        # Check country restrictions
        user_country = self._get_country_from_location(context.location)
        if user_country not in self.allowed_countries:
            return False

        # Check IP range restrictions
        if not self._ip_in_allowed_ranges(context.ip_address):
            return False

        return True

    def _get_country_from_location(self, location: str) -> str:
        # Implementation to extract country from location
        return location.split(',')[-1].strip()

    def _ip_in_allowed_ranges(self, ip: str) -> bool:
        # Implementation to check if IP is in allowed ranges
        return True  # Simplified for example

class DeviceCompliancePolicy(PolicyEngine):
    def __init__(self, device_registry):
        self.device_registry = device_registry

    def evaluate(self, request: AccessRequest) -> bool:
        context = request.context

        device = self.device_registry.get_device(context.device_id)
        if not device:
            return False

        # Check device compliance
        return (
            device.is_managed and
            device.is_encrypted and
            device.has_latest_patches and
            not device.is_jailbroken
        )

class RiskBasedPolicy(PolicyEngine):
    def __init__(self, max_risk_score: float = 0.7):
        self.max_risk_score = max_risk_score

    def evaluate(self, request: AccessRequest) -> bool:
        return request.context.risk_score <= self.max_risk_score

class RiskEngine:
    def calculate_risk(self, context: SecurityContext) -> float:
        """Calculate risk score based on various factors."""
        risk_factors = []

        # Location risk
        if self._is_high_risk_location(context.location):
            risk_factors.append(0.3)

        # Device risk
        if not self._is_known_device(context.device_id):
            risk_factors.append(0.4)

        # Time-based risk
        if self._is_unusual_time(context.authentication_time):
            risk_factors.append(0.2)

        # Behavioral risk
        behavioral_risk = self._calculate_behavioral_risk(context.user_id)
        risk_factors.append(behavioral_risk)

        # Combine risk factors
        total_risk = min(sum(risk_factors), 1.0)
        return total_risk

    def _is_high_risk_location(self, location: str) -> bool:
        # Implementation to check if location is high risk
        return False

    def _is_known_device(self, device_id: str) -> bool:
        # Implementation to check if device is known
        return True

    def _is_unusual_time(self, auth_time: float) -> bool:
        # Implementation to check if access time is unusual
        return False

    def _calculate_behavioral_risk(self, user_id: str) -> float:
        # Implementation to calculate behavioral risk
        return 0.1

class AuditLogger:
    def log_access_decision(self, decision: Dict[str, Any]):
        """Log access decision for audit purposes."""
        # Implementation to log to secure audit system
        print(f"AUDIT: {decision}")

# Usage example
def setup_zero_trust():
    zt_controller = ZeroTrustAccessControl()

    # Add policies
    zt_controller.add_policy(IdentityVerificationPolicy(mfa_required=True))
    zt_controller.add_policy(LocationPolicy(
        allowed_countries=['US', 'CA', 'UK'],
        allowed_ip_ranges=['10.0.0.0/8', '192.168.0.0/16']
    ))
    zt_controller.add_policy(DeviceCompliancePolicy(device_registry=None))
    zt_controller.add_policy(RiskBasedPolicy(max_risk_score=0.6))

    return zt_controller
```

### 1.2 Network Micro-Segmentation

#### Software-Defined Perimeters **[REQUIRED]**

```yaml
# Kubernetes Network Policies for Micro-segmentation
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: zero-trust-web-tier
  namespace: production
spec:
  podSelector:
    matchLabels:
      tier: web
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-system
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          tier: api
    ports:
    - protocol: TCP
      port: 3000
  - to: []
    ports:
    - protocol: TCP
      port: 53
    - protocol: UDP
      port: 53

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: zero-trust-api-tier
  namespace: production
spec:
  podSelector:
    matchLabels:
      tier: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          tier: web
    ports:
    - protocol: TCP
      port: 3000
  egress:
  - to:
    - podSelector:
        matchLabels:
          tier: database
    ports:
    - protocol: TCP
      port: 5432
```

#### Service Mesh Security **[REQUIRED]**

```yaml
# Istio Authorization Policies
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: zero-trust-api-access
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-service
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/web-service"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/v1/*"]
    when:
    - key: request.headers[x-user-id]
      values: ["*"]
    - key: request.headers[authorization]
      values: ["Bearer *"]

---
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: zero-trust-mtls
  namespace: production
spec:
  mtls:
    mode: STRICT

---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: zero-trust-circuit-breaker
spec:
  host: api-service
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        maxRequestsPerConnection: 10
```

---

## 2. Supply Chain Security

### 2.1 Software Bill of Materials (SBOM)

#### SBOM Generation **[REQUIRED]**

```yaml
# GitHub Actions workflow for SBOM generation
name: Generate SBOM

on:
  push:
    branches: [ main ]
  release:
    types: [ published ]

jobs:
  generate-sbom:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write

    steps:
      - uses: actions/checkout@v4

      - name: Generate SBOM with Syft
        uses: anchore/sbom-action@v0
        with:
          artifact-name: sbom.spdx.json
          format: spdx-json

      - name: Generate SBOM with CycloneDX
        run: |
          npm install -g @cyclonedx/cdxgen
          cdxgen -o sbom-cyclonedx.json

      - name: Scan SBOM for vulnerabilities
        uses: anchore/scan-action@v3
        with:
          sbom: sbom.spdx.json
          fail-build: true
          severity-cutoff: critical

      - name: Upload SBOM artifacts
        uses: actions/upload-artifact@v3
        with:
          name: sbom-files
          path: |
            sbom.spdx.json
            sbom-cyclonedx.json

      - name: Publish SBOM to registry
        run: |
          # Upload to container registry as OCI artifact
          oras push ghcr.io/${{ github.repository }}/sbom:${{ github.sha }} \
            sbom.spdx.json:application/spdx+json
```

#### Dependency Verification **[REQUIRED]**

```python
# Supply chain verification system
import hashlib
import json
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PackageMetadata:
    name: str
    version: str
    hash_sha256: str
    source_url: str
    maintainers: List[str]
    signature: Optional[str]
    published_date: datetime
    vulnerability_count: int

class SupplyChainValidator:
    def __init__(self, trusted_registries: List[str]):
        self.trusted_registries = trusted_registries
        self.vulnerability_db = VulnerabilityDatabase()
        self.signature_validator = SignatureValidator()

    def validate_package(self, package: PackageMetadata) -> Dict[str, any]:
        """Validate a package against supply chain security policies."""
        results = {
            'package': package.name,
            'version': package.version,
            'valid': True,
            'issues': [],
            'risk_score': 0.0
        }

        # Check if package is from trusted registry
        if not self._is_from_trusted_registry(package.source_url):
            results['issues'].append('Package not from trusted registry')
            results['risk_score'] += 0.3

        # Verify package signature
        if not self.signature_validator.verify(package):
            results['issues'].append('Invalid or missing package signature')
            results['risk_score'] += 0.4

        # Check for known vulnerabilities
        vulnerabilities = self.vulnerability_db.get_vulnerabilities(
            package.name, package.version
        )
        if vulnerabilities:
            critical_vulns = [v for v in vulnerabilities if v.severity == 'critical']
            if critical_vulns:
                results['issues'].append(f'Critical vulnerabilities found: {len(critical_vulns)}')
                results['risk_score'] += 0.5

        # Check package age and maintenance
        if self._is_unmaintained(package):
            results['issues'].append('Package appears unmaintained')
            results['risk_score'] += 0.2

        # Check for suspicious patterns
        if self._has_suspicious_patterns(package):
            results['issues'].append('Suspicious patterns detected')
            results['risk_score'] += 0.6

        results['valid'] = results['risk_score'] < 0.7
        return results

    def _is_from_trusted_registry(self, source_url: str) -> bool:
        return any(registry in source_url for registry in self.trusted_registries)

    def _is_unmaintained(self, package: PackageMetadata) -> bool:
        # Check if package hasn't been updated in over a year
        age_days = (datetime.now() - package.published_date).days
        return age_days > 365

    def _has_suspicious_patterns(self, package: PackageMetadata) -> bool:
        suspicious_patterns = [
            'eval',
            'exec',
            'process.env',
            'child_process',
            'crypto-mining',
            'bitcoin',
            'monero'
        ]
        # This is simplified - real implementation would analyze package contents
        return any(pattern in package.name.lower() for pattern in suspicious_patterns)

class VulnerabilityDatabase:
    def get_vulnerabilities(self, package_name: str, version: str) -> List[Dict]:
        """Get known vulnerabilities for a package version."""
        # Integration with vulnerability databases like OSV, NVD, etc.
        return []

class SignatureValidator:
    def verify(self, package: PackageMetadata) -> bool:
        """Verify package signature."""
        if not package.signature:
            return False

        # Implement signature verification logic
        return True

# Gradle configuration for dependency verification
gradle_verification = """
// gradle/verification-metadata.xml
<?xml version="1.0" encoding="UTF-8"?>
<verification-metadata>
   <configuration>
      <verify-metadata>true</verify-metadata>
      <verify-signatures>true</verify-signatures>
      <trusted-artifacts>
         <trust group="org.springframework" name="spring-core"/>
         <trust group="com.fasterxml.jackson.core"/>
      </trusted-artifacts>
      <ignored-keys>
         <ignored-key id="some-ignored-key"/>
      </ignored-keys>
   </configuration>
   <components>
      <component group="org.springframework" name="spring-core" version="5.3.21">
         <artifact name="spring-core-5.3.21.jar">
            <sha256 value="abcd1234..." origin="gradle verification"/>
         </artifact>
      </component>
   </components>
</verification-metadata>
"""
```

### 2.2 Container Image Security

#### Image Scanning Pipeline **[REQUIRED]**

```yaml
# Container security scanning workflow
name: Container Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  security-scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
      packages: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build image
        run: |
          docker build -t ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} .

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Run Grype vulnerability scanner
        uses: anchore/scan-action@v3
        with:
          image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          fail-build: true
          severity-cutoff: critical
          acs-report-enable: true

      - name: Run Docker Scout
        uses: docker/scout-action@v1
        with:
          command: cves
          image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          exit-code: true
          only-severities: critical,high

      - name: Sign container image
        uses: sigstore/cosign-installer@v3
      - run: |
          cosign sign --yes ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        env:
          COSIGN_EXPERIMENTAL: 1

      - name: Generate SLSA provenance
        uses: slsa-framework/slsa-github-generator/\
              .github/workflows/generator_container_slsa3.yml@v1.7.0
        with:
          image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          digest: ${{ steps.build.outputs.digest }}
          registry-username: ${{ github.actor }}
          registry-password: ${{ secrets.GITHUB_TOKEN }}

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'
```

#### Secure Container Configuration **[REQUIRED]**

```dockerfile
# Secure Dockerfile example
FROM node:18-alpine AS builder

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM node:18-alpine AS runner

# Security updates
RUN apk update && apk upgrade

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Set working directory
WORKDIR /app

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Run application
CMD ["npm", "start"]
```

### 2.3 Code Signing and Attestation

#### Sigstore Integration **[REQUIRED]**

```yaml
# Sigstore signing workflow
name: Sign and Attest

on:
  release:
    types: [published]

permissions:
  contents: read
  id-token: write
  packages: write
  attestations: write

jobs:
  sign-attest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Cosign
        uses: sigstore/cosign-installer@v3

      - name: Install Rekor CLI
        run: |
          wget https://github.com/sigstore/rekor/releases/latest/download/rekor-cli-linux-amd64
          chmod +x rekor-cli-linux-amd64
          sudo mv rekor-cli-linux-amd64 /usr/local/bin/rekor-cli

      - name: Build artifact
        run: |
          npm run build
          tar -czf release.tar.gz dist/

      - name: Sign artifact with Cosign
        run: |
          cosign sign-blob --yes release.tar.gz \
            --output-signature release.tar.gz.sig \
            --output-certificate release.tar.gz.crt
        env:
          COSIGN_EXPERIMENTAL: 1

      - name: Create SLSA attestation
        uses: actions/attest-build-provenance@v1
        with:
          subject-path: release.tar.gz

      - name: Verify signature
        run: |
          cosign verify-blob release.tar.gz \
            --signature release.tar.gz.sig \
            --certificate release.tar.gz.crt \
            --certificate-identity-regexp '^https://github\.com/${{ github.repository }}/' \
            --certificate-oidc-issuer https://token.actions.githubusercontent.com
        env:
          COSIGN_EXPERIMENTAL: 1

      - name: Upload signed artifacts
        uses: actions/upload-release-asset@v1
        with:
          upload_url: ${{ github.event.release.upload_url }}
          asset_path: release.tar.gz
          asset_name: release.tar.gz
          asset_content_type: application/gzip
```

---

## 3. Container and Kubernetes Security

### 3.1 Runtime Security

#### Falco Security Monitoring **[REQUIRED]**

```yaml
# Falco rules for runtime security
- rule: Unexpected Network Traffic
  desc: Detect unexpected network connections from containers
  condition: >
    (inbound_outbound) and
    container and
    not proc.name in (allowed_network_processes) and
    not fd.typechar = 'f'
  output: >
    Unexpected network traffic detected
    (user=%user.name command=%proc.cmdline connection=%fd.name container=%container.info)
  priority: WARNING
  tags: [network, container]

- rule: Suspicious File Access
  desc: Detect access to sensitive files
  condition: >
    open_read and
    container and
    (fd.name startswith /etc/passwd or
     fd.name startswith /etc/shadow or
     fd.name startswith /etc/sudoers or
     fd.name startswith /root/.ssh)
  output: >
    Sensitive file accessed
    (user=%user.name command=%proc.cmdline file=%fd.name container=%container.info)
  priority: CRITICAL
  tags: [filesystem, container]

- rule: Container Privilege Escalation
  desc: Detect privilege escalation attempts
  condition: >
    spawned_process and
    container and
    proc.name in (su, sudo, setuid, setgid, chmod) and
    not user.name in (allowed_users)
  output: >
    Privilege escalation attempt
    (user=%user.name command=%proc.cmdline container=%container.info)
  priority: CRITICAL
  tags: [privilege_escalation, container]

- rule: Cryptocurrency Mining
  desc: Detect potential cryptocurrency mining
  condition: >
    spawned_process and
    container and
    (proc.name contains "xmrig" or
     proc.name contains "minerd" or
     proc.name contains "cpuminer" or
     proc.cmdline contains "stratum" or
     proc.cmdline contains "pool.minergate.com")
  output: >
    Potential cryptocurrency mining detected
    (user=%user.name command=%proc.cmdline container=%container.info)
  priority: CRITICAL
  tags: [malware, container]
```

#### Container Runtime Security **[REQUIRED]**

```yaml
# gVisor runsc configuration
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc

---
# Pod with gVisor runtime
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
spec:
  runtimeClassName: gvisor
  securityContext:
    runAsNonRoot: true
    runAsUser: 1001
    runAsGroup: 1001
    fsGroup: 1001
    seccompProfile:
      type: RuntimeDefault
    supplementalGroups: [1001]
  containers:
  - name: app
    image: secure-app:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE
    resources:
      limits:
        memory: "256Mi"
        cpu: "500m"
      requests:
        memory: "128Mi"
        cpu: "250m"
    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: cache
      mountPath: /app/cache
  volumes:
  - name: tmp
    emptyDir: {}
  - name: cache
    emptyDir: {}
```

### 3.2 Pod Security Standards

#### Pod Security Policies **[REQUIRED]**

```yaml
# Pod Security Standards enforcement
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted

---
# Security Context Constraints (OpenShift)
apiVersion: security.openshift.io/v1
kind: SecurityContextConstraints
metadata:
  name: restricted-scc
allowHostDirVolumePlugin: false
allowHostIPC: false
allowHostNetwork: false
allowHostPID: false
allowHostPorts: false
allowPrivilegeEscalation: false
allowPrivilegedContainer: false
allowedCapabilities: null
defaultAddCapabilities: null
requiredDropCapabilities:
- KILL
- MKNOD
- SETUID
- SETGID
fsGroup:
  type: MustRunAs
  ranges:
  - min: 1
    max: 65535
runAsUser:
  type: MustRunAsNonRoot
seLinuxContext:
  type: MustRunAs
supplementalGroups:
  type: MustRunAs
  ranges:
  - min: 1
    max: 65535
volumes:
- configMap
- downwardAPI
- emptyDir
- persistentVolumeClaim
- projected
- secret
```

#### Admission Controllers **[REQUIRED]**

```yaml
# Open Policy Agent (OPA) Gatekeeper policies
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredsecuritycontext
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredSecurityContext
      validation:
        properties:
          runAsNonRoot:
            type: boolean
          readOnlyRootFilesystem:
            type: boolean
          allowPrivilegeEscalation:
            type: boolean
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredsecuritycontext

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not container.securityContext.runAsNonRoot
          msg := "Container must run as non-root user"
        }

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not container.securityContext.readOnlyRootFilesystem
          msg := "Container must have read-only root filesystem"
        }

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          container.securityContext.allowPrivilegeEscalation
          msg := "Container must not allow privilege escalation"
        }

---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredSecurityContext
metadata:
  name: must-have-security-context
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
    namespaces: ["production", "staging"]
  parameters:
    runAsNonRoot: true
    readOnlyRootFilesystem: true
    allowPrivilegeEscalation: false
```

### 3.3 Network Security

#### Network Policies **[REQUIRED]**

```yaml
# Default deny-all network policy
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
# Application-specific network policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-app-netpol
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: web-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
  egress:
  # Allow DNS
  - to: []
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
  # Allow API calls
  - to:
    - podSelector:
        matchLabels:
          app: api-server
    ports:
    - protocol: TCP
      port: 3000
  # Allow database access
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
```

---

## 4. API Security

<!-- @nist-controls: [ac-3, ac-6, ia-2, ia-5, sc-8, sc-13, si-10, au-2] -->

### 4.1 API Gateway Security

#### Rate Limiting and Throttling **[REQUIRED]**

```yaml
# Kong API Gateway rate limiting
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: rate-limit-plugin
config:
  minute: 100
  hour: 1000
  policy: cluster
  hide_client_headers: false
  fault_tolerant: true
plugin: rate-limiting

---
# Apply rate limiting to API
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  annotations:
    konghq.com/plugins: rate-limit-plugin,auth-plugin
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
```

#### API Authentication and Authorization **[REQUIRED]**

```python
# FastAPI security implementation
# @nist ia-2 "API authentication"
# @nist ac-3 "API authorization"
# @nist sc-8 "HTTPS enforcement"
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import jwt
from typing import List, Optional
import time
from pydantic import BaseModel

app = FastAPI(
    title="Secure API",
    docs_url=None,  # Disable docs in production
    redoc_url=None,
    openapi_url=None
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["api.example.com", "*.example.com"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Rate-Limit-Remaining"]
)

security = HTTPBearer()

class TokenData(BaseModel):
    user_id: str
    scopes: List[str]
    exp: int
    iat: int

class SecurityConfig:
    JWT_SECRET = "your-secret-key"
    JWT_ALGORITHM = "HS256"
    TOKEN_EXPIRE_SECONDS = 3600
    RATE_LIMIT_PER_MINUTE = 60

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> TokenData:
    """Verify and decode JWT token.
    @nist ia-5 "Token verification"
    @nist ac-12 "Session expiration check"
    """
    try:
        payload = jwt.decode(
            credentials.credentials,
            SecurityConfig.JWT_SECRET,
            algorithms=[SecurityConfig.JWT_ALGORITHM]
        )

        # Check token expiration
        # @nist ac-12 "Enforce session termination"
        if payload.get("exp", 0) < time.time():
            raise HTTPException(status_code=401, detail="Token expired")

        return TokenData(**payload)

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def require_scope(required_scope: str):
    """Dependency for checking required scopes."""
    def scope_checker(token_data: TokenData = Depends(verify_token)):
        if required_scope not in token_data.scopes:
            raise HTTPException(
                status_code=403,
                detail=f"Insufficient permissions. Required: {required_scope}"
            )
        return token_data
    return scope_checker

# Rate limiting decorator
from functools import wraps
import redis
import asyncio

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def rate_limit(max_requests: int = 60, window_seconds: int = 60):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get client IP or user ID
            request = kwargs.get('request')
            if request:
                client_id = request.client.host
            else:
                # Fallback to user ID from token
                token_data = kwargs.get('token_data')
                client_id = token_data.user_id if token_data else 'anonymous'

            # Check rate limit
            key = f"rate_limit:{client_id}"
            current_requests = redis_client.get(key)

            if current_requests is None:
                redis_client.setex(key, window_seconds, 1)
            elif int(current_requests) >= max_requests:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded",
                    headers={"Retry-After": str(window_seconds)}
                )
            else:
                redis_client.incr(key)

            return await func(*args, **kwargs)
        return wrapper
    return decorator

# API endpoints with security
@app.get("/api/users/{user_id}")
@rate_limit(max_requests=100, window_seconds=60)
async def get_user(
    user_id: str,
    token_data: TokenData = Depends(require_scope("users:read"))
):
    """Get user information."""
    # Verify user can access this user ID
    if token_data.user_id != user_id and "admin" not in token_data.scopes:
        raise HTTPException(status_code=403, detail="Access denied")

    # Implementation here
    return {"user_id": user_id, "data": "user data"}

@app.post("/api/users")
@rate_limit(max_requests=10, window_seconds=60)
async def create_user(
    user_data: dict,
    token_data: TokenData = Depends(require_scope("users:write"))
):
    """Create a new user."""
    # Input validation
    if not validate_user_input(user_data):
        raise HTTPException(status_code=400, detail="Invalid input")

    # Implementation here
    return {"message": "User created"}

def validate_user_input(data: dict) -> bool:
    """Validate user input data."""
    required_fields = ["email", "name"]

    # Check required fields
    for field in required_fields:
        if field not in data:
            return False

    # Validate email format
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, data.get("email", "")):
        return False

    # Additional validation rules
    return True

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)

    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response
```

### 4.2 API Vulnerability Testing

#### Automated Security Testing **[REQUIRED]**

```python
# API security testing with OWASP ZAP
import zapv2
import time
import json
from typing import Dict, List

class APISecurityTester:
    def __init__(self, zap_proxy_url: str = "http://127.0.0.1:8080"):
        self.zap = zapv2.ZAPv2(proxies={'http': zap_proxy_url, 'https': zap_proxy_url})

    def security_test_api(self, target_url: str, api_spec_path: str) -> Dict:
        """Perform comprehensive API security testing."""
        results = {
            'target': target_url,
            'timestamp': time.time(),
            'tests': {},
            'vulnerabilities': [],
            'risk_score': 0.0
        }

        try:
            # Import API specification
            with open(api_spec_path, 'r') as f:
                api_spec = json.load(f)

            # Spider the API
            spider_id = self.zap.spider.scan(target_url)
            self._wait_for_completion(spider_id, 'spider')

            # Passive scan
            self.zap.pscan.enable_all_scanners()
            while int(self.zap.pscan.records_to_scan) > 0:
                time.sleep(2)

            # Active scan
            active_scan_id = self.zap.ascan.scan(target_url)
            self._wait_for_completion(active_scan_id, 'ascan')

            # API-specific tests
            results['tests']['injection_attacks'] = self._test_injection_attacks(target_url)
            results['tests']['authentication_bypass'] = self._test_auth_bypass(target_url)
            results['tests']['authorization_flaws'] = self._test_authorization(target_url)
            results['tests']['input_validation'] = self._test_input_validation(target_url, api_spec)
            results['tests']['rate_limiting'] = self._test_rate_limiting(target_url)

            # Get vulnerabilities
            alerts = self.zap.core.alerts()
            for alert in alerts:
                results['vulnerabilities'].append({
                    'name': alert['alert'],
                    'risk': alert['risk'],
                    'confidence': alert['confidence'],
                    'description': alert['description'],
                    'solution': alert['solution'],
                    'url': alert['url']
                })

            # Calculate risk score
            results['risk_score'] = self._calculate_risk_score(results['vulnerabilities'])

        except Exception as e:
            results['error'] = str(e)

        return results

    def _test_injection_attacks(self, target_url: str) -> Dict:
        """Test for injection vulnerabilities."""
        injection_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "<script>alert('xss')</script>",
            "{{7*7}}",  # Template injection
            "../../../etc/passwd",  # Path traversal
        ]

        vulnerabilities = []
        for payload in injection_payloads:
            # Test each endpoint with payload
            try:
                response = self.zap.core.send_request(
                    f"{target_url}/api/test?param={payload}",
                    followRedirects=True
                )

                if self._detect_injection_response(response, payload):
                    vulnerabilities.append({
                        'payload': payload,
                        'response_code': response.get('statusCode'),
                        'evidence': response.get('responseBody', '')[:200]
                    })
            except Exception:
                pass

        return {
            'passed': len(vulnerabilities) == 0,
            'vulnerabilities_found': len(vulnerabilities),
            'details': vulnerabilities
        }

    def _test_auth_bypass(self, target_url: str) -> Dict:
        """Test for authentication bypass vulnerabilities."""
        bypass_tests = [
            {'method': 'missing_token', 'headers': {}},
            {'method': 'invalid_token', 'headers': {'Authorization': 'Bearer invalid_token'}},
            {'method': 'expired_token', 'headers': {'Authorization': 'Bearer expired_token'}},
            {'method': 'malformed_token', 'headers': {'Authorization': 'malformed'}},
        ]

        bypassed = []
        for test in bypass_tests:
            try:
                response = self.zap.core.send_request(
                    f"{target_url}/api/protected",
                    requestheader=test['headers']
                )

                # Check if request succeeded when it shouldn't
                if response.get('statusCode') == 200:
                    bypassed.append(test['method'])
            except Exception:
                pass

        return {
            'passed': len(bypassed) == 0,
            'bypassed_methods': bypassed
        }

    def _test_rate_limiting(self, target_url: str) -> Dict:
        """Test rate limiting implementation."""
        request_count = 0
        rate_limited = False

        # Send rapid requests
        for i in range(100):
            try:
                response = self.zap.core.send_request(f"{target_url}/api/test")
                request_count += 1

                if response.get('statusCode') == 429:  # Too Many Requests
                    rate_limited = True
                    break

            except Exception:
                break

        return {
            'passed': rate_limited,
            'requests_before_limit': request_count,
            'rate_limiting_active': rate_limited
        }

    def _detect_injection_response(self, response: Dict, payload: str) -> bool:
        """Detect if response indicates successful injection."""
        response_body = response.get('responseBody', '').lower()

        # SQL injection indicators
        sql_errors = ['sql syntax', 'mysql_fetch', 'ora-', 'postgresql error']
        if any(error in response_body for error in sql_errors):
            return True

        # XSS indicators
        if payload.lower() in response_body:
            return True

        # Template injection indicators
        if payload == "{{7*7}}" and "49" in response_body:
            return True

        return False

    def _calculate_risk_score(self, vulnerabilities: List[Dict]) -> float:
        """Calculate overall risk score based on vulnerabilities."""
        risk_weights = {'High': 0.4, 'Medium': 0.2, 'Low': 0.1, 'Informational': 0.05}
        total_risk = 0.0

        for vuln in vulnerabilities:
            risk_level = vuln.get('risk', 'Low')
            total_risk += risk_weights.get(risk_level, 0.1)

        return min(total_risk, 1.0)  # Cap at 1.0

    def _wait_for_completion(self, scan_id: str, scan_type: str):
        """Wait for scan to complete."""
        while True:
            if scan_type == 'spider':
                progress = int(self.zap.spider.status(scan_id))
            elif scan_type == 'ascan':
                progress = int(self.zap.ascan.status(scan_id))

            if progress >= 100:
                break

            time.sleep(5)

# Usage
if __name__ == "__main__":
    tester = APISecurityTester()
    results = tester.security_test_api(
        target_url="https://api.example.com",
        api_spec_path="openapi.json"
    )

    print(f"Security test completed. Risk score: {results['risk_score']}")
    print(f"Vulnerabilities found: {len(results['vulnerabilities'])}")
```

---

## 5. DevSecOps Integration

### 5.1 Security in CI/CD Pipeline

#### Comprehensive Security Pipeline **[REQUIRED]**

```yaml
# .github/workflows/devsecops.yml
name: DevSecOps Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  DOCKER_REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  static-analysis:
    name: Static Security Analysis
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # Secret scanning
      - name: Run GitLeaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      # SAST scanning
      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten

      # CodeQL Analysis
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: javascript, python
          queries: security-and-quality

      - name: Autobuild
        uses: github/codeql-action/autobuild@v2

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v2

      # License scanning
      - name: FOSSA Scan
        uses: fossas/fossa-action@main
        with:
          api-key: ${{ secrets.FOSSA_API_KEY }}
          run-tests: true

  dependency-security:
    name: Dependency Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # npm audit
      - name: npm audit
        run: |
          npm audit --audit-level high
          npm audit --json > npm-audit.json

      # Snyk vulnerability scan
      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

      # OSV Scanner
      - name: Run OSV Scanner
        uses: google/osv-scanner-action@v1
        with:
          scan-args: |-
            -r
            --skip-git
            ./

      # Dependency Check
      - name: Run OWASP Dependency Check
        uses: dependency-check/Dependency-Check_Action@main
        with:
          project: 'test'
          path: '.'
          format: 'ALL'
          args: >
            --enableRetired
            --enableExperimental
            --failOnCVSS 7

  container-security:
    name: Container Security Scan
    runs-on: ubuntu-latest
    needs: [static-analysis, dependency-security]
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: |
          docker build -t ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} .

      # Dockerfile security scan
      - name: Run Hadolint
        uses: hadolint/hadolint-action@v3.1.0
        with:
          dockerfile: Dockerfile
          failure-threshold: error

      # Multi-scanner approach
      - name: Run Trivy Scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Run Grype Scanner
        uses: anchore/scan-action@v3
        with:
          image: ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          fail-build: true
          severity-cutoff: critical

      - name: Run Clair Scanner
        run: |
          docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
            quay.io/coreos/clair:latest \
            analyze ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

      # Sign container if security checks pass
      - name: Install Cosign
        if: github.event_name != 'pull_request'
        uses: sigstore/cosign-installer@v3

      - name: Sign container image
        if: github.event_name != 'pull_request'
        run: |
          cosign sign --yes ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        env:
          COSIGN_EXPERIMENTAL: 1

  infrastructure-security:
    name: Infrastructure Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Terraform security scanning
      - name: Run Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: ./terraform
          framework: terraform
          output_format: sarif
          output_file_path: checkov-results.sarif
          quiet: true
          soft_fail: false

      # Kubernetes security scanning
      - name: Run Kubesec
        run: |
          curl -sSL https://github.com/controlplaneio/kubesec/releases/latest/\
download/kubesec_linux_amd64.tar.gz | tar xz
          ./kubesec scan k8s/*.yaml

      # Cloud formation security
      - name: Run CFN-Nag
        if: hashFiles('cloudformation/**/*.yml') != ''
        run: |
          gem install cfn-nag
          cfn_nag_scan --input-path cloudformation/

  dynamic-security-testing:
    name: Dynamic Security Testing
    runs-on: ubuntu-latest
    needs: [container-security]
    if: github.event_name != 'pull_request'
    steps:
      - uses: actions/checkout@v4

      # Start application for testing
      - name: Start application
        run: |
          docker-compose -f docker-compose.test.yml up -d
          sleep 30

      # OWASP ZAP Baseline scan
      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.7.0
        with:
          target: 'http://localhost:3000'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a'

      # ZAP Full Scan
      - name: ZAP Full Scan
        uses: zaproxy/action-full-scan@v0.4.0
        with:
          target: 'http://localhost:3000'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a'

      # Custom API security tests
      - name: API Security Tests
        run: |
          python tests/security/api_security_tests.py

      - name: Cleanup
        if: always()
        run: |
          docker-compose -f docker-compose.test.yml down

  security-report:
    name: Security Report
    runs-on: ubuntu-latest
    needs: [static-analysis, dependency-security, container-security, infrastructure-security]
    if: always()
    steps:
      - name: Generate Security Report
        run: |
          echo "# Security Scan Results" > security-report.md
          echo "## Summary" >> security-report.md
          echo "- Static Analysis: ${{ needs.static-analysis.result }}" >> security-report.md
          echo "- Dependency Scan: ${{ needs.dependency-security.result }}" >> security-report.md
          echo "- Container Scan: ${{ needs.container-security.result }}" >> security-report.md
          echo "- Infrastructure Scan: ${{ needs.infrastructure-security.result }}" \
            >> security-report.md

      - name: Upload Security Report
        uses: actions/upload-artifact@v3
        with:
          name: security-report
          path: security-report.md

      # Notify security team if any failures
      - name: Notify Security Team
        if: contains(needs.*.result, 'failure')
        uses: 8398a7/action-slack@v3
        with:
          status: failure
          text: 'Security scan failures detected in ${{ github.repository }}'
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SECURITY_SLACK_WEBHOOK }}
```

### 5.2 Security Gates and Policies

#### Policy as Code **[REQUIRED]**

```python
# Security policy engine
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import re

class SeverityLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class SecurityFinding:
    rule_id: str
    title: str
    description: str
    severity: SeverityLevel
    file_path: str
    line_number: Optional[int]
    evidence: str
    remediation: str

@dataclass
class PolicyViolation:
    policy_name: str
    description: str
    severity: SeverityLevel
    findings: List[SecurityFinding]

class SecurityPolicy(ABC):
    @abstractmethod
    def evaluate(self, scan_results: Dict[str, Any]) -> List[PolicyViolation]:
        pass

class CriticalVulnerabilityPolicy(SecurityPolicy):
    """Policy: No critical vulnerabilities allowed in production."""

    def evaluate(self, scan_results: Dict[str, Any]) -> List[PolicyViolation]:
        violations = []

        # Check dependency vulnerabilities
        dep_vulns = scan_results.get('dependency_scan', {}).get('vulnerabilities', [])
        critical_deps = [v for v in dep_vulns if v.get('severity') == 'critical']

        if critical_deps:
            violations.append(PolicyViolation(
                policy_name="no_critical_dependencies",
                description="Critical vulnerabilities found in dependencies",
                severity=SeverityLevel.CRITICAL,
                findings=[
                    SecurityFinding(
                        rule_id="CRIT_DEP",
                        title=f"Critical vulnerability in {v['package']}",
                        description=v['description'],
                        severity=SeverityLevel.CRITICAL,
                        file_path=v.get('file_path', 'package.json'),
                        line_number=None,
                        evidence=v['cve_id'],
                        remediation=f"Update {v['package']} to version "
                                   f"{v.get('fixed_version', 'latest')}"
                    ) for v in critical_deps
                ]
            ))

        # Check container vulnerabilities
        container_vulns = scan_results.get('container_scan', {}).get('vulnerabilities', [])
        critical_container = [v for v in container_vulns if v.get('severity') == 'CRITICAL']

        if critical_container:
            violations.append(PolicyViolation(
                policy_name="no_critical_container_vulns",
                description="Critical vulnerabilities found in container images",
                severity=SeverityLevel.CRITICAL,
                findings=[
                    SecurityFinding(
                        rule_id="CRIT_CONTAINER",
                        title=f"Critical vulnerability in container",
                        description=v['description'],
                        severity=SeverityLevel.CRITICAL,
                        file_path="Dockerfile",
                        line_number=None,
                        evidence=v.get('vulnerability_id', ''),
                        remediation="Update base image or affected packages"
                    ) for v in critical_container
                ]
            ))

        return violations

class SecretsPolicy(SecurityPolicy):
    """Policy: No secrets allowed in source code."""

    def __init__(self):
        self.secret_patterns = [
            (r'api[_-]?key[_-]?=\s*["\']([a-zA-Z0-9]{20,})["\']', 'API Key'),
            (r'password[_-]?=\s*["\']([^"\']{8,})["\']', 'Password'),
            (r'secret[_-]?=\s*["\']([a-zA-Z0-9]{20,})["\']', 'Secret'),
            (r'token[_-]?=\s*["\']([a-zA-Z0-9]{20,})["\']', 'Token'),
            (r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----', 'Private Key'),
        ]

    def evaluate(self, scan_results: Dict[str, Any]) -> List[PolicyViolation]:
        violations = []
        secret_findings = scan_results.get('secret_scan', {}).get('findings', [])

        if secret_findings:
            violations.append(PolicyViolation(
                policy_name="no_secrets_in_code",
                description="Secrets found in source code",
                severity=SeverityLevel.CRITICAL,
                findings=[
                    SecurityFinding(
                        rule_id="SECRET_EXPOSED",
                        title=f"Secret found: {finding['type']}",
                        description="Hardcoded secret detected in source code",
                        severity=SeverityLevel.CRITICAL,
                        file_path=finding['file'],
                        line_number=finding.get('line', None),
                        evidence=finding['match'][:50] + "...",
                        remediation="Remove secret and use environment "
                                   "variables or secret management"
                    ) for finding in secret_findings
                ]
            ))

        return violations

class SecurityCompliancePolicy(SecurityPolicy):
    """Policy: Enforce security compliance requirements."""

    def evaluate(self, scan_results: Dict[str, Any]) -> List[PolicyViolation]:
        violations = []

        # Check for security headers
        security_headers = scan_results.get('dynamic_scan', {}).get('security_headers', {})
        missing_headers = []

        required_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options',
            'X-XSS-Protection',
            'Strict-Transport-Security',
            'Content-Security-Policy'
        ]

        for header in required_headers:
            if not security_headers.get(header):
                missing_headers.append(header)

        if missing_headers:
            violations.append(PolicyViolation(
                policy_name="security_headers_required",
                description="Missing required security headers",
                severity=SeverityLevel.MEDIUM,
                findings=[
                    SecurityFinding(
                        rule_id="MISSING_HEADER",
                        title=f"Missing security header: {header}",
                        description="Required security header not found",
                        severity=SeverityLevel.MEDIUM,
                        file_path="application configuration",
                        line_number=None,
                        evidence=f"Header '{header}' not present",
                        remediation=f"Add {header} header to application configuration"
                    ) for header in missing_headers
                ]
            ))

        return violations

class SecurityPolicyEngine:
    def __init__(self):
        self.policies = [
            CriticalVulnerabilityPolicy(),
            SecretsPolicy(),
            SecurityCompliancePolicy(),
        ]

    def evaluate_all_policies(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate all security policies against scan results."""
        all_violations = []

        for policy in self.policies:
            violations = policy.evaluate(scan_results)
            all_violations.extend(violations)

        # Categorize violations by severity
        critical_violations = [v for v in all_violations if v.severity == SeverityLevel.CRITICAL]
        high_violations = [v for v in all_violations if v.severity == SeverityLevel.HIGH]

        # Determine if deployment should be blocked
        block_deployment = len(critical_violations) > 0

        return {
            'policy_evaluation_passed': not block_deployment,
            'block_deployment': block_deployment,
            'total_violations': len(all_violations),
            'critical_violations': len(critical_violations),
            'high_violations': len(high_violations),
            'violations': [
                {
                    'policy': v.policy_name,
                    'description': v.description,
                    'severity': v.severity.value,
                    'findings_count': len(v.findings),
                    'findings': [
                        {
                            'rule_id': f.rule_id,
                            'title': f.title,
                            'file': f.file_path,
                            'line': f.line_number,
                            'evidence': f.evidence,
                            'remediation': f.remediation
                        } for f in v.findings
                    ]
                } for v in all_violations
            ]
        }

# Usage in CI/CD
def main():
    # Load scan results from various security tools
    scan_results = {
        'dependency_scan': load_dependency_scan_results(),
        'container_scan': load_container_scan_results(),
        'secret_scan': load_secret_scan_results(),
        'dynamic_scan': load_dynamic_scan_results(),
    }

    # Evaluate policies
    policy_engine = SecurityPolicyEngine()
    evaluation_result = policy_engine.evaluate_all_policies(scan_results)

    # Output results
    print(f"Policy evaluation: "
          f"{'PASSED' if evaluation_result['policy_evaluation_passed'] else 'FAILED'}")
    print(f"Critical violations: {evaluation_result['critical_violations']}")
    print(f"High violations: {evaluation_result['high_violations']}")

    # Exit with appropriate code for CI/CD
    if evaluation_result['block_deployment']:
        print("🚫 Deployment blocked due to security policy violations")
        exit(1)
    else:
        print("✅ Security policies passed, deployment allowed")
        exit(0)

if __name__ == "__main__":
    main()
```

---

## Implementation Checklist

### Zero Trust Architecture

- [ ] Identity verification policies implemented
- [ ] Network micro-segmentation configured
- [ ] Risk-based access controls deployed
- [ ] Continuous monitoring active
- [ ] Policy engine operational

### Supply Chain Security

- [ ] SBOM generation automated
- [ ] Dependency verification enabled
- [ ] Container signing implemented
- [ ] Vulnerability scanning integrated
- [ ] Attestation pipeline configured

### Container Security

- [ ] Runtime security monitoring active
- [ ] Pod security standards enforced
- [ ] Network policies configured
- [ ] Admission controllers deployed
- [ ] Image scanning automated

### API Security

- [ ] Authentication and authorization implemented
- [ ] Rate limiting configured
- [ ] Input validation comprehensive
- [ ] Security headers applied
- [ ] Vulnerability testing automated

### DevSecOps Integration

- [ ] Security pipeline implemented
- [ ] Policy as code deployed
- [ ] Security gates configured
- [ ] Automated scanning enabled
- [ ] Compliance monitoring active

### Incident Response

- [ ] Response procedures documented
- [ ] Forensics capabilities ready
- [ ] Communication plans established
- [ ] Recovery procedures tested
- [ ] Lessons learned process active

---

## Related Standards

- [Coding Standards](CODING_STANDARDS.md) - Secure coding practices
- [Testing Standards](TESTING_STANDARDS.md) - Security testing requirements
- [Model Context Protocol Standards](MODEL_CONTEXT_PROTOCOL_STANDARDS.md) - Secure MCP implementation
- [Compliance Standards](COMPLIANCE_STANDARDS.md) - NIST compliance requirements

---

**End of Modern Security Standards**
