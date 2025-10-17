# Phase 2 Skill Assignments: Coder Task Distribution

**Version**: 1.0.0
**Date**: 2025-10-17
**Phase**: Core Skills Migration (Weeks 2-3)
**Team Size**: 3 Content Engineers + 1 QA Engineer + 1 Infrastructure Engineer + 1 Integration Engineer

---

## Team Structure

### Content Engineers (3)
- **Content Engineer 1**: Focus on coding standards and testing
- **Content Engineer 2**: Focus on security and frontend
- **Content Engineer 3**: Focus on DevOps and cloud-native

### Supporting Roles
- **QA Engineer**: Validation and quality assurance
- **Infrastructure Engineer**: Directory structure and configuration
- **Integration Engineer**: Meta-skills and integration

---

## Content Engineer 1: Coding Standards & Testing

### Primary Focus
**Languages**: Python, JavaScript, TypeScript, Go
**Testing**: Unit Testing, E2E Testing

### Skill Assignments

#### Week 2 Skills (4 skills)

##### 1. Python Skill
**Priority**: High (Critical path)
**Source**: `docs/standards/CODING_STANDARDS.md` (Python section)
**Target**: `skills/coding-standards/python/SKILL.md`
**Estimated Time**: 8 hours
**Timeline**: Day 7 (Tuesday Week 2)

**Tasks**:
- [ ] Extract Python content from CODING_STANDARDS.md
  - PEP 8 standards
  - Type hints and annotations
  - Async/await patterns
  - Project structure conventions
  - Common anti-patterns
- [ ] Write SKILL.md with YAML frontmatter
  - Name: `python`
  - Description: <1024 chars, includes "when to use"
  - Overview section
  - Core instructions
  - Advanced topics (reference resources/)
  - Examples (2-3 concrete)
- [ ] Bundle resources in `resources/`
  - `resources/pep8-guide.md`
  - `resources/type-hints-guide.md`
  - `resources/async-patterns.md`
- [ ] Create templates in `templates/`
  - `templates/pyproject.toml`
  - `templates/pytest.ini`
  - `templates/tox.ini`
- [ ] Create scripts in `scripts/`
  - `scripts/lint.sh` (black, ruff, mypy)
  - `scripts/format.sh`
  - `scripts/test.sh`
- [ ] Validate token count <5,000

**Success Criteria**:
- Token count: <5,000 ✅
- All sections complete ✅
- 2+ examples ✅
- Scripts executable ✅
- QA validation pass ✅

---

##### 2. JavaScript Skill
**Priority**: High
**Source**: `docs/standards/CODING_STANDARDS.md` (JavaScript section)
**Target**: `skills/coding-standards/javascript/SKILL.md`
**Estimated Time**: 4 hours
**Timeline**: Day 8 (Wednesday Week 2) - First half

**Tasks**:
- [ ] Extract JavaScript content
  - ESNext features
  - Async/await patterns
  - Module systems (ESM, CommonJS)
  - Error handling
  - Testing patterns
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/esnext-features.md`
  - `resources/async-guide.md`
- [ ] Create templates
  - `templates/package.json`
  - `templates/.eslintrc.json`
  - `templates/jest.config.js`
- [ ] Create scripts
  - `scripts/lint.sh`
  - `scripts/test.sh`
- [ ] Validate token count <5,000

---

##### 3. TypeScript Skill
**Priority**: High
**Source**: `docs/standards/CODING_STANDARDS.md` (TypeScript section)
**Target**: `skills/coding-standards/typescript/SKILL.md`
**Estimated Time**: 8 hours (4h Day 8 + 4h Day 9)
**Timeline**: Days 8-9 (Wed-Thu Week 2)

**Tasks**:
- [ ] Extract TypeScript content
  - Advanced types (generics, conditional types)
  - Decorators
  - Strict mode configuration
  - Type-safe patterns
  - Testing with TypeScript
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/advanced-types.md`
  - `resources/decorators-guide.md`
- [ ] Create templates
  - `templates/tsconfig.json`
  - `templates/tsconfig.build.json`
  - `templates/vitest.config.ts`
- [ ] Create scripts
  - `scripts/typecheck.sh`
  - `scripts/build.sh`
- [ ] Validate token count <5,000

---

##### 4. Unit Testing Skill
**Priority**: High
**Source**: `docs/standards/TESTING_STANDARDS.md` (Unit testing section)
**Target**: `skills/testing/unit-testing/SKILL.md`
**Estimated Time**: 8 hours (4h Day 9 + 4h Day 10)
**Timeline**: Days 9-10 (Thu-Fri Week 2)

