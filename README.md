# 🚀 Software Development Standards

**Start any project right in 30 seconds. Battle-tested standards from real production systems.**

## Why This Repository?

You're starting a new project. You need to make dozens of decisions: project structure, testing approach, security patterns, CI/CD setup, documentation format. Each wrong choice costs days or weeks to fix later.

**This repository gives you those answers immediately** - comprehensive, production-tested standards that work together as a complete system. No more arguing about code style. No more wondering about test coverage. No more security reviews finding basic issues.

Just copy, implement, and ship.

---

## ⚡ Quick Start (30 Seconds)

### For New Projects - Use the AI Kickstart

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

### For Existing Projects

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

### Complete Standards Library (24 Documents)

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

```bash
@load [product:api + CS:python + TS:pytest + SEC:auth]
# Gets you: FastAPI structure, pytest config, JWT auth, Docker, CI/CD
```

### Build a React App

```bash
@load [product:frontend-web + FE:react + SEC:*]
# Gets you: React patterns, testing, all security standards, deployment
```

### Data Pipeline

```bash
@load [product:data-pipeline + DE:* + OBS:monitoring]
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

## 🚦 Quick Links

**Get Started**

- 🚀 [KICKSTART_PROMPT.md](./docs/guides/KICKSTART_PROMPT.md) - AI project analyzer
- 📚 [UNIFIED_STANDARDS.md](./docs/standards/UNIFIED_STANDARDS.md) - Complete reference
- ✅ [ADOPTION_CHECKLIST.md](./docs/guides/ADOPTION_CHECKLIST.md) - Implementation roadmap

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
