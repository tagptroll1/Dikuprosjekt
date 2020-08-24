<script>
  import { goto } from "@sapper/app";
  export let chapterNumber;
  import selectedChapter from "../../../stores/selectedChapter";

  function start() {
    $selectedChapter = chapterNumber;
    goto("../dashboard/difficulty");
  }
</script>

<style>
  .startQuizButton {
    border: none;
    cursor: pointer;
    padding: 5px 12px;
    margin: 5px;
    border: 2px solid #5988bb;
    background-color: #5988bb;
    border-radius: 8px 4px;
    position: relative;
    font-size: 1em;
    transition: opacity 0.2s;
    outline: none;
  }

  .startQuizButton:not(:disabled)::after {
    content: "";
    display: block;
    position: absolute;
    left: 0;
    right: 0;
    margin: 0 auto;
    width: 0;
    height: 3px;
    border-radius: 50px;
    background-color: var(--bg-main);

    transition: width 0.1s ease;
  }

  .startQuizButton:focus::after,
  .startQuizButton:hover::after {
    width: calc(100% - 12px);
  }

  @media (max-width: 700px) {
    .startQuizButton {
      margin: 20px;
    }
  }
</style>

<main>
  <button class="startQuizButton" on:click={start}>Start</button>
</main>
