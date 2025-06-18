import { BaseAnnotationParser, ParserResult } from './annotation-parser';
import * as yaml from 'js-yaml';

export class YamlParser extends BaseAnnotationParser {
  get supportedExtensions(): string[] {
    return ['.yaml', '.yml'];
  }

  get language(): string {
    return 'yaml';
  }

  async parse(content: string, filePath: string): Promise<ParserResult> {
    this.reset();

    // Parse comments
    this.parseComments(content, filePath);

    // Parse YAML structure for nist-controls keys
    this.parseYamlStructure(content, filePath);

    return {
      annotations: this.annotations,
      errors: this.errors
    };
  }

  private parseComments(content: string, filePath: string): void {
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

  private parseYamlStructure(content: string, filePath: string): void {
    try {
      const doc = yaml.load(content) as any;

      if (doc && typeof doc === 'object') {
        this.findNistControlsInObject(doc, filePath, content);
      }
    } catch (error) {
      this.addError(`YAML parsing error: ${error}`);
    }
  }

  private findNistControlsInObject(obj: any, filePath: string, content: string, path: string = ''): void {
    for (const key in obj) {
      const currentPath = path ? `${path}.${key}` : key;

      // Look for nist-controls key
      if (key === 'nist-controls' || key === 'nist_controls') {
        const controls = obj[key];

        if (Array.isArray(controls)) {
          controls.forEach(controlId => {
            if (typeof controlId === 'string' && this.validateControlId(controlId)) {
              // Try to find the line number in the YAML
              const lineInfo = this.findLineForPath(content, currentPath);

              this.addAnnotation({
                controlId,
                description: '',
                file: filePath,
                line: lineInfo.line,
                column: lineInfo.column,
                context: `${key}: [${controls.join(', ')}]`
              });
            }
          });
        }
      }

      // Look for @nist annotations in string values
      if (typeof obj[key] === 'string' && obj[key].includes('@nist')) {
        this.extractNistTags(obj[key], filePath);
      }

      // Recurse into nested objects
      if (typeof obj[key] === 'object' && obj[key] !== null) {
        this.findNistControlsInObject(obj[key], filePath, content, currentPath);
      }
    }
  }

  private findLineForPath(content: string, path: string): { line: number; column: number } {
    // Simple heuristic to find the line number for a YAML path
    const pathParts = path.split('.');
    const lastPart = pathParts[pathParts.length - 1];

    const lines = content.split('\n');
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].includes(lastPart + ':')) {
        return {
          line: i + 1,
          column: lines[i].indexOf(lastPart)
        };
      }
    }

    return { line: 1, column: 0 };
  }
}
