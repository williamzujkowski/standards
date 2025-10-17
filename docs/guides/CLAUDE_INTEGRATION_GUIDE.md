# Claude API & Claude Code Integration Guide

**Version**: 1.0.0
**Target Audience**: Developers using Claude API or Claude Code CLI
**Last Updated**: 2025-10-16

---

## Overview

This guide shows how to integrate the Skills system with Claude API (programmatic) and Claude Code (CLI). Skills dramatically improve context efficiency and development workflows when using Claude.

---

## Quick Benefits

### Before Skills
```python
# Load entire standards (250,000+ tokens)
with open('docs/standards/UNIFIED_STANDARDS.md') as f:
    standards = f.read()

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": f"{standards}\n\nImplement user authentication"
    }]
)
# Token cost: ~250,000 input tokens
# Context overload: Claude sees too much irrelevant content
```

### After Skills
```python
# Load only what's needed (1,755 tokens for Level 1)
skills = load_skills(['coding-standards', 'security-practices', 'testing', 'nist-compliance'], level=1)

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": f"{skills}\n\nImplement user authentication"
    }]
)
# Token cost: ~1,755 input tokens (99.3% reduction)
# Better context: Claude sees only relevant guidance
```

**Result**: 99%+ token reduction, better responses, lower costs

---

## Claude Code CLI Integration

### Installation

```bash
# Install Claude Code (if not installed)
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version
```

### Project Setup

#### 1. Add CLAUDE.md

Create `/path/to/project/CLAUDE.md`:

```markdown
# Project Standards Configuration

## Skills Auto-Loading

This project uses the Skills system for progressive standards loading.

### Auto-Load Configuration

```bash
# Recommended skills for this project
@load product:api --language python

# This auto-loads:
# - coding-standards (Python patterns)
# - security-practices (API security)
# - testing (pytest best practices)
# - nist-compliance (AC, IA, AU controls)
```

### Quick Commands

```bash
# Load skills
@load product:api

# Get recommendations
npm run skill-loader -- recommend ./

# Validate compliance
python scripts/validate-nist-tags.py
```

### Project Context

- **Type**: REST API
- **Language**: Python 3.11
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Standards**: NIST 800-53r5 (AC, IA, AU families)
```

#### 2. Add .claudeignore

Create `/path/to/project/.claudeignore`:

```
# Ignore large files
*.log
*.db
*.sqlite

# Ignore generated files
.claude/cache/
reports/generated/
node_modules/
__pycache__/

# Ignore sensitive files
.env
.env.*
secrets/
credentials/
```

#### 3. Add Skills Loader Script

Add to `package.json`:

```json
{
  "scripts": {
    "skill-loader": "node scripts/skill-loader.js",
    "skills:recommend": "npm run skill-loader -- recommend ./",
    "skills:load": "npm run skill-loader -- load product:api --level 1 --output .claude/skills.md",
    "skills:validate": "python scripts/validate-skills.py skills/"
  }
}
```

### Usage with Claude Code

#### Interactive Mode

```bash
# Start Claude Code
claude

# Claude reads CLAUDE.md automatically and sees:
# - Skills configuration
# - Project context
# - Auto-load recommendations

# You can reference skills directly:
> Implement user authentication following skill:security-practices

# Or load additional skills mid-conversation:
> @load skill:nist-compliance --level 2
> Tag the authentication code with NIST controls
```

#### Command Mode

```bash
# Load skills and execute task
claude --load-skills "product:api" --task "Implement user authentication"

# With specific level
claude --load-skills "product:api --level 2" --task "Review code for security issues"

# Multiple skills
claude --load-skills "[skill:coding-standards + skill:security-practices]" --file src/auth.py --task "Review and suggest improvements"
```

#### File-Specific Skills

```bash
# Load skills based on file type
claude --auto-skills --file src/auth.py --task "Add NIST control tags"

# Claude auto-loads:
# - coding-standards (Python)
# - security-practices (auth patterns)
# - nist-compliance (control tagging)
```

---

## Claude API Integration

### Python SDK

#### Installation

