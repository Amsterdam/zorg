"""
Test the flow of the app. Steps taken:

- Create a user
- Create a token
- Add 2 orgs
- Check guid
- Create 2 locations
- Check guid
- Create 2 activities
- Check guid
- Do crazy stuff
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

import datasets.normalized as normalized
from datasets.normalized.tests import factories

class BaseCreate(object):
    model = None
    url = None

    @classmethod
    def setUpTestData(cls):
        cls.user = factories.create_user()
        cls.token = factories.create_token(cls.user.auth_user)

    def _get_client(self, token):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return client

    def _create_user_and_token(self):
        user = factories.create_user()
        token = factories.create_token(user.auth_user)

        return (user, token)

    def test_create_model(self):
        client = self._get_client(self.token)

        org = factories.create_organisate()
        response = client.post(self.url, org)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'guid': 'test-1', 'id': '1', 'naam': 'Org',
            'beschrijving': 'Dit is een lang verhaal', 'afdeling': '', 'contact': {'tel': '123'}}
        )

        org = factories.create_organisate(naam='Andere Org', id=2)
        response = client.post(self.url, org)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'guid': 'test-2', 'id': '2', 'naam': 'Andere Org',
            'beschrijving': 'Dit is een lang verhaal', 'afdeling': '', 'contact': {'tel': '123'}}
        )

    def test_unique_name_constrain(self):
        """
        Test that a same name org is not created
        """
        client = self._get_client(self.token)

        org = factories.create_organisate()
        response = client.post(self.url, org)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'guid': 'test-1', 'id': '1', 'naam': 'Org',
            'beschrijving': 'Dit is een lang verhaal', 'afdeling': '', 'contact': {'tel': '123'}}
        )

        org = factories.create_organisate(naam='Org', id=2)
        response = client.post(self.url, org)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_model_information(self):
        client = self._get_client(self.token)

        org = factories.create_organisate()
        response = client.post(self.url, org)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'guid': 'test-1', 'id': '1', 'naam': 'Org',
            'beschrijving': 'Dit is een lang verhaal', 'afdeling': '', 'contact': {'tel': '123'}}
        )

        response = client.put(f"{self.url}{response.data['guid']}/", {'id': '1', 'naam':' Nieuwe naam'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'guid': 'test-1', 'id': '1', 'naam': 'Nieuwe naam',
            'beschrijving': 'Dit is een lang verhaal', 'afdeling': '', 'contact': {'tel': '123'}}
        )


class OrganisatieTests(BaseCreate, APITestCase):
    model = normalized.models.Organisatie
    url = reverse('organisatie-list')


# class LocatieTests(BaseCreate):
#     model = normalized.models.Organisatie
#     url = '/zorg/locatie/'
