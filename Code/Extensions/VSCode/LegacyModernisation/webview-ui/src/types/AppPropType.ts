export type AppPropType = {
    sourceFolder: string,
    sourceFolderTree?: [],

    sourceLanguage: string,
    sourceFramework: string,

    targetLanguage: string,
    targetFramework: string,

    aiProvider: string,
    aiModel: string,

    fileMapping: { source: string, target: string }[]
    folderMapping: { source: string, target: string }[]

    targetFolder: string,
    targetFolderTree?: [],
    updateProps: (arg: Partial<AppPropType>) => void
}

export const defaultProps: AppPropType = {
    sourceFolder: '',
    updateProps: (x: any) => { },
    sourceLanguage: "",
    sourceFramework: "",
    targetLanguage: "",
    targetFramework: "",
    aiProvider: "",
    aiModel: "",
    fileMapping: [],
    folderMapping: [],
    targetFolder: ""
}
