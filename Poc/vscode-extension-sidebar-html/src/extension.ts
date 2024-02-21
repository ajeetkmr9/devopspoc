import * as vscode from 'vscode';
import { CustomSidebarViewProvider } from './customSidebarViewProvider';

export function activate(context: vscode.ExtensionContext) {
  // Register the webview provider
  const provider = new CustomSidebarViewProvider(context.extensionUri);
  context.subscriptions.push(vscode.window.registerWebviewViewProvider(CustomSidebarViewProvider.viewType, provider));

  // Register the "Refresh Webview" command
  context.subscriptions.push(
    vscode.commands.registerCommand('webviewViewSample.refresh', () => {
      // Refresh logic, if needed
      vscode.window.showInformationMessage('Webview refreshed!');
    })
  );
}

export function deactivate() {
  // Cleanup logic, if needed
}
