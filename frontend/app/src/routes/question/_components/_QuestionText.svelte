<script>
  import question from "../../../stores/question";

  function parseText(txt) {
    while (txt.search("\n") !== -1) {
      txt = txt.replace("\n", "<br/>");
    }

    let count = (txt.match(/`/g) || []).length;
    if (count >= 2 && count % 2 === 0) {
      while (txt.search("`") !== -1 && count % 2 === 0) {
        txt = txt.replace(
          "`",
          "<code style='background-color: var(--bg-aside)'>"
        );
        txt = txt.replace("`", "</code>");
        count = (txt.match(/`/g) || []).length;
      }
    }
    return txt;
  }

  $: text = parseText($question.question_text);
</script>

<p>
  {@html text}
</p>
