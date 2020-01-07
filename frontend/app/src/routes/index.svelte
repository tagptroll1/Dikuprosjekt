<script>
  import { goto } from "@sapper/app"
  import { onMount,onDestroy } from "svelte";
  import { slide, fade } from "svelte/transition";

  import user from "../stores/user.js";
  import index from "../stores/index";
  import questions from "../stores/questions";

  import Logo from "../components/LogoUIB.svelte";
  import Logo2 from "../components/LogoUIB_mpython.svelte";

  $index = 0;
  $questions = [];

  let canvas;
  let ctx;
  let color;
  onMount(()=>{
    ctx = canvas.getContext('2d');
    let frame;

    function loop(t) {
      frame = requestAnimationFrame(loop);

      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);

      for (let p = 0; p < imageData.data.length; p += 4) {
        const i = p / 4;
        const x = i % canvas.width;
        const y = i / canvas.height >>> 0;

        const r = 64 + (128 * x / canvas.width) + (64 * Math.sin(t / 2500));
        const g = 64 + (128 * y / canvas.height) + (64 * Math.cos(t / 2500));
        const b = 128;

        imageData.data[p + 0] = r * .9;
        imageData.data[p + 1] = g * .4;
        imageData.data[p + 2] = b * .7;
        imageData.data[p + 3] = 255;
      }

      ctx.putImageData(imageData, 0, 0);
    } requestAnimationFrame(loop);

    return () => {
      cancelAnimationFrame(frame);
    };
  });

  const pattern = `[a-zA-ZæøåÆØÅ]{3}\\d{3}`;

  let input;
  let value = '';
  let valid = true;
  let placeholder = "ex; rob404";
  let numberOfAttempts = 0;
  let wrongInput;

  const alternatives = [
    'joe432',
    'tom233',
    'aar444',
    'jef007',
  ]

  function handleEnter(event){
    const key = event.key;
    const code = event.keyCode;
    if(key === "Enter" || code === 13){
      start();
      event.preventDefault();
    }
  }

  function start(){
    valid = input.checkValidity();

    if(valid){
      $user = input.value;
      goto("/question");
    } else {
      if(numberOfAttempts >= 3){
        //just go there anyway...jees...
        goto("/question");
      } 
    }
  }

</script>

<canvas
  bind:this={canvas}
  width={32}
  height={32}
></canvas>

<div class="outer">
  <figure>
    {#if value === 'python'}
      <Logo2/>
    {:else}
      <Logo/>
    {/if}
  </figure>
  <h1>UiB Python</h1>

  <div class="inpblock">

    <span class="info">Please enter your UIB Username <br>(or <b>leave blank</b> to stay anonymous):</span>
    <input 
      {pattern} 
      {placeholder}
      bind:this={input} 
      bind:value
      on:keydown={handleEnter}
      on:input={()=>valid = input.checkValidity()}
      maxlength="6"
    >
    {#if wrongInput}
      <span transition:slide>Invalid format!<br>Try again or start as anonymous.</span>
    {/if}
  </div>

  <button
    disabled={!valid || null}
    class="start" 
    on:click={start}
  >Start as <b>{value ? value : 'anonymous'}</b></button>
</div>

<style>
  .outer{
    color: var(--bg-main);
    display: flex;
    flex-direction: column;
    align-items: center;

    /* background-color: hsla(0, 0%, 77%, 0.6); */
    padding: 20px 30px;
  }

  h1 {
    text-align: center;
    font-weight: 300;
    font-size: 3.2em;
    margin: 10px 0;
  }

  button:focus,
  button::-moz-focus-inner{
    outline: none;
    border:none;
  }

  .start {
    border: none;
    cursor: pointer;

    padding: 10px 25px;
    margin: 15px;
    color: var(--bg-main);
    background-color: var(--bg-focus);
    border-radius: 8px 4px;

    position: relative;

    font-size: 1em;

    transition: opacity .2s;
  }

  .start:disabled{
      opacity: .5;
      cursor: unset;
  }
  
  .start:not(:disabled)::after {
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

  .start:focus::after,
  .start:hover::after {
    width: calc(100% - 50px);
  }

  input{
    border: none;
    border-bottom: 4px solid;
    height: 1.5em;
    font-size: 1.4em;
    text-align: center;

    margin-bottom: 15px;
  }
  input::placeholder{
    opacity: .3;
  }
  input:valid{
    border-color: hsl(120, 100%, 70%);
  }
  input:invalid{
    border-color: hsl(7, 100%, 70%);

    box-shadow: none;
  }

  canvas{
    position: fixed;
    z-index: -1;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;

    width: 100%;
    height: 100%;

    background-color: #64344b;
  }

  .inpblock{
    display: flex;
    flex-direction: column;
  }

  .inpblock span{
    text-align: center;
    margin: 10px;
  }

  
  figure{
    max-width: 128px;
    max-height: 128px;
  }

  .inpblock input,.start{
    box-shadow: 1px 3px 1px -2px rgba(0, 0, 0, 0.3);
  }

  h1,
  span{
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8);
  }

  input + span{
    font-weight: bold;
  }

</style>
