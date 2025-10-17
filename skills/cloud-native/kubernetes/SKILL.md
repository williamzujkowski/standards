---
name: kubernetes
description: Kubernetes standards for container orchestration, deployments, services, ingress, ConfigMaps, Secrets, and security policies. Covers production-ready configurations, monitoring, and best practices for cloud-native applications.
---

# Kubernetes Cloud-Native Standards

> **Quick Navigation:**
> Level 1: [Quick Start](#level-1-quick-start-2000-tokens-5-minutes) (5 min) → Level 2: [Implementation](#level-2-implementation-5000-tokens-30-minutes) (30 min) → Level 3: [Mastery](#level-3-mastery-resources) (Extended)

---

## Level 1: Quick Start (<2,000 tokens, 5 minutes)

### Core Principles

1. **Declarative Configuration**: Define desired state, let Kubernetes manage it
2. **Resource Limits**: Always set requests and limits for CPU and memory
3. **Health Checks**: Implement liveness, readiness, and startup probes
4. **Security First**: RBAC, network policies, pod security standards
5. **Immutable Infrastructure**: Never modify running containers

### Essential Checklist

- [ ] **Deployments**: Use Deployments (not bare Pods) for applications
- [ ] **Resource Management**: Set CPU/memory requests and limits
- [ ] **Health Probes**: Configure liveness and readiness probes
- [ ] **Configuration**: Use ConfigMaps for config, Secrets for sensitive data
- [ ] **Networking**: Define Services for pod-to-pod communication
- [ ] **Security**: Enable RBAC, use NetworkPolicies, set PodSecurityContext
- [ ] **Monitoring**: Expose metrics endpoint for Prometheus
- [ ] **High Availability**: Run multiple replicas (min 3 for production)

### Quick Example

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
  labels:
    app: myapp
    version: v1.2.3
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1.2.3
    spec:
      serviceAccountName: myapp
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: myapp
        image: registry.example.com/myapp:v1.2.3
        ports:
        - containerPort: 8080
          name: http
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
  - protocol: TCP
    port: 80
    targetPort: 8080
```

### Quick Links to Level 2

- [Deployments](#deployments)
- [Services & Networking](#services--networking)
- [Configuration Management](#configuration-management)
- [Security](#security)
- [Resource Management](#resource-management)
- [Monitoring & Health Checks](#monitoring--health-checks)
- [Storage](#storage)

---

## Level 2: Implementation (<5,000 tokens, 30 minutes)

### Deployments

**Production-Ready Deployment**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
  labels:
    app: myapp
    environment: production
    managed-by: helm
  annotations:
    deployment.kubernetes.io/revision: "5"
spec:
  replicas: 5
  revisionHistoryLimit: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1.2.3
        environment: production
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: myapp
      automountServiceAccountToken: false

      # Security context
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault

      # Init containers
      initContainers:
      - name: migration
        image: registry.example.com/myapp-migrations:v1.2.3
        command: ['sh', '-c', 'migrate up']
        env:
        - name: DB_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database-url

      containers:
      - name: myapp
        image: registry.example.com/myapp:v1.2.3
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8080
          name: http
          protocol: TCP
        - containerPort: 9090
          name: metrics
          protocol: TCP

        # Resource limits
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
            ephemeral-storage: "1Gi"
          limits:
            memory: "512Mi"
            cpu: "500m"
            ephemeral-storage: "2Gi"

        # Health probes
        startupProbe:
          httpGet:
            path: /health
            port: 8080
          failureThreshold: 30
          periodSeconds: 10

        livenessProbe:
          httpGet:
            path: /health
            port: 8080
            httpHeaders:
            - name: X-Probe
              value: liveness
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 3

        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          successThreshold: 1
          failureThreshold: 3

        # Environment variables
        env:
        - name: NODE_ENV
          value: production
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace

        envFrom:
        - configMapRef:
            name: myapp-config
        - secretRef:
            name: myapp-secrets

        # Volume mounts
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
        - name: cache
          mountPath: /app/cache
        - name: tmp
          mountPath: /tmp

        # Security context
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
            - ALL

      # Volumes
      volumes:
      - name: config
        configMap:
          name: myapp-config
      - name: cache
        emptyDir: {}
      - name: tmp
        emptyDir: {}

      # Tolerations and affinity
      tolerations:
      - key: "dedicated"
        operator: "Equal"
        value: "app"
        effect: "NoSchedule"

      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - myapp
              topologyKey: kubernetes.io/hostname

        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: workload-type
                operator: In
                values:
                - application
```

### Services & Networking

**Service Types**

```yaml
# ClusterIP - Internal only (default)
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
  - protocol: TCP
    port: 80
    targetPort: 8080
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800

---
# LoadBalancer - External access
apiVersion: v1
kind: Service
metadata:
  name: myapp-external
  namespace: production
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 443
    targetPort: 8080
```

**Ingress Configuration** (see [templates/ingress.yaml](templates/ingress.yaml)):

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  namespace: production
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "30"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "30"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "30"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - myapp.example.com
    - www.myapp.example.com
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
  - host: www.myapp.example.com
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

**NetworkPolicy** (see [resources/security/network-policy.yaml](resources/security/network-policy.yaml)):

```yaml
# Default deny all ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress

---
# Allow specific ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: myapp-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: production
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443  # HTTPS
    - protocol: TCP
      port: 53   # DNS
    - protocol: UDP
      port: 53   # DNS
```

### Configuration Management

**ConfigMap** (see [templates/configmap.yaml](templates/configmap.yaml)):

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
  namespace: production
data:
  # Simple key-value
  database.host: "postgres.production.svc.cluster.local"
  database.port: "5432"
  log.level: "info"

  # File-like content
  app.properties: |
    server.port=8080
    server.shutdown=graceful
    spring.application.name=myapp

  # JSON configuration
  feature-flags.json: |
    {
      "enableNewUI": true,
      "maxUploadSize": 10485760,
      "enableDebugMode": false
    }
```

**Secrets** (see [templates/secret.yaml](templates/secret.yaml)):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
  namespace: production
type: Opaque
stringData:
  database-url: "postgresql://user:password@postgres:5432/myapp"
  api-key: "super-secret-key-12345"
  jwt-secret: "jwt-signing-secret"

---
# TLS Secret
apiVersion: v1
kind: Secret
metadata:
  name: myapp-tls
  namespace: production
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS...  # Base64 encoded certificate
  tls.key: LS0tLS...  # Base64 encoded private key
```

### Security

**RBAC** (see [resources/security/rbac.yaml](resources/security/rbac.yaml)):

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp
  namespace: production

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: myapp-role
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get"]
  resourceNames: ["myapp-secrets"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: myapp-rolebinding
  namespace: production
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: myapp-role
subjects:
- kind: ServiceAccount
  name: myapp
  namespace: production
```

**PodSecurityPolicy** (see [resources/security/pod-security-policy.yaml](resources/security/pod-security-policy.yaml)):

```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
  annotations:
    seccomp.security.alpha.kubernetes.io/allowedProfileNames: 'runtime/default'
    apparmor.security.beta.kubernetes.io/allowedProfileNames: 'runtime/default'
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
  - ALL
  volumes:
  - 'configMap'
  - 'emptyDir'
  - 'projected'
  - 'secret'
  - 'downwardAPI'
  - 'persistentVolumeClaim'
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
  readOnlyRootFilesystem: true
```

### Resource Management

**ResourceQuota**:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    requests.cpu: "100"
    requests.memory: "100Gi"
    requests.storage: "500Gi"
    limits.cpu: "200"
    limits.memory: "200Gi"
    persistentvolumeclaims: "20"
    services.loadbalancers: "5"
    services.nodeports: "0"
```

**LimitRange**:

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: production-limits
  namespace: production
spec:
  limits:
  - max:
      cpu: "2"
      memory: "4Gi"
    min:
      cpu: "100m"
      memory: "128Mi"
    default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "250m"
      memory: "256Mi"
    type: Container
```

**HorizontalPodAutoscaler**:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
  namespace: production
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
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 4
        periodSeconds: 30
      selectPolicy: Max
```

### Monitoring & Health Checks

**ServiceMonitor (Prometheus)**:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp
  namespace: production
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
    scheme: http
```

**Health Check Patterns**:

```yaml
# Startup probe for slow-starting containers
startupProbe:
  httpGet:
    path: /health
    port: 8080
  failureThreshold: 30
  periodSeconds: 10

# Liveness probe - restart if unhealthy
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

# Readiness probe - remove from load balancer if not ready
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

### Storage

**PersistentVolumeClaim**:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myapp-data
  namespace: production
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 10Gi
```

**StatefulSet** (for stateful apps):

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: myapp-db
  namespace: production
spec:
  serviceName: myapp-db
  replicas: 3
  selector:
    matchLabels:
      app: myapp-db
  template:
    metadata:
      labels:
        app: myapp-db
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
          name: postgres
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 50Gi
```

---

## Level 3: Mastery (Resources)

### Bundled Resources

1. **[templates/deployment.yaml](templates/deployment.yaml)** - Production-ready Deployment template
2. **[templates/service.yaml](templates/service.yaml)** - Service configuration (ClusterIP, LoadBalancer)
3. **[templates/ingress.yaml](templates/ingress.yaml)** - Ingress with TLS and rate limiting
4. **[templates/configmap.yaml](templates/configmap.yaml)** - ConfigMap examples
5. **[resources/security/network-policy.yaml](resources/security/network-policy.yaml)** - NetworkPolicy templates
6. **[resources/security/pod-security-policy.yaml](resources/security/pod-security-policy.yaml)** - PodSecurityPolicy for restricted access
7. **[templates/helm/Chart.yaml](templates/helm/Chart.yaml)** - Helm chart template

### Helm Charts

**Chart.yaml**:

```yaml
apiVersion: v2
name: myapp
description: A Helm chart for myapp
type: application
version: 1.2.3
appVersion: "1.2.3"
maintainers:
- name: DevOps Team
  email: devops@example.com
dependencies:
- name: postgresql
  version: "12.x.x"
  repository: https://charts.bitnami.com/bitnami
  condition: postgresql.enabled
```

**values.yaml**:

```yaml
replicaCount: 3

image:
  repository: registry.example.com/myapp
  pullPolicy: IfNotPresent
  tag: "1.2.3"

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
  - host: myapp.example.com
    paths:
    - path: /
      pathType: Prefix
  tls:
  - secretName: myapp-tls
    hosts:
    - myapp.example.com

resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70
```

### Advanced Topics

#### Custom Resource Definitions (CRDs)

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: applications.example.com
spec:
  group: example.com
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              replicas:
                type: integer
              image:
                type: string
  scope: Namespaced
  names:
    plural: applications
    singular: application
    kind: Application
    shortNames:
    - app
```

#### Operators

```go
// Example operator reconcile loop
func (r *ApplicationReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // Fetch the Application instance
    app := &examplev1.Application{}
    err := r.Get(ctx, req.NamespacedName, app)
    if err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // Create or update Deployment
    deployment := &appsv1.Deployment{}
    deployment.Name = app.Name
    deployment.Namespace = app.Namespace
    deployment.Spec.Replicas = &app.Spec.Replicas

    // ... configure deployment

    return ctrl.Result{}, nil
}
```

### Related Skills

- **[ci-cd](../../devops/ci-cd/SKILL.md)** - CI/CD pipelines for Kubernetes deployments
- **[docker-standards](../../containers/docker/SKILL.md)** - Container image best practices
- **[helm](../helm/SKILL.md)** - Kubernetes package manager
- **[monitoring](../../observability/monitoring/SKILL.md)** - Prometheus and Grafana setup

### Security Best Practices

1. **Pod Security Standards**: Use `restricted` profile for production
2. **Network Policies**: Implement default-deny, whitelist required connections
3. **RBAC**: Principle of least privilege for service accounts
4. **Secrets Management**: Use external secrets managers (Vault, AWS Secrets Manager)
5. **Image Scanning**: Scan container images for vulnerabilities
6. **Admission Controllers**: Use OPA/Gatekeeper for policy enforcement

### Performance Optimization

- **Resource Requests/Limits**: Right-size based on actual usage
- **Horizontal Pod Autoscaling**: Scale based on CPU, memory, or custom metrics
- **Vertical Pod Autoscaling**: Automatically adjust resource requests
- **Cluster Autoscaling**: Scale nodes based on pending pods
- **PodDisruptionBudgets**: Maintain availability during voluntary disruptions

### Disaster Recovery

**Backup Strategy**:
```bash
# Velero backup
velero backup create production-backup \
  --include-namespaces production \
  --snapshot-volumes

# Restore
velero restore create --from-backup production-backup
```

**Multi-Cluster Setup**: Use GitOps (ArgoCD/Flux) for disaster recovery

---

## When to Use This Skill

- ✅ Deploying containerized applications to Kubernetes
- ✅ Setting up production-ready configurations with health checks
- ✅ Implementing security policies (RBAC, NetworkPolicies)
- ✅ Managing configuration with ConfigMaps and Secrets
- ✅ Setting up autoscaling (HPA, VPA, Cluster Autoscaler)
- ✅ Configuring ingress and service mesh
- ✅ Implementing monitoring and observability
- ✅ Managing stateful workloads with StatefulSets

---

**Last Updated:** 2025-01-17
**Version:** 1.0.0
**Quality Score:** 95/100
