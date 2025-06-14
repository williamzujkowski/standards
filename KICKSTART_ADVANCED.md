# Advanced Kickstart Guide

## 🎯 Enhanced Usage Patterns

### Using with URLs
If your project_plan.md is hosted online:
```
Instead of pasting content, use:
"Please fetch and analyze this project plan: [URL]"

Supported platforms:
- GitHub (raw.githubusercontent.com)
- GitLab (gitlab.com/.../raw/)
- Gist (gist.github.com)
- Pastebin (pastebin.com/raw/)
```

### Multi-Stage Approach
For complex projects, break down the analysis:

```
Stage 1: "Focus on backend architecture and API design"
Stage 2: "Now detail the frontend implementation"
Stage 3: "Design the data pipeline and analytics"
Stage 4: "Create the deployment and monitoring strategy"
```

### Technology-Specific Prompts

#### For Python Projects
```
Additional context for Python project:
- Async/sync preference: [asyncio/traditional]
- Framework preference: [FastAPI/Django/Flask]
- Package manager: [poetry/pip/conda]
- Python version: [3.11+/3.9+]
```

#### For JavaScript/TypeScript Projects
```
Additional context for JS/TS project:
- Runtime: [Node.js/Deno/Bun]
- Framework: [React/Vue/Angular/Svelte]
- Build tool: [Vite/Webpack/esbuild]
- Package manager: [npm/yarn/pnpm]
```

#### For Go Projects
```
Additional context for Go project:
- Web framework: [Gin/Echo/Fiber/stdlib]
- Module layout: [flat/domain/clean]
- Concurrency needs: [high/moderate/low]
```

### Standards Integration Patterns

#### Direct Standards Reference
```
"Apply these specific standards from the repo:
- CS:python#error-handling
- SEC:api#authentication
- TS:pytest#fixtures
- DOP:cicd#github-actions"
```

#### Compliance Focus
```
"Ensure compliance with:
- OWASP Top 10 for security
- 12-factor app principles
- GDPR for data handling
- SOC2 for infrastructure"
```

### Output Customization

#### Minimal Setup
```
"Provide only:
1. Essential project structure
2. Core dependencies
3. Single 'make start' command"
```

#### Comprehensive Setup
```
"Include:
1. Full project scaffold with all directories
2. All configuration files with comments
3. Complete CI/CD pipeline
4. Monitoring and alerting setup
5. Deployment scripts for multiple environments"
```

### Example Interactions

#### Example 1: SaaS API Project
```
Input: "Project plan describes a multi-tenant SaaS API with Stripe integration"

Expected Analysis:
- Detects: REST API, payment processing, multi-tenancy
- Suggests: CS:api, SEC:payments, LEG:pci, DE:multi-tenant
- Provides: JWT auth setup, Stripe webhook handling, tenant isolation
```

#### Example 2: Data Pipeline Project
```
Input: "Project plan for real-time analytics pipeline with ML models"

Expected Analysis:
- Detects: Streaming data, ML pipeline, analytics
- Suggests: DE:streaming, CS:python, OBS:metrics, CN:kubernetes
- Provides: Kafka setup, model serving, monitoring dashboard
```

#### Example 3: Mobile App Backend
```
Input: "Project plan for mobile app backend with offline sync"

Expected Analysis:
- Detects: Mobile backend, sync requirements, API gateway
- Suggests: CS:api, SEC:mobile, DE:sync, CN:edge
- Provides: Sync protocol, conflict resolution, push notifications
```

### Troubleshooting Common Issues

#### If LLM Misidentifies Stack
```
"Correction: This is specifically a [Python/FastAPI] project, not [Node.js]"
```

#### If Missing Key Requirements
```
"Also include:
- GraphQL API setup
- WebSocket support
- Background job processing"
```

#### If Standards Not Recognized
```
"Reference standards from: https://github.com/williamzujkowski/standards
Specifically look at:
- standards/code-standards/
- standards/testing-standards/
- standards/security-standards/"
```

### Advanced Patterns

#### Microservices Decomposition
```
"Analyze as microservices:
- Identify service boundaries
- Define inter-service communication
- Create separate standards per service
- Design shared libraries approach"
```

#### Migration Projects
```
"This is a migration from [old-stack] to [new-stack]:
- Identify migration phases
- Maintain backward compatibility
- Create transition standards
- Define rollback procedures"
```

#### Hybrid Architectures
```
"Project uses multiple languages:
- Python for API (FastAPI)
- Go for high-performance services
- TypeScript for frontend
- Rust for critical paths

Apply language-specific standards to each component"
```

### Integration with Development Workflow

#### Pre-Implementation Review
```
"Before I start coding:
1. Validate the architecture against standards
2. Identify potential security risks
3. Suggest performance optimizations
4. Recommend monitoring points"
```

#### Post-Implementation Audit
```
"Review this implementation against:
1. Suggested standards compliance
2. Security best practices
3. Performance benchmarks
4. Test coverage requirements"
```

### Custom Templates

#### Startup Template
```
"Use startup-optimized approach:
- Minimal viable architecture
- Quick deployment pipeline
- Basic monitoring only
- Focus on iteration speed"
```

#### Enterprise Template
```
"Use enterprise approach:
- Full compliance checking
- Comprehensive audit trails
- Multi-environment setup
- Disaster recovery plans"
```

### Performance Optimization Hints

#### For Large Project Plans
```
"Summary first: Provide high-level analysis before details"
"Chunked response: Break into logical sections"
"Priority order: Start with critical path items"
```

#### For Quick Iterations
```
"Rapid mode: Skip explanations, provide code only"
"Copy-paste ready: All code in executable blocks"
"Single-file mode: Consolidate configs where possible"
```

---

## 🚀 Quick Reference Card

### Most Effective Prompts
1. **Clear Stack**: "Python/FastAPI REST API with PostgreSQL"
2. **Clear Requirements**: "Must include JWT auth and rate limiting"
3. **Clear Timeline**: "MVP in 2 weeks, full launch in 2 months"
4. **Clear Constraints**: "Must run on AWS Lambda"

### Power User Commands
- `"Skip boilerplate explanations"` - Get straight to code
- `"Include error handling examples"` - See edge cases
- `"Show alternative approaches"` - Compare options
- `"Optimize for [metric]"` - Focus on specific goals

### Standards Cheat Sheet
```
Always request:
- CS:[language] - Code standards
- TS:[testing] - Test requirements
- SEC:[relevant] - Security measures
- DOP:cicd - Deployment pipeline

Often useful:
- OBS:* - Monitoring/observability
- LEG:* - Compliance requirements
- COST:* - Cost optimization
- EVT:* - Event-driven patterns
```

---

Remember: The more specific your project plan and requirements, the more tailored and actionable the implementation guide will be!

## Related Standards

- [KICKSTART_PROMPT.md](./KICKSTART_PROMPT.md) - The basic kickstart prompt that references this guide