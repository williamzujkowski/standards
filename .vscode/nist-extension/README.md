# NIST 800-53r5 Compliance Helper for VS Code

Real-time NIST control suggestions and compliance validation for VS Code.

## Features

- 🚀 **Real-time Control Suggestions** - Get NIST control recommendations as you code
- 🔍 **Auto-completion** - Complete `@nist` tags with control IDs and descriptions
- 📝 **Hover Information** - See detailed control information on hover
- ⚡ **Quick Fixes** - Fix invalid control IDs and add missing descriptions
- 📊 **Compliance Reports** - Generate coverage reports for your project
- 🎯 **Smart Detection** - Automatically detect security patterns that need controls

## Usage

### Basic Tagging

Type `@nist` followed by a space to get auto-completion for NIST controls:

```javascript
// @nist ia-2 "User authentication"
function login(username, password) {
    // Implementation
}
```

### Snippets

Use these prefixes for quick insertion:

- `nist` - Basic control tag
- `nist-auth` - Authentication controls
- `nist-authz` - Authorization controls
- `nist-crypto` - Encryption controls
- `nist-log` - Logging/audit controls
- `nist-validate` - Input validation
- `nist-error` - Error handling
- `nist-session` - Session management

### Commands

Access these commands via Command Palette (Ctrl/Cmd+Shift+P):

- `NIST: Suggest Controls for Current Function` - Get control suggestions
- `NIST: Validate Control Tags in File` - Check all tags in current file
- `NIST: Generate Compliance Report` - Create project-wide report

## Configuration

Configure in VS Code settings:

```json
{
  "nist.baseline": "moderate",        // "low", "moderate", or "high"
  "nist.autoSuggest": true,          // Auto-suggest for security code
  "nist.validateOnSave": true        // Validate tags when saving
}
```

## Control Quick Reference

| Pattern | Suggested Controls |
|---------|-------------------|
| Authentication | `ia-2`, `ia-5` |
| Authorization | `ac-3`, `ac-6` |
| Encryption | `sc-8`, `sc-13` |
| Logging | `au-2`, `au-3` |
| Session | `ac-12` |
| Validation | `si-10` |
| Errors | `si-11` |

## Installation

1. Copy this extension folder to `.vscode/extensions/`
2. Run `npm install` in the extension directory
3. Reload VS Code
4. The extension activates automatically for supported languages

## Development

To modify or extend:

1. Open the extension folder in VS Code
2. Run `npm run watch` to compile TypeScript
3. Press F5 to launch Extension Development Host
4. Make changes and reload to test

## Future Enhancements

- Integration with OSCAL SSP generator
- Project-wide control coverage visualization
- Control relationship mapping
- Evidence collection automation
- CI/CD integration status
