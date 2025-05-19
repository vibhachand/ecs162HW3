<!-- Displays article info -->
<script lang="ts">
    import { onMount } from 'svelte';

  let { id, articles, hideHr = false, username} = $props();
  import CommentSection from './CommentSection.svelte';

  let comments = [] as Comment[];

  let state = $state({
        numOfComments: 0,
        showCommentSection: false
    })

  function showCommentSection(){
    state.showCommentSection = true;
  }

  // Add this function to close the comment section
  function closeCommentSection(){
    state.showCommentSection = false;
  }
    
  interface Comment {
      _id: string;
      username: string;
      comment: string;
      article: string;
      isReply?: boolean;
      comment_id?: number;
  }
  onMount(async() => {
    await fetchComments();
  })
  async function fetchComments() {
        const res = await fetch(`http://localhost:8000/get_comments?article=${articles[id].headline}`);
        const data = await res.json();
        comments = data;
        console.log(comments);
        state.numOfComments = comments.length;
    }
</script>

<div>
  <a href={articles[id].url} target="_blank">
    <img src={articles[id].image} alt={articles[id].caption}/>
    <h2 class="side-column">{articles[id].headline}</h2>
    <p data-testid="article-abstract" class="article-text">{articles[id].abstract}</p>
    <p data-testid="article-author" class="article-text">{articles[id].author}</p>
  </a>
    <button onclick={ showCommentSection }>{state.numOfComments} Comments</button>
</div>

<!-- don't want articles on the last row to have bottom divider -->
{#if !hideHr}
  <hr class="col-break">
{/if}

{#if state.showCommentSection}
  <CommentSection 
    username={username}
    articleName={articles[id].headline}
    onClose={closeCommentSection}
  />
{/if}

<style>
  hr{
      margin-bottom: 7%;
  }
  img{
      max-width: 100%;
      height: auto;
  }

  h2{
      font-size: 20px;
      font-family: Georgia, serif;
  }

  a{
      color: black; 
      text-decoration: none;  
  }  
  
</style>