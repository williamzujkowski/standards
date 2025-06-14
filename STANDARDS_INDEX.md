# Standards Index

## Overview

This index provides a comprehensive listing of all standards documents in this repository. Each standard is designed to be:

- **Self-contained**: Can be used independently
- **Cross-referenced**: Links to related standards
- **LLM-optimized**: Structured for AI consumption
- **Progressively disclosed**: From overview to deep implementation

## Quick Navigation

### By Category

#### 🏗️ Architecture & Infrastructure
- [Cloud Native Standards](./CLOUD_NATIVE_STANDARDS.md) (CN) - Container orchestration, microservices, serverless
- [Event-Driven Standards](./EVENT_DRIVEN_STANDARDS.md) (EVT) - Event architecture and messaging patterns
- [DevOps Platform Standards](./DEVOPS_PLATFORM_STANDARDS.md) (DOP) - CI/CD and infrastructure as code

#### 💻 Development
- [Coding Standards](./CODING_STANDARDS.md) (CS) - Language-agnostic best practices
- [Frontend & Mobile Standards](./FRONTEND_MOBILE_STANDARDS.md) (FE) - React, mobile, and web development
- [Data Engineering Standards](./DATA_ENGINEERING_STANDARDS.md) (DE) - Data pipelines and governance
- [Toolchain Standards](./TOOLCHAIN_STANDARDS.md) (TOOL) - Development tools and configurations

#### 🔒 Security & Compliance
- [Modern Security Standards](./MODERN_SECURITY_STANDARDS.md) (SEC) - Security patterns and threat modeling
- [Legal & Compliance Standards](./LEGAL_COMPLIANCE_STANDARDS.md) (LEG) - Privacy, licensing, and compliance

#### 📊 Operations & Quality
- [Testing Standards](./TESTING_STANDARDS.md) (TS) - Test strategies and quality assurance
- [Observability Standards](./OBSERVABILITY_STANDARDS.md) (OBS) - Monitoring and metrics
- [Cost Optimization Standards](./COST_OPTIMIZATION_STANDARDS.md) (COST) - FinOps and resource optimization

#### 📱 Product & Design
- [Web Design & UX Standards](./WEB_DESIGN_UX_STANDARDS.md) (WD) - Design systems and UX guidelines
- [SEO & Web Marketing Standards](./SEO_WEB_MARKETING_STANDARDS.md) (SEO) - Search optimization
- [Content Standards](./CONTENT_STANDARDS.md) (CONT) - Content strategy and governance

#### 📋 Management & Process
- [Project Management Standards](./PROJECT_MANAGEMENT_STANDARDS.md) (PM) - Agile and project practices
- [GitHub Platform Standards](./GITHUB_PLATFORM_STANDARDS.md) (GH) - GitHub best practices
- [Knowledge Management Standards](./KNOWLEDGE_MANAGEMENT_STANDARDS.md) (KM) - Documentation architecture

#### 🔗 Meta Standards
- [Unified Standards](./UNIFIED_STANDARDS.md) (UNIFIED) - Comprehensive overview
- [Creating Standards Guide](./CREATING_STANDARDS_GUIDE.md) - How to create new standards
- [Standard Template](./STANDARD_TEMPLATE.md) - Template for new standards

---

## Complete Standards List

### [Cloud Native Standards](./CLOUD_NATIVE_STANDARDS.md)
**Code:** CN  
**Description:** Container orchestration, microservices, serverless, and cloud-native best practices  
**Status:** Active  

### [Coding Standards](./CODING_STANDARDS.md)
**Code:** CS  
**Description:** Language-agnostic coding conventions, patterns, and best practices  
**Status:** Active  

### [Content Standards](./CONTENT_STANDARDS.md)
**Code:** CONT  
**Description:** Content strategy, writing guidelines, and governance  
**Status:** Active  

### [Cost Optimization Standards](./COST_OPTIMIZATION_STANDARDS.md)
**Code:** COST  
**Description:** FinOps practices, cloud cost management, and resource optimization  
**Status:** Active  

