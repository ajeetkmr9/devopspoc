import { useState } from "react";
import "./App.css";
import TreeView from "./components/Tree/tree-view";
//import TreeView from "./components/Tree/tree-view";

import CollapsePanel from "./components/collapse-panel";

import Configuration from "./components/configuration";
import FileMap from "./components/file-map";
import FolderMap from "./components/folder-map";
import ModelConfig from "./components/model-config";
import { getFileFolder } from "./utilities/file-system";
import { AppPropType, defaultProps } from "./types/AppPropType";
import { Minify } from "./utilities/utils";
import { vsCodeOutCommand } from "./utilities/vscode-commands";
import { vscode } from "./utilities/vscode";

const App: React.FC = () => {
  const structure = getFileFolder('')
  const [appState, setAppState] = useState<AppPropType>(defaultProps)
  const updater = (arg: Partial<AppPropType>) => {
    setAppState(Object.assign({}, appState, arg));
    console.log(JSON.stringify(appState))
  }

  const cloneProp = Object.assign({}, appState, { updateProps: updater });

  const onSourceFolderSelect = (message: any) => {
    console.log(JSON.stringify(message))
    let newState = Object.assign({}, appState, { sourceFolder: message.data.folderPath, sourceFolderTree: message.data.folderTree});
    setAppState(newState)
}
const onSourceDiskClick = (e: any) => {
    e.preventDefault();
    e.stopPropagation();
    vscode.postMessage({ command: vsCodeOutCommand.SelectSourceFolder }, onSourceFolderSelect)
}

const onTargetFolderSelect = (message: any) => {
  console.log(JSON.stringify(message))
  let newState = Object.assign({}, appState, { targetFolder: message.data.folderPath, targetFolderTree: message.data.folderTree});
  setAppState(newState)
}
const onTargetDiskClick = (e:any) => {
  e.preventDefault();
  e.stopPropagation();
  vscode.postMessage({ command: vsCodeOutCommand.SelectSourceFolder }, onTargetFolderSelect)
}
  return (


    <main>
      <CollapsePanel
        title={<span>Select source code from <a href="#" onClick={onSourceDiskClick}>disk</a> or <a href="#">git repo</a><br />
          {Minify(appState.sourceFolder)}
        </span>}
        open={appState.sourceFolderTree && appState.sourceFolderTree?.length > 0}
      >
        <TreeView data={appState.sourceFolderTree ?? []}></TreeView>
      </CollapsePanel>
      <CollapsePanel
        title={"Language Settings"}
        open={appState.sourceFolderTree && appState.sourceFolderTree?.length > 0}
      >
        <Configuration {...cloneProp}></Configuration>
      </CollapsePanel>
      <CollapsePanel title="File Mapping">
        <FileMap />
      </CollapsePanel>
      <CollapsePanel title="Folder Mapping">
        <FolderMap />
      </CollapsePanel>
      <CollapsePanel
        title={<span><a href="#">Download</a> our template or choose <a href="#" onClick={onTargetDiskClick}>your project structure</a></span>}
        tooltip={"Converted Code " + appState.targetFolder}
        open={appState.targetFolderTree && appState.targetFolderTree?.length > 0}
      >
        <TreeView data={appState.targetFolderTree ?? []}></TreeView>
      </CollapsePanel>
      <CollapsePanel title="Extension Settings">
        <ModelConfig></ModelConfig>
      </CollapsePanel>

    </main>

  );
}



export default App;
