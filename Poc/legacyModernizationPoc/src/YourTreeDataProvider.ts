import * as vscode from 'vscode';

class YourTreeDataProvider implements vscode.TreeDataProvider<TreeNode> {
    private _onDidChangeTreeData: vscode.EventEmitter<TreeNode | undefined | null | void> = new vscode.EventEmitter<TreeNode | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<TreeNode | undefined | null | void> = this._onDidChangeTreeData.event;

    refresh(): void {
        this._onDidChangeTreeData.fire(undefined);
    }

    getTreeItem(element: TreeNode): vscode.TreeItem {
        return element;
    }

    getChildren(element?: TreeNode): vscode.ProviderResult<TreeNode[]> {
        if (!element) {
            // This is the root node
            return [
                new TreeNode('Parent Node', vscode.TreeItemCollapsibleState.Expanded),
                new TreeNode('Another Parent Node', vscode.TreeItemCollapsibleState.Expanded)
            ];
        } else {
            // These are child nodes
            if (element.label === 'Parent Node') {
                // If the clicked node is the 'Parent Node', add a child node representing the webview
                return [new WebviewNode()];
            } else {
                // These are child nodes
                return [
                    new TreeNode('Child Node 1', vscode.TreeItemCollapsibleState.None),
                    new TreeNode('Child Node 2', vscode.TreeItemCollapsibleState.None)
                ];
            }
        }
    }
}

class TreeNode extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState
    ) {
        super(label, collapsibleState);
    }
}

class WebviewNode extends TreeNode {
    constructor() {
        super('Your WebView', vscode.TreeItemCollapsibleState.None);
        this.command = { command: 'extension.showWebView', title: 'Show WebView', arguments: [this] };
    }
}

export { YourTreeDataProvider, TreeNode, WebviewNode };
