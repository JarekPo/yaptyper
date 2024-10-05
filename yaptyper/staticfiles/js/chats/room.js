document.addEventListener('DOMContentLoaded', () => {
    const roomName = window.roomName;
    const username = window.username;
    const password = window.roomPassword || "";

    const socket = io.connect(`https://${SERVER}/`, {
        transports: ['websocket'],
        upgrade: false
    });

    const getMessageTime = (dateTime) => {
        dateTime = new Date(dateTime);
        year = dateTime.getFullYear()
        month = dateTime.getMonth() + 1
        day = dateTime.getDate()
        hours = dateTime.getHours() + 1
        minutes = dateTime.getMinutes()
        doubleDigitMinutes = minutes > 9 ? minutes : `0${minutes}`
        
        if (new Date().getDay() === dateTime.getDay()) {
            return `${hours}:${doubleDigitMinutes}`
        }
        else
            return `${year}-${month}-${day}`
    }

    socket.on('connect', () => {
        console.log('Connected to server');
        socket.emit('join', { room: roomName, username: username, password: password });
    });

    socket.on('message', (data) => {
        console.log('Received message:', data);
        const chatLog = document.getElementById('chat-log');
        const newMessage = document.createElement("p");
        newMessage.style.color = data.color;
        newMessage.textContent = `[${getMessageTime(data.message_time)}] ${data.username}: ${data.message}`;
        chatLog.appendChild(newMessage);
        chatLog.scrollTop = chatLog.scrollHeight;
    });

    socket.on('connect_error', (error) => {
        console.error('Connection error:', error);
    });

    document.getElementById('chat-message-submit').onclick = () => {
        const messageInput = document.getElementById('chat-message-input');
        const message = messageInput.value;
        socket.emit('message', { room: roomName, message: message, username: username });
        messageInput.value = '';
    };

    document.getElementById('chat-message-input').addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            document.getElementById("chat-message-submit").click();
        }
    });

    document.getElementById('leave-room').onclick = () => {
        socket.emit('leave', { room: roomName, username: username });
    };
});
