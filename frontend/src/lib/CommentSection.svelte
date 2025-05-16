<script>
    let {numOfComments = 0} = $props();
    import Comment from './Comment.svelte';
</script>

<div class="overlay"></div>

<!-- comment section  -->
<div>
    <h2>Comments <span id="numOfComments">{numOfComments}</span></h2>
    <form>
        <textarea id="comment" required placeholder="Share your thoughts."></textarea>
        <button type="submit">SUBMIT</button>
    </form>
    <div id="commentsContainer">
        <Comment username="student" comment="Blah blah blah."/>
    </div>
</div>

<style>
    *{
        font-family: Arial, Helvetica, sans-serif;
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

    /* @media screen and (max-width: 767px) {
        .overlay{
            display: none;
        }
        div{
            width: 100vw;
            height: 100vh;
            position: relative;
            padding: 10vw;
        }
        #comment{
            width: 70vw;
        }
    } */

    #numOfComments{
        font-weight: normal;
        font-family: Arial, Helvetica, sans-serif;
    }
</style>