### [Data Engineering Standards](./DATA_ENGINEERING_STANDARDS.md)
**Code:** DE  
**Description:** Data pipelines, quality, governance, and analytics best practices  
**Status:** Active  

### [DevOps Platform Standards](./DEVOPS_PLATFORM_STANDARDS.md)
**Code:** DOP  
**Description:** CI/CD, infrastructure as code, GitOps, and platform engineering  
**Status:** Active  

### [Event-Driven Standards](./EVENT_DRIVEN_STANDARDS.md)
**Code:** EVT  
**Description:** Event-driven architecture, messaging patterns, and saga orchestration  
**Status:** Active  

### [Frontend & Mobile Standards](./FRONTEND_MOBILE_STANDARDS.md)
**Code:** FE  
**Description:** React, mobile development, performance, and accessibility  
**Status:** Active  

### [GitHub Platform Standards](./GITHUB_PLATFORM_STANDARDS.md)
**Code:** GH  
**Description:** GitHub Actions, repository management, and collaboration best practices  
**Status:** Active  

### [Knowledge Management Standards](./KNOWLEDGE_MANAGEMENT_STANDARDS.md)
**Code:** KM  
**Description:** Documentation architecture, AI optimization, and knowledge organization  
**Status:** Active  

### [Legal & Compliance Standards](./LEGAL_COMPLIANCE_STANDARDS.md)
**Code:** LEG  
**Description:** Privacy regulations, licensing, accessibility, and compliance  
**Status:** Active  

### [Modern Security Standards](./MODERN_SECURITY_STANDARDS.md)
**Code:** SEC  
**Description:** Security patterns, authentication, encryption, and threat modeling  
**Status:** Active  

### [Observability Standards](./OBSERVABILITY_STANDARDS.md)
**Code:** OBS  
**Description:** Metrics, logging, tracing, and monitoring best practices  
**Status:** Active  

### [Project Management Standards](./PROJECT_MANAGEMENT_STANDARDS.md)
**Code:** PM  
**Description:** Agile practices, sprint planning, and stakeholder management  
**Status:** Active  

### [SEO & Web Marketing Standards](./SEO_WEB_MARKETING_STANDARDS.md)
**Code:** SEO  
**Description:** Technical SEO, content optimization, and analytics  
**Status:** Active  

### [Testing Standards](./TESTING_STANDARDS.md)
**Code:** TS  
**Description:** Test strategies, TDD, coverage requirements, and quality assurance  
**Status:** Active  

### [Toolchain Standards](./TOOLCHAIN_STANDARDS.md)
**Code:** TOOL  
**Description:** Development tools, linters, formatters, and IDE configurations  
**Status:** Active  

### [Unified Standards](./UNIFIED_STANDARDS.md)
**Code:** UNIFIED  
**Description:** Comprehensive overview and quick reference for all standards  
**Status:** Active  

### [Web Design & UX Standards](./WEB_DESIGN_UX_STANDARDS.md)
**Code:** WD  
**Description:** Design systems, visual standards, and user experience guidelines  
**Status:** Active  

---

## Using This Index

### For Developers
1. Find the relevant standard for your task
2. Start with the Overview section
3. Deep dive into specific sections as needed
4. Check cross-references for related standards

### For LLMs
Use the standard codes for efficient loading:
```
@load CS:api          # Load API section of Coding Standards
@load [SEC:* + TS:*]  # Load all Security and Testing standards
@load KM:architecture # Load architecture section of Knowledge Management
```

### Quick Reference
- Total Standards: 19 domain-specific + meta standards
- Last Updated: 2025-01-13
- All standards follow consistent structure
- Progressive disclosure from overview to implementation

---

## Contributing

To add new standards:
1. Use [STANDARD_TEMPLATE.md](./STANDARD_TEMPLATE.md)
2. Follow [CREATING_STANDARDS_GUIDE.md](./CREATING_STANDARDS_GUIDE.md)
3. Update this index
4. Update [MANIFEST.yaml](./MANIFEST.yaml)
5. Add to [CLAUDE.md](./CLAUDE.md) routing

---

**Navigation:** [README](./README.md) | [Standards Graph](./STANDARDS_GRAPH.md) | [Claude Router](./CLAUDE.md)