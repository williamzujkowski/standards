#!/usr/bin/env python3
"""
Batch optimize skills exceeding 5K token budget.
Uses proven pattern from aws-advanced and advanced-kubernetes optimizations.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple
import json


# Skills to optimize (from anthropic-compliance-report.md)
SKILLS_TO_OPTIMIZE = [
    # Highest priority (>8K tokens)
    ("ml-ai/model-development", 13121),
    ("security/authorization", 11469),
    ("ml-ai/mlops", 11159),
    ("ml-ai/model-deployment", 9465),
    ("security/zero-trust", 9342),
    ("security/api-security", 8718),

    # High priority (7K-8K tokens)
    ("compliance/gdpr", 7680),
    ("compliance/healthtech", 7763),
    ("devops/infrastructure-as-code", 7794),
    ("compliance/fintech", 7384),
    ("database/advanced-optimization", 7177),

    # Medium priority (6K-7K tokens)
    ("frontend/mobile-react-native", 6825),
    ("devops/monitoring-observability", 6797),
    ("api/graphql", 6610),
    ("cloud-native/serverless", 6612),
    ("data-engineering/orchestration", 6283),
    ("database/nosql", 6420),

    # Lower priority (5K-6K tokens)
    ("cloud-native/service-mesh", 5945),
    ("security/security-operations", 6100),
    ("security/threat-modeling", 6145),
    ("frontend/vue", 7586),
]


class SkillOptimizer:
    """Optimizes skill files by extracting examples to REFERENCE.md."""

    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self.results = []

    def extract_level2_section(self, content: str) -> Tuple[str, str, str]:
        """Extract Level 1, Level 2, and Level 3+ sections."""
        # Find Level 2 section
        level2_match = re.search(
            r'(## Level 2:.*?)(?=## Level 3:|$)',
            content,
            re.DOTALL
        )

        if not level2_match:
            return "", content, ""

        level2_content = level2_match.group(1)

        # Split at Level 2
        parts = content.split('## Level 2:', 1)
        before_level2 = parts[0] if len(parts) > 1 else ""

        # Find Level 3
        if '## Level 3:' in content:
            after_parts = content.split('## Level 3:', 1)
            level3_content = '## Level 3:' + after_parts[1] if len(after_parts) > 1 else ""
        else:
            level3_content = ""

        return before_level2, level2_content, level3_content

    def extract_code_blocks(self, text: str) -> Tuple[List[Dict], str]:
        """Extract code blocks from text, return blocks and text with placeholders."""
        code_blocks = []

        def replace_code(match):
            lang = match.group(1) or ''
            code = match.group(2)
            index = len(code_blocks)

            # Determine if this is a substantial code block
            is_substantial = (
                len(code) > 200 or  # Long code
                code.count('\n') > 10 or  # Many lines
                any(x in code for x in ['function', 'class', 'def', 'import', 'const', 'export'])
            )

            block_info = {
                'index': index,
                'lang': lang,
                'code': code,
                'substantial': is_substantial
            }
            code_blocks.append(block_info)

            if is_substantial:
                # Replace with reference
                return f"\n\n*See [REFERENCE.md](./REFERENCE.md#example-{index}) for complete implementation.*\n\n"
            else:
                # Keep short examples inline
                return match.group(0)

        pattern = r'```(\w*)\n(.*?)```'
        condensed_text = re.sub(pattern, replace_code, text, flags=re.DOTALL)

        return code_blocks, condensed_text

    def condense_section(self, text: str) -> Tuple[str, List[str]]:
        """Condense a section by extracting verbose content."""
        extracted_content = []

        # Pattern 1: Extract verbose lists
        def condense_list(match):
            items = match.group(0)
            if len(items) > 500:  # Long list
                extracted_content.append(('list', items))
                # Return abbreviated version
                lines = items.split('\n')
                if len(lines) > 8:
                    return '\n'.join(lines[:5]) + '\n\n*See REFERENCE.md for complete list.*\n'
            return items

        text = re.sub(r'(?:^[-*] .+$\n?)+', condense_list, text, flags=re.MULTILINE)

        # Pattern 2: Extract verbose configuration examples
        def condense_config(match):
            config = match.group(0)
            if len(config) > 400:
                extracted_content.append(('config', config))
                lang = match.group(1) or ''
                return f"\n\n*See [REFERENCE.md](./REFERENCE.md) for complete {lang} configuration.*\n\n"
            return config

        text = re.sub(r'```(yaml|json|toml)\n.*?```', condense_config, text, flags=re.DOTALL)

        return text, extracted_content

    def create_reference_doc(
        self,
        skill_name: str,
        code_blocks: List[Dict],
        extracted_content: List,
        original_level2: str
    ) -> str:
        """Create REFERENCE.md with extracted content."""

        doc = f"""# {skill_name} - Reference Implementation

