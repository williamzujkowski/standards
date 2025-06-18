import { BaseAnnotationParser, ParserResult } from './annotation-parser';

export class JavaScriptParser extends BaseAnnotationParser {
  get supportedExtensions(): string[] {
    return ['.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs'];
  }

  get language(): string {
    return 'javascript';
  }

  async parse(content: string, filePath: string): Promise<ParserResult> {
    this.reset();

    // Extract from JSDoc comments
    this.parseJSDocComments(content, filePath);

    // Extract from single-line comments
    this.parseSingleLineComments(content, filePath);

    // Extract from multi-line comments
    this.parseMultiLineComments(content, filePath);

    return {
      annotations: this.annotations,
      errors: this.errors
    };
  }

  private parseJSDocComments(content: string, filePath: string): void {
    // Match JSDoc blocks
    const jsDocPattern = /\/\*\*([\s\S]*?)\*\//g;
    let match;

    while ((match = jsDocPattern.exec(content)) !== null) {
      const jsDocContent = match[1];
      const startPos = this.getLineAndColumn(content, match.index);

      // Extract NIST tags from JSDoc
      this.extractNistTags(jsDocContent, filePath, startPos.line - 1, 3); // Account for /** prefix
    }
  }

  private parseSingleLineComments(content: string, filePath: string): void {
    const lines = content.split('\n');

    lines.forEach((line, lineIndex) => {
      // Match // @nist patterns
      const singleLinePattern = /\/\/\s*(@nist[\s\S]*?)$/;
      const match = line.match(singleLinePattern);

      if (match) {
        this.extractNistTags(match[1], filePath, lineIndex, match.index! + 2);
      }
    });
  }

  private parseMultiLineComments(content: string, filePath: string): void {
    // Match /* */ comments (but not JSDoc)
    const multiLinePattern = /\/\*(?!\*)([\s\S]*?)\*\//g;
    let match;

    while ((match = multiLinePattern.exec(content)) !== null) {
      const commentContent = match[1];
      const startPos = this.getLineAndColumn(content, match.index);

      this.extractNistTags(commentContent, filePath, startPos.line - 1, 2);
    }
  }
}
