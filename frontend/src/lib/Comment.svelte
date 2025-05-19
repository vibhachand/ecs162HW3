<script lang="ts">
    let {username, comment, isReply = false, replies = null, ogComment_id, articleName, fetchComments} = $props();
    import { onMount } from 'svelte';
    import { isMod } from '../sharedDataStore';



    let state = $state({
        showReplySection: false,
        newReply: '',
        replies: [] as Comment[],
        isDeleted: false
    })

    interface Comment {
        username: string;
        comment: string;
        article: string;
        isReply?: boolean;
        comment_id?: number;
    }

    // delete comment
    async function deleteComment() {
        const response = await fetch(`http://localhost:8000/api/delete_comment?comment_id=${ogComment_id}`, {
            method: 'DELETE'
        });
        if (response.ok) {
            console.log("comment deleted")
            state.isDeleted = true;
            state.replies = [];
            await fetchComments(articleName);

        } else {
            console.error("Failed to delete comment");
        }

    }

    function toggleReplySection(){
        state.showReplySection = !state.showReplySection;
    }

    // load all existing replies which updates state.replies, thus displaying it in real time
    onMount(async () => {
        await fetchReplies(ogComment_id);
    });
    
    console.log("ogComment_id before POST:", ogComment_id);

    // insert reply to mongo db
    async function postReply(e: SubmitEvent){
        e.preventDefault();
        console.log("Submitting comment:", state.newReply); 
        // Send a POST request to the Flask backend at /add_data
        const response = await fetch('http://localhost:8000/api/add_data', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify({
                article: articleName,
                username: 'student',       // Hardcoded username (can be dynamic later)
                comment: state.newReply,
                isReply: true,
                comment_id: ogComment_id     
            })
        });
        
        if (response.ok) {
            // Clear the input field after successful submission
            state.newReply = "";
            await fetchReplies(ogComment_id);
        } else {
            console.error('Failed to submit comment');
        }
    }

    // fetch replies from mongo db, want only replies with the specified comment_id (so we know what original comment the reply comment is under)
    async function fetchReplies(ogComment_id: string){
        const res = await fetch(`http://localhost:8000/get_replies?comment_id=${ogComment_id}`);
        const data = await res.json();
        state.replies = data;
        console.log("Replies: ");
        console.log(state.replies);
        // state.numOfComments = state.comments.length;
    }
    
</script>

{#if !state.isDeleted}
<div class="container">
    <div class="userInfo">
        <!-- TO-DO: move image to assets?-->
        <img id="pfp" alt="profile icon" src="https://static-00.iconduck.com/assets.00/profile-circle-icon-2048x2048-cqe5466q.png" />
        <div>
            <p class="username"><strong>{username}</strong></p>
        </div>
    </div>
    <div>
        <p class="comment">{comment}</p>
        <button id="replyButton" onclick={toggleReplySection}>{state.showReplySection ? 'Cancel' : 'Reply'}</button>
        {#if $isMod}
            <button id="deleteButton" onclick={deleteComment}>Delete</button>
        {/if}
    </div>
    <div>
        {#if state.showReplySection}
            <form onsubmit={postReply} class="reply">
                <textarea bind:value={state.newReply} placeholder="Share your reply."></textarea>
                <div id="submitReplyDiv">
                    <button type="submit">SUBMIT</button>
                </div>
            </form> 
        {/if}
        {#each state.replies as r}
            <div class="othersReply">
            <div class="userInfo">
                <img id="pfp" alt="profile icon" src="https://static-00.iconduck.com/assets.00/profile-circle-icon-2048x2048-cqe5466q.png" />
                <div>
                    <p class="username"><strong>user</strong></p>
                </div>
            </div>
            <div>
                <p class="comment">{r.comment}</p>              
            </div>
         </div>
       
        {/each}
        
        
    </div>
    
</div>
{/if}

<style>
    *{
        font-family: Arial, Helvetica, sans-serif;
    }
    .container{
        margin-top: 20px; 
        border-bottom: 1px #cccecf solid; 
        padding-bottom: 15px; 
    }

    img{
        width: 35px;
        height: 35px;
        opacity: 0.6;
    }

    .userInfo{
        display: flex;
        gap: 14px;
    }
   
    .comment{
        padding-left: 50px;
        margin-top: 8px;
    }
    
    #replyButton{
        background: none;
        border: none;
        font-size: 15px;
        font-weight: bold;
        color: #637080;
        margin: 0;
        cursor: pointer;
        padding-left: 50px;
    }
    #replyButton:hover{
        color: #8698b0;
    }
    .reply{
        display: flex;
        flex-direction: column;
        padding-top: 15px;
        margin-left: 25px;
        > textarea{
            resize: none; /* Disables resizing */
            width: 403px;
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
        }
    }
    
    #submitReplyDiv{
        display: flex;
        justify-content: flex-end;
    }
    .othersReply{
        border-left: 1px solid #cccecf;
        padding: 12px 0px 12px 12px;
        margin-top: 15px;
        margin-left: 20px;
    }
</style>