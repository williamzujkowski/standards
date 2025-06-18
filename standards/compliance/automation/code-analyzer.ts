import { readFile } from 'fs/promises';
import * as path from 'path';

export interface CodeFile {
  path: string;
  name: string;
  language: string;
  content: string;
}

export interface SecurityPattern {
  patternType: string;
  description: string;
  lineRange: [number, number];
  codeSnippet: string;
  confidence: number;
}

export interface CodeAnalysis {
  file: CodeFile;
  securityPatterns: SecurityPattern[];
  detectedFrameworks: string[];
  toolsUsed: string[];
}

export class CodeAnalyzer {
  private patterns: Map<string, RegExp[]>;

  constructor() {
    this.patterns = new Map();
    this.initializePatterns();
  }

  private initializePatterns(): void {
    // Authentication patterns
    this.patterns.set('authentication', [
      /authenticate\s*\(/i,
      /login\s*\(/i,
      /verify(Password|Credentials|Token)/i,
      /jwt\.(sign|verify)/i,
      /passport\.(authenticate|use)/i,
      /\bauth(orize|enticate)\b/i
    ]);

    // Encryption patterns
    this.patterns.set('encryption', [
      /crypto\.(create|encrypt|decrypt)/i,
      /bcrypt\.(hash|compare)/i,
      /\baes\b|\brsa\b/i,
      /encrypt(ed)?|decrypt/i,
      /https\.createServer/i,
      /tls\.createServer/i
    ]);

    // Access control patterns
    this.patterns.set('access-control', [
      /hasPermission|checkPermission/i,
      /isAuthorized|authorize/i,
      /rbac|abac/i,
      /role\.(check|verify)/i,
      /can\((read|write|delete|update)\)/i
    ]);

    // Logging patterns
    this.patterns.set('logging', [
      /logger?\.(info|warn|error|debug)/i,
      /console\.(log|warn|error)/i,
      /winston|bunyan|pino/i,
      /audit(Log|Trail)/i,
      /track(Event|Action)/i
    ]);

    // Input validation patterns
    this.patterns.set('input-validation', [
      /validate(Input|Data|Request)/i,
      /sanitize|escape/i,
      /joi\.validate|yup\.validate/i,
      /express-validator/i,
      /\bschema\.validate\b/i
    ]);
  }

  /**
   * Analyze a code file for security patterns
   */
  async analyzeFile(file: CodeFile): Promise<CodeAnalysis> {
    const securityPatterns: SecurityPattern[] = [];
    const detectedFrameworks = this.detectFrameworks(file.content);

    // Split content into lines for line number tracking
    const lines = file.content.split('\n');

    // Check each pattern category
    for (const [patternType, regexes] of this.patterns.entries()) {
      for (const regex of regexes) {
        const matches = file.content.matchAll(new RegExp(regex, 'gi'));

        for (const match of matches) {
          if (match.index !== undefined) {
            const lineNumber = this.getLineNumber(file.content, match.index);
            const snippet = this.extractSnippet(lines, lineNumber);

            securityPatterns.push({
              patternType,
              description: `${patternType} implementation detected`,
              lineRange: [lineNumber, lineNumber + snippet.split('\n').length - 1],
              codeSnippet: snippet,
              confidence: 0.8
            });
          }
        }
      }
    }

    return {
      file,
      securityPatterns,
      detectedFrameworks,
      toolsUsed: ['regex-pattern-matching', 'framework-detection']
    };
  }

  /**
   * Detect frameworks used in the code
   */
  private detectFrameworks(content: string): string[] {
    const frameworks: string[] = [];

    const frameworkPatterns: Record<string, RegExp> = {
      'express': /from\s+['"]express['"]|require\(['"]express['"]\)/,
      'fastify': /from\s+['"]fastify['"]|require\(['"]fastify['"]\)/,
      'nestjs': /from\s+['"]@nestjs/,
      'react': /from\s+['"]react['"]|React\.Component/,
      'angular': /from\s+['"]@angular/,
      'vue': /from\s+['"]vue['"]|Vue\.component/,
      'django': /from\s+django|import\s+django/,
      'flask': /from\s+flask|import\s+flask/,
      'spring': /@SpringBoot|@RestController/
    };

    for (const [framework, pattern] of Object.entries(frameworkPatterns)) {
      if (pattern.test(content)) {
        frameworks.push(framework);
      }
    }

    return frameworks;
  }

  /**
   * Get line number from character index
   */
  private getLineNumber(content: string, index: number): number {
    return content.substring(0, index).split('\n').length;
  }

  /**
   * Extract code snippet around a line
   */
  private extractSnippet(lines: string[], lineNumber: number, context: number = 2): string {
    const start = Math.max(0, lineNumber - context - 1);
    const end = Math.min(lines.length, lineNumber + context);
    return lines.slice(start, end).join('\n');
  }

  /**
   * Analyze file for specific NIST control implementations
   */
  async analyzeForControl(file: CodeFile, controlId: string): Promise<SecurityPattern[]> {
    const patterns: SecurityPattern[] = [];

    // Control-specific patterns
    const controlPatterns: Record<string, RegExp[]> = {
      'ac-2': [ // Account Management
        /createUser|addUser|registerUser/i,
        /deleteUser|removeUser|disableUser/i,
        /updateUser|modifyUser/i,
        /userProvisioning|accountManagement/i
      ],
      'ac-3': [ // Access Enforcement
        /checkAccess|verifyAccess/i,
        /hasPermission|isAuthorized/i,
        /accessControl|authorization/i
      ],
      'au-2': [ // Audit Events
        /audit|log\.(info|error|warn)/i,
        /trackEvent|recordAction/i,
        /eventLog|auditTrail/i
      ],
      'ia-2': [ // Identification and Authentication
        /authenticate|login/i,
        /verifyIdentity|checkCredentials/i,
        /mfa|twoFactor|2fa/i
      ],
      'sc-13': [ // Cryptographic Protection
        /encrypt|decrypt/i,
        /hash|bcrypt|crypto/i,
        /tls|ssl|https/i
      ]
    };

    const relevantPatterns = controlPatterns[controlId] || [];
    const lines = file.content.split('\n');

    for (const pattern of relevantPatterns) {
      const matches = file.content.matchAll(new RegExp(pattern, 'gi'));

      for (const match of matches) {
        if (match.index !== undefined) {
          const lineNumber = this.getLineNumber(file.content, match.index);
          const snippet = this.extractSnippet(lines, lineNumber, 5);

          patterns.push({
            patternType: `nist-${controlId}`,
            description: `Implementation pattern for NIST ${controlId.toUpperCase()}`,
            lineRange: [lineNumber, lineNumber + 10],
            codeSnippet: snippet,
            confidence: 0.85
          });
        }
      }
    }

    return patterns;
  }
}
