<script>
  import questions from "../../../stores/questions";
  import question from "../../../stores/question";
  import index from "../../../stores/index";
  import user from "../../../stores/user";
  import hljs from "highlight.js/lib/highlight";
  import python from "highlight.js/lib/languages/python";
  import { afterUpdate, onMount } from "svelte";

  //$: selected = $question.answer && $question.answer.selected_answer;


  let selected;
  hljs.registerLanguage("python", python);

  let prev_id;
  let piece1 = "";
  let piece2 = "";

  let pieces;

  if ($question.type === "dropdown") {
     pieces = $question.question_code.split("@@");
  }


  let tries;

  if ($questions[$index].answer) {
        tries = $questions[$index].answer.tries + 1
    } else {
        tries = 1
  }
  
  function disp() {
    const correct = selected == $question.question_answer
    $questions[$index].answer = {
      user: $user,
      question_id: $question._id,
      selected_answer: selected,
      correct: correct,
      ended_question: new Date(Date.now()).toString(),
      tries: tries
    };
    
  }

  onMount(() => {
    if (prev_id !== $question._id && !$question.answer) {
      selected = '';
    }
    
    piece1 = hljs.highlight("python", pieces[0]);
    piece2 = hljs.highlight("python", pieces[1]);
    prev_id = $question._id;

  });
</script>

<pre>
  <code>
    {@html piece1.value} <select bind:value={selected} on:change={disp}>
      <option value="" />
      {#if $question.type === "dropdown"}
      {#each $question.alternatives as item}
        <option value={item}>{item}</option>
      {/each}
      {/if}
    </select> {@html piece2.value || ''}
  </code>
</pre>
