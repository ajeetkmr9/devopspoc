import * as vscode from 'vscode';

export class YourWebViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'yourWebViewId';

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        webviewView.webview.options = {
            enableScripts: true
        };

        // Use a nonce to only allow a specific script to be run
        const nonce = getNonce();
        webviewView.webview.html = getWebviewContent(nonce);

        function getWebviewContent(nonce: string): string {
            return `<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'nonce-${nonce}';">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Webview</title>
            </head>
            <body>
                <h1>Hello from your WebView!</h1>
            </body>
            </html>`;
        }
    }
}

function getNonce() {
    let text = '';
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < 32; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}
