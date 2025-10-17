# Project Templates

**Copy-paste ready templates for starting new projects with AI assistance.**

---

## 🎯 Quick Start

### For a New Project

```bash
# 1. Copy the kickstart template to your new repository
cd /path/to/your/new/project
curl -o KICKSTART.md https://raw.githubusercontent.com/williamzujkowski/standards/master/templates/KICKSTART_REPO.md

# 2. Fill in basic details (or let AI auto-detect)
# Edit KICKSTART.md and fill in the "Project Information" section

# 3. Provide to your AI assistant
# Copy the entire KICKSTART.md file and provide to Claude, ChatGPT, Gemini, etc.
# The AI will auto-detect your tech stack and generate PROJECT_PLAN.md
```

---

## 📄 Available Templates

### 1. KICKSTART_REPO.md

**Purpose:** LLM-optimized template for repository initialization

**Use When:**

- Starting a brand new project
- You want AI to auto-detect tech stack and generate a complete plan
- You need standards-aligned project structure

**What It Does:**

1. Provides project context to AI assistant
2. AI auto-detects technologies from your repository
3. AI loads appropriate standards via `@load` directives
4. AI generates comprehensive PROJECT_PLAN.md

**What AI Generates:**

- Complete project structure (directories, files)
- Configuration files (pyproject.toml, package.json, etc.)
- CI/CD pipelines (.github/workflows/)
- Testing setup with 80%+ coverage targets
- Security implementation with NIST controls
- 8-week implementation timeline
- Development workflow and quality gates

**Usage:**

```bash
# Copy to your repo
curl -o KICKSTART.md https://raw.githubusercontent.com/williamzujkowski/standards/master/templates/KICKSTART_REPO.md

# Edit the "Project Information" section
vim KICKSTART.md

# Provide to AI assistant (copy entire file)
# AI will generate PROJECT_PLAN.md
```

---

### 2. PROJECT_PLAN_TEMPLATE.md

**Purpose:** Comprehensive project planning document

**Use When:**

- AI has processed KICKSTART_REPO.md
- You need a detailed implementation roadmap
- Manual project planning is required

**What It Contains:**

- Executive summary and timeline
- System architecture and data flow
- Technology stack with justifications
- Standards applied and compliance requirements
- Project structure with file organization
- Development workflow (Git, code review, testing)
- Security implementation (auth, secrets, NIST controls)
- Testing strategy (unit, integration, E2E)
- Quality gates (coverage, security scans, performance)
- 8-week implementation timeline with phases
- Success criteria and risk management

**Note:** AI generates this automatically from KICKSTART_REPO.md, but you can use it as a reference template for manual planning.

---

## 🚀 Workflow Examples

### Example 1: Python FastAPI Project

**Step 1:** Copy kickstart template

```bash
cd my-fastapi-project
curl -o KICKSTART.md https://raw.githubusercontent.com/williamzujkowski/standards/master/templates/KICKSTART_REPO.md
```

**Step 2:** Fill in project details

```markdown
**Project Name:** `Healthcare Patient Portal API`
**Project Description:** `RESTful API for patient data management`
**Team Size:** `medium (4-10)`
**Experience Level:** `intermediate`
**Timeline:** `short-term (weeks)`
**Compliance Needs:** `HIPAA`
```

**Step 3:** Provide to AI

```
[Copy entire KICKSTART.md]

AI detects:
- Language: Python 3.11
- Framework: FastAPI
- Database: PostgreSQL
- Infrastructure: Docker, Kubernetes

AI loads:
@load [product:api + CS:python + TS:pytest + SEC:* + COMP:hipaa + DE:database]

AI generates:
- PROJECT_PLAN.md with full implementation details
- HIPAA-compliant architecture
- Security controls mapped to NIST
- Complete 8-week timeline
```

---

### Example 2: React Web Application

**Step 1:** Copy kickstart template

