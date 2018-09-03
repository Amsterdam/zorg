from django.contrib.auth.models import User
from django.contrib.gis.db import models as geo
from django.contrib.postgres.fields import JSONField
from django.db import models


class TagDefinition(models.Model):
    """
    Predefined tags each with a category to eventually separate them in
    a front end
    """
    CATEGORIES = (
        ('BETAALD', 'Betaald'),
        ('DAG', 'Dagen'),
        ('TIJD', 'Tijdstip'),
        ('LEEFTIJDSCATEGORIE', 'Leeftijdscategorie')
    )

    naam = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=25, choices=CATEGORIES)

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name_plural = 'TagDefinitions'


class Profile(models.Model):
    """
    Contain all the non auth information about
    the user.
    """
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Contains the GUID initial code used in GUID generation
    guid = models.CharField(max_length=4, unique=True)  # prefix for related guids
    naam = models.CharField(max_length=255, unique=True)
    beschrijving = models.CharField(max_length=255, blank=True)
    afdeling = models.CharField(max_length=255, blank=True)
    contact = JSONField()  # for tele, fax, emai, www etc.

    def __str__(self):
        return self.naam


class Persoon(models.Model):
    guid = models.CharField(max_length=255, primary_key=True)
    contact = JSONField()  # See organisation for example
    naam = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Personen"

    def __str__(self):
        return self.naam


class Locatie(models.Model):

    id = models.CharField(max_length=100)
    guid = models.CharField(max_length=255, primary_key=True)
    naam = models.CharField(max_length=255)
    openbare_ruimte_naam = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=6, blank=True)
    huisnummer = models.CharField(max_length=64, blank=True)
    huisletter = models.CharField(max_length=1, blank=True)
    huisnummer_toevoeging = models.CharField(max_length=32, blank=True)
    bag_link = models.URLField(blank=True)
    geometrie = geo.PointField(null=True, srid=28992, blank=True)

    objects = geo.GeoManager()

    def __str__(self):
        return f'<{self.naam}>'

    def __repr(self):
        return f'<{self.guid}>'

    class Meta:
        verbose_name_plural = "Locaties"


class Organisatie(models.Model):

    id = models.CharField(max_length=100)
    guid = models.CharField(max_length=255, primary_key=True)
    naam = models.CharField(max_length=255, unique=True)
    beschrijving = models.CharField(max_length=255, blank=True)
    afdeling = models.CharField(max_length=255, blank=True)
    contact = JSONField()  # for tele, fax, emai, www etc.
    locatie = models.ForeignKey(Locatie, related_name='locatie', blank=True, null=True)

    def __str__(self):
        return f'<{self.naam}>'

    def __repr(self):
        return f'<{self.guid}>'

    class Meta:
        verbose_name_plural = "Organisaties"


class Activiteit(models.Model):
    es_tags = None

    id = models.CharField(max_length=100)
    guid = models.CharField(max_length=255, primary_key=True)
    naam = models.CharField(max_length=255)
    beschrijving = models.TextField(blank=True)
    bron_link = models.URLField()
    contactpersoon = models.CharField(max_length=255, blank=True)
    persoon = models.ManyToManyField(to=Persoon, related_name='activiteiten', blank=True)
    tags = models.ManyToManyField(to=TagDefinition, related_name='activiteiten', blank=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    locatie = models.ForeignKey(Locatie, related_name='activiteiten', blank=True, null=True)
    organisatie = models.ForeignKey(Organisatie, related_name='activiteiten', blank=True, null=True)

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

    def __str__(self):
        return f'<{self.naam}>'

    def __repr(self):
        return f'<{self.guid}>'

    class Meta:
        verbose_name_plural = "Activiteiten"
