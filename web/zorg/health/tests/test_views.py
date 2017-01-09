# Packages
from django.test import TestCase
from django.test import Client


class StatusViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_status_health(self):
        """check health url"""
        response = self.client.get('/status/health')
        # Making sure its a 200
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Health OK')

    def test_status_data(self):
        """check data status url"""
        response = self.client.get('/status/data')
        # Making sure its a 200
        self.assertEqual(response.status_code, 200)
