# NIST LLM Context Management System

The `.nist/control-context.json` file provides a comprehensive context for LLMs to understand and suggest NIST 800-53r5 controls intelligently.

## Overview

This system enables:
- 🤖 **Smart Control Suggestions** - Pattern-based control recommendations
- 📚 **Implementation Guidance** - Language-specific examples and libraries
- 🎯 **Project Context** - Baseline and focus area customization
- 🔍 **Evidence Requirements** - Clear evidence collection guidance
- 💬 **LLM Integration** - Pre-built prompts for AI assistants

## Structure

### Project Configuration
```json
{
  "project": {
    "name": "Your Project Name",
    "baseline": "moderate",
    "primaryLanguages": ["typescript", "python"],
    "securityFocus": ["authentication", "encryption"]
  }
}
```

### Control Descriptions
Enhanced control information with:
- Implementation guidance
- Common patterns
- Project-specific examples

### Implementation Patterns
Language-specific examples for common security patterns:
- Authentication
- Authorization
- Encryption
- Logging
- Validation

### Auto-tagging Rules
Pattern matching for automatic control suggestions based on code content.

## Usage

### CLI Commands

```bash
# Suggest controls for a file
npm run nist-context suggest src/auth.ts

# Get implementation guidance
npm run nist-context guidance ia-2 typescript

# Check evidence requirements
npm run nist-context evidence code

# Export context for LLM
npm run nist-context export-llm -o llm-context.json

# Update project baseline
npm run nist-context update-baseline high
```

### In Your IDE

The VS Code extension uses this context to provide:
- Real-time control suggestions
- Implementation snippets
- Evidence type hints

### With LLMs

When using AI assistants, reference the context:
```
Load the NIST context from .nist/control-context.json
Suggest controls for the following authentication code...
```

## Customization

### Adding Project-Specific Controls

Edit `control-context.json` to add custom controls:
```json
"controlDescriptions": {
  "custom-1": {
    "title": "Custom Security Control",
    "summary": "Project-specific requirement",
    "implementation_guidance": "How to implement",
    "common_patterns": ["pattern1", "pattern2"],
    "project_examples": ["Example 1", "Example 2"]
  }
}
```

### Updating Auto-tagging Rules

Add patterns for your codebase:
```json
"autoTaggingRules": {
  "patterns": [
    {
      "regex": "\\byour_security_function\\b",
      "suggestedControls": ["ac-3", "au-2"],
      "confidence": "high"
    }
  ]
}
```

### Language-Specific Examples

Add examples for your tech stack:
```json
"implementationPatterns": {
  "your_pattern": {
    "controls": ["ia-2"],
    "description": "Your pattern description",
    "rust": {
      "example": "fn authenticate(creds: &Credentials) -> Result<User>",
      "libraries": ["actix-identity", "argon2"],
      "testingApproach": "Property-based testing"
    }
  }
}
```

## Integration Points

### Git Hooks
Pre-commit hooks use this context to suggest missing controls.

### CI/CD
GitHub Actions use this context for compliance validation.

### Documentation
SSP generator uses this context for control descriptions.

### Testing
Test generators use implementation patterns for security tests.

## Best Practices

1. **Keep Context Updated**: Update when adding new security features
2. **Language Coverage**: Add examples for all languages in use
3. **Evidence Types**: Define what constitutes valid evidence
4. **Regular Reviews**: Review auto-tagging rules quarterly

## Troubleshooting

### Context Not Loading
- Check file exists: `.nist/control-context.json`
- Validate JSON syntax
- Ensure read permissions

### No Suggestions
- Check auto-tagging is enabled
- Review pattern regex syntax
- Verify code matches patterns

### Wrong Language Examples
- Update `primaryLanguages` in project config
- Add language-specific patterns
