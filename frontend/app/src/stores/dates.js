import { writable } from "svelte/store";

export const startDate = writable(new Date(Date.now()));
export const startTime = writable(new Date().getTime() / 1000);
