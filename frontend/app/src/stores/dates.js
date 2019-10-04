import { writable } from "svelte/store";

export const startDate = writable(new Date(Date.now()));