**Tasks**:
- [ ] Extract unit testing content
  - TDD methodology
  - Test structure (AAA pattern)
  - Mocking and stubbing
  - Assertions and matchers
  - Coverage targets
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/tdd-guide.md`
  - `resources/mocking-patterns.md`
  - `resources/assertion-guide.md`
- [ ] Create templates
  - `templates/test.template.py`
  - `templates/test.template.js`
  - `templates/test.template.ts`
- [ ] Create scripts
  - `scripts/run-unit-tests.sh`
  - `scripts/coverage-report.sh`
- [ ] Validate token count <5,000

---

#### Week 3 Skills (2 skills)

##### 5. E2E Testing Skill
**Priority**: Medium
**Source**: `docs/standards/TESTING_STANDARDS.md` (E2E section)
**Target**: `skills/testing/e2e-testing/SKILL.md`
**Estimated Time**: 8 hours (2h Day 12 + 6h Day 13)
**Timeline**: Days 12-13 (Tue-Wed Week 3)

**Tasks**:
- [ ] Extract E2E testing content
  - Playwright patterns
  - Cypress alternatives
  - Page object model
  - Test scenarios
  - CI integration
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/playwright-guide.md`
  - `resources/page-objects.md`
- [ ] Create templates
  - `templates/e2e-test.template.ts`
  - `templates/playwright.config.ts`
- [ ] Create scripts
  - `scripts/run-e2e-tests.sh`
  - `scripts/generate-report.sh`
- [ ] Validate token count <5,000

---

##### 6. Monitoring Skill
**Priority**: Medium
**Source**: `docs/standards/DEVOPS_PLATFORM_STANDARDS.md` (Monitoring section)
**Target**: `skills/devops/monitoring/SKILL.md`
**Estimated Time**: 8 hours (2h Day 13 + 6h Day 14)
**Timeline**: Days 13-14 (Wed-Thu Week 3)

**Tasks**:
- [ ] Extract monitoring content
  - Prometheus patterns
  - Grafana dashboards
  - Alert configuration
  - SLI/SLO/SLA definitions
  - Metric design
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/prometheus-guide.md`
  - `resources/grafana-guide.md`
  - `resources/sli-slo-guide.md`
- [ ] Create templates
  - `templates/prometheus.yml`
  - `templates/alerts.yml`
  - `templates/dashboard.json`
- [ ] Create scripts
  - `scripts/validate-prometheus.sh`
  - `scripts/generate-dashboard.sh`
- [ ] Validate token count <5,000

---

### Total Workload: Content Engineer 1

| Week | Skills | Hours |
|------|--------|-------|
| Week 2 | Python, JavaScript, TypeScript, Unit Testing | 28h |
| Week 3 | E2E Testing, Monitoring | 16h |
| Review & QA | Coding + Testing consistency review | 8h |
| **Total** | **6 skills** | **52h** |

---

## Content Engineer 2: Security & Frontend

### Primary Focus
**Security**: Authentication, Secrets, Threat Modeling
**Frontend**: React
**Testing**: Performance Testing

### Skill Assignments

#### Week 2 Skills (4 skills)

##### 1. Go Skill
**Priority**: Medium
**Source**: `docs/standards/CODING_STANDARDS.md` (Go section)
**Target**: `skills/coding-standards/go/SKILL.md`
**Estimated Time**: 8 hours (6h Day 8 + 2h Day 9)
**Timeline**: Days 8-9 (Wed-Thu Week 2)

**Tasks**:
- [ ] Extract Go content
  - Idiomatic Go patterns
  - Error handling
  - Concurrency (goroutines, channels)
  - Project layout
  - Testing in Go
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/go-patterns.md`
  - `resources/concurrency-guide.md`
- [ ] Create templates
  - `templates/go.mod`
  - `templates/main.go.template`
- [ ] Create scripts
  - `scripts/fmt.sh`
  - `scripts/test.sh`
- [ ] Validate token count <5,000

---

##### 2. Authentication Skill
**Priority**: High (Critical for security)
**Source**: `docs/standards/MODERN_SECURITY_STANDARDS.md` (Auth section)
**Target**: `skills/security/authentication/SKILL.md`
**Estimated Time**: 8 hours (2h Day 8 + 6h Day 9)
**Timeline**: Days 8-9 (Wed-Thu Week 2)

