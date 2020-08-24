<script>
  //Your script goes here.
  import Chapter from "./_components/_Chapter.svelte";
  import Status from "./_components/_Status.svelte";
  import user from "../../stores/user.js";
  import { goto } from "@sapper/app";
  import { postNewUser, getUserData, updateUserData } from "api.js";
  import index from "../../stores/index";
  import userdata from "../../stores/userdata";
  import questions from "../../stores/questions";
  import feedback from "../../stores/feedback";

  let username;
  const unsubscribe = user.subscribe(value => {
    username = value;
  });

  let completePercentage = {};
  if ($user !== "" && $user !== "anon") {
    generatePercentages();
  } else {
    //endre i når flere kapitler legges til
    for (let i = 2; i < 7; i++) {
      completePercentage[`chapter${i}`] = 0;
    }
  }

  //Resets stored variables when visiting dashboard.
  $index = 0;
  $questions = [];
  $feedback = false;

  getNewUserId();

  function tilLogin() {
    //Send's the user to login screen.
    goto("../");
  }

  async function getNewUserId() {
    //Retrieves the users progress unless logged in as anonymous.
    if (!("_id" in $userdata) && !($user === "" || $user === "anon")) {
      $userdata = await getUserData($user);
    }
  }

  function generatePercentages() {
    //Generate a visual percentage of the student's progress.
    for (let i = 2; i < 7; i++) {
      //For each chapter..
      let progress_score = 0;
      if (`chapter${i}` in $userdata["results"]) {
        //..if the user has attempted this chapter before
        for (let j = 1; j <= 3; j++) {
          //.. loop through the different difficulties..
          if (`difficulty${j}` in $userdata["results"][`chapter${i}`]) {
            //..if there is a registered attempt
            //Collect the score from that attempt.
            progress_score +=
              $userdata["results"][`chapter${i}`][`difficulty${j}`][0] /
              $userdata["results"][`chapter${i}`][`difficulty${j}`][1];
          }
        }
      }
      completePercentage[`chapter${i}`] = (progress_score / 3) * 100;
    }
  }

  //Denne funksjonen kan brukes med en knapp for å slette "results" for en bruker
  //Veldig inconsistent behaviour for øyeblikket
  async function resetProgress() {
    try {
      let datapack = {};
      datapack["old"] = {};
      datapack["old"]["_id"] = $userdata["_id"];
      datapack["new"] = {};
      datapack["new"]["results"] = {};

      await updateUserData(datapack);
    } catch (err) {
      console.log(err);
    }
    goto("../");
  }
</script>

<style>
  .myProgress.svelte-c43gvp {
    max-width: 180px;
  }

  button {
    font-size: 100%;
  }

  .status {
    width: 30%;
  }
  .chapter {
    font-size: 85%;
  }
  .infoText {
    max-width: 30vw;
    line-height: 1.6;
  }

  table {
    padding: 15px;
    box-shadow: 0 7px 15px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
    margin-bottom: 60px;
  }

  th,
  td {
    padding: 15px;
    text-align: left;
  }

  .tableRow:hover {
    background-color: #f5f5f5;
  }

  @media (max-width: 1350px) {
    .infoText {
      max-width: 55vw;
      line-height: 1.6;
    }
  }

  @media (max-width: 785px) {
    .infoText {
      max-width: 90vw;
      line-height: 1.6;
    }

    table {
      zoom: 80%;
      padding: 0px;
      font-size: 150%;
      box-shadow: none;
    }
  }

  /*Mobile styling*/
  @media (max-width: 700px) {
    .header {
      text-align: center;
    }

    td {
      width: 200px;
    }

    .chapterHeader {
      display: none;
    }

    .statusHeader {
      text-align: center;
    }

    .loggin {
      margin-left: 15px;
    }

    .chapter {
      display: none;
    }

    table td {
      zoom: 85%;
      padding: 0px;
      margin-bottom: 5px;
      padding-left: 5px;
    }

    table {
      margin-bottom: 30vh;
    }

    th {
      padding-left: 5vw;
    }
  }
</style>

