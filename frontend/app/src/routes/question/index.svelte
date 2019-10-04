<script>
  const type = "questions";

  import Question from "./_Question.svelte";
  import questions from "../../stores/questions";
  import {startDate} from "../../stores/dates";

  let promise = getQuestions();

  async function getQuestions() {
    if ($questions.length <= 0 && process.browser) {
      const resp = await fetch(`api/${type}`); // Change this to get different questions
      const json = await resp.json();
      $questions = json;
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
