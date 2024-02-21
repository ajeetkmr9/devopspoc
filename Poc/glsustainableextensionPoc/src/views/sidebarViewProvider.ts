import * as vscode from 'vscode';

export class SidebarViewProvider implements vscode.WebviewViewProvider {
  public static readonly viewType = 'vscodeSidebar.openview';

  private _view?: vscode.WebviewView;
  private _disposables: vscode.Disposable[] = [];
  private _extensionContext!: vscode.ExtensionContext;

  constructor(private readonly _extensionUri: vscode.Uri) { }

  activate(context: vscode.ExtensionContext) {
    this._extensionContext = context;
  }

  resolveWebviewView(
    webviewView: vscode.WebviewView,
    _context: vscode.WebviewViewResolveContext<unknown>,
    _token: vscode.CancellationToken
  ): void | Thenable<void> {
    this._view = webviewView;

    webviewView.webview.options = {
      enableScripts: true,
      localResourceRoots: [this._extensionUri],
    };

    webviewView.webview.html = this.getHtmlContent(webviewView.webview);

    // Retrieve inputs from the context and send them to the webview
    const inputs = this.getInputsFromContext();
    webviewView.webview.postMessage({
      command: 'updateInputs',
      inputs: inputs,
    });

    // Handle messages from the webview
    webviewView.webview.onDidReceiveMessage(
      (message: any) => {
        switch (message.command) {
          case 'submitForm':
            // Save inputs in the extension's context
            //this.saveInputsInContext(message.cpu, message.os, message.memory, message.selectedCode);
            // Show information message with the submitted data
            vscode.window.showInformationMessage(`Form submitted with message- ${JSON.stringify(message)}`);
            break;
          case 'showError':
            // Show error message in VS Code
            vscode.window.showErrorMessage(message.text);
            break;
          case 'showInformationMessage':
            // Show Info message in VS Code
            vscode.window.showInformationMessage(message.text);
            break;
          // Add more cases if needed
        }
      },
      undefined,
      this._disposables
    );

    // Dispose of subscriptions when the view is closed
    webviewView.onDidDispose(
      () => {
        this.dispose();
      },
      null,
      this._disposables
    );
  }

  private getHtmlContent(webview: vscode.Webview): string {
    const scriptUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, 'assets', 'main.js'));
    const styleResetUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, 'assets', 'reset.css'));
    const styleVSCodeUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, 'assets', 'vscode.css'));
    const stylesheetUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, 'assets', 'main.css'));

    const nonce = this.getNonce();

    // Pass the vscode object to the webview
    const vscodeObject = {
      postMessage: (message: any) => {
        webview.postMessage(message);
      },
      getState: () => {
        return {
          update: (key: any, value: any) => {
            // Implement your logic to update workspace state
            this._extensionContext.workspaceState.update(key, value);
          },
          get: (key: any) => {
            // Implement your logic to retrieve workspace state
            return this._extensionContext.workspaceState.get(key);
          },
        };
      },
      window: {
        showInformationMessage: (message: string) => {
          // Implement your logic to show information message
          vscode.window.showInformationMessage(message);
        },
        showErrorMessage: (message: string) => {
          // Implement your logic to show error message
          vscode.window.showErrorMessage(message);
        },
      },
    };

    const vscodeScript = `
    const vscode = acquireVsCodeApi();
  `;

    return `<!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Security-Policy" script-src 'self' http://localhost:3000/* 'unsafe-inline' 'unsafe-eval';">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="${stylesheetUri}">
    <link rel="stylesheet" href="${styleResetUri}">
    <link rel="stylesheet" href="${styleVSCodeUri}">
  </head>
  <body>
      <div class="container">
          <input type="text" id="cpu" class="textbox" placeholder="Enter CPU" required>

          <input type="text" id="os" class="textbox" placeholder="Enter OS" required>

          <input type="text" id="memory" class="textbox" placeholder="Enter Memory" required>

          <textarea id="selectedCode" class="textarea"  placeholder="Selected Code" required></textarea>

          <button id="submitBtn" class="submit-btn">Submit</button>
      </div>

      <script nonce="${nonce}">
        ${vscodeScript}
      </script>
      <script nonce="${nonce}" src="${scriptUri}"></script>
  </body>
  </html>`;
  }

  private getInputsFromContext(): { cpu?: string; os?: string; memory?: string; selectedCode?: string } {
    return this._extensionContext?.workspaceState.get('userInputs') || {};
  }

  private saveInputsInContext(cpu: string, os: string, memory: string, selectedCode: string): void {
    this._extensionContext?.workspaceState.update('userInputs', { cpu, os, memory, selectedCode });
  }

  private getNonce() {
    let text = '';
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < 32; i++) {
      text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
  }

  private dispose() {
    // Dispose of all subscriptions
    this._disposables.forEach((d) => d.dispose());
    this._disposables = [];
  }
}
