<script>
  import { onMount } from "svelte";
  import { fly } from "svelte/transition";
  import { goto } from "@sapper/app";
  import { postData, getResponses } from "api.js";

  import questions from "../stores/questions";
  import { startDate } from "../stores/dates";
  import user from "../stores/user";

  import Codeblock from "./question/_components/_Codeblock.svelte";

  let any_answers = $questions.some(
    q => q.answer.selected_answer !== "No answer"
  );

  if (!any_answers && process.browser) {
    alert("No questions were answered, so nothing to show");
    goto("/");
  }

  let totalCorrect = 0;
  let datapack = init();

  async function init() {
    totalCorrect = 0;

    const dataset = {
      start_time: $startDate,
      end_time: new Date(Date.now()),
      user: $user,
      questions: []
    };

    const ids = [];
    const return_value = [];

    $questions.forEach(q => {
      ids.push(q._id);
      dataset.questions.push({
        question_id: q._id,
        selected_answer: q.answer.selected_answer,
        correct: q.answer.correct,
        time_spent: q.timeSpent
      });
      if (q.answer.correct) totalCorrect++;
    });

    await postData(dataset);
    let feedbacks = await getResponses(ids);

    $questions.forEach((q, i) => {
      const feedback_set = feedbacks.find(f => f.question_id === q._id) || {};
      let feedback = feedback_set[q.answer.selected_answer];

      return_value.push({
        ...q,
        show: true,
        feedback
      });
    });

    return return_value;
  }
</script>

<style>
  span {
    color: red;
  }
  .correct {
    color: green;
  }

  h2 {
    position: relative;
    z-index: 5;
    margin: 0;
    padding: 0;
    background-color: inherit;
  }

  li {
    position: relative;

    background-color: white;
    padding: 20px;
    margin: 20px;
    max-width: 90%;
  }

  ol {
    margin: 0;
    padding: 0;
    list-style: none;
    background-color: lightgrey;
    width: 60%;
  }

  code {
    background-color: burlywood;
  }

  #carrot {
    position: absolute;
    right: 10px;
    font-size: 0.8em;
  }

  button {
    margin: 10px;
    padding: 10px;
  }
</style>

<h1>Question results</h1>
<p>Total correct answers {totalCorrect}/{$questions.length}</p>
<button on:click={() => goto('/')}>Try again</button>
{#await datapack}
  loading..
{:then resp}
  <ol>
    {#each resp as quest, i}
      <li on:click={() => (quest.show ^= 1)}>
        <h2>
          <span class:correct={quest.answer.correct}>
            {quest.answer.correct ? '✔' : '✖'}
          </span>
          Question {i + 1}
          <span id="carrot">{quest.show ? '⏫' : '⏬'}</span>
        </h2>
        {#if quest.show}
          <section
            out:fly={{ y: -100, duration: 100 }}
            in:fly={{ y: -100, duration: 500 }}>
            <p>{quest.question_text}</p>
            <Codeblock code={quest.question_code.replace('@@', '[ ]')} />

            <p>
              You selected:
              <code>{quest.answer.selected_answer || 'Nothing'}</code>

            </p>
            {#if !quest.answer.correct}
              <p>
                Correct answer was
                <code>{quest.question_answer}</code>
              </p>
            {/if}
            {#if quest.feedback}
              <p>{quest.feedback}</p>
            {/if}
          </section>
        {/if}
      </li>
    {/each}
  </ol>
{:catch err}
  {err}
{/await}
