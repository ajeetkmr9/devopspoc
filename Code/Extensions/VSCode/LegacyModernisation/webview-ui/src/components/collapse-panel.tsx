import { ReactElement } from "react";
import Collapsible from "react-collapsible";


const CollapsePanel: React.FC<{ title: string | ReactElement, open?: boolean, tooltip?: string }> = (props) => {


    return (
        <>
            <Collapsible
                open={props.open ?? false}
                triggerTagName="div"
                trigger={props.title}
                //contentHiddenWhenClosed={true}
                overflowWhenOpen='auto'
            >

                {props.children}

            </Collapsible>
        </>
    );
}

export default CollapsePanel;