```bash
pip install anthropic
```

#### Basic Integration

```python
import anthropic
from pathlib import Path

# Initialize client
client = anthropic.Anthropic(api_key="your-api-key")

# Load skills
def load_skills(skill_names: list[str], level: int = 1) -> str:
    """Load skills from the standards repository."""
    skills_content = []

    for skill in skill_names:
        skill_path = Path(f"skills/{skill}/SKILL.md")
        if skill_path.exists():
            content = skill_path.read_text()

            # Extract specified level
            if level == 1:
                # Extract Level 1 content only
                match = re.search(
                    r"## Level 1: Quick Start.*?(?=## Level 2:|$)",
                    content,
                    re.DOTALL
                )
            elif level == 2:
                # Extract Level 1 + 2
                match = re.search(
                    r"## Level 1: Quick Start.*?(?=## Level 3:|$)",
                    content,
                    re.DOTALL
                )
            else:
                # Full content (all levels)
                match = re.search(r"---\n\n# .*", content, re.DOTALL)

            if match:
                skills_content.append(match.group(0))

    return "\n\n".join(skills_content)

# Use in API call
skills = load_skills(['coding-standards', 'security-practices', 'testing'], level=1)

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    system=f"""You are a senior software engineer.

Follow these standards:

{skills}
""",
    messages=[{
        "role": "user",
        "content": "Implement user authentication with password hashing"
    }]
)

print(response.content[0].text)
```

#### Advanced Integration with Auto-Recommendations

```python
import anthropic
import subprocess
import json
from pathlib import Path

class ClaudeWithSkills:
    def __init__(self, api_key: str, project_path: str = "./"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.project_path = project_path

    def get_skill_recommendations(self) -> list[dict]:
        """Get skill recommendations for the project."""
        result = subprocess.run(
            ["npm", "run", "skill-loader", "--", "recommend", self.project_path, "--format", "json"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return json.loads(result.stdout)

        return []

    def load_skills(self, skill_names: list[str], level: int = 1) -> str:
        """Load skills at specified level."""
        # Use skill-loader tool
        skills_str = "+".join([f"skill:{s}" for s in skill_names])
        result = subprocess.run(
            ["npm", "run", "skill-loader", "--", "load", skills_str, "--level", str(level)],
            capture_output=True,
            text=True
        )

        return result.stdout if result.returncode == 0 else ""

    def create_message_with_skills(
        self,
        user_message: str,
        skills: list[str] = None,
        level: int = 1,
        auto_recommend: bool = False
    ):
        """Create message with skills context."""

        # Auto-recommend if requested
        if auto_recommend and not skills:
            recommendations = self.get_skill_recommendations()
            skills = [rec['skill'] for rec in recommendations if rec['priority'] in ['high', 'critical']]

        # Load skills
        skills_content = self.load_skills(skills, level) if skills else ""

        # Create message
        return self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            system=f"""You are a senior software engineer.

Follow these standards:

{skills_content}
""",
            messages=[{
                "role": "user",
                "content": user_message
            }]
        )

# Usage
claude = ClaudeWithSkills(api_key="your-api-key", project_path="./")

# With auto-recommendations
response = claude.create_message_with_skills(
    "Implement user authentication",
    auto_recommend=True,
    level=1
)

# With specific skills
response = claude.create_message_with_skills(
    "Review this code for security issues",
    skills=['security-practices', 'nist-compliance'],
    level=2
)

# Print response
print(response.content[0].text)
```

### TypeScript SDK

