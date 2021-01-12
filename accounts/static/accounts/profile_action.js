document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('.action-btn').forEach(button => {
        button.onclick = function(){
            friend_request_action(this);
        }
    })
})


function friend_request_action(button){
    fetch(`${button.dataset.slug}/`, {
        method: 'POST',
        body: JSON.stringify({
            'action': button.dataset.action
        })
    }).then(response => response.json())
    .then(result => {
        console.log(result);
        if (button.dataset.disabled){
            location.reload();
        }
        else{
            if (!result.is_friend && result.check_friend_request){
                button.classList.remove('btn-primary');
                button.classList.add('btn-warning');
                button.innerText = 'Cancel request';
                button.dataset.action = 'cancel_friend_request';
            
            }
            if(!result.is_friend && !result.check_friend_request){
                button.classList.remove('btn-warning');
                button.classList.remove('btn-danger')
                button.classList.add('btn-primary');
                button.innerText = 'Add friend';
                button.dataset.action = 'send_friend_request';
            }
        }
    })

}