<script>
  import Question from "./_Question.svelte";
  import questions from "../../stores/questions";
  import { startDate } from "../../stores/dates";

  let promise = getQuestions();

  async function getQuestions() {
    try {
      const resp = await fetch("/api/questions?limit=10"); // Change this to get different questions


      const json = await resp.json();
      $questions = json;

      if (json.length > 0) {
        return json;
      }
    } catch (err) {

    }
  }
  $startDate = new Date(Date.now());
</script>

<style>
  p {
    color: tomato;
  }
</style>

{#await promise}
  Loading.
{:then result}
  <Question />
{:catch err}
  <p>Something went wrong :(</p>
{/await}