```typescript
import Anthropic from '@anthropic-ai/sdk'
import { readFileSync } from 'fs'
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

class ClaudeWithSkills {
  private client: Anthropic

  constructor(apiKey: string, private projectPath: string = './') {
    this.client = new Anthropic({ apiKey })
  }

  async getSkillRecommendations(): Promise<any[]> {
    const { stdout } = await execAsync(
      `npm run skill-loader -- recommend ${this.projectPath} --format json`
    )
    return JSON.parse(stdout)
  }

  async loadSkills(skillNames: string[], level: number = 1): Promise<string> {
    const skillsStr = skillNames.map(s => `skill:${s}`).join('+')
    const { stdout } = await execAsync(
      `npm run skill-loader -- load "${skillsStr}" --level ${level}`
    )
    return stdout
  }

  async createMessageWithSkills(
    userMessage: string,
    options: {
      skills?: string[]
      level?: number
      autoRecommend?: boolean
    } = {}
  ) {
    const { skills, level = 1, autoRecommend = false } = options

    // Auto-recommend if requested
    let skillsToLoad = skills
    if (autoRecommend && !skills) {
      const recommendations = await this.getSkillRecommendations()
      skillsToLoad = recommendations
        .filter(rec => ['high', 'critical'].includes(rec.priority))
        .map(rec => rec.skill)
    }

    // Load skills
    const skillsContent = skillsToLoad
      ? await this.loadSkills(skillsToLoad, level)
      : ''

    // Create message
    return this.client.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 4096,
      system: `You are a senior software engineer.

Follow these standards:

${skillsContent}`,
      messages: [{
        role: 'user',
        content: userMessage
      }]
    })
  }
}

// Usage
const claude = new ClaudeWithSkills('your-api-key', './')

// With auto-recommendations
const response = await claude.createMessageWithSkills(
  'Implement user authentication',
  { autoRecommend: true, level: 1 }
)

// With specific skills
const response2 = await claude.createMessageWithSkills(
  'Review this code for security issues',
  { skills: ['security-practices', 'nist-compliance'], level: 2 }
)

console.log(response.content[0].text)
```

---

## Best Practices

### 1. Progressive Loading

```python
# Start with Level 1
skills_l1 = load_skills(['coding-standards'], level=1)
# Fast, high-level guidance

# Scale to Level 2 when implementing
skills_l2 = load_skills(['coding-standards'], level=2)
# Detailed patterns and examples

# Use Level 3 for deep dives
skills_l3 = load_skills(['coding-standards'], level=3)
# Comprehensive resources
```

### 2. Context-Aware Loading

```python
# Load based on task
def load_skills_for_task(task_type: str):
    if task_type == 'authentication':
        return load_skills(['security-practices', 'nist-compliance'], level=2)
    elif task_type == 'testing':
        return load_skills(['testing'], level=2)
    elif task_type == 'code-review':
        return load_skills(['coding-standards', 'security-practices'], level=1)
    else:
        return load_skills(['coding-standards'], level=1)
```

### 3. Caching Skills

```python
from functools import lru_cache

@lru_cache(maxsize=10)
def load_skills_cached(skill_tuple: tuple[str, ...], level: int) -> str:
    """Load and cache skills."""
    return load_skills(list(skill_tuple), level)

# Usage
skills = load_skills_cached(('coding-standards', 'testing'), level=1)
# Subsequent calls use cache
```

### 4. Token Budgeting

```python
# Calculate token budget
MAX_SKILLS_TOKENS = 5000  # Reserve for skills
MAX_CODE_TOKENS = 10000   # Reserve for code context
MAX_OUTPUT_TOKENS = 4096  # Claude output

# Load skills within budget
def load_skills_with_budget(skills: list[str], max_tokens: int = MAX_SKILLS_TOKENS):
    level = 1
    content = load_skills(skills, level)

    # Estimate tokens (rough: 4 chars per token)
    estimated_tokens = len(content) / 4

    if estimated_tokens > max_tokens and level > 1:
        # Try lower level
        content = load_skills(skills, level=1)

    return content
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/claude-code-review.yml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm install

      - name: Load skills
        run: |
          npm run skill-loader -- load product:api --level 1 --output .claude/skills.md

      - name: Run Claude Code Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude --load-skills ".claude/skills.md" \
                 --diff "origin/${{ github.base_ref }}..HEAD" \
                 --task "Review code changes for standards compliance" \
                 --output review-comments.md

      - name: Post review comments
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs')
            const review = fs.readFileSync('review-comments.md', 'utf8')

            github.rest.pulls.createReview({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number,
              body: review,
              event: 'COMMENT'
            })
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Load skills
npm run skill-loader -- load product:api --level 1 --output .claude/skills.md

# Run Claude for pre-commit checks
claude --load-skills ".claude/skills.md" \
       --diff "HEAD" \
       --task "Check for security issues and NIST control tags" \
       --output pre-commit-review.md

# Check for issues
if grep -q "ISSUE:" pre-commit-review.md; then
    echo "❌ Pre-commit review found issues:"
    cat pre-commit-review.md
    exit 1
fi

echo "✅ Pre-commit review passed"
exit 0
```

