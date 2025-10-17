I'll help you create a comprehensive prompt to align your standards repo with Anthropic's new agent skills format. Let me first examine both the Anthropic documentation and your current standards repository to understand the alignment needed.Based on my analysis of your standards repository and Anthropic's new Agent Skills format, I'll create a comprehensive prompt for Claude Flow to help you modernize your standards repo. Your repository already has excellent content that aligns well with the Skills philosophy - it just needs restructuring to follow the new format.

## **Claude Flow Prompt for Standards-to-Skills Migration**

```markdown
# Mission: Transform Standards Repository into Anthropic Agent Skills Format

You are an expert agent swarm tasked with modernizing the williamzujkowski/standards repository to align with Anthropic's new Agent Skills architecture while preserving all existing value and enhancing functionality.

## Context & Objectives

### Current State Analysis
- Repository: https://github.com/williamzujkowski/standards/
- Contains 24+ comprehensive standards documents covering software development
- Has token optimization system (CLAUDE.md with 90% reduction)
- Includes NIST compliance features, templates, and automation scripts
- Uses a loading system with @load patterns for selective content

### Target State (Agent Skills Format)
- Transform each standard into a self-contained Skill directory
- Implement progressive disclosure (Level 1: metadata, Level 2: instructions, Level 3: resources)
- Create SKILL.md files with YAML frontmatter (name, description)
- Bundle related scripts, templates, and resources within each skill
- Maintain backward compatibility with existing usage patterns

## Transformation Tasks

### Phase 1: Repository Structure Analysis
1. **Inventory Current Standards**
   - Map all .md files in docs/standards/
   - Identify dependencies and cross-references
   - Catalog associated templates, scripts, and resources
   - Document the token optimization patterns in CLAUDE.md

2. **Create Skills Hierarchy**
   ```
   skills/
   ├── coding-standards/
   │   ├── SKILL.md
   │   ├── languages/
   │   │   ├── python.md
   │   │   ├── javascript.md
   │   │   └── go.md
   │   └── templates/
   ├── security-nist/
   │   ├── SKILL.md
   │   ├── controls/
   │   ├── templates/
   │   └── scripts/
   ├── testing/
   │   ├── SKILL.md
   │   ├── unit-testing.md
   │   ├── integration-testing.md
   │   └── test-templates/
   └── [additional skills...]
   ```

### Phase 2: Skills Creation Strategy

For each standard, create a skill following this pattern:

```yaml
---
name: [skill-name]
description: [Clear description of what this skill does, when Claude should use it, and key capabilities - max 1024 chars]
---

# [Skill Title]

## Overview
[Brief introduction - this loads at Level 2]

## When to Use This Skill
[Clear triggers and use cases]

## Core Instructions
[Main procedural knowledge]

## Advanced Topics
[Reference to additional files that load at Level 3]
- For [specific topic], see `./resources/[file].md`
- For templates, access `./templates/`
- For scripts, run `./scripts/[script].sh`

