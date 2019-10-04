<script>
  import questions from "../../../stores/questions";
  import question from "../../../stores/question";
  import index from "../../../stores/index";
  import user from "../../../stores/user";

  $: selected = $question.answer && $question.answer.selected_answer;

  function handleClick(option) {
    selected = option;

    const correct = selected === $question.question_answer;

    $questions[$index].answer = {
      user: $user,
      question_id: $question._id,
      selected_answer: selected,
      correct: correct,
      ended_question: new Date(Date.now()).toString()
    };

    const dispatch_obj = {
      selected: option,
      correct: selected === $question.question_answer
    };
  }
</script>

<style>
  button {
    outline: none;
    font-size: 20px;
    display: inline-block;
    padding: 0.35em 1.2em;
    border: 0.1em solid rgb(0, 0, 0);
    margin: 0 0.3em 0.3em 0;
    border-radius: 0.12em;
    box-sizing: border-box;
    text-decoration: none;
    font-family: "Roboto", sans-serif;
    font-weight: 300;
    color: black;
    text-align: center;
    transition: all 0.15s;
    background-color: transparent;
  }
  button:hover {
    color: #ffffff;
    background-color: black;
  }
  #choices {
    padding: 40px;
  }
  li {
    list-style: none;
  }

  .selected {
    background-color: greenyellow;
  }
</style>

<div id="choices">
  <ul>
    {#each $question.alternatives as alternative}
      <li>
        <button
          class:selected={alternative === selected}
          on:click={() => handleClick(alternative)}>
          {alternative}
        </button>
      </li>
    {/each}
  </ul>
</div>
