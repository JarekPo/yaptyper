from django.shortcuts import render


def index(request, username):
    return render(request, "chats/index.html", {"username": username})


def room(request, room_name):
    return render(request, "chats/room.html", {"room_name": room_name})
