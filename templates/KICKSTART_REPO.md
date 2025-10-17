# Repository Kickstart Template

**Copy this file to your new repository and follow the instructions. This template helps you automatically discover your project type, load appropriate standards, and generate a comprehensive project plan.**

---

## 🤖 For AI Assistants (LLM Instructions)

When processing this template, you should:

1. **Auto-Detect Project Type** by analyzing:
   - Repository structure and files
   - Dependencies (package.json, requirements.txt, go.mod, etc.)
   - Framework indicators (React components, Django settings, FastAPI routers)
   - Infrastructure files (Dockerfile, terraform/, kubernetes/)
   - Database configurations

2. **Load Standards Automatically** using the `@load` directive:
   - Map detected tech stack to product type from `config/product-matrix.yaml`
   - Resolve language-specific and framework-specific standards
   - Auto-include NIST-IG:base when security standards are present
   - Expand wildcards (e.g., `SEC:*` → all security standards)

3. **Generate Comprehensive Plan** including:
   - Project structure recommendations
   - Development workflow setup
   - Testing strategy aligned with standards
   - Security implementation checklist
   - CI/CD pipeline configuration
   - Quality gates and validation

4. **Provide Actionable Outputs**:
   - Exact commands to run
   - Configuration files to create
   - Code scaffolding following standards
   - Testing setup with examples
   - Documentation structure

---

## 📋 Project Information

### Basic Details

**Project Name:** `[Enter project name]`

**Project Description:** `[Enter 1-2 sentence description]`

**Primary Goal:** `[What problem does this solve?]`

### Technical Context (Optional - AI will auto-detect if blank)

**Languages:** `[e.g., Python, TypeScript, Go - leave blank for auto-detection]`

**Frameworks:** `[e.g., FastAPI, React, Django - leave blank for auto-detection]`

**Databases:** `[e.g., PostgreSQL, MongoDB - leave blank for auto-detection]`

**Infrastructure:** `[e.g., Docker, Kubernetes, AWS - leave blank for auto-detection]`

### Team Context

**Team Size:** `[small (1-3) / medium (4-10) / large (10+)]`

**Experience Level:** `[beginner / intermediate / expert]`

**Timeline:** `[MVP / short-term (weeks) / long-term (months)]`

### Special Requirements

**Compliance Needs:** `[e.g., HIPAA, PCI-DSS, SOC2, GDPR - or "none"]`

**Performance Requirements:** `[e.g., high-throughput, low-latency, or "standard"]`

**Scale Requirements:** `[e.g., concurrent users, data volume, or "standard"]`

---

## 🚀 AI Processing Instructions

### Step 1: Repository Analysis

Analyze the repository to detect:

```yaml
# Example auto-detection output
project_analysis:
  detected_type: "web-service"  # From product-matrix.yaml
  primary_language: "python"
  frameworks:
    - "fastapi"
    - "sqlalchemy"
  databases:
    - "postgresql"
  infrastructure:
    - "docker"
    - "kubernetes"
  testing_frameworks:
    - "pytest"
    - "pytest-cov"
```

### Step 2: Standards Loading

Based on detection, generate the appropriate `@load` directive:

```bash
# For web-service with Python/FastAPI/PostgreSQL
@load [product:web-service + CS:python + TS:pytest + SEC:* + DE:database]

# This expands to:
# - CS:python (Python coding standards)
# - TS:pytest (pytest testing standards)
# - SEC:auth, SEC:secrets, SEC:input-validation, etc. (all security)
# - DE:database (database patterns)
# - NIST-IG:base (auto-included with SEC)
# - DOP:ci-cd (from web-service product type)
# - OBS:monitoring (from web-service product type)
```

### Step 3: Project Structure Generation

Create recommended directory structure:

