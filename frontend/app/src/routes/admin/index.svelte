<script context="module">
  export async function preload(page, session) {
    const loggedIn = session && session.loggedIn;

    if (!loggedIn) {
      
    }
    if (!(session && session.loggedIn)) {
      this.redirect(401, "/");
    }
  }
</script>

