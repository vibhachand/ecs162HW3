<!-- run pytests: "pytest -v backend/tests" -->
<script lang="ts">
  import { onMount } from 'svelte';
  import Date from './lib/Date.svelte';
  import Article from './lib/Article.svelte';
  import CommentSection from './lib/CommentSection.svelte';

  let apiKey: string = '';

  let loggedIn = false;
  let email = "";

  let showAccount = false;

  // toggle panel at log in
  function toggleAccount() {
    showAccount = !showAccount;
  }

  // logout function
  async function logout() {
    await fetch('http://localhost:8000/logout', {
      method: 'GET'
    });
    
    window.location.href = '/';
  }

  // log in function
  function redirectLogin() {
    const currentUrl = encodeURIComponent(window.location.href);
    window.location.href = `http://localhost:8000/login?returnTo=${currentUrl}`;
  }


  let commentSectionVisible = false;

  // format of article objects
  let articles: {
    headline: string;
    url: string;
    author: string;
    abstract: string;
    image: string | null;
    caption: string;
  }[] = [];
  // from TA's OH code
  // async function handleLogin(){
  //   const authUrl = 'http://localhost:8000/login'
  //   window.location.href = authUrl;
  // }
  onMount(async () => {
    // from TA's OH code:
    // const url = new URL(window.location.href);
    // userEmail = url.searchParams.get('user');
    try {
      console.log("here")

      const params = new URLSearchParams(window.location.search);
      loggedIn = params.get('loggedIn') === 'true';
      email = params.get('email');
      console.log(loggedIn)
      console.log(email)


    } catch (err) {
      console.error('Error checking login status:', err);
    }

    try {
      const res = await fetch('http://localhost:8000/api/key');
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
    <!-- UNCOMMENT THE LINE BELOW TO SHOW COMMENT SECTION -->
    <!-- <CommentSection/> -->
    <div style="z-index: 1;">
    <header>
        {#if loggedIn}
          <button id="account-button" on:click={toggleAccount}>Account</button>
        {:else}
          <button id="login-button" on:click={redirectLogin}>LOG IN</button>
        {/if}
        <img class="logo" alt="logo of new york times" src="./src/assets/The_New_York_Times_logo.png">
        <div class="features">
          <Date/>
          <p class="date-text">Today's Paper</p>
        </div>
    </header>
    {#if showAccount}
      <div class="account">
        <button class="close" on:click={toggleAccount}>x</button>
        <p id="email">{email}</p>
        <p id="greeting">Good Afternoon.</p>
        <button id="logout-button" on:click={logout}>Log out</button>
      </div>
    {/if}
    <div class="grid-container">
        <div class="column1">
            {#if articles.length > 2}
               
                <!-- column1: first article -->
                <Article id = 0 articles={articles} />
                
                <!-- column1: second article -->
                <Article id = 1 articles={articles} hideHr={true} />
                
            {:else}
                <!-- Placeholder content -->
                <h2 class="side-column">Loading...</h2>
                <p class="article-text">Loading articles...</p>
            {/if}
        </div>
        
        <!-- column2: main column -->
        <div class="column2">
            {#if articles.length > 4}
                <Article id = 3 articles={articles} />
              
                <!-- column2: second article -->
                <Article id = 4 articles={articles} hideHr={true} />
            {:else}
                <!-- Placeholder content -->
                <h2 class="main-column">Loading...</h2>
                <p class="article-text">Loading articles...</p>
                <hr class="col-break" id="col2-separator1">
            {/if}
        </div>
        
        <div class="column3">
            {#if articles.length > 6}
                <Article id=5 articles={articles} />
                
                <!-- column3: second article -->
                <Article id = 6 articles={articles} hideHr={true} />
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
  </div>
</main>

<style>
  /* all css styles located in app.css */
  
</style>