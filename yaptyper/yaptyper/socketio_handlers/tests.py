from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock

from chats.models import Chat
from chat_messages.models import ChatMessage
from .events import disconnect, join, message, leave, usernames, user_rooms, usernames, user_colors, user_rooms


class SocketIOTestCase(TestCase):
    def setUp(self):
        self.sid = 'test_sid'
        self.password = 'test_password'
        self.room = 'test_room'
        self.user = User.objects.create_user(
            username="test_user",
            password="pass123")
        self.chat = Chat.objects.create(
            room_name=self.room,
            created_by=self.user
        )
        usernames[self.sid] = self.user
        user_rooms[self.user] = self.room

    @patch('yaptyper.socketio_handlers.events.sio')
    def test_disconnect(self, mock_sio):
        mock_sio.rooms.return_value = [self.room]
        disconnect(self.sid)

        self.assertNotIn(self.sid, usernames)
        mock_sio.leave_room.assert_called_once_with(self.sid, self.room)
        mock_sio.emit.assert_called_once_with(
            "message",
            {
                "username": "INFO",
                "message": f"{self.user} has left the room.",
                "color": "#FF0000",
            },
            room=self.room,
            skip_sid=self.sid
        )
    
    @patch('yaptyper.socketio_handlers.events.sio')
    @patch('yaptyper.socketio_handlers.events.generate_random_color')
    def test_join_success(self, mock_generate_color, mock_sio):
        mock_generate_color.return_value = '#FFFFFF'
        mock_sio.enter_room = MagicMock()
        mock_sio.emit = MagicMock()

        data = {
            'room': self.room,
            'username': self.user,
            'password': self.password
        }

        join(self.sid, data)

        self.assertEqual(usernames[self.sid], self.user)
        self.assertEqual(user_colors[self.sid], '#FFFFFF')
        self.assertEqual(user_rooms[self.user], self.room)

        mock_sio.enter_room.assert_called_once_with(self.sid, self.room)
        mock_sio.emit.assert_called_with(
            "message",
            {
                "username": "INFO",
                "message": f"{self.user} has entered the room.",
                "color": "#005700",
            },
            room=self.room,
            skip_sid=self.sid
        )

    @patch('yaptyper.socketio_handlers.events.sio')
    def test_join_room_does_not_exist(self, mock_sio):
        mock_sio.emit = MagicMock()
        data = {
            'room': 'non_existent_room',
            'username': self.user,
            'password': self.password
        }

        join(self.sid, data)

        mock_sio.emit.assert_called_once_with(
            "message",
            {
                "username": "INFO",
                "message": "Room does not exist.",
                "color": "#FF0000",
            },
            room=self.sid
        )

    @patch('yaptyper.socketio_handlers.events.sio')
    @patch('yaptyper.socketio_handlers.events.timezone')
    def test_message(self, mock_timezone, mock_sio):
        mock_now = timezone.now()
        mock_timezone.now.return_value = mock_now

        message_text = "Hello, world!"
        data = {
            'room': self.room,
            'message': message_text
        }
        message(self.sid, data)

        saved_message = ChatMessage.objects.filter(chat=self.chat).first()
        self.assertIsNotNone(saved_message)
        self.assertEqual(saved_message.nick_name, self.user.username)
        self.assertEqual(saved_message.text, message_text)
        self.assertEqual(saved_message.message_time, mock_now)

        mock_sio.emit.assert_called_once_with(
            "message",
            {
                "username": self.user,
                "message": message_text,
                "color": '#FFFFFF',
                "message_time": mock_now.strftime("%Y-%m-%d %H:%M"),
            },
            room=self.room
        )

    @patch('yaptyper.socketio_handlers.events.sio')
    def test_message_room_not_found(self, mock_sio):
        non_existent_room = 'non_existent_room'
        data = {
            'room': non_existent_room,
            'message': "This should not be sent"
        }
        with self.assertRaises(Chat.DoesNotExist):
            message(self.sid, data)
        mock_sio.emit.assert_not_called()
        self.assertEqual(ChatMessage.objects.count(), 0)

    @patch('yaptyper.socketio_handlers.events.sio')
    def test_leave(self, mock_sio):
        mock_sio.emit = MagicMock()
        data = {
            'room': self.room,
            'username': self.user
        }
        leave(self.sid, data)

        self.assertNotIn(self.user, user_rooms)
        mock_sio.leave_room.assert_called_once_with(self.sid, self.room)
        mock_sio.emit.assert_called_once_with(
            "message",
            {
                "username": "INFO",
                "message": f"{self.user} has left the room.",
                "color": "#FF0000",
            },
            room=self.room,
            skip_sid=self.sid
        )
