import * as vscode from "vscode";
import VsCodeActions from "./vscode-actions";



export const handle = (message: any, postMessageCallback: (msg: any) => Thenable<boolean>, context: vscode.ExtensionContext) => {
    {
        const command = message.command;
        const payload = message.payload;
        switch (command) {
            case "SourceFolderSelect":
                VsCodeActions.openSourceFolder(postMessageCallback);
                break;
            case "scanSubFolder":
                VsCodeActions.scanSubFolder(payload, postMessageCallback);
        }
    }
}