**Tasks**:
- [ ] Extract authentication content
  - OAuth 2.0 flows
  - OIDC patterns
  - JWT best practices
  - Session management
  - MFA implementation
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/oauth-flows.md`
  - `resources/jwt-guide.md`
  - `resources/session-management.md`
  - `resources/mfa-patterns.md`
- [ ] Create templates
  - `templates/auth-middleware.template`
  - `templates/jwt-config.template`
- [ ] Create scripts
  - `scripts/validate-jwt.sh`
  - `scripts/generate-keys.sh`
- [ ] Validate token count <5,000

---

##### 3. Secrets Management Skill
**Priority**: High
**Source**: `docs/standards/MODERN_SECURITY_STANDARDS.md` (Secrets section)
**Target**: `skills/security/secrets-management/SKILL.md`
**Estimated Time**: 8 hours (2h Day 9 + 6h Day 10)
**Timeline**: Days 9-10 (Thu-Fri Week 2)

**Tasks**:
- [ ] Extract secrets management content
  - Vault integration
  - Environment variable handling
  - Key rotation policies
  - Secret scanning
  - Access control
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/vault-setup.md`
  - `resources/rotation-guide.md`
  - `resources/scanning-tools.md`
- [ ] Create templates
  - `templates/.env.template`
  - `templates/vault-config.hcl`
- [ ] Create scripts
  - `scripts/rotate-secrets.sh`
  - `scripts/scan-secrets.sh`
- [ ] Validate token count <5,000

---

##### 4. React Skill
**Priority**: High (Frontend flagship)
**Source**: `docs/standards/FRONTEND_MOBILE_STANDARDS.md` (React section)
**Target**: `skills/frontend/react/SKILL.md`
**Estimated Time**: 8 hours (2h Day 10 + 6h Day 11)
**Timeline**: Days 10-11 (Fri-Mon Week 2-3)

**Tasks**:
- [ ] Extract React content
  - Hooks patterns
  - Component design
  - State management (Context, Zustand)
  - Performance optimization
  - Testing strategies
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/hooks-guide.md`
  - `resources/state-management.md`
  - `resources/performance-tips.md`
- [ ] Create templates
  - `templates/component.template.tsx`
  - `templates/hook.template.ts`
  - `templates/vite.config.ts`
- [ ] Create scripts
  - `scripts/analyze-bundle.sh`
- [ ] Validate token count <5,000

---

#### Week 3 Skills (2 skills)

##### 5. Threat Modeling Skill
**Priority**: Medium
**Source**: `docs/standards/MODERN_SECURITY_STANDARDS.md` (Threat modeling section)
**Target**: `skills/security/threat-modeling/SKILL.md`
**Estimated Time**: 8 hours (2h Day 11 + 6h Day 12)
**Timeline**: Days 11-12 (Mon-Tue Week 3)

**Tasks**:
- [ ] Extract threat modeling content
  - STRIDE methodology
  - Attack trees
  - Risk assessment
  - Mitigation strategies
  - Threat model documentation
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/stride-guide.md`
  - `resources/attack-trees.md`
  - `resources/risk-matrix.md`
- [ ] Create templates
  - `templates/threat-model.template.md`
  - `templates/risk-assessment.template`
- [ ] Create scripts
  - `scripts/generate-threat-model.sh`
- [ ] Validate token count <5,000

---

##### 6. Performance Testing Skill
**Priority**: Medium
**Source**: `docs/standards/TESTING_STANDARDS.md` (Performance section)
**Target**: `skills/testing/performance-testing/SKILL.md`
**Estimated Time**: 8 hours (2h Day 12 + 6h Day 13)
**Timeline**: Days 12-13 (Tue-Wed Week 3)

