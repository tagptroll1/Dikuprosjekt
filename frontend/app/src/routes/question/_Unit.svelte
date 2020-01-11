
<script>

  import questions from "../../stores/questions";
  import index from "../../stores/index";
  import { onMount } from "svelte";
  import QuestionText from "./_components/_QuestionText.svelte";

    
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
  let q_text = $questions[$index].question_text

  function handleClick() {
      const dataset = {
        end_time: new Date(Date.now()),
        code: editor.getValue(),
        unit_tests: $questions[$index].unit_test
      };
      postCode(dataset).then((data) => {
        feedback_text = data["fd"]
        ans = "Koden din evaluerte til: " + data["ans"]
      })
  }
  
</script>


<body>
<div id="text">
{q_text}
</div>

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

<div id="wrapper">
<div id="editor"> def main():
    "Skriv koden din her"
</div>
</div>

  <div>
    <style type="text/css" media="screen">
          #editor {
              position: absolute;
              width: 100%;
              height: 50%;
          }
          #button {
            position: absolute;
          }
          #feedback {
            position: absolute;
            border: 5px;
            right: 250px;
            bottom: 25px;
          } 
          #wrapper {
            position: absolute;
            width : 500px;
            height: 500px;
            right: 100px;
            top: 70px;
          }
          #text { 
            bottom: 50px;
          }
      
      </style>
    <script src="https://pagecdn.io/lib/ace/1.4.6/ace.js" type="text/javascript" charset="utf-8"></script>
    
    <script>
          var editor = ace.edit("editor");
          editor.setTheme("ace/theme/monokai");
          editor.session.setMode("ace/mode/python");
          //editor.resize()
    </script>
  </div>
</body>
