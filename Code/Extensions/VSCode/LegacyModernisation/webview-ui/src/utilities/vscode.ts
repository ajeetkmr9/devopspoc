import type { WebviewApi } from "vscode-webview";
import { vsCodeOutCommand } from "./vscode-commands";

type cmdMsg = {
  command: vsCodeOutCommand,
  payload: any
}

class VSCodeAPIWrapper {
  private readonly vsCodeApi: WebviewApi<cmdMsg> | undefined;

  constructor() {
    if (typeof acquireVsCodeApi === "function") {
      this.vsCodeApi = acquireVsCodeApi();
    }
  }

  public postMessage(message: Partial<cmdMsg>, callback?: (msg: any) => void) {
    debugger;
    console.log(message)
    if (this.vsCodeApi) {
      if (callback)
        this.onMessage(callback)
      this.vsCodeApi.postMessage(message);
    } else {
      console.log(message);
    }
  }

  public onMessage(callback: (message: any) => void): () => void {
    window.addEventListener('message', callback);
    return () => {debugger; window.removeEventListener('message', callback);};
  }

  public getState(): unknown | undefined {
    if (this.vsCodeApi) {
      return this.vsCodeApi.getState();
    } else {
      const state = localStorage.getItem("vscodeState");
      return state ? JSON.parse(state) : undefined;
    }
  }

  public setState<T extends cmdMsg | undefined>(newState: T): T {
    if (this.vsCodeApi) {
      return this.vsCodeApi.setState(newState);
    } else {
      localStorage.setItem("vscodeState", JSON.stringify(newState));
      return newState;
    }
  }
}

// Exports class singleton to prevent multiple invocations of acquireVsCodeApi.
export const vscode = new VSCodeAPIWrapper();
