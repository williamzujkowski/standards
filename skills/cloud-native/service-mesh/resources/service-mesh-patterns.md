# Service Mesh Patterns and Anti-Patterns

## Proven Patterns

### 1. Progressive Traffic Shifting

**Pattern**: Gradually shift traffic to new versions using weighted routing.

**Implementation**:

- Start with 5-10% traffic to new version
- Monitor error rates, latency, and business metrics
- Double traffic every 15-30 minutes if metrics are healthy
- Roll back instantly if issues detected

**Benefits**:

- Reduced blast radius of bugs
- Confidence in production deployments
- Easy rollback mechanism

**Code Example**:

```bash
# Shift traffic: 10% → 25% → 50% → 100%
for weight in 10 25 50 100; do
  kubectl apply -f virtualservice-canary-$weight.yaml
  sleep 1800  # Wait 30 minutes
  # Check metrics before proceeding
done
```

---

### 2. Circuit Breaker with Graceful Degradation

**Pattern**: Detect failing services and fail fast to prevent cascade failures.

**Implementation**:

- Set conservative error thresholds (5 consecutive errors)
- Define ejection time (30s minimum)
- Limit max ejection to 50% of instances
- Implement fallback logic in application

**Benefits**:

- Prevents resource exhaustion
- Improves system resilience
- Faster error detection

**Configuration**:

```yaml
outlierDetection:
  consecutiveErrors: 5
  interval: 30s
  baseEjectionTime: 30s
  maxEjectionPercent: 50
```

---

### 3. Zero-Trust Security Model

**Pattern**: Deny all traffic by default, explicitly allow required communication.

**Implementation**:

1. Apply default deny-all policy
2. Enable strict mTLS cluster-wide
3. Create allow policies per service
4. Use service accounts for identity
5. Audit regularly with Kiali

**Benefits**:

- Defense in depth
- Compliance with security standards
- Clear communication boundaries

**Policy Structure**:

```yaml
# Step 1: Deny all
spec: {}
---
# Step 2: Allow specific
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/frontend"]
```

---

### 4. Shadow Traffic Testing

**Pattern**: Mirror production traffic to new version without impacting users.

**Implementation**:

