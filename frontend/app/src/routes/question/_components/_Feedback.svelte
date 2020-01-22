<script>
  
  import { postData, getResponses } from "api.js";

  import question from "../../../stores/question";
  import questions from "../../../stores/questions";
  import index from "../../../stores/index";
    

$: selected = $question.answer && $question.answer.selected_answer;

let data = init();
let feedback_index = {}
let feedback;

export async function init() {
    data = await getResponses([$question._id])
    for(var key in data[0]) {
        feedback_index[key] = 0
    }
}

let showCorrect = false;
let showFeedback = false;
let correct_ans = false;

function handleClick() {
    let correct = selected === $question.question_answer

    if (feedback_index[selected] >= data[0][selected].length) {
        feedback_index[selected] = data[0][selected].length - 1
        feedback = data[0][selected][feedback_index[selected]];

    } else {
        feedback = data[0][selected][feedback_index[selected]];
        feedback_index[selected]++
    }
    showFeedback = true
    showCorrect = true

    correct_ans = correct

    if ($questions[$index].answer.tries) {
        $questions[$index].answer.tries++;
    } else {
        $questions[$index].answer.tries = 1
    }    
}
</script>

<style>
    .correct {
        color: green;
    }

    span {
        color: red;
    }
</style>


{#await data}
    loading...
{:then}
    <button on:click={handleClick}> Go </button>
    {#if showCorrect}
        <h2>
            <span class:correct={correct_ans}>
                {correct_ans ? '✔' : '✖'}
            </span>
        </h2>
    {/if}
    {#if showFeedback}
        {feedback}
    {/if}
{/await}
