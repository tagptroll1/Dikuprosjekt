<script>
  import hljs from "highlight.js/lib/highlight";
  import python from "highlight.js/lib/languages/python";
  hljs.registerLanguage("python", python);

  export let code = undefined;
  $: highlighted = hljs.highlight("python", code);
</script>

<style>
  code {
    display: block;
    border-radius: 8px 4px;
    background-color: var(--bg-aside);
  }
</style>

{#if highlighted.value}
  <pre>
    <code>
      {@html highlighted.value}
    </code>
  </pre>
{/if}
