import { writable } from "svelte/store";

//writable store, which means it has set, subscribe and update methods.
//Any unrelated component or regular JS module can access this value.

export default writable(0);
