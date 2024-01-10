
export const Minify = (input: string, padding: number = 15) => {
    if(!input) return '';
    if(input && input.length <= padding * 2 + 5 ) return input;

    return input.substring(0, padding)
        + "..."
        + input.substring(input.length - padding)
}