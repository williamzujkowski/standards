import * as vscode from 'vscode';
import { NistControl } from '../data/controlsLoader';

export class NistCodeActionProvider implements vscode.CodeActionProvider {
    constructor(private controls: Map<string, NistControl>) {}

    provideCodeActions(
        document: vscode.TextDocument,
        range: vscode.Range | vscode.Selection,
        context: vscode.CodeActionContext,
        token: vscode.CancellationToken
    ): vscode.CodeAction[] {
        const actions: vscode.CodeAction[] = [];

        // Handle diagnostics
        for (const diagnostic of context.diagnostics) {
            if (diagnostic.code === 'unknown-control') {
                // Suggest fixing unknown control
                const match = diagnostic.message.match(/Unknown NIST control: ([a-z]{2}-\d+)/);
                if (match) {
                    const invalidControl = match[1];
                    const suggestedControls = this.findSimilarControls(invalidControl);

                    for (const control of suggestedControls.slice(0, 3)) {
                        const fix = new vscode.CodeAction(
                            `Change to ${control.id}: ${control.title}`,
                            vscode.CodeActionKind.QuickFix
                        );
                        fix.edit = new vscode.WorkspaceEdit();
                        fix.edit.replace(
                            document.uri,
                            diagnostic.range,
                            `@nist ${control.id} "${control.title}"`
                        );
                        actions.push(fix);
                    }
                }
            } else if (diagnostic.code === 'missing-description') {
                // Add description
                const text = document.getText(diagnostic.range);
                const match = text.match(/@nist\s+([a-z]{2}-\d+)/);
                if (match) {
                    const controlId = match[1];
                    const control = this.controls.get(controlId);
                    if (control) {
                        const fix = new vscode.CodeAction(
                            'Add description',
                            vscode.CodeActionKind.QuickFix
                        );
                        fix.edit = new vscode.WorkspaceEdit();
                        fix.edit.replace(
                            document.uri,
                            diagnostic.range,
                            `@nist ${controlId} "${control.title}"`
                        );
                        actions.push(fix);
                    }
                }
            } else if (diagnostic.code === 'missing-tag') {
                // Add NIST tag suggestion
                const addTagAction = new vscode.CodeAction(
                    'Add NIST control tag',
                    vscode.CodeActionKind.QuickFix
                );
                addTagAction.command = {
                    command: 'nist.suggestControls',
                    title: 'Suggest NIST Controls'
                };
                actions.push(addTagAction);
            }
        }

        // Provide refactoring to add NIST tags
        const line = document.lineAt(range.start.line);
        if (!/@nist/.test(line.text)) {
            const addTagAction = new vscode.CodeAction(
                'Add NIST compliance tag',
                vscode.CodeActionKind.RefactorExtract
            );
            addTagAction.command = {
                command: 'nist.suggestControls',
                title: 'Suggest NIST Controls'
            };
            actions.push(addTagAction);
        }

        return actions;
    }

    private findSimilarControls(invalidControl: string): NistControl[] {
        const suggestions: NistControl[] = [];

        // Extract family prefix
        const match = invalidControl.match(/([a-z]{2})-(\d+)/);
        if (match) {
            const family = match[1];
            const number = parseInt(match[2]);

            // Find controls in same family
            for (const control of this.controls.values()) {
                if (control.id.startsWith(family + '-')) {
                    suggestions.push(control);
                }
            }

            // Sort by numeric proximity
            suggestions.sort((a, b) => {
                const aNum = parseInt(a.id.split('-')[1]);
                const bNum = parseInt(b.id.split('-')[1]);
                return Math.abs(aNum - number) - Math.abs(bNum - number);
            });
        }

        return suggestions;
    }
}