---

## Performance Optimization

### Token Usage Comparison

| Approach | Tokens | Cost (per 1M tokens) | Time |
|----------|--------|----------------------|------|
| Full standards | 250,000 | $0.75 | Slow |
| Skills Level 1 | 1,755 | $0.0053 | Fast |
| Skills Level 2 | 6,500 | $0.0195 | Medium |
| Skills Level 3 | 16,000 | $0.048 | Medium |

**Recommendation**: Use Level 1 for 90% of tasks, Level 2 for implementation, Level 3 rarely.

### Batching Requests

```python
# Batch multiple files with same skills
skills = load_skills(['coding-standards', 'security-practices'], level=1)

files_to_review = ['src/auth.py', 'src/users.py', 'src/api.py']

for file_path in files_to_review:
    with open(file_path) as f:
        code = f.read()

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        system=f"Follow these standards:\n\n{skills}",
        messages=[{
            "role": "user",
            "content": f"Review this code:\n\n```python\n{code}\n```"
        }]
    )

    # Process response
    print(f"Review for {file_path}:")
    print(response.content[0].text)
```

---

## Troubleshooting

### Issue: Skills not loading

```bash
# Check skills exist
ls skills/

# Validate skills
python scripts/validate-skills.py skills/

# Check skill-loader script
npm run skill-loader -- list
```

### Issue: High token usage

```python
# Check token estimates
from skill_loader import estimate_tokens

skills = load_skills(['coding-standards'], level=2)
tokens = estimate_tokens(skills)
print(f"Estimated tokens: {tokens}")

# If too high, use Level 1
skills = load_skills(['coding-standards'], level=1)
```

### Issue: Claude not following standards

```python
# Be explicit in prompt
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    system=f"""You MUST follow these standards strictly:

{skills}

Do not deviate from these standards under any circumstances.""",
    messages=[...]
)
```

---

## Examples

### Example 1: Code Generation

```python
skills = load_skills(['coding-standards', 'security-practices', 'testing'], level=2)

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    system=f"""You are a senior software engineer.

Follow these standards strictly:

{skills}""",
    messages=[{
        "role": "user",
        "content": """Implement a user authentication system with:
- Password hashing (bcrypt)
- JWT token generation
- Rate limiting
- NIST control tagging
- Comprehensive tests
"""
    }]
)

print(response.content[0].text)
```

### Example 2: Code Review

```python
skills = load_skills(['coding-standards', 'security-practices', 'nist-compliance'], level=1)

with open('src/auth.py') as f:
    code = f.read()

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    system=f"""You are a code reviewer.

Review against these standards:

{skills}

Provide specific, actionable feedback.""",
    messages=[{
        "role": "user",
        "content": f"""Review this code:

```python
{code}
```

Check for:
1. Standards compliance
2. Security issues
3. Missing NIST control tags
4. Test coverage
"""
    }]
)

print(response.content[0].text)
```

---

## Additional Resources

- **Skills User Guide**: [SKILLS_USER_GUIDE.md](./SKILLS_USER_GUIDE.md)
- **API Documentation**: [SKILLS_API.md](../api/SKILLS_API.md)
- **Claude API Docs**: [https://docs.anthropic.com/](https://docs.anthropic.com/)
- **Claude Code Docs**: [https://docs.anthropic.com/claude-code/](https://docs.anthropic.com/claude-code/)

---

*Last Updated: 2025-10-16*
*Version: 1.0.0*
*Maintained by: Standards Repository Team*
