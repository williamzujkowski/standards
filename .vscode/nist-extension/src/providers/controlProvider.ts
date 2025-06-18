import * as vscode from 'vscode';
import { NistControl, getControlsByPattern } from '../data/controlsLoader';

export class NistControlProvider {
    private securityPatterns = [
        { pattern: /auth(?:enticate|orize)/i, controls: ['ia-2', 'ac-3'] },
        { pattern: /password|credential/i, controls: ['ia-5'] },
        { pattern: /session|logout|timeout/i, controls: ['ac-12'] },
        { pattern: /encrypt|crypto|hash/i, controls: ['sc-13'] },
        { pattern: /tls|https|ssl/i, controls: ['sc-8'] },
        { pattern: /log|audit|track/i, controls: ['au-2', 'au-3'] },
        { pattern: /validat|sanitiz/i, controls: ['si-10'] },
        { pattern: /error|exception|catch/i, controls: ['si-11'] },
        { pattern: /permission|role|access/i, controls: ['ac-3', 'ac-6'] },
        { pattern: /user\s*management|account/i, controls: ['ac-2'] }
    ];

    constructor(private controls: Map<string, NistControl>) {}

    async suggestControlsForFunction(document: vscode.TextDocument, position: vscode.Position): Promise<NistControl[]> {
        const functionText = this.getFunctionContext(document, position);
        const suggestions = new Set<NistControl>();

        // Check for security patterns in the function
        for (const { pattern, controls: controlIds } of this.securityPatterns) {
            if (pattern.test(functionText)) {
                for (const id of controlIds) {
                    const control = this.controls.get(id);
                    if (control) {
                        suggestions.add(control);
                    }
                }
            }
        }

        // Also check for specific keywords
        const keywords = this.extractKeywords(functionText);
        for (const keyword of keywords) {
            const relatedControls = getControlsByPattern(this.controls, keyword);
            relatedControls.forEach(control => suggestions.add(control));
        }

        return Array.from(suggestions);
    }

    async checkForSecurityPatterns(document: vscode.TextDocument, position: vscode.Position): Promise<string[]> {
        const line = document.lineAt(position.line).text;
        const patterns: string[] = [];

        for (const { pattern } of this.securityPatterns) {
            if (pattern.test(line)) {
                patterns.push(pattern.source);
            }
        }

        return patterns;
    }

    async generateComplianceReport(): Promise<string> {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            return '# NIST Compliance Report\n\nNo workspace folder open.';
        }

        let report = '# NIST 800-53r5 Compliance Report\n\n';
        report += `Generated: ${new Date().toISOString()}\n\n`;

        const taggedControls = new Map<string, number>();
        const filesByControl = new Map<string, string[]>();

        // Search for NIST tags in all files
        const files = await vscode.workspace.findFiles('**/*.{js,ts,py,go,yaml}', '**/node_modules/**');

        for (const file of files) {
            const document = await vscode.workspace.openTextDocument(file);
            const text = document.getText();
            const matches = text.matchAll(/@nist\s+([a-z]{2}-\d+)/g);

            for (const match of matches) {
                const controlId = match[1];
                taggedControls.set(controlId, (taggedControls.get(controlId) || 0) + 1);

                const files = filesByControl.get(controlId) || [];
                const relativePath = vscode.workspace.asRelativePath(file);
                if (!files.includes(relativePath)) {
                    files.push(relativePath);
                }
                filesByControl.set(controlId, files);
            }
        }

        report += `## Summary\n\n`;
        report += `- Total controls tagged: ${taggedControls.size}\n`;
        report += `- Total tags found: ${Array.from(taggedControls.values()).reduce((a, b) => a + b, 0)}\n`;
        report += `- Files scanned: ${files.length}\n\n`;

        report += `## Tagged Controls\n\n`;
        for (const [controlId, count] of taggedControls) {
            const control = this.controls.get(controlId);
            if (control) {
                report += `### ${controlId}: ${control.title}\n`;
                report += `- Count: ${count}\n`;
                report += `- Files:\n`;
                const files = filesByControl.get(controlId) || [];
                for (const file of files.slice(0, 5)) {
                    report += `  - ${file}\n`;
                }
                if (files.length > 5) {
                    report += `  - ... and ${files.length - 5} more\n`;
                }
                report += '\n';
            }
        }

        const baseline = vscode.workspace.getConfiguration('nist').get<string>('baseline') || 'moderate';
        report += `## Coverage Analysis (${baseline} baseline)\n\n`;

        const baselineControls = Array.from(this.controls.values())
            .filter(c => c.baselines[baseline as keyof typeof c.baselines]);

        const coveredControls = baselineControls.filter(c => taggedControls.has(c.id));
        const coverage = (coveredControls.length / baselineControls.length) * 100;

        report += `- Required controls: ${baselineControls.length}\n`;
        report += `- Covered controls: ${coveredControls.length}\n`;
        report += `- Coverage: ${coverage.toFixed(1)}%\n\n`;

        report += `### Missing Controls\n\n`;
        const missingControls = baselineControls.filter(c => !taggedControls.has(c.id));
        for (const control of missingControls) {
            report += `- ${control.id}: ${control.title}\n`;
        }

        return report;
    }

    private getFunctionContext(document: vscode.TextDocument, position: vscode.Position): string {
        // Get surrounding lines for context
        const startLine = Math.max(0, position.line - 10);
        const endLine = Math.min(document.lineCount - 1, position.line + 10);

        let context = '';
        for (let i = startLine; i <= endLine; i++) {
            context += document.lineAt(i).text + '\n';
        }

        return context;
    }

    private extractKeywords(text: string): string[] {
        const keywords = new Set<string>();
        const words = text.toLowerCase().match(/\b\w+\b/g) || [];

        const securityKeywords = [
            'auth', 'authenticate', 'authorize', 'permission', 'role',
            'password', 'token', 'credential', 'session', 'logout',
            'encrypt', 'decrypt', 'hash', 'crypto', 'tls', 'ssl',
            'log', 'audit', 'track', 'monitor', 'validate', 'sanitize',
            'error', 'exception', 'security', 'access', 'user'
        ];

        for (const word of words) {
            if (securityKeywords.some(kw => word.includes(kw))) {
                keywords.add(word);
            }
        }

        return Array.from(keywords);
    }
}