This document contains detailed configuration examples and full code samples extracted from the main skill guide to keep the implementation guide concise.

## Table of Contents

"""

        # Add TOC based on original structure
        sections = re.findall(r'###\s+(.+)', original_level2)
        for section in sections[:10]:  # Limit TOC
            anchor = section.lower().replace(' ', '-').replace('/', '').replace('&', '')
            doc += f"- [{section}](#{anchor})\n"

        doc += "\n---\n\n"

        # Add code examples
        if code_blocks:
            doc += "## Code Examples\n\n"
            for block in code_blocks:
                if block['substantial']:
                    doc += f"### Example {block['index']}\n\n"
                    doc += f"```{block['lang']}\n{block['code']}```\n\n"

        # Add extracted configurations
        if extracted_content:
            doc += "## Detailed Configurations\n\n"
            for idx, (content_type, content) in enumerate(extracted_content):
                doc += f"### Configuration {idx + 1}\n\n{content}\n\n"

        # Add link to official docs
        doc += """---

## Additional Resources

See the main SKILL.md file for essential patterns and the official documentation for complete API references.
"""

        return doc

    def optimize_skill(self, skill_path: str, current_tokens: int) -> Dict:
        """Optimize a single skill file."""
        skill_file = self.skills_dir / skill_path / "SKILL.md"

        print(f"\n{'='*80}")
        print(f"Processing: {skill_path}")
        print(f"Current tokens: {current_tokens:,} (target: <5,000)")

        if not skill_file.exists():
            return {
                'skill': skill_path,
                'status': 'error',
                'message': 'SKILL.md not found'
            }

        # Read content
        content = skill_file.read_text()
        original_chars = len(content)

        # Extract sections
        level1, level2, level3 = self.extract_level2_section(content)

        if not level2:
            return {
                'skill': skill_path,
                'status': 'error',
                'message': 'No Level 2 section found'
            }

        # Extract code blocks
        code_blocks, level2_condensed = self.extract_code_blocks(level2)

        # Condense verbose content
        level2_final, extracted_content = self.condense_section(level2_condensed)

        # Add reference link if content was extracted
        if code_blocks or extracted_content:
            # Add reference link at top of Level 2
            reference_note = '\n> **📚 Full Examples**: See [REFERENCE.md](./REFERENCE.md) for complete code samples, detailed configurations, and production-ready implementations.\n\n'

            # Insert after Level 2 header
            level2_final = level2_final.replace(
                '## Level 2:',
                '## Level 2:' + reference_note,
                1
            )

        # Reconstruct file
        new_content = level1 + level2_final + level3
        new_chars = len(new_content)
        new_tokens = new_chars // 4  # Rough estimate

        # Calculate savings
        char_reduction = original_chars - new_chars
        token_reduction = current_tokens - new_tokens
        reduction_pct = (token_reduction / current_tokens * 100) if current_tokens > 0 else 0

        print(f"  Original: {original_chars:,} chars ({current_tokens:,} tokens)")
        print(f"  New:      {new_chars:,} chars ({new_tokens:,} tokens)")
        print(f"  Saved:    {char_reduction:,} chars ({token_reduction:,} tokens, {reduction_pct:.1f}%)")
        print(f"  Extracted: {len(code_blocks)} code blocks, {len(extracted_content)} configs")

        # Create REFERENCE.md if content was extracted
        reference_created = False
        if code_blocks or extracted_content:
            skill_name = skill_path.split('/')[-1].replace('-', ' ').title()
            reference_content = self.create_reference_doc(
                skill_name,
                code_blocks,
                extracted_content,
                level2
            )

            reference_file = self.skills_dir / skill_path / "REFERENCE.md"
            reference_file.write_text(reference_content)
            reference_created = True
            print(f"  ✅ Created REFERENCE.md ({len(reference_content):,} chars)")

        # Write optimized SKILL.md
        skill_file.write_text(new_content)
        print(f"  ✅ Updated SKILL.md")

        return {
            'skill': skill_path,
            'status': 'success',
            'original_tokens': current_tokens,
            'new_tokens': new_tokens,
            'token_reduction': token_reduction,
            'reduction_pct': reduction_pct,
            'original_chars': original_chars,
            'new_chars': new_chars,
            'code_blocks_extracted': len(code_blocks),
            'configs_extracted': len(extracted_content),
            'reference_created': reference_created,
            'now_compliant': new_tokens < 5000
        }

    def optimize_all(self) -> List[Dict]:
        """Optimize all skills in the list."""
        print(f"Starting batch optimization of {len(SKILLS_TO_OPTIMIZE)} skills")
        print(f"Skills directory: {self.skills_dir}")

        for skill_path, current_tokens in SKILLS_TO_OPTIMIZE:
            result = self.optimize_skill(skill_path, current_tokens)
            self.results.append(result)

        return self.results

    def generate_summary(self) -> str:
        """Generate optimization summary report."""
        successful = [r for r in self.results if r['status'] == 'success']
        errors = [r for r in self.results if r['status'] == 'error']

        total_token_reduction = sum(r.get('token_reduction', 0) for r in successful)
        total_original = sum(r.get('original_tokens', 0) for r in successful)
        avg_reduction = (total_token_reduction / total_original * 100) if total_original > 0 else 0

        now_compliant = sum(1 for r in successful if r.get('now_compliant', False))
        references_created = sum(1 for r in successful if r.get('reference_created', False))

        report = f"""
