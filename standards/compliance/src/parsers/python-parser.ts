import { BaseAnnotationParser, ParserResult } from './annotation-parser';

export class PythonParser extends BaseAnnotationParser {
  get supportedExtensions(): string[] {
    return ['.py', '.pyw'];
  }

  get language(): string {
    return 'python';
  }

  async parse(content: string, filePath: string): Promise<ParserResult> {
    this.reset();

    // Parse docstrings
    this.parseDocstrings(content, filePath);

    // Parse single-line comments
    this.parseSingleLineComments(content, filePath);

    // Parse decorators (if using custom NIST decorators)
    this.parseDecorators(content, filePath);

    return {
      annotations: this.annotations,
      errors: this.errors
    };
  }

  private parseDocstrings(content: string, filePath: string): void {
    // Match triple-quoted strings used as docstrings
    const docstringPatterns = [
      /"""([\s\S]*?)"""/g,
      /'''([\s\S]*?)'''/g
    ];

    docstringPatterns.forEach(pattern => {
      let match;
      while ((match = pattern.exec(content)) !== null) {
        const docstringContent = match[1];
        const startPos = this.getLineAndColumn(content, match.index);

        // Check if this is likely a docstring (follows def, class, or at module level)
        const beforeMatch = content.substring(Math.max(0, match.index - 100), match.index);
        if (this.isLikelyDocstring(beforeMatch)) {
          this.extractNistTags(docstringContent, filePath, startPos.line - 1, 3);
        }
      }
    });
  }

  private parseSingleLineComments(content: string, filePath: string): void {
    const lines = content.split('\n');

    lines.forEach((line, lineIndex) => {
      // Match # @nist patterns
      const commentPattern = /#\s*(@nist[\s\S]*?)$/;
      const match = line.match(commentPattern);

      if (match) {
        this.extractNistTags(match[1], filePath, lineIndex, match.index! + 1);
      }
    });
  }

  private parseDecorators(content: string, filePath: string): void {
    // Match @nist_control decorators
    const decoratorPattern = /@nist_control\s*\(\s*["']([a-z]{2}-\d+(?:\.\d+)?)["']\s*(?:,\s*["']([^"']*?)["'])?\s*\)/g;
    let match;

    while ((match = decoratorPattern.exec(content)) !== null) {
      const startPos = this.getLineAndColumn(content, match.index);

      this.addAnnotation({
        controlId: match[1],
        description: match[2] || '',
        file: filePath,
        line: startPos.line,
        column: startPos.column,
        context: match[0]
      });
    }
  }

  private isLikelyDocstring(beforeText: string): boolean {
    // Check if the text before the string looks like it's after a function/class definition
    const trimmed = beforeText.trim();
    return trimmed.endsWith(':') ||
           trimmed.endsWith('def') ||
           trimmed.endsWith('class') ||
           trimmed === '' || // Module-level docstring
           /^\s*$/.test(trimmed); // Only whitespace
  }
}
