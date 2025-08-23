# 🚀 Comprehensive Software Development Standards

**Battle-tested standards for modern software development with AI-powered kickstart and NIST 800-53r5 compliance**

[![Version](https://img.shields.io/badge/version-latest-blue.svg)](https://github.com/williamzujkowski/standards)
[![Standards](https://img.shields.io/badge/standards-24%20documents-green.svg)](https://github.com/williamzujkowski/standards)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)
[![Compliance](https://github.com/williamzujkowski/standards/actions/workflows/standards-compliance.yml/badge.svg)](https://github.com/williamzujkowski/standards/actions/workflows/standards-compliance.yml)
[![Audit Gates](https://github.com/williamzujkowski/standards/actions/workflows/lint-and-validate.yml/badge.svg)](https://github.com/williamzujkowski/standards/actions/workflows/lint-and-validate.yml)
[![NIST](https://img.shields.io/badge/NIST%20800--53r5-Compliant-brightgreen.svg)](./docs/nist/NIST_IMPLEMENTATION_GUIDE.md)

---

---

## 🆕 What's New

### 🔐 NIST 800-53r5 Compliance Integration

- **Automated Control Tagging**: Tag security features with `@nist` annotations
- **VS Code Extension**: Real-time NIST control suggestions
- **CI/CD Integration**: Automated compliance checking and SSP generation
- **Quick Start**: `./scripts/setup-nist-hooks.sh` - Get compliant in minutes!
- **See**: [NIST_IMPLEMENTATION_GUIDE.md](./docs/nist/NIST_IMPLEMENTATION_GUIDE.md) for details

---

## 📁 File Organization Guidelines

### Generated Reports

Generated reports and summaries should be placed in `reports/generated/` to keep the root directory clean. This includes:

- Testing reports
- Implementation summaries
- Validation reports
- Weekly digests

### Important Files Not to Commit

The following files/directories are automatically ignored by `.gitignore`:

- `.claude-flow/` - Claude Flow runtime data
- `node_modules/` - Node.js dependencies
- `__pycache__/` - Python cache files
- `.vscode/`, `.idea/` - IDE configuration
- `*.log` - Log files
- `*.bak`, `*.orig`, `*.tmp` - Backup/temporary files

### Development Setup

Run `./scripts/setup-development.sh` to set up your development environment with:

- Pre-commit hooks for code quality
- Python virtual environment
- Required dependencies
- Proper directory structure

## 🎯 Quick Start Guide

### 🚀 **Option 1: AI-Powered Project Kickstart** (Recommended)

Get instant project analysis and implementation guidance:

1. **Copy the kickstart prompt** from [KICKSTART_PROMPT.md](./docs/guides/KICKSTART_PROMPT.md)
2. **Paste into any LLM** (ChatGPT, Claude, Gemini, etc.) along with your project plan
3. **Get instant analysis** including:
   - Tech stack validation
   - Relevant standards recommendations
   - Project structure and boilerplate
   - Implementation roadmap
   - Tool recommendations

> 💡 **Example**: See [examples/project_plan_example.md](./examples/project_plan_example.md) for a sample project plan

### ⚡ **Option 2: Automated Setup Script**

```bash
curl -O https://raw.githubusercontent.com/williamzujkowski/standards/master/scripts/setup-project.sh
chmod +x setup-project.sh
./setup-project.sh my-new-project
```

### 📋 **Option 3: Manual Setup**

1. Start with **[UNIFIED_STANDARDS.md](./docs/standards/UNIFIED_STANDARDS.md)** - Your comprehensive foundation
2. Copy **[CLAUDE.md](./CLAUDE.md)** to your project for AI assistance
3. Use templates from `examples/project-templates/` for your language
4. Follow **[ADOPTION_CHECKLIST.md](./docs/guides/ADOPTION_CHECKLIST.md)** for systematic implementation
5. **NEW**: Install NIST compliance hooks with `./scripts/setup-nist-hooks.sh`

### 🤖 **For AI/LLM Users**

Use our token-optimized loading system:

```
# Basic usage
@load [CS:python + TS:pytest + SEC:*]

# Natural language
"I need to build a React app with authentication"
→ Automatically loads: FE:react + SEC:auth + WD:components
```

---

## ⚖️ Legal Disclaimer

**IMPORTANT**: These standards are provided "as is" without warranty. Legal compliance documents do NOT constitute legal advice. Always consult qualified professionals for legal matters. You are responsible for evaluating suitability for your specific use case.

---

## 📚 What's Included

### **24 Comprehensive Standards Documents**

Complete coverage of modern software development practices from coding to deployment, security to compliance, including AI integration via Model Context Protocol.

### **🔐 NIST 800-53r5 Compliance Suite**

- **Control Tagging**: `@nist` annotations for security features
- **VS Code Extension**: Real-time control suggestions
- **Annotation Framework**: Multi-language parsers (JS/TS, Python, Go, Java, YAML)
- **Automated Tools**: Git hooks, CI/CD integration, SSP generation
- **Templates**: Pre-tagged security components
- **LLM Prompts**: Compliance-focused AI assistance

### **AI-Powered Features**

- 90% token reduction with CLAUDE.md
- Natural language to standards mapping
- Instant project kickstart analysis
- Context-aware recommendations
- NIST control suggestions

### **Ready-to-Use Templates**

- Language configs (Python, JS/TS, Go)
- NIST-tagged security templates
- CI/CD workflows with compliance checks
- Docker & Kubernetes manifests
- Tool configurations

### **Integration Tools**

- Automated setup scripts
- NIST compliance checking
- SSP generation
- Badge generation
- Migration guides

---

## 📂 Standards Categories

### 💻 **Development & Engineering**

- **[UNIFIED_STANDARDS.md](./docs/standards/UNIFIED_STANDARDS.md)** - Master document with all core standards
- **[CODING_STANDARDS.md](./docs/standards/CODING_STANDARDS.md)** - Language-specific best practices
- **[TESTING_STANDARDS.md](./docs/standards/TESTING_STANDARDS.md)** - Comprehensive testing methodologies
- **[MODERN_SECURITY_STANDARDS.md](./docs/standards/MODERN_SECURITY_STANDARDS.md)** - Zero Trust security implementation
- **[DATA_ENGINEERING_STANDARDS.md](./docs/standards/DATA_ENGINEERING_STANDARDS.md)** - Data pipeline and analytics
- **[KNOWLEDGE_MANAGEMENT_STANDARDS.md](./docs/standards/KNOWLEDGE_MANAGEMENT_STANDARDS.md)** - Documentation architecture patterns

### 🎨 **Frontend & Design**

- **[FRONTEND_MOBILE_STANDARDS.md](./docs/standards/FRONTEND_MOBILE_STANDARDS.md)** - React/Vue/Angular & mobile
- **[WEB_DESIGN_UX_STANDARDS.md](./docs/standards/WEB_DESIGN_UX_STANDARDS.md)** - Design systems & accessibility

### 🔧 **Operations & Infrastructure**

- **[CLOUD_NATIVE_STANDARDS.md](./docs/standards/CLOUD_NATIVE_STANDARDS.md)** - Container & microservices patterns
- **[DEVOPS_PLATFORM_STANDARDS.md](./docs/standards/DEVOPS_PLATFORM_STANDARDS.md)** - CI/CD & Infrastructure as Code
- **[OBSERVABILITY_STANDARDS.md](./docs/standards/OBSERVABILITY_STANDARDS.md)** - Monitoring, logging, tracing
- **[EVENT_DRIVEN_STANDARDS.md](./docs/standards/EVENT_DRIVEN_STANDARDS.md)** - Event architecture patterns
- **[MODEL_CONTEXT_PROTOCOL_STANDARDS.md](./docs/standards/MODEL_CONTEXT_PROTOCOL_STANDARDS.md)** - MCP server/client implementation

### 📊 **Business & Compliance**

- **[PROJECT_MANAGEMENT_STANDARDS.md](./docs/standards/PROJECT_MANAGEMENT_STANDARDS.md)** - Agile & team practices
- **[COST_OPTIMIZATION_STANDARDS.md](./docs/standards/COST_OPTIMIZATION_STANDARDS.md)** - FinOps & resource optimization
- **[LEGAL_COMPLIANCE_STANDARDS.md](./docs/standards/LEGAL_COMPLIANCE_STANDARDS.md)** - Privacy & regulatory compliance
- **[SEO_WEB_MARKETING_STANDARDS.md](./docs/standards/SEO_WEB_MARKETING_STANDARDS.md)** - Technical SEO & marketing

### 🔐 **NIST 800-53r5 Compliance**

- **[NIST_IMPLEMENTATION_GUIDE.md](./docs/nist/NIST_IMPLEMENTATION_GUIDE.md)** - 🚀 Quick start guide (15 min setup)
- **[COMPLIANCE_STANDARDS.md](./docs/standards/COMPLIANCE_STANDARDS.md)** - Detailed control tagging standards
- **[NIST_QUICK_REFERENCE.md](./docs/nist/NIST_QUICK_REFERENCE.md)** - Essential controls cheat sheet
- **[examples/nist-templates/](./examples/nist-templates/)** - Pre-tagged security templates
- **[prompts/nist-compliance/](./prompts/nist-compliance/)** - LLM prompts for compliance

### 🤖 **AI/LLM Integration**

- **[CLAUDE.md](./CLAUDE.md)** - Primary LLM interface (90% token reduction)
- **[KICKSTART_PROMPT.md](./docs/guides/KICKSTART_PROMPT.md)** - Universal project kickstart prompt
- **[KICKSTART_ADVANCED.md](./docs/guides/KICKSTART_ADVANCED.md)** - Advanced kickstart patterns
- **[KNOWLEDGE_MANAGEMENT_STANDARDS.md](./docs/standards/KNOWLEDGE_MANAGEMENT_STANDARDS.md)** - How to build AI-optimized documentation systems

---

## 🛠️ Integration Options

### **For New Projects**

1. Use the AI Kickstart (Option 1) for instant guidance
2. Run setup script (Option 2) for automated structure
3. Copy relevant templates from `examples/project-templates/`

### **For Existing Projects**

1. Read **[INTEGRATION_GUIDE.md](./docs/core/INTEGRATION_GUIDE.md)** for strategies
2. Perform gap analysis using standard checklists
3. Prioritize: Security → Testing → Core Standards
4. Use **[ADOPTION_CHECKLIST.md](./docs/guides/ADOPTION_CHECKLIST.md)** for phased adoption

### **Quick Integration Methods**

- **Git Submodule**: `git submodule add https://github.com/williamzujkowski/standards.git .standards`
- **Direct Copy**: Copy CLAUDE.md + relevant standards to your project
- **Remote Access**: Use standards directly via LLM without downloading

---

## 🌟 Essential Links

### **Getting Started**

- 🚀 [KICKSTART_PROMPT.md](./docs/guides/KICKSTART_PROMPT.md) - AI project analyzer
- 📚 [UNIFIED_STANDARDS.md](./docs/standards/UNIFIED_STANDARDS.md) - Complete standards reference
- 🤖 [CLAUDE.md](./CLAUDE.md) - LLM optimization interface
- ✅ [ADOPTION_CHECKLIST.md](./docs/guides/ADOPTION_CHECKLIST.md) - Implementation roadmap

### **Templates & Tools**

- 📁 [Project Templates](./examples/project-templates/) - Language-specific configs
- 🔐 [NIST Templates](./examples/nist-templates/) - Security components with controls
- 🔧 [Setup Script](./scripts/setup-project.sh) - Automated project setup
- 🛡️ [NIST Setup](./scripts/setup-nist-hooks.sh) - One-command compliance setup
- 📊 [Integration Guide](./docs/core/INTEGRATION_GUIDE.md) - Detailed integration strategies
- 🏷️ [Badge Generator](./scripts/generate-badges.sh) - Compliance badges
- 📝 [Standard Template](./docs/guides/STANDARD_TEMPLATE.md) - Template for new standards
- 📖 [Creating Standards Guide](./docs/guides/CREATING_STANDARDS_GUIDE.md) - How to contribute standards

### **Advanced Features**

- 🧩 [KICKSTART_ADVANCED.md](./docs/guides/KICKSTART_ADVANCED.md) - Advanced kickstart patterns
- 📋 [TOOLS_CATALOG.yaml](./config/TOOLS_CATALOG.yaml) - Centralized tool management
- 🔍 [STANDARDS_INDEX.md](./docs/guides/STANDARDS_INDEX.md) - Quick reference summaries
- 📈 [STANDARDS_GRAPH.md](./docs/guides/STANDARDS_GRAPH.md) - Standards relationships
- 🤖 VS Code NIST extension - Available in the .vscode/nist-extension/ directory
- 📊 [standards/compliance/](./standards/compliance/) - OSCAL compliance platform

---

## 📊 Why These Standards?

- **Comprehensive**: 24 documents covering all aspects of modern development
- **Battle-Tested**: Based on real-world projects and industry best practices
- **AI-Optimized**: 90% token reduction for efficient LLM usage
- **Compliance-Ready**: NIST 800-53r5 controls integrated throughout
- **Always Current**: Regular updates reflecting industry changes
- **Ready-to-Use**: Includes templates, configs, and automation scripts
- **Developer-Friendly**: Quick setup, minimal friction, maximum value

---

## 📚 Archived Reports

Historical implementation and validation reports have been archived to `reports/generated/`:

- Implementation reports
- Validation reports
- Cleanup summaries
- Weekly digests

See [reports/generated/](./reports/generated/) for full archive.

## 🤝 Contributing

We welcome contributions! Please:

- Report issues or suggest improvements
- Submit PRs with clear descriptions
- Follow existing format and structure
- Include practical examples
- Keep LLM optimization in mind

**Creating New Standards?** See [CREATING_STANDARDS_GUIDE.md](./docs/guides/CREATING_STANDARDS_GUIDE.md) and use [STANDARD_TEMPLATE.md](./docs/guides/STANDARD_TEMPLATE.md)

### 🧪 Quality Assurance

**Testing Suite** - Validate standards compliance:

```bash
cd tests && ./validate_knowledge_management.sh
```

**Linting System** - Enforce standards automatically:

```bash
cd lint && ./setup-hooks.sh  # One-time setup
pre-commit run --all-files    # Manual check
```

See [tests/README.md](./tests/README.md) and [lint/README.md](./lint/README.md) for details.

---

## 🛠️ Tools & Automation

### **Script Utilities**

| Script | Purpose | Usage |
|--------|---------|-------|
| `setup-project.sh` | Create new project with standards | `./scripts/setup-project.sh project-name` |
| `generate_standards_index.py` | Generate standards quick reference | `python3 scripts/generate_standards_index.py` |
| `fix_trailing_whitespace.sh` | Remove trailing whitespace | `./scripts/fix_trailing_whitespace.sh` |
| `test_redundancy.py` | Check for DRY violations | `python3 tests/test_redundancy.py` |
| `generate-badges.sh` | Generate compliance badges | `./scripts/generate-badges.sh` |

### **VS Code Extension**

Install our NIST compliance extension for real-time control suggestions:

```bash
# Install the extension
cd .vscode/nist-extension
npm install
npm run compile

# Link to VS Code (development mode)
ln -s $(pwd) ~/.vscode/extensions/nist-compliance-helper
```

**Features:**

- 🎯 Real-time NIST control suggestions while coding
- 📝 Code snippets for common security patterns
- 🔍 Hover information for control details
- ⚡ Quick fixes for missing controls
- 🏷️ Auto-completion for @nist tags

### **GitHub Actions Workflows**

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `standards-compliance.yml` | Push/PR | Validate standards compliance |
| `nist-compliance.yml` | Push/PR | Check NIST control coverage |
| `standards-validation.yml` | Push/PR | Run comprehensive validation tests |
| `redundancy-check.yml` | Push/PR | Detect code redundancy |
| `auto-fix-whitespace.yml` | Push | Auto-fix trailing whitespace |
| `auto-summaries.yml` | Schedule | Generate periodic summaries |

📖 **See [GITHUB_WORKFLOWS.md](./docs/core/GITHUB_WORKFLOWS.md) for detailed workflow documentation**

### **Compliance Automation Platform**

Our TypeScript-based compliance platform in `standards/compliance/` provides:

- **OSCAL Processing**: Import/export NIST controls in OSCAL format
- **Multi-Language Parsers**: Extract controls from Python, Go, JS/TS, Java, YAML
- **Evidence Collection**: Automated evidence harvesting for assessments
- **SSP Generation**: Create System Security Plans from code annotations
- **Knowledge Graphs**: Semantic analysis of control relationships

**Quick Start:**

```bash
cd standards/compliance
./quickstart.sh
```

### **Micro Standards**

Ultra-condensed versions (500 tokens) for token-efficient LLM usage:

```bash
# Access micro standards directly
cat micro/CS-api.micro.md     # API standards
cat micro/SEC-auth.micro.md   # Auth standards
cat micro/TS-unit.micro.md    # Unit testing
```

### **Standards API**

Remote access patterns defined in `config/standards-api.json`:

```javascript
// Fetch specific rules
@fetch-rule CS:api#rate-limiting

// Get examples
@fetch-example SEC:auth#jwt-implementation

// Search standards
@search "authentication patterns"
```

### **Test Infrastructure**

Comprehensive validation suite in `tests/`:

- `validate_cross_references.py` - Verify all links and references
- `validate_token_efficiency.py` - Check token optimization
- `fix_validation_issues.py` - Auto-fix common issues
- `validate_knowledge_management.sh` - Run all tests

### **Linting Tools**

Custom linting in `lint/`:

- `standards-linter.py` - Enforce standards format
- `custom-rules.js` - Project-specific rules
- Pre-commit hooks for automatic checking

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details. Free to use in personal and commercial projects.

---

**Remember**: These are living documents. Use them as a foundation but always consider your specific context and requirements.

*Happy coding! 🚀*

## Catalog (auto)

<!-- AUTO-LINKS:badges/** -->

- [standards-compliance-template](badges/standards-compliance-template.md)

<!-- /AUTO-LINKS -->
<!-- AUTO-LINKS:badges/**/*.md -->

- [Readme](badges/README.md)
- [Standards Compliance Template](badges/standards-compliance-template.md)

<!-- /AUTO-LINKS -->
