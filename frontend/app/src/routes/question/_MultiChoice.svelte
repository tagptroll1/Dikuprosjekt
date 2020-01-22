<script>
  import MultipleChoiceAlternatives from "./_components/_MultipleChoiceAlternatives.svelte";
  import QuestionText from "./_components/_QuestionText.svelte";
  import Codeblock from "./_components/_Codeblock.svelte";
  import Feedback from "./_components/_Feedback.svelte";

  import question from "../../stores/question";
    
</script>

<QuestionText />
<Codeblock code={$question.question_code} />
<MultipleChoiceAlternatives />
<Feedback />
