import { VSCodeOption } from "@vscode/webview-ui-toolkit/react";

export const getOptions = (title:string, enumType:{ [s: string]: string } | ArrayLike<string> | {}, selected:string = '') : JSX.Element=> {
    return (
     <>
     <VSCodeOption>-- {title} --</VSCodeOption>
     {
          Object.values(enumType)
             .filter(i => isNaN(Number(i)))
             .map(x=> <VSCodeOption selected={x === selected}>{x}</VSCodeOption>)
     }
     </>
    );
 }