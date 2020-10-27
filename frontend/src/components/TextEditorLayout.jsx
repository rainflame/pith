import React from "react";
import ContentEditable from "react-contenteditable";

import styled from "styled-components";

import { Button } from "./StandardUI";
import { UpArrow, RightArrow } from "./Symbols";

const StyledButton = styled(Button)`
    position: absolute;
    height: calc(100% - 2px);
    right: 1px;
    top: 1px;
    padding-top: 0;
    background-color: ${(props) => props.theme.shade1};

    :hover {
        background-color: ${(props) => props.theme.shade1};
        color: ${(props) => props.theme.shade3};
    }
`;

const StyledContainer = styled.div`
    position: relative;
    width: 100%;
    margin: ${(props) => (props.showButton ? 20 : 0)}px 0;
`;

const StyledEditor = styled(ContentEditable)`
    box-sizing: border-box;
    display: inline-block;
    padding-right: ${(props) => (props.showButton ? 50 : 0)}px;
    width: 100%;
    margin: 0;
    font-family: ${(props) => props.theme.serif};

    :empty::after {
        color: ${(props) => props.theme.shade2};
        content: "${(props) => `${props.placeholder}` || "type a message..."}";
    }

    :focus {
        outline: none;
    }
`;

const TextEditorLayout = (props) => {
    return (
        <StyledContainer showButton={props.showButton}>
            <StyledEditor {...props} />
            {props.showButton ? (
                <StyledButton>
                    {props.buttonDir === "right" ? <RightArrow /> : <UpArrow />}
                </StyledButton>
            ) : null}
        </StyledContainer>
    );
};

export default TextEditorLayout;