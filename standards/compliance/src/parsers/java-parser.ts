import { BaseAnnotationParser, ParserResult } from './annotation-parser';

export class JavaParser extends BaseAnnotationParser {
  get supportedExtensions(): string[] {
    return ['.java'];
  }

  get language(): string {
    return 'java';
  }

  async parse(content: string, filePath: string): Promise<ParserResult> {
    this.reset();

    // Parse Javadoc comments
    this.parseJavadocComments(content, filePath);

    // Parse single-line comments
    this.parseSingleLineComments(content, filePath);

    // Parse multi-line comments
    this.parseMultiLineComments(content, filePath);

    // Parse annotations (if using custom NIST annotations)
    this.parseAnnotations(content, filePath);

    return {
      annotations: this.annotations,
      errors: this.errors
    };
  }

  private parseJavadocComments(content: string, filePath: string): void {
    // Match Javadoc blocks
    const javadocPattern = /\/\*\*([\s\S]*?)\*\//g;
    let match;

    while ((match = javadocPattern.exec(content)) !== null) {
      const javadocContent = match[1];
      const startPos = this.getLineAndColumn(content, match.index);

      // Extract NIST tags from Javadoc
      this.extractNistTags(javadocContent, filePath, startPos.line - 1, 3);
    }
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
    // Match /* */ comments (but not Javadoc)
    const multiLinePattern = /\/\*(?!\*)([\s\S]*?)\*\//g;
    let match;

    while ((match = multiLinePattern.exec(content)) !== null) {
      const commentContent = match[1];
      const startPos = this.getLineAndColumn(content, match.index);

      this.extractNistTags(commentContent, filePath, startPos.line - 1, 2);
    }
  }

  private parseAnnotations(content: string, filePath: string): void {
    // Match @NistControl annotations
    const annotationPattern = /@NistControl\s*\(\s*(?:value\s*=\s*)?["']([a-z]{2}-\d+(?:\.\d+)?)["']\s*(?:,\s*description\s*=\s*["']([^"']*?)["'])?\s*\)/g;
    let match;

    while ((match = annotationPattern.exec(content)) !== null) {
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
