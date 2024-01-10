import * as vscode from 'vscode';

export class CustomSidebarViewProvider implements vscode.WebviewViewProvider {
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
      (message) => {
        switch (message.command) {
          case 'submitForm':
            // Save inputs in the extension's context
            this.saveInputsInContext(message.fileInput);
            // Show information message with the submitted data
            vscode.window.showInformationMessage(`Form submitted with message- ${JSON.stringify(message)}`);
            break;
          case 'showError':
            // Show error message in VS Code
            vscode.window.showErrorMessage(message.text);
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
      <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline' ${webview.cspSource} 'nonce-${nonce}'; script-src 'nonce-${nonce}';">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link rel="stylesheet" href="${stylesheetUri}">
      <link rel="stylesheet" href="${styleResetUri}">
      <link rel="stylesheet" href="${styleVSCodeUri}">
    </head>
    <body>
      <div class="outer-container">
        <div class="container">
          <div class="inner-container">
            <button id="submitBtn" class="submit-btn">Select Source</button>
            <input type="file" id="fileInput" style="display:none;" />
          </div>
          <div class="inner-container">
            <button id="button1" class="submit-btn">Select Source Language/Framework</button>
          </div>
          <div class="inner-container">
            <button id="button2" class="submit-btn">Select Target Language/Framework</button>
          </div>
          <div class="inner-container">
            <button id="button3" class="submit-btn">Download Template/Choose Template</button>
          </div>
        </div>
        <div class="container">
          <h3>Folder Tree View</h3>
          <div id="folderTreeViewContainer"></div>
        </div>
        <div class="container">
        Hello3
        </div>
        <div class="container">
        Hello
        </div>
      </div>
      <script nonce="${nonce}">
        ${vscodeScript}
        const fileInput = document.getElementById('fileInput');
        const buttonsToDisable = ['button1', 'button2', 'button3']; // Add the IDs of other buttons to disable
        fileInput.style.display = 'none';
        // Disable and blur other buttons
        buttonsToDisable.forEach((buttonId) => {
          const button = document.getElementById(buttonId);
          if (button) {
            button.classList.add('blurred');
            button.disabled = true;
          }
        });
        // Add an event listener to the "Select Source" button
        document.getElementById('submitBtn').addEventListener('click', function () { 
          // Trigger click on the hidden file input
          document.getElementById('fileInput').click();
        });

        // Add an event listener to the file input for handling file selection
        document.getElementById('fileInput').addEventListener('change', function (event) {
          const selectedFile = event.target.files[0];
          // Now you can do something with the selected file, for example, log its name
          console.log('Selected file:', selectedFile.name);
    
          // Enable and un-blur other buttons after file selection
          buttonsToDisable.forEach((buttonId) => {
            const button = document.getElementById(buttonId);
            if (button) {
             button.classList.remove('blurred');
              button.disabled = false;
            }
          });
        });
      </script>
      <script nonce="${nonce}" src="${scriptUri}"></script>
    </body>
  </html>`;
  }

  private getInputsFromContext(): { fileInput?: string } {
    return this._extensionContext?.workspaceState.get('userInputs') || {};
  }

  private saveInputsInContext(fileInput: string): void {
    this._extensionContext?.workspaceState.update('userInputs', { fileInput });
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