- Mirror 10-100% of traffic to new version
- Compare response times and error rates
- Discard mirrored responses (users don't see them)
- Validate new version handles production load

**Benefits**:

- Real production testing without risk
- Validate performance under load
- Detect edge cases early

**Configuration**:

```yaml
mirror:
  host: api
  subset: v2
mirrorPercentage:
  value: 50.0
```

---

### 5. Locality-Aware Load Balancing

**Pattern**: Route traffic to nearby instances, failover to remote on failure.

**Implementation**:

- Define locality (region/zone) for each instance
- Configure distribution percentages
- Set failover targets
- Enable failoverPriority for multi-cluster

**Benefits**:

- Reduced latency
- Lower cross-AZ costs
- Better user experience

**Configuration**:

```yaml
localityLbSetting:
  enabled: true
  distribute:
  - from: us-west/*
    to:
      "us-west/zone1/*": 70
      "us-west/zone2/*": 30
  failover:
  - from: us-west/zone1
    to: us-west/zone2
```

---

### 6. Request-Level Authentication

**Pattern**: Validate JWT tokens at mesh level before reaching application.

**Implementation**:

- Configure RequestAuthentication with JWKS URI
- Validate issuer, audience, expiration
- Extract claims for authorization
- Forward validated token to application

**Benefits**:

- Centralized authentication
- No code changes required
- Consistent security across services

---

### 7. Retry Budget Pattern

**Pattern**: Limit retries to prevent retry storms.

**Implementation**:

- Set maximum retry attempts (2-3)
- Define per-try timeout (shorter than total)
- Only retry on specific errors (5xx, connection failure)
- Use exponential backoff (implicit in Istio)

**Configuration**:

```yaml
retries:
  attempts: 3
  perTryTimeout: 2s
  retryOn: 5xx,reset,connect-failure
```

---

### 8. Observability Triad

**Pattern**: Combine metrics, logs, and traces for full visibility.

**Implementation**:

- Metrics: Prometheus for quantitative data
- Logs: Envoy access logs with request IDs
- Traces: Jaeger for distributed tracing
- Dashboards: Grafana for visualization

**Benefits**:

- Complete system visibility
- Faster troubleshooting
- Data-driven decisions

---

## Anti-Patterns to Avoid

### 1. ❌ Over-Meshing Everything

**Problem**: Adding service mesh to all services immediately.

**Why It Fails**:

- Increased complexity overnight
- Resource overhead (100-200MB per pod)
- Learning curve for entire team
- Difficult rollback if issues occur

**Instead**:

- Start with critical services
- Gradual adoption (10-20% per month)
- Train team incrementally
- Measure ROI at each stage

---

### 2. ❌ Ignoring Sidecar Resource Limits

**Problem**: Not setting CPU/memory limits on Envoy proxies.

**Why It Fails**:

- Proxies can consume unlimited resources
- Node resource exhaustion
- OOMKilled pods
- Performance degradation

**Instead**:

```yaml
proxy:
  resources:
    requests:
      cpu: 10m
      memory: 40Mi
    limits:
      cpu: 2000m
      memory: 1024Mi
```

---

### 3. ❌ Too-Aggressive Circuit Breaking

**Problem**: Setting thresholds too low (e.g., 1 error = circuit open).

**Why It Fails**:

- False positives from transient errors
- Unnecessary service degradation
- Poor user experience
- Hiding real issues

**Instead**:

- Start conservative (5-10 consecutive errors)
- Monitor false positive rate
- Adjust based on service SLO
- Use outlier detection, not just error count

---

### 4. ❌ Permissive mTLS Mode in Production

**Problem**: Using PERMISSIVE mode indefinitely.

**Why It Fails**:

- Allows unencrypted traffic
- Defeats security purpose
- Compliance violations
- False sense of security

**Instead**:

- Use PERMISSIVE only during migration
- Set timeline for STRICT mode (2-4 weeks)
- Monitor mTLS adoption metrics
- Enforce STRICT mode in production

---

### 5. ❌ No Authorization Policies

**Problem**: Enabling mTLS without AuthorizationPolicy.

**Why It Fails**:

- mTLS only encrypts, doesn't authorize
- Any pod can call any service
- No defense against compromised pods
- Lateral movement possible

**Instead**:

- Start with deny-all policy
- Explicitly allow required traffic
- Use principle of least privilege
- Regular policy audits

---

### 6. ❌ 100% Trace Sampling in Production

**Problem**: Collecting traces for every request.

**Why It Fails**:

- Massive storage costs
- Performance overhead
- Trace backend overload
- Diminishing returns

**Instead**:

```yaml
traceSampling: 1.0  # 1% for production
```

- Use adaptive sampling for specific services
- Increase sampling for problem investigations
- Set retention policies (7-30 days)

---

### 7. ❌ Ignoring Sidecar Scoping

**Problem**: Every sidecar has full mesh configuration.

**Why It Fails**:

- Increased memory usage per pod
- Longer configuration push times
- Unnecessary network rules
- Scale limitations

**Instead**:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Sidecar
spec:
  egress:
  - hosts:
    - "./*"  # Only same namespace
    - "istio-system/*"
```

---

### 8. ❌ Timeouts Longer Than Client Timeouts

**Problem**: Setting mesh timeouts > application timeouts.

**Why It Fails**:

- Application gives up before mesh
- Mesh holds connections open
- Resource leaks
- Confusing timeout errors

**Instead**:

- Mesh timeout = 80% of client timeout
- Example: Client 10s → Mesh 8s
- Set per-try timeout < total timeout
- Document timeout chains

---

### 9. ❌ Not Planning for Mesh Upgrades

**Problem**: Treating mesh as "set and forget" infrastructure.

**Why It Fails**:

- Security vulnerabilities accumulate
- Miss new features and improvements
- Breaking changes become overwhelming
- No tested upgrade procedure

**Instead**:

- Quarterly upgrade schedule
- Test in dev/staging first
- Use canary upgrades with revisions
- Automate upgrade validation

---

### 10. ❌ No Disaster Recovery Plan

**Problem**: No procedure for mesh failure or removal.

**Why It Fails**:

- Control plane outage = application downtime
- Broken configuration = cascading failures
- No rollback plan for bad updates
- Panic during incidents

**Instead**:

- Document mesh removal procedure
- Test control plane failure scenarios
- Backup critical configurations
- Practice failover to direct service communication

---

## Pattern Selection Guide

| Use Case | Recommended Patterns |
|----------|---------------------|
| **New Service Deployment** | Progressive Traffic Shifting, Shadow Testing |
| **High-Reliability Service** | Circuit Breaker, Retry Budget, Locality LB |
| **Security Compliance** | Zero-Trust Model, Request Auth, Strict mTLS |
| **Performance Optimization** | Sidecar Scoping, Metric Reduction, Connection Pooling |
| **Multi-Cluster** | Locality LB, Mesh Federation, Cross-Cluster Discovery |
| **Debugging** | Observability Triad, Access Logs, Distributed Tracing |

---

## Migration Patterns

### Strangler Fig Pattern

Gradually migrate services to mesh without big-bang cutover:

1. **Phase 1**: Install mesh, no injection
2. **Phase 2**: Inject non-critical services
3. **Phase 3**: Inject critical services one-by-one
4. **Phase 4**: Enable strict mTLS after full adoption
5. **Phase 5**: Apply authorization policies

### Blue-Green Migration

Run old and new mesh versions side-by-side:

```bash
# Install new mesh revision
istioctl install --set revision=1-20 -y

# Label namespace for new revision
kubectl label namespace default istio.io/rev=1-20 --overwrite
kubectl label namespace default istio-injection-

# Restart pods to pick up new revision
kubectl rollout restart deployment -n default
```

---

## Summary

**Do**:

- Start small, scale gradually
- Set resource limits on proxies
- Use default-deny security model
- Plan for mesh lifecycle (upgrades, DR)
- Monitor golden signals (latency, errors, saturation)

**Don't**:

- Mesh everything at once
- Ignore resource constraints
- Rely on mTLS alone for security
- Set aggressive circuit breaker thresholds
- Forget about observability overhead
