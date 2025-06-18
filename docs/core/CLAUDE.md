# CLAUDE.md - Advanced LLM-Optimized Project Standards Router

**Purpose:** Next-generation LLM interface for comprehensive standards management
**Token Efficiency:** ~90% reduction with intelligent context management
**Version:** 3.0.0
**Last Updated:** January 2025

> 🚀 **New:** Use [KICKSTART_PROMPT.md](./docs/guides/KICKSTART_PROMPT.md) for instant project analysis and implementation guidance!

---

## 🧠 Intelligent Context System

### Auto-Detection
```yaml
context:
  detect: [language, framework, project-type]
  analyze: [recent-files, commit-history, dependencies]
  suggest: [relevant-standards, improvements, next-steps]
```

### Context-Aware Loading
```
@load context:[auto] + history:[recent] + related:[graph-expansion]
```

---

## 📚 Enhanced Standards Library

### Smart Loading Syntax
```
# Basic Loading
@load CS:api                    # Single section
@load [CS:* + TS:* + SEC:*]    # Multiple standards
@load KM:*                      # Knowledge management architecture

# Advanced Loading
@load CS:api version:[latest] expand:[dependencies]
@load context:[react-app] auto:[true]
@load similar-to:[example-project] adapt:[team-size]

# Semantic Loading
@ask "How to build secure API" → auto-loads relevant standards
@need "performance optimization" → loads performance toolkit
@ask "how to organize docs" → loads KM:architecture + examples
```

### Natural Language Mappings
| Query | Standards Loaded | Context |
|-------|------------------|---------|
| "How to start NIST compliance?" | `NIG:quick-start` | Setup guide |
| "NIST tag examples" | `NIG:tagging-reference` | Code examples |
| "Check my NIST tags" | `NIG:workflow` | Validation |
| "NIST CI/CD setup" | `NIG:workflow` | Automation |
| "NIST implementation guide" | `NIG:* + COMPLIANCE:overview` | Full guide |
| "How do I build a secure API?" | `CS:api + SEC:api + TS:integration` | API security patterns |
| "Make my app faster" | `CS:performance + OBS:metrics + COST:optimization` | Performance toolkit |
| "Start React project" | `FE:react + WD:* + TS:jest + CS:javascript` | React ecosystem |
| "Database optimization" | `CS:performance + DE:optimization + OBS:metrics` | Query optimization |
| "Data engineering" | `DE:* + CS:patterns + OBS:monitoring` | Data pipelines |
| "Unified overview" | `UNIFIED:* + CS:overview + TS:overview` | Quick reference |
| "All standards overview" | `UNIFIED:comprehensive` | Complete reference |
| "Microservices setup" | `CN:microservices + EVT:* + OBS:distributed` | Distributed systems |
| "CI/CD pipeline" | `DOP:cicd + GH:actions + TS:*` | Automation setup |
| "GDPR compliance" | `LEG:privacy + SEC:encryption + CS:audit` | Privacy focus |
| "NIST compliance" | `COMPLIANCE:* + nist:moderate + evidence:patterns` | NIST 800-53r5 |
| "Tag NIST controls" | `COMPLIANCE:tagging + nist:quick-ref` | Control tagging |
| "Mobile app standards" | `FE:mobile + SEC:mobile + TS:mobile` | Cross-platform |
| "Documentation system" | `KM:* + CS:documentation + DOP:automation` | Knowledge management |
| "Organize standards" | `KM:architecture + KM:cross-reference` | Standards architecture |
| "Project management" | `PM:* + GH:projects + CONT:*` | Project organization |
| "Content strategy" | `CONT:* + SEO:content + WD:content` | Content management |
| "SEO optimization" | `SEO:* + FE:performance + WD:*` | Search optimization |
| "Tool selection" | `TOOL:* + CS:tools + SEC:tools` | Toolchain guidance |
| "Cost management" | `COST:* + CN:optimization + OBS:metrics` | Cost optimization |
| "Testing strategy" | `TS:* + CS:testing + SEC:security` | Testing practices |
| "Monitoring setup" | `OBS:* + CN:kubernetes + DOP:sre` | Observability |
| "UX design" | `WD:* + FE:accessibility + SEO:technical` | Design standards |
| "Event architecture" | `EVT:* + CN:microservices + OBS:tracing` | Event-driven |
| "Security audit" | `SEC:* + TS:security + LEG:compliance` | Security review |
| "Legal compliance" | `LEG:* + SEC:privacy + CONT:governance` | Compliance |
| "GitHub best practices" | `GH:* + DOP:cicd + SEC:github` | GitHub usage |

