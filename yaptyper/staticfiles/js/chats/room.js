document.addEventListener('DOMContentLoaded', () => {
    const roomName = "{{ room_name }}";
    // const username = localStorage.getItem("username");
    const username = 'USER 12';
    const socket = io.connect('http://localhost:8000', {
        transports: ['websocket'],
        upgrade: false
    });

    socket.on('connect', () => {
        console.log('Connected to server');
        const chatLog = document.getElementById('chat-log');
        chatLog.value += `${username} joined the room \n`;
        socket.emit('join', { room: roomName });
    });

    socket.on('message', (data) => {
        console.log('Received message:', data);
        const chatLog = document.getElementById('chat-log');
        chatLog.value += `${username}: ${data.message} \n`;
    });

    socket.on('connect_error', (error) => {
        console.error('Connection error:', error);
    });

    document.getElementById('chat-message-submit').onclick = () => {
        const messageInput = document.getElementById('chat-message-input');
        const message = messageInput.value;
        socket.emit('message', { room: roomName, message: message });
        messageInput.value = '';
    };

    document.getElementById('chat-message-input').addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          document.getElementById("chat-message-submit").click();
        }
      });

    document.getElementById('leave-room').onclick = () => {
        socket.emit('leave', { room: roomName });
    };
});