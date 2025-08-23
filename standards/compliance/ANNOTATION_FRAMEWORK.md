# NIST Annotation Framework

> 📚 See also: [Unified Software Development Standards](../../docs/standards/UNIFIED_STANDARDS.md)

A multi-language parser framework for extracting NIST 800-53r5 control annotations from source code.

## Features

- **Multi-Language Support**: JavaScript, TypeScript, Python, Go, Java, YAML
- **Flexible Annotation Formats**: Comments, docstrings, decorators, struct tags
- **Comprehensive Parsing**: Extracts control IDs, descriptions, implementation details, and evidence
- **CLI Tool**: Scan entire codebases and generate reports
- **Extensible**: Easy to add new language parsers

## Supported Annotation Formats

### JavaScript/TypeScript

```javascript
/**
 * @nist ia-2 "User authentication"
 * @nist-implements ia-2.1 "Multi-factor authentication"
 * @evidence code, test
 */
function login() {}

// @nist ac-3 "Access enforcement"
const checkPermission = () => {};
```

### Python

```python
# @nist ac-3 "Access enforcement"
def check_permission():
    """
    @nist-implements ac-3.a "Enforce approved authorizations"
    @evidence code, test, config
    """
    pass

@nist_control("ia-5", "Password management")
def change_password():
    pass
```

### Go

```go
// @nist ia-2 "User authentication"
func authenticate() {}

type User struct {
    // Using struct tags
    Password string `nist:"ia-5"`
}
```

### Java

```java
/**
 * @nist ac-2 "Account management"
 */
@NistControl(value = "ac-2", description = "Account management")
public class UserManager {}
```

### YAML

```yaml
# @nist-controls: [sc-8, sc-13, ac-12]
security:
  tls:
    enabled: true  # @nist sc-8 "Transmission confidentiality"
```

## Usage

### CLI Tool

```bash
# Scan current directory
npm run scan-annotations

# Scan specific directory with JSON output
npm run scan-annotations scan ./src -f json -o report.json

# Generate markdown report
npm run scan-annotations scan ./src -f markdown -o compliance-report.md

# Export to CSV
npm run scan-annotations scan ./src -f csv -o annotations.csv

# Exclude certain patterns
npm run scan-annotations scan . -e "**/test/**,**/vendor/**"
```

### Programmatic Usage

```typescript
import { AnnotationParserFactory } from './parsers';

// Parse a single file
const result = await AnnotationParserFactory.parseFile('src/auth.ts');
console.log(result.annotations);

// Parse JavaScript content directly
import { JavaScriptParser } from './parsers/javascript-parser';
const parser = new JavaScriptParser();
const result = await parser.parse(fileContent, 'src/file.js');
```

## Output Formats

### JSON Output

```json
{
  "annotations": [
    {
      "controlId": "ia-2",
      "description": "User authentication",
      "file": "/path/to/file.ts",
      "line": 15,
      "column": 3,
      "language": "javascript",
      "implements": "ia-2.1",
      "evidence": ["code", "test"]
    }
  ],
  "errors": []
}
```

### Markdown Report

- Summary statistics
- Annotations grouped by control
- File locations with line numbers
- Implementation details and evidence

### CSV Export

- Tabular format for spreadsheet analysis
- All annotation fields included
- Easy to import into compliance tools

## Extending the Framework

To add support for a new language:

1. Create a new parser class extending `BaseAnnotationParser`
2. Implement required methods:
   - `supportedExtensions`
   - `language`
   - `parse`
3. Register the parser in `index.ts`

Example:

```typescript
export class RubyParser extends BaseAnnotationParser {
  get supportedExtensions(): string[] {
    return ['.rb'];
  }

  get language(): string {
    return 'ruby';
  }

  async parse(content: string, filePath: string): Promise<ParserResult> {
    this.reset();
    // Parse Ruby-specific annotation formats
    return {
      annotations: this.annotations,
      errors: this.errors
    };
  }
}
```

## Integration with NIST Tools

The annotation framework integrates with:

- **VS Code Extension**: Real-time annotation validation
- **Git Hooks**: Pre-commit annotation checks
- **CI/CD**: Automated compliance reporting
- **SSP Generator**: Evidence collection from annotations
