<script>
  import { onMount } from "svelte";
  export let barNum = "bar0";
  export let percentage = 0;

  var i = 0;
  function move(percentage) {
    if (i == 0) {
      i = 1;
      var elem = document.getElementById(barNum);
      var width = 0;
      var id = setInterval(frame, 10);
      function frame() {
        if (width >= percentage) {
          clearInterval(id);
          i = 0;
        } else {
          width++;
          elem.style.width = width + "%";
          elem.innerHTML = width + "%";
        }
      }
    }
  }

  onMount(() => {
    move(percentage);
  });
</script>

<style>
  .myProgress {
    background-color: rgba(202, 202, 202, 0.76);
    border-radius: 10px;
    width: 190px;
  }

  .integer {
    margin-left: 90px;
  }

  .bar {
    width: 0%;
    height: 30px;
    background-color: #4caf50;
    text-align: center;
    /* To center it horizontally (if you want) */
    line-height: 30px;
    /* To center it vertically */
    color: black;
    border-radius: 10px;
  }
</style>

<main>
  <div class="myProgress">
    <div id={barNum} class="bar">
      <p class="integer">0%</p>
    </div>
  </div>
</main>
