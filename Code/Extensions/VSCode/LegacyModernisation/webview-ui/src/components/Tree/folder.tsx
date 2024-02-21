
import React, { ReactElement, useState } from 'react';
import styled from 'styled-components';
import { MdFolderOpen, MdFolder } from 'react-icons/md';

const StyledFolder = styled.div`
  padding-left: 20px;
  cursor:pointer;
  .folder--label {
    display: flex;
    align-items: center;
    span {
      margin-left: 5px;
      padding:0 5px;
    }
    span:hover {
      color:#000;
      background-color:orange;
    }
  }
`;
const Collapsible = styled.div<{ isOpen: boolean }>`
  /* set the height depending on isOpen prop */
  height: ${(p: any) => (p.isOpen ? 'auto' : '0')};
  /* hide the excess content */
  overflow: hidden;
`;


const Folder: React.FC<{ name: string, children?: ReactElement }> = ({ name, children }) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleToggle = (e: any) => {
    e.preventDefault();
    setIsOpen(!isOpen);
  };

  return (
    <StyledFolder>
      <div className="folder--label" onClick={handleToggle}>
        {isOpen?<MdFolderOpen/>:<MdFolder/>}
        <span>{name}</span>
      </div>
      <Collapsible isOpen={isOpen}>{children}</Collapsible>
    </StyledFolder>
  );
};

export default Folder;