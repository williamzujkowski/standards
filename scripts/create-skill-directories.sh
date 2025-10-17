#!/bin/bash
# create-skill-directories.sh
# Creates complete 50-skill directory structure with placeholder files

set -e

BASE_DIR="/home/william/git/standards/skills"
DOCS_DIR="/home/william/git/standards/docs/migration"

echo "Creating skills directory structure..."

# Create base skills directory
mkdir -p "$BASE_DIR"

# Function to create skill directory with subdirectories
create_skill_dir() {
    local skill_path="$1"
    local skill_name="$2"

    echo "Creating: $skill_path"
    mkdir -p "$skill_path"/{templates,scripts,resources}

    # Create placeholder SKILL.md
    cat > "$skill_path/SKILL.md" << 'EOF'
---
name: {{SKILL_NAME}}
description: TODO - Add skill description
---

# {{SKILL_NAME}} Skill

## Overview

TODO: Add overview

## When to Use This Skill

TODO: Add usage scenarios

## Core Instructions

TODO: Add core instructions

## Advanced Topics

TODO: Add advanced topics and resource references

## Related Skills

TODO: Add related skills
EOF
    sed -i "s/{{SKILL_NAME}}/$skill_name/g" "$skill_path/SKILL.md"

    # Create README.md files in subdirectories
    echo "# Templates for $skill_name" > "$skill_path/templates/README.md"
    echo "# Scripts for $skill_name" > "$skill_path/scripts/README.md"
    echo "# Resources for $skill_name" > "$skill_path/resources/README.md"
}

# META-SKILLS
create_skill_dir "$BASE_DIR/skill-loader" "skill-loader"
mkdir -p "$BASE_DIR/skill-loader/config"
echo "# Skill Loader Configuration" > "$BASE_DIR/skill-loader/config/README.md"

create_skill_dir "$BASE_DIR/legacy-bridge" "legacy-bridge"
mkdir -p "$BASE_DIR/legacy-bridge/config"
echo "# Legacy Bridge Configuration" > "$BASE_DIR/legacy-bridge/config/README.md"

# CODING STANDARDS CATEGORY
mkdir -p "$BASE_DIR/coding-standards"
create_skill_dir "$BASE_DIR/coding-standards/python" "python"
create_skill_dir "$BASE_DIR/coding-standards/javascript" "javascript"
create_skill_dir "$BASE_DIR/coding-standards/typescript" "typescript"
create_skill_dir "$BASE_DIR/coding-standards/go" "go"
create_skill_dir "$BASE_DIR/coding-standards/rust" "rust"

# SECURITY CATEGORY
mkdir -p "$BASE_DIR/security"
create_skill_dir "$BASE_DIR/security/authentication" "authentication"
create_skill_dir "$BASE_DIR/security/secrets-management" "secrets-management"
create_skill_dir "$BASE_DIR/security/zero-trust" "zero-trust"
create_skill_dir "$BASE_DIR/security/threat-modeling" "threat-modeling"
create_skill_dir "$BASE_DIR/security/input-validation" "input-validation"

# TESTING CATEGORY
mkdir -p "$BASE_DIR/testing"
create_skill_dir "$BASE_DIR/testing/unit-testing" "unit-testing"
create_skill_dir "$BASE_DIR/testing/integration-testing" "integration-testing"
create_skill_dir "$BASE_DIR/testing/e2e-testing" "e2e-testing"
create_skill_dir "$BASE_DIR/testing/performance-testing" "performance-testing"

# DEVOPS CATEGORY
mkdir -p "$BASE_DIR/devops"
create_skill_dir "$BASE_DIR/devops/ci-cd" "ci-cd"
create_skill_dir "$BASE_DIR/devops/infrastructure" "infrastructure"
create_skill_dir "$BASE_DIR/devops/monitoring" "monitoring"

# CLOUD-NATIVE CATEGORY
mkdir -p "$BASE_DIR/cloud-native"
create_skill_dir "$BASE_DIR/cloud-native/kubernetes" "kubernetes"
create_skill_dir "$BASE_DIR/cloud-native/containers" "containers"
create_skill_dir "$BASE_DIR/cloud-native/serverless" "serverless"

# FRONTEND CATEGORY
mkdir -p "$BASE_DIR/frontend"
create_skill_dir "$BASE_DIR/frontend/react" "react"
create_skill_dir "$BASE_DIR/frontend/vue" "vue"
create_skill_dir "$BASE_DIR/frontend/mobile-ios" "mobile-ios"
create_skill_dir "$BASE_DIR/frontend/mobile-android" "mobile-android"

# DATA-ENGINEERING CATEGORY
mkdir -p "$BASE_DIR/data-engineering"
create_skill_dir "$BASE_DIR/data-engineering/orchestration" "orchestration"
create_skill_dir "$BASE_DIR/data-engineering/data-quality" "data-quality"

# ML-AI CATEGORY
mkdir -p "$BASE_DIR/ml-ai"
create_skill_dir "$BASE_DIR/ml-ai/model-development" "model-development"
create_skill_dir "$BASE_DIR/ml-ai/model-deployment" "model-deployment"

# OBSERVABILITY CATEGORY
mkdir -p "$BASE_DIR/observability"
create_skill_dir "$BASE_DIR/observability/logging" "logging"
create_skill_dir "$BASE_DIR/observability/metrics" "metrics"

# MICROSERVICES CATEGORY
mkdir -p "$BASE_DIR/microservices"
create_skill_dir "$BASE_DIR/microservices/patterns" "patterns"

# DATABASE CATEGORY
mkdir -p "$BASE_DIR/database"
create_skill_dir "$BASE_DIR/database/sql" "sql"
create_skill_dir "$BASE_DIR/database/nosql" "nosql"

# ARCHITECTURE CATEGORY
mkdir -p "$BASE_DIR/architecture"
create_skill_dir "$BASE_DIR/architecture/patterns" "patterns"

# COMPLIANCE CATEGORY
mkdir -p "$BASE_DIR/compliance"
create_skill_dir "$BASE_DIR/compliance/nist" "nist"
mkdir -p "$BASE_DIR/compliance/nist/controls"
echo "# NIST Control Families" > "$BASE_DIR/compliance/nist/controls/README.md"
create_skill_dir "$BASE_DIR/compliance/gdpr" "gdpr"

# DESIGN CATEGORY
mkdir -p "$BASE_DIR/design"
create_skill_dir "$BASE_DIR/design/ux" "ux"

# CONTENT CATEGORY
mkdir -p "$BASE_DIR/content"
create_skill_dir "$BASE_DIR/content/documentation" "documentation"

echo "✓ Directory structure created successfully"

# Count skills
skill_count=$(find "$BASE_DIR" -name "SKILL.md" | wc -l)
echo "Total skills created: $skill_count"

# Create root README.md
cat > "$BASE_DIR/README.md" << 'ENDREADME'
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
ENDREADME

echo "✓ Root README.md created"

echo ""
echo "=== DIRECTORY CREATION COMPLETE ==="
echo "Base directory: $BASE_DIR"
echo "Total skills: $skill_count"
echo ""
echo "Next steps:"
echo "1. Validate structure: tree $BASE_DIR"
echo "2. Review placeholder files"
echo "3. Begin Phase 2: Content population"
