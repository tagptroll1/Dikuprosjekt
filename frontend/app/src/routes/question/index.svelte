<script>
  import { goto } from "@sapper/app";
  import { onMount, onDestroy } from "svelte";
  import Question from "./_Question.svelte";
  import questions from "../../stores/questions";
  import { startDate } from "../../stores/dates";
  import { startTime } from "../../stores/dates";

  import selectedChapter from "../../stores/selectedChapter";
  import selectedDifficulty from "../../stores/selectedDifficulty";
  import newQuestionSet from "../../stores/newQuestionSet";

  let promise;

  if ($newQuestionSet == true) {
    promise = getQuestions($selectedChapter, $selectedDifficulty);
  }

  async function getQuestions(chapter, diff) {
    let count = 0;
    while ($questions.length <= 0 && process.browser && count < 10) {
      try {
        const resp = await fetch(
          `api/questions/?difficulty=${diff}&tags=chapter${chapter}`
        );
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
    $newQuestionSet = false;
  }
  $startDate = new Date(Date.now());
  $startTime = new Date().getTime() / 1000;

  function goToDash() {
    goto("../dashboard");
  }
</script>

<style>
  p {
    color: tomato;
  }
</style>

{#if $selectedChapter == 0}
  <button style="display:none" on:click|once={goToDash()} />
{:else}
  {#await promise}
    Loading...
  {:then result}

    <Question />
  {:catch err}
    <p>Something went wrong :(</p>
  {/await}
{/if}
