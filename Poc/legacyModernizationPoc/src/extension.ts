import * as vscode from 'vscode';
import * as path from 'path';
import { YourTreeDataProvider,WebviewNode } from './YourTreeDataProvider';

export function activate(context: vscode.ExtensionContext) {
    const treeDataProvider = new YourTreeDataProvider();

    // Create your tree view
    const treeView = vscode.window.createTreeView('yourTreeViewId', {
        treeDataProvider,
        showCollapseAll: true
    });
    context.subscriptions.push(treeView);

    // Register the "Show WebView" command
    let webViewDisposable = vscode.commands.registerCommand('extension.showWebView', function (node: WebviewNode) {
        // Get the path to the HTML file
        const panel = vscode.window.createWebviewPanel(
            'yourExtensionWebView', // Identifies the type of the webview. Used internally
            'Your Extension WebView', // Title of the panel displayed to the user
            vscode.ViewColumn.One, // Editor column to show the new webview panel in
            {
                enableScripts: true // Enable scripts in the webview
            }
        );

        // Use the relative path to your HTML file
        const relativePath = path.join('webviews', 'index.html');
        const htmlContentPromise = getWebviewContent(context, relativePath);

        htmlContentPromise.then(htmlContent => {
            panel.webview.html = htmlContent;
        }, error => {
            console.error(`Error reading HTML content: ${error.message}`);
            vscode.window.showErrorMessage(`Error reading HTML content: ${error.message}`);
        });
    });

    context.subscriptions.push(webViewDisposable);
}

function getWebviewContent(context: vscode.ExtensionContext, relativePath: string): Thenable<string> {
    const absolutePath = context.asAbsolutePath(relativePath);

    // Use fs.readFile to read the HTML file directly from the file system
    const fs = require('fs');

    return new Promise<string>((resolve, reject) => {
        fs.readFile(absolutePath, 'utf-8', (err: any, data: any) => {
            if (err) {
                reject(err);
            } else {
                resolve(data);
            }
        });
    }).then(htmlContent => htmlContent).catch(error => {
        console.error(`Error reading HTML content: ${error.message}`);
        vscode.window.showErrorMessage(`Error reading HTML content: ${error.message}`);
        return ''; // Return an empty string or handle the error as needed
    });
}

// this method is called when your extension is deactivated
export function deactivate() { }
