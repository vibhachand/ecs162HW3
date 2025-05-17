<script>
    let {username, comment, isReply = false, replies = null} = $props();
    let state = $state({
        showReplySection: false,
        replyText: ''
    })

    function toggleReplySection(){
        state.showReplySection = !state.showReplySection;
    }
    function submitReply(){

    }
    
</script>

<div style="margin-top: 15px; border-bottom: 1px #cccecf solid; padding-bottom: 15px; ">
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
  
    </div>
    <div>
        {#if state.showReplySection}
            <div class="reply">
                <textarea placeholder="Share your reply."></textarea>
                <div id="submitReplyDiv">
                    <button onclick={submitReply}>SUBMIT</button>
                </div>
            </div>
            
        {/if}
        <!-- add code to iterate through each reply -->
        <div class="othersReply">
            <div class="userInfo">
                <!-- TO-DO: move image to assets?-->
                <img id="pfp" alt="profile icon" src="https://static-00.iconduck.com/assets.00/profile-circle-icon-2048x2048-cqe5466q.png" />
                <div>
                    <p class="username"><strong>user</strong></p>
                </div>
            </div>
            <div>
                <p class="comment">Hi everyone</p>              
            </div>
         </div>
        
    </div>
    
</div>

<style>
    *{
        font-family: Arial, Helvetica, sans-serif;
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
   
    
    #replyButton{
        background: none;
        border: none;
        font-size: 15px;
        font-weight: bold;
        color: #637080;
        margin: 0;
        cursor: pointer;
        padding-left: 0;
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
    button{
        margin-top: 7px;
        width: fit-content;
        padding: 5px 6px;
        cursor: pointer;
        font-weight: bold;
        background: white;
        border-radius: 5px;
        border: 1px gray solid;
    }
    button:hover{
        color: white;
        background: #78919e;
        border-color: #78919e;
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