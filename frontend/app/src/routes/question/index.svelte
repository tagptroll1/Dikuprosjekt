<script>
  const type = "questions";

  import Question from "./_Question.svelte";
  import questions from "../../stores/questions";
  import { startDate } from "../../stores/dates";

  let promise = getQuestions();

  async function getQuestions() {
    let count = 0;
    while ($questions.length <= 0 && process.browser && count < 10) {
      try {
        const resp = await fetch("http://localhost/api/questions"); // Change this to get different questions
        if (!resp.ok) {
          continue;
        }

        const json = await resp.json();
        $questions = json;

        if (json.length > 0) {
          return json;
        }
      } catch (err) {
        if (count === 9) {
          throw err;
        }
      }

      count++;
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
