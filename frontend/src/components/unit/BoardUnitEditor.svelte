<script>
  import { boardStore } from "../../stores/boardStore";

  import { boardDisplayContextStore } from "../../stores/boardDisplayContextStore";

  import UnitEditor from "../inputs/UnitEditor.svelte";
  import BoardUnit from "./BoardUnit.svelte";

  export let onSubmit = () => {};
  export let onCancel = () => {};
  export let noBorder = false;
  export let content;

  const onSearch = (query) => {
    boardStore.search($boardStore.boardId, query);
  };
</script>

<UnitEditor
  {onSubmit}
  {onSearch}
  {onCancel}
  {noBorder}
  {content}
  submitOnClickOff
  noResults={$boardStore.searchResults.length === 0}
  placeholder="type a pith..."
>
  <div slot="search-results" let:onSelectResult>
    {#each $boardStore.searchResults as resultId (resultId)}
      {#if resultId !== $boardDisplayContextStore.focused}
        <BoardUnit
          noControls
          unit={$boardStore.units[resultId]}
          onClick={() => onSelectResult(resultId)}
        />
      {/if}
    {/each}
  </div>
</UnitEditor>
