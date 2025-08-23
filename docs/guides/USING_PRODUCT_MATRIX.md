# Using the Product Matrix for Standards Auto-Loading

**Version:** 1.0.0  
**Last Updated:** 2025-08-23

## Overview

The Product Matrix (`config/product-matrix.yaml`) provides intelligent mapping from product types to curated bundles of development standards. This enables automatic loading of relevant standards based on your project type.

## Quick Start

### 1. Identify Your Product Type

```yaml
Available Product Types:
- web-service       # Full-stack web application
- api              # REST/GraphQL API service  
- cli              # Command-line tool
- frontend-web     # SPA/MPA web application
- mobile           # iOS/Android app
- data-pipeline    # ETL/ELT workflow
- ml-service       # ML training/inference
- infra-module     # IaC module
- documentation-site # Technical docs
- compliance-artifacts # Security docs
```

### 2. Load Standards Bundle

Use the `@load` directive in CLAUDE.md:

```
@load product:web-service
```

Or combine with specific overrides:

```
@load [product:api + CS:python + TS:pytest]
```

## Worked Examples

### Example 1: Python FastAPI Service

**Scenario:** Building a REST API with FastAPI, PostgreSQL, and Docker.

**Product Type Detection:**
```yaml
Detected: api
Language: python
Framework: fastapi
Database: postgresql
Infrastructure: docker
```

**Standards Loading:**
```
@load [product:api + CS:python + TS:pytest + DB:postgresql + CN:docker]
```

**Resolved Standards:**
- **CS:python** - Python coding standards (PEP 8, type hints)
- **TS:pytest** - Pytest testing framework
- **SEC:auth** - API authentication (OAuth2, JWT)
- **SEC:input-validation** - Input sanitization
- **DB:postgresql** - PostgreSQL best practices
- **CN:docker** - Container standards
- **DOP:ci-cd** - CI/CD pipeline
- **OBS:monitoring** - API monitoring
- **LEG:privacy** - GDPR/CCPA compliance
- **NIST-IG:base** - NIST 800-53r5 controls (auto-included with SEC)

**Implementation Steps:**
1. Project structure follows Python package conventions
2. FastAPI router organization per `CS:python`
3. Pytest fixtures and parametrized tests per `TS:pytest`
4. JWT authentication with refresh tokens per `SEC:auth`
5. Pydantic models for validation per `SEC:input-validation`
6. Docker multi-stage builds per `CN:docker`
7. GitHub Actions workflow per `DOP:ci-cd`
8. Prometheus metrics per `OBS:monitoring`
9. NIST control tags on security features per `NIST-IG:base`

### Example 2: React TypeScript Application

**Scenario:** Building a React SPA with TypeScript, Material-UI, and AWS deployment.

**Product Type Detection:**
```yaml
Detected: frontend-web
Language: typescript
Framework: react
UI Library: material-ui
Deployment: aws-s3-cloudfront
```

**Standards Loading:**
```
@load [product:frontend-web + FE:react + WD:material-design + DOP:aws]
```

**Resolved Standards:**
- **FE:react** - React component patterns
- **FE:design-system** - Design system architecture
- **FE:accessibility** - WCAG 2.1 AA compliance
- **CS:typescript** - TypeScript strict mode
- **TS:vitest** - Vitest + React Testing Library
- **WD:material-design** - Material Design principles
- **SEC:auth-ui** - Frontend authentication flow
- **DOP:aws** - AWS deployment patterns
- **DOP:ci-cd** - Build and deployment pipeline
- **OBS:web-vitals** - Core Web Vitals monitoring

**Implementation Steps:**
1. Component structure: `/components`, `/pages`, `/hooks`
2. TypeScript strict mode with no implicit any
3. Material-UI theming with custom palette
4. React Testing Library with user event simulation
5. Auth0/Cognito integration for authentication
6. Webpack optimization for code splitting
7. S3 + CloudFront with cache invalidation
8. Datadog RUM for performance monitoring

