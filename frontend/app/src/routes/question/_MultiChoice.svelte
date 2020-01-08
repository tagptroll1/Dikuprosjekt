<script>
  import MultipleChoiceAlternatives from "./_components/_MultipleChoiceAlternatives.svelte";
  import QuestionText from "./_components/_QuestionText.svelte";
  import Codeblock from "./_components/_Codeblock.svelte";

  //import Feedback, { getFeedback } from "./_components/_Feedback.svelte";

  import question from "../../stores/question";
    
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

let t = getResponse($question._id)
console.log(t)
let feedback_text = ""
export function getFeedback(id) {
    getResponse(id).then((data) => {
        feedback_text = data["feedback"]
        return data
    })
     return feedback_text
}


let promise = getFeedback($question._id)

console.log(feedback_text)
console.log(promise)

</script>

<QuestionText />
<Codeblock code={$question.question_code} />
<MultipleChoiceAlternatives />