# Batch Skill Optimization Summary

**Date**: {Path(__file__).stat().st_mtime}
**Skills Processed**: {len(self.results)}
**Successful**: {len(successful)}
**Errors**: {len(errors)}

## Overall Impact

- **Total Token Reduction**: {total_token_reduction:,} tokens
- **Average Reduction**: {avg_reduction:.1f}%
- **Skills Now Compliant**: {now_compliant}/{len(successful)} ({now_compliant/len(successful)*100:.1f}%)
- **REFERENCE.md Files Created**: {references_created}

## Detailed Results

"""

        # Sort by token reduction (highest first)
        successful_sorted = sorted(successful, key=lambda x: x.get('token_reduction', 0), reverse=True)

        for result in successful_sorted:
            status_icon = "✅" if result.get('now_compliant') else "⚠️"
            report += f"""
### {status_icon} `{result['skill']}`

- Original: {result['original_tokens']:,} tokens → New: {result['new_tokens']:,} tokens
- Reduction: {result['token_reduction']:,} tokens ({result['reduction_pct']:.1f}%)
- Extracted: {result['code_blocks_extracted']} code blocks, {result['configs_extracted']} configs
- REFERENCE.md: {"Created" if result['reference_created'] else "Not needed"}
- Status: {"✅ Now compliant (<5K)" if result['now_compliant'] else "⚠️ Still over budget"}
"""

        if errors:
            report += "\n## Errors\n\n"
            for error in errors:
                report += f"- ❌ `{error['skill']}`: {error['message']}\n"

        report += """
## Next Steps

1. Review generated REFERENCE.md files for accuracy
2. Test optimized skills with validation scripts
3. Update anthropic-compliance-report.md
4. Run pre-commit hooks
5. Commit changes

## Validation Commands

```bash
# Validate all skills
python3 scripts/validate-skills.py

# Check compliance
python3 scripts/validate-anthropic-compliance.py

# Run pre-commit
pre-commit run --all-files
```
"""

        return report


def main():
    """Main execution."""
    script_dir = Path(__file__).parent
    repo_dir = script_dir.parent
    skills_dir = repo_dir / "skills"

    if not skills_dir.exists():
        print(f"Error: Skills directory not found: {skills_dir}")
        return 1

    optimizer = SkillOptimizer(skills_dir)
    results = optimizer.optimize_all()

    # Generate and save summary
    summary = optimizer.generate_summary()
    summary_file = repo_dir / "reports" / "generated" / "batch-optimization-summary.md"
    summary_file.parent.mkdir(parents=True, exist_ok=True)
    summary_file.write_text(summary)

    print(f"\n{'='*80}")
    print(f"Optimization complete!")
    print(f"Summary saved to: {summary_file}")
    print(f"\nQuick stats:")
    print(f"  Processed: {len(results)} skills")
    print(f"  Successful: {sum(1 for r in results if r['status'] == 'success')}")
    print(f"  Now compliant: {sum(1 for r in results if r.get('now_compliant', False))}")
    print(f"  REFERENCE.md created: {sum(1 for r in results if r.get('reference_created', False))}")

    return 0


if __name__ == "__main__":
    exit(main())
