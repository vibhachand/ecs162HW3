<script lang="ts">
    import Comment from './Comment.svelte';
    import { onMount } from 'svelte';
    
    let {articleName} = $props();

    let state = $state({
        newComment: "",
        numOfComments: 0,
        comments: [] as Comment[]
    })
    
    interface Comment {
        _id: string;
        username: string;
        comment: string;
        article: string;
        isReply?: boolean;
        comment_id?: number;
    }

    // loads and displays all existing comments
    onMount(async () => {
        await fetchComments(articleName);
    });
    
    // insert comment into mongodb
    async function postComment(e: SubmitEvent){
        e.preventDefault();
        console.log("Submitting comment:", state.newComment); 
        // Send a POST request to the Flask backend at /add_data
        const response = await fetch('http://localhost:8000/api/add_data', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify({
                article: articleName,
                username: 'student',       // Hardcoded username (can be dynamic later)
                comment: state.newComment,
                comment_id: "",
                isReply: false        
            })
        });
        
        if (response.ok) {
            // Clear the input field after successful submission
            state.newComment = "";
            await fetchComments(articleName);
        } else {
            console.error('Failed to submit comment');
        }
    }

    async function fetchComments(article_id: string) {
        const res = await fetch(`http://localhost:8000/get_comments?article=${article_id}`);
        const data = await res.json();
        state.comments = data;
        console.log(state.comments);
        state.numOfComments = state.comments.length;
    }
</script>

<div class="overlay" style="position: fixed; "></div>

<!-- comment section  -->
<div class="container">
    <h1>{articleName}</h1>
    <h2>Comments <span id="numOfComments">{state.numOfComments}</span></h2>
    <!-- comment form for new comment -->
    <form onsubmit={postComment}>
        <textarea bind:value={state.newComment} id="comment" required placeholder="Share your thoughts."></textarea>
        <button type="submit">SUBMIT</button>
    </form>
    <div id="commentsContainer">
        {#each state.comments as c}
            <!-- pass the comment's username, comment, and _id (to be used to identify which parent comment a reply belongs to) as props to Comment component -->
            <Comment username={c.username} comment={c.comment} ogComment_id={c._id} isReply={false}/>
        {/each}
    </div>
</div>

<style>
    *{
        font-family: Arial, Helvetica, sans-serif;
    }
    .container{
        position: fixed; 
        overflow-y: auto; 
        padding-bottom: 25px;
    }
    h1{
        margin-top: 0px;
        padding-bottom: 20px;
        border-bottom: 1px solid #cccecf;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    div{
        width: 450px;
        height: 100vh;
        background: white;
        position: absolute;
        right: 0;
        top: 0;
        z-index: 2;
        padding: 2vw 5vw 2vw 5vw;
    }
    #commentsContainer{
        position: relative;
        padding-left: 0
    }
    
    /* gray overlay to the left of comment section */
    .overlay{
        margin: 0px;
        width: 50vw;
        height: 100vh;
        top: 0;
        left: 0;
        background-color: rgba(0, 0, 0, 0.3);
        position: absolute;

    }
    textarea {
        resize: none; /* Disables resizing */
        padding: 15px;
        border-radius: 5px;
        font-size: 16px;
    }
   
    #comment{
        width: 100%;
        height: 30px;
    }
    form{
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    

    #numOfComments{
        font-weight: normal;
        font-family: Arial, Helvetica, sans-serif;
    }
</style>
