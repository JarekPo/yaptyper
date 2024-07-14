import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yaptyper.settings")
django.setup()

import socketio
import eventlet
from django.core.wsgi import get_wsgi_application

sio = socketio.Server(async_mode="eventlet")
usernames = {}


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
            {"username": "INFO", "message": f"{username} has left the room."},
            room=room,
            skip_sid=sid,
        )


@sio.on("join")
def join(sid, data):
    room = data["room"]
    username = data["username"]
    usernames[sid] = username
    sio.enter_room(sid, room)
    sio.emit(
        "message",
        {"username": "INFO", "message": f"{username} has entered the room."},
        room=room,
        skip_sid=sid,
    )


@sio.on("message")
def message(sid, data):
    room = data["room"]
    username = usernames.get(sid, "Unknown user")
    sio.emit("message", {"username": username, "message": data["message"]}, room=room)


@sio.on("leave")
def leave(sid, data):
    room = data["room"]
    username = data["username"]
    sio.leave_room(sid, room)
    sio.emit(
        "message",
        {"username": "INFO", "message": f"{username} has left the room."},
        room=room,
        skip_sid=sid,
    )


django_app = get_wsgi_application()
app = socketio.WSGIApp(sio, django_app)

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 8000)), app)
