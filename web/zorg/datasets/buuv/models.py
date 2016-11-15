# Python
import datetime
# Package
import requests
import json
from requests.auth import HTTPBasicAuth
from django.db import models
import os


class Buuv(models.Model):
    id = models.IntegerField(primary_key=True)
    titel = models.CharField(max_length=255)
    type = models.Charfield(max_length=10)
    omschrijving = models.TextField()
    deelnemer = models.CharField(max_length=255)
    aangemaakt = models.DateTimeField()
    gewijzigd = models.DateTimeField()
    gemeente = models.CharField(max_length=255)
    stadsdeel = models.CharField(max_length=255)
    buurt = models.CharField(max_length=255)

    class Meta(object):
        verbose_name = "API data Buuv"
        verbose_name_plural = "Buuv data"

    def __str__(self) -> str:
        return self.titel

    def import_data(self):
        """
        Import BUUV api data
        query keys for the buuv api url
        # k = key
        # z = zipcode (uppercase)
        # d = distance max=40
        # q = search
        # since = time "2015-12-21T12:16:05Z"

        :return:
        """
        url = "https://api.buuv.org/?k={}&z=1078BG&d=30&q=e".format(os.getenv('APIKEY', 'insecure'))
        res = requests.get(url, auth=HTTPBasicAuth(os.getenv('USER', 'user'), os.getenv('PASS')),
                           headers={'Content-Type': 'text/json'})
        data = []
        if res.status_code == 200:
            # de json string is verborgen in een XML doc, vind de eerste `[` en neem alle tekst tot de laatste `]`
            data = json.loads(str(res.content)[str(res.content).find('['):str(res.content).rfind(']') + 1])
        res.raise_for_status()

        for row in data:
            r = self.model()
            r.id = row['ID']
            r.titel = row['Titel']
            r.type = row['Type']
            r.omschrijving = row['Omschriiving']
            r.deelnemer = row['Deelnemer']
            r.aangemaakt = row['Aangemaakt']
            r.gewijzigd = row['gewijzigd']
            r.gemeente = row['Gemeente']
            r.stadsdeel = row['Stadsdeel']
            r.buurt = row['Buurt']
            r.save()
