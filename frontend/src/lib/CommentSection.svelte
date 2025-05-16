<script>
    let {numOfComments = 0} = $props();
</script>

<div class="overlay"></div>

<!-- comment section  -->
<div>
    <h2>Comments <span id="numOfComments">{numOfComments}</span></h2>
    <form>
        <textarea id="comment" required placeholder="Share your thoughts."></textarea>
        <button type="submit">Post Comment</button>
    </form>
</div>

<style>
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
    h2{
        font-family: Arial, Helvetica, sans-serif;
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
    }
    #comment{
        width: 100%;
        height: 20vh;
    }
    form{
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    button{
        margin-top: 20px;
        width: fit-content;
        padding: 10px;
        cursor: pointer;
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
