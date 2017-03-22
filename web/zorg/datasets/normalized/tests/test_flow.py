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

class OrganisatieTests(APITestCase):
    url = reverse('organisatie-list')

    @classmethod
    def setUpTestData(cls):
        cls.user = factories.create_user()
        cls.token = factories.create_token(cls.user.auth_user)

    def _get_client(self, token):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return client

    def test_create_organisaties(self):
        client = self._get_client(self.token)

        org = factories.create_organisate()
        response = client.post(self.url, org)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'guid': 'test-1', 'id': '1', 'naam': 'Org',
            'beschrijving': 'Dit is een lang verhaal', 'afdeling': '', 'contact': {'tel': '123'}, 'locatie_id': None}
        )

        org = factories.create_organisate(naam='Andere Org', id=2)
        response = client.post(self.url, org)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'guid': 'test-2', 'id': '2', 'naam': 'Andere Org',
            'beschrijving': 'Dit is een lang verhaal', 'afdeling': '', 'contact': {'tel': '123'}, 'locatie_id': None}
        )

    def test_unique_name_constrain(self):
        """
        Test that a same name org is not created
        """
        client = self._get_client(self.token)

        org = factories.create_organisate()
        response = client.post(self.url, org)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'guid': 'test-1', 'locatie_id': None, 'id': '1', 'naam': 'Org',
            'beschrijving': 'Dit is een lang verhaal', 'afdeling': '', 'contact': {'tel': '123'}}
        )

        org = factories.create_organisate(naam='Org', id=2)
        response = client.post(self.url, org)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_organisatie_information(self):
        client = self._get_client(self.token)

        org = factories.create_organisate()
        response = client.post(self.url, org)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'guid': 'test-1', 'id': '1', 'naam': 'Org',
            'beschrijving': 'Dit is een lang verhaal', 'afdeling': '', 'contact': {'tel': '123'}, 'locatie_id': None}
        )

        response = client.put(f"{self.url}{response.data['guid']}/", {'id': '1', 'naam':' Nieuwe naam'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'guid': 'test-1', 'id': '1', 'naam': 'Nieuwe naam',
            'beschrijving': 'Dit is een lang verhaal', 'afdeling': '', 'contact': {'tel': '123'}, 'locatie_id': None}
        )


class LocatieTests(APITestCase):
    url = reverse('locatie-list')
    org_url = reverse('organisatie-list')

    @classmethod
    def setUpTestData(cls):
        cls.user = factories.create_user()
        cls.token = factories.create_token(cls.user.auth_user)
        cls.org = factories.create_organisate()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + cls.token.key)
        response = client.post(cls.org_url, cls.org)
        cls.org['guid'] = response.data['guid']

    def _get_client(self, token):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return client

    def test_create_locations(self):
        client = self._get_client(self.token)

        loc = factories.create_locatie(huisletter='A')
        response = client.post(self.url, loc)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'guid': 'test-1', 'id': '1', 'naam': 'Loc', 'openbare_ruimte_naam': 'Straat',
            'postcode': '1111AA', 'huisnummer': '1', 'huisletter': 'A', 'huisnummer_toevoeging': '',
            'bag_link': '', 'geometrie': None}
        )

        loc = factories.create_locatie(naam='Ergens Anders', id=2, postcode='1012JS', openbare_ruimte_naam='Dam')
        response = client.post(self.url, loc)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'guid': 'test-2', 'id': '2', 'naam': 'Ergens Anders',
            'openbare_ruimte_naam': 'Dam', 'postcode': '1012JS', 'huisnummer': '1', 'huisletter': '',
            'huisnummer_toevoeging': '', 'bag_link': 'https://api.datapunt.amsterdam.nl/bag/nummeraanduiding/03630003761447/',
            'geometrie': 'SRID=28992;POINT (121394 487383)'}
        )

    def test_add_location_to_org(self):
        client = self._get_client(self.token)

        loc = factories.create_locatie()
        response = client.post(self.url, loc)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Adding the loc to the org
        response = client.put(f"{self.org_url}{self.org['guid']}/", {'id': '1', 'locatie_id': response.data['guid']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        update_resp = response.data
        response = client.get(f"{self.org_url}{self.org['guid']}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(response.data, update_resp)
