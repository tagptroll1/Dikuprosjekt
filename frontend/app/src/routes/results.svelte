<script>
  import { onMount } from "svelte";
  import { fly } from "svelte/transition";
  import { goto } from "@sapper/app";
  import { postData, getResponses, updateUserData, getFeedback } from "api.js";

  import questions from "../stores/questions";
  import { startDate } from "../stores/dates";
  import user from "../stores/user";
  import userdata from "../stores/userdata";
  import selectedChapter from "../stores/selectedChapter";
  import selectedDifficulty from "../stores/selectedDifficulty";

  import Codeblock from "./question/_components/_Codeblock.svelte";

  let any_answers = $questions.some(
    q => q.answer.selected_answer !== "No answer"
  );

  if (!any_answers && process.browser) {
    alert("Ingen spørsmål ble besvart, dermed finnes det ingen feedback.");
    goto("/dashboard");
  }

  function formatUserData(data) {
    let body = {};
    body["old"] = {};
    body["old"]["_id"] = data["_id"];
    body["new"] = {};
    body["new"]["results"] = data["results"];
    return body;
  }

  let totalCorrect = 0;
  let datapack = init();

  async function init() {
    totalCorrect = 0;
    const ids = []; //Question IDs of all questions in this quiz.
    const return_value = []; //Return value of the init() function.

    //General dataset for this particular user.
    const dataset = {
      start_time: $startDate,
      end_time: new Date(Date.now()),
      user: $user,
      selected_chapter: $selectedChapter,
      selected_difficulty: $selectedDifficulty,
      questions: []
    };


    $questions.forEach(q => {
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
      if (q.answer.correct) totalCorrect++;
    });


    //await postData(dataset);
    //Posting of dataset doesn't work and needs to happen somewhere else than feedback retrieval for some reason.

    let feedbacks = await getFeedback();
    $questions.forEach((q, i) => {
      let question_feedback = feedbacks.find(f => f.question_id === q._id) || { feedbacks: "No feedback." }
      let feedback = question_feedback.feedbacks[q.answer.selected_answer];

      return_value.push({
        ...q,
        show: true,
        feedback
      });
    });

    return return_value;
  }

  async function saveAndQuit() {
    let chapterKey = `chapter${$selectedChapter}`;

    if (!($user == "anon" || $user == "")) {
      try {
        if (!(chapterKey in $userdata["results"])) {
          $userdata["results"][chapterKey] = {};
        }

        $userdata["results"][chapterKey][`difficulty${$selectedDifficulty}`] = [
          totalCorrect,
          $questions.length
        ];
        let formattedUserData = await formatUserData($userdata);

        await updateUserData(formattedUserData);
      } catch (err) {
        console.log(err);
      }
    }
    goto("/dashboard");
  }
</script>

<style>
  .false {
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
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
  }

  ol {
    margin: 0;
    padding: 0;
    list-style: none;
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
    font-size: 100%;
  }
</style>

<h1>Resultater</h1>
<p>Antall riktige svar {totalCorrect}/{$questions.length}</p>
<button on:click={saveAndQuit}>Tilbake til dashbord</button>
{#await datapack}
  laster inn..
{:then resp}
  <ol>
    {#each resp as quest, i}
      <li>
        <h2>
          <span class={quest.answer.correct ? 'correct' : 'false'}>
            {quest.answer.correct ? '✔' : '✖'}
          </span>
          Spørsmål {i + 1}
          <span id="carrot" on:click={() => (quest.show ^= 1)}>{quest.show ? '▲' : '▼'}</span>
        </h2>
        {#if quest.show}
          <section
            out:fly={{ y: -100, duration: 100 }}
            in:fly={{ y: -100, duration: 500 }}>
            <p>{quest.question_text}</p>
            {#if quest.type === 'unittest'}
              <p>
                Your code:
                <Codeblock code={quest.answer.selected_answer || 'Nothing'} />
              </p>
              <p>
                You got
                <code>
                  {quest.answer.selected_answer || 'Nothing'}{quest.answer.num_correct}
                </code>
                out of
                <code>
                  {quest.answer.selected_answer || 'Nothing'}{quest.answer.num_tests}
                </code>
              </p>
              {#if quest.answer.correct}
                <h3>That is everything correct! Good work</h3>
              {/if}
            {:else}
              <Codeblock code={quest.question_code.replace('@@', '[ ]')} />
              <p>
                Ditt svar:
                <code>{quest.answer.selected_answer || 'Nothing'}</code>

              </p>
              {#if !quest.answer.correct}
                <p>
                  Fasit:
                  <code>{quest.question_answer}</code>
                </p>
              {/if}
                <p><b>Tilbakemelding:</b> {quest.feedback}</p>

            {/if}
          </section>
        {/if}
      </li>
    {/each}
  </ol>
{:catch err}
  {err}
{/await}
