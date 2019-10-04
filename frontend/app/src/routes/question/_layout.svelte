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
  button {
    margin: 20px;
    width: 8rem;
  }

  article div {
    display: none;
    width: 50%;
    height: 30%;
    position: fixed;
    top: 45%;
    left: 0;
    right: 0;
    margin: 0 auto;
    z-index: 50;

    background-color: lightgrey;
    box-shadow: 1px 1px 1px 1px black;
    text-align: center;
  }

  article .show {
    display: block;
  }

  #pbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
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
    <button on:click={() => (areYouSure = false)}>Go back</button>
    <button on:click={e => submit(e, true)}>Submit!</button>
  </div>
  <section>
    <slot />
  </section>
</article>
<section>
  <!-- Buttons -->
  {#if $index > 0}
    <button id="prev" on:click={prev}>Forrige</button>
  {/if}
  {#if $index != $questions.length - 1}
    <button id="next" on:click={next}>Neste</button>
  {:else}
    <button id="end" on:click={submit}>Fullfør quiz</button>
  {/if}
</section>
