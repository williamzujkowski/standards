---
name: service-mesh
category: cloud-native
difficulty: advanced
tags: [istio, linkerd, envoy, mtls, traffic-management, observability]
prerequisites: [kubernetes, networking, security]
estimated_time: 8-12 hours
---

# Service Mesh

## Level 1: Quick Reference

### What is a Service Mesh?

A service mesh is an infrastructure layer that provides transparent service-to-service communication with built-in observability, traffic management, and security features without requiring application code changes.

**Core Components:**

- **Control Plane**: Configuration and policy management (Istiod)
- **Data Plane**: Sidecar proxies handling traffic (Envoy)
- **Service Identity**: Certificate-based authentication (mTLS)

### Key Benefits

**1. Observability**

- Automatic metrics collection (latency, throughput, errors)
- Distributed tracing (request flow visualization)
- Traffic topology and service dependencies
- Real-time dashboards (Kiali, Grafana)

**2. Traffic Management**

- Intelligent routing (canary, blue-green, A/B)
- Load balancing (round-robin, least-request, consistent hash)
- Traffic splitting and mirroring
- Request retries and timeouts

**3. Security**

- Automatic mutual TLS (mTLS) encryption
- Service-to-service authentication
- Fine-grained authorization policies
- Certificate rotation and management

**4. Resilience**

- Circuit breaking and outlier detection
- Rate limiting and quota management
- Fault injection for chaos testing
- Connection pooling

### Istio vs Linkerd Comparison

| Feature | Istio | Linkerd |
|---------|-------|---------|
| **Proxy** | Envoy (C++) | Linkerd2-proxy (Rust) |
| **Resource Usage** | Higher (100-200MB/pod) | Lower (10-20MB/pod) |
| **Features** | Comprehensive (100+ CRDs) | Focused (essential features) |
| **Complexity** | More complex setup | Simpler, faster setup |
| **Multi-cluster** | Full support | Basic support |
| **Traffic Management** | Advanced (mirroring, A/B) | Basic (canary, split) |
| **Observability** | Full stack (Kiali/Jaeger) | Built-in (Linkerd Viz) |
| **Maturity** | Production-ready (CNCF) | Production-ready (CNCF) |

**Choose Istio when:**

- Need advanced traffic management (mirroring, A/B testing)
- Multi-cluster or multi-cloud deployments
- Complex authorization requirements
- Established operations team

**Choose Linkerd when:**

- Resource efficiency is critical
- Prefer simplicity over features
- Kubernetes-only environment
- Faster onboarding required

### Essential Service Mesh Checklist

**Pre-Installation:**

```yaml
□ Kubernetes cluster v1.22+ running
□ CNI plugin supporting network policies
□ Prometheus and Grafana available
□ Resource capacity planned (2-4 CPU, 4-8GB RAM)
□ DNS resolution working correctly
```

**Post-Installation:**

```yaml
□ mTLS enabled cluster-wide (STRICT mode)
□ Sidecar injection configured (automatic/manual)
□ Monitoring dashboards accessible
□ Health checks and readiness probes adjusted
□ Certificate rotation configured
□ Resource limits set on proxies
```

**Traffic Management:**

```yaml
□ VirtualService defines routing rules
□ DestinationRule configures load balancing
□ Circuit breaking thresholds set
□ Retry policies configured
□ Timeouts appropriate for services
```

**Security:**

```yaml
□ Authorization policies applied (default-deny)
□ PeerAuthentication enforces mTLS
□ Service accounts properly scoped
□ Ingress/egress gateways secured
□ Certificate validity monitored
```

### Quick Start Commands

```bash
# Install Istio (demo profile)
istioctl install --set profile=demo -y

# Enable sidecar injection
kubectl label namespace default istio-injection=enabled

# Deploy sample app
kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml

# Create ingress gateway
kubectl apply -f samples/bookinfo/networking/bookinfo-gateway.yaml

# Check mesh status
istioctl proxy-status

# View metrics
kubectl -n istio-system port-forward svc/kiali 20001:20001
```

