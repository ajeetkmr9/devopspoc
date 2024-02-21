import * as fs from "fs";
import * as vscode from "vscode";

class VsCodeActions {
    static scanSubFolder(folderPath: any, callback: (x: any) => Thenable<boolean>) {
        console.log('payload', folderPath);
        var directories = fs.readdirSync(folderPath)
            .filter(x => !x.startsWith('.'))
            .map(x=> `${folderPath}/${x}`)
            .map((x) => fs.statSync(x).isDirectory() ? x : '')
            .filter((x) => x != '');
        callback(directories);
    }

    static openSourceFolder = (callback: (msg: any) => Thenable<boolean>) => {
        const options: vscode.OpenDialogOptions = {
            canSelectMany: false,
            openLabel: 'Select Source Folder',
            canSelectFiles: false,
            canSelectFolders: true
        };

        vscode.window.showOpenDialog(options).then((fileUri: any) => {
            if (fileUri && fileUri[0]) {
                callback(fileUri[0].fsPath);
            }
        });
    }
}

export default VsCodeActions;