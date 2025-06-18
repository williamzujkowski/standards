import * as vscode from 'vscode';
import { NistControlProvider } from './providers/controlProvider';
import { NistDiagnosticProvider } from './providers/diagnosticProvider';
import { NistCompletionProvider } from './providers/completionProvider';
import { NistHoverProvider } from './providers/hoverProvider';
import { NistCodeActionProvider } from './providers/codeActionProvider';
import { loadNistControls, NistControl } from './data/controlsLoader';

export function activate(context: vscode.ExtensionContext) {
    console.log('NIST Compliance Helper is now active!');

    // Load NIST controls data
    const controls = loadNistControls();

    // Create providers
    const controlProvider = new NistControlProvider(controls);
    const diagnosticProvider = new NistDiagnosticProvider(controls);
    const completionProvider = new NistCompletionProvider(controls);
    const hoverProvider = new NistHoverProvider(controls);
    const codeActionProvider = new NistCodeActionProvider(controls);

    // Register completion provider for @nist tags
    const completionDisposable = vscode.languages.registerCompletionItemProvider(
        [
            { scheme: 'file', language: 'javascript' },
            { scheme: 'file', language: 'typescript' },
            { scheme: 'file', language: 'python' },
            { scheme: 'file', language: 'go' },
            { scheme: 'file', language: 'yaml' }
        ],
        completionProvider,
        '@'
    );

    // Register hover provider for control information
    const hoverDisposable = vscode.languages.registerHoverProvider(
        [
            { scheme: 'file', language: 'javascript' },
            { scheme: 'file', language: 'typescript' },
            { scheme: 'file', language: 'python' },
            { scheme: 'file', language: 'go' },
            { scheme: 'file', language: 'yaml' }
        ],
        hoverProvider
    );

    // Register code action provider for quick fixes
    const codeActionDisposable = vscode.languages.registerCodeActionProvider(
        [
            { scheme: 'file', language: 'javascript' },
            { scheme: 'file', language: 'typescript' },
            { scheme: 'file', language: 'python' },
            { scheme: 'file', language: 'go' },
            { scheme: 'file', language: 'yaml' }
        ],
        codeActionProvider
    );

    // Register commands
    const suggestCommand = vscode.commands.registerCommand('nist.suggestControls', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor');
            return;
        }

        const suggestions = await controlProvider.suggestControlsForFunction(editor.document, editor.selection.active);
        if (suggestions.length > 0) {
            const quickPick = vscode.window.createQuickPick();
            quickPick.items = suggestions.map(control => ({
                label: control.id,
                description: control.title,
                detail: control.description
            }));
            quickPick.onDidChangeSelection(selection => {
                if (selection[0]) {
                    insertNistTag(editor, selection[0].label, selection[0].description || '');
                }
                quickPick.hide();
            });
            quickPick.show();
        } else {
            vscode.window.showInformationMessage('No specific controls suggested for this code');
        }
    });

    const validateCommand = vscode.commands.registerCommand('nist.validateFile', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor');
            return;
        }

        diagnosticProvider.validateDocument(editor.document);
        vscode.window.showInformationMessage('NIST control validation complete');
    });

    const reportCommand = vscode.commands.registerCommand('nist.generateReport', async () => {
        const report = await controlProvider.generateComplianceReport();
        const doc = await vscode.workspace.openTextDocument({
            content: report,
            language: 'markdown'
        });
        vscode.window.showTextDocument(doc);
    });

    // Auto-validate on save
    const saveDisposable = vscode.workspace.onDidSaveTextDocument(document => {
        const config = vscode.workspace.getConfiguration('nist');
        if (config.get('validateOnSave')) {
            diagnosticProvider.validateDocument(document);
        }
    });

    // Real-time suggestions
    const changeDisposable = vscode.workspace.onDidChangeTextDocument(event => {
        const config = vscode.workspace.getConfiguration('nist');
        if (config.get('autoSuggest') && event.contentChanges.length > 0) {
            const document = event.document;
            const position = event.contentChanges[0].range.start;

            // Check if we're in a security-related context
            controlProvider.checkForSecurityPatterns(document, position).then(patterns => {
                if (patterns.length > 0 && !hasNistTagNearby(document, position)) {
                    vscode.window.showInformationMessage(
                        `Consider adding NIST controls for ${patterns[0]}`,
                        'Add Control'
                    ).then(selection => {
                        if (selection === 'Add Control') {
                            vscode.commands.executeCommand('nist.suggestControls');
                        }
                    });
                }
            });
        }
    });

    context.subscriptions.push(
        completionDisposable,
        hoverDisposable,
        codeActionDisposable,
        suggestCommand,
        validateCommand,
        reportCommand,
        saveDisposable,
        changeDisposable
    );
}

function insertNistTag(editor: vscode.TextEditor, controlId: string, description: string) {
    const position = editor.selection.active;
    const line = editor.document.lineAt(position.line);
    const indent = line.text.match(/^\s*/)?.[0] || '';

    let tagFormat: string;
    const language = editor.document.languageId;

    switch (language) {
        case 'python':
            tagFormat = `${indent}# @nist ${controlId} "${description}"`;
            break;
        case 'yaml':
            tagFormat = `${indent}# @nist ${controlId} "${description}"`;
            break;
        case 'go':
            tagFormat = `${indent}// @nist ${controlId} "${description}"`;
            break;
        default: // JavaScript/TypeScript
            tagFormat = `${indent}// @nist ${controlId} "${description}"`;
    }

    editor.edit(editBuilder => {
        editBuilder.insert(new vscode.Position(position.line, 0), tagFormat + '\n');
    });
}

function hasNistTagNearby(document: vscode.TextDocument, position: vscode.Position, radius: number = 5): boolean {
    const startLine = Math.max(0, position.line - radius);
    const endLine = Math.min(document.lineCount - 1, position.line + radius);

    for (let i = startLine; i <= endLine; i++) {
        const line = document.lineAt(i).text;
        if (/@nist\s+[a-z]{2}-\d+/.test(line)) {
            return true;
        }
    }
    return false;
}

export function deactivate() {}
