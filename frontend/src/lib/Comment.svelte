<script>
    let {username, comment} = $props();
    let state = $state({
        showReplySection: true,
        replyText: ''
    })

    function toggleReplySection(){
        state.showReplySection = !state.showReplySection;
    }
    function submitReply(){

    }
</script>

<div>
    <div id="userInfo">
        <!-- TO-DO: move image to assets?-->
        <img id="pfp" alt="profile icon" src="https://static-00.iconduck.com/assets.00/profile-circle-icon-2048x2048-cqe5466q.png" />
        <p id="username">{username}</p>
    </div>
    <div>
        <p id="comment">{comment}</p>
       
        <button id="replyButton" onclick={toggleReplySection}>{state.showReplySection ? 'Cancel' : 'Reply'}</button>
  
    </div>
    <div>
        {#if state.showReplySection}
            <div id="reply">
                <textarea placeholder="Share your reply."></textarea>
                <div id="submitReplyDiv">
                    <button onclick={submitReply}>SUBMIT</button>
                </div>
            </div>
        {/if}
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

    #userInfo{
        display: flex;
        gap: 14px;
    }
   
    #username{
        font-weight: bold;
        position: absolute;
        top: 25px;
        margin-left: 45px;
    }
    #replyButton{
        background: none;
        border: none;
        font-size: 15px;
        font-weight: bold;
        color: #637080;
        margin: none;
        cursor: pointer;
        padding-left: 0;
    }
    #replyButton:hover{
        color: #8698b0;
    }
    #reply{
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
</style>