from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request, username):
    return render(request, "chats/index.html", {"username": username})


@login_required
def room(request, room_name):
    return render(
        request,
        "chats/room.html",
        {"room_name": room_name, "username": request.user.username},
    )
