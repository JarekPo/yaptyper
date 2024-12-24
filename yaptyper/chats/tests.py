from django.test import TestCase
from django.contrib.auth.models import User
from .models import Chat

class ChatModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            password="pass123")
        self.chat = Chat.objects.create(room_name="Test_Room", created_by=self.user)

    def test_chat_creation(self):
        """Tests if Chat was created correctly"""
        self.assertEqual(self.chat.room_name, "test_room")
        self.assertEqual(self.chat.created_by, self.user)
        self.assertIsNone(self.chat.password)

    def test_chat_str_method(self):
        """Tests __str__ method of Chat model"""
        self.assertEqual(str(self.chat), "test_room")

    def test_get_messages(self):
        """Tests get_messages method of Chat model"""
        messages = self.chat.get_messages()
        self.assertQuerysetEqual(messages, [])

    def test_room_name_lowercase(self):
        """Tests if room_name is saved as lowercase"""
        chat = Chat.objects.create(room_name="camelCaseName", created_by=self.user)
        self.assertEqual(chat.room_name, "camelcasename")