### Tool Selection Queries
| Query | Tools Loaded | Purpose |
|-------|--------------|---------|
| "Setup Python project" | `tools:[python:required]` | Essential Python tools |
| "Add security scanning" | `tools:[security:*]` | All security tools |
| "Modern JS toolchain" | `tools:[javascript:recommended]` | Recommended JS tools |
| "Migrate from flake8" | `tools:[python:ruff] + migration:[flake8→ruff]` | Tool migration |
| "Container security" | `tools:[container:scanning + security:container]` | Container tools |

---

## 🎯 Intelligent Task Routing

### Task-Based Loading 2.0
```yaml
bug_fix:
  load: [TS:regression + CS:error-handling]
  suggest: [root-cause-analysis, test-patterns]
  validate: [fix-completeness, regression-prevention]

new_feature:
  load: [CS:architecture + TS:tdd + SEC:relevant]
  generate: [boilerplate, tests, documentation]
  check: [standards-compliance, coverage]
  nist_tag: [auto-suggest, validate-controls]

security_feature:
  load: [SEC:* + COMPLIANCE:tagging + nist:moderate]
  suggest: [nist-controls, implementation-patterns]
  generate: [tagged-code, evidence-templates]
  validate: [control-coverage, evidence-quality]

performance:
  load: [CS:performance + OBS:metrics + COST:*]
  analyze: [bottlenecks, cost-drivers]
  optimize: [code, infrastructure, queries]

compliance_check:
  load: [COMPLIANCE:* + nist:all + evidence:patterns]
  analyze: [control-coverage, implementation-gaps]
  generate: [ssp, assessment-results, evidence-inventory]
  suggest: [missing-controls, remediation-steps]

quick_reference:
  load: [UNIFIED:overview + CS:patterns + TS:best-practices]
  suggest: [common-patterns, quick-wins]
  validate: [standards-compliance]
```

---

## 🤖 AI-Powered Features

### Compliance Assistant
```
@analyze [code] → compliance-report
@fix [violations] → automated-fixes
@suggest [improvements] → enhancement-plan
@validate [changes] → real-time-feedback
```

### Code Generation
```
@generate [component] following:[standards] with:[patterns]
@create [test-suite] covering:[requirements] style:[team-preference]
@scaffold [project] using:[standards + templates]
```

### Interactive Validation
```
@validate live:[true] show:[inline-hints] fix:[auto-safe]
@check pr:[url] comment:[violations] suggest:[fixes]
```

---

## 📊 Standards Intelligence

### Relationship Graph
```
@show dependencies for:[CS:api]
@find related to:[SEC:auth]
@suggest path from:[current] to:[target-maturity]
```

### Version Management
```
@load CS:api version:[latest]
@migrate from:[old] to:[new] generate:[migration-script]
@diff versions:[previous...latest] impact:[current-project]

# Version info now in MANIFEST.yaml under 'versioning' section
@check versions in:[MANIFEST.yaml#versioning]
```

### Learning Paths
```
@show progression for:[testing-maturity]
@recommend next:[based-on-current-usage]
@generate training:[personalized-plan]
```

---

## 🔧 Advanced Operations

### Multi-Modal Support
```
@visualize architecture:[current] highlight:[violations]
@generate diagram:[component-relationships] style:[mermaid]
@explain standard:[CS:patterns] format:[interactive-tutorial]
```

### Batch Operations
```
@fix-all type:[docstring] style:[google] preview:[true]
@update standards:[CS:previous→latest] project-wide:[true]
@enforce standards:[critical-only] auto-fix:[true]
```

### Custom Workflows
```
@define workflow:[pre-release]
  - validate:[SEC:* + TS:coverage]
  - generate:[changelog, release-notes]
  - check:[breaking-changes]
  - notify:[stakeholders]
```

---

## 💡 Contextual Templates

### Smart Templates
```
@template [api-endpoint] context:[fastapi + auth + postgres]
@template [react-component] patterns:[hooks + testing + accessibility]
@template [data-pipeline] style:[airflow + dbt + quality-checks]
```

### Adaptive Examples
```
@example [error-handling] for:[current-language] level:[team-expertise]
@show [best-practice] adapted-to:[project-patterns]
```

---

## 🔍 Semantic Search

### Natural Queries
```
"How to handle errors properly" → CS:error-handling + examples
"Security best practices" → SEC:* prioritized by relevance
"Make code faster" → CS:performance + OBS:profiling + patterns
```

### Smart Suggestions
```
Based on your current file:
- Consider adding: [error-handling]
- Related standard: [SEC:validation]
- Similar pattern in: [other-module]
```

