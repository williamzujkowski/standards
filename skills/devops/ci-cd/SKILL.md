---
name: ci-cd
description: CI/CD pipeline standards for GitHub Actions, GitLab CI, and deployment automation. Covers testing gates, security scanning, artifact management, and deployment strategies for reliable software delivery.
---

# CI/CD DevOps Standards

> **Quick Navigation:**
> Level 1: [Quick Start](#level-1-quick-start-2000-tokens-5-minutes) (5 min) → Level 2: [Implementation](#level-2-implementation-5000-tokens-30-minutes) (30 min) → Level 3: [Mastery](#level-3-mastery-resources) (Extended)

---

## Level 1: Quick Start (<2,000 tokens, 5 minutes)

### Core Principles

1. **Automate Everything**: Build, test, security scan, and deploy automatically
2. **Fail Fast**: Detect issues early with comprehensive testing gates
3. **Security First**: Scan dependencies, containers, and code for vulnerabilities
4. **Reproducible Builds**: Same code → same artifact every time
5. **Rapid Rollback**: Deploy with confidence, roll back quickly if needed

### Essential Checklist

- [ ] **Continuous Integration**: Automated builds and tests on every commit
- [ ] **Testing Gates**: Unit tests pass (>80% coverage), integration tests pass
- [ ] **Security Scanning**: Dependency vulnerabilities checked, SAST enabled
- [ ] **Artifact Management**: Built artifacts stored with version tags
- [ ] **Deployment Automation**: One-click deploy to staging/production
- [ ] **Rollback Strategy**: Automated rollback on deployment failure
- [ ] **Monitoring**: Pipeline metrics, build success rates tracked
- [ ] **Secrets Management**: No hardcoded secrets, use vault/parameter store

### Quick Example (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linters
        run: npm run lint

      - name: Run tests
        run: npm test -- --coverage

      - name: Check coverage threshold
        run: |
          COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80% threshold"
            exit 1
          fi

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run security audit
        run: npm audit --audit-level=high

      - name: SAST scan
        uses: github/codeql-action/analyze@v2

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Scan container
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:${{ github.sha }}'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Push to registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker tag myapp:${{ github.sha }} registry.example.com/myapp:${{ github.sha }}
          docker push registry.example.com/myapp:${{ github.sha }}
```

### Quick Links to Level 2

- [GitHub Actions Workflows](#github-actions-workflows)
- [GitLab CI Configuration](#gitlab-ci-configuration)
- [Testing Gates](#testing-gates)
- [Security Scanning](#security-scanning)
- [Artifact Management](#artifact-management)
- [Deployment Strategies](#deployment-strategies)
- [Environment Management](#environment-management)

---

## Level 2: Implementation (<5,000 tokens, 30 minutes)

### GitHub Actions Workflows

**Multi-Stage Pipeline**

```yaml
# .github/workflows/cd.yml
name: CD Pipeline

on:
  push:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to staging
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --namespace=staging

      - name: Wait for rollout
        run: kubectl rollout status deployment/myapp -n staging --timeout=5m

      - name: Run smoke tests
        run: |
          curl -f https://staging.example.com/health || exit 1

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
    steps:
      - uses: actions/checkout@v4

      - name: Blue-green deployment
        run: |
          # Deploy to green environment
          kubectl set image deployment/myapp-green \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --namespace=production

          # Wait for green to be ready
          kubectl rollout status deployment/myapp-green -n production --timeout=5m

          # Switch traffic to green
          kubectl patch service myapp -n production \
            -p '{"spec":{"selector":{"version":"green"}}}'
```

**Caching Strategy**

```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

- name: Cache Docker layers
  uses: actions/cache@v3
  with:
    path: /tmp/.buildx-cache
    key: ${{ runner.os }}-buildx-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-buildx-
```

### GitLab CI Configuration

**Complete Pipeline**

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - build
  - test
  - scan
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

cache:
  paths:
    - node_modules/
    - .npm/

validate:
  stage: validate
  image: node:18-alpine
  script:
    - npm ci
    - npm run lint
    - npm run typecheck
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

unit-tests:
  stage: test
  image: node:18-alpine
  script:
    - npm ci
    - npm test -- --coverage
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

security-scan:
  stage: scan
  image: aquasec/trivy:latest
  script:
    - trivy fs --severity CRITICAL,HIGH --exit-code 1 .
    - trivy config --severity CRITICAL,HIGH --exit-code 1 .

build-image:
  stage: build
  image: docker:24-dind
  services:
    - docker:24-dind
  before_script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin $CI_REGISTRY
  script:
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  only:
    - main
    - develop

deploy-staging:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/myapp myapp=$IMAGE_TAG --namespace=staging
    - kubectl rollout status deployment/myapp -n staging --timeout=5m
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy-production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/myapp myapp=$IMAGE_TAG --namespace=production
    - kubectl rollout status deployment/myapp -n production --timeout=5m
  environment:
    name: production
    url: https://example.com
  when: manual
  only:
    - main
```

### Testing Gates

**Comprehensive Test Strategy**

```yaml
# GitHub Actions example
jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test -- --coverage --maxWorkers=2

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
          fail_ci_if_error: true

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:e2e

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
```

### Security Scanning

**Multi-Layer Security**

```yaml
security:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    # Dependency scanning
    - name: Run npm audit
      run: npm audit --audit-level=moderate

    # SAST (Static Application Security Testing)
    - name: Initialize CodeQL
      uses: github/codeql-action/init@v2
      with:
        languages: javascript

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v2

    # Container scanning
    - name: Build image
      run: docker build -t myapp:test .

    - name: Run Trivy scan
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'myapp:test'
        format: 'sarif'
        output: 'trivy-results.sarif'
        severity: 'CRITICAL,HIGH'

    - name: Upload Trivy results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

    # Secrets scanning
    - name: Gitleaks scan
      uses: gitleaks/gitleaks-action@v2
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Artifact Management

**Docker Image Tagging Strategy**

```bash
# Tag with semantic version
docker tag myapp:latest registry.example.com/myapp:v1.2.3

# Tag with git SHA (for traceability)
docker tag myapp:latest registry.example.com/myapp:${GIT_SHA:0:7}

# Tag with environment
docker tag myapp:latest registry.example.com/myapp:production

# Tag with date (for retention policies)
docker tag myapp:latest registry.example.com/myapp:$(date +%Y%m%d)
```

**Artifact Retention Policy** (see [templates/.github/workflows/cleanup.yml](templates/.github/workflows/cleanup.yml)):

```yaml
name: Cleanup Old Artifacts

on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday at 2 AM

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Delete old artifacts
        uses: actions/github-script@v6
        with:
          script: |
            const artifacts = await github.rest.actions.listArtifactsForRepo({
              owner: context.repo.owner,
              repo: context.repo.repo,
            });

            const cutoffDate = new Date();
            cutoffDate.setDate(cutoffDate.getDate() - 30);  // 30 days retention

            for (const artifact of artifacts.data.artifacts) {
              if (new Date(artifact.created_at) < cutoffDate) {
                await github.rest.actions.deleteArtifact({
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  artifact_id: artifact.id,
                });
              }
            }
```

### Deployment Strategies

**Blue-Green Deployment** (see [scripts/deploy.sh](scripts/deploy.sh)):

```bash
#!/bin/bash
set -e

ENVIRONMENT=${1:-staging}
VERSION=${2:-latest}
NAMESPACE="myapp-${ENVIRONMENT}"

echo "Deploying version $VERSION to $ENVIRONMENT"

# Deploy to inactive environment (green)
kubectl set image deployment/myapp-green \
  myapp=registry.example.com/myapp:$VERSION \
  --namespace=$NAMESPACE

# Wait for green to be ready
kubectl rollout status deployment/myapp-green -n $NAMESPACE --timeout=5m

# Run smoke tests against green
echo "Running smoke tests..."
GREEN_URL=$(kubectl get service myapp-green -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
curl -f "http://${GREEN_URL}/health" || exit 1

# Switch traffic to green
echo "Switching traffic to green..."
kubectl patch service myapp -n $NAMESPACE \
  -p '{"spec":{"selector":{"version":"green"}}}'

echo "Deployment successful! Old blue environment remains for rollback."
```

**Canary Deployment**

```yaml
# Kubernetes Deployment with Istio
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp.example.com
  http:
  - match:
    - headers:
        x-canary:
          exact: "true"
    route:
    - destination:
        host: myapp
        subset: canary
  - route:
    - destination:
        host: myapp
        subset: stable
      weight: 90
    - destination:
        host: myapp
        subset: canary
      weight: 10  # 10% traffic to canary
```

**Rolling Update** (default Kubernetes strategy):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2          # Max 2 new pods above desired count
      maxUnavailable: 1    # Max 1 pod can be unavailable
  template:
    spec:
      containers:
      - name: myapp
        image: registry.example.com/myapp:v1.2.3
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Environment Management

**Environment Configuration**

```yaml
# GitHub Environments with protection rules
environments:
  staging:
    url: https://staging.example.com
    protection_rules:
      - type: required_reviewers
        reviewers: []
      - type: wait_timer
        wait_timer: 0

  production:
    url: https://example.com
    protection_rules:
      - type: required_reviewers
        reviewers:
          - devops-team
      - type: wait_timer
        wait_timer: 300  # 5 minute wait
```

**Secrets Management**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Fetch secrets from Parameter Store
        run: |
          export DB_PASSWORD=$(aws ssm get-parameter \
            --name /myapp/production/db-password \
            --with-decryption \
            --query 'Parameter.Value' \
            --output text)

      - name: Deploy with secrets
        run: |
          kubectl create secret generic myapp-secrets \
            --from-literal=db-password=$DB_PASSWORD \
            --namespace=production \
            --dry-run=client -o yaml | kubectl apply -f -
```

### Rollback Procedures

**Automated Rollback on Failure**

```yaml
deploy:
  runs-on: ubuntu-latest
  steps:
    - name: Deploy new version
      id: deploy
      run: |
        kubectl set image deployment/myapp myapp=$IMAGE_TAG --namespace=production
        kubectl rollout status deployment/myapp -n production --timeout=5m

    - name: Health check
      id: health_check
      run: |
        sleep 30  # Wait for metrics
        ERROR_RATE=$(curl -s https://example.com/metrics | jq '.error_rate')
        if (( $(echo "$ERROR_RATE > 0.05" | bc -l) )); then
          echo "Error rate ${ERROR_RATE} exceeds 5% threshold"
          exit 1
        fi

    - name: Rollback on failure
      if: failure()
      run: |
        echo "Deployment failed, rolling back..."
        kubectl rollout undo deployment/myapp -n production
        kubectl rollout status deployment/myapp -n production --timeout=5m

    - name: Notify on rollback
      if: failure()
      uses: slackapi/slack-github-action@v1
      with:
        payload: |
          {
            "text": "🚨 Production deployment rolled back!",
            "blocks": [
              {
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": "*Rollback Alert*\nDeployment to production failed and was automatically rolled back.\n\n*Run:* ${{ github.run_id }}\n*Commit:* ${{ github.sha }}"
                }
              }
            ]
          }
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Pipeline Monitoring

**Metrics and Alerting**

```yaml
- name: Track deployment metrics
  run: |
    curl -X POST https://metrics.example.com/api/v1/events \
      -H "Content-Type: application/json" \
      -d '{
        "event": "deployment",
        "environment": "production",
        "version": "${{ github.sha }}",
        "status": "success",
        "duration": "${{ steps.deploy.outputs.duration }}",
        "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
      }'

- name: Update status page
  if: success()
  run: |
    curl -X POST https://status.example.com/api/v2/incidents \
      -H "Authorization: Bearer ${{ secrets.STATUS_PAGE_TOKEN }}" \
      -d '{
        "incident": {
          "name": "Deployment Complete",
          "status": "resolved",
          "body": "Production deployment completed successfully."
        }
      }'
