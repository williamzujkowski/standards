# 🚀 Software Development Standards

![Anthropic Skills](https://img.shields.io/badge/Anthropic%20Skills-68.9%25%20Compliant-yellow)

**Start any project right in 30 seconds. Based on industry best practices and NIST guidelines.**

## Why This Repository?

You're starting a new project. You need to make dozens of decisions: project structure, testing approach, security patterns, CI/CD setup, documentation format. Each wrong choice costs days or weeks to fix later.

**This repository gives you those answers immediately** - comprehensive, production-tested standards that work together as a complete system. No more arguing about code style. No more wondering about test coverage. No more security reviews finding basic issues.

Just copy, implement, and ship.

---

## 🆕 Skills System (NEW!)

**Last Updated**: 2025-10-24 21:45:00 EDT (UTC-04:00)

**Load only what you need. Progressive loading reduces token usage by 91-99.6% depending on scenario:**

- Repository metadata: 127K → 500 tokens (99.6% reduction)
- Typical usage: 8.9K → 573 tokens (93.6% reduction)
- Single skill Level 1: ~300-600 tokens

**Evidence**: 61 active skills with progressive disclosure (Level 1: metadata, Level 2: instructions, Level 3: resources)

### What Are Skills?

Instead of loading massive 50,000+ token documents, use **progressive skills** that deliver the right information at the right time:

**Note**: The `@load` directive is planned for v2.0. Current implementation uses the skill-loader script.

**Current (v1.x):**

```bash
# Load Level 1: Quick Start (5 minutes, ~336 tokens)
python3 scripts/skill-loader.py load skill:coding-standards

# Load by product type (auto-selects relevant skills)
python3 scripts/skill-loader.py load product:api --language python
# Loads: coding-standards, security-practices, testing, nist-compliance

# Total: ~1,755 tokens compared to loading all standards documents (~150K tokens) (98.8% reduction)
```

**Planned (v2.0):**

```bash
@load skill:coding-standards
@load product:api --language python
```

### Quick Skills Tutorial (2 minutes)

**Current (v1.x):**

```bash
# 1. Get skill recommendations for your project
python3 scripts/skill-loader.py recommend ./

# 2. Load recommended skills
python3 scripts/skill-loader.py load product:api

# 3. See the difference!
# Before: ~150,000 tokens (full standards)
# After: ~1,755 tokens (Level 1)
```

**Planned (v2.0):**

```bash
# 2. Load recommended skills
@load product:api
```

### Available Skills (61 Total)

**Skill Count Verified**: 2025-10-24 19:21:55 EDT (UTC-04:00)

**Core Skills** (examples with estimated Level 1 token counts):

- **coding-standards**: Code quality patterns (~300-400 tokens L1)
- **security-practices**: Modern security (~400-500 tokens L1)
- **testing**: TDD & testing strategies (~400-500 tokens L1)
- **nist-compliance**: NIST 800-53r5 controls (~500-600 tokens L1)

Note: Token counts are estimates. Actual counts vary based on skill complexity. See `skills/` directory for complete catalog.

**[View Full Catalog →](./docs/SKILLS_CATALOG.md) | [Quick Start Guide →](./docs/guides/SKILLS_QUICK_START.md) | [Skills Directory →](./skills/README.md)**

---

## ⚡ Quick Start for New Projects

**Copy these templates to your new repository and let AI do the rest:**

### Option 1: Full Kickstart Template (Recommended)

```bash
# 1. Copy the kickstart template to your new repo
curl -o KICKSTART.md https://raw.githubusercontent.com/williamzujkowski/standards/master/templates/KICKSTART_REPO.md

# 2. Fill in basic project details (or let AI auto-detect)

# 3. Provide KICKSTART.md to any AI assistant (Claude, ChatGPT, Gemini)
# AI will auto-detect your tech stack and generate:
# - Complete project structure
# - Standards-aligned code
# - Configuration files
# - CI/CD pipelines
# - Testing setup
# - Security implementation
```

### Option 2: Use LLM Prompt Directly

1. **Copy this prompt**: [KICKSTART_PROMPT.md](./docs/guides/KICKSTART_PROMPT.md)
2. **Paste into any LLM** (ChatGPT, Claude, Gemini, etc.) with your project description
3. **Get instant analysis**:
   - Complete project structure
   - Relevant standards selection
   - Implementation roadmap
   - Tool configurations
   - First PR ready to go

**Example:**

```
You: [Paste kickstart prompt] + "I'm building a Python API with FastAPI and PostgreSQL"

AI: Here's your complete setup:
- Project structure with /src, /tests, /docs
- FastAPI best practices from CODING_STANDARDS.md
- pytest configuration from TESTING_STANDARDS.md
- PostgreSQL patterns from DATA_ENGINEERING_STANDARDS.md
- Docker setup from CLOUD_NATIVE_STANDARDS.md
- GitHub Actions from .github/workflows/
[... complete implementation plan ...]
```

### What You Get

The AI assistant will generate a complete `PROJECT_PLAN.md` including:

- **Auto-detected tech stack** from your repository
- **Standards recommendations** using `@load` directives (v2.0 - planned) or skill-loader script (v1.x - current)
- **Project structure** with full directory tree
- **Configuration files** (pyproject.toml, package.json, etc.)
- **CI/CD pipelines** with quality gates
- **Security implementation** with NIST controls
- **Testing strategy** with 80%+ coverage targets
- **8-week implementation timeline** with phases

### Common Scenarios

**Note**: The `@load` directive examples below are planned for v2.0. Current implementation uses skill-loader script.

**Python API (v2.0 - planned):**

```bash
@load [product:api + CS:python + TS:pytest + SEC:* + DE:database]
```

**Python API (v1.x - current):**

```bash
python3 scripts/skill-loader.py load product:api --language python
```

**React Web App (v2.0 - planned):**

```bash
@load [product:frontend-web + FE:react + SEC:auth + DOP:ci-cd]
```

**React Web App (v1.x - current):**

```bash
python3 scripts/skill-loader.py load product:frontend-web --framework react
```

**Mobile App (v2.0 - planned):**

```bash
@load [product:mobile + CS:swift + TS:xctest + SEC:mobile-auth]
```

**Mobile App (v1.x - current):**

```bash
python3 scripts/skill-loader.py load product:mobile
```

**Data Pipeline (v2.0 - planned):**

```bash
@load [product:data-pipeline + CS:python + DE:* + OBS:monitoring]
```

**Data Pipeline (v1.x - current):**

```bash
python3 scripts/skill-loader.py load product:data-pipeline --language python
```

---

## 📋 Available Templates

### Core Templates

| Template | Purpose | Usage |
|----------|---------|-------|
| [KICKSTART_REPO.md](./templates/KICKSTART_REPO.md) | LLM-optimized repo kickstart | Copy to new repo, fill details, provide to AI |
| [PROJECT_PLAN_TEMPLATE.md](./templates/PROJECT_PLAN_TEMPLATE.md) | Systematic project planning | AI generates this from kickstart |

### Example Projects

| Example | Tech Stack | Located In |
|---------|-----------|------------|
| Python API | FastAPI + PostgreSQL | [examples/project-templates/python-api/](./examples/project-templates/) |
| React SPA | React + TypeScript | [examples/project-templates/react-spa/](./examples/project-templates/) |
| NIST-compliant Service | Security controls | [examples/nist-templates/](./examples/nist-templates/) |

---

## 🔄 For Existing Projects

```bash
# Quick assessment
curl -O https://raw.githubusercontent.com/williamzujkowski/standards/master/scripts/setup-project.sh
chmod +x setup-project.sh
./setup-project.sh --assess my-project

# Or manually:
1. Review UNIFIED_STANDARDS.md for gaps
2. Copy relevant templates from examples/
3. Run validation: python scripts/generate-audit-reports.py
```

---

## 📚 What You Get

### Complete Standards Library (25 Documents)

**Core Development**

- [UNIFIED_STANDARDS.md](./docs/standards/UNIFIED_STANDARDS.md) - Master reference (start here)
- [CODING_STANDARDS.md](./docs/standards/CODING_STANDARDS.md) - Language-specific patterns
- [TESTING_STANDARDS.md](./docs/standards/TESTING_STANDARDS.md) - Test strategies & coverage
- [MODERN_SECURITY_STANDARDS.md](./docs/standards/MODERN_SECURITY_STANDARDS.md) - Security implementation
- [KNOWLEDGE_MANAGEMENT_STANDARDS.md](./docs/standards/KNOWLEDGE_MANAGEMENT_STANDARDS.md) - Documentation architecture

**Specialized Domains**

- Frontend, Mobile, Backend, Data Engineering
- Cloud Native, DevOps, Observability
- AI/ML, Event-Driven, Microservices
- Cost Optimization, Legal Compliance

### Ready-to-Use Templates

```
examples/
├── project-templates/     # Python, JS/TS, Go starter projects
├── nist-templates/        # Security components with compliance tags
├── docker/                # Container configurations
└── ci-cd/                 # GitHub Actions workflows
```

### Automation & Tools

- **Setup Scripts**: Auto-configure new projects
- **Validation Tools**: Check standards compliance
- **NIST Tagging**: Security control annotations
- **VS Code Extension**: Real-time compliance hints
- **Pre-commit Hooks**: Enforce standards automatically

---

## 🎯 For Different Roles

### Developers

- Copy working code patterns
- Skip bikeshedding discussions
- Focus on building features
- Pass code reviews easily

### Tech Leads

- Onboard team members faster
- Maintain consistency across projects
- Reduce technical debt
- Implement best practices systematically

### Architects

- Reference architecture patterns
- Security-by-default designs
- Scalability guidelines
- Integration strategies

### Compliance Teams

- NIST 800-53r5 control templates
- Audit-ready documentation
- Automated compliance checking
- Evidence collection tools

---

## 🔥 Real Examples

### Start a Python API

**Planned (v2.0):**

```bash
@load [product:api + CS:python + TS:pytest + SEC:auth]
# Gets you: FastAPI structure, pytest config, JWT auth, Docker, CI/CD
```

**Current (v1.x):**

```bash
python3 scripts/skill-loader.py load product:api --language python
# Gets you: FastAPI structure, pytest config, JWT auth, Docker, CI/CD
```

### Build a React App

**Planned (v2.0):**

```bash
@load [product:frontend-web + FE:react + SEC:*]
# Gets you: React patterns, testing, all security standards, deployment
```

**Current (v1.x):**

```bash
python3 scripts/skill-loader.py load product:frontend-web --framework react
# Gets you: React patterns, testing, all security standards, deployment
```

### Data Pipeline

**Planned (v2.0):**

```bash
@load [product:data-pipeline + DE:* + OBS:monitoring]
# Gets you: ETL patterns, data quality, monitoring, orchestration
```

**Current (v1.x):**

```bash
python3 scripts/skill-loader.py load product:data-pipeline
# Gets you: ETL patterns, data quality, monitoring, orchestration
```

---

## 📁 Repository Structure

```
standards/
├── docs/
│   ├── standards/          # 24 comprehensive standards
│   ├── guides/             # Implementation guides
│   └── nist/               # NIST compliance docs
├── examples/               # Copy-paste templates
├── scripts/                # Automation tools
├── config/                 # Configuration files
├── .github/workflows/      # CI/CD templates
└── CLAUDE.md               # LLM interface & routing
```

---

## ⚖️ Legal & License

MIT License - Free for commercial use. Standards provided "as-is" without warranty. Legal compliance documents are templates, not legal advice. Always consult professionals for your specific needs.

---

## 🤝 Contributing

We actively welcome contributions! The standards evolve with real-world usage.

- **Report issues** you encounter
- **Submit PRs** with improvements
- **Share templates** that work
- **Add examples** from your projects

See [CREATING_STANDARDS_GUIDE.md](./docs/guides/CREATING_STANDARDS_GUIDE.md) for guidelines.

### 📖 Documentation (MkDocs)

This repository uses [MkDocs](https://www.mkdocs.org/) with the [Material theme](https://squidfunk.github.io/mkdocs-material/) for documentation.

**Local Development:**

```bash
# Install dependencies
pip install -r requirements.txt

# Serve documentation locally (with live reload)
mkdocs serve
# Visit http://127.0.0.1:8000

# Build static site
mkdocs build

# Build with strict mode (fails on warnings)
mkdocs build --strict
```

**Features:**

- Material theme with light/dark mode
- Enhanced search functionality
- Mobile-responsive navigation
- Automatic deployment via GitHub Actions

Documentation automatically deploys to GitHub Pages when changes are pushed to the master branch.

---

## 🤖 Claude Code Integration

Make all standards skills and agents globally available in Claude Code via auto-discovery.

### Quick Install

```bash
# Run from standards repo root
./scripts/sync-to-claude.sh

# Verify installation
ls ~/.claude/skills/std-* | head -5
ls ~/.claude/agents/std-*.md | head -5
```

### What Gets Installed

- **61 Skills**: Symlinked to `~/.claude/skills/std-*`
- **60 Agents**: Symlinked to `~/.claude/agents/std-*.md`

All items prefixed with `std-` for easy identification and to avoid conflicts.

### Uninstall

```bash
./scripts/sync-to-claude.sh --uninstall
```

---

## 🚦 Quick Links

**Get Started**

- 🚀 [KICKSTART_PROMPT.md](./docs/guides/KICKSTART_PROMPT.md) - AI project analyzer
- 📚 [UNIFIED_STANDARDS.md](./docs/standards/UNIFIED_STANDARDS.md) - Complete reference
- ✅ [ADOPTION_CHECKLIST.md](./docs/guides/ADOPTION_CHECKLIST.md) - Implementation roadmap

**Skills (NEW!)**

- 🆕 [Skills Quick Start](./docs/guides/SKILLS_QUICK_START.md) - 5-minute tutorial
- 📖 [Skills User Guide](./docs/guides/SKILLS_USER_GUIDE.md) - Complete guide
- 📚 [Skills Catalog](./docs/SKILLS_CATALOG.md) - All available skills
- 🔄 [Migration Guide](./docs/migration/MIGRATION_GUIDE.md) - Migrate to skills
- ✍️ [Authoring Guide](./docs/guides/SKILL_AUTHORING_GUIDE.md) - Create skills
- 🔌 [Claude Integration](./docs/guides/CLAUDE_INTEGRATION_GUIDE.md) - API & CLI integration
- 📡 [API Documentation](./docs/api/SKILLS_API.md) - Programmatic API

**Resources**

- [Project Templates](./examples/project-templates/)
- [Setup Script](./scripts/setup-project.sh)
- [Standards Index](./docs/guides/STANDARDS_INDEX.md)
- [Creating Standards Guide](./docs/guides/CREATING_STANDARDS_GUIDE.md)

**Support**

- [GitHub Issues](https://github.com/williamzujkowski/standards/issues)
- [Discussions](https://github.com/williamzujkowski/standards/discussions)

---

*Stop debating. Start shipping. Your standards are here.*

## Catalog (auto)

<!-- AUTO-LINKS:badges/** -->

- [standards-compliance-template](badges/standards-compliance-template.md)

<!-- /AUTO-LINKS -->
<!-- AUTO-LINKS:badges/**/*.md -->

- [Readme](badges/README.md)
- [Standards Compliance Template](badges/standards-compliance-template.md)

<!-- /AUTO-LINKS -->