---

## 📈 Analytics and Insights

### Compliance Tracking
```
@report compliance:[current] trend:[30-days] gaps:[highlighted]
@track adoption:[team] standards:[all] frequency:[weekly]
```

### Usage Analytics
```
Most used standards: [CS:api, TS:unit, SEC:auth]
Compliance score: 87% (+5% this month)
Top violations: [missing-docstrings, test-coverage]
```

---

## 🚀 Quick Actions

### One-Line Commands
| Command | Action |
|---------|--------|
| `@quick security-check` | Run security validation |
| `@quick setup-project` | Initialize with standards |
| `@quick fix-style` | Auto-fix style issues |
| `@quick generate-tests` | Create test suite |
| `@quick check-compliance` | Full compliance report |

---

## 🔧 Tool Management

### Tool Selection
```
@load tools:[language:level] → Load tools by recommendation level
@suggest tools:[category] → Get tool recommendations
@compare tools:[tool1 vs tool2] → Compare tool options
@migrate tools:[old→new] → Get migration guide
```

### Tool Catalog Access
```
@show tools:[python:all] → List all Python tools
@show tools:[required] → Show all required tools
@show tools:[security:recommended] → Recommended security tools
@check tool:[name] → Check tool details and version
```

### Tool Configuration
```
@generate config:[black + ruff + mypy] → Generate tool configs
@setup toolchain:[python + recommended] → Complete setup
@validate tools:[current] → Check tool compliance
```

### Examples
```
# Setup new Python project with modern tools
@load tools:[python:required + python:recommended]
@generate config:[all] in:[pyproject.toml]

# Migrate from legacy tools
@migrate tools:[flake8→ruff + pylint→ruff]
@show migration:[step-by-step]

# Security audit toolchain
@load tools:[security:required]
@generate workflow:[security-scanning]
```

---

## 🧩 Integration Patterns

### IDE Integration
```
@integrate with:[vscode|intellij|vim]
@configure realtime:[validation + hints + fixes]
@sync settings:[team-wide]
```

### CI/CD Integration
```
@generate workflow:[github-actions|gitlab-ci|jenkins]
@configure gates:[quality + security + coverage]
@report to:[slack|email|dashboard]
```

---

## 🔐 Security-First Defaults

### Automatic Security
```
When loading any standard:
- Include relevant security sections
- Validate against OWASP Top 10
- Check for exposed secrets
- Suggest security improvements
```

---

## 💾 Cache Management

### Smart Caching Directives
```
# Cache for session
@cache standards:[CS:api, SEC:auth] duration:[session]
@cache frequently-used:[CS:*, TS:unit] duration:[24h]

# Preload common patterns
@preload common:[bug_fix, new_feature, security_review]
@preload based-on:[project-type] auto:[true]

# Cache control
@cache-status  # Show cached standards and expiry
@cache-clear [specific-standard]  # Clear specific cache
@cache-refresh  # Update all cached standards
```

### Conditional Loading
```
@if-cached CS:api use:[cache] else:[@load CS:api]
@fetch-if-modified CS:api since:[last-check]
@use-cached-or-micro CS:api  # Use cache, fallback to micro
```

---

## 🚀 Lazy Loading Syntax

### Progressive Loading
```
@peek CS:api  # First 100 tokens preview
@summary CS:api  # AI-generated summary
@toc CS:api  # Table of contents only
@stats CS:api  # Size, sections, last updated
```

### Section-Based Loading
```
@lazy-load CS:api sections:[overview]  # Start minimal
@expand CS:api add:[patterns]  # Add more sections
@load-on-demand CS:api  # Load sections as referenced
```

### Smart Chunking
```
@chunk CS:api size:[1000-tokens]  # Load in chunks
@stream CS:api  # Progressive streaming
@load CS:api until:[token-limit:5000]  # Stop at limit
```

---

## 🔍 Real-Time Validation

### Remote Validation Endpoints
```
@validate-remote code:[snippet] against:[CS:python]
@check-remote url:[github.com/user/repo] standards:[SEC:*]
@lint-remote file:[path] rules:[CS:style + TS:coverage]

# Remote access patterns now in standards-api.json
@see standards-api.json#direct_access
```

### Live Validation
```
@validate-live enabled:[true] standards:[current-context]
@auto-fix-remote violations:[safe-only]
@suggest-fixes show:[inline] confidence:[high]
```

---

## 📝 Memory and Learning

### Session Context
```
@remember preferences:[style, patterns, standards]
@learn from:[corrections, choices, feedback]
@adapt to:[team-conventions, project-patterns]
```

