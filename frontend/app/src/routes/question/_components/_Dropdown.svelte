<script>
  import questions from "../../../stores/questions";
  import question from "../../../stores/question";
  import index from "../../../stores/index";
  import user from "../../../stores/user";
  import hljs from "highlight.js/lib/highlight";
  import python from "highlight.js/lib/languages/python";
  import { beforeUpdate } from "svelte";

  $: selected = $question.answer && $question.answer.selected_answer;

  hljs.registerLanguage("python", python);

  let prev_id;
  let piece1 = "";
  let piece2 = "";
  $: pieces = $question.question_code.split("@@");

  function disp() {
    const correct = selected == $question.question_answer
    $questions[$index].answer = {
      user: $user,
      question_id: $question._id,
      selected_answer: selected,
      correct: correct,
      ended_question: new Date(Date.now()).toString()
    };
  }

  beforeUpdate(() => {
    if (prev_id !== $question._id && !$question.answer) {
      selected = null;
    }

    piece1 = hljs.highlight("python", pieces[0]);
    piece2 = hljs.highlight("python", pieces[1]);
    prev_id = $question._id;

  });
</script>

<style>
  code {
    display: block;
    border-radius: 8px 4px;
    background-color: var(--bg-aside);
  }
</style>

<pre>
  <code>
    {@html piece1.value} <select bind:value={selected} on:change={disp}>
      <option value="" />
      {#each $question.alternatives as item}
        <option value={item}>{item}</option>
      {/each}
    </select> {@html piece2.value || ''}
  </code>
</pre>
