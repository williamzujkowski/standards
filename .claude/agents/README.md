# Claude Code Agents Directory Structure

## Index

- [code-analyzer](analysis/code-analyzer.md)

### Github

- [code-review-swarm](github/code-review-swarm.md)
- [github-modes](github/github-modes.md)
- [issue-tracker](github/issue-tracker.md)
- [multi-repo-swarm](github/multi-repo-swarm.md)
- [pr-manager](github/pr-manager.md)
- [project-board-sync](github/project-board-sync.md)
- [release-manager](github/release-manager.md)
- [release-swarm](github/release-swarm.md)
- [repo-architect](github/repo-architect.md)
- [swarm-issue](github/swarm-issue.md)
- [swarm-pr](github/swarm-pr.md)
- [sync-coordinator](github/sync-coordinator.md)
- [workflow-automation](github/workflow-automation.md)

### Optimization

- [benchmark-suite](optimization/benchmark-suite.md)
- [load-balancer](optimization/load-balancer.md)
- [performance-monitor](optimization/performance-monitor.md)
- [resource-allocator](optimization/resource-allocator.md)
- [topology-optimizer](optimization/topology-optimizer.md)

### Sparc

- [architecture](sparc/architecture.md)
- [pseudocode](sparc/pseudocode.md)
- [refinement](sparc/refinement.md)
- [specification](sparc/specification.md)

### Consensus

- [byzantine-coordinator](consensus/byzantine-coordinator.md)
- [crdt-synchronizer](consensus/crdt-synchronizer.md)
- [gossip-coordinator](consensus/gossip-coordinator.md)
- [performance-benchmarker](consensus/performance-benchmarker.md)
- [quorum-manager](consensus/quorum-manager.md)
- [raft-manager](consensus/raft-manager.md)
- [security-manager](consensus/security-manager.md)

### Templates

- [automation-smart-agent](templates/automation-smart-agent.md)
- [coordinator-swarm-init](templates/coordinator-swarm-init.md)
- [github-pr-manager](templates/github-pr-manager.md)
- [implementer-sparc-coder](templates/implementer-sparc-coder.md)
- [memory-coordinator](templates/memory-coordinator.md)
- [migration-plan](templates/migration-plan.md)
- [orchestrator-task](templates/orchestrator-task.md)
- [performance-analyzer](templates/performance-analyzer.md)
- [sparc-coordinator](templates/sparc-coordinator.md)

### Swarm

- [adaptive-coordinator](swarm/adaptive-coordinator.md)
- [hierarchical-coordinator](swarm/hierarchical-coordinator.md)
- [mesh-coordinator](swarm/mesh-coordinator.md)

### Core

- [coder](core/coder.md)
- [planner](core/planner.md)
- [researcher](core/researcher.md)
- [reviewer](core/reviewer.md)
- [tester](core/tester.md)

This directory contains sub-agent definitions organized by type and purpose. Each agent has specific capabilities, tool restrictions, and naming conventions that trigger automatic delegation.

## Directory Structure

```
.claude/agents/
├── README.md                    # This file
├── _templates/                  # Agent templates
│   ├── base-agent.yaml
│   └── agent-types.md
├── development/                 # Development agents
│   ├── backend/
│   ├── frontend/
│   ├── fullstack/
│   └── api/
├── testing/                     # Testing agents
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── performance/
├── architecture/                # Architecture agents
│   ├── system-design/
│   ├── database/
│   ├── cloud/
│   └── security/
├── devops/                      # DevOps agents
│   ├── ci-cd/
│   ├── infrastructure/
│   ├── monitoring/
│   └── deployment/
├── documentation/               # Documentation agents
│   ├── api-docs/
│   ├── user-guides/
│   ├── technical/
│   └── readme/
├── analysis/                    # Analysis agents
│   ├── code-review/
│   ├── performance/
│   ├── security/
│   └── refactoring/
├── data/                        # Data agents
│   ├── etl/
│   ├── analytics/
│   ├── ml/
│   └── visualization/
└── specialized/                 # Specialized agents
    ├── mobile/
    ├── embedded/
    ├── blockchain/
    └── ai-ml/
```

## Naming Conventions

Agent files follow this naming pattern:
`[type]-[specialization]-[capability].agent.yaml`

Examples:

- `dev-backend-api.agent.yaml`
- `test-unit-jest.agent.yaml`
- `arch-cloud-aws.agent.yaml`
- `docs-api-openapi.agent.yaml`

## Automatic Delegation Triggers

Claude Code automatically delegates to agents based on:

1. **Keywords in user request**: "test", "deploy", "document", "review"
2. **File patterns**: `*.test.js` → testing agent, `*.tf` → infrastructure agent
3. **Task complexity**: Multi-step tasks spawn coordinator agents
4. **Domain detection**: Database queries → data agent, API endpoints → backend agent

## Tool Restrictions

Each agent type has specific tool access:

- **Development agents**: Full file system access, code execution
- **Testing agents**: Test runners, coverage tools, limited write access
- **Architecture agents**: Read-only access, diagram generation
- **Documentation agents**: Markdown tools, read access, limited write to docs/
- **DevOps agents**: Infrastructure tools, deployment scripts, environment access
- **Analysis agents**: Read-only access, static analysis tools
