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

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.conf import settings
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
        self.assertEqual(response.data['guid'], 'test-2')
        self.assertEqual(response.data['id'], '2')
        self.assertEqual(response.data['naam'], 'Ergens Anders')
        self.assertEqual(response.data['openbare_ruimte_naam'], 'Dam')
        self.assertEqual(response.data['postcode'], '1012JS')
        self.assertEqual(response.data['huisnummer'], '1')
        self.assertEqual(response.data['huisletter'], '')
        self.assertEqual(response.data['huisnummer_toevoeging'], '')
        self.assertEqual(response.data['bag_link'], f'{settings.DATAPUNT_API_URL}bag/nummeraanduiding/0363200003761447/')
        self.assertEqual(response.data['geometrie'], 'SRID=28992;POINT (121394 487383)')

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
        self.assertEqual(response.data, update_resp)

class ActiviteitenTests(APITestCase):
    loc_url = reverse('locatie-list')
    org_url = reverse('organisatie-list')
    url = reverse('activiteit-list')

    @classmethod
    def setUpTestData(cls):
        cls.user = factories.create_user()
        cls.token = factories.create_token(cls.user.auth_user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + cls.token.key)

        # Creating organisation
        cls.org = factories.create_organisate()
        response = client.post(cls.org_url, cls.org)
        cls.org['guid'] = response.data['guid']
        # Creating location
        cls.loc = factories.create_locatie()
        response = client.post(cls.loc_url, cls.org)
        cls.loc['guid'] = response.data['guid']

    def _get_client(self, token):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return client

    def test_create_activiteiten(self):
        client = self._get_client(self.token)

        act = factories.create_activiteit()
        response = client.post(self.url, act)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'guid': 'test-1', 'locatie_id': None, 'organisatie_id': None, 'id': '1',
            'naam': 'Activiteit', 'beschrijving': 'Dingen doen', 'bron_link': 'http://amsterdam.nl',
            'contactpersoon': 'Ik', 'tags': '', 'start_time': None, 'end_time': None, 'persoon': []}
        )

        act = factories.create_activiteit(naam='Doe nog eens wat',
                                          id=2, bron_link='http://amsterdam.nl/actie',
                                          locatie_id=self.loc['guid'])
        response = client.post(self.url, act)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'guid': 'test-2', 'locatie_id': 'test-1', 'organisatie_id': None, 'id': '2',
            'naam': 'Doe nog eens wat', 'beschrijving': 'Dingen doen', 'bron_link': 'http://amsterdam.nl/actie',
            'contactpersoon': 'Ik', 'tags': '', 'start_time': None, 'end_time': None, 'persoon': []}
        )

    def test_add_location_to_activiteit(self):
        client = self._get_client(self.token)

        act = factories.create_activiteit()
        response = client.post(self.url, act)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Adding the loc to the org
        response = client.put(f"{self.org_url}{self.org['guid']}/", {'id': '1', 'locatie_id': response.data['guid']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        update_resp = response.data
        response = client.get(f"{self.org_url}{self.org['guid']}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, update_resp)