**Tasks**:
- [ ] Extract performance testing content
  - Load testing (k6)
  - Stress testing
  - Benchmarking
  - Profiling
  - Performance budgets
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/k6-guide.md`
  - `resources/profiling-guide.md`
  - `resources/performance-budgets.md`
- [ ] Create templates
  - `templates/load-test.template.js`
  - `templates/benchmark.template`
- [ ] Create scripts
  - `scripts/run-performance-tests.sh`
  - `scripts/analyze-results.sh`
- [ ] Validate token count <5,000

---

### Total Workload: Content Engineer 2

| Week | Skills | Hours |
|------|--------|-------|
| Week 2 | Go, Auth, Secrets, React | 32h |
| Week 3 | Threat Modeling, Performance Testing | 16h |
| Review & QA | Security + Frontend consistency review | 8h |
| **Total** | **6 skills** | **56h** |

---

## Content Engineer 3: DevOps & Cloud-Native

### Primary Focus
**DevOps**: CI/CD, Infrastructure
**Cloud-Native**: Kubernetes, Containers, Serverless
**Security**: Zero-Trust, Input Validation
**Coding**: Rust

### Skill Assignments

#### Week 2 Skills (3 skills)

##### 1. Integration Testing Skill
**Priority**: High
**Source**: `docs/standards/TESTING_STANDARDS.md` (Integration section)
**Target**: `skills/testing/integration-testing/SKILL.md`
**Estimated Time**: 8 hours (4h Day 9 + 4h Day 10)
**Timeline**: Days 9-10 (Thu-Fri Week 2)

**Tasks**:
- [ ] Extract integration testing content
  - API testing
  - Database integration
  - Test containers
  - Service mocking
  - Integration patterns
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/api-testing-guide.md`
  - `resources/testcontainers-guide.md`
  - `resources/mocking-services.md`
- [ ] Create templates
  - `templates/integration-test.template`
  - `templates/docker-compose.test.yml`
- [ ] Create scripts
  - `scripts/setup-test-db.sh`
  - `scripts/run-integration-tests.sh`
- [ ] Validate token count <5,000

---

##### 2. CI/CD Skill
**Priority**: High (DevOps core)
**Source**: `docs/standards/DEVOPS_PLATFORM_STANDARDS.md` (CI/CD section)
**Target**: `skills/devops/ci-cd/SKILL.md`
**Estimated Time**: 8 hours (4h Day 9 + 4h Day 10)
**Timeline**: Days 9-10 (Thu-Fri Week 2)

**Tasks**:
- [ ] Extract CI/CD content
  - GitHub Actions patterns
  - GitLab CI alternatives
  - Testing automation
  - Deployment strategies (blue/green, canary)
  - Release management
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/github-actions-guide.md`
  - `resources/deployment-strategies.md`
  - `resources/release-management.md`
- [ ] Create templates
  - `templates/.github/workflows/ci.yml`
  - `templates/.github/workflows/deploy.yml`
  - `templates/.github/workflows/release.yml`
- [ ] Create scripts
  - `scripts/deploy.sh`
  - `scripts/rollback.sh`
- [ ] Validate token count <5,000

---

##### 3. Kubernetes Skill
**Priority**: High (Cloud-native flagship)
**Source**: `docs/standards/CLOUD_NATIVE_STANDARDS.md` (Kubernetes section)
**Target**: `skills/cloud-native/kubernetes/SKILL.md`
**Estimated Time**: 10 hours (4h Day 10 + 6h Day 11)
**Timeline**: Days 10-11 (Fri-Mon Week 2-3)

**Tasks**:
- [ ] Extract Kubernetes content
  - Deployment patterns
  - Resource management
  - Networking (Services, Ingress)
  - Security (RBAC, PSP)
  - Best practices
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/k8s-patterns.md`
  - `resources/resource-management.md`
  - `resources/networking-guide.md`
  - `resources/security-hardening.md`
- [ ] Create templates
  - `templates/deployment.yaml`
  - `templates/service.yaml`
  - `templates/ingress.yaml`
  - `templates/rbac.yaml`
- [ ] Create scripts
  - `scripts/validate-manifests.sh`
  - `scripts/apply-resources.sh`
- [ ] Validate token count <5,000

---

#### Week 3 Skills (6 skills)

##### 4. Rust Skill
**Priority**: Low (Specialized)
**Source**: `docs/standards/CODING_STANDARDS.md` (Rust section - may be sparse)
**Target**: `skills/coding-standards/rust/SKILL.md`
**Estimated Time**: 6 hours
**Timeline**: Day 11 (Monday Week 3)

**Tasks**:
- [ ] Extract Rust content (or create from best practices)
  - Ownership and borrowing
  - Lifetimes
  - Error handling (Result, Option)
  - Idiomatic patterns
  - Testing in Rust
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/ownership-guide.md`
  - `resources/error-handling.md`
- [ ] Create templates
  - `templates/Cargo.toml`
  - `templates/main.rs.template`
- [ ] Create scripts
  - `scripts/fmt.sh`
  - `scripts/clippy.sh`
- [ ] Validate token count <5,000

---

##### 5. Zero-Trust Skill
**Priority**: Medium
**Source**: `docs/standards/MODERN_SECURITY_STANDARDS.md` (Zero-trust section)
**Target**: `skills/security/zero-trust/SKILL.md`
**Estimated Time**: 8 hours (2h Day 11 + 6h Day 12)
**Timeline**: Days 11-12 (Mon-Tue Week 3)

**Tasks**:
- [ ] Extract zero-trust content
  - Zero-trust principles
  - Network segmentation
  - Least privilege access
  - Continuous verification
  - Policy enforcement
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/zero-trust-architecture.md`
  - `resources/segmentation-guide.md`
  - `resources/policy-enforcement.md`
