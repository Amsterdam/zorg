# Python
import datetime
# Package
from django.contrib.gis.db import models as geo
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
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
    beschrijving = models.CharField(max_length=255, blank=True)
    afdeling = models.CharField(max_length=255, blank=True)
    contact = JSONField()  # for tele, fax, emai, www etc.


class OrganisatieEventLog(EventLogMixin):
    ref_model = Organisatie


class Activiteit(models.Model):
    id = models.CharField(max_length=100)
    guid = models.CharField(max_length=255, primary_key=True)
    naam = models.CharField(max_length=255)
    beschrijving = models.TextField(blank=True)
    bron_link = models.URLField()
    contactpersoon = models.CharField(max_length=255, blank=True)
    persoon = models.ManyToManyField(to=Persoon, related_name='activiteiten', blank=True)
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

    def clean(self):
        # An activity should have either a contactperson or a person
        if not self.contactpersoon and not self.persoon:
            raise ValidationError('Give either a contact person\'s name or a refrence to a person')


class ActiviteitEventLog(EventLogMixin):
    ref_model = Activiteit


class Locatie(models.Model):
    id = models.CharField(max_length=100)
    guid = models.CharField(max_length=255, primary_key=True)
    naam = models.CharField(max_length=255)
    openbare_ruimte_naam = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=6, blank=True)
    huisnummer = models.CharField(max_length=5, blank=True)
    huisletter = models.CharField(max_length=1, blank=True)
    huisnummer_toevoeging = models.CharField(max_length=4, blank=True)
    bag_link = models.URLField()
    geometrie = geo.PointField(null=True, srid=28992, blank=True)

    objects = geo.GeoManager()

    def clean(self):
        # Either an addres or a point
        if not self.geometrie and not self.postcode:
            raise ValidationError('A geolocation or address is needed')


class LocatieEventLog(EventLogMixin):
    ref_model = Locatie
