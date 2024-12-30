from datetime import datetime
from zoneinfo import ZoneInfo
from django.test import TestCase

from .models import ChatMessage
from chats.models import Chat
from django.contrib.auth.models import User

class ChatMessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            password="pass123"
        )
        self.chat = Chat.objects.create(room_name="test_room", created_by=self.user)
        self.chat_message = ChatMessage.objects.create(
            chat=self.chat, nick_name="test_user", text="test_message", message_time=datetime(2024,12,23,0,0, tzinfo=ZoneInfo("UTC"))
        )

    def test_chat_message_creation(self):
        """Tests if ChatMessage was created correctly"""
        self.assertEqual(self.chat_message.chat.room_name, "test_room")
        self.assertEqual(self.chat_message.nick_name, "test_user")
        self.assertEqual(self.chat_message.text, "test_message")
        self.assertEqual(self.chat_message.message_time, datetime(2024,12,23,0,0, tzinfo=ZoneInfo("UTC")))

    def test_chat_message_str_method(self):
        """Tests __str__ method of ChatMessage model"""
        self.assertEqual(str(self.chat_message), "test_room-test_user")
