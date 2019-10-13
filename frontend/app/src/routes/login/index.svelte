<script context="module">
  export async function preload(page, session) {
    const loggedIn = session && session.loggedIn;
    return { loggedIn }
  }
</script>

<script>
  import Login from "../../components/Login.svelte";
  import {stores, goto} from "@sapper/app"
  export let loggedIn;

  const {session} = stores();

  async function login({detail}) {
    const {username, password} = detail;

    const resp = await fetch("/api/login", {
      method: "POST",
      headers: {
        Authorization: `${username}:${password}`
      }
    });

    if (resp.ok) {
      loggedIn = true;
      $session.loggedIn = true;
      goto("/questionmaker")
    }
  }
</script>

{#if loggedIn} 
  Logged in
{:else}
  <Login on:login={login} />
{/if}

