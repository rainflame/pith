<script>
    import { beforeUpdate, afterUpdate, onMount } from "svelte";

    import ChatUnit from "../unit/ChatUnit.svelte";

    let div;
    let autoscroll;

    let messages = [
        {
            pith:
                "Libero repellat molestias et soluta nihil. Repudiandae illum officiis sunt veniam est",
            author: "Christian",
            time: "2021-02-05T02:57:01.206Z",
        },
        {
            pith:
                "Possimus nemo voluptatem ut beatae cumque cumque ea voluptas.",
        },
        {
            pith:
                "Asperiores temporibus adipisci est occaecati perspiciatis quis quibusdam",
            author: "Sydney",
            time: "2021-02-05T03:01:01.206Z",
        },
    ];
    let prevNumMessages = messages.length;
    let missedMessages = 0;

    beforeUpdate(() => {
        autoscroll =
            div && div.offsetHeight + div.scrollTop > div.scrollHeight - 20;
    });

    afterUpdate(() => {
        if (autoscroll) div.scrollTo(0, div.scrollHeight);
        else if (prevNumMessages < messages.length) {
            // add an indication that a message was missed
            missedMessages += 1;
            prevNumMessages = messages.length;
        }
    });

    onMount(() => {
        // add messages at a regular interval for testing purposes
        // window.setInterval(() => {
        //     messages = [...messages, messages[0]];
        // }, 2000);
    });

    const handleScroll = () => {
        if (
            missedMessages > 0 &&
            Math.abs(div.scrollHeight - div.scrollTop - div.clientHeight) <= 5
        ) {
            missedMessages = 0;
        }
    };
</script>

<!--<script>
	import { chat } from "../../stores/chat";
	import { discussionJoinStatus } from "../../stores/discussionJoinStatus";

	import ChatMessage from "./ChatMessage.svelte";

	let content = "";

	const onSubmit = () => {
		if (content !== "") {
			chat.makePost(content, $discussionJoinStatus.nickname);
			content = "";
		}
	};

	const onKeydown = (e) => {
		if (e.key === "Enter") onSubmit();
	};
</script><div>
	{#each $chat.messages as message}
	<ChatMessage {...$chat.messagesContent[message]} />
	{/each} {#each $chat.pendingMessages as message}
	<ChatMessage {...$chat.messagesContent[message]} />
	{/each}
	<input
		placeholder="type a message..."
		bind:value="{content}"
		on:keydown="{onKeydown}"
	/>
</div> -->

<div class="chat-wrapper">
    <div class="chat-overflow" bind:this={div} on:scroll={handleScroll}>
        <div class="chat">
            {#each messages as message}
                <ChatUnit
                    pith={message.pith}
                    author={message.author}
                    time={message.time}
                />
            {/each}
        </div>
    </div>

    <div class="chat-base">
        {#if missedMessages > 0}
            <div class="chat-missed-messages">
                Missed messages: {missedMessages}
            </div>
        {/if}

        <input placeholder="type a message..." />
    </div>
</div>

<style>
    .chat-overflow {
        height: 100%;
        overflow-y: auto;
        position: relative;
        grid-row: 1 / 2;
    }

    .chat {
        position: absolute;
        min-height: 100%;
        display: flex;
        align-items: flex-end;
        flex-wrap: wrap;
        align-content: flex-end;
        width: 100%;
    }

    .chat-wrapper {
        display: grid;
        grid-template-rows: 1fr auto;
        height: 100%;
    }

    .chat-base {
        grid-row: 2 / 3;
        margin-top: 20px;
    }
</style>