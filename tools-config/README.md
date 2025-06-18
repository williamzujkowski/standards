# Tools Configuration Directory

This directory contains standardized configuration files for development tools referenced in [TOOLS_CATALOG.yaml](../config/TOOLS_CATALOG.yaml).

## 📁 Configuration Files

### Security Tools
- `trivy.yaml` - Container and dependency scanning configuration
- `semgrep.yaml` - SAST rules and custom patterns
- `.gitleaks.toml` - Secret scanning configuration

### CI/CD Templates
- `github-actions-security.yml` - Security scanning workflow
- `github-actions-python.yml` - Python CI/CD template
- `github-actions-node.yml` - Node.js CI/CD template

### Linting Configurations
- `ruff.toml` - Python linting rules
- `eslint-strict.json` - Strict ESLint configuration

## 🚀 Usage

Copy relevant configuration files to your project:

```bash
# For Python projects
cp tools-config/ruff.toml pyproject.toml

# For security scanning
cp tools-config/trivy.yaml .trivy.yaml
cp tools-config/semgrep.yaml .semgrep.yaml

# For CI/CD
cp tools-config/github-actions-python.yml .github/workflows/ci.yml
```

## 🔧 Customization

These configurations provide sensible defaults. Customize based on your project needs:

1. Copy the configuration file
2. Modify rules/settings as needed
3. Document any deviations from defaults
4. Ensure changes align with standards

## 📝 Contributing

When adding new tool configurations:

1. Use the most secure and strict defaults
2. Include inline documentation
3. Test the configuration thoroughly
4. Update this README with usage instructions
