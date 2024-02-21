
import styled from "styled-components";
import FILE_ICONS from './icons';
import { MdDescription } from 'react-icons/md';

const StyledFile = styled.div`
  padding-left: 20px;
  display: flex;
  align-items: center;
  cursor:pointer;
  span {
    margin-left: 5px;
    padding:0 5px;
  }
  span:hover {
    color:#000;
    background-color:orange;
  }
`;


const File: React.FC<{ name: string }> = ({ name }) => {
  // get the extension
  let ext = name.split('.')[1];

  return (
    <StyledFile>
      {/* render the extension or fallback to generic file icon  */}
      {FILE_ICONS[ext] || <MdDescription />}
      <span>{name}</span>
    </StyledFile>
  );
};

export default File;