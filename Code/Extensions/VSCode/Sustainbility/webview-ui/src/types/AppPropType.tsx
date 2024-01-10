import { ReactElement } from "react"

export type AppPropType = {
    sustainableResult: ReactElement,
    cpuConfig:string,
    memoryConfig:string,
    osConfig:string,
    bitArchitecture:string,
    language:string,
    framework:string
    aiProvider:string,
    aiModel:string,
    updateProps: (arg: Partial<AppPropType>) => void
}

export const defaultProps: AppPropType = {
    sustainableResult: <></>,
    aiProvider:'AzureOpenAI',
    aiModel:"GPT-4",
    cpuConfig:'',
    memoryConfig:'',
    osConfig:'',
    bitArchitecture:'',
    language:'',
    framework:'',
    updateProps:(arg: Partial<AppPropType>) => {}
}
