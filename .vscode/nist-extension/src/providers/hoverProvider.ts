import * as vscode from 'vscode';
import { NistControl } from '../data/controlsLoader';

export class NistHoverProvider implements vscode.HoverProvider {
    constructor(private controls: Map<string, NistControl>) {}

    provideHover(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken
    ): vscode.Hover | null {
        const range = document.getWordRangeAtPosition(position, /@nist\s+([a-z]{2}-\d+)/);
        if (!range) {
            return null;
        }

        const text = document.getText(range);
        const match = text.match(/@nist\s+([a-z]{2}-\d+)/);
        if (!match) {
            return null;
        }

        const controlId = match[1];
        const control = this.controls.get(controlId);
        if (!control) {
            return new vscode.Hover(
                new vscode.MarkdownString(`⚠️ Unknown NIST control: ${controlId}`)
            );
        }

        const markdown = new vscode.MarkdownString();
        markdown.appendMarkdown(`### NIST ${control.id}: ${control.title}\n\n`);
        markdown.appendMarkdown(`${control.description}\n\n`);
        markdown.appendMarkdown(`**Family:** ${control.family}\n\n`);
        markdown.appendMarkdown(`**Required in baselines:**\n`);
        markdown.appendMarkdown(`- Low: ${control.baselines.low ? '✅' : '❌'}\n`);
        markdown.appendMarkdown(`- Moderate: ${control.baselines.moderate ? '✅' : '❌'}\n`);
        markdown.appendMarkdown(`- High: ${control.baselines.high ? '✅' : '❌'}\n\n`);

        if (control.examples && control.examples.length > 0) {
            markdown.appendMarkdown(`**Implementation Examples:**\n`);
            control.examples.forEach(example => {
                markdown.appendMarkdown(`- ${example}\n`);
            });
        }

        if (control.relatedPatterns.length > 0) {
            markdown.appendMarkdown(`\n**Related patterns:** ${control.relatedPatterns.join(', ')}`);
        }

        return new vscode.Hover(markdown, range);
    }
}