```

---

## Level 3: Mastery (Resources)

### Bundled Resources

1. **[templates/.github/workflows/ci.yml](templates/.github/workflows/ci.yml)** - Complete CI workflow with testing gates
2. **[templates/.github/workflows/cd.yml](templates/.github/workflows/cd.yml)** - CD workflow with deployment strategies
3. **[templates/.gitlab-ci.yml](templates/.gitlab-ci.yml)** - GitLab CI/CD configuration
4. **[resources/deployment-strategies.md](resources/deployment-strategies.md)** - In-depth deployment patterns
5. **[scripts/deploy.sh](scripts/deploy.sh)** - Blue-green deployment automation

### Advanced Topics

#### Matrix Builds

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    node-version: [16, 18, 20]
    exclude:
      - os: macos-latest
        node-version: 16
```

#### Composite Actions

```yaml
# .github/actions/setup-env/action.yml
name: 'Setup Environment'
description: 'Setup Node.js and dependencies'
runs:
  using: "composite"
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
    - run: npm ci
      shell: bash
```

#### Reusable Workflows

```yaml
# .github/workflows/deploy-reusable.yml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      deploy-token:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh ${{ inputs.environment }}
```

### Related Skills

- **[kubernetes](../../cloud-native/kubernetes/SKILL.md)** - Container orchestration for deployments
- **[docker-standards](../docker/SKILL.md)** - Container image best practices
- **[security-scanning](../../security/scanning/SKILL.md)** - Security vulnerability detection
- **[monitoring](../monitoring/SKILL.md)** - Production observability

