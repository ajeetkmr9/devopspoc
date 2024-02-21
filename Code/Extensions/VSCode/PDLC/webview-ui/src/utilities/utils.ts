
export const Minify = (input: string, padding: number = 15) => {
    return input.substring(0, padding)
        + "..."
        + input.substring(input.length - padding)
}