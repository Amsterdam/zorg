# Python
import datetime
# Package
from django.contrib.gis.db import models as geo
from django.contrib.postgres.fields import JSONField
from django.db import models
# Project
from datasets.general import events
from datasets.general.mixins import EventLogMixin


class Persoon(models.Model):
    guid = models.CharField(max_length=255, primary_key=True)
    contact = JSONField()  # See organisation for example
    naam = models.CharField(max_length=255)


class PersoonEventLog(EventLogMixin):
    ref_model = Persoon


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
    id = models.CharField(max_length=100)
    guid = models.CharField(max_length=255, primary_key=True)
    naam = models.CharField(max_length=255)
    beschrijving = models.CharField(max_length=255)
    afdeling = models.CharField(max_length=255)
    contact = JSONField()  # for tele, fax, emai, www etc.


class OrganisatieEventLog(EventLogMixin):
    ref_model = Organisatie


class Activiteit(models.Model):
    guid = models.CharField(max_length=255, primary_key=True)
    naam = models.CharField(max_length=255)
    beschrijving = models.TextField()
    bron_link = models.URLField()
    contactpersoon = models.CharField(max_length=255)
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


class ActiviteitEventLog(EventLogMixin):
    ref_model = Activiteit


class Locatie(models.Model):
    guid = models.CharField(max_length=255, primary_key=True)
    naam = models.CharField(max_length=255)
    openbare_ruimte_naam = models.CharField(max_length=255)
    huisnummer = models.CharField(max_length=5)
    huisletter = models.CharField(max_length=1)
    huisnummer_toevoeging = models.CharField(max_length=4)
    bag_link = models.URLField()

    objects = geo.GeoManager()


class LocatieEventLog(EventLogMixin):
    ref_model = Locatie


