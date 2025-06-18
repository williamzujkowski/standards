# Project Management Standards

**Version:** 2.0.0
**Last Updated:** January 2025
**Status:** Active
**Standard Code:** PM

---

**Version:** 2.0.0
**Last Updated:** January 2025
**Status:** Active
**Focus:** Agile project management with enterprise adaptability

## Table of Contents

1. [Core Principles](#1-core-principles)
2. [Methodology Framework](#2-methodology-framework)
3. [Project Lifecycle](#3-project-lifecycle)
4. [Agile Implementation](#4-agile-implementation)
5. [Planning and Execution](#5-planning-and-execution)
6. [Risk and Issue Management](#6-risk-and-issue-management)
7. [Stakeholder Engagement](#7-stakeholder-engagement)
8. [Team Excellence](#8-team-excellence)
9. [Metrics and Reporting](#9-metrics-and-reporting)
10. [Implementation Guidelines](#10-implementation-guidelines)

---

## Overview

This standard provides comprehensive guidelines and best practices for the subject area.
It aims to ensure consistency, quality, and maintainability across all related implementations.

## 1. Core Principles

### 1.1 Foundation Standards **[REQUIRED]**

```yaml
core_principles:
  customer_focus:
    - Deliver value early and continuously
    - Validate assumptions with users
    - Prioritize based on business impact

  team_empowerment:
    - Self-organizing teams
    - Psychological safety
    - Continuous learning culture

  adaptive_planning:
    - Embrace change as competitive advantage
    - Short feedback loops
    - Data-driven decisions

  quality_first:
    - Built-in quality, not inspected in
    - Definition of Done enforcement
    - Technical excellence
```

### 1.2 Success Criteria **[REQUIRED]**

```yaml
project_success:
  dimensions:
    delivery: "On time, on budget, on scope"
    quality: "Meets acceptance criteria"
    value: "Achieves business objectives"
    team: "Sustainable pace, high morale"
    stakeholder: "Satisfaction > 4/5"
```

---

## 2. Methodology Framework

### 2.1 Methodology Selection **[REQUIRED]**

```yaml
methodology_guide:
  agile_scrum:
    use_when:
      - Evolving requirements
      - Need frequent delivery
      - High collaboration possible
    team_size: "3-9 members"
    sprint_length: "1-4 weeks"

  kanban:
    use_when:
      - Continuous flow needed
      - Varying task sizes
      - Support/maintenance work
    wip_limits: "Required"

  waterfall:
    use_when:
      - Fixed requirements
      - Regulatory compliance
      - Hardware dependencies
    phases: [Requirements, Design, Build, Test, Deploy]

  hybrid:
    use_when:
      - Mixed requirement stability
      - Phased rollouts needed
      - Enterprise constraints
    approach: "Waterfall phases with Agile execution"
```

### 2.2 Framework Components **[REQUIRED]**

```yaml
framework_elements:
  roles:
    product_owner:
      - Owns product vision
      - Manages backlog
      - Stakeholder liaison

    scrum_master:
      - Facilitates process
      - Removes impediments
      - Coaches team

    development_team:
      - Self-organizing
      - Cross-functional
      - Delivers increment

  artifacts:
    product_backlog: "Prioritized feature list"
    sprint_backlog: "Committed work for sprint"
    increment: "Potentially shippable product"

  events:
    sprint_planning: "Define sprint work"
    daily_standup: "Sync and impediments"
    sprint_review: "Demo and feedback"
    retrospective: "Continuous improvement"
```

---

## 3. Project Lifecycle

### 3.1 Project Phases **[REQUIRED]**

```yaml
lifecycle_phases:
  initiation:
    activities:
      - Define business case
      - Identify stakeholders
      - Create project charter
      - Secure funding
    deliverables:
      - Project charter
      - Stakeholder register
      - Initial budget

  planning:
    activities:
      - Develop roadmap
      - Create WBS
      - Define team structure
      - Risk assessment
    deliverables:
      - Project plan
      - Resource plan
      - Risk register

  execution:
    activities:
      - Sprint execution
      - Progress monitoring
      - Stakeholder communication
      - Quality assurance
    deliverables:
      - Working increments
      - Status reports
      - Updated documentation

  closure:
    activities:
      - Final delivery
      - Knowledge transfer
      - Retrospective
      - Team transition
    deliverables:
      - Final product
      - Lessons learned
      - Project archive
```

### 3.2 Phase Gates **[RECOMMENDED]**

```yaml
phase_gates:
  go_no_go_criteria:
    initiation_to_planning:
      - Approved business case
      - Committed sponsor
      - Available funding

    planning_to_execution:
      - Approved plan
      - Team assembled
      - Environment ready

    execution_to_closure:
      - Acceptance criteria met
      - Documentation complete
      - Support plan ready
```

---

## 4. Agile Implementation

### 4.1 Sprint Management **[REQUIRED]**

```yaml
sprint_standards:
  planning:
    duration: "4 hours for 2-week sprint"
    inputs:
      - Refined backlog
      - Team capacity
      - Sprint goal
    outputs:
      - Sprint backlog
      - Commitment
      - Plan

  execution:
    daily_standup:
      duration: "15 minutes"
      questions:
        - What did I complete?
        - What will I do today?
        - Any impediments?

    practices:
      - Update board daily
      - Raise blockers immediately
      - Collaborate actively

  review:
    duration: "2 hours for 2-week sprint"
    activities:
      - Demo working software
      - Gather feedback
      - Update backlog

  retrospective:
    duration: "1.5 hours for 2-week sprint"
    format:
      - What went well?
      - What could improve?
      - Action items
```

### 4.2 Backlog Management **[REQUIRED]**

```yaml
backlog_standards:
  user_stories:
    format: "As a [user], I want [feature] so that [benefit]"

    INVEST_criteria:
      Independent: "Minimal dependencies"
      Negotiable: "Not a contract"
      Valuable: "Delivers user value"
      Estimable: "Can size it"
      Small: "Fits in sprint"
      Testable: "Clear acceptance criteria"

  prioritization:
    methods:
      - MoSCoW (Must/Should/Could/Won't)
      - Value vs Effort matrix
      - WSJF (Weighted Shortest Job First)

  refinement:
    frequency: "Weekly, 10% of capacity"
    activities:
      - Split large stories
      - Add acceptance criteria
      - Estimate effort
      - Identify dependencies
```

### 4.3 Definition of Done **[REQUIRED]**

```yaml
definition_of_done:
  code_complete:
    - Feature implemented
    - Unit tests passing
    - Code reviewed
    - Documentation updated

  quality_assured:
    - Integration tests passing
    - Acceptance criteria met
    - No critical bugs
    - Performance validated

  ready_to_ship:
    - Deployed to staging
    - Product owner approved
    - Release notes written
    - Monitoring configured
```

---

## 5. Planning and Execution

### 5.1 Project Charter **[REQUIRED]**

```yaml
project_charter:
  components:
    vision: "Why this project exists"
    objectives: "Measurable goals"
    scope: "In/out boundaries"
    stakeholders: "Key players and roles"
    success_criteria: "How we measure success"
    constraints: "Time, budget, resources"
    assumptions: "What we believe true"
    risks: "Major concerns"

  approval:
    sponsor: "Required"
    stakeholders: "Key ones"
    team: "Commitment"
```

### 5.2 Work Breakdown Structure **[REQUIRED]**

```yaml
wbs_standards:
  principles:
    - 100% rule (all work included)
    - Mutually exclusive elements
    - Outcome-oriented
    - 8-80 hour work packages

  structure:
    level_1: "Project"
    level_2: "Major deliverables"
    level_3: "Components"
    level_4: "Work packages"

  work_package:
    attributes:
      - Clear deliverable
      - Single owner
      - Effort estimate
      - Dependencies
      - Acceptance criteria
```

### 5.3 Estimation Standards **[REQUIRED]**

```yaml
estimation:
  techniques:
    planning_poker:
      scale: "Fibonacci (1,2,3,5,8,13)"
      process: "Reveal simultaneously"

    t_shirt_sizing:
      scale: [XS, S, M, L, XL]
      use: "Initial estimates"

    three_point:
      formula: "(Optimistic + 4*Likely + Pessimistic) / 6"
      use: "Detailed planning"

  best_practices:
    - Estimate as team
    - Include buffer (15-20%)
    - Track actuals
    - Refine over time
```

### 5.4 Schedule Management **[REQUIRED]**

```yaml
scheduling:
  critical_path:
    identify: "Longest duration path"
    monitor: "Weekly updates"
    optimize: "Fast-track or crash"

  milestones:
    types:
      - Phase completion
      - Major deliveries
      - External dependencies
      - Go/no-go decisions

  tracking:
    burndown: "Daily sprint progress"
    burnup: "Release progress"
    velocity: "Team capacity"
    gantt: "Dependencies view"
```

---

## 6. Risk and Issue Management

### 6.1 Risk Management **[REQUIRED]**

```yaml
risk_management:
  identification:
    techniques:
      - Brainstorming
      - SWOT analysis
      - Expert interviews
      - Historical data
      - Security/compliance review (see [NIST_IMPLEMENTATION_GUIDE.md](./docs/nist/NIST_IMPLEMENTATION_GUIDE.md))

  assessment:
    probability: [Low, Medium, High]
    impact: [Low, Medium, High]
    score: "Probability × Impact"

  response_strategies:
    avoid: "Eliminate risk"
    mitigate: "Reduce probability/impact"
    transfer: "Insurance/outsource"
    accept: "Contingency plan"

  monitoring:
    frequency: "Weekly review"
    triggers: "Define thresholds"
    escalation: "Clear paths"
```

### 6.2 Issue Management **[REQUIRED]**

```yaml
issue_management:
  classification:
    severity:
      critical: "Blocks progress"
      high: "Major impact"
      medium: "Workaround exists"
      low: "Minor inconvenience"

  process:
    capture:
      - Description
      - Impact
      - Reporter
      - Date

    triage:
      - Assign owner
      - Set priority
      - Define timeline

    resolution:
      - Root cause
      - Action taken
      - Verification
      - Lessons learned

  escalation:
    level_1: "Team lead (1 day)"
    level_2: "PM (2 days)"
    level_3: "Sponsor (3 days)"
```

---

## 7. Stakeholder Engagement

### 7.1 Stakeholder Analysis **[REQUIRED]**

```yaml
stakeholder_analysis:
  mapping:
    dimensions:
      interest: [Low, Medium, High]
      influence: [Low, Medium, High]

    strategies:
      high_high: "Manage closely"
      high_low: "Keep informed"
      low_high: "Keep satisfied"
      low_low: "Monitor"

  engagement:
    plan:
      - Communication frequency
      - Preferred channels
      - Level of detail
      - Key messages

  raci_matrix:
    responsible: "Does the work"
    accountable: "Owns outcome"
    consulted: "Provides input"
    informed: "Kept updated"
```

### 7.2 Communication Plan **[REQUIRED]**

```yaml
communication:
  channels:
    synchronous:
      - Daily standups
      - Sprint reviews
      - Steering committees
      - War rooms

    asynchronous:
      - Email updates
      - Dashboards
      - Wiki/docs
      - Chat channels

  cadence:
    daily: "Team sync"
    weekly: "Status report"
    bi_weekly: "Stakeholder update"
    monthly: "Steering committee"

  templates:
    status_report:
      - Progress summary
      - Key metrics
      - Risks/issues
      - Next steps

    executive_summary:
      - Business value
      - Timeline status
      - Budget status
      - Key decisions needed
```

---

## 8. Team Excellence

### 8.1 Team Development **[REQUIRED]**

```yaml
team_development:
  stages:
    forming:
      - Set clear expectations
      - Define working agreements
      - Establish communication norms

    storming:
      - Address conflicts openly
      - Facilitate discussions
      - Build trust

    norming:
      - Reinforce positive behaviors
      - Celebrate successes
      - Continuous improvement

    performing:
      - Empower decision-making
      - Foster innovation
      - Scale practices

  practices:
    psychological_safety:
      - Encourage questions
      - Learn from failures
      - Value diverse opinions

    continuous_learning:
      - Regular training
      - Knowledge sharing
      - Experimentation time
```

### 8.2 Performance Management **[REQUIRED]**

```yaml
performance:
  team_metrics:
    velocity: "Story points per sprint"
    quality: "Defect escape rate"
    satisfaction: "Team health surveys"
    predictability: "Commitment accuracy"

  individual_support:
    one_on_ones:
      frequency: "Bi-weekly"
      topics:
        - Progress and blockers
        - Career development
        - Feedback exchange

    growth_plans:
      - Skill assessment
      - Learning objectives
      - Stretch assignments
      - Mentoring
```

### 8.3 Remote Team Standards **[RECOMMENDED]**

```yaml
remote_teams:
  communication:
    - Video-on for meetings
    - Overlap hours defined
    - Response time SLAs
    - Documentation first

  collaboration:
    tools:
      - Video conferencing
      - Virtual whiteboards
      - Async updates
      - Shared workspaces

    practices:
      - Virtual coffee chats
      - Online team building
      - Clear working hours
      - Results over hours
```

---

## 9. Metrics and Reporting

### 9.1 Key Metrics **[REQUIRED]**

```yaml
project_metrics:
  delivery:
    schedule_variance: "Actual vs planned"
    budget_variance: "Actual vs budget"
    scope_creep: "Added vs original"

  quality:
    defect_density: "Bugs per feature"
    test_coverage: "> 80%"
    technical_debt: "Track and plan"
    nist_compliance: "% of security features tagged"

  team:
    velocity_trend: "Improving"
    happiness_index: "> 7/10"
    retention_rate: "> 90%"

  business:
    roi: "Value delivered / cost"
    time_to_market: "Idea to production"
    customer_satisfaction: "> 4/5"
```

### 9.2 Reporting Standards **[REQUIRED]**

```yaml
reporting:
  dashboards:
    real_time:
      - Sprint burndown
      - Build status
      - Current blockers

    weekly:
      - Progress summary
      - Risk heat map
      - Budget burn

    monthly:
      - Trend analysis
      - Milestone status
      - Team metrics

  formats:
    executive:
      - One-page summary
      - Traffic light status
      - Key decisions needed

    detailed:
      - Full metrics
      - Root cause analysis
      - Action plans
```

### 9.3 Continuous Improvement **[REQUIRED]**

```yaml
improvement:
  retrospectives:
    frequency: "Every sprint"
    participation: "Whole team"
    output: "2-3 action items"
    follow_up: "Track completion"

  metrics_review:
    frequency: "Monthly"
    analyze:
      - Trends
      - Anomalies
      - Correlations

  process_optimization:
    - Remove waste
    - Automate repeatable
    - Simplify complex

  compliance_tracking:
    - Monitor NIST control coverage
    - Review security feature tagging
    - Update compliance documentation
    - See [NIST Implementation Guide](./docs/nist/NIST_IMPLEMENTATION_GUIDE.md)
    - Measure impact
```

---

## 10. Implementation Guidelines

### 10.1 Adoption Strategy **[REQUIRED]**

```yaml
adoption:
  phases:
    pilot:
      duration: "1-2 months"
      scope: "Single team"
      focus: "Core practices"

    rollout:
      duration: "3-6 months"
      scope: "Department"
      focus: "Standardization"

    scale:
      duration: "6-12 months"
      scope: "Organization"
      focus: "Optimization"

  success_factors:
    - Executive sponsorship
    - Team buy-in
    - Training investment
    - Tool support
    - Regular coaching
```

### 10.2 Maturity Model **[RECOMMENDED]**

```yaml
maturity_levels:
  level_1_initial:
    - Ad hoc processes
    - Hero culture
    - Reactive mode

  level_2_managed:
    - Basic standards
    - Regular planning
    - Some metrics

  level_3_defined:
    - Documented processes
    - Consistent practices
    - Proactive management

  level_4_quantified:
    - Data-driven decisions
    - Predictable delivery
    - Continuous improvement

  level_5_optimizing:
    - Innovation culture
    - Self-organizing
    - Industry leader
```

### 10.3 Common Pitfalls **[REQUIRED]**

```yaml
avoid:
  process_over_people:
    - Rigid adherence to process
    - Ignoring team feedback
    - Documentation overload

  planning_paralysis:
    - Over-planning upfront
    - Resisting change
    - Perfect vs good enough

  metrics_madness:
    - Measuring everything
    - Gaming the system
    - Quantity over quality

  communication_breakdown:
    - Information silos
    - Assuming understanding
    - Delayed escalation

remedies:
  - Start simple, evolve
  - Focus on outcomes
  - Empower teams
  - Fail fast, learn faster
```

### 10.4 Tools and Automation **[RECOMMENDED]**

```yaml
tool_categories:
  project_management:
    examples: [Jira, Azure DevOps, Asana]
    capabilities:
      - Backlog management
      - Sprint planning
      - Progress tracking

  collaboration:
    examples: [Slack, Teams, Miro]
    capabilities:
      - Real-time chat
      - Video conferencing
      - Virtual whiteboarding

  reporting:
    examples: [PowerBI, Tableau, Grafana]
    capabilities:
      - Real-time dashboards
      - Trend analysis
      - Custom reports

  automation:
    focus:
      - Status updates
      - Metric collection
      - Report generation
      - Notifications
```

---

## Quick Reference

### Sprint Checklist
```yaml
sprint_checklist:
  before:
    - [ ] Backlog refined
    - [ ] Capacity confirmed
    - [ ] Dependencies identified

  during:
    - [ ] Daily standups held
    - [ ] Board updated
    - [ ] Blockers addressed

  after:
    - [ ] Demo completed
    - [ ] Retrospective held
    - [ ] Metrics updated
```

### RACI Template
```yaml
raci_template:
  decisions:
    technical: "R: Tech Lead, A: Architect, C: Team, I: PM"
    business: "R: PM, A: Product Owner, C: Sponsor, I: Team"
    budget: "R: PM, A: Sponsor, C: Finance, I: Team"
```

### Risk Register Template
```yaml
risk_template:
  fields:
    - ID: "RISK-001"
    - Description: "Key developer may leave"
    - Probability: "Medium"
    - Impact: "High"
    - Response: "Document knowledge, pair programming"
    - Owner: "Tech Lead"
    - Status: "Monitoring"
```

---

**Remember:** These standards are guidelines. Adapt them to your context while maintaining the core principles of transparency, collaboration, and continuous improvement.

## Implementation

### Getting Started

1. Review the relevant sections of this standard for your use case
2. Identify which guidelines apply to your project
3. Implement the required practices and patterns
4. Validate compliance using the provided checklists

### Implementation Checklist

- [ ] Review and understand applicable standards
- [ ] Implement required practices
- [ ] Follow recommended patterns
- [ ] Validate implementation against guidelines
- [ ] Document any deviations with justification
