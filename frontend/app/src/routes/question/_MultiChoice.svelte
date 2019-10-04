<script>
  import MultipleChoiceAlternatives from "./_components/_MultipleChoiceAlternatives.svelte";
  import QuestionText from "./_components/_QuestionText.svelte";
  import Codeblock from "./_components/_Codeblock.svelte";

  import question from "../../stores/question";
</script>

<style>
  h1 {
    font-family: "Roboto", sans-serif;
    font-weight: 300;
    text-align: center;
  }
</style>

<h1>Multiple choice</h1>

<QuestionText />
<Codeblock code={$question.question_code} />
<MultipleChoiceAlternatives />
