
import { useState } from "react";
import { AppPropType } from "../types/AppPropType";
import { VSCodeButton, VSCodeTextField } from "@vscode/webview-ui-toolkit/react";

const ChatPanel: React.FC<AppPropType> = (props) => {

    const [chatText, setChatText] = useState('');
    const onTextChange = (e: any) => {
        setChatText(e.target.value)
    }

    const onCommandExecute = () => {
        props.updateProps(Object.assign({}, props, { chatResponse: <>{props.chatResponse} <p>{chatText}</p></> }))
        setChatText('');
    }

    return <>
        <div>
            {props.chatResponse}
        </div>
        <div style={{ display: "flex" }}>
            <VSCodeTextField
                onChange={onTextChange}
                autoFocus placeholder="/command: your message"
                value={chatText}
                style={{ flex: 1 }} />
            <VSCodeButton
                onClick={onCommandExecute}
            >&gt;</VSCodeButton>
        </div>
    </>
}

export default ChatPanel;