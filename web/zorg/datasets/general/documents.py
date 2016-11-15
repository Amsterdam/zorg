# Python
from typing import List, cast
# Packages
from django.conf import settings
import elasticsearch_dsl as es


class NormalizedOrganisatie(es.DocType):

    naam = es.String()  # ngram
    beschrijving = es.String()
    afdeling = es.String()
    bron = es.String()


class NormalizedActiviteit(es.DocType):

    naam = es.String()
    beschrijving = es.String()
    bronLink = es.String()
    contactpersoon = es.String()
    telefoon = es.String()
    fax = es.String()
    email = es.String()
    mobiel = es.String()
    website = es.String()
    tijdstip = es.String()
    tags = es.String()


class NormalizedLocatie(es.DocType):

    naam = es.String()
    centroid = es.GeoPoint()
    straatnaam = es.String()
    huisnummer = es.String()
    huisnummer_toevoeging = es.String()
    postcode = es.String()
