import File from './file';
import Folder from './folder';
const TreeRecursive: React.FC<{ data: any[] }> = ({data}) => {
    // loop through the data
    
    const createTreeView = () => {
        if(!data) return <></>
        return data.map((item:any) => {
            // if its a file render <File />
            if (item.type === 'file') {
              return <File name={item.name} />;
            }
            // if its a folder render <Folder />
            if (item.type === 'folder') {
              return (
                <Folder name={item.name} >
                  <TreeRecursive data={item.children} />
                </Folder>
              );
            }
            return <></>
          });
    
    }

    return <>
        {createTreeView()}
    </>
};

export default TreeRecursive;