import { ReactElement } from "react"

export type AppPropType = {
    chatResponse: ReactElement,
    aiProvider:string,
    aiModel:string,
    updateProps: (arg: Partial<AppPropType>) => void
}

export const defaultProps: AppPropType = {
    chatResponse: <>Available commands</>,
    aiProvider:'AzureOpenAI',
    aiModel:"GPT-4",
    updateProps:(arg: Partial<AppPropType>) => {}
}