### Example 3: Data Pipeline with Airflow

**Scenario:** Building an ETL pipeline with Apache Airflow, handling PII data.

**Product Type Detection:**
```yaml
Detected: data-pipeline
Orchestrator: airflow
Data Sensitivity: pii
Storage: s3, redshift
Processing: spark
```

**Standards Loading:**
```
@load [product:data-pipeline + DE:airflow + SEC:data-classification + LEG:gdpr]
```

**Resolved Standards:**
- **DE:orchestration** - Airflow DAG best practices
- **DE:data-quality** - Data validation checks
- **DE:airflow** - Airflow-specific patterns
- **SEC:secrets** - AWS Secrets Manager integration
- **SEC:data-classification** - PII handling procedures
- **SEC:encryption** - Encryption at rest/in transit
- **DOP:ci-cd** - DAG deployment automation
- **OBS:logging** - Centralized logging
- **LEG:data-retention** - GDPR retention policies
- **LEG:gdpr** - GDPR compliance requirements
- **NIST-IG:base** - NIST privacy controls

**Implementation Steps:**
1. DAG structure: one DAG per data source
2. Idempotent tasks with proper retry logic
3. Data quality checks using Great Expectations
4. PII detection and masking utilities
5. Encryption using AWS KMS
6. Secrets rotation every 90 days
7. Audit logging to CloudWatch
8. Data retention: 7 years for financial, 3 years for behavioral
9. GDPR data subject request automation
10. NIST SC-13 for cryptographic protection

## Wildcard Expansion

### Security Wildcard (`SEC:*`)
```
@load [CS:python + SEC:*]
```
Expands to:
- SEC:auth
- SEC:secrets
- SEC:input-validation
- SEC:encryption
- SEC:audit
- NIST-IG:base (automatically included)

### Testing Wildcard (`TS:*`)
```
@load [CS:javascript + TS:*]
```
Expands to:
- TS:unit
- TS:integration
- TS:e2e
- TS:performance
- TS:security

## Language Auto-Detection

When a language is detected, the matrix automatically maps generic codes:

**Python Detection:**
- `CS` → `CS:python`
- `TS` → `TS:pytest`
- `TOOL` → `TOOL:python`

**TypeScript Detection:**
- `CS` → `CS:typescript`
- `TS` → `TS:vitest`
- `TOOL` → `TOOL:nodejs`

## Stack Presets

Quick presets for common technology stacks:

### MERN Stack
```
@load stack:mern
```
Loads: MongoDB, Express, React, Node.js standards

### JAMstack
```
@load stack:jamstack
```
Loads: Static site generation, CDN, API standards

## NIST Auto-Inclusion

When any security standard (`SEC:*`) is loaded, `NIST-IG:base` is automatically included. This ensures:

1. Security features get tagged with NIST controls
2. Compliance documentation is generated
3. Audit trails are properly configured
4. Security testing includes compliance checks

## Integration with CLAUDE.md

The router (CLAUDE.md) resolves these directives:

```markdown
# In your prompt to Claude:
@load [product:api + CS:python]

# Claude interprets this as:
- Load all standards for API product type
- Override with Python-specific coding standards
- Include NIST compliance (via SEC standards)
- Apply the combined bundle to the project
```

## Custom Combinations

Mix and match for unique requirements:

```
@load [product:web-service + FE:vue + DB:mongodb + DOP:kubernetes]
```

This loads web-service base standards but overrides:
- Frontend framework to Vue
- Database to MongoDB  
- Deployment to Kubernetes

## Validation

To verify your standards bundle:

```bash
# Check resolved standards
npx claude-flow standards resolve --product api --language python

# Validate against your project
npx claude-flow standards validate --path ./src
```

## See Also

- [Product Matrix Configuration](../../config/product-matrix.yaml)
- [KICKSTART_PROMPT.md](./KICKSTART_PROMPT.md)
- [CLAUDE.md](../../CLAUDE.md)
- [Standards Index](./STANDARDS_INDEX.md)
