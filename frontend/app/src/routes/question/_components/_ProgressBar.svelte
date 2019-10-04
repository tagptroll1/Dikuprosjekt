<script>
  import index from "../../../stores/index";
  import { afterUpdate } from "svelte";

  export let len;
  let myBar;
  let myBarWidth = 0;

  afterUpdate(() => {
    let hop = 100 / (len - 1);
    let width = $index * hop;
    if (width > 100) {
      width = 100;
    }
    myBar.style.width = width + "%";
  });
</script>

<style>
  #myProgress {
    position: relative;
    width: 100%;
    background-color: #ddd;
    margin-bottom: 20px;
  }
  #myBar {
    display: flex;
    align-items: center;
    height: 30px;
    background-color: #5cb85c;
    /* width of the bar set initially to 0% to hide it */

    width: 0;
    /* transition for smooth animation */
    transition: all ease-in-out 0.5s;
  }

  span {
    position: absolute;
    width: 100%;
    text-align: center;
  }
</style>

<!-- Progress bar -->
<div id="myProgress">
  <div id="myBar" bind:this={myBar}>
    <span>{$index + 1} / {len}</span>
  </div>
</div>
