# Service Mesh - Reference Implementation

This document contains detailed configuration examples and full code samples extracted from the main skill guide to keep the implementation guide concise.

## Table of Contents

- [Service Mesh Architecture](#service-mesh-architecture)
- [Control Plane (Istiod)](#control-plane-(istiod))
- [Data Plane (Envoy Proxies)](#data-plane-(envoy-proxies))
- [Traffic Flow](#traffic-flow)
- [Istio Installation and Configuration](#istio-installation-and-configuration)
- [Installation Options](#installation-options)
- [Sidecar Injection Strategies](#sidecar-injection-strategies)
- [Configuration Validation](#configuration-validation)
- [Advanced Traffic Management](#advanced-traffic-management)
- [1. Canary Deployments](#1.-canary-deployments)

---

## Code Examples

### Example 0

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

### Example 1

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

### Example 2

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

### Example 3

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

### Example 4

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

### Example 5

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

### Example 9

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

### Example 10

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

### Example 11

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

### Example 12

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

### Example 13

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

### Example 14

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

### Example 15

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

### Example 17

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

### Example 19

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

### Example 20

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

### Example 22

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

### Example 24

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

### Example 25

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

### Example 26

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

### Example 27

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

### Example 28

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: default
spec:
  {}  # Empty spec = deny all
```

### Example 29

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

### Example 30

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

### Example 31

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

### Example 32

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

### Example 33

```bash
# Generate load to trigger circuit breaker
kubectl run -it --rm load-generator --image=busybox --restart=Never -- /bin/sh -c \
  "while true; do wget -q -O- http://backend:8080/api/slow; done"

# Monitor circuit breaker stats
istioctl pc cluster <pod> --fqdn backend.default.svc.cluster.local -o json | \
  jq '.outlierDetection'
```

### Example 34

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

### Example 35

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

### Example 36

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

### Example 37

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

### Example 38

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

### Example 39

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

### Example 40

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

### Example 41

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

### Example 42

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

### Example 43

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

### Example 44

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

### Example 45

```python
// TODO: Add basic example for service-mesh
// This example demonstrates core functionality
```

---

## Additional Resources

See the main SKILL.md file for essential patterns and the official documentation for complete API references.
