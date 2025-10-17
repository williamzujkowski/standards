# Skills Directory

This directory contains 50 modular skills following Anthropic's Agent Skills format.

## Structure

```
skills/
├── skill-loader/              # Meta-skill for coordination
├── legacy-bridge/             # Meta-skill for backward compatibility
├── coding-standards/          # Language-specific development standards
│   ├── python/
│   ├── javascript/
│   ├── typescript/
│   ├── go/
│   └── rust/
├── security/                  # Security standards
│   ├── authentication/
│   ├── secrets-management/
│   ├── zero-trust/
│   ├── threat-modeling/
│   └── input-validation/
├── testing/                   # Testing standards
│   ├── unit-testing/
│   ├── integration-testing/
│   ├── e2e-testing/
│   └── performance-testing/
├── devops/                    # DevOps standards
│   ├── ci-cd/
│   ├── infrastructure/
│   └── monitoring/
├── cloud-native/              # Cloud-native standards
│   ├── kubernetes/
│   ├── containers/
│   └── serverless/
├── frontend/                  # Frontend standards
│   ├── react/
│   ├── vue/
│   ├── mobile-ios/
│   └── mobile-android/
├── data-engineering/          # Data engineering standards
│   ├── orchestration/
│   └── data-quality/
├── ml-ai/                     # ML/AI standards
│   ├── model-development/
│   └── model-deployment/
├── observability/             # Observability standards
│   ├── logging/
│   └── metrics/
├── microservices/             # Microservices standards
│   └── patterns/
├── database/                  # Database standards
│   ├── sql/
│   └── nosql/
├── architecture/              # Architecture standards
│   └── patterns/
├── compliance/                # Compliance standards
│   ├── nist/
│   └── gdpr/
├── design/                    # Design standards
│   └── ux/
└── content/                   # Content standards
    └── documentation/
```

## Skill Categories

### Meta Skills (2)
- **skill-loader**: Skill discovery and loading coordination
- **legacy-bridge**: Backward compatibility with old patterns

### Domain Skills (48)

#### Coding Standards (5)
- python, javascript, typescript, go, rust

#### Security (5)
- authentication, secrets-management, zero-trust, threat-modeling, input-validation

#### Testing (4)
- unit-testing, integration-testing, e2e-testing, performance-testing

#### DevOps (3)
- ci-cd, infrastructure, monitoring

#### Cloud-Native (3)
- kubernetes, containers, serverless

#### Frontend (4)
- react, vue, mobile-ios, mobile-android

#### Data Engineering (2)
- orchestration, data-quality

#### ML/AI (2)
- model-development, model-deployment

#### Observability (2)
- logging, metrics

#### Microservices (1)
- patterns

#### Database (2)
- sql, nosql

#### Architecture (1)
- patterns

#### Compliance (2)
- nist, gdpr

#### Design (1)
- ux

#### Content (1)
- documentation

## Skill Structure

Each skill directory contains:

```
skill-name/
├── SKILL.md           # Main skill definition
├── templates/         # Code/config templates
├── scripts/          # Executable automation scripts
└── resources/        # Detailed reference documentation
```

## Usage

Skills are loaded on-demand using progressive disclosure:

1. **Level 1 (Metadata)**: All skill names and descriptions (~100 tokens/skill)
2. **Level 2 (Instructions)**: Full SKILL.md content (<5,000 tokens/skill)
3. **Level 3 (Resources)**: Detailed docs via filesystem (0 tokens)

### Loading Skills

```
# Single skill
@load python

# Multiple skills
@load [python + unit-testing + security-authentication]

# Category wildcard
@load security:*

# Product bundle
@load product:api
```

## Status

**Phase 1**: Directory structure created ✓
**Phase 2**: Skill content population (in progress)
**Phase 3**: Validation and testing (pending)
**Phase 4**: Integration and deployment (pending)

## Documentation

- [Architecture Design](../docs/migration/architecture-design.md)
- [Migration Plan](../docs/migration/migration-plan.md)
- [Skill Authoring Guide](../docs/migration/skill-authoring-guide.md) (TBD)

---

**Total Skills**: 50 (2 meta + 48 domain)
**Token Target**: <5,000 tokens per skill
**Repository**: https://github.com/williamzujkowski/standards
