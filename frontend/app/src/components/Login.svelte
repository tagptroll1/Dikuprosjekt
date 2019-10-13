<script>
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  let username = "";
  let password = "";

  function login() {
    if (username && password) {
      dispatch("login", {username, password})
    }
  }
</script>

<form on:submit|preventDefault>
  <label>Username
    <input type="text" bind:value={username}>
  </label>
  <label>Password
    <input type="password" bind:value={password}>
  </label>
  <button on:click={login}>Login</button>
</form>