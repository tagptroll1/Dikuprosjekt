<script>
  import MultipleChoiceAlternatives from "./_components/_MultipleChoiceAlternatives.svelte";
  import QuestionText from "./_components/_QuestionText.svelte";
  import Codeblock from "./_components/_Codeblock.svelte";

  //import Feedback, { getFeedback } from "./_components/_Feedback.svelte";

  import question from "../../stores/question";
  import questions from "../../stores/questions";
  import index from "../../stores/index";
  import user from "../../stores/user";
    

  async function getResponse(id) {
    try {
        const resp = await fetch(`http://127.0.0.1:5000/api/v1/feedback/${id}`, {
            method: "GET",
            headers: { "Content-Type": "application/json",
            "Authorization": "token a204bbe9-c5fe-4239-b4c8-5e79a6e28a20"},
        });
        return await resp.json();
    } catch (err) {
        console.error(err);
        return [];
    }    
}   

$: selected = $question.answer && $question.answer.selected_answer;

let show_correct = false

let promise = getResponse($question._id)
let showFeedback = false
let feedback_idx = 0

let correct = false

let correct_ans = false

let tries = 0

async function handleClick() {
    tries++;

    correct = selected === $question.question_answer

    show_correct = true

    if (correct) {
        correct_ans = true

        $questions[$index].answer = {
        user : $user,
        question_id: $question._id,
        selected_answer: selected,
        correct: correct,
        ended_question: new Date(Date.now()).toString(),
        tries : tries
        };
    }

    feedback_idx++;
    showFeedback = true
    promise = await getResponse($question._id);
    if (feedback_idx >= promise.feedback.length) {
        feedback_idx = promise.feedback.length;
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

<QuestionText />
<Codeblock code={$question.question_code} />
<MultipleChoiceAlternatives />


<button on:click={handleClick}> Go </button>

{#if show_correct}
    <h2>
        <span class:correct={correct_ans}>
            {correct_ans ? '✔' : '✖'}
        </span>
    </h2>
{/if}

{#if showFeedback}
    {#await promise}
        <p>...waiting</p>
    {:then feedback}
        <p>{feedback.feedback[feedback_idx - 1]}</p>
    {:catch error}
        <p style="color: red">No feedback for this question</p>
    {/await}
{/if}