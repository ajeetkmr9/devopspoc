import { Uri, Webview } from "vscode";
import { TreeType } from "./types/treeType";


export function getUri(webview: Webview, extensionUri: Uri, pathList: string[]) {
  return webview.asWebviewUri(Uri.joinPath(extensionUri, ...pathList));
}

export function getNonce() {
  let text = "";
  const possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  for (let i = 0; i < 32; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}

export const getAllFilesFromFolder = (dir: string) => {

  var filesystem = require("fs");
  var results: TreeType[] = [];


  filesystem.readdirSync(dir)
    .forEach((file: string) => {
      const path = dir + '/' + file;
      const node: TreeType = {
        name: file,
        path: path,
        type: 'file'
      }


      var stat = filesystem.statSync(path);
      console.log(path, stat.isDirectory())
      if (stat && stat.isDirectory()) {
        if (file.startsWith('.')
          || file.toLocaleLowerCase() == 'obj'
          || file.toLocaleLowerCase() == 'bin')
          return [];
        node.type = 'folder'
        node.children = getAllFilesFromFolder(path)

      }
      results.push(node);
    });

  return results
    .sort((x, y) => x.name.toLocaleLowerCase() < y.name.toLocaleLowerCase() ? 1 : -1)
    .sort((x, y) => x.type == "folder" ? -1 : 1);
};