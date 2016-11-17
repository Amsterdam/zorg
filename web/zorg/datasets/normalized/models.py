# Python
import datetime
# Package
from django.contrib.gis.db import models as geo
from django.db import models
import requests


class Organisatie(models.Model):
    """

    Contact json example:
    {
        telefoon: {
            'main': 12345678,
            'jelink algemeen':23456789
        },
        email: {
            'main': 12345678,
            'jelink algemeen':23456789
        }
    }

    Possible contanct keys:
    telefoon, fax, email, website, mobiel
    """
    naam = models.CharField(max_length=255)
    beschrijving = models.CharField(max_length=255)
    afdeling = models.CharField(max_length=255)
    contact = models.JsonField()  # for tele, fax, emai, www etc.


class Activiteit(models.Model):
    naam = models.CharField(max_length=255)
    beschrijving = models.TextField()
    bron_link = models.URLField()
    contactpersoon = model.CharField(max_length=255)
    persoon = models.ManyToManyField(to=Persoon, related_name='activiteiten')
    tags = models.CharField(max_length=255)

    @property
    def contact(self):
        """
        Always return a Persoon object as
        a representation of the contact person
        """
        if self.persoon:
            return self.persoon
        else:
            p = Persoon()
            p.naam = self.contactpersoon
            return p


class Locatie(models.Model):
    naam = models.CharField(max_length=255)
    openbare_ruimte_naam = model.Charfield(max_length=255)
    huisnummer = models.CharField(max_length=5)
    huisletter = models.CharField(max_length=1)
    huisnummer_toevoeging = models.CharField(max_length=4)
    bag_link = models.URLField()

    objects = geo.GeoManager()


class Persoon(models.Model):
    contact = models.JsonField()  # See organisation for example

