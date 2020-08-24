<script>
  import selectedChapter from "../../stores/selectedChapter";
  import user from "../../stores/user";
  import userdata from "../../stores/userdata";
  import Difficulty from "./_components/_Difficulty.svelte";
  import { goto } from "@sapper/app";

  function goToDash() {
    goto("../dashboard");
  }

  let status = {
    difficulty1: "Ingen Forsøk ✖",
    difficulty2: "Ingen Forsøk ✖",
    difficulty3: "Ingen Forsøk ✖"
  };

  function generateStatus() {
    if (`chapter${$selectedChapter}` in $userdata["results"]) {
      for (let i = 1; i <= 3; i++) {
        if (
          `difficulty${i}` in $userdata["results"][`chapter${$selectedChapter}`]
        ) {
          if (
            $userdata["results"][`chapter${$selectedChapter}`][
              `difficulty${i}`
            ][0] ==
            $userdata["results"][`chapter${$selectedChapter}`][
              `difficulty${i}`
            ][1]
          ) {
            status[`difficulty${i}`] = "Ferdig ✔";
          } else {
            status[
              `difficulty${i}`
            ] = `Påbegynt 🤔 ${$userdata["results"][`chapter${$selectedChapter}`][`difficulty${i}`][0]} / ${$userdata["results"][`chapter${$selectedChapter}`][`difficulty${i}`][1]}`;
          }
        }
      }
    }
  }

  if ($user !== "anon" && $user !== "") {
    generateStatus();
  }

  let pageInfo = {
    "2": {
      title: "Kapittel 2 - Uttrykk",
      content: " "
    },

    "3": {
      title: "Kapittel 3 - Betinget Utførelse",
      content: " "
    },

    "4": {
      title: "Kapittel 4 - Funksjoner",
      content: " "
    },

    "5": {
      title: "Kapittel 5 - Iterasjon",
      content: " "
    },

    "6": {
      title: "Kapittel 6 - Tegnstrenger",
      content: " "
    },

    "14": {
      title: "Kapittel 14 - Objekter & klasser",
      content: " "
    },

    "7": {
      title: "Kapittel 7 - Filbehandling",
      content: " "
    },

    "8": {
      title: "Kapittel 8-10 - Samlingsstrukturer",
      content: " "
    },

    "16": {
      title: "Grafisk brukergrensesnitt",
      content: " "
    },

    "12": {
      title: "Vevtjenester",
      content: " "
    }
  };
</script>

<style>
  table {
    padding: 35px;
    box-shadow: 0 7px 15px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
  }

  .infoText {
    max-width: 30vw;
    line-height: 1.6;
  }

  th,
  td {
    padding: 15px;
    text-align: left;
  }
</style>

<main>
  {#if $selectedChapter == 0}
    <button style="display:none" on:click|once={goToDash()} />
  {:else}
    <h1 class="header">{pageInfo[$selectedChapter]['title']}</h1>
    <p>{pageInfo[$selectedChapter]['content']}</p>
    <p class="infoText">Velg en vanskelighetsgrad</p>
    <button on:click={goToDash}>Tilbake til dashboard</button>

    <table style="padding: 10px">
      <tr>
        <th class="tableHeader">Vanskelighetsgrad</th>
        <th style="text-align: center" class="tableHeader">Status</th>
        <th />
      </tr>

      <tr>
        <td>Lett</td>
        <td>{status['difficulty1']}</td>
        <td>
          <Difficulty difficulty={'Lett'} />
        </td>
      </tr>

      <tr>
        <td>Middels</td>
        <td>{status['difficulty2']}</td>
        <td>
          <Difficulty difficulty={'Middels'} />
        </td>
      </tr>

      <tr>
        <td>Vanskelig</td>
        <td>{status['difficulty3']}</td>
        <td>
          <Difficulty difficulty={'Vanskelig'} />
        </td>
      </tr>

    </table>
    <br />
  {/if}
</main>
