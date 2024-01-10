import { CSSProperties } from "react";
import Collapsible from "react-collapsible";


const CollapsePanel: React.FC<{ title: string, open?: boolean, style?: CSSProperties, className?: string }> = (props) => {
    return (
        <>
            <Collapsible
                style={props.style}
                className={props.className}
                open={props.open ?? false}
                triggerTagName="div"
                trigger={props.title}
                overflowWhenOpen='auto'
            >
                {props.children}
            </Collapsible>
        </>
    );
}

export default CollapsePanel;