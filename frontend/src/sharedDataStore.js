import { writable } from 'svelte/store';

export const isLoggedIn = writable(false);
export const isMod = writable(false);