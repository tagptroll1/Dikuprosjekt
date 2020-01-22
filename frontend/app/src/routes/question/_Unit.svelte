
<script>

  import questions from "../../stores/questions";
  import index from "../../stores/index";
  import { onMount } from "svelte";
  import QuestionText from "./_components/_QuestionText.svelte";

  console.log($questions)
    
    async function postCode(data) {
      try {
          const resp = await fetch("http://127.0.0.1:5000/api/v1/coderunner", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
              },
              body: JSON.stringify(data),
          });
          return await resp.json();

      } catch (err) {
          console.log(`Data post failed ${err}`);
      }
    }

  let feedback_text = ""
  let ans = ""

  function handleClick() {
      const dataset = {
        end_time: new Date(Date.now()),
        code: editor.getValue(),
        unit_tests: $questions[$index].unit_test
      };
      postCode(dataset).then((data) => {
        feedback_text = data["fd"]
        if (data["ans"] != "None") {
          ans = "Koden din evaluerte til: " + data["ans"]
        }
      })
  }
  
</script>

<QuestionText />
 
<div id="editor"> def main():
    "Skriv koden din her"
</div>

  <div>
    <style type="text/css" media="screen">
          #editor {
              position: relative;
              width: 100%;
              height: 90%;
          }
      </style>
  
<div id="button">
  <button
        on:click={() => handleClick()}>
        Go
  </button>
</div>

<div id="feedback">
  <p>{ans} </p>
  {feedback_text} 
</div>
    <script>
          var editor = ace.edit("editor");
          editor.setTheme("ace/theme/monokai");
          editor.session.setMode("ace/mode/python");
          editor.resize()
    </script>
  </div>
