# GitHub Platform Standards

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active
**Standard Code:** GH

---

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active

## Table of Contents

1. [Repository Standards](#1-repository-standards)
2. [GitHub Actions CI/CD](#2-github-actions-cicd)
3. [GitHub Pages Hosting](#3-github-pages-hosting)
4. [Security and Compliance](#4-security-and-compliance)
5. [Project Management](#5-project-management)
6. [GitHub Apps and Integrations](#6-github-apps-and-integrations)
7. [Advanced GitHub Features](#7-advanced-github-features)

---

## Overview

This standard provides comprehensive guidelines and best practices for the subject area.
It aims to ensure consistency, quality, and maintainability across all related implementations.

## 1. Repository Standards

### 1.1 Repository Structure

#### Base Repository Layout **[REQUIRED]**
```
project-name/
├── .github/                    # GitHub-specific files
│   ├── workflows/             # GitHub Actions workflows
│   ├── ISSUE_TEMPLATE/        # Issue templates
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS            # Code ownership
│   ├── dependabot.yml        # Dependency updates
│   └── SECURITY.md           # Security policy
├── docs/                      # Documentation
│   └── index.md              # For GitHub Pages
├── src/                       # Source code
├── tests/                     # Test files
├── scripts/                   # Build/utility scripts
├── .gitignore
├── README.md
├── LICENSE
├── CONTRIBUTING.md
└── CODE_OF_CONDUCT.md
```

#### Repository Settings **[REQUIRED]**
```yaml
# .github/settings.yml (using GitHub Settings App)
repository:
  name: project-name
  description: Clear, concise description
  topics:
    - topic1
    - topic2
  private: false
  has_issues: true
  has_projects: true
  has_wiki: false
  has_downloads: true
  default_branch: main
  allow_squash_merge: true
  allow_merge_commit: false
  allow_rebase_merge: true
  delete_branch_on_merge: true
  enable_vulnerability_alerts: true
  enable_automated_security_fixes: true

branches:
  - name: main
    protection:
      required_status_checks:
        strict: true
        contexts:
          - continuous-integration
          - security-scan
      enforce_admins: false
      required_pull_request_reviews:
        required_approving_review_count: 1
        dismiss_stale_reviews: true
        require_code_owner_reviews: true
      restrictions: null
```

### 1.2 Branch Protection

#### Protection Rules **[REQUIRED]**
```yaml
# Branch protection for main/master
protection_rules:
  main:
    # Require PR reviews
    required_reviews:
      count: 1
      dismiss_stale: true
      require_codeowner: true

    # Required status checks
    required_checks:
      - "build"
      - "test"
      - "security-scan"
      - "lint"

    # Additional restrictions
    enforce_admins: false
    restrict_pushes: true
    allow_force_pushes: false
    allow_deletions: false

    # Require up-to-date branches
    strict_checks: true

    # Require signed commits
    required_signatures: true
```

### 1.3 Repository Templates

#### README Template **[REQUIRED]**
```markdown
# Project Name

![Build Status](https://github.com/org/repo/workflows/CI/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/org/repo)
![License](https://img.shields.io/github/license/org/repo)

Brief description of the project.

## 🚀 Quick Start

```bash
# Installation
npm install

# Development
npm run dev

# Testing
npm test

# Build
npm run build
```

## 📋 Prerequisites

- Node.js >= 18
- npm >= 9

## 🛠️ Installation

Detailed installation instructions.

## 📖 Documentation

- [Contributing Guide](./docs/core/CONTRIBUTING.md)
- [Code of Conduct](./docs/core/CODE_OF_CONDUCT.md)

## 🧪 Testing

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test
npm test -- --grep "test name"
```

## 🤝 Contributing

Please read [CONTRIBUTING.md](./docs/core/CONTRIBUTING.md) for details.

## 📝 License

This project is licensed under the MIT License - see [LICENSE](./LICENSE).
```

#### CONTRIBUTING Template **[REQUIRED]**
```markdown
# Contributing to Project Name

## Code of Conduct

Please read our [Code of Conduct](./docs/core/CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Issues

1. Check existing issues
2. Create detailed bug report
3. Include reproduction steps
4. Add system information

### Pull Requests

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/repo-name

# Install dependencies
npm install

# Run tests
npm test

# Start development
npm run dev
```

### Coding Standards

- Follow existing code style
- Add tests for new features
- Update documentation
- Ensure CI passes

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `test:` Tests
- `chore:` Maintenance
```

---

## 2. GitHub Actions CI/CD

### 2.1 Workflow Structure

#### Basic CI Workflow **[REQUIRED]**
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # Weekly security scan

env:
  NODE_VERSION: '18'

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Check formatting
        run: npm run format:check

  test:
    name: Test
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Upload coverage
        if: matrix.node-version == '18'
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          file: ./coverage/lcov.info

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run security audit
        run: npm audit --audit-level=high

      - name: Run Snyk scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Upload SARIF results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: snyk.sarif

  build:
    name: Build
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build project
        run: npm run build

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build-artifacts
          path: dist/
          retention-days: 7
```

### 2.2 Advanced Workflows

#### Release Workflow **[REQUIRED]**
```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write
  packages: write

jobs:
  release:
    name: Create Release
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 18
          registry-url: 'https://registry.npmjs.org'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Generate changelog
        id: changelog
        uses: conventional-changelog-action@v3
        with:
          preset: 'angular'

      - name: Create Release
        uses: ncipollo/release-action@v1
        with:
          artifacts: "dist/*"
          body: ${{ steps.changelog.outputs.clean_changelog }}
          draft: false
          prerelease: false

      - name: Publish to npm
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

      - name: Build Docker image
        run: |
          docker build -t ghcr.io/${{ github.repository }}:${{ github.ref_name }} .
          docker push ghcr.io/${{ github.repository }}:${{ github.ref_name }}
```

#### Deployment Workflow **[REQUIRED]**
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        type: choice
        options:
          - development
          - staging
          - production

jobs:
  deploy:
    name: Deploy to ${{ github.event.inputs.environment }}
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment }}
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to environment
        run: |
          ./scripts/deploy.sh ${{ github.event.inputs.environment }}

      - name: Notify deployment
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Deployment to ${{ github.event.inputs.environment }} ${{ job.status }}'
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
        if: always()
```

### 2.3 Reusable Workflows

#### Shared Workflow **[REQUIRED]**
```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      node-version:
        required: false
        type: string
        default: '18'
    secrets:
      codecov-token:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: 'npm'

      - name: Install and test
        run: |
          npm ci
          npm test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.codecov-token }}
```

#### Using Reusable Workflow
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '18'
    secrets:
      codecov-token: ${{ secrets.CODECOV_TOKEN }}
```

### 2.4 GitHub Actions Best Practices

#### Action Security **[REQUIRED]**
```yaml
# Pin actions to commit SHA for security
steps:
  - uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608 # v4.1.0

  # Use environment for secrets
  - name: Deploy
    environment: production
    env:
      API_KEY: ${{ secrets.API_KEY }}
    run: |
      # Never echo secrets
      ./deploy.sh
```

#### Caching Strategy **[RECOMMENDED]**
```yaml
# Cache dependencies
- name: Cache node modules
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

# Cache build artifacts
- name: Cache build
  uses: actions/cache@v3
  with:
    path: |
      .next/cache
      dist
    key: ${{ runner.os }}-build-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-build-
```

#### Matrix Builds **[RECOMMENDED]**
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    node: [16, 18, 20]
    exclude:
      - os: windows-latest
        node: 16
  fail-fast: false
  max-parallel: 3
```

---

## 3. GitHub Pages Hosting

### 3.1 Static Site Configuration

#### Jekyll Configuration **[REQUIRED]**
```yaml
# _config.yml
title: Project Documentation
description: Comprehensive project documentation
theme: just-the-docs
baseurl: "/project-name"
url: "https://username.github.io"

# Navigation
nav_enabled: true
nav_sort: case_insensitive

# Search
search_enabled: true
search_tokenizer_separator: /[\s/]+/

# Footer
footer_content: "Copyright &copy; 2025"

# Collections
collections:
  docs:
    permalink: "/:collection/:path/"
    output: true

# Defaults
defaults:
  - scope:
      path: ""
      type: "docs"
    values:
      layout: "default"
      nav_order: 1
```

#### GitHub Pages Workflow **[REQUIRED]**
```yaml
# .github/workflows/deploy-pages.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
    paths:
      - 'docs/**'
      - '_config.yml'

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1'
          bundler-cache: true

      - name: Build Jekyll site
        run: bundle exec jekyll build
        env:
          JEKYLL_ENV: production

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: ./_site

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v3
```

### 3.2 Custom Domain Setup

#### DNS Configuration **[REQUIRED]**
```
# CNAME file in repository root
docs.example.com
```

```
# DNS Records
Type    Name    Value                   TTL
A       @       185.199.108.153        300
A       @       185.199.109.153        300
A       @       185.199.110.153        300
A       @       185.199.111.153        300
CNAME   www     username.github.io     300
```

### 3.3 Documentation Site Structure

#### Documentation Layout **[REQUIRED]**
```
docs/
├── _config.yml
├── index.md
├── getting-started/
│   ├── installation.md
│   ├── configuration.md
│   └── quick-start.md
├── guides/
│   ├── development.md
│   ├── deployment.md
│   └── troubleshooting.md
├── api/
│   ├── reference.md
│   └── examples.md
└── assets/
    ├── css/
    ├── js/
    └── images/
```

#### Front Matter Template **[REQUIRED]**
```markdown
---
layout: default
title: Page Title
nav_order: 1
parent: Parent Page
has_children: true
has_toc: true
---

# Page Title

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Section 1

Content here...
```

---

## 4. Security and Compliance

### 4.1 Security Configuration

#### Dependabot Configuration **[REQUIRED]**
```yaml
# .github/dependabot.yml
version: 2
updates:
  # npm dependencies
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "04:00"
    open-pull-requests-limit: 10
    reviewers:
      - "username"
    labels:
      - "dependencies"
      - "npm"
    commit-message:
      prefix: "chore"
      include: "scope"
    ignore:
      - dependency-name: "aws-sdk"
        versions: ["2.x"]

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "github-actions"

  # Docker
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "docker"
```

#### Security Policy **[REQUIRED]**
```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.x.x   | :white_check_mark: |
| 1.x.x   | :x:                |

## Reporting a Vulnerability

Please report security vulnerabilities to security@example.com.

- We will acknowledge receipt within 24 hours
- We will provide updates every 72 hours
- We aim to patch critical issues within 7 days

Do not disclose security issues publicly until patched.

## Security Measures

- All dependencies are automatically scanned
- Security patches are applied promptly
- Code is reviewed for security issues
- Penetration testing performed quarterly
```

#### Code Scanning **[REQUIRED]**
```yaml
# .github/workflows/codeql.yml
name: "CodeQL"

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 1 * * 0'

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    strategy:
      fail-fast: false
      matrix:
        language: [ 'javascript', 'python' ]

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v2
      with:
        languages: ${{ matrix.language }}
        queries: security-and-quality

    - name: Autobuild
      uses: github/codeql-action/autobuild@v2

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v2
      with:
        category: "/language:${{matrix.language}}"
```

### 4.2 Compliance Automation

#### License Scanning **[REQUIRED]**
```yaml
# .github/workflows/license-scan.yml
name: License Scan

on: [push, pull_request]

jobs:
  license-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: License Finder
        uses: pivotal/licensefinder-action@v1
        with:
          permitted_licenses: |
            MIT
            Apache-2.0
            BSD-3-Clause
            ISC

      - name: FOSSA Scan
        uses: fossas/fossa-action@main
        with:
          api-key: ${{ secrets.FOSSA_API_KEY }}
```

#### SBOM Generation **[REQUIRED]**
```yaml
# Generate Software Bill of Materials
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    artifact-name: sbom.spdx.json
    format: spdx-json

- name: Publish SBOM
  uses: anchore/sbom-action/publish-sbom@v0
  with:
    sbom-artifact-match: ".*\\.spdx\\.json$"
```

---

## 5. Project Management

### 5.1 Issue Templates

#### Bug Report Template **[REQUIRED]**
```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: Bug Report
description: File a bug report
title: "[Bug]: "
labels: ["bug", "triage"]
assignees:
  - octocat
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!

  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: A clear and concise description of the bug
      placeholder: Tell us what you see!
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Steps to reproduce
      description: Steps to reproduce the behavior
      value: |
        1. Go to '...'
        2. Click on '....'
        3. Scroll down to '....'
        4. See error
    validations:
      required: true

  - type: dropdown
    id: version
    attributes:
      label: Version
      description: What version are you running?
      options:
        - 1.0.2 (Default)
        - 1.0.3 (Edge)
    validations:
      required: true

  - type: dropdown
    id: browsers
    attributes:
      label: What browsers are you seeing the problem on?
      multiple: true
      options:
        - Firefox
        - Chrome
        - Safari
        - Microsoft Edge

  - type: textarea
    id: logs
    attributes:
      label: Relevant log output
      description: Please copy and paste any relevant log output
      render: shell

  - type: checkboxes
    id: terms
    attributes:
      label: Code of Conduct
      description: By submitting this issue, you agree to follow our Code of Conduct
      options:
        - label: I agree to follow this project's Code of Conduct
          required: true
```

#### Feature Request Template **[REQUIRED]**
```yaml
# .github/ISSUE_TEMPLATE/feature_request.yml
name: Feature Request
description: Suggest a new feature
title: "[Feature]: "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for suggesting a new feature!

  - type: textarea
    id: problem
    attributes:
      label: Problem Statement
      description: What problem does this feature solve?
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: Describe your proposed solution
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: What alternatives have you considered?

  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - Low
        - Medium
        - High
        - Critical
```

### 5.2 Project Automation

#### Project Board Automation **[REQUIRED]**
```yaml
# .github/workflows/project-automation.yml
name: Project Automation

on:
  issues:
    types: [opened, labeled]
  pull_request:
    types: [opened, ready_for_review, review_requested]

jobs:
  add-to-project:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/add-to-project@v0.5.0
        with:
          project-url: https://github.com/orgs/myorg/projects/1
          github-token: ${{ secrets.GITHUB_TOKEN }}
          labeled: bug, enhancement
          label-operator: OR
```

#### Auto-labeling **[REQUIRED]**
```yaml
# .github/labeler.yml
documentation:
  - docs/**
  - '*.md'

frontend:
  - src/frontend/**
  - src/components/**
  - '*.css'
  - '*.scss'

backend:
  - src/backend/**
  - src/api/**
  - src/services/**

tests:
  - tests/**
  - '**/*.test.js'
  - '**/*.spec.js'

dependencies:
  - package.json
  - package-lock.json
  - yarn.lock
  - requirements.txt
  - go.mod
  - go.sum
```

### 5.3 Release Management

#### Release Drafter **[REQUIRED]**
```yaml
# .github/release-drafter.yml
name-template: 'v$RESOLVED_VERSION'
tag-template: 'v$RESOLVED_VERSION'
categories:
  - title: '🚀 Features'
    labels:
      - 'feature'
      - 'enhancement'
  - title: '🐛 Bug Fixes'
    labels:
      - 'fix'
      - 'bugfix'
      - 'bug'
  - title: '🧰 Maintenance'
    labels:
      - 'chore'
      - 'dependencies'
change-template: '- $TITLE @$AUTHOR (#$NUMBER)'
change-title-escapes: '\<*_&'
version-resolver:
  major:
    labels:
      - 'major'
      - 'breaking-change'
  minor:
    labels:
      - 'minor'
      - 'feature'
  patch:
    labels:
      - 'patch'
      - 'bug'
  default: patch
template: |
  ## Changes

  $CHANGES

  **Full Changelog**: https://github.com/$OWNER/$REPOSITORY/compare/$PREVIOUS_TAG...v$RESOLVED_VERSION
```

#### Changelog Generation **[REQUIRED]**
```yaml
# .github/workflows/changelog.yml
name: Changelog

on:
  push:
    branches: [ main ]

jobs:
  changelog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate changelog
        uses: orhun/git-cliff-action@v2
        with:
          config: .github/cliff.toml
          args: --verbose
        env:
          OUTPUT: CHANGELOG.md

      - name: Commit changelog
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add CHANGELOG.md
          git commit -m "chore: update changelog" || exit 0
          git push
```

---

## 6. GitHub Apps and Integrations

### 6.1 Essential GitHub Apps

#### Recommended Apps **[RECOMMENDED]**
```yaml
# Essential GitHub Apps to install:
apps:
  - name: "Dependabot"
    purpose: "Automated dependency updates"

  - name: "Codecov"
    purpose: "Code coverage tracking"
    config: |
      codecov:
        require_ci_to_pass: yes
        coverage:
          status:
            project:
              default:
                target: 80%
                threshold: 2%

  - name: "Renovate"
    purpose: "Advanced dependency management"
    config: |
      {
        "extends": ["config:base"],
        "prConcurrentLimit": 3,
        "prHourlyLimit": 2
      }

  - name: "Stale"
    purpose: "Manage stale issues/PRs"
    config: |
      daysUntilStale: 60
      daysUntilClose: 7
      staleLabel: wontfix

  - name: "AllContributors"
    purpose: "Recognize contributors"

  - name: "Settings"
    purpose: "Repository settings as code"
```

### 6.2 Webhook Configuration

#### Webhook Setup **[RECOMMENDED]**
```javascript
// Example webhook handler
const crypto = require('crypto');
const express = require('express');
const app = express();

// Middleware to verify GitHub webhook signature
function verifyGitHubWebhook(req, res, next) {
  const signature = req.headers['x-hub-signature-256'];
  const body = JSON.stringify(req.body);

  if (!signature) {
    return res.status(401).send('Unauthorized');
  }

  const hmac = crypto.createHmac('sha256', process.env.WEBHOOK_SECRET);
  const digest = 'sha256=' + hmac.update(body).digest('hex');

  if (signature !== digest) {
    return res.status(401).send('Unauthorized');
  }

  next();
}

// Webhook handler
app.post('/webhook', express.json(), verifyGitHubWebhook, (req, res) => {
  const event = req.headers['x-github-event'];
  const payload = req.body;

  switch (event) {
    case 'push':
      handlePush(payload);
      break;
    case 'pull_request':
      handlePullRequest(payload);
      break;
    case 'issues':
      handleIssue(payload);
      break;
    default:
      console.log(`Unhandled event: ${event}`);
  }

  res.status(200).send('OK');
});
```

---

## 7. Advanced GitHub Features

### 7.1 GitHub CLI Automation

#### CLI Scripts **[RECOMMENDED]**
```bash
#!/bin/bash
# scripts/github-automation.sh

# Create issue from template
create_issue() {
  gh issue create \
    --title "$1" \
    --body-file .github/ISSUE_TEMPLATE/bug_report.md \
    --label "bug,needs-triage" \
    --assignee "@me"
}

# Bulk update PRs
update_prs() {
  gh pr list --label "needs-rebase" --json number --jq '.[].number' | \
  while read -r pr; do
    gh pr checkout "$pr"
    git rebase origin/main
    git push --force-with-lease
    gh pr review "$pr" --comment --body "Rebased on main"
  done
}

# Archive old issues
archive_issues() {
  gh issue list \
    --state closed \
    --search "updated:<$(date -d '90 days ago' +%Y-%m-%d)" \
    --json number,title --limit 100 | \
  jq -r '.[] | "\(.number)\t\(.title)"' > archived_issues.txt
}

# Generate release notes
generate_release() {
  local version=$1
  local previous=$(gh release list --limit 1 --json tagName --jq '.[0].tagName')

  gh api repos/:owner/:repo/releases/generate-notes \
    --method POST \
    --field tag_name="v$version" \
    --field target_commitish=main \
    --field previous_tag_name="$previous" \
    --jq '.body' > release_notes.md
}
```

### 7.2 GitHub API Usage

#### API Automation **[RECOMMENDED]**
```javascript
// GitHub API client setup
const { Octokit } = require("@octokit/rest");
const { retry } = require("@octokit/plugin-retry");
const { throttling } = require("@octokit/plugin-throttling");

const MyOctokit = Octokit.plugin(retry, throttling);

const octokit = new MyOctokit({
  auth: process.env.GITHUB_TOKEN,
  throttle: {
    onRateLimit: (retryAfter, options) => {
      console.warn(`Rate limit exceeded, retrying after ${retryAfter} seconds`);
      return true;
    },
    onSecondaryRateLimit: (retryAfter, options) => {
      console.warn(`Secondary rate limit hit, retrying after ${retryAfter} seconds`);
      return true;
    },
  },
});

// Example: Auto-merge dependabot PRs
async function autoMergeDependabot() {
  const { data: pulls } = await octokit.pulls.list({
    owner: 'myorg',
    repo: 'myrepo',
    state: 'open',
  });

  for (const pull of pulls) {
    if (pull.user.login === 'dependabot[bot]' && pull.mergeable_state === 'clean') {
      await octokit.pulls.merge({
        owner: 'myorg',
        repo: 'myrepo',
        pull_number: pull.number,
        merge_method: 'squash',
      });
      console.log(`Merged PR #${pull.number}`);
    }
  }
}

// Example: Bulk issue operations
async function bulkUpdateIssues(labels, milestone) {
  const iterator = octokit.paginate.iterator(octokit.issues.listForRepo, {
    owner: 'myorg',
    repo: 'myrepo',
    state: 'open',
    per_page: 100,
  });

  for await (const { data: issues } of iterator) {
    for (const issue of issues) {
      await octokit.issues.update({
        owner: 'myorg',
        repo: 'myrepo',
        issue_number: issue.number,
        labels: [...issue.labels.map(l => l.name), ...labels],
        milestone: milestone,
      });
    }
  }
}
```

### 7.3 Code Spaces Configuration

#### DevContainer Setup **[RECOMMENDED]**
```json
// .devcontainer/devcontainer.json
{
  "name": "Project Dev Container",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:18",
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/kubectl-helm-minikube:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "GitHub.copilot",
        "GitHub.vscode-pull-request-github"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode"
      }
    }
  },
  "postCreateCommand": "npm install",
  "forwardPorts": [3000, 5432],
  "portsAttributes": {
    "3000": {
      "label": "Application",
      "onAutoForward": "notify"
    }
  },
  "remoteUser": "node"
}
```

---

## Implementation Checklist

### Repository Setup
- [ ] Repository structure follows standards
- [ ] Branch protection configured
- [ ] CODEOWNERS file created
- [ ] Issue/PR templates added
- [ ] Security policy defined

### CI/CD Pipeline
- [ ] Basic CI workflow implemented
- [ ] Security scanning enabled
- [ ] Deployment automation configured
- [ ] Release process automated
- [ ] Artifact management setup

### GitHub Pages
- [ ] Documentation site configured
- [ ] Custom domain setup (if needed)
- [ ] Automatic deployment enabled
- [ ] Search functionality added
- [ ] Analytics configured

### Security & Compliance
- [ ] Dependabot enabled
- [ ] CodeQL scanning active
- [ ] Secret scanning enabled
- [ ] License compliance checked
- [ ] SBOM generation automated

### Project Management
- [ ] Project boards configured
- [ ] Automation rules created
- [ ] Labels standardized
- [ ] Milestones defined
- [ ] Team permissions set

### Advanced Features
- [ ] GitHub Apps installed
- [ ] Webhooks configured (if needed)
- [ ] API integrations built
- [ ] CLI scripts created
- [ ] DevContainer configured

---

**End of GitHub Platform Standards**
