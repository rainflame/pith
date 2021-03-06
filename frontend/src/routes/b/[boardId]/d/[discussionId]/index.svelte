<script context="module">
  export async function preload({ params }) {
    return { bId: params.boardId, id: params.discussionId };
  }
</script>

<script>
  import { goto } from "@sapper/app";
  import { onMount } from "svelte";

  import { discussionStore } from "../../../../../stores/discussionStore";
  import { boardStore } from "../../../../../stores/boardStore";

  import DiscussionPageLayout from "../../../../../components/layouts/DiscussionPageLayout.svelte";
  import SectionLayout from "../../../../../components/layouts/SectionLayout.svelte";

  import CanvasBoard from "../../../../../components/sections/CanvasBoard.svelte";
  import Chat from "../../../../../components/sections/Chat.svelte";

  import BoardUnit from "../../../../../components/unit/BoardUnit.svelte";
  import ChatUnit from "../../../../../components/unit/ChatUnit.svelte";

  export let id;
  export let bId;

  let boardMaximized = false;

  onMount(async () => {
    if ($boardStore.userId === null) {
      // if the user hasn't joined or loaded the board yet, redirect them up to do that
      goto(`/b/${bId}/?d=${id}`);
    } else {
      await discussionStore.joinDiscussion(bId, id, $boardStore.userId);
      discussionStore.subscribeDiscussion();
    }
  });

  const onLeave = () => {
    discussionStore.leaveDiscussion(bId, id, $boardStore.userId);
    goto(`/b/${bId}/`);
  };

  const onBoardSizeToggle = () => {
    boardMaximized = !boardMaximized;
  };
</script>

<DiscussionPageLayout {boardMaximized}>
  <div class="section" slot="chat">
    <SectionLayout sectionName="Chat">
      <div slot="header" class="header chat-controls">
        <details>
          <summary>{$discussionStore.participants.length} here now</summary>
          {#each $discussionStore.participants as participant (participant.id)}
            <div><strong>{participant.nickname}</strong></div>
          {/each}
        </details>
        <button on:click={onLeave} class="inline-button"
          >Leave discussion</button
        >
      </div>
      <Chat {id} />
    </SectionLayout>
  </div>

  <div class="section" slot="pinned">
    <SectionLayout sectionName="Summary">
      {#if $discussionStore.pinned.length === 0}
        <p>Pin a message from the chat to start your discussion's summary.</p>
      {/if}
      {#each $discussionStore.pinned as unitId}
        <ChatUnit {...$discussionStore.units[unitId]} unpin />
      {/each}
    </SectionLayout>
  </div>

  <div class="section" slot="focus">
    <SectionLayout sectionName="Focusing on">
      {#if $discussionStore.focused.length === 0}
        <p>Select a unit from the board to focus your discussion.</p>
      {/if}
      {#each $discussionStore.focused as unitId}
        <BoardUnit
          truncate
          unit={$boardStore.units[unitId]}
          unfocus
          edit={false}
          remove={false}
        />
      {/each}
    </SectionLayout>
  </div>

  <div class="section" slot="board">
    <SectionLayout sectionName="Board">
      <div slot="header" class="header board-controls">
        <button on:click={onBoardSizeToggle} class="inline-button"
          >{boardMaximized ? "Minimize Board" : "Maximize Board"}</button
        >
      </div>
      <CanvasBoard />
    </SectionLayout>
  </div>
</DiscussionPageLayout>

<style>
  .section {
    height: 100%;
    width: 100%;
  }

  .header {
    display: flex;
    margin-left: 15px;

    width: 100%;
  }

  .chat-controls {
    align-items: flex-start;
    justify-content: space-between;
  }

  details > div {
    margin-left: 15px;
  }
</style>
