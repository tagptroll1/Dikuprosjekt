<script>
    import { goto } from "@sapper/app";
    export let difficulty;
    import selectedDifficulty from "../../../stores/selectedDifficulty";
    import newQuestionSet from "../../../stores/newQuestionSet";

    let difficulties = {
        "Lett": 1,
        "Middels": 2,
        "Vanskelig": 3
    }

    function start() {
        $selectedDifficulty = difficulties[difficulty];
        $newQuestionSet = true;
        goto("../question");
    }
</script>

<main>
    <button class="startQuizButton" on:click={start}>Start</button>
</main>

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
        transition: opacity .2s;
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
</style>