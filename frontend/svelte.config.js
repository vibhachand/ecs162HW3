// used chatgpt to fix an error on finding package
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('svelte/compiler').PreprocessGroup} */
const config = {
  preprocess: vitePreprocess()
};

export default config;