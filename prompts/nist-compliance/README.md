# NIST Compliance LLM Prompts

A collection of battle-tested prompts for leveraging LLMs in NIST 800-53r5 compliance implementation.

## 🎯 Purpose

These prompts help developers and security teams:
- Identify applicable NIST controls for their code
- Get implementation guidance with examples
- Review code for compliance gaps
- Generate evidence documentation
- Prioritize remediation efforts

## 📚 Prompt Categories

### 1. Control Suggestion (`control-suggestion-prompt.md`)
**When to use**: You have code that needs NIST tags but don't know which controls apply

**Example use case**:
```
"I have an authentication function. What NIST controls should I tag it with?"
```

### 2. Implementation Guide (`implementation-guide-prompt.md`)
**When to use**: You need to implement a specific NIST control from scratch

**Example use case**:
```
"Show me how to implement NIST au-2 (audit logging) in Python with FastAPI"
```

### 3. Gap Analysis (`gap-analysis-prompt.md`)
**When to use**: You need to identify missing controls and prioritize implementation

**Example use case**:
```
"What NIST controls am I missing for moderate baseline compliance?"
```

### 4. Code Review (`code-review-prompt.md`)
**When to use**: You want to review existing code for compliance issues

**Example use case**:
```
"Review my authentication module for NIST compliance issues"
```

### 5. Complete Library (`NIST_PROMPT_LIBRARY.md`)
**When to use**: Reference for all available prompts and advanced use cases

## 🚀 Quick Start

### Step 1: Choose Your Scenario

| I want to... | Use this prompt |
|--------------|-----------------|
| Add NIST tags to existing code | `control-suggestion-prompt.md` |
| Implement a new security feature | `implementation-guide-prompt.md` |
| Find what I'm missing | `gap-analysis-prompt.md` |
| Review code before commit | `code-review-prompt.md` |
| Generate documentation | See `NIST_PROMPT_LIBRARY.md` |

### Step 2: Customize the Prompt

All prompts have placeholders marked with `[BRACKETS]`. Replace with your specifics:
- `[LANGUAGE]`: Your programming language (Python, JavaScript, Go, etc.)
- `[FRAMEWORK]`: Your framework (Django, Express, React, etc.)
- `[CONTROL-ID]`: Specific NIST control (ia-2, au-3, etc.)
- `[CODE]`: Your actual code snippet

### Step 3: Get Better Results

**DO** ✅:
- Include actual code, not descriptions
- Specify your tech stack
- Mention your baseline (usually moderate)
- Provide context about your application
- Ask for specific output formats

**DON'T** ❌:
- Use vague descriptions
- Omit language/framework details
- Forget to validate results
- Implement without testing
- Skip the evidence collection

## 📖 Example Workflow

### Scenario: Adding NIST compliance to an existing login function

1. **Start with control suggestions**:
```
Use: control-suggestion-prompt.md
Input: Your login function code
Output: List of applicable controls with explanations
```

2. **Get implementation details**:
```
Use: implementation-guide-prompt.md
Input: "Implement au-2 for authentication logging in Python"
Output: Step-by-step implementation with code
```

3. **Review your changes**:
```
Use: code-review-prompt.md
Input: Your updated code with NIST tags
Output: Validation and improvement suggestions
```

4. **Check overall compliance**:
```
Use: gap-analysis-prompt.md
Input: List of implemented controls
Output: Missing controls and priority roadmap
```

## 🔧 Integration Ideas

### Git Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Get staged files
files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(py|js|go)$')

for file in $files; do
    echo "Checking $file for NIST compliance..."
    # Use LLM with code-review-prompt.md
    # Block commit if critical issues found
done
```

### CI/CD Pipeline
```yaml
- name: NIST Compliance Check
  run: |
    # Use gap-analysis-prompt.md to check coverage
    # Fail build if below threshold
```

### IDE Integration
```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Suggest NIST Controls",
      "type": "shell",
      "command": "llm-cli --prompt control-suggestion-prompt.md --file ${file}"
    }
  ]
}
```

## 💡 Pro Tips

### 1. Chain Prompts for Complex Tasks
```
First: Use gap-analysis-prompt.md to find missing controls
Then: Use implementation-guide-prompt.md for each missing control
Finally: Use code-review-prompt.md to validate
```

### 2. Create Project-Specific Variations
```
Copy prompt → Add your tech stack details → Save as team template
```

### 3. Build a Knowledge Base
```
Save good responses → Create internal documentation → Train team
```

### 4. Validate with Official Sources
```
LLM suggestions → Check NIST docs → Implement → Test → Document
```

## 📊 Measuring Success

Track these metrics:
- **Coverage**: % of security features with NIST tags
- **Accuracy**: % of correctly mapped controls
- **Completeness**: % of required controls implemented
- **Evidence**: % of controls with test coverage
- **Time Saved**: Hours reduced in compliance work

## 🤝 Contributing

To add new prompts:
1. Create a new `.md` file in this directory
2. Follow the existing format
3. Include real-world examples
4. Test with multiple LLMs
5. Add to this README

## ⚠️ Important Notes

1. **LLMs are assistants, not authorities** - Always verify suggestions
2. **Context matters** - Provide complete information for better results
3. **Test everything** - Generated code needs validation
4. **Document decisions** - Keep track of why controls were chosen
5. **Stay updated** - NIST standards evolve, so should these prompts

## 🔗 Related Resources

- [NIST 800-53r5 Official Documentation](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [OSCAL Documentation](https://pages.nist.gov/OSCAL/)
- Project Templates: `/examples/nist-templates/`
- VS Code Extension: `/.vscode/nist-extension/`
- Context Management: `/.nist/control-context.json`

## 📝 License

These prompts are part of the Software Development Standards repository and are available under the same license terms.
