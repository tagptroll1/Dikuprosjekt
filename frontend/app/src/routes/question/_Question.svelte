<script>
  import question from "../../stores/question";

  import Dropdown from "./_Dropdown.svelte";
  import MultiChoice from "./_MultiChoice.svelte";
  import FillIn from "./_FillIn.svelte";
</script>

{#if $question.type === 'dropdown'}
  <Dropdown />
{:else if $question.type === 'multichoice'}
  <MultiChoice />
{:else if $question.type === 'fillin'}
  <FillIn />
{/if}
