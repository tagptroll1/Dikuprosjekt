<script>
  export let segment;
</script>

<style>
  main {
    position: relative;
    z-index: 1;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 100vh;

    background-color: rgb(231, 231, 231);
  }
</style>

<main>
  <slot/>
</main>
