# DevOps and Platform Engineering Standards

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active
**Standard Code:** DOP

---

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active

## Table of Contents

1. [Infrastructure as Code (IaC)](#1-infrastructure-as-code-iac)
2. [CI/CD Pipeline Standards](#2-cicd-pipeline-standards)
3. [Container Orchestration](#3-container-orchestration)
4. [Platform Engineering](#4-platform-engineering)
5. [Site Reliability Engineering](#5-site-reliability-engineering)
6. [GitOps and Deployment](#6-gitops-and-deployment)
7. [Configuration Management](#7-configuration-management)
8. [Release Management](#8-release-management)

---

## Overview

This standard provides comprehensive guidelines and best practices for the subject area.
It aims to ensure consistency, quality, and maintainability across all related implementations.

## 1. Infrastructure as Code (IaC)

### 1.1 Terraform Standards

#### Core Terraform Practices **[REQUIRED]**
```hcl
# terraform/modules/example/main.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "infrastructure/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

# Module structure
module "network" {
  source = "./modules/network"

  environment = var.environment
  cidr_block  = var.vpc_cidr

  tags = merge(
    local.common_tags,
    {
      Module = "network"
    }
  )
}
```

#### State Management **[REQUIRED]**
```yaml
# State management configuration
state_management:
  backend:
    type: "s3"  # or "azurerm", "gcs"
    encryption: true
    locking: true
    versioning: true

  workspace_strategy:
    pattern: "{environment}-{region}"
    isolation: "complete"

  security:
    access_control: "role-based"
    audit_logging: true
    state_encryption: "at-rest"
```

#### Module Design **[REQUIRED]**
```hcl
# modules/rds/variables.tf
variable "instance_class" {
  description = "RDS instance class"
  type        = string

  validation {
    condition     = can(regex("^db\\.", var.instance_class))
    error_message = "Instance class must start with 'db.'"
  }
}

variable "allocated_storage" {
  description = "Allocated storage in GB"
  type        = number
  default     = 100

  validation {
    condition     = var.allocated_storage >= 20 && var.allocated_storage <= 65536
    error_message = "Storage must be between 20 and 65536 GB."
  }
}

# modules/rds/outputs.tf
output "endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = false
}

output "connection_string" {
  description = "Database connection string"
  value       = "postgresql://${aws_db_instance.main.username}@${aws_db_instance.main.endpoint}/${aws_db_instance.main.db_name}"
  sensitive   = true
}
```

### 1.2 Ansible Automation

#### Playbook Standards **[REQUIRED]**
```yaml
# ansible/playbooks/deploy-app.yml
---
- name: Deploy Application
  hosts: app_servers
  become: yes
  gather_facts: yes

  vars_files:
    - ../vars/{{ environment }}.yml
    - ../vars/secrets.yml

  pre_tasks:
    - name: Verify target environment
      assert:
        that:
          - environment is defined
          - environment in ['dev', 'staging', 'prod']
        fail_msg: "Environment must be specified and valid"

    - name: Create deployment audit log
      lineinfile:
        path: /var/log/deployments.log
        line: "{{ ansible_date_time.iso8601 }} - {{ ansible_user }} - {{ app_version }}"
        create: yes

  roles:
    - role: common
      tags: ['always']
    - role: app-deploy
      tags: ['deploy']
    - role: health-check
      tags: ['verify']

  post_tasks:
    - name: Send deployment notification
      uri:
        url: "{{ slack_webhook_url }}"
        method: POST
        body_format: json
        body:
          text: "Deployment complete: {{ app_name }} v{{ app_version }} to {{ environment }}"
      when: notify_slack | default(true)
```

#### Role Structure **[REQUIRED]**
```yaml
# ansible/roles/app-deploy/tasks/main.yml
---
- name: Include OS-specific variables
  include_vars: "{{ ansible_os_family }}.yml"

- name: Validate deployment prerequisites
  include_tasks: validate.yml
  tags: ['validate']

- name: Prepare deployment directory
  file:
    path: "{{ app_directory }}"
    state: directory
    owner: "{{ app_user }}"
    group: "{{ app_group }}"
    mode: '0755'

- name: Deploy application artifacts
  unarchive:
    src: "{{ artifact_url }}"
    dest: "{{ app_directory }}"
    remote_src: yes
    owner: "{{ app_user }}"
    group: "{{ app_group }}"
    validate_certs: yes
  notify:
    - restart application
    - verify application health

- name: Template configuration files
  template:
    src: "{{ item.src }}"
    dest: "{{ item.dest }}"
    owner: "{{ app_user }}"
    group: "{{ app_group }}"
    mode: "{{ item.mode | default('0644') }}"
    backup: yes
  loop:
    - { src: 'app.conf.j2', dest: '/etc/app/app.conf' }
    - { src: 'env.j2', dest: '{{ app_directory }}/.env', mode: '0600' }
  notify:
    - reload configuration
```

### 1.3 Infrastructure Testing

#### Terraform Testing **[REQUIRED]**
```hcl
# tests/terraform/network_test.go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestNetworkModule(t *testing.T) {
    t.Parallel()

    terraformOptions := &terraform.Options{
        TerraformDir: "../../modules/network",
        Vars: map[string]interface{}{
            "environment": "test",
            "cidr_block":  "10.0.0.0/16",
        },
    }

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    // Validate outputs
    vpcId := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcId)

    // Test network connectivity
    validateNetworkConnectivity(t, terraformOptions)
}
```

#### Ansible Testing **[RECOMMENDED]**
```yaml
# molecule/default/molecule.yml
---
dependency:
  name: galaxy
driver:
  name: docker
platforms:
  - name: instance
    image: "geerlingguy/docker-${MOLECULE_DISTRO:-ubuntu2004}-ansible:latest"
    command: ${MOLECULE_DOCKER_COMMAND:-""}
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    privileged: true
    pre_build_image: true
provisioner:
  name: ansible
  playbooks:
    converge: ${MOLECULE_PLAYBOOK:-converge.yml}
verifier:
  name: ansible
lint: |
  set -e
  yamllint .
  ansible-lint .
```

---

## 2. CI/CD Pipeline Standards

### 2.1 Pipeline Architecture

#### Pipeline Stages **[REQUIRED]**
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  DOCKER_BUILDKIT: 1
  COMPOSE_DOCKER_CLI_BUILD: 1

jobs:
  # 1. Code Quality Stage
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for better analysis

      - name: Code Quality Checks
        run: |
          make lint
          make format-check
          make type-check

      - name: Security Scanning
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'

      - name: License Compliance
        run: |
          pip install pip-licenses
          pip-licenses --fail-on="GPL"

  # 2. Build Stage
  build:
    needs: quality
    runs-on: ubuntu-latest
    strategy:
      matrix:
        target: [app, worker]
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and Cache
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./docker/Dockerfile.${{ matrix.target }}
          push: false
          tags: app:${{ matrix.target }}-${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          outputs: type=docker,dest=/tmp/${{ matrix.target }}.tar

      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: ${{ matrix.target }}-image
          path: /tmp/${{ matrix.target }}.tar
          retention-days: 1

  # 3. Test Stage
  test:
    needs: build
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4

      - name: Download artifacts
        uses: actions/download-artifact@v3

      - name: Load Docker images
        run: |
          docker load --input app-image/app.tar
          docker load --input worker-image/worker.tar

      - name: Run Tests
        run: |
          make test-unit
          make test-integration
          make test-e2e
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test

      - name: Upload Coverage
        uses: codecov/codecov-action@v3
        with:
          fail_ci_if_error: true

  # 4. Deploy Stage
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_DEPLOY_ROLE }}
          aws-region: us-east-1

      - name: Deploy to ECS
        run: |
          make deploy-ecs ENV=production
```

#### Jenkins Pipeline **[ALTERNATIVE]**
```groovy
// Jenkinsfile
@Library('shared-pipeline-library@v2') _

pipeline {
    agent {
        kubernetes {
            yamlFile 'jenkins/pod-templates/build-pod.yaml'
        }
    }

    options {
        timeout(time: 1, unit: 'HOURS')
        timestamps()
        ansiColor('xterm')
        buildDiscarder(logRotator(numToKeepStr: '30'))
    }

    environment {
        DOCKER_REGISTRY = credentials('docker-registry')
        SONAR_TOKEN = credentials('sonar-token')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()
                }
            }
        }

        stage('Quality Gates') {
            parallel {
                stage('Lint') {
                    steps {
                        sh 'make lint'
                    }
                }
                stage('Security Scan') {
                    steps {
                        sh 'make security-scan'
                    }
                }
                stage('SonarQube') {
                    steps {
                        withSonarQubeEnv('SonarQube') {
                            sh 'make sonar-scan'
                        }
                    }
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    docker.withRegistry(DOCKER_REGISTRY) {
                        def app = docker.build("app:${GIT_COMMIT_SHORT}")
                        app.push()
                        app.push('latest')
                    }
                }
            }
        }

        stage('Test') {
            steps {
                sh 'make test-all'
                junit 'reports/**/*.xml'
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'coverage',
                    reportFiles: 'index.html',
                    reportName: 'Coverage Report'
                ])
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    deployToKubernetes(
                        namespace: 'production',
                        deployment: 'app',
                        image: "app:${GIT_COMMIT_SHORT}"
                    )
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            slackSend(
                color: 'good',
                message: "Build Successful: ${env.JOB_NAME} - ${env.BUILD_NUMBER}"
            )
        }
        failure {
            slackSend(
                color: 'danger',
                message: "Build Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}"
            )
        }
    }
}
```

### 2.2 Deployment Strategies

#### Blue-Green Deployment **[RECOMMENDED]**
```yaml
# kubernetes/deployments/blue-green.yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: myapp
    version: green  # Switch between blue/green
  ports:
    - port: 80
      targetPort: 8080

---
# Blue Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: app
        image: myapp:1.0.0
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5

---
# Green Deployment (New Version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: app
        image: myapp:2.0.0
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
```

#### Canary Deployment **[RECOMMENDED]**
```yaml
# kubernetes/deployments/canary.yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: app-canary
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  progressDeadlineSeconds: 60
  service:
    port: 80
    targetPort: 8080
    gateways:
    - public-gateway.istio-system.svc.cluster.local
    hosts:
    - app.example.com
  analysis:
    interval: 30s
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 30s
    webhooks:
    - name: load-test
      url: http://flagger-loadtester.test/
      timeout: 5s
      metadata:
        cmd: "hey -z 1m -q 10 -c 2 http://app-canary.test:80/"
```

### 2.3 Pipeline Security

#### Secret Management **[REQUIRED]**
```yaml
# .github/workflows/secrets-management.yml
name: Secure Pipeline

env:
  # Never hardcode secrets
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  API_KEY: ${{ secrets.API_KEY }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Configure HashiCorp Vault
        uses: hashicorp/vault-action@v2
        with:
          url: https://vault.example.com
          method: approle
          roleId: ${{ secrets.VAULT_ROLE_ID }}
          secretId: ${{ secrets.VAULT_SECRET_ID }}
          secrets: |
            secret/data/app database_password | DB_PASSWORD ;
            secret/data/app api_key | API_KEY

      - name: Use secrets securely
        run: |
          # Secrets are available as environment variables
          echo "::add-mask::$DB_PASSWORD"
          echo "::add-mask::$API_KEY"

          # Use secrets in deployment
          helm upgrade app ./charts/app \
            --set database.password="$DB_PASSWORD" \
            --set api.key="$API_KEY"
```

---

## 3. Container Orchestration

### 3.1 Kubernetes Operations

#### Resource Management **[REQUIRED]**
```yaml
# kubernetes/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app.kubernetes.io/name: myapp
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/component: backend
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app.kubernetes.io/name: myapp
  template:
    metadata:
      labels:
        app.kubernetes.io/name: myapp
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: app-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: app
        image: myapp:1.0.0
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/live
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/ready
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          successThreshold: 1
          failureThreshold: 3
        volumeMounts:
        - name: config
          mountPath: /etc/app
          readOnly: true
        - name: cache
          mountPath: /tmp/cache
      volumes:
      - name: config
        configMap:
          name: app-config
      - name: cache
        emptyDir:
          sizeLimit: 1Gi
```

#### Network Policies **[REQUIRED]**
```yaml
# kubernetes/network/policies.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-network-policy
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: myapp
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
          app.kubernetes.io/name: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: database
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
```

### 3.2 Helm Packaging

#### Chart Structure **[REQUIRED]**
```yaml
# charts/myapp/Chart.yaml
apiVersion: v2
name: myapp
description: A Helm chart for MyApp
type: application
version: 1.0.0
appVersion: "1.0.0"
home: https://github.com/company/myapp
sources:
  - https://github.com/company/myapp
maintainers:
  - name: Platform Team
    email: platform@company.com
dependencies:
  - name: postgresql
    version: "~12.0.0"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
  - name: redis
    version: "~17.0.0"
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
```

#### Values Configuration **[REQUIRED]**
```yaml
# charts/myapp/values.yaml
# Default values for myapp
replicaCount: 3

image:
  repository: mycompany/myapp
  pullPolicy: IfNotPresent
  tag: ""  # Overrides the image tag

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  annotations: {}
  name: ""

podAnnotations: {}

podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 2000

securityContext:
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false

service:
  type: ClusterIP
  port: 80
  targetPort: http
  annotations: {}

ingress:
  enabled: false
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: app-tls
      hosts:
        - app.example.com

resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

postgresql:
  enabled: true
  auth:
    database: myapp
    existingSecret: postgresql-secret

redis:
  enabled: true
  auth:
    enabled: true
    existingSecret: redis-secret

configMap:
  NODE_ENV: production
  LOG_LEVEL: info

secrets:
  DATABASE_URL: ""  # Set via --set or values file
  REDIS_URL: ""
  API_KEY: ""
```

### 3.3 Service Mesh

#### Istio Configuration **[RECOMMENDED]**
```yaml
# istio/virtual-service.yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp.example.com
  gateways:
  - myapp-gateway
  http:
  - match:
    - headers:
        x-version:
          exact: v2
    route:
    - destination:
        host: myapp
        subset: v2
      weight: 100
  - route:
    - destination:
        host: myapp
        subset: v1
      weight: 90
    - destination:
        host: myapp
        subset: v2
      weight: 10
    timeout: 30s
    retries:
      attempts: 3
      perTryTimeout: 10s
      retryOn: gateway-error,connect-failure,refused-stream
---
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
        http1MaxPendingRequests: 10
        http2MaxRequests: 100
        maxRequestsPerConnection: 2
    loadBalancer:
      simple: LEAST_REQUEST
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 50
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

---

## 4. Platform Engineering

### 4.1 Internal Developer Platform

#### Platform Architecture **[REQUIRED]**
```yaml
# platform/architecture.yaml
platform:
  name: "Internal Developer Platform"
  version: "2.0"

  components:
    portal:
      type: "backstage"
      features:
        - service_catalog
        - api_documentation
        - tech_radar
        - cost_insights

    ci_cd:
      type: "tekton"
      integrations:
        - github
        - gitlab
        - bitbucket

    infrastructure:
      provisioning: "crossplane"
      providers:
        - aws
        - azure
        - gcp

    observability:
      metrics: "prometheus"
      logs: "loki"
      traces: "tempo"
      visualization: "grafana"

    security:
      scanning: "trivy"
      policy: "opa"
      secrets: "vault"

  self_service:
    templates:
      - microservice
      - web_app
      - data_pipeline
      - ml_model

    resources:
      - database
      - cache
      - message_queue
      - storage_bucket
```

#### Service Catalog **[REQUIRED]**
```yaml
# backstage/catalog-info.yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-service
  description: Payment processing microservice
  tags:
    - java
    - spring-boot
    - payments
  links:
    - url: https://dashboard.example.com/payment-service
      title: Monitoring Dashboard
    - url: https://wiki.example.com/payment-service
      title: Documentation
  annotations:
    github.com/project-slug: company/payment-service
    prometheus.io/rule: 'payment_error_rate > 0.01'
    pagerduty.com/integration-key: ${PAGERDUTY_KEY}
spec:
  type: service
  lifecycle: production
  owner: team-payments
  system: payment-platform
  dependsOn:
    - component:default/user-service
    - resource:default/payment-database
  providesApis:
    - payment-api
---
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: payment-api
  description: Payment Service API
spec:
  type: openapi
  lifecycle: production
  owner: team-payments
  definition:
    $text: ./openapi/payment-api.yaml
```

#### Developer Experience **[REQUIRED]**
```typescript
// platform/cli/src/commands/create-service.ts
import { Command } from 'commander';
import { generateFromTemplate } from '../templates';
import { provisionInfrastructure } from '../infrastructure';
import { setupPipeline } from '../cicd';

export const createServiceCommand = new Command('create-service')
  .description('Create a new microservice with all platform integrations')
  .option('-n, --name <name>', 'Service name')
  .option('-t, --template <template>', 'Service template', 'microservice')
  .option('-l, --language <language>', 'Programming language', 'typescript')
  .option('--with-database', 'Include database', false)
  .option('--with-cache', 'Include cache', false)
  .action(async (options) => {
    console.log('🚀 Creating new service...');

    // Generate code from template
    const servicePath = await generateFromTemplate({
      template: options.template,
      language: options.language,
      name: options.name,
      features: {
        database: options.withDatabase,
        cache: options.withCache,
      },
    });

    // Provision infrastructure
    const infrastructure = await provisionInfrastructure({
      service: options.name,
      resources: {
        kubernetes: {
          namespace: options.name,
          serviceAccount: true,
        },
        database: options.withDatabase ? {
          type: 'postgresql',
          size: 'small',
        } : undefined,
        cache: options.withCache ? {
          type: 'redis',
          size: 'small',
        } : undefined,
      },
    });

    // Setup CI/CD pipeline
    const pipeline = await setupPipeline({
      service: options.name,
      repository: `company/${options.name}`,
      stages: ['build', 'test', 'scan', 'deploy'],
      environments: ['dev', 'staging', 'prod'],
    });

    console.log('✅ Service created successfully!');
    console.log(`📁 Code: ${servicePath}`);
    console.log(`🏗️  Infrastructure: ${infrastructure.dashboardUrl}`);
    console.log(`🔄 Pipeline: ${pipeline.url}`);
  });
```

### 4.2 Self-Service Infrastructure

#### Resource Templates **[REQUIRED]**
```yaml
# platform/templates/database.yaml
apiVersion: platform.io/v1
kind: ResourceTemplate
metadata:
  name: postgresql-database
  description: PostgreSQL database instance
spec:
  parameters:
    - name: size
      type: string
      description: Database size (small, medium, large)
      default: small
      enum: [small, medium, large]
    - name: version
      type: string
      description: PostgreSQL version
      default: "15"
      enum: ["13", "14", "15"]
    - name: highAvailability
      type: boolean
      description: Enable high availability
      default: false

  resources:
    - apiVersion: postgresql.cnpg.io/v1
      kind: Cluster
      metadata:
        name: "{{ .Name }}-postgres"
        namespace: "{{ .Namespace }}"
      spec:
        instances: "{{ if .Values.highAvailability }}3{{ else }}1{{ end }}"
        postgresql:
          parameters:
            max_connections: "200"
            shared_buffers: "256MB"
        bootstrap:
          initdb:
            database: "{{ .Name }}"
            owner: "{{ .Name }}"
            secret:
              name: "{{ .Name }}-postgres-secret"
        storage:
          size: |
            {{- if eq .Values.size "small" }}10Gi
            {{- else if eq .Values.size "medium" }}50Gi
            {{- else if eq .Values.size "large" }}200Gi
            {{- end }}
        monitoring:
          enabled: true
        backup:
          enabled: true
          retentionPolicy: "30d"
```

#### Platform API **[REQUIRED]**
```go
// platform/api/handlers/resource.go
package handlers

import (
    "net/http"
    "github.com/gin-gonic/gin"
    "platform/internal/resources"
    "platform/internal/auth"
)

type CreateResourceRequest struct {
    Type       string                 `json:"type" binding:"required"`
    Name       string                 `json:"name" binding:"required"`
    Team       string                 `json:"team" binding:"required"`
    Parameters map[string]interface{} `json:"parameters"`
}

func CreateResource(c *gin.Context) {
    var req CreateResourceRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    // Validate team ownership
    user := auth.GetUser(c)
    if !user.IsInTeam(req.Team) {
        c.JSON(http.StatusForbidden, gin.H{"error": "not authorized for team"})
        return
    }

    // Create resource
    resource, err := resources.Create(c.Request.Context(), resources.CreateOptions{
        Type:       req.Type,
        Name:       req.Name,
        Team:       req.Team,
        Parameters: req.Parameters,
        CreatedBy:  user.Email,
    })
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    // Audit log
    audit.Log(c.Request.Context(), audit.Entry{
        Action:   "resource.create",
        Resource: resource.ID,
        User:     user.Email,
        Team:     req.Team,
    })

    c.JSON(http.StatusCreated, gin.H{
        "id":          resource.ID,
        "status":      resource.Status,
        "dashboardUrl": resource.DashboardURL,
        "credentials": resource.Credentials,
    })
}
```

---

## 5. Site Reliability Engineering

### 5.1 Service Level Objectives

#### SLO Definition **[REQUIRED]**
```yaml
# sre/slos/payment-service.yaml
apiVersion: sloth.slok.dev/v1
kind: PrometheusServiceLevel
metadata:
  name: payment-service
  labels:
    team: payments
    tier: critical
spec:
  service: payment-service
  labels:
    team: payments
  slos:
    - name: availability
      objective: 99.9
      description: "99.9% of requests should be successful"
      sli:
        events:
          error_query: |
            sum(rate(http_requests_total{
              service="payment-service",
              status=~"5.."
            }[5m]))
          total_query: |
            sum(rate(http_requests_total{
              service="payment-service"
            }[5m]))
      alerting:
        name: PaymentServiceAvailability
        page_alert:
          labels:
            severity: critical
            team: payments
        ticket_alert:
          labels:
            severity: warning
            team: payments

    - name: latency
      objective: 99
      description: "99% of requests should complete within 500ms"
      sli:
        events:
          error_query: |
            sum(rate(http_request_duration_seconds_bucket{
              service="payment-service",
              le="0.5"
            }[5m]))
          total_query: |
            sum(rate(http_request_duration_seconds_count{
              service="payment-service"
            }[5m]))
      alerting:
        name: PaymentServiceLatency
        page_alert:
          labels:
            severity: critical
```

#### Error Budget Policy **[REQUIRED]**
```yaml
# sre/policies/error-budget.yaml
error_budget_policy:
  payment_service:
    slo_target: 99.9
    measurement_window: 30d

    thresholds:
      - remaining_budget: 75%
        actions:
          - type: notification
            target: team-slack
            message: "Error budget at 75% - review recent changes"

      - remaining_budget: 50%
        actions:
          - type: review
            description: "Mandatory review of recent deployments"
          - type: slow_rollout
            description: "Reduce deployment velocity to 1/day"

      - remaining_budget: 25%
        actions:
          - type: freeze
            description: "Feature freeze - only critical fixes"
          - type: incident_review
            description: "Conduct thorough incident analysis"

      - remaining_budget: 0%
        actions:
          - type: halt_deployments
            description: "Stop all non-emergency deployments"
          - type: dedicated_response
            description: "Assign dedicated team to reliability"

    exemptions:
      - type: security_patch
        approval: security_team
      - type: data_corruption_fix
        approval: engineering_director
```

### 5.2 Incident Management

#### Incident Response **[REQUIRED]**
```yaml
# sre/runbooks/incident-response.yaml
incident_response:
  roles:
    incident_commander:
      responsibilities:
        - Overall incident coordination
        - External communication
        - Decision making
      backup: platform_lead

    technical_lead:
      responsibilities:
        - Technical investigation
        - Solution implementation
        - Root cause analysis
      backup: senior_engineer

    communications_lead:
      responsibilities:
        - Status page updates
        - Customer communication
        - Internal updates
      backup: product_manager

  severities:
    sev1:
      definition: "Complete service outage or data loss"
      response_time: 5_minutes
      escalation:
        - oncall_engineer
        - team_lead
        - engineering_director
        - cto
      communication:
        - status_page: immediate
        - customer_email: 15_minutes
        - executive_brief: 30_minutes

    sev2:
      definition: "Major feature unavailable or significant degradation"
      response_time: 15_minutes
      escalation:
        - oncall_engineer
        - team_lead
      communication:
        - status_page: 15_minutes
        - customer_email: 1_hour

    sev3:
      definition: "Minor feature unavailable or minor degradation"
      response_time: 1_hour
      escalation:
        - oncall_engineer
      communication:
        - status_page: 1_hour

  procedures:
    initial_response:
      - Acknowledge alert within SLA
      - Assess severity and impact
      - Create incident channel
      - Assign roles
      - Begin investigation

    investigation:
      - Review monitoring dashboards
      - Check recent deployments
      - Analyze logs and traces
      - Test hypotheses
      - Document findings

    mitigation:
      - Implement immediate fixes
      - Consider rollback if needed
      - Monitor impact of changes
      - Update stakeholders

    resolution:
      - Verify issue is resolved
      - Monitor for recurrence
      - Update status page
      - Schedule post-mortem
```

#### Runbook Automation **[REQUIRED]**
```python
# sre/automation/runbooks/database_recovery.py
#!/usr/bin/env python3
"""
Automated database recovery runbook
"""
import logging
import time
from typing import Dict, List
import boto3
import psycopg2
from datadog import api
from slack_sdk import WebClient

logger = logging.getLogger(__name__)

class DatabaseRecoveryRunbook:
    def __init__(self):
        self.rds_client = boto3.client('rds')
        self.cloudwatch = boto3.client('cloudwatch')
        self.slack = WebClient(token=os.environ['SLACK_TOKEN'])
        self.incident_channel = None

    def execute(self, alert_data: Dict) -> None:
        """Execute database recovery runbook"""
        try:
            # 1. Create incident channel
            self.incident_channel = self._create_incident_channel(alert_data)

            # 2. Assess database state
            db_state = self._assess_database_state(alert_data['db_identifier'])
            self._post_to_slack(f"Database state: {db_state}")

            # 3. Determine recovery action
            if db_state['status'] == 'failed':
                self._initiate_failover(alert_data['db_identifier'])
            elif db_state['connections'] > db_state['max_connections'] * 0.9:
                self._terminate_idle_connections(alert_data['db_identifier'])
            elif db_state['cpu_utilization'] > 90:
                self._scale_up_instance(alert_data['db_identifier'])

            # 4. Monitor recovery
            self._monitor_recovery(alert_data['db_identifier'])

            # 5. Validate recovery
            if self._validate_recovery(alert_data['db_identifier']):
                self._post_to_slack("✅ Database recovered successfully")
                self._close_incident()
            else:
                self._escalate_incident()

        except Exception as e:
            logger.error(f"Runbook execution failed: {e}")
            self._escalate_incident()

    def _assess_database_state(self, db_identifier: str) -> Dict:
        """Assess current database state"""
        # Get RDS instance status
        response = self.rds_client.describe_db_instances(
            DBInstanceIdentifier=db_identifier
        )
        instance = response['DBInstances'][0]

        # Get performance metrics
        metrics = self._get_performance_metrics(db_identifier)

        # Check replica lag if applicable
        replica_lag = self._check_replica_lag(db_identifier)

        return {
            'status': instance['DBInstanceStatus'],
            'endpoint': instance.get('Endpoint', {}).get('Address'),
            'connections': metrics['DatabaseConnections'],
            'max_connections': self._get_max_connections(instance),
            'cpu_utilization': metrics['CPUUtilization'],
            'replica_lag': replica_lag,
            'storage_free': metrics['FreeStorageSpace'],
        }

    def _initiate_failover(self, db_identifier: str) -> None:
        """Initiate database failover"""
        self._post_to_slack("🔄 Initiating database failover...")

        try:
            # For Multi-AZ deployments
            self.rds_client.reboot_db_instance(
                DBInstanceIdentifier=db_identifier,
                ForceFailover=True
            )

            # Wait for failover to complete
            waiter = self.rds_client.get_waiter('db_instance_available')
            waiter.wait(
                DBInstanceIdentifier=db_identifier,
                WaiterConfig={
                    'Delay': 30,
                    'MaxAttempts': 40
                }
            )

            self._post_to_slack("✅ Failover completed successfully")

        except Exception as e:
            logger.error(f"Failover failed: {e}")
            raise
```

### 5.3 Chaos Engineering

#### Chaos Experiments **[RECOMMENDED]**
```yaml
# chaos/experiments/payment-service.yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: Schedule
metadata:
  name: payment-service-chaos
  namespace: chaos-testing
spec:
  schedule: "0 10 * * 1-5"  # Weekdays at 10 AM
  concurrencyPolicy: Forbid
  type: PodChaos
  podChaos:
    action: pod-kill
    mode: one
    duration: "60s"
    selector:
      namespaces:
        - production
      labelSelectors:
        "app.kubernetes.io/name": "payment-service"
    scheduler:
      cron: "@hourly"
---
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: payment-network-delay
spec:
  action: delay
  mode: all
  selector:
    namespaces:
      - production
    labelSelectors:
      "app.kubernetes.io/name": "payment-service"
  delay:
    latency: "100ms"
    correlation: "25"
    jitter: "10ms"
  duration: "5m"
  scheduler:
    cron: "0 */4 * * *"
---
apiVersion: chaos-mesh.org/v1alpha1
kind: StressChaos
metadata:
  name: payment-cpu-stress
spec:
  mode: one
  selector:
    namespaces:
      - production
    labelSelectors:
      "app.kubernetes.io/name": "payment-service"
  stressors:
    cpu:
      workers: 2
      load: 80
  duration: "3m"
```

#### Gameday Automation **[RECOMMENDED]**
```python
# chaos/gameday/scenarios.py
import asyncio
from typing import List, Dict
import structlog
from chaos_toolkit import run_experiment
from prometheus_client import Gauge

logger = structlog.get_logger()

# Metrics
gameday_score = Gauge('gameday_score', 'Gameday scenario score', ['scenario'])
gameday_mttr = Gauge('gameday_mttr', 'Mean time to recovery', ['scenario'])

class GamedayScenario:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.start_time = None
        self.recovery_time = None

    async def run(self) -> Dict:
        """Run gameday scenario"""
        logger.info("Starting gameday scenario", scenario=self.name)
        self.start_time = asyncio.get_event_loop().time()

        try:
            # Run chaos experiment
            result = await self._execute_chaos()

            # Monitor system behavior
            impact = await self._monitor_impact()

            # Verify auto-recovery
            recovery = await self._verify_recovery()

            # Calculate metrics
            self.recovery_time = asyncio.get_event_loop().time()
            mttr = self.recovery_time - self.start_time

            # Score the scenario
            score = self._calculate_score(impact, recovery, mttr)

            # Update metrics
            gameday_score.labels(scenario=self.name).set(score)
            gameday_mttr.labels(scenario=self.name).set(mttr)

            return {
                'scenario': self.name,
                'success': True,
                'score': score,
                'mttr': mttr,
                'impact': impact,
                'recovery': recovery,
            }

        except Exception as e:
            logger.error("Gameday scenario failed", scenario=self.name, error=str(e))
            return {
                'scenario': self.name,
                'success': False,
                'error': str(e),
            }

    async def _execute_chaos(self) -> Dict:
        """Execute chaos experiment"""
        experiment = {
            "version": "1.0.0",
            "title": f"Gameday: {self.name}",
            "description": self.description,
            "steady-state-hypothesis": {
                "title": "System is healthy",
                "probes": [
                    {
                        "type": "probe",
                        "name": "service-available",
                        "provider": {
                            "type": "http",
                            "url": "http://payment-service/health",
                            "timeout": 5,
                        },
                    },
                ],
            },
            "method": [
                {
                    "type": "action",
                    "name": "inject-failure",
                    "provider": {
                        "type": "python",
                        "module": "chaosaws.ec2.actions",
                        "func": "terminate_instances",
                        "arguments": {
                            "instance_ids": ["i-1234567890abcdef0"],
                        },
                    },
                },
            ],
            "rollbacks": [],
        }

        return await asyncio.to_thread(run_experiment, experiment)
```

---

## 6. GitOps and Deployment

### 6.1 GitOps Workflows

#### ArgoCD Configuration **[REQUIRED]**
```yaml
# argocd/applications/production.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payment-service-prod
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: production
  source:
    repoURL: https://github.com/company/payment-service
    targetRevision: main
    path: kubernetes/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: payment-service
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  revisionHistoryLimit: 10
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /spec/replicas
  - group: autoscaling
    kind: HorizontalPodAutoscaler
    jsonPointers:
    - /spec/minReplicas
    - /spec/maxReplicas
```

#### Flux Configuration **[ALTERNATIVE]**
```yaml
# flux/clusters/production/payment-service.yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository
metadata:
  name: payment-service
  namespace: flux-system
spec:
  interval: 1m
  ref:
    branch: main
  url: https://github.com/company/payment-service
  secretRef:
    name: github-token
---
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: payment-service
  namespace: flux-system
spec:
  interval: 10m
  path: "./kubernetes/overlays/production"
  prune: true
  sourceRef:
    kind: GitRepository
    name: payment-service
  validation: client
  timeout: 5m
  retryInterval: 2m
  targetNamespace: payment-service
  postBuild:
    substitute:
      cluster_env: production
      region: us-east-1
    substituteFrom:
    - kind: ConfigMap
      name: cluster-config
    - kind: Secret
      name: cluster-secrets
  healthChecks:
  - apiVersion: apps/v1
    kind: Deployment
    name: payment-service
    namespace: payment-service
  - apiVersion: v1
    kind: Service
    name: payment-service
    namespace: payment-service
```

### 6.2 Progressive Delivery

#### Flagger Configuration **[RECOMMENDED]**
```yaml
# flagger/canary/payment-service.yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: payment-service
  namespace: production
spec:
  provider: istio
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: payment-service
  progressDeadlineSeconds: 600
  service:
    port: 80
    targetPort: 8080
    gateways:
    - public-gateway.istio-system.svc.cluster.local
    hosts:
    - payment.example.com
    trafficPolicy:
      tls:
        mode: SIMPLE
    match:
    - headers:
        x-canary:
          exact: "true"
  analysis:
    interval: 1m
    threshold: 10
    maxWeight: 50
    stepWeight: 5
    stepWeightPromotion: 10
    metrics:
    - name: request-success-rate
      templateRef:
        name: success-rate
        namespace: flagger-system
      thresholdRange:
        min: 99
      interval: 1m
    - name: request-duration
      templateRef:
        name: latency
        namespace: flagger-system
      thresholdRange:
        max: 500
      interval: 1m
    - name: error-rate
      templateRef:
        name: error-rate
        namespace: flagger-system
      thresholdRange:
        max: 1
      interval: 1m
    webhooks:
    - name: smoke-test
      type: pre-rollout
      url: http://flagger-loadtester.test/
      timeout: 15s
      metadata:
        type: smoke
        cmd: "curl -s http://payment-service-canary/health"
    - name: load-test
      type: rollout
      url: http://flagger-loadtester.test/
      timeout: 5s
      metadata:
        type: cmd
        cmd: "hey -z 1m -q 100 -c 10 http://payment-service-canary/"
    - name: rollback-notification
      type: rollback
      url: http://webhook.example.com/
      metadata:
        environment: production
        service: payment-service
  alerts:
  - name: "payment-service canary"
    severity: info
    providerRef:
      name: slack
      namespace: flagger-system
```

---

## 7. Configuration Management

### 7.1 Configuration Standards

#### External Configuration **[REQUIRED]**
```yaml
# kubernetes/configmaps/app-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: payment-service-config
  namespace: production
  labels:
    app.kubernetes.io/name: payment-service
    app.kubernetes.io/component: configuration
data:
  application.yaml: |
    server:
      port: 8080
      shutdown: graceful

    spring:
      application:
        name: payment-service

      datasource:
        hikari:
          maximum-pool-size: 20
          minimum-idle: 5
          connection-timeout: 30000
          idle-timeout: 600000
          max-lifetime: 1800000

    management:
      endpoints:
        web:
          exposure:
            include: health,info,metrics,prometheus
      metrics:
        export:
          prometheus:
            enabled: true

    resilience4j:
      circuitbreaker:
        instances:
          payment-gateway:
            sliding-window-size: 100
            permitted-number-of-calls-in-half-open-state: 10
            wait-duration-in-open-state: 60000
            failure-rate-threshold: 50
            slow-call-rate-threshold: 50
            slow-call-duration-threshold: 2000

      retry:
        instances:
          payment-gateway:
            max-attempts: 3
            wait-duration: 1000
            retry-exceptions:
              - java.net.SocketTimeoutException
              - java.io.IOException
```

#### Secret Management **[REQUIRED]**
```yaml
# kubernetes/secrets/sealed-secrets.yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: payment-service-secrets
  namespace: production
spec:
  encryptedData:
    database-url: AgBvA7sF2H... # Encrypted value
    api-key: AgCpQ9kL3M... # Encrypted value
    jwt-secret: AgDrS4mN5P... # Encrypted value
  template:
    metadata:
      name: payment-service-secrets
      namespace: production
    type: Opaque
```

#### Dynamic Configuration **[RECOMMENDED]**
```go
// config/dynamic/client.go
package dynamic

import (
    "context"
    "fmt"
    "sync"
    "time"

    "github.com/hashicorp/consul/api"
    "go.uber.org/zap"
)

type ConfigClient struct {
    consul      *api.Client
    logger      *zap.Logger
    cache       sync.Map
    subscribers map[string][]chan string
    mu          sync.RWMutex
}

func NewConfigClient(consulAddr string, logger *zap.Logger) (*ConfigClient, error) {
    config := api.DefaultConfig()
    config.Address = consulAddr

    client, err := api.NewClient(config)
    if err != nil {
        return nil, fmt.Errorf("failed to create consul client: %w", err)
    }

    cc := &ConfigClient{
        consul:      client,
        logger:      logger,
        subscribers: make(map[string][]chan string),
    }

    // Start watching for changes
    go cc.watchChanges(context.Background())

    return cc, nil
}

func (c *ConfigClient) Get(key string) (string, error) {
    // Check cache first
    if value, ok := c.cache.Load(key); ok {
        return value.(string), nil
    }

    // Fetch from Consul
    kv := c.consul.KV()
    pair, _, err := kv.Get(key, nil)
    if err != nil {
        return "", fmt.Errorf("failed to get key %s: %w", key, err)
    }

    if pair == nil {
        return "", fmt.Errorf("key %s not found", key)
    }

    value := string(pair.Value)
    c.cache.Store(key, value)

    return value, nil
}

func (c *ConfigClient) Watch(key string) <-chan string {
    c.mu.Lock()
    defer c.mu.Unlock()

    ch := make(chan string, 1)
    c.subscribers[key] = append(c.subscribers[key], ch)

    // Send current value
    if value, err := c.Get(key); err == nil {
        ch <- value
    }

    return ch
}

func (c *ConfigClient) watchChanges(ctx context.Context) {
    kv := c.consul.KV()

    for {
        select {
        case <-ctx.Done():
            return
        default:
            keys, _, err := kv.List("", nil)
            if err != nil {
                c.logger.Error("Failed to list keys", zap.Error(err))
                time.Sleep(5 * time.Second)
                continue
            }

            for _, key := range keys {
                oldValue, _ := c.cache.Load(key.Key)
                newValue := string(key.Value)

                if oldValue != newValue {
                    c.cache.Store(key.Key, newValue)
                    c.notifySubscribers(key.Key, newValue)
                }
            }

            time.Sleep(10 * time.Second)
        }
    }
}
```

### 7.2 Feature Flags

#### Feature Flag System **[RECOMMENDED]**
```yaml
# featureflags/flags.yaml
flags:
  - key: new-payment-provider
    description: Enable new payment provider integration
    enabled: false
    rules:
      - type: percentage
        enabled: true
        percentage: 10
        conditions:
          - attribute: region
            operator: in
            values: [us-east-1, us-west-2]

      - type: user-list
        enabled: true
        users:
          - user123
          - user456

      - type: group
        enabled: true
        groups:
          - beta-testers
          - internal-users

  - key: enhanced-fraud-detection
    description: Use ML-based fraud detection
    enabled: true
    rules:
      - type: gradual-rollout
        enabled: true
        stages:
          - percentage: 5
            duration: 1h
          - percentage: 25
            duration: 24h
          - percentage: 50
            duration: 72h
          - percentage: 100
```

---

## 8. Release Management

### 8.1 Versioning Strategy

#### Semantic Versioning **[REQUIRED]**
```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Calculate Version
        id: version
        uses: mathieudutour/github-tag-action@v6.1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          default_bump: patch
          release_branches: main
          pre_release_branches: develop
          custom_release_rules: |
            breaking:major:Breaking Changes
            feat:minor:Features
            fix:patch:Bug Fixes
            perf:patch:Performance

      - name: Generate Changelog
        id: changelog
        run: |
          npm install -g conventional-changelog-cli
          conventional-changelog -p angular -i CHANGELOG.md -s -r 0

      - name: Create Release
        uses: ncipollo/release-action@v1
        with:
          tag: ${{ steps.version.outputs.new_tag }}
          name: Release ${{ steps.version.outputs.new_tag }}
          body: ${{ steps.version.outputs.changelog }}
          artifacts: |
            dist/*
            checksums.txt
```

#### Release Notes Automation **[REQUIRED]**
```typescript
// scripts/generate-release-notes.ts
import { Octokit } from '@octokit/rest';
import { getChangelogEntry } from 'conventional-changelog';

interface ReleaseNotes {
  version: string;
  date: string;
  breaking: string[];
  features: string[];
  fixes: string[];
  performance: string[];
  security: string[];
  dependencies: string[];
}

async function generateReleaseNotes(
  owner: string,
  repo: string,
  fromTag: string,
  toTag: string
): Promise<ReleaseNotes> {
  const octokit = new Octokit({
    auth: process.env.GITHUB_TOKEN,
  });

  // Get commits between tags
  const commits = await octokit.repos.compareCommits({
    owner,
    repo,
    base: fromTag,
    head: toTag,
  });

  // Parse commit messages
  const notes: ReleaseNotes = {
    version: toTag,
    date: new Date().toISOString(),
    breaking: [],
    features: [],
    fixes: [],
    performance: [],
    security: [],
    dependencies: [],
  };

  for (const commit of commits.data.commits) {
    const message = commit.commit.message;

    if (message.includes('BREAKING CHANGE:')) {
      notes.breaking.push(extractDescription(message));
    } else if (message.startsWith('feat:')) {
      notes.features.push(extractDescription(message));
    } else if (message.startsWith('fix:')) {
      notes.fixes.push(extractDescription(message));
    } else if (message.startsWith('perf:')) {
      notes.performance.push(extractDescription(message));
    } else if (message.startsWith('security:')) {
      notes.security.push(extractDescription(message));
    } else if (message.startsWith('deps:')) {
      notes.dependencies.push(extractDescription(message));
    }
  }

  return notes;
}

function formatReleaseNotes(notes: ReleaseNotes): string {
  let output = `# Release ${notes.version}\n\n`;
  output += `Released: ${notes.date}\n\n`;

  if (notes.breaking.length > 0) {
    output += '## ⚠️ Breaking Changes\n\n';
    notes.breaking.forEach(item => output += `- ${item}\n`);
    output += '\n';
  }

  if (notes.features.length > 0) {
    output += '## ✨ Features\n\n';
    notes.features.forEach(item => output += `- ${item}\n`);
    output += '\n';
  }

  if (notes.fixes.length > 0) {
    output += '## 🐛 Bug Fixes\n\n';
    notes.fixes.forEach(item => output += `- ${item}\n`);
    output += '\n';
  }

  if (notes.security.length > 0) {
    output += '## 🔒 Security\n\n';
    notes.security.forEach(item => output += `- ${item}\n`);
    output += '\n';
  }

  if (notes.performance.length > 0) {
    output += '## ⚡ Performance\n\n';
    notes.performance.forEach(item => output += `- ${item}\n`);
    output += '\n';
  }

  if (notes.dependencies.length > 0) {
    output += '## 📦 Dependencies\n\n';
    notes.dependencies.forEach(item => output += `- ${item}\n`);
    output += '\n';
  }

  return output;
}
```

### 8.2 Rollback Procedures

#### Automated Rollback **[REQUIRED]**
```yaml
# kubernetes/rollback/policy.yaml
apiVersion: flagger.app/v1beta1
kind: AlertProvider
metadata:
  name: rollback-webhook
  namespace: flagger-system
spec:
  type: webhook
  address: http://rollback-controller.platform/webhook
  secret:
    name: rollback-webhook-secret
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: rollback-policy
  namespace: platform
data:
  policy.yaml: |
    rollback_triggers:
      - name: high_error_rate
        condition: "error_rate > 5%"
        duration: 5m
        action: immediate

      - name: latency_degradation
        condition: "p99_latency > 2 * baseline"
        duration: 10m
        action: immediate

      - name: memory_leak
        condition: "memory_usage_rate > 10MB/min"
        duration: 30m
        action: scheduled

      - name: crash_loop
        condition: "restart_count > 5"
        duration: 15m
        action: immediate

    rollback_procedures:
      immediate:
        - pause_deployments
        - revert_to_previous
        - notify_oncall
        - create_incident

      scheduled:
        - notify_team
        - schedule_rollback
        - monitor_metrics
        - prepare_hotfix
```

#### Manual Rollback Procedures **[REQUIRED]**
```bash
#!/bin/bash
# scripts/rollback.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
NAMESPACE=${NAMESPACE:-production}
SERVICE=${SERVICE:-}
VERSION=${VERSION:-}

function usage() {
    echo "Usage: $0 -s SERVICE -v VERSION [-n NAMESPACE]"
    echo "  -s SERVICE    Service name to rollback"
    echo "  -v VERSION    Version to rollback to"
    echo "  -n NAMESPACE  Kubernetes namespace (default: production)"
    exit 1
}

function log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

function error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" >&2
}

function warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

# Parse arguments
while getopts "s:v:n:h" opt; do
    case ${opt} in
        s) SERVICE=$OPTARG ;;
        v) VERSION=$OPTARG ;;
        n) NAMESPACE=$OPTARG ;;
        h) usage ;;
        *) usage ;;
    esac