### Common Patterns

**Canary Deployment:**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews-canary
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        end-user:
          exact: jason
    route:
    - destination:
        host: reviews
        subset: v2
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 90
    - destination:
        host: reviews
        subset: v2
      weight: 10
```

**Circuit Breaking:**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: reviews-circuit-breaker
spec:
  host: reviews
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 10
        maxRequestsPerConnection: 2
    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

**Zero Trust Security:**

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: default
spec:
  {} # Empty spec denies all traffic
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/frontend"]
    to:
    - operation:
        methods: ["GET", "POST"]
```

---

## Level 2: Implementation Guide

### Service Mesh Architecture

#### Control Plane (Istiod)

The control plane manages and configures the data plane proxies:

**Core Functions:**

1. **Service Discovery**: Abstracts platform-specific discovery mechanisms
2. **Configuration Distribution**: Pushes routing rules to proxies
3. **Certificate Authority**: Issues and rotates mTLS certificates
4. **Policy Enforcement**: Applies security and traffic policies

**Istiod Components:**

```
┌─────────────────────────────────────────┐
│             Istiod (Control Plane)      │
├─────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐      │
│  │   Pilot     │  │   Citadel   │      │
│  │ (Discovery) │  │    (CA)     │      │
│  └─────────────┘  └─────────────┘      │
│  ┌─────────────┐  ┌─────────────┐      │
│  │   Galley    │  │   Telemetry │      │
│  │  (Config)   │  │  (Metrics)  │      │
│  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────┘
```

#### Data Plane (Envoy Proxies)

**Sidecar Pattern:**

```
┌────────────────────────────────────┐
│             Pod                    │
│  ┌──────────────┐  ┌────────────┐ │
│  │ Application  │  │   Envoy    │ │
│  │ Container    │◄─┤   Proxy    │ │
│  │              │  │  (Sidecar) │ │
│  └──────────────┘  └────────────┘ │
│         ▲                ▲         │
└─────────┼────────────────┼─────────┘
          │                │
    Business Logic    Traffic Management
                      Security, Observability
```

**Envoy Capabilities:**

- Layer 7 (HTTP/gRPC) and Layer 4 (TCP) proxying
- Dynamic configuration via xDS APIs
- Advanced load balancing algorithms
- Health checking and circuit breaking
- Rich metrics and distributed tracing

#### Traffic Flow

```
Client Request
      │
      ▼
┌─────────────┐
│   Ingress   │ ← External entry point
│   Gateway   │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐
│  Service A  │────►│  Service B  │
│   (Envoy)   │     │   (Envoy)   │
└──────┬──────┘     └──────┬──────┘
       │                   │
       ▼                   ▼
  Application         Application
   Container           Container
```

### Istio Installation and Configuration

#### Installation Options

**1. IstioOperator (Recommended):**

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-installation
spec:
  profile: default
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
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
  meshConfig:
    accessLogFile: /dev/stdout
    enableTracing: true
    defaultConfig:
      tracing:
        sampling: 100.0
  values:
    global:
      proxy:
        resources:
          requests:
            cpu: 10m
            memory: 40Mi
          limits:
            cpu: 2000m
            memory: 1024Mi
```

**2. Helm Installation:**

```bash
# Add Istio repository
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update

# Create istio-system namespace
kubectl create namespace istio-system

# Install base components
helm install istio-base istio/base -n istio-system

# Install Istiod
helm install istiod istio/istiod -n istio-system --wait

# Install ingress gateway
helm install istio-ingress istio/gateway -n istio-system
```

**3. Production Profile:**

```bash
# Minimal production setup
istioctl install --set profile=minimal \
  --set values.pilot.autoscaleEnabled=true \
  --set values.pilot.autoscaleMin=2 \
  --set values.pilot.autoscaleMax=5 \
  --set values.global.proxy.resources.requests.cpu=100m \
  --set values.global.proxy.resources.requests.memory=128Mi \
  --set values.global.proxy.resources.limits.cpu=2000m \
  --set values.global.proxy.resources.limits.memory=1024Mi
