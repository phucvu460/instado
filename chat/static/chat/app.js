let currentRecipient = '';
let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let userList = $('#user-list');
let messageList = $('#messages');

function updateUserList() {
    $.getJSON('http://127.0.0.1:8000/accounts/api/v1/user/', function (data) {
        userList.children('.user').remove();
        for (let i = 0; i < data.length; i++) {
            const userItem = `<a class="list-group-item user">${data[i]['username']}</a>`;
            $(userItem).appendTo('#user-list');
        }
        $('.user').click(function () {
            userList.children('.active').removeClass('active');
            let selected = event.target;
            $(selected).addClass('active');
            setCurrentRecipient(selected.text);
        });
    });
}


function updateFriendList() {
    $.getJSON('http://127.0.0.1:8000/accounts/api/v1/friendlist/', function (data) {
        userList.children('.user').remove();
        // console.log(data)
        for (let i = 0; i < data.friends.length; i++) {
            const userItem = `<a class="list-group-item user">${data.friends[i]['user']}</a>`;
            $(userItem).appendTo('#user-list');
        }
        $('.user').click(function () {
            userList.children('.active').removeClass('active');
            let selected = event.target;
            $(selected).addClass('active');
            setCurrentRecipient(selected.text);
        });
    });
}

function drawMessage(message) {
    let position = 'left';
    const date = new Date(message.timestamp);
    if (message.owner === currentUser) position = 'right';
    const messageItem = `
            <li class="message ${position}">
                <div class="avatar">${message.owner}</div>
                    <div class="text_wrapper">
                        <div class="text">${message.body}<br>
                            <span class="small">${date}</span>
                    </div>
                </div>
            </li>`;
    $(messageItem).appendTo('#messages');
}

function getConversation(recipient) {
    $.getJSON(`http://127.0.0.1:8000/chat/api/v1/message/?target=${recipient}`, function (data) {
        messageList.children('.message').remove();
        for (let i = data['results'].length - 1; i >= 0; i--) {
            drawMessage(data['results'][i]);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });

}

function getMessageById(message) {
    const id = JSON.parse(message).message;
    $.getJSON(`http://127.0.0.1:8000/chat/api/v1/message/${id}/`, function (data) {
        if (data.owner === currentRecipient ||
            (data.recipient === currentRecipient && data.owner == currentUser)) {
            console.log(data)
            drawMessage(data);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });
}

function sendMessage(recipient, body) {
    $.post('http://127.0.0.1:8000/chat/api/v1/message/', {
        recipient: recipient,
        body: body
    }).fail(function () {
        alert('Error! Check console!');
    });
}

function setCurrentRecipient(username) {
    currentRecipient = username;
    getConversation(currentRecipient);
    enableInput();
}


function enableInput() {
    chatInput.prop('disabled', false);
    chatButton.prop('disabled', false);
    chatInput.focus();
}

function disableInput() {
    chatInput.prop('disabled', true);
    chatButton.prop('disabled', true);
}

$(document).ready(function () {
    updateFriendList();
    disableInput();

//    let socket = new WebSocket(`ws://127.0.0.1:8000/?session_key=${sessionKey}`);
    var socket = new WebSocket(
        'ws://' + window.location.host +
        '/ws?session_key=' + `${sessionKey}` + '/')

    chatInput.keypress(function (e) {
        if (e.keyCode == 13)
            chatButton.click();
    });

    chatButton.click(function () {
        if (chatInput.val().length > 0) {
            sendMessage(currentRecipient, chatInput.val());
            // socket.send(JSON.stringify({
            //     'message': chatInput.val()
            // }))
            chatInput.val('');
        }
    });

    socket.onmessage = function (e) {
        getMessageById(e.data);
    };
});