
import { useState } from "react";
import { AppPropType } from "../types/AppPropType";
import { VSCodeButton, VSCodeTextField } from "@vscode/webview-ui-toolkit/react";

const Configuration: React.FC<AppPropType> = (props) => {

    const onTextChange = (propName: string, e: any) => {
        let newprop: { [key: string]: string } = {};
        newprop[propName] = e.target.value;
        props.updateProps(Object.assign({}, props, newprop))
    }

    const onCommandExecute = () => {
    }
    const displayPreference = (title: string, value: string) => {
        return value ? <div><span className="bold">{title}:</span> {value}</div> : <></>
    }
    const getSummary = () => {
        return <p className="summary">
            {displayPreference("Cpu", props.cpuConfig)}
            {displayPreference("Memory", props.memoryConfig)}
            {displayPreference("OS", props.osConfig)}
            {displayPreference("Bit Arch.", props.bitArchitecture)}
            {displayPreference("Language", props.language)}
            {displayPreference("Framework", props.framework)}
            {displayPreference("GenAI Provide", props.aiProvider)}
            {displayPreference("GetAI Model", props.aiModel)}

        </p>
    }
    return <>
        <div style={{ display: "flex", flexDirection: "column" }}>
            <VSCodeTextField
                onChange={(e) => onTextChange('cpuConfig', e)}
                autoFocus placeholder="/CPU Configuration"
                value={props.cpuConfig}
            />
            <VSCodeTextField
                onChange={(e) => onTextChange('memoryConfig', e)}
                autoFocus placeholder="/Memory Configuration"
                value={props.memoryConfig}
            />

            <VSCodeTextField
                onChange={(e) => onTextChange('osConfig', e)}
                autoFocus placeholder="/Operating System"
                value={props.osConfig}
            />

            <VSCodeTextField
                onChange={(e) => onTextChange('bitArchitecture', e)}
                autoFocus placeholder="/Bit Architecture"
                value={props.bitArchitecture}
            />

            <VSCodeTextField
                onChange={(e) => onTextChange('language', e)}
                autoFocus placeholder="/Programing Language"
                value={props.language}
            />

            <VSCodeTextField
                onChange={(e) => onTextChange('framework', e)}
                autoFocus placeholder="/Application Framework"
                value={props.framework}
            />

            <div>{getSummary()}</div>

            <VSCodeButton
                onClick={onCommandExecute}
            >Generate</VSCodeButton>

            <div>
                {props.sustainableResult}
            </div>
        </div>
    </>
}

export default Configuration;