<main>
  <h1 class="header">INFO132 Pensum Quiz</h1>

  <p class="infoText">
    Velkommen til feedback.uib.no! Her får du testet deg selv i ulike temaer fra
    pensum, hensikten er å tilby en form for øving hvor du som student får
    øyeblikkelig feedback. Trykk på 'Start' knappen for å få en oversikt over
    oppgavene som tilhører hvert individuelle kapittel.
  </p>
  <br />
  {#if username === undefined || username == 'anon' || username == ''}
    <p class="loggin">
      Du er ikke logget inn
      <button on:click={tilLogin}>Logg Inn</button>
    </p>
  {:else}
    <p class="loggin">
      Logget inn som
      <b>{username}</b>
    </p>
  {/if}

  <table id="curriculum">
    <tr>

      <th class="tableHeader">Tema</th>
      <th class="tableHeader chapterHeader">Kapittel</th>
      <th class="tableHeader statusHeader">Status</th>
      <th />
    </tr>

    <tr class="tableRow">
      <td>Uttrykk</td>
      <td class="chapter">Kapittel 2</td>
      <td>
        <Status
          barNum={'bar2'}
          percentage={completePercentage[`chapter${2}`]} />
      </td>
      <td>
        <Chapter chapterNumber={2} />
      </td>
    </tr>

    <tr class="tableRow">

      <td>Betinget Utførelse</td>
      <td class="chapter">Kapittel 3</td>
      <td>
        <Status
          barNum={'bar3'}
          percentage={completePercentage[`chapter${3}`]} />
      </td>
      <td>
        <Chapter chapterNumber={3} />
      </td>
    </tr>

    <tr class="tableRow">
      <td>Funksjoner</td>
      <td class="chapter">Kapittel 4</td>
      <td>
        <Status
          barNum={'bar4'}
          percentage={completePercentage[`chapter${4}`]} />
      </td>
      <td>
        <Chapter chapterNumber={4} />
      </td>
    </tr>

    <tr class="tableRow">
      <td>Iterasjon</td>
      <td class="chapter">Kapittel 5</td>
      <td>
        <Status
          barNum={'bar5'}
          percentage={completePercentage[`chapter${5}`]} />
      </td>
      <td>
        <Chapter chapterNumber={5} />
      </td>
    </tr>

    <tr class="tableRow">
      <td>Objekter og klasser</td>
      <td class="chapter">Seksjon 14.1 - 14.9</td>
      <td>
        <Status
          barNum={'bar6'}
          percentage={completePercentage[`chapter${14}`]} />
      </td>
      <td>
        <Chapter chapterNumber={5} />
      </td>
    </tr>

    <tr class="tableRow">
      <td>Tegnstrenger</td>
      <td class="chapter">Kapittel 6</td>
      <td>
        <Status
          barNum={'bar7'}
          percentage={completePercentage[`chapter${6}`]} />
      </td>
      <td>
        <Chapter chapterNumber={6} />
      </td>
    </tr>

    <tr class="tableRow">
      <td>Filbehandling</td>
      <td class="chapter">Kapittel 7</td>
      <td>
        <Status
          barNum={'bar8'}
          percentage={completePercentage[`chapter${7}`]} />
      </td>
      <td>
        <Chapter chapterNumber={7} />
      </td>
    </tr>

    <tr class="tableRow">
      <td>Samlingsstrukturer</td>
      <td class="chapter">Kapittel 8, 9, 10</td>
      <td>
        <Status
          barNum={'bar9'}
          percentage={completePercentage[`chapter${8}`]} />
      </td>
      <td>
        <Chapter chapterNumber={8} />
      </td>
    </tr>

    <tr class="tableRow">
      <td>Grafiske brukergrensesnitt</td>
      <td class="chapter">Gries et al, kapittel 16</td>
      <td>
        <Status
          barNum={'bar10'}
          percentage={completePercentage[`chapter${16}`]} />
      </td>
      <td>
        <Chapter chapterNumber={16} />
      </td>
    </tr>

    <tr class="tableRow">
      <td>Vevtjenester</td>
      <td class="chapter">Sanatans vevartikkel</td>
      <td>
        <Status
          barNum={'bar11'}
          percentage={completePercentage[`chapter${12}`]} />
      </td>
      <td>
        <Chapter chapterNumber={12} />
      </td>
    </tr>
  </table>

</main>
