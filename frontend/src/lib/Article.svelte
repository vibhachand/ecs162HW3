<!-- Displays article info -->
<script lang="ts">
  let { id, articles, hideHr = false} = $props();
  import CommentSection from './CommentSection.svelte';
  import { onMount } from 'svelte';
  let state = $state({
        numOfComments: 0,
        comments: [] as Comment[],
        showCommentSection: false
    })

  // let openComments = document.getElementById("openComments");
  
  // if(openComments){
  //   openComments.onclick = function() {
      
  //   };
  // }

  // interface Comment {
  //       username: string;
  //       comment: string;
  //       article: "test";
  //       isReply?: boolean;
  //   }

    
    // onMount(async () => {
    //     await fetchComments("test");
    // });
  
  // async function fetchComments(article_id: string) {
  //       const res = await fetch(`http://localhost:8000/get_comments?article=${article_id}`);
  //       const data = await res.json();
  //       state.comments = data;
  //       state.numOfComments = state.comments.length;
  //   }

  function showCommentSection(){
    state.showCommentSection = true;
  }

</script>


  <div>
    <a href={articles[id].url} target="_blank">
      <img src={articles[id].image} alt={articles[id].caption}/>
      <h2 class="side-column">{articles[id].headline}</h2>
      <p data-testid="article-abstract" class="article-text">{articles[id].abstract}</p>
      <p data-testid="article-author" class="article-text">{articles[id].author}</p>
    </a>
      <button onclick={ showCommentSection }>Comments</button>
  </div>

<!-- don't want articles on the last row to have bottom divider -->
{#if !hideHr}
  <hr class="col-break">
{/if}

{#if state.showCommentSection}
  <CommentSection articleName={articles[id].headline}/>
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