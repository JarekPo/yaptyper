import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yaptyper.settings")
django.setup()

import socketio
import eventlet
from django.core.wsgi import get_wsgi_application

sio = socketio.Server(async_mode="eventlet")


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


@sio.on("join")
def join(sid, data):
    room = data["room"]
    sio.enter_room(sid, room)
    sio.emit("message", {"message": f"{sid} has entered the room."}, room=room)


@sio.on("message")
def message(sid, data):
    room = data["room"]
    sio.emit("message", {"message": data["message"]}, room=room)


django_app = get_wsgi_application()
app = socketio.WSGIApp(sio, django_app)

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 8000)), app)
