<script>

  import questions from "../../stores/questions";
  import { onMount } from "svelte";

    
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

  function handleClick() {
      const dataset = {
        end_time: new Date(Date.now()),
        code: editor.getValue(),
        unit_tests: "Her skal det være en lille test"
      };
      postCode(dataset).then((data) => {
        feedback_text = data["fd"]
      })
  }
  
</script>


<body>
<div id="editor"> def main():
    return sum(range(1,100))
</div>

<div id="button">
  <button
        on:click={() => handleClick()}>
        Go
  </button>
</div>

<div id="feedback">
  {feedback_text} 
</div> 
  <div>
    <style type="text/css" media="screen">
          #editor {
              position: absolute;
              top: 100px;
              right: 100px;
              bottom: 100px;
              left: 100px;
              width: 50%;
              height: 50%;
              align-content: center;
          }
          #button {
            position: absolute;
          }
          #feedback {
            position: absolute;
            border: 5px;
            right: 300px;
          }
      </style>
    <script src="https://pagecdn.io/lib/ace/1.4.6/ace.js" type="text/javascript" charset="utf-8"></script>
    
    <script>
          var editor = ace.edit("editor");
          editor.setTheme("ace/theme/monokai");
          editor.session.setMode("ace/mode/python");
          editor.resize()
    </script>
  </div>
</body>
