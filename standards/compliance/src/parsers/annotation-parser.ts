import * as fs from 'fs/promises';
import * as path from 'path';

export interface NistAnnotation {
  controlId: string;
  description: string;
  implements?: string;
  evidence?: string[];
  file: string;
  line: number;
  column: number;
  language: string;
  context?: string;
}

export interface ParserResult {
  annotations: NistAnnotation[];
  errors: string[];
}

export abstract class BaseAnnotationParser {
  protected annotations: NistAnnotation[] = [];
  protected errors: string[] = [];

  abstract get supportedExtensions(): string[];
  abstract get language(): string;
  abstract parse(content: string, filePath: string): Promise<ParserResult>;

  protected addAnnotation(annotation: Omit<NistAnnotation, 'language'>): void {
    this.annotations.push({
      ...annotation,
      language: this.language
    });
  }

  protected addError(error: string): void {
    this.errors.push(error);
  }

  protected reset(): void {
    this.annotations = [];
    this.errors = [];
  }

  protected extractNistTags(
    text: string,
    filePath: string,
    lineOffset: number = 0,
    columnOffset: number = 0
  ): void {
    // Common patterns for NIST annotations
    const patterns = [
      // @nist ac-2 "description"
      /@nist\s+([a-z]{2}-\d+(?:\.\d+)?)\s*(?:"([^"]*)")?/gi,
      // @nist-implements ac-2.a "description"
      /@nist-implements\s+([a-z]{2}-\d+(?:\.\d+)?(?:\.[a-z])?)\s*(?:"([^"]*)")?/gi,
      // @nist-controls: [ac-2, ac-3]
      /@nist-controls:\s*\[([^\]]+)\]/gi,
      // @evidence code, test, config
      /@evidence\s+([^\n]+)/gi
    ];

    const lines = text.split('\n');

    lines.forEach((line, lineIndex) => {
      // Standard @nist tags
      const nistPattern = /@nist\s+([a-z]{2}-\d+(?:\.\d+)?)\s*(?:"([^"]*)")?/gi;
      let match;

      while ((match = nistPattern.exec(line)) !== null) {
        this.addAnnotation({
          controlId: match[1],
          description: match[2] || '',
          file: filePath,
          line: lineIndex + lineOffset + 1,
          column: match.index + columnOffset,
          context: line.trim()
        });
      }

      // @nist-implements tags
      const implementsPattern = /@nist-implements\s+([a-z]{2}-\d+(?:\.\d+)?(?:\.[a-z])?)\s*(?:"([^"]*)")?/gi;
      while ((match = implementsPattern.exec(line)) !== null) {
        const baseControl = match[1].split('.').slice(0, 2).join('.');
        const existingAnnotation = this.annotations.find(
          a => a.controlId === baseControl && a.line === lineIndex + lineOffset + 1
        );

        if (existingAnnotation) {
          existingAnnotation.implements = match[1];
        } else {
          this.addAnnotation({
            controlId: baseControl,
            description: match[2] || '',
            implements: match[1],
            file: filePath,
            line: lineIndex + lineOffset + 1,
            column: match.index + columnOffset,
            context: line.trim()
          });
        }
      }

      // @evidence tags
      const evidencePattern = /@evidence\s+([^\n]+)/gi;
      while ((match = evidencePattern.exec(line)) !== null) {
        const evidenceTypes = match[1].split(',').map(e => e.trim());
        // Find the most recent annotation to attach evidence to
        if (this.annotations.length > 0) {
          const lastAnnotation = this.annotations[this.annotations.length - 1];
          lastAnnotation.evidence = evidenceTypes;
        }
      }
    });

    // Handle multi-control format: @nist-controls: [ac-2, ac-3]
    const multiControlPattern = /@nist-controls:\s*\[([^\]]+)\]/gi;
    let multiMatch: RegExpExecArray | null;

    while ((multiMatch = multiControlPattern.exec(text)) !== null) {
      const controls = multiMatch[1].split(',').map(c => c.trim());
      const startPos = this.getLineAndColumn(text, multiMatch.index);

      controls.forEach(controlId => {
        if (/^[a-z]{2}-\d+/.test(controlId)) {
          this.addAnnotation({
            controlId,
            description: '',
            file: filePath,
            line: startPos.line + lineOffset,
            column: startPos.column + columnOffset,
            context: multiMatch![0]  // Use non-null assertion since we know it's not null here
          });
        }
      });
    }
  }

  protected getLineAndColumn(text: string, index: number): { line: number; column: number } {
    const lines = text.substring(0, index).split('\n');
    return {
      line: lines.length,
      column: lines[lines.length - 1].length
    };
  }

  protected validateControlId(controlId: string): boolean {
    return /^[a-z]{2}-\d+(?:\.\d+)?(?:\.[a-z])?$/.test(controlId);
  }
}

export class AnnotationParserFactory {
  private static parsers: Map<string, BaseAnnotationParser> = new Map();

  static registerParser(parser: BaseAnnotationParser): void {
    parser.supportedExtensions.forEach(ext => {
      this.parsers.set(ext, parser);
    });
  }

  static async parseFile(filePath: string): Promise<ParserResult> {
    const ext = path.extname(filePath).toLowerCase();
    const parser = this.parsers.get(ext);

    if (!parser) {
      return {
        annotations: [],
        errors: [`No parser found for file extension: ${ext}`]
      };
    }

    try {
      const content = await fs.readFile(filePath, 'utf-8');
      return parser.parse(content, filePath);
    } catch (error) {
      return {
        annotations: [],
        errors: [`Error reading file: ${error}`]
      };
    }
  }

  static getSupportedExtensions(): string[] {
    return Array.from(this.parsers.keys());
  }
}