```
project-root/
├── src/
│   ├── api/              # API routes and endpoints
│   ├── core/             # Core business logic
│   ├── models/           # Data models
│   ├── services/         # Service layer
│   └── utils/            # Utility functions
├── tests/
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── e2e/              # End-to-end tests
├── docs/
│   ├── api/              # API documentation
│   ├── guides/           # User guides
│   └── architecture/     # Architecture docs
├── config/
│   ├── development/      # Dev environment configs
│   ├── staging/          # Staging configs
│   └── production/       # Production configs
├── scripts/
│   ├── setup/            # Setup scripts
│   └── deploy/           # Deployment scripts
├── .github/
│   └── workflows/        # CI/CD workflows
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Python project config
├── .env.example          # Environment template
├── .gitignore
├── README.md
└── PROJECT_PLAN.md       # Generated plan
```

### Step 4: Configuration Files

Generate essential configuration files based on standards:

**Example: Python Project (pyproject.toml)**

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=src --cov-report=html --cov-report=term --cov-fail-under=80"

[tool.black]
line-length = 88
target-version = ['py311']

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W"]
ignore = []

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

**Example: CI/CD Pipeline (.github/workflows/ci.yml)**

```yaml
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
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run linting
        run: |
          ruff check .
          black --check .
          mypy src/
      - name: Run tests
        run: pytest
      - name: Security scan
        run: bandit -r src/

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
```

### Step 5: Implementation Checklist

Generate a comprehensive checklist in PROJECT_PLAN.md:

```markdown
## Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Repository setup with .gitignore, README, LICENSE
- [ ] Project structure creation
- [ ] Development environment configuration
- [ ] Install and configure linting tools
- [ ] Set up pre-commit hooks
- [ ] Initial CI/CD pipeline

### Phase 2: Core Implementation (Weeks 2-3)
- [ ] Database models and migrations
- [ ] API endpoints with validation
- [ ] Authentication and authorization
- [ ] Business logic implementation
- [ ] Error handling and logging
- [ ] Unit tests for core functionality

### Phase 3: Security & Testing (Week 4)
- [ ] Input validation on all endpoints
- [ ] Secret management setup
- [ ] Security scanning integration
- [ ] Integration test suite
- [ ] End-to-end test scenarios
- [ ] Achieve 80%+ test coverage

### Phase 4: Deployment (Week 5)
- [ ] Docker containerization
- [ ] Environment-specific configurations
- [ ] Deployment scripts and automation
- [ ] Monitoring and alerting setup
- [ ] Documentation completion
- [ ] Production readiness review
```

### Step 6: Quick Start Commands

Provide exact commands for immediate productivity:

```bash
# 1. Clone standards repository for reference
git clone https://github.com/williamzujkowski/standards.git ../standards

# 2. Install development dependencies
pip install -r requirements-dev.txt

# 3. Set up pre-commit hooks
pre-commit install

# 4. Create environment file
cp .env.example .env
# Edit .env with your configuration

# 5. Run database migrations (if applicable)
alembic upgrade head

# 6. Run tests to verify setup
pytest

# 7. Start development server
uvicorn src.main:app --reload

# 8. Access API documentation
# http://localhost:8000/docs
```

---

## 🎯 Standards Reference

The AI assistant should reference these standards from the repository:

- **Standards URL:** `https://github.com/williamzujkowski/standards`
- **Router:** `CLAUDE.md` (main LLM interface)
- **Product Matrix:** `config/product-matrix.yaml` (product type mappings)
- **Standards Docs:** `docs/standards/*.md` (comprehensive standards)
- **Examples:** `examples/` (templates and patterns)
- **Scripts:** `scripts/` (automation tools)

### Key Standards Files by Category

**Coding Standards (CS)**

- `docs/standards/CODING_STANDARDS.md`
- Language-specific sections for Python, JavaScript, TypeScript, Go, Java, etc.

**Testing Standards (TS)**

- `docs/standards/TESTING_STANDARDS.md`
- Framework-specific patterns (pytest, Jest, Vitest, etc.)

**Security Standards (SEC)**

- `docs/standards/MODERN_SECURITY_STANDARDS.md`
- Authentication, secrets management, input validation

**DevOps Standards (DOP)**

- `docs/standards/DEVOPS_STANDARDS.md`
- CI/CD, infrastructure as code, deployment