```

#### Sidecar Injection Strategies

**Automatic Injection (Namespace-level):**

```bash
# Label namespace for injection
kubectl label namespace production istio-injection=enabled

# Verify
kubectl get namespace -L istio-injection
```

**Manual Injection (Pod-level):**

```bash
# Inject sidecar into existing deployment
kubectl get deployment myapp -o yaml | \
  istioctl kube-inject -f - | \
  kubectl apply -f -
```

**Selective Injection (Pod annotation):**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
  annotations:
    sidecar.istio.io/inject: "true"  # Explicit injection
spec:
  containers:
  - name: app
    image: myapp:v1
```

#### Configuration Validation

```bash
# Validate installation
istioctl verify-install

# Check proxy status
istioctl proxy-status

# Analyze configuration
istioctl analyze --all-namespaces

# View proxy configuration
istioctl proxy-config cluster <pod-name> -n <namespace>
```

### Advanced Traffic Management

#### 1. Canary Deployments

**Gradual Rollout Strategy:**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews-canary
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        user-agent:
          regex: ".*Mobile.*"
    route:
    - destination:
        host: reviews
        subset: v2
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 80
    - destination:
        host: reviews
        subset: v2
      weight: 20
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: reviews-destination
spec:
  host: reviews
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

**Progressive Rollout Script:**

```bash
#!/bin/bash
# Gradual canary rollout: 10% → 25% → 50% → 100%

WEIGHTS=(10 25 50 100)
for weight in "${WEIGHTS[@]}"; do
  echo "Shifting $weight% traffic to v2..."

  kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews-canary
spec:
  hosts:
  - reviews
  http:
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: $((100 - weight))
    - destination:
        host: reviews
        subset: v2
      weight: $weight
EOF

  # Monitor metrics for 5 minutes
  sleep 300

  # Check error rate
  ERROR_RATE=$(kubectl exec -it deploy/prometheus -n istio-system -- \
    promtool query instant 'rate(istio_requests_total{destination_version="v2",response_code=~"5.."}[5m])')

  if (( $(echo "$ERROR_RATE > 0.05" | bc -l) )); then
    echo "Error rate too high, rolling back!"
    kubectl apply -f virtualservice-v1-only.yaml
    exit 1
  fi
done
```

#### 2. Blue-Green Deployments

**Zero-Downtime Cutover:**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp-bluegreen
spec:
  hosts:
  - myapp.example.com
  gateways:
  - myapp-gateway
  http:
  - match:
    - headers:
        x-version:
          exact: green
    route:
    - destination:
        host: myapp
        subset: green
  - route:  # Default to blue
    - destination:
        host: myapp
        subset: blue
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp-destination
spec:
  host: myapp
  subsets:
  - name: blue
    labels:
      version: blue
  - name: green
    labels:
      version: green
```

**Cutover Process:**

```bash
# 1. Deploy green version
kubectl apply -f deployment-green.yaml

# 2. Test green version
curl -H "x-version: green" https://myapp.example.com/health

# 3. Switch all traffic to green
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp-bluegreen
spec:
  hosts:
  - myapp.example.com
  http:
  - route:
    - destination:
        host: myapp
        subset: green
EOF

# 4. Verify metrics, then remove blue
kubectl delete deployment myapp-blue
```

#### 3. A/B Testing

**User Cohort Routing:**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: frontend-ab-test
spec:
  hosts:
  - frontend.example.com
  gateways:
  - frontend-gateway
  http:
  - match:
    - headers:
        cookie:
          regex: ".*session=premium.*"
    route:
    - destination:
        host: frontend
        subset: premium-ui
  - match:
    - headers:
        x-user-id:
          regex: "^[0-4].*"  # 50% of users (IDs starting with 0-4)
    route:
    - destination:
        host: frontend
        subset: variant-a
  - route:  # Default variant B
    - destination:
        host: frontend
        subset: variant-b
```