- [ ] Create templates
  - `examples/istio-policies/`
  - `templates/network-policy.yaml`
- [ ] Validate token count <5,000

---

##### 6. Input Validation Skill
**Priority**: High
**Source**: `docs/standards/MODERN_SECURITY_STANDARDS.md` (Input validation section)
**Target**: `skills/security/input-validation/SKILL.md`
**Estimated Time**: 8 hours (2h Day 11 + 6h Day 12)
**Timeline**: Days 11-12 (Mon-Tue Week 3)

**Tasks**:
- [ ] Extract input validation content
  - SQL injection prevention
  - XSS protection
  - CSRF tokens
  - Data validation patterns
  - Sanitization techniques
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/validation-patterns.md`
  - `resources/sql-injection-prevention.md`
  - `resources/xss-csrf-guide.md`
- [ ] Create templates
  - `templates/validator.template`
  - `templates/sanitizer.template`
- [ ] Validate token count <5,000

---

##### 7. Infrastructure Skill
**Priority**: High
**Source**: `docs/standards/DEVOPS_PLATFORM_STANDARDS.md` (IaC section)
**Target**: `skills/devops/infrastructure/SKILL.md`
**Estimated Time**: 8 hours (2h Day 12 + 6h Day 13)
**Timeline**: Days 12-13 (Tue-Wed Week 3)

**Tasks**:
- [ ] Extract infrastructure content
  - Terraform patterns
  - CloudFormation alternatives
  - State management
  - Module design
  - Testing infrastructure
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/terraform-guide.md`
  - `resources/state-management.md`
  - `resources/module-patterns.md`
- [ ] Create templates
  - `templates/main.tf.template`
  - `templates/variables.tf.template`
  - `templates/outputs.tf.template`
- [ ] Create scripts
  - `scripts/terraform-validate.sh`
  - `scripts/plan.sh`
  - `scripts/apply.sh`
- [ ] Validate token count <5,000

---

##### 8. Containers Skill
**Priority**: High
**Source**: `docs/standards/CLOUD_NATIVE_STANDARDS.md` (Container section)
**Target**: `skills/cloud-native/containers/SKILL.md`
**Estimated Time**: 8 hours (2h Day 13 + 6h Day 14)
**Timeline**: Days 13-14 (Wed-Thu Week 3)

