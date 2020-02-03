<script>
  
  import { postData, getResponses } from "api.js";

  import question from "../../../stores/question";
  import questions from "../../../stores/questions";
  import index from "../../../stores/index";
  import showFeedback from "../../../stores/feedback";
    

$: selected = $question.answer && $question.answer.selected_answer && handleClick();
$: data = init() && $question._id

let feedback_index = {}
let feedback;

async function init() {
    data = await getResponses([$question._id])
    for(var key in data[0]) {
        feedback_index[key] = 0
    }
}

let showCorrect = false;
let correct_ans = false;

function handleClick() {
    selected = $question.answer.selected_answer;
    let correct = selected === $question.question_answer
    correct_ans = correct

    console.log($question)
    // No feedback exists for this question, just showing default values
    if (data.length == 0 || data[0][selected] == null) {
        console.log("There is no feedback for this question")
        showCorrect = true
        $showFeedback = true
        if (correct) {
            feedback = "Riktig!"
            return
        } else {
            feedback = "Feil svar!"
            return
        }
    }

    if (feedback_index[selected] >= data[0][selected].length) {
        feedback_index[selected] = data[0][selected].length - 1
        feedback = data[0][selected][feedback_index[selected]];
    } else {
        feedback = data[0][selected][feedback_index[selected]];
        feedback_index[selected]++
    }
    $showFeedback = true
    showCorrect = true

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
    <!-- <button on:click={handleClick}> Go </button> -->
    {#if $showFeedback}
        <span class:correct={correct_ans}>
            {correct_ans ? '✔' : '✖'}
        </span>
        {feedback}
    {/if}
{/await}
