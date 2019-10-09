<script>
  export let segment;
  import { goto } from "@sapper/app";
  import { onMount, onDestroy } from "svelte";

  // Stores
  import user from "../../stores/user";
  import index from "../../stores/index";
  import question from "../../stores/question";
  import questions from "../../stores/questions";

  // Components
  import ProgressBar from "./_components/_ProgressBar.svelte";


  let areYouSure = false;
  let interval;
  
  onMount(() => {
    interval = setInterval(() => {
      if ($question.timeSpent === undefined) {
        $questions[$index].timeSpent = 0;
      } else {
        $questions[$index].timeSpent++;
      }
    }, 1000);
  });

  onDestroy(() => {
    if (interval) {
      clearInterval(interval);
    }
  });

  let unanswered_index;

  function ensureAnswer() {
    if (!$question.answer) {
      $questions[$index].answer = {
        user: $user,
        question_id: $question._id,
        selected_answer: "No answer",
        correct: false,
        ended_question: new Date(Date.now()).toString()
      };
    }
  }

  function next() {
    ensureAnswer();
    if ($index < $questions.length) $index++;
  }

  function prev() {
    ensureAnswer();
    if ($index > 0) $index--;
  }

  function submit(e, force = false) {
    ensureAnswer();
    const unanswered = $questions.some(
      q => q.answer == undefined || q.answer.selected_answer === "No answer"
    );
    if (unanswered && !force) {
      unanswered_index = [];

      $questions.forEach((q, i) => {
        if (q.answer.selected_answer === "No answer")
          unanswered_index.push(i + 1);
      });
      areYouSure = true;
    } else {
      goto("/results");
    }
  }
</script>

<style>
  article {
    position: relative;
    display: flex;
    flex-direction: column;
  }

  article > div {
    display: none;
  }

  article .show {
    display: flex;

    position: absolute;
    margin: 0 auto;
    padding: 10px 20px;

    background-color: rgb(217, 255, 247);
    box-shadow: 0 0 3px -2px black;
    text-align: center;

    align-items: center;
    justify-content: center;
    flex-direction: column;
  }

  #pbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
  }

  .q{
    max-width: 800px;
  }
</style>

<section>
  <div id="pbar">
    <ProgressBar len={$questions.length} />
  </div>
</section>
<article>
  <div class:show={areYouSure}>
    <p>Are you sure you wish to submit you answers and view the results?</p>
    <p>
      You have unanswered questions. Index: {unanswered_index && unanswered_index.toString()}
    </p>
    <div>
      <button on:click={() => (areYouSure = false)}>Go back</button>
      <button on:click={e => submit(e, true)}>Submit!</button>
    </div>
  </div>
  <section class="q">
    <slot />
  </section>
</article>
<section>
  <!-- Buttons -->
  {#if $index > 0}
    <button id="prev" on:click={prev}>Forrige</button>
  {/if}
  {#if $index != $questions.length - 1}
    <button id="next" on:click={next}>Next</button>
  {:else}
    <button id="end" on:click={submit}>Finish quiz</button>
  {/if}
</section>
