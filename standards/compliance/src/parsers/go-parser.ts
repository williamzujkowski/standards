import { BaseAnnotationParser, ParserResult } from './annotation-parser';

export class GoParser extends BaseAnnotationParser {
  get supportedExtensions(): string[] {
    return ['.go'];
  }

  get language(): string {
    return 'go';
  }

  async parse(content: string, filePath: string): Promise<ParserResult> {
    this.reset();

    // Parse single-line comments
    this.parseSingleLineComments(content, filePath);

    // Parse multi-line comments
    this.parseMultiLineComments(content, filePath);

    // Parse struct tags (if using custom NIST tags)
    this.parseStructTags(content, filePath);

    return {
      annotations: this.annotations,
      errors: this.errors
    };
  }

  private parseSingleLineComments(content: string, filePath: string): void {
    const lines = content.split('\n');

    lines.forEach((line, lineIndex) => {
      // Match // @nist patterns
      const commentPattern = /\/\/\s*(@nist[\s\S]*?)$/;
      const match = line.match(commentPattern);

      if (match) {
        this.extractNistTags(match[1], filePath, lineIndex, match.index! + 2);
      }
    });
  }

  private parseMultiLineComments(content: string, filePath: string): void {
    // Match /* */ comments
    const multiLinePattern = /\/\*([\s\S]*?)\*\//g;
    let match;

    while ((match = multiLinePattern.exec(content)) !== null) {
      const commentContent = match[1];
      const startPos = this.getLineAndColumn(content, match.index);

      this.extractNistTags(commentContent, filePath, startPos.line - 1, 2);
    }
  }

  private parseStructTags(content: string, filePath: string): void {
    // Match struct field tags with nist:"control-id"
    const structTagPattern = /`[^`]*nist:"([a-z]{2}-\d+(?:\.\d+)?)(?:,([^"]*?))?"`/g;
    let match;

    while ((match = structTagPattern.exec(content)) !== null) {
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
}
