from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app_version import __version__

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
