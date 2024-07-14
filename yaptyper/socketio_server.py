import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yaptyper.settings")
django.setup()

import socketio
import eventlet
from django.core.wsgi import get_wsgi_application
from chats.models import Chat
from chat_messages.models import ChatMessage

sio = socketio.Server(async_mode="eventlet")
usernames = {}
user_colors = {}


def generate_random_color():
    import random

    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
def disconnect(sid):
    print("disconnect ", sid)
    username = usernames.pop(sid, "Unknown user")
    rooms = sio.rooms(sid)
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
    room_name = data["room"]
    username = data["username"]
    usernames[sid] = username
    user_colors[sid] = generate_random_color()

    chat, created = Chat.objects.get_or_create(room_name=room_name)

    previous_messages = chat.get_messages()
    for message in previous_messages:
        sio.emit(
            "message",
            {
                "username": message.nick_name,
                "message": message.text,
                "color": user_colors.get(sid, "#000000"),
            },
            room=sid,
        )

    sio.enter_room(sid, room_name)
    sio.emit(
        "message",
        {
            "username": "INFO",
            "message": f"{username} has entered the room.",
            "color": user_colors[sid],
        },
        room=room_name,
        skip_sid=sid,
    )


@sio.on("message")
def message(sid, data):
    room_name = data["room"]
    username = usernames.get(sid, "Unknown user")
    color = user_colors.get(sid, "#000000")

    chat = Chat.objects.get(room_name=room_name)
    ChatMessage.objects.create(chat=chat, nick_name=username, text=data["message"])

    sio.emit(
        "message",
        {"username": username, "message": data["message"], "color": color},
        room=room_name,
    )


@sio.on("leave")
def leave(sid, data):
    room_name = data["room"]
    username = data["username"]
    sio.leave_room(sid, room_name)
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


django_app = get_wsgi_application()
app = socketio.WSGIApp(sio, django_app)

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 8000)), app)
