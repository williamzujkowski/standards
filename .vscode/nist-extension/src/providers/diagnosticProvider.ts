import * as vscode from 'vscode';
import { NistControl } from '../data/controlsLoader';

export class NistDiagnosticProvider {
    private diagnosticCollection: vscode.DiagnosticCollection;

    constructor(private controls: Map<string, NistControl>) {
        this.diagnosticCollection = vscode.languages.createDiagnosticCollection('nist');
    }

    validateDocument(document: vscode.TextDocument): void {
        const diagnostics: vscode.Diagnostic[] = [];
        const text = document.getText();
        const lines = text.split('\n');

        // Check for invalid NIST tags
        const tagPattern = /@nist\s+([a-z]{2}-\d+)(?:\s+"([^"]*)")?/g;
        let match;

        while ((match = tagPattern.exec(text)) !== null) {
            const controlId = match[1];
            const description = match[2];
            const startPos = document.positionAt(match.index);
            const endPos = document.positionAt(match.index + match[0].length);
            const range = new vscode.Range(startPos, endPos);

            // Validate control ID
            if (!this.controls.has(controlId)) {
                const diagnostic = new vscode.Diagnostic(
                    range,
                    `Unknown NIST control: ${controlId}`,
                    vscode.DiagnosticSeverity.Error
                );
                diagnostic.code = 'unknown-control';
                diagnostics.push(diagnostic);
            } else if (!description || description.trim() === '') {
                // Warn about missing description
                const diagnostic = new vscode.Diagnostic(
                    range,
                    `NIST tag should include a description`,
                    vscode.DiagnosticSeverity.Warning
                );
                diagnostic.code = 'missing-description';
                diagnostics.push(diagnostic);
            }
        }

        // Check for security patterns without NIST tags
        const securityPatterns = [
            { pattern: /\bauth(?:enticate|orize)\b/i, suggestion: 'Consider adding @nist ia-2 or ac-3' },
            { pattern: /\bpassword\b/i, suggestion: 'Consider adding @nist ia-5' },
            { pattern: /\bencrypt(?:ion)?\b/i, suggestion: 'Consider adding @nist sc-13' },
            { pattern: /\b(?:log|audit)\b/i, suggestion: 'Consider adding @nist au-2' },
            { pattern: /\bvalidat(?:e|ion)\b/i, suggestion: 'Consider adding @nist si-10' }
        ];

        lines.forEach((line, lineNum) => {
            // Skip if line already has a NIST tag
            if (/@nist/.test(line)) {
                return;
            }

            for (const { pattern, suggestion } of securityPatterns) {
                if (pattern.test(line)) {
                    // Check if there's a NIST tag within 5 lines
                    let hasNearbyTag = false;
                    for (let i = Math.max(0, lineNum - 5); i <= Math.min(lines.length - 1, lineNum + 5); i++) {
                        if (/@nist/.test(lines[i])) {
                            hasNearbyTag = true;
                            break;
                        }
                    }

                    if (!hasNearbyTag) {
                        const lineRange = new vscode.Range(lineNum, 0, lineNum, line.length);
                        const diagnostic = new vscode.Diagnostic(
                            lineRange,
                            suggestion,
                            vscode.DiagnosticSeverity.Information
                        );
                        diagnostic.code = 'missing-tag';
                        diagnostics.push(diagnostic);
                        break; // Only one suggestion per line
                    }
                }
            }
        });

        this.diagnosticCollection.set(document.uri, diagnostics);
    }

    dispose(): void {
        this.diagnosticCollection.dispose();
    }
}