#### 4. Traffic Mirroring

**Shadow Testing:**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-mirror
spec:
  hosts:
  - api.example.com
  http:
  - route:
    - destination:
        host: api
        subset: v1
      weight: 100
    mirror:
      host: api
      subset: v2
    mirrorPercentage:
      value: 100.0  # Mirror 100% of traffic
```

**Use Cases:**

- Test new version without impacting users
- Load testing with real traffic patterns
- Validate refactored services
- Debug production issues safely

### Observability Stack

#### Kiali (Service Mesh Dashboard)

**Installation:**

```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/kiali.yaml

# Access dashboard
istioctl dashboard kiali
```

**Key Features:**

- Service topology graph
- Traffic flow visualization
- Configuration validation
- Distributed tracing integration

**Kiali Configuration:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kiali
  namespace: istio-system
data:
  config.yaml: |
    auth:
      strategy: anonymous
    deployment:
      accessible_namespaces:
      - '**'
    external_services:
      prometheus:
        url: "http://prometheus:9090"
      tracing:
        url: "http://jaeger-query:16686"
      grafana:
        url: "http://grafana:3000"
```

#### Jaeger (Distributed Tracing)

**Installation:**

```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/jaeger.yaml

# Access UI
istioctl dashboard jaeger
```

**Enable Tracing in Mesh:**

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  meshConfig:
    enableTracing: true
    defaultConfig:
      tracing:
        sampling: 100.0  # 100% sampling for testing
        zipkin:
          address: jaeger-collector.istio-system:9411
```

**Application Instrumentation:**

```python
# Python (Flask) example
from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configure Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)

@app.route('/api/data')
def get_data():
    with tracer.start_as_current_span("get_data"):
        # Business logic
        return {"data": "value"}
```

#### Prometheus & Grafana

**Prometheus Installation:**

```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/prometheus.yaml
```

**Key Metrics:**

```promql
# Request rate (QPS)
rate(istio_requests_total{reporter="source"}[1m])

# Error rate
rate(istio_requests_total{reporter="source",response_code=~"5.."}[1m])
 / rate(istio_requests_total{reporter="source"}[1m])

# P95 latency
histogram_quantile(0.95,
  rate(istio_request_duration_milliseconds_bucket{reporter="source"}[1m])
)

# Circuit breaker triggers
rate(envoy_cluster_upstream_rq_pending_overflow[1m])
```

**Grafana Dashboards:**

```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/grafana.yaml

istioctl dashboard grafana
```

**Custom Dashboard (JSON):**

```json
{
  "dashboard": {
    "title": "Service Mesh Overview",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "sum(rate(istio_requests_total[1m])) by (destination_service)"
          }
        ]
      },
      {
        "title": "Error Rate (%)",
        "targets": [
          {
            "expr": "sum(rate(istio_requests_total{response_code=~\"5..\"}[1m])) / sum(rate(istio_requests_total[1m])) * 100"
          }
        ]
      }
    ]
  }
}
```

### Security Configuration

#### Mutual TLS (mTLS)

**Enable Strict mTLS (Cluster-wide):**

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT  # Enforce mTLS on all services
```

**Per-Namespace mTLS:**

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: namespace-policy
  namespace: production
spec:
  mtls:
    mode: STRICT
---
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: legacy-policy
  namespace: legacy
spec:
  mtls:
    mode: PERMISSIVE  # Allow plaintext for migration
```

**Per-Port mTLS:**

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: service-policy
  namespace: default
spec:
  selector:
    matchLabels:
      app: myapp
  mtls:
    mode: STRICT
  portLevelMtls:
    8080:
      mode: DISABLE  # Health check endpoint
```

#### Authorization Policies

**Default Deny:**

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: default
spec:
  {}  # Empty spec = deny all
```

**Allow Specific Services:**

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: frontend-to-backend
  namespace: default
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/frontend"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
```