done

# Validate arguments
if [[ -z "$SERVICE" ]] || [[ -z "$VERSION" ]]; then
    error "Service and version are required"
    usage
fi

# Main rollback procedure
function main() {
    log "Starting rollback for $SERVICE to version $VERSION in namespace $NAMESPACE"

    # 1. Check current deployment
    log "Checking current deployment..."
    CURRENT_VERSION=$(kubectl get deployment "$SERVICE" -n "$NAMESPACE" \
        -o jsonpath='{.spec.template.spec.containers[0].image}' | cut -d: -f2)
    log "Current version: $CURRENT_VERSION"

    if [[ "$CURRENT_VERSION" == "$VERSION" ]]; then
        warning "Already at version $VERSION, nothing to do"
        exit 0
    fi

    # 2. Create backup of current state
    log "Creating backup of current deployment..."
    kubectl get deployment "$SERVICE" -n "$NAMESPACE" -o yaml > \
        "/tmp/${SERVICE}-${CURRENT_VERSION}-backup.yaml"

    # 3. Check if target version exists
    log "Verifying target version exists..."
    if ! docker manifest inspect "${REGISTRY}/${SERVICE}:${VERSION}" &>/dev/null; then
        error "Version $VERSION not found in registry"
        exit 1
    fi

    # 4. Update deployment
    log "Rolling back to version $VERSION..."
    kubectl set image "deployment/$SERVICE" \
        "${SERVICE}=${REGISTRY}/${SERVICE}:${VERSION}" \
        -n "$NAMESPACE" \
        --record

    # 5. Monitor rollout
    log "Monitoring rollout status..."
    if ! kubectl rollout status "deployment/$SERVICE" -n "$NAMESPACE" --timeout=10m; then
        error "Rollback failed, attempting to restore previous version"
        kubectl apply -f "/tmp/${SERVICE}-${CURRENT_VERSION}-backup.yaml"
        exit 1
    fi

    # 6. Verify health
    log "Verifying service health..."
    sleep 30  # Give pods time to stabilize

    READY_REPLICAS=$(kubectl get deployment "$SERVICE" -n "$NAMESPACE" \
        -o jsonpath='{.status.readyReplicas}')
    DESIRED_REPLICAS=$(kubectl get deployment "$SERVICE" -n "$NAMESPACE" \
        -o jsonpath='{.spec.replicas}')

    if [[ "$READY_REPLICAS" != "$DESIRED_REPLICAS" ]]; then
        error "Not all replicas are ready: $READY_REPLICAS/$DESIRED_REPLICAS"
        exit 1
    fi

    # 7. Run smoke tests
    log "Running smoke tests..."
    if command -v smoke-test &>/dev/null; then
        smoke-test --service "$SERVICE" --namespace "$NAMESPACE"
    else
        warning "Smoke test command not found, skipping"
    fi

    # 8. Update incident
    log "Updating incident tracking..."
    if [[ -n "${INCIDENT_ID:-}" ]]; then
        incident-cli update "$INCIDENT_ID" \
            --status "mitigated" \
            --comment "Rolled back $SERVICE from $CURRENT_VERSION to $VERSION"
    fi

    log "Rollback completed successfully!"
    log "Service $SERVICE is now running version $VERSION"
}

