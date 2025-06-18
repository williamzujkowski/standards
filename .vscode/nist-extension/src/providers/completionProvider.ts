import * as vscode from 'vscode';
import { NistControl } from '../data/controlsLoader';

export class NistCompletionProvider implements vscode.CompletionItemProvider {
    constructor(private controls: Map<string, NistControl>) {}

    provideCompletionItems(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken,
        context: vscode.CompletionContext
    ): vscode.CompletionItem[] {
        const line = document.lineAt(position).text;
        const prefix = line.slice(0, position.character);

        // Check if we're in a @nist context
        if (!prefix.includes('@nist')) {
            // Offer @nist as a completion
            const nistCompletion = new vscode.CompletionItem('@nist', vscode.CompletionItemKind.Snippet);
            nistCompletion.detail = 'NIST 800-53r5 control tag';
            nistCompletion.documentation = 'Add a NIST control tag to document compliance';
            nistCompletion.insertText = new vscode.SnippetString('@nist ${1|' + Array.from(this.controls.keys()).join(',') + '|} "${2:description}"');
            return [nistCompletion];
        }

        // We're after @nist, provide control completions
        const completions: vscode.CompletionItem[] = [];

        for (const [id, control] of this.controls) {
            const item = new vscode.CompletionItem(id, vscode.CompletionItemKind.Reference);
            item.detail = control.title;
            item.documentation = new vscode.MarkdownString(
                `**${control.id}: ${control.title}**\n\n` +
                `${control.description}\n\n` +
                `**Family:** ${control.family}\n\n` +
                `**Baselines:** Low: ${control.baselines.low ? '✓' : '✗'}, ` +
                `Moderate: ${control.baselines.moderate ? '✓' : '✗'}, ` +
                `High: ${control.baselines.high ? '✓' : '✗'}\n\n` +
                (control.examples ? `**Examples:**\n${control.examples.map(e => `- ${e}`).join('\n')}` : '')
            );

            // Create appropriate snippet based on language
            const language = document.languageId;
            let snippet: string;

            switch (language) {
                case 'python':
                    snippet = `${id} "${control.title}"`;
                    break;
                case 'yaml':
                    snippet = `${id} "${control.title}"`;
                    break;
                default:
                    snippet = `${id} "${control.title}"`;
            }

            item.insertText = new vscode.SnippetString(snippet);
            completions.push(item);
        }

        return completions;
    }
}
