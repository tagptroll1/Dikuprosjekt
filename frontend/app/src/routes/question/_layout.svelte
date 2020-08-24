<script>
  //export let segment;
  import { goto } from "@sapper/app";
  import { onMount, onDestroy } from "svelte";
  import { postData } from "api.js";

  // Stores
  import user from "../../stores/user";
  import index from "../../stores/index";
  import question from "../../stores/question";
  import questions from "../../stores/questions";
  import showFeedback from "../../stores/feedback";

  import selectedChapter from "../../stores/selectedChapter";
  import selectedDifficulty from "../../stores/selectedDifficulty";
  import { startDate } from "../../stores/dates";
  import { startTime } from "../../stores/dates";

  // Components
  import ProgressBar from "./_components/_ProgressBar.svelte";

  //Copied and slightly altered from results.svelte, refactor later
  async function init() {
    const dataset = {
      start_time: $startDate,
      end_time: new Date(Date.now()),
      user: $user,
      selected_chapter: $selectedChapter,
      selected_difficulty: $selectedDifficulty,
      questions: []
    };

    const ids = [];
    const return_value = [];
    ensureAnswer();

    for (let i = 0; i <= $index; i++) {
      let q = $questions[i];

      ids.push(q._id);

      if (q.type == "unittest") {
        dataset.questions.push({
          question_id: q._id,
          selected_answer: q.answer.selected_answer,
          num_tests: q.answer.num_tests,
          num_correct: q.answer.num_correct,
          correct: q.answer.all_correct,
          show_solution: q.answer.show_solution,
          tries: q.answer.tries
        });
      } else {
        dataset.questions.push({
          question_id: q._id,
          selected_answer: q.answer.selected_answer,
          correct: q.answer.correct,
          time_spent: q.answer.time_spent,
          tries: q.answer.tries
        });
      }
    }
    await postData(dataset);

    goto("/dashboard");
  }

  let areYouSure = false;
  let interval;

  onDestroy(() => {
    if (interval) {
      clearInterval(interval);
    }
  });

  let unanswered_index;

  function ensureAnswer() {
    if (!$question.answer) {
      let end_time = new Date().getTime() / 1000;
      $questions[$index].answer = {
        user: $user,
        question_id: $question._id,
        selected_answer: "No answer",
        correct: false,
        ended_question: new Date(Date.now()).toString(),
        tries: 0,
        time_spent: Math.round(end_time - $startTime)
      };
    }
  }

  function submitMidways() {
    let datapack = init();
    console.log(datapack);
  }

  function next() {
    ensureAnswer();
    if ($index < $questions.length) {
      $index++;
      $showFeedback = false;
    }
  }

  function prev() {
    ensureAnswer();
    if ($index > 0) $index--;
    $showFeedback = false;
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
    width: 80%;
  }

  article > div {
    display: none;
  }

  article .show {
    display: flex;

    position: block;
    margin: 0 auto;
    padding: 10px 20px;

    background-color: rgb(217, 255, 247);
    box-shadow: 0 0 3px -2px bla ck;
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

  .q {
    width: 80%;
    margin: 0 auto;
  }

  .prompt {
    margin-top: 30px;
    margin-bottom: 20px;
  }
</style>

<section>
  <div id="pbar">
    <ProgressBar len={$questions.length} />
  </div>
</section>
<article class="prompt">
  <div class:show={areYouSure}>
    <p>Er du sikker på at du vil fullføre denne seksjonen?</p>
    <p>
      Du har ubesvarte spørsmål: {unanswered_index && unanswered_index.toString()}
    </p>
    <div>
      <button on:click={() => (areYouSure = false)}>Gå tilbake!</button>
      <button on:click={e => submit(e, true)}>Fullfør</button>
    </div>
  </div>
  <section class="q">
    <slot />
  </section>
</article>
<section>
  <!-- Buttons -->
  {#if $index < $questions.length - 1}
    <button id="quit" on:click={submitMidways}>Avslutt</button>
  {/if}
  {#if $index > 0}
    <!-- <button id="prev" on:click={prev}>Forrige</button> -->
  {/if}
  {#if $index != $questions.length - 1}
    <button id="next" on:click={next}>Neste</button>
  {:else}
    <button id="end" on:click={submit}>Fullfør quiz</button>
  {/if}
</section>