# Execute main function
main
```

### 8.3 Deployment Monitoring

#### Deployment Metrics **[REQUIRED]**
```yaml
# monitoring/deployment-dashboard.json
{
  "dashboard": {
    "title": "Deployment Monitoring",
    "panels": [
      {
        "title": "Deployment Frequency",
        "targets": [
          {
            "expr": "sum(rate(deployments_total[1h])) by (service)",
            "legendFormat": "{{ service }}"
          }
        ]
      },
      {
        "title": "Deployment Success Rate",
        "targets": [
          {
            "expr": "sum(rate(deployments_total{status=\"success\"}[1h])) / sum(rate(deployments_total[1h])) * 100",
            "legendFormat": "Success Rate %"
          }
        ]
      },
      {
        "title": "Mean Time to Recovery",
        "targets": [
          {
            "expr": "avg(deployment_rollback_duration_seconds) by (service)",
            "legendFormat": "{{ service }}"
          }
        ]
      },
      {
        "title": "Change Failure Rate",
        "targets": [
          {
            "expr": "sum(rate(deployments_total{status=\"failed\"}[7d])) / sum(rate(deployments_total[7d])) * 100",
            "legendFormat": "Failure Rate %"
          }
        ]
      }
    ]
  }
}
```

---

## Implementation Guidelines

### Adoption Strategy
1. **Assessment Phase**: Evaluate current DevOps maturity
2. **Foundation Phase**: Implement core IaC and CI/CD standards
3. **Platform Phase**: Build internal developer platform
4. **Optimization Phase**: Add SRE practices and chaos engineering
5. **Excellence Phase**: Achieve full automation and self-service

### Tool Selection Criteria
- **Compatibility**: Integration with existing tools
- **Scalability**: Support for growth
- **Community**: Active development and support
- **Security**: Built-in security features
- **Cost**: TCO including licenses and operations

### Success Metrics
- **Deployment Frequency**: Daily deployments per service
- **Lead Time**: < 1 hour from commit to production
- **MTTR**: < 30 minutes for critical services
- **Change Failure Rate**: < 5% of deployments
- **Platform Adoption**: > 90% of teams using IDP

---

**End of DevOps and Platform Engineering Standards**
