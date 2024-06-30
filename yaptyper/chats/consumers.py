from socketio_server import sio


async def websocket_app(scope, receive, send):
    await sio.handle_request(scope, receive=receive, send=send)
