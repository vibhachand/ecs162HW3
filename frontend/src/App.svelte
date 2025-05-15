<!-- run pytests: "pytest -v backend/tests" -->
<script lang="ts">
  import { onMount } from 'svelte';
  import Date from './lib/Date.svelte';
  import Article from './lib/Article.svelte';

  let apiKey: string = '';

  // format of article objects
  let articles: {
    headline: string;
    url: string;
    author: string;
    abstract: string;
    image: string | null;
    caption: string;
  }[] = [];

  onMount(async () => {
    try {
      const res = await fetch('/api/key');
      const data = await res.json();
      apiKey = data.apiKey;
    } catch (error) {
      console.error('Failed to fetch API key:', error);
    }

    try{
      const res = await fetch('http://localhost:8000/articles?q=Davis');
      const data = await res.json();
      articles = data.articles;
    } catch(error){
      console.error('Error fetching articles:', error);
    }
  });
</script>

<main>
    <!--header includes title and date -->
    <header>
        <img class="logo" alt="logo of new york times" src="./src/assets/The_New_York_Times_logo.png">
        <div class="features">
          <Date/>
          <p class="date-text">Today's Paper</p>
        </div>
    </header>
    <div class="grid-container">
        <div class="column1">
            {#if articles.length > 2}
               
                <!-- column1: first article -->
                <Article id = 0 articles={articles}/>
                
                <!-- column1: second article -->
                <Article id = 1 articles={articles} hideHr={true}/>
                
            {:else}
                <!-- Placeholder content -->
                <h2 class="side-column">Loading...</h2>
                <p class="article-text">Loading articles...</p>
            {/if}
        </div>
        
        <!-- column2: main column -->
        <div class="column2">
            {#if articles.length > 4}
                <Article id = 3 articles={articles}/>
              
                <!-- column2: second article -->
                <Article id = 4 articles={articles} hideHr={true}/>
            {:else}
                <!-- Placeholder content -->
                <h2 class="main-column">Loading...</h2>
                <p class="article-text">Loading articles...</p>
                <hr class="col-break" id="col2-separator1">
            {/if}
        </div>
        
        <div class="column3">
            {#if articles.length > 6}
                <Article id=5 articles={articles}/>
                
                <!-- column3: second article -->
                <Article id = 6 articles={articles} hideHr={true}/>
            {:else}
                <!-- Placeholder content -->
                <h2 class="side-column">Loading...</h2>
                <p class="article-text">Loading...</p>
            {/if}
        </div>
    </div>
    <footer>
        <hr class="footer-line-break">
    </footer>
</main>

<style>
  /* all css styles located in app.css */
  
</style>