## Examples
[2-3 concrete usage examples]
```

### Phase 3: Specific Transformation Rules

#### 1. **Unified Standards → Multiple Focused Skills**
Split UNIFIED_STANDARDS.md into:
- `core-practices/SKILL.md` - Fundamental principles
- `code-quality/SKILL.md` - Code standards
- `architecture/SKILL.md` - System design patterns

#### 2. **CLAUDE.md → Meta-Skill Loader**
Transform into `skill-loader/SKILL.md`:
```yaml
---
name: skill-loader
description: Intelligent skill discovery and loading system that identifies which skills are needed based on natural language requests and loads them progressively
---
```

#### 3. **NIST Compliance → Dedicated Skill**
Create `nist-compliance/SKILL.md`:
- Bundle all NIST templates, scripts, and VS Code extension
- Include control mappings as loadable resources
- Integrate SSP generation tools

#### 4. **Language-Specific Standards → Composable Skills**
Create individual skills:
- `python-standards/SKILL.md`
- `javascript-standards/SKILL.md`
- `go-standards/SKILL.md`

### Phase 4: Enhancement Opportunities

#### Progressive Disclosure Implementation
1. **Level 1 (Metadata)**: Only name + description in frontmatter
2. **Level 2 (Core Instructions)**: Main SKILL.md body (<5k tokens)
3. **Level 3 (Resources)**: Additional files loaded on-demand

#### Token Optimization
- Preserve the existing @load pattern as a resource discovery mechanism
- Create index files for quick reference
- Use executable scripts for complex operations (no token cost)

#### Backward Compatibility
- Create a `legacy-bridge/SKILL.md` that maps old references to new skills
- Maintain original file structure in an archive/ directory
- Provide migration scripts for existing users

### Phase 5: Quality Assurance

#### Validation Checklist
- [ ] Each skill has proper YAML frontmatter
- [ ] Descriptions clearly indicate when to use the skill
- [ ] No skill exceeds 5k tokens in main body
- [ ] Resources are properly referenced, not embedded
- [ ] Cross-skill dependencies are documented
- [ ] Scripts are executable and tested
- [ ] Templates are validated

#### Testing Strategy
1. Create test scenarios for each skill
2. Validate progressive loading behavior
3. Test composability (multiple skills working together)
4. Verify backward compatibility

## Implementation Workflow

### Step 1: Skill Mapping
Create a mapping document showing:
```
Current File → Target Skill(s)
UNIFIED_STANDARDS.md → core-practices/, code-quality/, architecture/
CODING_STANDARDS.md → language-specific skills (python/, js/, go/)
MODERN_SECURITY_STANDARDS.md → security-practices/, zero-trust/
```

### Step 2: Skill Templates
For each identified skill, generate:
1. SKILL.md with proper frontmatter
2. Directory structure for resources
3. Migration of relevant content
4. Script/template organization

### Step 3: Cross-References
Update all cross-references to use skill-based paths:
- Old: `See CODING_STANDARDS.md#python`
- New: `Load python-standards skill for details`

### Step 4: Documentation
Create:
- README explaining the new structure
- Migration guide for existing users
- Skill authoring guide for contributors

## Success Metrics

1. **Token Efficiency**: Maintain or improve 90% reduction
2. **Discoverability**: Skills are auto-discovered based on context
3. **Composability**: Skills work together seamlessly
4. **Maintainability**: Each skill is self-contained and versioned
5. **Compatibility**: Existing workflows continue to function

## Additional Considerations

### Security Skills
- Create audit-friendly skill structures
- Include security scanning scripts
- Bundle NIST control validators

### Performance Optimization
- Lazy loading of heavy resources
- Caching mechanisms for frequently used skills
- Efficient skill discovery algorithms

### Community Contribution
- Template for community skills
- Validation pipeline for submissions
- Skill marketplace structure

## Output Deliverables

1. **Restructured Repository**
   - New skills/ directory with all converted standards
   - Preserved original structure in archive/
   - Updated documentation

2. **Migration Toolkit**
   - Automated conversion scripts
   - Validation tools
   - Rollback procedures

3. **Skills Catalog**
   - Complete inventory of available skills
   - Dependency graph
   - Usage examples

4. **Integration Guide**
   - How to use with Claude API
   - Claude Code integration
   - CI/CD pipeline updates

Start by analyzing the current repository structure and creating a detailed transformation plan. Focus on preserving all existing value while enhancing with Skills capabilities.
```

## **Key Transformation Highlights**

Your standards repo is already well-architected for this transformation:

1. **Natural Skill Boundaries**: Your existing standards naturally map to focused skills (coding, testing, security, etc.)

2. **Token Optimization Synergy**: Your CLAUDE.md loading system aligns perfectly with Skills' progressive disclosure principle

3. **NIST as a Premium Skill**: Your NIST compliance features become a powerful, self-contained skill with bundled tools

4. **Template Preservation**: All your templates become Level 3 resources that load only when needed

5. **Automation Scripts**: Convert to executable resources that don't consume tokens

This migration will make your standards:
- **More discoverable** - Claude automatically identifies relevant skills
- **More efficient** - Progressive loading reduces token usage further
- **More maintainable** - Each skill is independently versioned
- **More powerful** - Skills can execute code and scripts directly
- **More composable** - Multiple skills work together seamlessly

The swarm should prioritize maintaining backward compatibility while adding the new Skills capabilities, ensuring a smooth transition for existing users.
