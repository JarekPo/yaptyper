from django.test import Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class StaticFilesTest(StaticLiveServerTestCase):
    def setUp(self):
        self.client = Client()

    def test_static_files_serving(self):
        """
        Test if static files are served correctly.
        """
        styles_response = self.client.get('/static/css/dist/styles.css')
        self.assertEqual(styles_response.status_code, 200)

        scripts_response = self.client.get('/static/js/chats/main.js')
        self.assertEqual(scripts_response.status_code, 200)