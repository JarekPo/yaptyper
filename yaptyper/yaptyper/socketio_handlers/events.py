from django.contrib.auth.hashers import check_password
from chats.models import Chat
from chat_messages.models import ChatMessage
from django.utils import timezone
from .utils import generate_random_color, get_message_color, get_message_time
from chats.users_data import usernames, user_colors, user_rooms

import socketio


sio = socketio.Server(async_mode="eventlet", cors_allowed_origins="*")

@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
def disconnect(sid):
    print("disconnect ", sid)
    username = usernames.pop(sid, "Unknown user")
    rooms = sio.rooms(sid)
    user_rooms.pop(username, None)
    for room in rooms:
        sio.leave_room(sid, room)
        sio.emit(
            "message",
            {
                "username": "INFO",
                "message": f"{username} has left the room.",
                "color": "#FF0000",
            },
            room=room,
            skip_sid=sid,
        )


@sio.on("join")
def join(sid, data):
    room_name = data["room"].lower()
    username = data["username"]
    password = data.get("password", "")

    try:
        chat = Chat.objects.get(room_name__iexact=room_name)
        if chat.password and not check_password(password, chat.password):
            sio.emit(
                "message",
                {
                    "username": "INFO",
                    "message": "Incorrect password.",
                    "color": "#FF0000",
                },
                room=sid,
            )
            return
    except Chat.DoesNotExist:
        sio.emit(
            "message",
            {"username": "INFO", "message": "Room does not exist.", "color": "#FF0000"},
            room=sid,
        )
        return

    usernames[sid] = username
    user_colors[sid] = generate_random_color()
    user_rooms[username] = room_name
    previous_messages = chat.get_messages()
    for message in previous_messages:
        sio.emit(
            "message",
            {
                "username": message.nick_name,
                "message": message.text,
                "color": get_message_color(message),
                "message_time": get_message_time(message),
            },
            room=sid,
        )

    sio.enter_room(sid, room_name)
    sio.emit(
        "message",
        {
            "username": "INFO",
            "message": f"{username} has entered the room.",
            "color": "#005700",
        },
        room=room_name,
        skip_sid=sid,
    )


@sio.on("message")
def message(sid, data):
    room_name = data["room"].lower()
    username = usernames.get(sid, "Unknown user")
    color = user_colors.get(sid, "#000000")
    message_time = timezone.now()

    chat = Chat.objects.get(room_name__iexact=room_name)
    ChatMessage.objects.create(
        chat=chat,
        nick_name=username,
        text=data["message"],
        message_time=message_time,
    )

    sio.emit(
        "message",
        {
            "username": username,
            "message": data["message"],
            "color": color,
            "message_time": message_time.strftime("%Y-%m-%d %H:%M"),
        },
        room=room_name,
    )


@sio.on("leave")
def leave(sid, data):
    room_name = data["room"].lower()
    username = data["username"]
    sio.leave_room(sid, room_name)
    user_rooms.pop(username, None)
    sio.emit(
        "message",
        {
            "username": "INFO",
            "message": f"{username} has left the room.",
            "color": "#FF0000",
        },
        room=room_name,
        skip_sid=sid,
    )