**JWT Authentication:**

```yaml
apiVersion: security.istio.io/v1beta1
kind: RequestAuthentication
metadata:
  name: jwt-auth
  namespace: default
spec:
  selector:
    matchLabels:
      app: api
  jwtRules:
  - issuer: "https://auth.example.com"
    jwksUri: "https://auth.example.com/.well-known/jwks.json"
    audiences:
    - "api.example.com"
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: require-jwt
spec:
  selector:
    matchLabels:
      app: api
  action: ALLOW
  rules:
  - from:
    - source:
        requestPrincipals: ["*"]  # Any valid JWT
```

**RBAC with Custom Claims:**

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: admin-only
spec:
  selector:
    matchLabels:
      app: admin-api
  action: ALLOW
  rules:
  - when:
    - key: request.auth.claims[role]
      values: ["admin"]
    to:
    - operation:
        methods: ["DELETE", "PUT"]
```

### Resilience Patterns

#### Circuit Breaking

**Configuration:**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: backend-circuit-breaker
spec:
  host: backend
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100  # Max TCP connections
      http:
        http1MaxPendingRequests: 10  # Max queued requests
        http2MaxRequests: 100
        maxRequestsPerConnection: 2
        maxRetries: 3
    outlierDetection:
      consecutiveErrors: 5  # Eject after 5 errors
      interval: 30s  # Analysis interval
      baseEjectionTime: 30s  # Minimum ejection duration
      maxEjectionPercent: 50  # Max 50% of instances ejected
      minHealthPercent: 40  # Panic threshold
```

**Testing Circuit Breaker:**

```bash
# Generate load to trigger circuit breaker
kubectl run -it --rm load-generator --image=busybox --restart=Never -- /bin/sh -c \
  "while true; do wget -q -O- http://backend:8080/api/slow; done"

# Monitor circuit breaker stats
istioctl pc cluster <pod> --fqdn backend.default.svc.cluster.local -o json | \
  jq '.outlierDetection'
```

#### Retries and Timeouts

**Retry Configuration:**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: backend-retry
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend
    retries:
      attempts: 3  # Retry up to 3 times
      perTryTimeout: 2s  # Each attempt timeout
      retryOn: 5xx,reset,connect-failure,refused-stream
```

**Timeout Configuration:**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-timeout
spec:
  hosts:
  - api
  http:
  - route:
    - destination:
        host: api
    timeout: 10s  # Total request timeout
    retries:
      attempts: 2
      perTryTimeout: 3s
```

**Fault Injection (Chaos Testing):**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: chaos-testing
spec:
  hosts:
  - backend
  http:
  - fault:
      delay:
        percentage:
          value: 10  # 10% of requests
        fixedDelay: 5s  # Add 5s latency
      abort:
        percentage:
          value: 5  # 5% of requests
        httpStatus: 503  # Return 503 error
    route:
    - destination:
        host: backend
```

#### Rate Limiting

**Local Rate Limiting (Envoy):**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: EnvoyFilter
metadata:
  name: local-rate-limit
  namespace: istio-system
spec:
  workloadSelector:
    labels:
      app: api
  configPatches:
  - applyTo: HTTP_FILTER
    match:
      context: SIDECAR_INBOUND
    patch:
      operation: INSERT_BEFORE
      value:
        name: envoy.filters.http.local_ratelimit
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
          stat_prefix: http_local_rate_limiter
          token_bucket:
            max_tokens: 100
            tokens_per_fill: 100
            fill_interval: 1s
          filter_enabled:
            runtime_key: local_rate_limit_enabled
            default_value:
              numerator: 100
              denominator: HUNDRED
          filter_enforced:
            runtime_key: local_rate_limit_enforced
            default_value:
              numerator: 100
              denominator: HUNDRED
```

### Multi-Cluster Service Mesh

#### Cluster Federation

**Primary-Remote Model:**

```yaml
# On primary cluster
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster1
      network: network1
```

