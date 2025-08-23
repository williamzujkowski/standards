# Examples Directory

This directory contains practical implementation patterns, templates, and examples that demonstrate how to apply the standards defined in this repository.

## 📂 Directory Structure

```
examples/
├── ai-generation-hints/     # Templates for AI code generation
│   ├── python-hints.py      # Python templates and patterns
│   └── typescript-hints.ts  # TypeScript/React templates
├── project-templates/       # Project setup templates
│   ├── docker/              # Docker configuration templates
│   ├── go-project/          # Go project structure
│   ├── javascript-project/  # JavaScript/Node.js project setup
│   ├── kubernetes/          # Kubernetes manifests
│   ├── python-project/      # Python project structure
│   └── terraform/           # Infrastructure as Code templates
└── README.md               # This file
```

## 🤖 AI Generation Hints

The `ai-generation-hints` directory contains language-specific templates that serve as:

1. **Code Generation Templates** - Base patterns for AI assistants to follow
2. **Standards Examples** - Practical implementations of our standards
3. **Learning Resources** - Examples for developers to understand best practices

### Python Hints (`python-hints.py`)

Demonstrates:

- Result type pattern for error handling
- API endpoint templates with security
- Test generation templates
- Logging and audit patterns
- Type hints and documentation

Usage:

```
@generate python:[component] with:[CS:python + TS:pytest + SEC:*]
```

### TypeScript Hints (`typescript-hints.ts`)

Demonstrates:

- React component patterns with hooks
- TypeScript type safety
- API service with retry logic
- Custom React hooks
- Test templates for React Testing Library

Usage:

```
@generate typescript:[component] with:[FE:react + CS:typescript + TS:jest]
```

## 📁 Project Templates

The `project-templates` directory contains ready-to-use project configurations:

### Docker Templates

- `Dockerfile.standards` - Production-ready Dockerfile with security best practices
- `docker-compose.standards.yml` - Multi-service orchestration template

### Language-Specific Project Templates

#### Python Project

- `pyproject.toml` - Modern Python project configuration
- Includes: Black, isort, mypy, pytest configurations
- Poetry/pip-tools compatible

#### JavaScript Project

- `package.json` - Node.js project with ESLint, Prettier, Jest
- Scripts for linting, testing, and building
- TypeScript support ready

#### Go Project

- `Makefile` - Build, test, and deployment automation
- Follows Go module structure
- Includes linting and security scanning

### Infrastructure Templates

#### Kubernetes

- `deployment.standards.yaml` - Production-grade deployment manifest
- Includes: Resource limits, health checks, security contexts

#### Terraform

- `main.tf` - Infrastructure as Code template
- Follows Terraform best practices
- Includes provider configuration and state management

## 🎯 How to Use These Examples

### For AI Assistants

1. Reference these templates when generating code
2. Follow the patterns for consistency
3. Apply the relevant standards annotations
4. Use the Result type pattern for error handling

### For Developers

1. Copy project templates to bootstrap new projects:

   ```bash
   # Python project
   cp -r examples/project-templates/python-project/* my-new-project/

   # JavaScript project
   cp -r examples/project-templates/javascript-project/* my-new-project/

   # Go project
   cp -r examples/project-templates/go-project/* my-new-project/
   ```

2. Use AI generation hints as reference for code patterns
3. Follow the documentation and testing patterns
4. Maintain the security and quality standards

### For DevOps/Infrastructure

1. Use Docker templates for containerization
2. Apply Kubernetes templates for deployments
3. Bootstrap infrastructure with Terraform templates
4. Customize based on your specific requirements

## 📝 Adding New Examples

When adding new examples:

1. Follow the existing directory structure
2. Include comprehensive documentation
3. Add AI instruction comments where applicable
4. Demonstrate multiple standards in action
5. Include test examples where relevant
6. Update this README with descriptions

## 🔗 Related Documentation

- [CLAUDE.md](../docs/core/CLAUDE.md) - Primary AI interface and standards router
- [VALIDATION_PATTERNS.md](../docs/guides/VALIDATION_PATTERNS.md) - Validation examples
- [STANDARDS_INDEX.md](../docs/guides/STANDARDS_INDEX.md) - Quick reference index
- [README.md](../README.md) - Main repository documentation

## 💡 Quick Tips

1. **Project Setup**: Start with the appropriate project template
2. **Code Generation**: Use AI hints for consistent patterns
3. **Standards Compliance**: Reference the validation patterns
4. **Documentation**: Follow the examples for clear documentation
5. **Testing**: Use the test templates for comprehensive coverage

## Catalog (auto)

<!-- AUTO-LINKS:examples/** -->

- [project_plan_example](project_plan_example.md)

<!-- /AUTO-LINKS -->
<!-- AUTO-LINKS:examples/**/*.md -->

- [Readme](ai-generation-hints/README.md)
- [Readme](nist-templates/README.md)
- [Readme](nist-templates/go/README.md)
- [Readme](nist-templates/python/README.md)
- [Readme](nist-templates/quickstart/.pytest_cache/README.md)
- [Readme](nist-templates/quickstart/README.md)
- [Readme](nist-templates/typescript/README.md)
- [Readme](project-templates/README.md)
- [Readme](project-templates/docker/README.md)
- [Readme](project-templates/go-project/README.md)
- [Readme](project-templates/javascript-project/README.md)
- [Readme](project-templates/kubernetes/README.md)
- [Readme](project-templates/python-project/README.md)
- [Readme](project-templates/terraform/README.md)
- [Project Plan Example](project_plan_example.md)

<!-- /AUTO-LINKS -->


<!-- AUTO-LINKS:examples/*.md -->

- [Project Plan Example](project_plan_example.md)

<!-- /AUTO-LINKS -->
