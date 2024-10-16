from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_chatroom, name="create_chatroom"),
    path("join/", views.join_chatroom, name="join_chatroom"),
    path("my_chats/", views.my_chats, name="my_chats"),
    path("<str:room_name>/", views.chat_room, name="chat_room"),
    path("api/usernames/", views.get_usernames, name="get_usernames"),
    path("api/user_rooms/", views.get_user_rooms, name="get_user_rooms"),
]