**NIST Compliance (NIST-IG)**

- `docs/nist/NIST_IMPLEMENTATION_GUIDE.md`
- Control tagging and compliance mapping

---

## 📊 Expected Output Format

The AI assistant should generate PROJECT_PLAN.md with these sections:

### 1. Executive Summary

- Project overview
- Technical stack decision rationale
- Timeline and milestones

### 2. Architecture

- System architecture diagram (mermaid or ASCII)
- Component responsibilities
- Data flow
- External integrations

### 3. Technology Stack

- Languages and frameworks with versions
- Databases and storage
- Infrastructure and deployment
- Development tools

### 4. Standards Applied

- List of loaded standards with justification
- Key patterns from each standard
- Compliance requirements

### 5. Project Structure

- Directory tree with explanations
- File naming conventions
- Module organization

### 6. Development Workflow

- Git branching strategy
- Code review process
- Testing approach
- Deployment process

### 7. Security Implementation

- Authentication mechanism
- Authorization model
- Secret management approach
- Security scanning tools
- NIST control mapping (if applicable)

### 8. Testing Strategy

- Unit test approach (target: 80%+ coverage)
- Integration test scenarios
- E2E test cases
- Performance testing
- Security testing

### 9. Quality Gates

- Pre-commit checks
- CI pipeline stages
- Code coverage thresholds
- Security scan requirements
- Performance benchmarks

### 10. Implementation Timeline

- Phase breakdown
- Task dependencies
- Resource requirements
- Risk mitigation

### 11. Success Criteria

- Functional requirements met
- Quality metrics achieved
- Performance targets
- Security compliance
- Documentation completeness

---

## 🔄 Iteration and Refinement

After initial plan generation:

1. **Review** the generated plan for accuracy
2. **Validate** that detected technologies match reality
3. **Adjust** standards loading if needed
4. **Refine** timeline based on team capacity
5. **Document** any deviations from standards with rationale

---

## 📚 Additional Resources

- **Full Standards Repository:** https://github.com/williamzujkowski/standards
- **Skills System (Progressive Loading):** `docs/SKILLS_CATALOG.md`
- **Product Matrix Guide:** `docs/guides/USING_PRODUCT_MATRIX.md`
- **NIST Implementation:** `docs/nist/NIST_IMPLEMENTATION_GUIDE.md`
- **Creating Standards:** `docs/guides/CREATING_STANDARDS_GUIDE.md`

---

## ⚠️ Important Notes for AI Assistants

1. **Auto-Detection First:** Always attempt auto-detection before asking users for tech stack details
2. **Standards-Based:** All recommendations must align with loaded standards
3. **Practical Outputs:** Provide copy-paste ready code and commands
4. **Security Default:** Always include security standards (SEC) for production systems
5. **NIST Auto-Include:** When SEC standards are loaded, auto-include NIST-IG:base
6. **Quality Focus:** Enforce quality gates from the start (testing, linting, security)
7. **Documentation:** Generate clear, maintainable documentation
8. **Scalability:** Design for growth from day one
9. **Team Context:** Adjust complexity based on team size and experience
10. **Compliance Aware:** If compliance mentioned, heavily reference NIST controls

---

## 🎓 Example Usage

**User provides:**

```
Project: Healthcare patient portal API
Team: 3 developers (intermediate)
Timeline: 8 weeks MVP
Compliance: HIPAA required
```

**AI detects:**

```yaml
type: api
language: python
framework: fastapi
database: postgresql
compliance: hipaa
```

**AI loads:**

```bash
@load [product:api + CS:python + TS:pytest + SEC:* + COMP:hipaa + DE:database]
```

**AI generates:**

- Full project structure
- HIPAA-compliant architecture
- Security implementation (encryption, audit logging, access controls)
- NIST control mapping for HIPAA requirements
- Testing strategy with privacy considerations
- CI/CD with security scanning
- Documentation with compliance notes
- 8-week implementation timeline

---

**Ready to start? Fill in the Project Information section above and provide this file to your AI assistant!**
