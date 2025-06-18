# Cloud-Native and Container Standards

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active
**Standard Code:** CN

---

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active

## Table of Contents

1. [Container Standards](#1-container-standards)
2. [Kubernetes Standards](#2-kubernetes-standards)
3. [Infrastructure as Code](#3-infrastructure-as-code)
4. [Serverless Architecture](#4-serverless-architecture)
5. [Service Mesh](#5-service-mesh)
6. [Cloud Provider Standards](#6-cloud-provider-standards)
7. [Cloud-Native Security](#7-cloud-native-security)
8. [Monitoring and Observability](#8-monitoring-and-observability)

---

## Overview

This standard provides comprehensive guidelines and best practices for the subject area.
It aims to ensure consistency, quality, and maintainability across all related implementations.

## 1. Container Standards

### 1.1 Docker Best Practices

#### Image Building **[REQUIRED]**

##### Multi-Stage Builds
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Runtime stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
EXPOSE 3000
CMD ["node", "server.js"]
```

##### Image Optimization Rules
1. **Base Image Selection**
   - Use official images
   - Prefer Alpine or distroless
   - Specify exact versions
   - Scan for vulnerabilities

2. **Layer Optimization**
   - Combine RUN commands
   - Order from least to most changing
   - Clean up in same layer
   - Use .dockerignore

3. **Security Hardening**
   - Run as non-root user
   - Remove unnecessary packages
   - No secrets in images
   - Sign images

#### Container Configuration **[REQUIRED]**

##### Resource Limits
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

##### Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

### 1.2 Container Registry Standards

#### Registry Management **[REQUIRED]**
1. **Image Naming**
   ```
   registry.example.com/namespace/app-name:version
   ```

2. **Tagging Strategy**
   - Semantic versioning for releases
   - Git SHA for builds
   - Environment tags (dev, staging, prod)
   - Never use 'latest' in production

3. **Retention Policy**
   - Keep last 10 versions
   - Archive after 90 days
   - Delete untagged after 7 days

#### Security Scanning **[REQUIRED]**
- Scan on push
- Block critical vulnerabilities
- Daily scans of production images
- SBOM generation

---

## 2. Kubernetes Standards

### 2.1 Resource Management

#### Namespace Strategy **[REQUIRED]**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: app-production
  labels:
    environment: production
    team: platform
  annotations:
    contact: platform@example.com
```

##### Namespace Patterns
- Environment-based: `app-dev`, `app-staging`, `app-prod`
- Team-based: `team-frontend`, `team-backend`
- Feature-based: `feature-x-preview`

#### Resource Quotas **[REQUIRED]**
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
spec:
  hard:
    requests.cpu: "100"
    requests.memory: "100Gi"
    limits.cpu: "200"
    limits.memory: "200Gi"
    persistentvolumeclaims: "10"
```

### 2.2 Workload Standards

#### Deployment Configuration **[REQUIRED]**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: myapp
    version: v1.0.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1.0.0
    spec:
      containers:
      - name: app
        image: registry/myapp:v1.0.0
        ports:
        - containerPort: 8080
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
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        securityContext:
          runAsNonRoot: true
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
```

#### Pod Standards **[REQUIRED]**
1. **Labels**
   - `app`: Application name
   - `version`: Application version
   - `component`: Component type
   - `managed-by`: Deployment tool

2. **Probes**
   - Always define liveness probe
   - Always define readiness probe
   - Startup probe for slow-starting apps
   - Appropriate timeouts and thresholds

3. **Security Context**
   - Run as non-root
   - Read-only root filesystem
   - Drop all capabilities
   - Use Pod Security Standards

### 2.3 Service Standards

#### Service Types **[REQUIRED]**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  type: ClusterIP  # Default for internal
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```

#### Ingress Configuration **[REQUIRED]**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - app.example.com
    secretName: app-tls
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

### 2.4 Configuration Management

#### ConfigMaps and Secrets **[REQUIRED]**
```yaml
# ConfigMap for non-sensitive data
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  app.properties: |
    server.port=8080
    log.level=info

---
# Secret for sensitive data
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  database-url: postgresql://user:pass@db:5432/myapp
```

##### Best Practices
1. **Separation of Concerns**
   - ConfigMaps for configuration
   - Secrets for sensitive data
   - Never commit secrets to Git

2. **Secret Management**
   - Use external secret managers
   - Rotate secrets regularly
   - Encrypt secrets at rest
   - Audit secret access

### 2.5 RBAC Standards

#### Service Account Configuration **[REQUIRED]**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: app-production
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-rolebinding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: app-role
subjects:
- kind: ServiceAccount
  name: app-sa
```

---

## 3. Infrastructure as Code

### 3.1 Terraform Standards

#### Project Structure **[REQUIRED]**
```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── production/
├── modules/
│   ├── networking/
│   ├── compute/
│   └── database/
└── global/
    ├── providers.tf
    └── versions.tf
```

#### Coding Standards **[REQUIRED]**
```hcl
# Resource naming convention
resource "aws_instance" "web_server" {
  # Use data sources for AMIs
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  # Always tag resources
  tags = merge(
    var.common_tags,
    {
      Name        = "${var.environment}-web-server"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  )

  # Lifecycle rules
  lifecycle {
    create_before_destroy = true
    prevent_destroy       = var.environment == "production"
  }
}

# Variable validation
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"

  validation {
    condition     = contains(["t3.micro", "t3.small", "t3.medium"], var.instance_type)
    error_message = "Instance type must be t3.micro, t3.small, or t3.medium."
  }
}
```

#### State Management **[REQUIRED]**
```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "env/production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### 3.2 GitOps Standards

#### Repository Structure **[REQUIRED]**
```
gitops-repo/
├── apps/
│   ├── base/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── kustomization.yaml
│   └── overlays/
│       ├── dev/
│       ├── staging/
│       └── production/
├── infrastructure/
│   ├── cert-manager/
│   ├── ingress-nginx/
│   └── monitoring/
└── clusters/
    ├── dev/
    ├── staging/
    └── production/
```

#### ArgoCD Application **[REQUIRED]**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/company/gitops
    targetRevision: HEAD
    path: apps/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp-production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

### 3.3 CI/CD Pipeline Standards

#### Pipeline Stages **[REQUIRED]**
```yaml
# .gitlab-ci.yml or similar
stages:
  - validate
  - build
  - test
  - scan
  - deploy

validate:
  stage: validate
  script:
    - terraform fmt -check
    - terraform validate
    - tflint
    - checkov -d .

build:
  stage: build
  script:
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG

security-scan:
  stage: scan
  script:
    - trivy image $IMAGE_TAG
    - grype image $IMAGE_TAG
    - docker scout cves $IMAGE_TAG
```

---

## 4. Serverless Architecture

### 4.1 Function Standards

#### Function Design **[REQUIRED]**
```javascript
// AWS Lambda example
exports.handler = async (event, context) => {
  // Initialize outside handler for connection reuse
  const db = await getDBConnection();

  try {
    // Input validation
    const input = validateInput(event);

    // Business logic
    const result = await processRequest(input, db);

    // Structured response
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'X-Request-ID': context.requestId
      },
      body: JSON.stringify(result)
    };
  } catch (error) {
    // Structured error handling
    logger.error('Handler error', {
      error: error.message,
      stack: error.stack,
      requestId: context.requestId
    });

    return {
      statusCode: error.statusCode || 500,
      body: JSON.stringify({
        error: error.message,
        requestId: context.requestId
      })
    };
  }
};
```

#### Configuration Standards **[REQUIRED]**
```yaml
# serverless.yml
service: myapp

provider:
  name: aws
  runtime: nodejs18.x
  memorySize: 256
  timeout: 30
  environment:
    NODE_ENV: ${opt:stage}
  tracing:
    lambda: true
  logs:
    restApi: true

functions:
  api:
    handler: src/handler.main
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true
    environment:
      DB_CONNECTION: ${ssm:/myapp/${opt:stage}/db-connection}
    vpc:
      securityGroupIds:
        - ${ssm:/myapp/${opt:stage}/sg-id}
      subnetIds:
        - ${ssm:/myapp/${opt:stage}/subnet-1}
        - ${ssm:/myapp/${opt:stage}/subnet-2}
```

### 4.2 Event-Driven Patterns

#### Event Bridge Standards **[REQUIRED]**
```json
{
  "version": "0",
  "id": "6a7e8feb-b491-4cf7-a9f1-bf3703467718",
  "detail-type": "Order Placed",
  "source": "com.company.orders",
  "account": "111122223333",
  "time": "2023-10-12T15:30:00Z",
  "region": "us-east-1",
  "detail": {
    "orderId": "12345",
    "customerId": "67890",
    "amount": 99.99,
    "currency": "USD",
    "items": [
      {
        "sku": "ITEM-001",
        "quantity": 2,
        "price": 49.99
      }
    ]
  }
}
```

#### Message Queue Standards **[REQUIRED]**
```javascript
// SQS Message Handler
const processMessage = async (message) => {
  const startTime = Date.now();
  const { Body, MessageId, Attributes } = message;

  try {
    // Parse and validate message
    const data = JSON.parse(Body);
    await validateMessage(data);

    // Process with idempotency
    const result = await processWithIdempotency(MessageId, data);

    // Delete message on success
    await sqs.deleteMessage({
      QueueUrl: process.env.QUEUE_URL,
      ReceiptHandle: message.ReceiptHandle
    }).promise();

    // Emit metrics
    metrics.recordSuccess(Date.now() - startTime);

  } catch (error) {
    // Handle poison messages
    const receiveCount = parseInt(Attributes.ApproximateReceiveCount);
    if (receiveCount > MAX_RETRIES) {
      await moveToDeadLetterQueue(message);
    }
    throw error;
  }
};
```

---

## 5. Service Mesh

### 5.1 Istio Standards

#### Service Mesh Configuration **[REQUIRED]**
```yaml
# VirtualService
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
  http:
  - match:
    - headers:
        version:
          exact: v2
    route:
    - destination:
        host: myapp
        subset: v2
  - route:
    - destination:
        host: myapp
        subset: v1
      weight: 90
    - destination:
        host: myapp
        subset: v2
      weight: 10

---
# DestinationRule
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
spec:
  host: myapp
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
    loadBalancer:
      simple: LEAST_CONN
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

#### Traffic Management **[REQUIRED]**
```yaml
# Circuit Breaker
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp-circuit-breaker
spec:
  host: myapp
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 50
```

### 5.2 Security Policies

#### mTLS Configuration **[REQUIRED]**
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT

---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: myapp-authz
spec:
  selector:
    matchLabels:
      app: myapp
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/frontend"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
```

---

## 6. Cloud Provider Standards

### 6.1 AWS Standards

#### Resource Tagging **[REQUIRED]**
```json
{
  "Tags": [
    {"Key": "Environment", "Value": "production"},
    {"Key": "Application", "Value": "myapp"},
    {"Key": "Team", "Value": "platform"},
    {"Key": "CostCenter", "Value": "engineering"},
    {"Key": "ManagedBy", "Value": "terraform"},
    {"Key": "Owner", "Value": "platform@example.com"},
    {"Key": "DataClassification", "Value": "internal"}
  ]
}
```

#### IAM Best Practices **[REQUIRED]**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

##### Least Privilege Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/data/*",
      "Condition": {
        "StringEquals": {
          "s3:ExistingObjectTag/Environment": "production"
        }
      }
    }
  ]
}
```

### 6.2 Azure Standards

#### Resource Groups **[REQUIRED]**
```bash
# Naming convention
rg-<app>-<environment>-<region>-<instance>

# Example
rg-myapp-prod-eastus-001
```

#### Azure Policy **[REQUIRED]**
```json
{
  "properties": {
    "displayName": "Require tag on resources",
    "policyType": "Custom",
    "mode": "Indexed",
    "parameters": {
      "tagName": {
        "type": "String",
        "metadata": {
          "displayName": "Tag Name",
          "description": "Name of the tag, such as 'environment'"
        }
      }
    },
    "policyRule": {
      "if": {
        "field": "[concat('tags[', parameters('tagName'), ']')]",
        "exists": "false"
      },
      "then": {
        "effect": "deny"
      }
    }
  }
}
```

### 6.3 GCP Standards

#### Project Structure **[REQUIRED]**
```
Organization
├── Folders
│   ├── Production
│   │   └── Projects
│   │       ├── prod-app-compute
│   │       ├── prod-app-data
│   │       └── prod-app-network
│   └── Non-Production
│       └── Projects
│           ├── dev-app-sandbox
│           └── staging-app-test
```

#### IAM Bindings **[REQUIRED]**
```yaml
# Terraform example
resource "google_project_iam_binding" "app_developers" {
  project = google_project.app.project_id
  role    = "roles/container.developer"

  members = [
    "group:developers@example.com",
  ]

  condition {
    title       = "Only during business hours"
    description = "Access only during business hours"
    expression  = "request.time.getHours('America/New_York') >= 9 && request.time.getHours('America/New_York') <= 17"
  }
}
```

---

## 7. Cloud-Native Security

### 7.1 Container Security

#### Image Scanning **[REQUIRED]**
```yaml
# GitHub Actions example
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: '${{ github.repository }}:${{ github.sha }}'
    format: 'sarif'
    severity: 'CRITICAL,HIGH'
    exit-code: '1'
```

#### Runtime Security **[REQUIRED]**
```yaml
# Falco rules
- rule: Unauthorized Process
  desc: Detect unauthorized process execution
  condition: >
    spawned_process and
    container and
    not proc.name in (allowed_processes)
  output: >
    Unauthorized process started
    (user=%user.name command=%proc.cmdline container=%container.info)
  priority: WARNING
```

### 7.2 Network Policies

#### Default Deny **[REQUIRED]**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

#### Application Policies **[REQUIRED]**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-network-policy
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
          name: production
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
```

### 7.3 Secrets Management

#### External Secrets **[REQUIRED]**
```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "myapp"

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
spec:
  refreshInterval: 15s
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: app-secrets
    creationPolicy: Owner
  data:
  - secretKey: database-password
    remoteRef:
      key: myapp/database
      property: password
```

---

## 8. Monitoring and Observability

### 8.1 Metrics Standards

#### Prometheus Metrics **[REQUIRED]**
```yaml
# ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

#### Custom Metrics **[REQUIRED]**
```go
// Metric naming convention
var (
    httpRequestsTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Namespace: "myapp",
            Subsystem: "http",
            Name:      "requests_total",
            Help:      "Total number of HTTP requests",
        },
        []string{"method", "endpoint", "status"},
    )

    httpRequestDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Namespace: "myapp",
            Subsystem: "http",
            Name:      "request_duration_seconds",
            Help:      "HTTP request latencies in seconds",
            Buckets:   prometheus.DefBuckets,
        },
        []string{"method", "endpoint"},
    )
)
```

### 8.2 Logging Standards

#### Structured Logging **[REQUIRED]**
```json
{
  "timestamp": "2023-10-12T15:30:00Z",
  "level": "INFO",
  "service": "myapp",
  "version": "1.2.3",
  "trace_id": "abc123",
  "span_id": "def456",
  "user_id": "user123",
  "method": "GET",
  "path": "/api/users/123",
  "status": 200,
  "duration_ms": 145,
  "message": "Request completed successfully"
}
```

#### Log Aggregation **[REQUIRED]**
```yaml
# Fluentd configuration
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<filter kubernetes.**>
  @type kubernetes_metadata
  @id filter_kube_metadata
</filter>

<match **>
  @type elasticsearch
  host elasticsearch.logging.svc.cluster.local
  port 9200
  logstash_format true
  logstash_prefix kubernetes
  <buffer>
    @type file
    path /var/log/fluentd-buffers/kubernetes.system.buffer
    flush_mode interval
    retry_type exponential_backoff
    flush_interval 5s
    retry_forever true
    retry_max_interval 30
    chunk_limit_size 2M
    queue_limit_length 8
    overflow_action drop_oldest_chunk
  </buffer>
</match>
```

### 8.3 Tracing Standards

#### OpenTelemetry **[REQUIRED]**
```javascript
const { NodeTracerProvider } = require('@opentelemetry/node');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');

const provider = new NodeTracerProvider({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'myapp',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.2.3',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV,
  }),
});

// Instrument HTTP calls
const http = require('http');
const https = require('https');
const { HttpInstrumentation } = require('@opentelemetry/instrumentation-http');

const httpInstrumentation = new HttpInstrumentation({
  requestHook: (span, request) => {
    span.setAttributes({
      'http.request.body.size': request.headers['content-length'],
    });
  },
});

httpInstrumentation.enable();
```

---

## Implementation Checklist

### Container Adoption
- [ ] Dockerfiles use multi-stage builds
- [ ] Images scanned for vulnerabilities
- [ ] Resource limits defined
- [ ] Health checks implemented
- [ ] Non-root user configured

### Kubernetes Adoption
- [ ] Namespace strategy defined
- [ ] RBAC policies implemented
- [ ] Resource quotas set
- [ ] Network policies configured
- [ ] Secrets externalized

### Infrastructure as Code
- [ ] Terraform modules created
- [ ] State management configured
- [ ] GitOps repository setup
- [ ] CI/CD pipelines automated
- [ ] Environment promotion defined

### Serverless Implementation
- [ ] Function sizing optimized
- [ ] Cold start mitigation
- [ ] Event schemas defined
- [ ] Error handling standardized
- [ ] Monitoring configured

### Security Implementation
- [ ] Image signing enabled
- [ ] Runtime security active
- [ ] Network policies enforced
- [ ] Secrets management automated
- [ ] Compliance scanning enabled

### Observability Setup
- [ ] Metrics collection configured
- [ ] Distributed tracing enabled
- [ ] Log aggregation working
- [ ] Dashboards created
- [ ] Alerts defined

---

**End of Cloud-Native Standards**
