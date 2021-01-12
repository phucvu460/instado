function like_post(button, event){
    event.preventDefault();
    fetch(`/like_post/${button.dataset.post}`)
    .then(response => response.json())
    .then(result => {
        console.log(result)
        if (result.liked){
            document.getElementById(`like-btn-${button.dataset.post}`).classList.remove('btn-outline-primary');
            document.getElementById(`like-btn-${button.dataset.post}`).classList.add('btn-primary');
            span = document.getElementById(`like-btn-${button.dataset.post}`).children[1];
            span.innerHTML = parseInt(span.innerText) + 1;
        }
        else{
            document.getElementById(`like-btn-${button.dataset.post}`).classList.remove('btn-primary');
            document.getElementById(`like-btn-${button.dataset.post}`).classList.add('btn-outline-primary');
            span = document.getElementById(`like-btn-${button.dataset.post}`).children[1];
            span.innerHTML = parseInt(span.innerText) - 1;
        }
    })
}


function comment_post(event){
    event.preventDefault();
    const post_id = document.getElementById('post_id').value;
    fetch(`/post/${post_id}`, {
        method: 'POST',
        body: JSON.stringify({
            content: document.getElementById('comment').value
        })
    }).then(response => response.json())
    .then(result => {
        console.log(result);
        if (!result.message){
            load_comment(result);
            document.getElementById('comment').value = '';
        }

    })
}


function load_comment(comment){
    container = document.getElementById('post-details')
    comments_body = document.createElement('div')
    comments_body.innerHTML = `<a href="${comment.profileURL}">
    <img src="${comment.profileImage}" class="rounded-circle" width="30" height="30">
    </a>
    <a class="text-dark" href="${comment.profileURL}"><b>${comment.profileName}</b></a>
    <br><small>${ comment.createdOn }</small><br><br>
    <p class="card-text text-dark">${ comment.content }</p>
    <hr class="my-1">`;
    container.appendChild(comments_body);
}
