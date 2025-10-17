# Threat Modeling Templates

This directory contains practical templates for conducting threat modeling exercises.

## Available Templates

### 1. stride-template.md

Complete STRIDE threat model template with:

- System overview and architecture
- STRIDE analysis tables for each category
- DREAD scoring
- Mitigation planning
- Risk assessment (NIST RA-3)

**Use for:** Complete threat modeling documentation

### 2. data-flow-diagram.md

Data flow diagram (DFD) creation template with:

- DFD notation guide
- Component inventory tables
- Trust boundary mapping
- Common DFD patterns

**Use for:** Visualizing system architecture and data flows

### 3. threat-scenario.md

Attack scenario and attack tree template with:

- Step-by-step attack paths
- Attack tree visualization
- Impact analysis
- Detection and response planning

**Use for:** Documenting specific attack scenarios

### 4. mitigation-plan.md

Comprehensive mitigation tracking template with:

- Threat prioritization matrix
- Implementation phases
- Resource allocation
- Progress tracking
- NIST control mapping

**Use for:** Managing mitigation implementation

## Quick Start

1. **Start with DFD**: Create data flow diagram to understand your system
2. **Apply STRIDE**: Use stride-template.md to identify threats
3. **Build Attack Trees**: Document scenarios with threat-scenario.md
4. **Plan Mitigations**: Track implementation with mitigation-plan.md

## Integration

These templates work together as a complete threat modeling workflow:

```
DFD → STRIDE Analysis → Attack Scenarios → Mitigation Plan
```

## Customization

All templates are Markdown-based and can be:

- Version controlled in Git
- Customized for your organization
- Converted to other formats (PDF, HTML)
- Integrated with issue tracking systems
