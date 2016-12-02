# Python
from typing import List, cast
# Packages
from django.conf import settings
import elasticsearch_dsl as es
# Project
import datasets.normalized.models as models


class Organisatie(es.DocType):

    ext_id = es.String()
    naam = es.String()  # ngram
    beschrijving = es.String()
    afdeling = es.String()


class Activiteit(es.DocType):

    ext_id = es.String()
    naam = es.String()
    beschrijving = es.String()
    website = es.String()
    tijdstip = es.String()
    tags = es.String()


class Locatie(es.DocType):

    ext_id = es.String()
    naam = es.String()
    centroid = es.GeoPoint()
    straatnaam = es.String()
    huisnummer = es.String()
    huisnummer_toevoeging = es.String()
    postcode = es.String()


def doc_from_organisatie(n: models.Organisatie) -> Organisatie:
    """
    Create an elastic Organisate doc
    """
    doc = Organisatie(_id=n.guid)
    for key in ('naam', 'beschrijving', 'afdeling'):
        setattr(doc, key, getattr(n, key))
    doc.ext_id = n.id
    return doc


def doc_from_activiteit(n: models.Activiteit) -> Activiteit:
    """
    Create an elastic Activiteit doc
    """
    doc = Activiteit(_id=n.guid)
    for key in ('naam', 'beschrijving', 'website', 'tags'):
        setattr(doc, key, getattr(n, key))
    doc.ext_id = n.id
    return doc


def doc_from_locatie(n: models.Locatie) -> Locatie:
    """
    Create an elastic Locatie doc
    """
    doc = Locatie(_id=n.guid)
    for key in ('naam', 'straatnaam', 'huisnummer', 'huisnummer_toevoeging', 'postcode'):
        setattr(doc, key, getattr(n, key))
    # Adding geometrie
    doc.centroid = n.centroid.coords
    doc.ext_id = n.id
    return doc
