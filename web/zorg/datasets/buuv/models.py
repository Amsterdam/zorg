# Python
import datetime
# Package
import requests
from django.db import models


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
        verbose_name_plural = "Woonplaatsen"

    def __str__(self) -> str:
        return self.titel

# k = key
# z = zipcode (uppercase)
# d = distance max=40
# q = search
# since = time "2015-12-21T12:16:05Z"