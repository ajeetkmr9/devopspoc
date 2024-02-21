import * as vscode from 'vscode';
import { getNonce, getUri } from './utils';
import { handle } from './commands/vscode-handlers';

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

    webviewView.webview.html = this.getHtmlContent(webviewView.webview, this._extensionUri);


    // Handle messages from the webview
    const pmCallback = (x: any) => webviewView.webview.postMessage(x);
    webviewView.webview.onDidReceiveMessage(
      (m) => handle(m, pmCallback, this._extensionContext),
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

  private getHtmlContent(webview: vscode.Webview, extensionUri: vscode.Uri): string {
    // The CSS file from the React build output
    const stylesUri = getUri(webview, extensionUri, [
      "webview-ui",
      "build",
      "static",
      "css",
      "main.css",
    ]);
    // The JS file from the React build output
    const scriptUri = getUri(webview, extensionUri, [
      "webview-ui",
      "build",
      "static",
      "js",
      "main.js",
    ]);

    const nonce = getNonce();

    // Tip: Install the es6-string-html VS Code extension to enable code highlighting below
    return /*html*/ `
          <!DOCTYPE html>
          <html lang="en">
            <head>
              <meta charset="utf-8">
              <meta name="viewport" content="width=device-width,initial-scale=1,shrink-to-fit=no">
              <meta name="theme-color" content="#000000">
              <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline' ${webview.cspSource}; script-src 'nonce-${nonce}';">
              <link rel="stylesheet" type="text/css" href="${stylesUri}">
              <title>TechXform</title>
            </head>
            <body>
              <noscript>You need to enable JavaScript to run this app.</noscript>
              <div id="root"></div>
              <script nonce="${nonce}" src="${scriptUri}"></script>
            </body>
          </html>
        `;
  }

  private dispose() {
    // Dispose of all subscriptions
    this._disposables.forEach((d) => d.dispose());
    this._disposables = [];
  }
}
