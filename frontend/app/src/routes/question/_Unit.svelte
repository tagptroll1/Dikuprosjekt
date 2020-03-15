<script>
  import questions from "../../stores/questions";
  import question from "../../stores/question";
  import user from "../../stores/user";
  import index from "../../stores/index";
  import { onMount, onDestroy } from "svelte";
  import QuestionText from "./_components/_QuestionText.svelte";

  let studentAns = []
  let ans = []
  
  let mustReturn = false;
  let ran = false;
  let allCorrect = false;
  let showSolution = false;
  let showHint = false;
  let codeSignature;

  if ($question.type === "unittest") {
      codeSignature =$question.question_answer_code.split(":")[0]+":" + "\n"
  }

  function handleClick() {
    if (!editor.getValue().includes("return")) {
      mustReturn = true;
      return;
    } else {
      mustReturn = false;
      const dataset = {
        code: editor.getValue(),
        tests: $questions[$index].question_testcases,
        answer_code: $questions[$index].question_answer_code,
        function_name: $questions[$index].function_name
      };

      fetch("api/coderunner", {
        body: JSON.stringify(dataset),
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(data => data.json())
        .then(data => {
          ran = true;
          studentAns = data.student_ans;
          ans = data.ans;
          allCorrect = data.all_same;

          console.log(data)

          const tries = ($questions[$index].answer ? $questions[$index].answer.tries + 1 : 0)
          const num_correct = ans.filter(element => studentAns.includes(element)).length;

          $questions[$index].answer = {
            user: $user,
            question_id: $question._id,
            selected_answer: editor.getValue(),
            correct: allCorrect,
            show_solution: showSolution,
            tries: tries,
            num_tests: $questions[$index].question_testcases.length,
            num_correct: num_correct
          };
        });
    }
  }
</script>

<style>
  table {
  border-collapse: collapse;
  margin-bottom: 50px;
}

  #container {
    display: flex;
    justify-content: space-around;
  }

  #feedback {
    width:30%;
    padding-left: 50px;
  }

   td {
    border: 1px solid black;
    padding: 5px;
  }
</style>


<QuestionText />

<div id="container">


<div id="editor">{codeSignature}

     
</div>

  <style type="text/css" media="screen">
    #editor {
      position: relative;
      width: 70%;
      height: 300px;
    }
  </style>

  {#if $question.type === "unittest"}
  <div id="feedback">
    {#if mustReturn}
      <span>Your code must return a value</span>
    {/if}     

     <table>
        {#if ran}
        <th colspan="0"> 
            Expected
        </th>
        <th colspan="1">
          Run
        </th>
      {#each ans as a, i}
        <tr>
          <td>
            {#if $question.question_testcases[0].length === 1}
              <span> {$question.function_name}({$question.question_testcases[i][0]}) &#8594; {a}</span>
            {:else if $question.question_testcases[0].length === 2}
              <span> {$question.function_name}({$question.question_testcases[i][0]}, {$question.question_testcases[i][1]}) &#8594; {a}</span>
            {:else}
              <span> {$question.function_name}({$question.question_testcases[i][0]}, {$question.question_testcases[i][1]}, {$question.question_testcases[i][2]}) &#8594; {a}</span>
            {/if}
          </td>
          <td style="width: 20px;">
            <span> {studentAns[i]} </span> 
          </td>
          <td>
            <span>{#if studentAns[i] === a} OK {:else} X {/if}</span>
          </td>
         {#if studentAns[i] === a}
            <td style="background-color: green; width: 20px;"></td> 
          {:else}
            <td style="background-color: red; width: 20px"></td> 
          {/if}
        </tr>
     {/each}
             
             {/if}
 
     </table>
     
     {#if allCorrect}
        <h2>All Correct</h2>
      {/if}
      {#if showSolution}
        <span>{$questions[$index].question_answer_code}</span>
      {/if}
  </div>
  <script>
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/python");
  </script>

</div>
<button on:click={() => handleClick()}>Run</button>

{#if ran}
  <button on:click={() => showSolution = true}>Show solution</button>
{/if}

