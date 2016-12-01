# Python
from typing import List, cast
# Packages
from django.conf import settings
import elasticsearch_dsl as es


class Organisatie(es.DocType):

    naam = es.String()  # ngram
    beschrijving = es.String()
    afdeling = es.String()


class Activiteit(es.DocType):

    naam = es.String()
    beschrijving = es.String()
    website = es.String()
    tijdstip = es.String()
    tags = es.String()


class Locatie(es.DocType):

    naam = es.String()
    centroid = es.GeoPoint()
    straatnaam = es.String()
    huisnummer = es.String()
    huisnummer_toevoeging = es.String()
    postcode = es.String()


def doc_from_organisatie(n: models.Organisatie) -> es.DocType:
    """
    Create an elastic Organisate doc
    """
    doc = Organisatie(_id=n.guid)
    for key in ('naam', 'beschrijving', 'afdeling'):
        setattr(doc, key, getattr(n, key))
    return doc


def doc_from_activiteit(n: models.Activiteit) -> es.DocType:
    """
    Create an elastic Activiteit doc
    """
    doc = Activiteit(_id=n.guid)
    for key in ('naam', 'beschrijving', 'website', 'tags'):
        setattr(doc, key, getattr(n, key))
    return doc


def doc_from_locatie(n: models.Locatie) -> es.Locatie:
    """
    Create an elastic Locatie doc
    """
    doc = Locatie(_id=n.guid)
    for key in ('naam', 'straatnaam', 'huisnummer', 'huisnummer_toevoeging', 'postcode'):
        setattr(doc, key, getattr(n, key))
    
    return doc
