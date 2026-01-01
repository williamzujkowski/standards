---
name: kubernetes
description: Kubernetes standards for container orchestration, deployments, services, ingress, ConfigMaps, Secrets, and security policies. Covers production-ready configurations, monitoring, and best practices for cloud-native applications.
---

# Kubernetes Cloud-Native Standards

> **Quick Navigation:**
> Level 1: [Quick Start](#level-1-quick-start) (5 min) | Level 2: [Implementation](#level-2-implementation) (30 min) | Level 3: [REFERENCE.md](REFERENCE.md) (Extended)

---

## Level 1: Quick Start

### Core Principles

1. **Declarative Configuration**: Define desired state, let Kubernetes manage it
2. **Resource Limits**: Always set requests and limits for CPU and memory
3. **Health Checks**: Implement liveness, readiness, and startup probes
4. **Security First**: RBAC, network policies, pod security standards
5. **Immutable Infrastructure**: Never modify running containers

### Essential Checklist

- [ ] Use Deployments (not bare Pods) for applications
- [ ] Set CPU/memory requests and limits
- [ ] Configure liveness and readiness probes
- [ ] Use ConfigMaps for config, Secrets for sensitive data
- [ ] Define Services for pod-to-pod communication
- [ ] Enable RBAC, use NetworkPolicies, set PodSecurityContext
- [ ] Expose metrics endpoint for Prometheus
- [ ] Run multiple replicas (min 3 for production)

### Minimal Deployment Example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
      - name: myapp
        image: registry.example.com/myapp:v1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: myapp
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
```

---

## Level 2: Implementation

### Essential kubectl Commands

```bash
# Cluster info
kubectl cluster-info
kubectl get nodes -o wide

# Namespace operations
kubectl create namespace production
kubectl config set-context --current --namespace=production

# Deployment management
kubectl apply -f deployment.yaml
kubectl rollout status deployment/myapp
kubectl rollout history deployment/myapp
kubectl rollout undo deployment/myapp

# Debugging
kubectl get pods -o wide
kubectl describe pod <pod-name>
kubectl logs <pod-name> -f --tail=100
kubectl exec -it <pod-name> -- /bin/sh

# Resource inspection
kubectl get all -n production
kubectl top pods
kubectl get events --sort-by='.lastTimestamp'
```

### Deployment Patterns

**Rolling Update Strategy**:

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
  revisionHistoryLimit: 10
```

**Pod Security Context** (required for production):

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: myapp
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
```

**Resource Management**:

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
    ephemeral-storage: "1Gi"
  limits:
    memory: "512Mi"
    cpu: "500m"
    ephemeral-storage: "2Gi"
```

### Services & Networking

**Service Types**:

| Type | Use Case |
|------|----------|
| ClusterIP | Internal communication (default) |
| NodePort | Development/testing external access |
| LoadBalancer | Production external access |
| ExternalName | DNS alias to external service |

**Basic Ingress**:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp
            port:
              number: 80
```

**Network Policy (Default Deny + Allow)**:

```yaml
# Default deny all ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}
  policyTypes:
  - Ingress
---
# Allow specific traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-myapp
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
```

### Configuration Management

**ConfigMap**:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  database.host: "postgres.production.svc.cluster.local"
  log.level: "info"
  app.properties: |
    server.port=8080
    server.shutdown=graceful
```

**Secret** (use stringData for plain text):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
stringData:
  database-url: "postgresql://user:password@postgres:5432/myapp"
  api-key: "your-api-key"
```

**Using in Pods**:

```yaml
env:
- name: DB_HOST
  valueFrom:
    configMapKeyRef:
      name: myapp-config
      key: database.host
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: myapp-secrets
      key: db-password
envFrom:
- configMapRef:
    name: myapp-config
- secretRef:
    name: myapp-secrets
```

### Health Probes

```yaml
# Startup - for slow-starting apps
startupProbe:
  httpGet:
    path: /health
    port: 8080
  failureThreshold: 30
  periodSeconds: 10

# Liveness - restart if unhealthy
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3

# Readiness - remove from LB if not ready
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 3
```

### RBAC Essentials

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: myapp-role
rules:
- apiGroups: [""]
  resources: ["pods", "configmaps"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: myapp-rolebinding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: myapp-role
subjects:
- kind: ServiceAccount
  name: myapp
```

### Autoscaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## Troubleshooting Quick Reference

### Pod Issues

| Status | Common Cause | Debug Command |
|--------|--------------|---------------|
| Pending | Resource constraints, scheduling | `kubectl describe pod <name>` |
| CrashLoopBackOff | App crash, bad config | `kubectl logs <name> --previous` |
| ImagePullBackOff | Wrong image, no auth | `kubectl describe pod <name>` |
| OOMKilled | Memory limit exceeded | Increase memory limit |

### Common Debug Commands

```bash
# Check events
kubectl get events --sort-by='.lastTimestamp' -n production

# Check resource usage
kubectl top pods -n production

# Enter pod for debugging
kubectl exec -it <pod> -- /bin/sh

# Port forward for local testing
kubectl port-forward svc/myapp 8080:80

# Check service endpoints
kubectl get endpoints myapp
```

---

## Security Best Practices

1. **Pod Security Standards**: Use `restricted` profile for production
2. **Network Policies**: Default-deny, whitelist required connections
3. **RBAC**: Principle of least privilege for service accounts
4. **Secrets Management**: Use Vault, AWS Secrets Manager, or external-secrets
5. **Image Scanning**: Scan images with Trivy, Snyk, or similar
6. **Admission Controllers**: Use OPA/Gatekeeper for policy enforcement

---

## When to Use This Skill

- Deploying containerized applications to Kubernetes
- Setting up production-ready configurations with health checks
- Implementing security policies (RBAC, NetworkPolicies)
- Managing configuration with ConfigMaps and Secrets
- Setting up autoscaling (HPA, VPA, Cluster Autoscaler)
- Configuring ingress and load balancing

---

## Level 3: Extended Resources

See **[REFERENCE.md](REFERENCE.md)** for:

- Complete production deployment manifests
- Advanced Helm chart examples
- StatefulSet configurations
- Custom Resource Definitions (CRDs)
- Operator patterns
- Multi-cluster and disaster recovery
- Complete security policy examples
- ServiceMonitor configurations
- ResourceQuota and LimitRange templates

### Related Skills

- [CI/CD](../../devops/ci-cd/SKILL.md) - Deployment pipelines
- [Docker](../../containers/docker/SKILL.md) - Container image best practices
- [Helm](../helm/SKILL.md) - Kubernetes package manager
- [Monitoring](../../observability/monitoring/SKILL.md) - Prometheus and Grafana

---

**Last Updated:** 2025-01-01
**Version:** 2.0.0
