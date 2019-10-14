<script>
  import { createEventDispatcher } from "svelte";
	import { fly } from 'svelte/transition';
  const dispatch = createEventDispatcher();

  let username = "";
  let password = "";

  function login() {
    if (username && password) {
      dispatch("login", {username, password});
    }
  }

  function cancel() {
    dispatch("cancel");
  }
</script>

<style>
  .wrapper {
    width: 300px;
    height: 400px;

    position: fixed;
    margin: auto;

    background-color: white;
    box-shadow: 1px 2px 3px black;

    display: flex;
    flex-direction: column;
    justify-content: center;

    z-index: 5;
  }

  h1{
    text-align: center;
  }

  form {
    display: flex;
    flex-direction: column;

    padding: 5px;
  }

  label {
    margin: 5px;
    display: flex;
    justify-content: center;
  }

  input {
    margin: 0 5px;
  }

  button {
    margin: 5px;
  }

  .buttons {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }

</style>


<div class="wrapper" in:fly="{{ y: -400, duration: 1000 }}" out:fly="{{ y: -400, duration: 1000 }}" on:click|stopPropagation>
  <h1>Login</h1>
  <form on:submit|preventDefault>
    <label>Username:
      <input type="text" bind:value={username}>
    </label>
    <label>Password:
      <input type="password" bind:value={password}>
    </label>
    <div class="buttons">
      <button on:click={cancel}>Cancel</button>
      <button on:click={login}>Login</button>
    </div>
  </form>
</div>