```yaml
# On remote cluster
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster2
      network: network2
      remotePilotAddress: istiod.istio-system.svc.cluster.local
```

**Cross-Cluster Service Discovery:**

```bash
# Create remote secret on primary cluster
istioctl x create-remote-secret \
  --context=cluster2 \
  --name=cluster2 | \
  kubectl apply -f - --context=cluster1

# Enable ServiceEntry for remote services
kubectl apply --context=cluster1 -f - <<EOF
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: backend-cluster2
spec:
  hosts:
  - backend.default.svc.cluster.local
  location: MESH_INTERNAL
  ports:
  - number: 8080
    name: http
    protocol: HTTP
  resolution: DNS
  endpoints:
  - address: backend.default.svc.cluster2.global
    locality: us-west/zone1
EOF
```

### Performance Tuning

#### Resource Optimization

**Sidecar Resource Limits:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: istio-sidecar-injector
  namespace: istio-system
data:
  values: |
    global:
      proxy:
        resources:
          requests:
            cpu: 10m  # Minimum for idle
            memory: 40Mi
          limits:
            cpu: 2000m  # Burst capacity
            memory: 1024Mi
        concurrency: 2  # Worker threads
```

**Sidecar Scoping:**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Sidecar
metadata:
  name: default
  namespace: production
spec:
  egress:
  - hosts:
    - "./*"  # Only services in same namespace
    - "istio-system/*"  # And istio-system
```

#### Telemetry Optimization

**Reduce Metrics Cardinality:**

```yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: mesh-default
  namespace: istio-system
spec:
  metrics:
  - providers:
    - name: prometheus
    overrides:
    - match:
        metric: ALL_METRICS
      tagOverrides:
        source_cluster:
          operation: REMOVE
        destination_cluster:
          operation: REMOVE
```

**Sampling Configuration:**

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  meshConfig:
    enableTracing: true
    defaultConfig:
      tracing:
        sampling: 1.0  # 1% sampling for production
```

---

## Level 3: Deep Dive Resources

### Official Documentation

- [Istio Documentation](https://istio.io/latest/docs/)
- [Linkerd Documentation](https://linkerd.io/2/overview/)
- [Envoy Proxy Documentation](https://www.envoyproxy.io/docs)
- [CNCF Service Mesh Landscape](https://landscape.cncf.io/guide#orchestration-management--service-mesh)

### Books

- **"Istio in Action" by Christian Posta and Rinor Maloku** - Comprehensive guide
- **"Service Mesh Patterns" by Alex Soto Bueno** - Design patterns
- **"Mastering Service Mesh" by Anjul Sahu** - Advanced concepts

### Online Courses

- [Istio Fundamentals (Tetrate Academy)](https://academy.tetrate.io/)
- [Service Mesh with Istio (Pluralsight)](https://www.pluralsight.com/)
- [Linkerd Fundamentals (Linux Foundation)](https://training.linuxfoundation.org/)

### Hands-On Labs

- [Istio Workshop](https://github.com/solo-io/istio-workshops)
- [Service Mesh Patterns](https://servicemeshpatterns.github.io/servicemeshbook/)
- [Envoy Proxy Sandbox](https://www.envoyproxy.io/docs/envoy/latest/start/sandboxes/)

### Community Resources

- [IstioCon Talks](https://events.istio.io/)
- [CNCF Webinars](https://www.cncf.io/webinars/)
- [Service Mesh Summit](https://servicemeshsummit.io/)

### Tools & Extensions

- **Kiali** - Service mesh observability
- **Flagger** - Progressive delivery operator
- **Meshery** - Multi-mesh management
- **SMI (Service Mesh Interface)** - Standard specification

### Best Practices

- [Istio Production Best Practices](https://istio.io/latest/docs/ops/best-practices/)
- [Service Mesh Security Patterns](https://www.nist.gov/publications/zero-trust-architecture)
- [Performance Tuning Guide](https://istio.io/latest/docs/ops/deployment/performance-and-scalability/)
