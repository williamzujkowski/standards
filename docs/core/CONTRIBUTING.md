# Contributing to Software Development Standards

Thank you for your interest in contributing to our comprehensive standards repository!

## 📋 Quick Links

- **Creating new standards?** See [CREATING_STANDARDS_GUIDE.md](../guides/CREATING_STANDARDS_GUIDE.md)
- **Use our template:** [STANDARD_TEMPLATE.md](../guides/STANDARD_TEMPLATE.md)
- **Report issues:** [GitHub Issues](https://github.com/williamzujkowski/standards/issues)

## 🚀 Ways to Contribute

### 1. Report Issues

- Bug reports
- Unclear documentation
- Missing examples
- Broken links
- Outdated practices

### 2. Suggest Improvements

- Enhanced examples
- Additional patterns
- Tool recommendations
- Performance optimizations
- Security enhancements

### 3. Create New Standards

Follow our [Creating Standards Guide](../guides/CREATING_STANDARDS_GUIDE.md) to add new standards.

### 4. Update Existing Standards

- Fix typos and grammar
- Update deprecated practices
- Add missing examples
- Improve clarity
- Update tool versions

## 📝 Pull Request Process

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-improvement`
3. **Make your changes**
4. **Validate your changes**:

   ```bash
   # Run validation checks
   yamllint .
   markdownlint '**/*.md'
   ```

5. **Commit with clear message**: `git commit -m "Add: [brief description]"`
6. **Push to your fork**: `git push origin feature/your-improvement`
7. **Open a Pull Request**

## ✅ PR Checklist

- [ ] Follows existing format and structure
- [ ] Includes practical, working examples
- [ ] Updates related documentation
- [ ] Adds/updates tests if applicable
- [ ] Passes all validation checks
- [ ] Includes clear commit messages
- [ ] Updates CHANGELOG.md if significant

## 🎨 Style Guidelines

### Markdown

- Use clear, descriptive headings
- Include code examples with syntax highlighting
- Use tables for structured data
- Add links to related standards

### Code Examples

- Provide examples in multiple languages (Python, JS/TS, Go)
- Include both good and bad examples
- Add comments explaining key concepts
- Ensure examples are production-ready

### Tone

- Be prescriptive and clear
- Avoid ambiguity
- Use active voice
- Focus on practical application

## 🔍 Review Process

1. **Automated checks** run on all PRs
2. **Maintainer review** for content quality
3. **Community feedback** period (if significant change)
4. **Merge** when approved

## 🤖 For LLMs Contributing

When creating PRs via LLMs:

1. Follow [CREATING_STANDARDS_GUIDE.md](../guides/CREATING_STANDARDS_GUIDE.md) precisely
2. Ensure all integration points are updated
3. Validate against [STANDARD_TEMPLATE.md](../guides/STANDARD_TEMPLATE.md)
4. Include rationale for changes in PR description

## 📄 License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers this project.

## 🙏 Thank You!

Your contributions help make software development better for everyone. We appreciate your time and effort!

## Related Standards

- [GitHub Platform Standards](../standards/GITHUB_PLATFORM_STANDARDS.md) - Best practices for GitHub usage
- [Knowledge Management Standards](../standards/KNOWLEDGE_MANAGEMENT_STANDARDS.md) - Documentation standards