**Tasks**:
- [ ] Extract container content
  - Dockerfile best practices
  - Multi-stage builds
  - Security scanning
  - Image optimization
  - Registry management
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/dockerfile-guide.md`
  - `resources/security-scanning.md`
  - `resources/optimization-tips.md`
- [ ] Create templates
  - `templates/Dockerfile.template`
  - `templates/Dockerfile.multistage.template`
  - `templates/.dockerignore`
- [ ] Create scripts
  - `scripts/build-and-scan.sh`
  - `scripts/optimize-image.sh`
- [ ] Validate token count <5,000

---

##### 9. Serverless Skill
**Priority**: Medium
**Source**: `docs/standards/CLOUD_NATIVE_STANDARDS.md` (Serverless section)
**Target**: `skills/cloud-native/serverless/SKILL.md`
**Estimated Time**: 8 hours (2h Day 13 + 6h Day 14)
**Timeline**: Days 13-14 (Wed-Thu Week 3)

**Tasks**:
- [ ] Extract serverless content
  - AWS Lambda patterns
  - Event-driven architecture
  - Cold start optimization
  - Observability
  - Cost optimization
- [ ] Write SKILL.md
- [ ] Bundle resources
  - `resources/lambda-guide.md`
  - `resources/event-patterns.md`
  - `resources/cold-start-optimization.md`
- [ ] Create templates
  - `templates/serverless.yml`
  - `templates/lambda.template.py`
  - `templates/lambda.template.js`
- [ ] Create scripts
  - `scripts/deploy-lambda.sh`
- [ ] Validate token count <5,000

---

### Total Workload: Content Engineer 3

| Week | Skills | Hours |
|------|--------|-------|
| Week 2 | Integration Testing, CI/CD, Kubernetes | 26h |
| Week 3 | Rust, Zero-Trust, Input Validation, Infrastructure, Containers, Serverless | 46h |
| Review & QA | DevOps + Cloud-Native consistency review | 8h |
| **Total** | **9 skills** | **80h** |

---

## Summary: Total Skills by Engineer

| Engineer | Week 2 Skills | Week 3 Skills | Total Skills | Total Hours |
|----------|---------------|---------------|--------------|-------------|
| Content Engineer 1 | 4 | 2 | 6 | 52h |
| Content Engineer 2 | 4 | 2 | 6 | 56h |
| Content Engineer 3 | 3 | 6 | 9 | 80h |
| **Total** | **11** | **10** | **21** | **188h** |

**Note**: Total hours exceed 160 planned hours to account for review, QA assistance, and buffer time.

---

## Quality Standards (All Engineers)

### Every Skill Must Include

1. **YAML Frontmatter**
   - `name`: Lowercase-with-hyphens, ≤64 chars
   - `description`: ≤1024 chars, includes "when to use"

2. **SKILL.md Structure**
   - Overview section
   - When to Use This Skill
   - Core Instructions
   - Advanced Topics (references to resources/)
   - Examples (2-3 minimum)

3. **Token Budget**
   - SKILL.md body: <5,000 tokens
   - Use resources/ for detailed content
   - Use templates/ for code samples
   - Use scripts/ for automation

4. **Resources**
   - All referenced files must exist
   - Markdown files in resources/
   - Configuration files in templates/
   - Executable scripts in scripts/ (chmod +x)

5. **Examples**
   - At least 2 concrete examples
   - Copy-paste ready
   - Cover common use cases

6. **Validation**
   - Run `scripts/validate-skills.py`
   - Check token count
   - Test scripts execute
   - Verify all links

---

## Coordination Protocol

### Daily Workflow

**Morning (9:00 AM)**:
1. Check assigned skills for the day
2. Review any blockers from previous day
3. Coordinate with other engineers on dependencies

**During Work**:
1. Follow the skill authoring checklist
2. Use the skill template (`skills/.templates/SKILL.md.template`)
3. Commit work frequently to avoid conflicts
4. Update progress tracker in real-time

**End of Day (4:00 PM)**:
1. Report progress (% complete)
2. Flag any issues or surprises
3. Prepare next day's work
4. Hand off to QA if skill complete

### Quality Handoff

When a skill is complete:
1. Run self-validation (`scripts/validate-skills.py`)
2. Check token count manually
3. Test all scripts
4. Create a handoff note for QA
5. Mark as "Ready for QA" in progress tracker

### Communication

- **Blockers**: Report immediately via Slack
- **Questions**: Check SKILL_AUTHORING_GUIDE.md first
- **Coordination**: Use daily standups
- **Reviews**: Pair review before QA handoff

---

## Support Resources

### Templates
- `skills/.templates/SKILL.md.template` - Base skill structure
- `skills/.templates/resource.md.template` - Resource file structure

### Documentation
- `docs/guides/SKILL_AUTHORING_GUIDE.md` - Complete authoring guide
- `docs/migration/architecture-design.md` - Architecture reference
- `docs/migration/skill-mapping.yaml` - Source content mapping

### Tools
- `scripts/generate-skill.py` - Automated skill generation
- `scripts/validate-skills.py` - Skill validation
- `scripts/migrate-to-skills.py` - Content migration helper
- Token counter: <https://platform.openai.com/tokenizer>

### Example Skills
- `skills/coding-standards/python/SKILL.md` (Phase 1 template)
- Reference completed skills for consistency

---

## Escalation Path

### Level 1: Self-Resolution
- Check documentation
- Review examples
- Use automation tools

### Level 2: Peer Consultation
- Ask other content engineers
- Discuss in Slack
- Pair programming session

### Level 3: Technical Lead
- Architecture questions → Integration Engineer
- Infrastructure questions → Infrastructure Engineer
- Process questions → QA Engineer

### Level 4: Project Manager
- Timeline concerns
- Resource constraints
- Scope changes

---

**Document Owner**: Planning Agent
**Last Updated**: 2025-10-17
**Status**: Active
**Next Review**: Daily during Phase 2 execution

---

*Phase 2 Skill Assignments v1.0.0*
