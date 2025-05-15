<!-- Displays article info -->
<script>
  let { id, articles, hideHr = false, numOfComments} = $props();

  let openComments = document.getElementById("openComments");
  
  if(openComments){
    openComments.onclick = function() {
      
    };
  }
  

</script>

<a href={articles[id].url} target="_blank">
  <div>
      <img src={articles[id].image} alt={articles[id].caption}/>
      <h2 class="side-column">{articles[id].headline}</h2>
      <p data-testid="article-abstract" class="article-text">{articles[id].abstract}</p>
      <p data-testid="article-author" class="article-text">{articles[id].author}</p>
      <button id="openComments">{numOfComments} Comments</button>
  </div>
</a>

<!-- don't want articles on the last row to have bottom divider -->
{#if !hideHr}
  <hr class="col-break">
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