import styled from "styled-components";
import TreeRecursive from "./tree-recursive";

const StyledTree = styled.div`
  line-height: 1.5;
`;

const TreeView: React.FC<{ data: any, children?: any }> = ({ data, children }) => {
  const isImperative = data && !children;

  return <StyledTree>{isImperative ? <TreeRecursive data={data} /> : children}</StyledTree>;
};

export default TreeView