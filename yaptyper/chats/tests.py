from urllib import request
from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import ChatRoomForm, JoinRoomForm
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

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='pass123')
        self.chat = Chat.objects.create(room_name='testroom', created_by=self.user)

    def test_index_view(self):
        """
        Test if the index view returns a 200 status code and uses the correct template.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chats/index.html')

    def test_create_chatroom_view(self):
        """
        Test if a logged-in user can create a new chat room.
        Check if the view redirects after successful creation and if the room is actually created in the database.
        """
        self.client.login(username='test_user', password='pass123')
        data = {'room_name': 'newroom', 'password': 'roompass'}
        response = self.client.post(reverse('create_chatroom'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Chat.objects.filter(room_name='newroom').exists())

    def test_join_chatroom_view(self):
        """
        Test if the join chatroom view handles a POST request correctly.
        This test assumes the view renders the form again on GET request.
        """
        data = {'room_name': 'testroom', 'password': ''}
        response = self.client.post(reverse('join_chatroom'), data=data)
        self.assertEqual(response.status_code, 302)

    def test_chat_room_view(self):
        """
        Test if a logged-in user can access a specific chat room.
        Check if the correct template is used and the response status is 200.
        """
        self.client.login(username='test_user', password='pass123')
        response = self.client.get(reverse('chat_room', args=['testroom']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chats/room.html')

    def test_my_chats_view(self):
        """
        Test if a logged-in user can access their chat rooms list.
        Verify that the correct template is used and the response status is 200.
        """
        self.client.login(username='test_user', password='pass123')
        response = self.client.get(reverse('my_chats'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chats/my_chats.html')

    def test_get_usernames_view(self):
        """
        Test if the get_usernames API endpoint returns a JSON response with status 200.
        """
        response = self.client.get(reverse('get_usernames'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_get_user_rooms_view(self):
        """
        Test if the get_user_rooms API endpoint returns a JSON response with status 200.
        """
        response = self.client.get(reverse('get_user_rooms'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

class FormTest(TestCase):
    def test_chatroom_form(self):
        """
        Test if the ChatRoomForm is valid with correct data.
        """
        form = ChatRoomForm(data={'room_name': 'testroom', 'password': 'roompass'})
        self.assertTrue(form.is_valid())

    def test_chatroom_form_invalid(self):
        """
        Test if the ChatRoomForm is invalid with incorrect data.
        """
        form = ChatRoomForm(data={'room_name': '', 'password': 'roompass'})
        self.assertFalse(form.is_valid())

    def join_room_form(self):
        """
        Test if the JoinRoomForm is valid with correct data.
        """
        form = JoinRoomForm(data={'room_name': 'testroom', 'password': 'roompass'})
        self.assertTrue(form.is_valid())

    def join_room_form_invalid(self):
        """
        Test if the JoinRoomForm is invalid with incorrect data.
        """
        form = JoinRoomForm(data={'room_name': '', 'password': 'roompass'})
        self.assertFalse(form.is_valid())

class URLTests(TestCase):
    """
    Test if all URLs are accessible.
    """
    def test_index_url(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_create_chatroom_url(self):
        response = self.client.get(reverse('create_chatroom'))
        self.assertEqual(response.status_code, 302)

    def test_join_chatroom_url(self):
        response = self.client.get(reverse('join_chatroom'))
        self.assertEqual(response.status_code, 200)

    def test_my_chats_url(self):
        response = self.client.get(reverse('my_chats'))
        self.assertEqual(response.status_code, 302)

    def test_chat_room_url(self):
        response = self.client.get(reverse('chat_room', args=['testroom']))
        self.assertEqual(response.status_code, 302)

    def test_get_usernames_url(self):
        response = self.client.get(reverse('get_usernames'))
        self.assertEqual(response.status_code, 200)

    def test_get_user_rooms_url(self):
        response = self.client.get(reverse('get_user_rooms'))
        self.assertEqual(response.status_code, 200)


class APIViewsTestCase(TestCase):
    """
    Test API views.
    """
    def setUp(self):
        self.client = Client()

    def test_get_usernames(self):
        response = self.client.get(reverse('get_usernames'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_get_user_rooms(self):
        response = self.client.get(reverse('get_user_rooms'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')


class TestTemplates(TestCase):
    """
    Test if all templates are rendered correctly.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='pass123')
        self.client = Client()
        self.client.login(username='test_user', password='pass123')
        self.chat = Chat.objects.create(room_name="Test_Room", created_by=self.user)

    def test_index_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chats/index.html')

    def test_create_chatroom_template(self):
        response = self.client.get(reverse('create_chatroom'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chats/create_chatroom.html')

    def test_join_chatroom_template(self):
        response = self.client.get(reverse('join_chatroom'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chats/join_chatroom.html')

    def test_my_chats_template(self):
        response = self.client.get(reverse('my_chats'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chats/my_chats.html')

    def test_chat_room_template(self):
        response = self.client.get(reverse('chat_room', args=['Test_Room']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chats/room.html')

    def test_chat_room_template_invalid(self):
        response = self.client.get(reverse('chat_room', args=['Invalid_Room']))
        self.assertEqual(response.status_code, 404)