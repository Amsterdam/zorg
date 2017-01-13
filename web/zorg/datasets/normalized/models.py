# Python
import datetime
import logging
# Package
from django.contrib.gis.db import models as geo
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
import requests
# Project
from datasets.general import events
from datasets.general.mixins import EventLogMixin, ReadOptimizedModel
from datasets.normalized import documents


log = logging.getLogger(__name__)
bag_url = "https://api.datapunt.amsterdam.nl/bag/nummeraanduiding/?"


class Persoon(models.Model):
    guid = models.CharField(max_length=255, primary_key=True)
    contact = JSONField()  # See organisation for example
    naam = models.CharField(max_length=255)


class PersoonEventLog(EventLogMixin):
    read_model = Persoon


class Organisatie(ReadOptimizedModel):
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
    create_doc = documents.doc_from_organisatie

    id = models.CharField(max_length=100)
    guid = models.CharField(max_length=255, primary_key=True)
    naam = models.CharField(max_length=255)
    beschrijving = models.CharField(max_length=255, blank=True)
    afdeling = models.CharField(max_length=255, blank=True)
    contact = JSONField()  # for tele, fax, emai, www etc.

    def __repr__(self):
        return f'<{self.naam}>'


class OrganisatieEventLog(EventLogMixin):
    read_model = Organisatie


class Locatie(ReadOptimizedModel):
    create_doc = documents.doc_from_locatie

    id = models.CharField(max_length=100)
    guid = models.CharField(max_length=255, primary_key=True)
    naam = models.CharField(max_length=255)
    openbare_ruimte_naam = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=6, blank=True)
    huisnummer = models.CharField(max_length=5, blank=True)
    huisletter = models.CharField(max_length=1, blank=True)
    huisnummer_toevoeging = models.CharField(max_length=32, blank=True)
    bag_link = models.URLField(blank=True)
    geometrie = geo.PointField(null=True, srid=28992, blank=True)

    objects = geo.GeoManager()

    def save(self, *args, **kwargs):
        # Finding the bag object
        try:
            postcode = f'postcode={self.postcode}'
            if self.huisnummer:
                huisnummer = f'&huisnummer={self.huisnummer}'
            else:
                huisnummer = ''
            self.bag_link = requests.get(f'{bag_url}{postcode}{huisnummer}').json()['results'][0]['_links']['self']['href']
        except IndexError:
            # No results found
            self.bag_link = ''
        except Exception as exp:
            log.error(repr(exp))
        # If no geolocation is geven, retrivint that as well
        try:
            if not self.geometrie and self.bag_link:
                geo = requests.get(self.bag_link).json()['_geometrie']
                point = Point(geo['coordinates'], srid=28992)
                self.geometrie = point
        except Exception as exp:
            log.error(repr(exp))

        # Saving
        return super(Locatie, self).save(*args, **kwargs)

    def clean(self):
        # Either an addres or a point
        if not self.geometrie and not self.postcode:
            raise ValidationError('A geolocation or address is needed')

    def __repr__(self):
        return f'<{self.naam}>'


class LocatieEventLog(EventLogMixin):
    read_model = Locatie

    def save(self, *args, **kwargs):
        # Setting sequence
        try:
            prev = LocatieEventLog.objects.filter(guid=self.guid).order_by('-sequence')[0]
            self.sequence = prev.sequence + 1
        except IndexError:
            self.sequence = 0
        except Exception as exp:
            log.error(repr(exp))
            self.sequence = 0
        # Saving
        return super(LocatieEventLog, self).save(args, kwargs)


class Activiteit(ReadOptimizedModel):
    create_doc = documents.doc_from_activiteit

    id = models.CharField(max_length=100)
    guid = models.CharField(max_length=255, primary_key=True)
    naam = models.CharField(max_length=255)
    beschrijving = models.TextField(blank=True)
    bron_link = models.URLField()
    contactpersoon = models.CharField(max_length=255, blank=True)
    persoon = models.ManyToManyField(to=Persoon, related_name='activiteiten', blank=True)
    tags = models.CharField(max_length=255)
    locatie = models.ForeignKey(Locatie, related_name='activiteiten')
    organisatie = models.ForeignKey(Organisatie, related_name='activiteiten')

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

    def __repr__(self):
        return f'<{self.naam} {self.guid}>'


class ActiviteitEventLog(EventLogMixin):
    read_model = Activiteit

    def save(self, *args, **kwargs):
        # Setting sequence
        try:
            prev = ActiviteitEventLog.objects.filter(guid=self.guid).order_by('-sequence')[0]
            self.sequence = prev.sequence + 1
        except IndexError:
            self.sequence = 0
        except Exception as exp:
            log.error(repr(exp))
            self.sequence = 0
        # Saving
        return super(ActiviteitEventLog, self).save(args, kwargs)