```bash
cd my-react-app
curl -o KICKSTART.md https://raw.githubusercontent.com/williamzujkowski/standards/master/templates/KICKSTART_REPO.md
```

**Step 2:** Fill in project details

```markdown
**Project Name:** `E-commerce Dashboard`
**Project Description:** `Admin dashboard for product management`
**Team Size:** `small (1-3)`
**Experience Level:** `expert`
**Timeline:** `MVP`
```

**Step 3:** AI auto-detects and generates

```
AI detects:
- Language: TypeScript
- Framework: React, Vite
- State: Redux Toolkit
- UI: Material-UI

AI loads:
@load [product:frontend-web + FE:react + CS:typescript + TS:vitest + SEC:auth]

AI generates:
- Component structure
- State management patterns
- Testing setup (Vitest + React Testing Library)
- CI/CD with Vercel deployment
- Security headers and CSP
```

---

## 🔗 Integration with Standards Repository

### How It Works

1. **Standards Router (`CLAUDE.md`)**: Main LLM interface
2. **Product Matrix (`config/product-matrix.yaml`)**: Maps product types to standards
3. **Standards Docs (`docs/standards/*.md`)**: Comprehensive implementation guides
4. **Templates (this directory)**: Copy-paste ready kickstart files

### @load Directive Examples

**Product Types:**

```bash
@load product:api              # REST/GraphQL API service
@load product:web-service       # Full-stack web application
@load product:frontend-web      # React/Vue/Angular SPA
@load product:mobile           # iOS/Android application
@load product:data-pipeline    # ETL/ELT data workflow
@load product:ml-service       # ML training/inference service
```

**Custom Combinations:**

```bash
@load [product:api + CS:python + TS:pytest]       # Python API
@load [product:frontend-web + FE:react + SEC:*]   # React with all security
@load [CS:python + TS:* + SEC:* + NIST-IG:full]  # Full compliance stack
```

**Wildcard Expansion:**

```bash
SEC:*  → SEC:auth, SEC:secrets, SEC:input-validation, SEC:encryption, SEC:audit, NIST-IG:base
TS:*   → TS:unit, TS:integration, TS:e2e, TS:performance, TS:security
DOP:*  → DOP:ci-cd, DOP:iac, DOP:monitoring, DOP:incident-response
FE:*   → FE:design-system, FE:accessibility, FE:performance, FE:responsive
```

---

## 📊 What Gets Generated

When AI processes KICKSTART_REPO.md, it generates:

### 1. Project Structure

```
project-root/
├── src/                   # Source code
├── tests/                 # Test suite
├── docs/                  # Documentation
├── config/                # Configurations
├── scripts/               # Automation scripts
├── .github/workflows/     # CI/CD pipelines
├── docker/                # Container configs
├── requirements.txt       # Dependencies
├── pyproject.toml         # Python config
└── PROJECT_PLAN.md        # This gets generated
```

### 2. Configuration Files

**Python Example:**

- `pyproject.toml` with black, ruff, mypy, pytest configs
- `requirements.txt` and `requirements-dev.txt`
- `.pre-commit-config.yaml` with hooks
- `pytest.ini` with coverage settings

**TypeScript Example:**

- `package.json` with scripts and dependencies
- `tsconfig.json` with strict type checking
- `vitest.config.ts` with coverage
- `.eslintrc.json` and `.prettierrc`

### 3. CI/CD Pipelines

**GitHub Actions:**

- Linting and formatting
- Security scanning (Gitleaks, Bandit, Trivy)
- Unit and integration tests
- Code coverage enforcement
- Docker build and push
- Deployment to staging/production

### 4. Security Setup

- Authentication mechanism (JWT, OAuth2)
- Authorization model (RBAC)
- Secret management (environment variables, AWS Secrets Manager)
- Input validation (Pydantic, Zod)
- Security scanning (Bandit, ESLint security plugins)
- NIST control mapping (if compliance required)

### 5. Testing Strategy

