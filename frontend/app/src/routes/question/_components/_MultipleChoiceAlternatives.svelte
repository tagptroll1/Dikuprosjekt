<script>
  import questions from "../../../stores/questions";
  import question from "../../../stores/question";
  import index from "../../../stores/index";
  import user from "../../../stores/user";
  import { startTime } from "../../../stores/dates";

  $: selected = $question.answer && $question.answer.selected_answer;

  function handleClick(option) {
    let end_time = new Date().getTime() / 1000;
    selected = option;
    const correct = selected === $question.question_answer;

    let tries;

    if ($questions[$index].answer) {
      tries = $questions[$index].answer.tries + 1;
    } else {
      tries = 1;
    }

    $questions[$index].answer = {
      user: $user,
      question_id: $question._id,
      selected_answer: selected,
      correct: correct,
      tries: tries,
      time_spent: Math.round(end_time - $startTime)
    };

    const dispatch_obj = {
      selected: option,
      correct: selected === $question.question_answer
    };
  }
</script>

<style>
  button {
    cursor: pointer;

    outline: none;
    font-size: 1em;

    padding: 5px 10px;
    margin: 10px 0;

    display: block;
    width: 100%;

    box-sizing: border-box;
    text-decoration: none;
    font-family: var(--code);
    font-weight: 300;
    text-align: center;
    transition: all 0.15s;

    color: rgb(221, 221, 221);
    background-color: rgb(47, 47, 47);

    border: none;
  }

  button:hover {
    color: #ffffff;
    background-color: black;
    background-color: rgb(33, 111, 255);
  }

  #choices {
    margin: 40px;
  }

  li {
    list-style: none;
  }

  ul {
    margin: 0;
    padding: 0;
  }

  .selected {
    font-weight: bold;
    border: 2px solid rgb(0, 0, 0);
    background-color: rgb(33, 111, 255);
  }
</style>

<div id="choices">
  <ul>
    {#if $question.type === 'multichoice'}
      {#each $question.alternatives as alternative}
        <li>
          <button
            class:selected={alternative === selected}
            on:click={() => handleClick(alternative)}>
            {alternative}
          </button>
        </li>
      {/each}
    {/if}
  </ul>
</div>
