# Agents Directory

**Last Updated**: 2025-10-24 19:21:55 EDT (UTC-04:00)
**Agent Count**: 65 agent definitions (verified)
**Location**: `.claude/agents/`

## Overview

This directory serves as a reference point for the agent definitions used in the standards repository. The actual agent definitions are located in `.claude/agents/` and follow Anthropic's agent delegation patterns.

## Agent Statistics

**Verified Count**: 2025-10-24 19:21:55 EDT (UTC-04:00)

- **Total Agent Definitions**: 65 markdown files
- **Categories**: 18 directories
- **Primary Location**: `/home/william/git/standards/.claude/agents/`

## Directory Structure

```
.claude/agents/
├── README.md                    # Agent directory index
├── analysis/                    # Code analysis agents (3)
├── architecture/                # Architecture design agents (1)
├── consensus/                   # Consensus coordination agents (7)
├── core/                        # Core development agents (5)
├── data/                        # Data processing agents (1)
├── development/                 # Development workflow agents (1)
├── devops/                      # DevOps & deployment agents (1)
├── documentation/               # Documentation agents (1)
├── github/                      # GitHub integration agents (13)
├── hive-mind/                   # Hive mind collective agents (1)
├── optimization/                # Performance optimization agents (5)
├── sparc/                       # SPARC methodology agents (4)
├── specialized/                 # Specialized domain agents (1)
├── swarm/                       # Swarm coordination agents (3)
└── base-template-generator.md  # Base template agent
```

## Agent Categories

### Core Development (5 agents)

Located in `.claude/agents/core/`

- `coder`: Primary development implementation
- `planner`: Project planning and task decomposition
- `researcher`: Information gathering and analysis
- `reviewer`: Code review and quality assurance
- `tester`: Test creation and validation

### GitHub Integration (13 agents)

Located in `.claude/agents/github/`

- `code-review-swarm`: Automated PR reviews
- `github-modes`: Multi-mode GitHub operations
- `issue-tracker`: Issue management and triage
- `multi-repo-swarm`: Cross-repository coordination
- `pr-manager`: Pull request lifecycle management
- `project-board-sync`: Project board automation
- `release-manager`: Release coordination
- `release-swarm`: Multi-repository releases
- `repo-architect`: Repository structure design
- `swarm-issue`: Swarm-based issue resolution
- `swarm-pr`: Swarm-based PR management
- `sync-coordinator`: Repository synchronization
- `workflow-automation`: CI/CD workflow automation

### Swarm Coordination (3 agents)

Located in `.claude/agents/swarm/`

- `adaptive-coordinator`: Dynamic topology adaptation
- `hierarchical-coordinator`: Hierarchical task delegation
- `mesh-coordinator`: Peer-to-peer coordination

### Consensus & Distributed (7 agents)

Located in `.claude/agents/consensus/`

- `byzantine-coordinator`: Byzantine fault tolerance
- `crdt-synchronizer`: Conflict-free replicated data types
- `gossip-coordinator`: Gossip protocol coordination
- `performance-benchmarker`: Performance testing
- `quorum-manager`: Quorum-based decision making
- `raft-manager`: Raft consensus protocol
- `security-manager`: Security policy enforcement

### Performance & Optimization (5 agents)

Located in `.claude/agents/optimization/`

- `benchmark-suite`: Comprehensive benchmarking
- `load-balancer`: Task load distribution
- `performance-monitor`: Real-time performance tracking
- `resource-allocator`: Resource allocation optimization
- `topology-optimizer`: Swarm topology optimization

### SPARC Methodology (4 agents)

Located in `.claude/agents/sparc/`

- `architecture`: System architecture design
- `pseudocode`: Pseudocode specification
- `refinement`: Code refinement and optimization
- `specification`: Requirements specification

### Analysis (3 agents)

Located in `.claude/agents/analysis/`

- `code-analyzer`: Static code analysis
- `code-review/analyze-code-quality`: Quality metrics analysis
- Additional analysis subdirectories

## Usage Patterns

### Direct Agent Reference

Agents are referenced in CLAUDE.md and used by Claude Code for task delegation:

```markdown
## Agent Types for Task Tool (65 Available)

**Note**: These are conceptual agent types used with the Task tool,
not separate callable tools. Agent definitions are located in
`.claude/agents/` directory.
```

### Automatic Delegation

Claude Code automatically delegates to agents based on:

1. **Keywords in user request**: "test", "deploy", "document", "review"
2. **File patterns**: `*.test.js` → testing agent, `*.tf` → infrastructure agent
3. **Task complexity**: Multi-step tasks spawn coordinator agents
4. **Domain detection**: Database queries → data agent, API endpoints → backend agent

### Tool Restrictions

Each agent type has specific tool access as defined in their respective markdown files:

- **Development agents**: Full file system access, code execution
- **Testing agents**: Test runners, coverage tools, limited write access
- **Architecture agents**: Read-only access, diagram generation
- **Documentation agents**: Markdown tools, read access, limited write to docs/
- **DevOps agents**: Infrastructure tools, deployment scripts, environment access
- **Analysis agents**: Read-only access, static analysis tools

## Relationship to Skills

Agents complement the skills system:

- **Skills** (61 total): Domain knowledge and implementation patterns
- **Agents** (65 total): Task delegation and workflow orchestration

**Skills** provide the "what" (standards, patterns, best practices)
**Agents** provide the "how" (task execution, coordination, tooling)

## Documentation Standards

All agent definitions follow these standards:

### Datetime Format

- **Standard**: NIST ET (America/New_York)
- **Format**: ISO 8601 with timezone offset
- **Example**: `2025-10-24 19:21:55 EDT (UTC-04:00)`

### Metadata Requirements

- Version number
- Last updated timestamp (NIST ET)
- Description and purpose
- Tool restrictions
- Delegation triggers

## Verification

**Last Audit**: 2025-10-24 19:21:55 EDT (UTC-04:00)

```bash
# Verify agent count
find .claude/agents -type f -name "*.md" | wc -l
# Output: 65

# List agent categories
ls -1 .claude/agents/
# Output: 18 directories + files
```

## Integration with CLAUDE.md

The main CLAUDE.md file references these agents and provides:

- Agent type categorization
- Usage examples
- Coordination protocols
- MCP tool integration
- Concurrent execution patterns

## Migration Notes

When migrating or updating agents:

1. **Preserve datetime format**: Always use NIST ET timezone
2. **Update counts**: Run verification commands after changes
3. **Document changes**: Update README with timestamp
4. **Validate structure**: Ensure agent definitions follow standards
5. **Test delegation**: Verify automatic delegation triggers work

## Support & Resources

### Primary Documentation

- **Main Router**: [CLAUDE.md](../CLAUDE.md)
- **Agent Index**: [.claude/agents/README.md](../.claude/agents/README.md)
- **Skills System**: [skills/README.md](../skills/README.md)

### Related Guides

- [Migration Guide](../docs/migration/MIGRATION_GUIDE.md)
- [Skills User Guide](../docs/guides/SKILLS_USER_GUIDE.md)
- [Product Matrix](../config/product-matrix.yaml)

### Verification Tools

```bash
# Count agents
find .claude/agents -type f -name "*.md" | wc -l

# List agent categories
ls -1 .claude/agents/

# Check for datetime format compliance
grep -r "EDT\|EST" .claude/agents/ | head -5
```

---

**Maintained by**: Standards Repository Team
**Repository**: https://github.com/williamzujkowski/standards
**Datetime Standard**: NIST ET (America/New_York) - ISO 8601 format
