<script>
  import hljs from "highlight.js/lib/highlight";
  import python from "highlight.js/lib/languages/python";
  hljs.registerLanguage("python", python);

  export let code = undefined;
  $: highlighted = hljs.highlight("python", code);
</script>

{#if highlighted.value}
  <pre>
    <code>
      {@html highlighted.value}
    </code>
  </pre>
{/if}
