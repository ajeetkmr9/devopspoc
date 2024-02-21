import * as vscode from 'vscode';
import { SidebarViewProvider } from './views/sidebarViewProvider';

export function activate(context: vscode.ExtensionContext) {
  // Register the webview provider
  const provider = new SidebarViewProvider(context.extensionUri);
  context.subscriptions.push(vscode.window.registerWebviewViewProvider(SidebarViewProvider.viewType, provider));

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
