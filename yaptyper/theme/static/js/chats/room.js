document.addEventListener('DOMContentLoaded', () => {
    const roomName = window.roomName;
    const username = window.username;
    const password = window.roomPassword || "";

    const socket = io.connect(`https://${SERVER}/`, {
        transports: ['websocket'],
        upgrade: false
    });

    const getMessageTime = (dateTimeString) => {
        const dateTime = dateTimeString === undefined ? new Date() : new Date(dateTimeString);
        const year = dateTime.getFullYear()
        const month = dateTime.getMonth() + 1
        const day = dateTime.getDate()
        const hours = dateTime.getHours()
        const minutes = dateTime.getMinutes()
        const doubleDigitMinutes = minutes > 9 ? minutes : `0${minutes}`
        const today = new Date()

        if (dateTime.toDateString() === today.toDateString()) {
            return `${hours}:${doubleDigitMinutes}`
        }
        else
            return `${year}-${month}-${day}`
    }

    const getUsersForRoom = (usersRooms, targetRoom) => {
        const usersInRoom = Object.entries(usersRooms)
          .filter(([user, room]) => room === targetRoom)
          .map(([user, room]) => user);
        return usersInRoom;
      }

    const getActiveUsers = () => {
        fetch('/chats/api/user_rooms')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const userList = document.getElementById('users-display');
            userList.innerHTML = '';
            const usersForCurrentRoom = getUsersForRoom(data, roomName);
            uniqueUsernames = new Set(usersForCurrentRoom);
            const userArray = Array.from(uniqueUsernames);
            const paragraph = document.createElement('p');
            paragraph.textContent = `[${userArray.join(', ')}]`;
            userList.appendChild(paragraph);
        })
        .catch(error => console.error('Error fetching user_rooms:', error));
            }

    socket.on('connect', () => {
        console.log('Connected to server');
        socket.emit('join', { room: roomName, username: username, password: password });
        getActiveUsers();
    });

    socket.on('disconnect', () => {
        socket.emit('disconnect', { room: roomName, username: username, password: password });
        getActiveUsers();
    });

    socket.on('message', (data) => {
        const chatLog = document.getElementById('chat-log');
        const newMessage = document.createElement("p");
        newMessage.style.color = data.color;
        newMessage.textContent = `[${getMessageTime(data.message_time)}] ${data.username}: ${data.message}`;
        chatLog.appendChild(newMessage);
        chatLog.scrollTop = chatLog.scrollHeight;
        if (data.username === 'INFO') {
            getActiveUsers();
        }
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
        getActiveUsers();
    };
});
