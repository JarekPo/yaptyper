from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.db import IntegrityError
from .forms import ChatRoomForm, JoinRoomForm
from .models import Chat
from .users_data import usernames


def index(request, username):
    return render(request, "chats/index.html", {"username": username})


@login_required
def room(request, room_name):
    return render(
        request,
        "chats/room.html",
        {"room_name": room_name, "username": request.user.username},
    )


@login_required(login_url="/login/")
def create_chatroom(request):
    if request.method == "POST":
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.created_by = request.user
            chat.room_name = chat.room_name.lower()
            if chat.password:
                chat.password = make_password(chat.password)
            try:
                chat.save()
            except IntegrityError:
                form.add_error("room_name", "Room name already exists")
                return render(request, "chats/create_chatroom.html", {"form": form})
            return redirect("chat_room", room_name=chat.room_name)
    else:
        form = ChatRoomForm()
    return render(request, "chats/create_chatroom.html", {"form": form})


def join_chatroom(request):
    if request.method == "POST":
        form = JoinRoomForm(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data["room_name"].lower()
            password = form.cleaned_data["password"]

            try:
                chat = Chat.objects.get(room_name__iexact=room_name)
                if chat.password and not check_password(password, chat.password):
                    form.add_error("password", "Incorrect password")
                else:
                    return redirect("chat_room", room_name=room_name)
            except Chat.DoesNotExist:
                form.add_error("room_name", "Room does not exist")
    else:
        form = JoinRoomForm()
    return render(request, "chats/join_chatroom.html", {"form": form})


@login_required(login_url="/login/")
def chat_room(request, room_name):
    chat = get_object_or_404(Chat, room_name__iexact=room_name)
    username = request.user.username
    return render(
        request,
        "chats/room.html",
        {"room_name": chat.room_name, "username": username, "SERVER": settings.SERVER},
    )


@login_required(login_url="/login/")
def my_chats(request):
    chatrooms = Chat.objects.filter(created_by=request.user)
    return render(request, "chats/my_chats.html", {"chatrooms": chatrooms})


def get_usernames(request):
    return JsonResponse(usernames)
