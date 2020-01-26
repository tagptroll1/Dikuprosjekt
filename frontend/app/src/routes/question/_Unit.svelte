
<script>

  import questions from "../../stores/questions";
  import question from "../../stores/question";
  import user from "../../stores/user";
  import index from "../../stores/index";
  import { onMount, onDestroy } from "svelte";
  import QuestionText from "./_components/_QuestionText.svelte";
  
  import { runCode } from "../api/coderunner"

  let feedback_text = ""
  let ans_text = ""
  let ans = ""

  function handleClick() {
      if (!editor.getValue().includes("return")) {
        feedback_text = "Your code must return something"
        return 
      } else {
      const dataset = {
        end_time: new Date(Date.now()),
        code: editor.getValue(),
        unit_tests: $questions[$index].unit_test
      };
      runCode(dataset).then((data) => {
        feedback_text = data["fd"]
        ans = data["ans"]
        if (data["ans"] != "None") {
          ans_text = "Koden din evaluerte til: " + ans
        }
        const correct = ans === $question.question_answer;

        $questions[$index].answer = {
          user: $user,
          question_id: $question._id,
          selected_answer: ans,
          correct: correct,
          ended_question: new Date(Date.now()).toString()
        };
      })
      }
  }
  
</script>

<QuestionText />
 
<div id="editor"> def my_function():
    # Skriv koden din her
</div>

  <div>
    <style type="text/css" media="screen">
          #editor {
              position: relative;
              width: 100%;
              height: 90%;
          }
      </style>
  
<button on:click={() => handleClick()}>Run</button>

<div id="feedback">
  <p> {ans_text} </p>
  <p>{feedback_text} </p>
</div>
    <script>
          var editor = ace.edit("editor");
          editor.setTheme("ace/theme/monokai");
          editor.session.setMode("ace/mode/python");
    </script>
  </div>
