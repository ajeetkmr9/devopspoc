

export const getFileFolder = (path: string) => {
        return [
            {
              type: "folder",
              name: "src",
              children: [
                {
                  type: "folder",
                  name: "Components",
                  children: [
                    { type: "file", name: "Modal.js" },
                    { type: "file", name: "Modal.css" }
                  ]
                },
                { type: "file", name: "index.js" },
                { type: "file", name: "index.html" }
              ]
            },
            { type: "file", name: "package.json" }
          ]
    // return fs.readdirSync('./dirpath', { withFileTypes: true })
    //     .map((item: any) => {
    //         return {
    //             name: item.name,
    //             path: item.fullpath,
    //             directory: item.isDirectory()
    //         }
    //     })
}