- Unit tests with fixtures and mocks
- Integration tests for API endpoints
- E2E tests for critical workflows
- Performance tests (load testing with Locust)
- Security tests (OWASP ZAP)
- Coverage targets (80%+ overall, 90%+ critical paths)

### 6. Documentation

- README.md with quick start
- API documentation (OpenAPI/Swagger auto-generated)
- Architecture diagrams (Mermaid)
- Deployment guides
- Contributing guidelines

---

## 🎓 Best Practices

### When Using Templates

1. **Be Specific:** Provide clear project description and requirements
2. **Let AI Detect:** Leave tech stack fields blank to enable auto-detection
3. **Review Generated Plan:** Always review PROJECT_PLAN.md before implementation
4. **Customize:** Adapt generated plan to your specific needs
5. **Iterate:** Refine with AI if initial generation isn't perfect

### Standards Alignment

- Templates enforce standards from this repository
- Generated code follows coding standards (CS)
- Testing targets align with testing standards (TS)
- Security implements modern security standards (SEC)
- NIST controls auto-included when security is present

### Quality Assurance

- All generated code includes tests (80%+ coverage)
- CI/CD pipelines enforce quality gates
- Security scanning integrated from day one
- Documentation generated alongside code
- Pre-commit hooks prevent common mistakes

---

## 🔄 Template Lifecycle

### 1. Project Initialization

```
User copies KICKSTART_REPO.md → Fills in details → Provides to AI
```

### 2. AI Processing

```
AI auto-detects tech stack → Loads standards → Generates PROJECT_PLAN.md
```

### 3. Implementation

```
Follow PROJECT_PLAN.md phases → Use generated configs → Run quality gates
```

### 4. Iteration

```
Update PROJECT_PLAN.md as project evolves → Re-run AI for new features
```

---

## 📚 Related Documentation

**Standards Repository:**

- [Main README](../README.md) - Repository overview
- [UNIFIED_STANDARDS.md](../docs/standards/UNIFIED_STANDARDS.md) - Complete standards
- [CLAUDE.md](../CLAUDE.md) - LLM router and interface

**Kickstart System:**

- [KICKSTART_PROMPT.md](../docs/guides/KICKSTART_PROMPT.md) - Direct LLM prompt
- [Product Matrix](../config/product-matrix.yaml) - Product type mappings
- [Skills Catalog](../docs/SKILLS_CATALOG.md) - Progressive skill loading

**Implementation Guides:**

- [Standards Index](../docs/guides/STANDARDS_INDEX.md) - All standards
- [Adoption Checklist](../docs/guides/ADOPTION_CHECKLIST.md) - Implementation steps
- [Creating Standards Guide](../docs/guides/CREATING_STANDARDS_GUIDE.md) - Authoring standards

---

## ❓ FAQ

**Q: Can I modify the templates?**
A: Yes! These are starting points. Customize to your needs.

**Q: Do I need to use AI?**
A: No, but AI makes it much faster. You can use PROJECT_PLAN_TEMPLATE.md manually.

**Q: What AI models work best?**
A: Claude, ChatGPT, and Gemini all work well. Claude excels at structured output.

**Q: Can I use this for existing projects?**
A: Yes, but templates are optimized for new projects. For existing projects, use the [setup script](../scripts/setup-project.sh).

**Q: Are NIST controls required?**
A: Only if you have compliance requirements (HIPAA, PCI-DSS, etc.). Otherwise, they're optional but recommended.

**Q: How do I update generated PROJECT_PLAN.md?**
A: Edit directly or re-run AI with updated KICKSTART.md context.

---

## 🤝 Contributing

Have a template improvement? Found an issue?

1. Open an issue describing the problem
2. Submit a PR with improvements
3. Share your generated PROJECT_PLAN.md examples

See [Contributing Guide](../docs/guides/CREATING_STANDARDS_GUIDE.md) for details.

---

**Ready to start? Copy KICKSTART_REPO.md to your new project and let AI build your standards-aligned foundation!**