### Security Best Practices

1. **Secrets Management**: Use GitHub Secrets, AWS Secrets Manager, or HashiCorp Vault
2. **OIDC Authentication**: Use workload identity instead of long-lived credentials
3. **Least Privilege**: Pipeline permissions should be minimal and scoped
4. **Audit Logs**: Track all pipeline executions and deployments
5. **Signed Commits**: Require GPG-signed commits for production deployments

### Performance Optimization

- **Parallel Jobs**: Run independent jobs concurrently
- **Caching**: Cache dependencies, build artifacts, Docker layers
- **Conditional Execution**: Skip unnecessary jobs with `if` conditions
- **Self-Hosted Runners**: Use for compute-intensive builds
- **Incremental Builds**: Only build changed components

### Compliance & Governance

- **Change Approval**: Require manual approval for production deployments
- **Deployment Windows**: Restrict deployments to business hours
- **Audit Trail**: Log all deployments with who/what/when/where
- **Rollback SLA**: Define acceptable rollback time (e.g., <5 minutes)
- **Post-Deployment Verification**: Automated smoke tests after deployment

---

## When to Use This Skill

- ✅ Setting up CI/CD pipelines for new projects
- ✅ Automating build, test, and deployment workflows
- ✅ Implementing security scanning and compliance gates
- ✅ Configuring multi-environment deployments (dev/staging/prod)
- ✅ Establishing artifact management and versioning strategies
- ✅ Creating rollback procedures and disaster recovery plans
- ✅ Optimizing pipeline performance and reducing build times
- ✅ Implementing GitOps workflows with Kubernetes

## Examples

### Basic Usage

```python
// TODO: Add basic example for ci-cd
// This example demonstrates core functionality
```

### Advanced Usage

```python
// TODO: Add advanced example for ci-cd
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how ci-cd
// works with other systems and services
```

See `examples/ci-cd/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: GitHub Actions, GitLab CI, Jenkins, CircleCI
- **Prerequisites**: Basic understanding of devops concepts

### Downstream Consumers

- **Applications**: Production systems requiring ci-cd functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- [Infrastructure As Code](../../infrastructure-as-code/SKILL.md)
- [Monitoring Observability](../../monitoring-observability/SKILL.md)

### Common Integration Patterns

1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points

## Common Pitfalls

### Pitfall 1: Insufficient Testing

**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:

- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration

**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:

- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices

**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:

- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**

- Follow established patterns and conventions for ci-cd
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

---

**Last Updated:** 2025-01-17
**Version:** 1.0.0
**Quality Score:** 95/100
