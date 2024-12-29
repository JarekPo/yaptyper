from unittest.mock import Mock
from django.utils import timezone
from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app_version import __version__
from .socketio_handlers.utils import generate_random_color, get_message_color, get_message_time

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='pass123')

    def test_login_view(self):
        """
        Test if the login view returns a 200 status code and uses the correct template.
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')

    def test_logout_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Should redirect after logout
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_register_view_get(self):
        """
        Test if the register view returns a 200 status code and uses the correct template for GET request.
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')

    def test_register_view_post(self):
        """
        Test if the register view creates a new user and redirects on successful registration.
        """
        data = {
            'username': 'newuser',
            'password1': 'complex_password123',
            'password2': 'complex_password123',
        }
        response = self.client.post(reverse('register'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_home_view(self):
        """
        Test if the home view returns a 200 status code, uses the correct template, and includes the version number.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, __version__)

    def test_login_functionality(self):
        """
        Test if a user can successfully log in.
        """
        response = self.client.post(reverse('login'), {'username': 'test_user', 'password': 'pass123'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout_functionality(self):
        """
        Test if a user can successfully log out using a POST request.
        """
        self.client.login(username='test_user', password='pass123')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)


class URLTests(TestCase):
    def test_urls(self):
        """
        Test if all URLs are accessible.
        """
        urls = [
            reverse('login'),
            reverse('register'),
            reverse('home'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

class CustomFunctionsTests(SimpleTestCase):
    def test_generate_random_color(self):
        """
        Test random text color picker.
        """
        chat_text_colors = [
        "#003366",
        "#990000",
        "#5B2E91",
        "#0033CC",
        "#4B3D28",
        "#007A7A",
        "#CC6600",
        "#FF1493",
        "#6B8E23",
        "#2F4F4F",
        "#4B0082",
        "#A52A2A",
    ]
        self.assertIn(generate_random_color(), chat_text_colors)


    def test_get_message_time(self):
        """
        Test get message time.
        """
        mock_message = Mock()
        mock_message.message_time = timezone.now()
        empty_message = Mock()
        empty_message.message_time = None

        self.assertEqual(get_message_time(mock_message), mock_message.message_time.strftime("%Y-%m-%d %H:%M"))
        self.assertEqual(get_message_time(empty_message), None)


    def test_get_message_color(self):
        """
        Test get message color.
        """
        mock_message = Mock()
        mock_message.message_time = timezone.now()

        old_message = Mock()
        old_message.message_time = timezone.now() - timezone.timedelta(days=1)

        self.assertEqual(get_message_color(mock_message), "#000000")
        self.assertEqual(get_message_color(old_message), "#A9A9A9")