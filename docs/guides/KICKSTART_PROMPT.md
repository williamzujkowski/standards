# Universal Project Kickstart Prompt

Copy this prompt into any web-based LLM chat (ChatGPT, Claude, Gemini, etc.) along with your project_plan.md content.

---

## 🚀 Project Kickstart Assistant

I need help implementing a project based on my project plan. I'll provide the plan content below, and I'd like you to:

### 1. **Analyze & Identify** (Auto-Detection)
- Detect the project type, tech stack, and languages
- Identify frameworks, databases, and infrastructure needs
- Recognize architectural patterns and deployment targets
- Note any compliance or security requirements

### 2. **Standards Mapping** (From: https://github.com/williamzujkowski/standards)
> 💡 **Note**: For creating new standards, see [CREATING_STANDARDS_GUIDE.md](https://github.com/williamzujkowski/standards/blob/master/CREATING_STANDARDS_GUIDE.md)

#### Using the Standards Router (CLAUDE.md) & Product Matrix
After Tech Stack Analysis, the router at `CLAUDE.md` resolves bundles from `config/product-matrix.yaml`:

```
@load [product:api + CS:python + TS:pytest]  # API service with Python
@load [product:frontend-web + FE:react]       # React SPA
@load [CS:python + TS:pytest + SEC:*]         # Python with all security standards
```

The router (`CLAUDE.md` at repository root) provides:
- **Fast Path Loading**: Reads `config/product-matrix.yaml` for product mappings
- **Wildcard Expansion**: `SEC:*` expands to all security standards + NIST-IG:base
- **Language Detection**: Auto-maps CS/TS to language-specific implementations
- **NIST Auto-Inclusion**: Security standards automatically include compliance

See [USING_PRODUCT_MATRIX.md](./USING_PRODUCT_MATRIX.md) for detailed examples.

Based on the detected technologies, recommend relevant standards:
- **Code Standards (CS):** Language-specific best practices
- **Testing Standards (TS):** Testing frameworks and coverage requirements
- **Security Standards (SEC):** Security patterns and authentication
- **Frontend/Backend (FE/WD):** UI/UX and API standards
- **Infrastructure (CN/DOP):** Container and deployment standards
- **Data Engineering (DE):** Database and data pipeline standards
- **Legal/Compliance (LEG):** Privacy and regulatory requirements
- **NIST Compliance (NIST-IG):** NIST 800-53r5 control tagging ([NIST_IMPLEMENTATION_GUIDE.md](https://github.com/williamzujkowski/standards/blob/master/NIST_IMPLEMENTATION_GUIDE.md))

### 3. **Implementation Blueprint**
Create a structured implementation plan with:
- Project scaffold/boilerplate structure
- Core dependencies and toolchain setup
- Development workflow (git flow, CI/CD)
- Testing strategy and coverage targets
- Security checklist and authentication approach
- Compliance requirements (NIST controls for security features)
- Deployment pipeline and monitoring

### 4. **Code Generation**
Provide starter code for:
- Project configuration files (package.json, pyproject.toml, etc.)
- CI/CD pipeline configuration
- Docker/container setup if applicable
- Basic application skeleton following identified standards
- Testing setup and example tests
- Security configurations and middleware

### 5. **Quality Gates**
Define automated checks for:
- Code style and linting rules
- Test coverage thresholds
- Security scanning requirements
- Performance benchmarks
- Documentation standards

### 6. **Tool Recommendations**
Suggest modern tools for:
- **Required:** Essential tools for the detected stack
- **Recommended:** Tools that enhance developer experience
- **Optional:** Nice-to-have tools for advanced workflows

---

## My Project Plan:

[PASTE YOUR PROJECT_PLAN.MD CONTENT HERE]

---

## Additional Context (Optional):
- Team size: [small/medium/large]
- Experience level: [beginner/intermediate/expert]
- Timeline: [MVP/short-term/long-term]
- Special requirements: [compliance/performance/scale]

---

## Expected Output Format:

1. **Tech Stack Analysis**
   ```yaml
   detected:
     languages: [...]
     frameworks: [...]
     databases: [...]
     infrastructure: [...]
   ```

2. **Standards Recommendations**
   ```
   Essential Standards:
   - CS:[language] - Core language patterns
   - TS:[framework] - Testing approach
   - SEC:[relevant] - Security requirements

   Recommended Standards:
   - FE/WD:[as-applicable]
   - DOP:[deployment]
   - OBS:[monitoring]
   ```

3. **Project Structure**
   ```
   project-root/
   ├── src/
   ├── tests/
   ├── docs/
   └── [configuration files]
   ```

4. **Quick Start Commands**
   ```bash
   # Initialize project
   # Install dependencies
   # Run tests
   # Start development
   ```

5. **Implementation Checklist**
   - [ ] Project setup and structure
   - [ ] Core functionality implementation
   - [ ] Testing framework and initial tests
   - [ ] Security measures
   - [ ] CI/CD pipeline
   - [ ] Documentation
   - [ ] Deployment configuration

---

Please analyze my project plan and provide comprehensive implementation guidance following the standards repository approach.

## Related Standards

- [CLAUDE.md](../../CLAUDE.md) - The main LLM router that references this prompt
- [KICKSTART_ADVANCED.md](KICKSTART_ADVANCED.md) - Advanced kickstart features