### Cross-Reference Learning
```
When you use: [pattern-A]
Also consider: [related-pattern-B]
Teams like yours use: [pattern-C]
```

---

## 📋 Compliance Automation

### NIST 800-53r5 Control Tagging

When asked about NIST compliance, automatically load:
```
@load NIST_IMPLEMENTATION_GUIDE.md + COMPLIANCE_STANDARDS.md + context:[nist-moderate]
```

Quick commands:
- `@nist suggest` - Get control suggestions for current code
- `@nist validate` - Check existing tags
- `@nist implement [control]` - Get implementation guidance
- `@nist quickstart` - Load implementation guide
- `@nist coverage report:[by-family|by-control|gaps]`
- `@nist generate ssp:[auto-collect-evidence]`

See [NIST_IMPLEMENTATION_GUIDE.md](./docs/nist/NIST_IMPLEMENTATION_GUIDE.md) for the complete quick start.

### Automated NIST Tagging
When writing security-related code, automatically suggest NIST controls:
```
# Quick Reference
Authentication → @nist ia-2, ia-5
Authorization → @nist ac-2, ac-3, ac-6  
Encryption → @nist sc-8, sc-13
Logging → @nist au-2, au-3
Session management → @nist ac-12
Error handling → @nist si-11

# Format
@nist <control-id> "<brief description>"
```

### Control Context Loading
```
@load compliance:nist-moderate  # Load moderate baseline controls
@load nist:[ac-* + ia-* + sc-*]  # Load specific families
@load evidence:[code + config + test]  # Load evidence patterns
@load NIST_IMPLEMENTATION_GUIDE.md  # Load quick start guide
```

### Automated Analysis
```
@analyze [codebase] against:[standards] output:[report|suggestions|fixes]
@audit [pull-request] using:[CS:* + TS:* + SEC:*] flag:[violations|improvements]
@suggest improvements for:[file|module] based-on:[relevant-standards]
```

### Fix Generation
```
@fix [violation-type] in:[code-context] following:[standard-section]
@fix-all [violation-type] in:[directory|project]
@generate migration-script from:[old-standard] to:[new-standard]
```

### CI/CD Integration
```
@validate pull-request:[PR-URL]
@comment violations on:[specific-lines]
@block commit if:[critical-violations]
```

---

## ⚡ Quick Reference (No Loading Required)

### Instant Answers
| Question | Answer | Reference |
|----------|---------|-----------|
| "Python naming?" | `snake_case` functions, `PascalCase` classes | CS:python |
| "Test coverage?" | 85% overall, 95% critical, 90% new code | TS:coverage |
| "Password rules?" | Min 12 chars, mixed case/numbers/symbols | SEC:auth |
| "JWT expiry?" | Access: 1 hour, Refresh: 7 days | SEC:auth |
| "API versioning?" | URL path: `/api/v1/`, `/api/v2/` | CS:api |

### Quick Numbers
- Max function: 50 lines
- Max file: 500 lines
- Session timeout: 30 min activity
- API rate limit: 1000 req/hour/user
- Log retention: 30 days minimum

---

## 🎓 Advanced Prompt Engineering

### Chain-of-Thought Pattern
```
Task: [DESCRIPTION]
1. Identify context → @load smart:[context-aware]
2. Analyze requirements → Required: [list], Recommended: [list]
3. Generate solution → Following: [standards], Validating: [real-time]
```

### Few-Shot Learning
```
Example 1: Auth endpoint → @load [CS:api + SEC:auth]
Example 2: Data endpoint → @load [CS:api + LEG:privacy]
Your task: [REQUIREMENT] → Applying patterns...
```

### Progressive Refinement
```
Initial: @generate based-on:[requirements]
+ "Add auth" → @enhance with:[SEC:auth]
+ "Optimize" → @optimize using:[CS:performance]
```

---

**Token Optimization:** Advanced features with only ~10% token increase over v2.0

---

## 📝 Contributing New Standards

To create new standards that integrate with this system:
1. Use [STANDARD_TEMPLATE.md](./docs/guides/STANDARD_TEMPLATE.md) as your starting point
2. Follow [CREATING_STANDARDS_GUIDE.md](./docs/guides/CREATING_STANDARDS_GUIDE.md) for integration
3. Update this file with new loading patterns and mappings

## Related Standards

- [Knowledge Management Standards](./docs/standards/KNOWLEDGE_MANAGEMENT_STANDARDS.md) - Core architecture principles
- [Compliance Standards](./docs/standards/COMPLIANCE_STANDARDS.md) - NIST 800-53r5 control tagging guidelines
