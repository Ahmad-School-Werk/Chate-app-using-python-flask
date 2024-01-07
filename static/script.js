
var socket = io.connect('http://' + document.domain + ':' + location.port)
socket.on('message', function(data) {
    var chatDiv = document.getElementById('chat');
    var messageDiv = document.createElement('div');
    messageDiv.innerHTML = '<b>' + data.username + ':</b> ' + data.msg;
    chatDiv.appendChild(messageDiv);
})
socket.emit('join_room', { 'username': '{{ username }}', 'group': '{{ group }}' })
document.getElementById('message-form').onsubmit = function(e) {
    e.preventDefault();
    var messageInput = document.getElementById('message');
    var message = messageInput.value;
    socket.emit('message', { 'username': '{{ username }}', 'msg': message, 'group': '{{ group }}' });
    messageInput.value = '';
};
