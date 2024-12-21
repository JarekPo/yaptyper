import os
from django.core.wsgi import get_wsgi_application
import eventlet
import socketio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yaptyper.settings")
import django
django.setup()

from yaptyper.socketio_handlers import sio

django_app = get_wsgi_application()
app = socketio.WSGIApp(sio, django_app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    eventlet.wsgi.server(eventlet.listen(("", port)), app)
