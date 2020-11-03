import React from "react";
import styled from "styled-components";

const StyledContainer = styled.div`
    box-sizing: border-box;
    background-color: ${(props) => props.theme.shade1};
    width: 100%;
    display: grid;
    grid-template-rows: 1fr auto;
    align-items: end;
    height: 100%;
    align-content: stretch;
    align-items: stretch;

    @media (min-width: 768px) {
        border-right: 1px solid ${(props) => props.theme.shade2};
    }
`;

const StyledChatOverflow = styled.div`
    height: 100%;
    overflow-y: auto;
`;

const StyledChat = styled.div`
    min-height: 100%;
    display: flex;
    align-items: flex-end;
    flex-wrap: wrap;
    align-content: flex-end;
`;

const StyledChatEditor = styled.div`
    position: relative;
    border-top: 1px solid ${(props) => props.theme.shade2};
    margin-top: 20px;
`;

const StyledNoContentContainer = styled.div`
    font-style: italic;
    color: ${(props) => props.theme.shade2};
`;

const StyledLoadingContainer = styled.div`
    font-style: italic;
    color: ${(props) => props.theme.shade2};
`;

const ChatLayout = (props) => {
    let postContent = props.children;

    if (postContent.length <= 0 && !props.loading) {
        postContent = (
            <StyledNoContentContainer>No posts yet</StyledNoContentContainer>
        );
    } else if (props.loading) {
        postContent = (
            <StyledLoadingContainer>Loading chat...</StyledLoadingContainer>
        );
    }
    return (
        <StyledContainer>
            <StyledChatOverflow>
                <StyledChat>{postContent}</StyledChat>
            </StyledChatOverflow>
            <StyledChatEditor>{props.editor}</StyledChatEditor>
        </StyledContainer>
    );
};

export default ChatLayout;
