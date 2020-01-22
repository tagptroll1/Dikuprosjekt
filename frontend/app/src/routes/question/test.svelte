<!-- <script>
  import Feedback, { getFeedback } from "./question/_components/_Feedback.svelte";
  
  let promise = getFeedback("5d5998ac583853378350a33d")
</script>

<Feedback />


{#await promise}
  Loading.
{:then result}
  { result }
{:catch err}
  <p>Something went wrong :(</p>
{/await} -->