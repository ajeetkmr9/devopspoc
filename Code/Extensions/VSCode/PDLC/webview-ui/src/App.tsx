import { useState } from "react";
import "./App.css";
import CollapsePanel from "./components/collapse-panel";
import ModelConfig from "./components/model-config";
import { AppPropType, defaultProps } from "./types/AppPropType";
import ChatPanel from "./components/chat-panel";

const App: React.FC = () => {
  const [appState, setAppState] = useState<AppPropType>(defaultProps)
  const updater = (arg: Partial<AppPropType>) => {
    setAppState(Object.assign({}, appState, arg));
    console.log(JSON.stringify(appState))
  }

  const propClone = Object.assign({}, appState, { updateProps: updater });
  return (
    <main>
      <CollapsePanel title="Chat" open={true}>
        <ChatPanel {...propClone}/>
      </CollapsePanel>
      <CollapsePanel title="Model Config">
        <ModelConfig></ModelConfig>
      </CollapsePanel>
    </main>
  );
}



export default App;
