# Python
from typing import List, cast
# Packages
from django.conf import settings
from django.db import models
import elasticsearch_dsl as es
from elasticsearch_dsl import analyzer, tokenizer
# Project
from datasets.normalized import models as norm_models


base_analyzer = analyzer('zorg_base_txt',
                         tokenizer=tokenizer('trigram', 'nGram', min_gram=2, max_gram=20),
                         filter=['lowercase']
                         )


class Organisatie(es.DocType):

    ext_id = es.String(index='not_analyzed')
    naam = es.String(analyzer=base_analyzer)  # ngram
    beschrijving = es.String(analyzer=base_analyzer)
    afdeling = es.String(index='not_analyzed')

    class Meta(object):
        index = settings.ELASTIC_INDEX


class Locatie(es.DocType):

    ext_id = es.String(index='not_analyzed')
    naam = es.String(analyzer=base_analyzer)
    centroid = es.GeoPoint()
    openbare_ruimte_naam = es.String(index='not_analyzed')
    huisnummer = es.String(index='not_analyzed')
    huisnummer_toevoeging = es.String(index='not_analyzed')
    postcode = es.String(index='not_analyzed')

    class Meta(object):
        index = settings.ELASTIC_INDEX


class Activiteit(es.DocType):

    ext_id = es.String(index='not_analyzed')
    naam = es.String(analyzer=base_analyzer)
    beschrijving = es.String(analyzer=base_analyzer)
    bron_link = es.String(index='not_analyzed')
    tijdstip = es.String(index='not_analyzed')
    tags = es.String(index='not_analyzed')
    locatie = es.Object(
        doc_class=Locatie,
        properties={
            'ext_id': es.String(index='not_analyzed'),
            'naam': es.String(analyzer=base_analyzer),
            'centroid': es.GeoPoint(),
            'openbare_ruimte_naam': es.String(index='not_analyzed'),
            'huisnummer': es.String(index='not_analyzed'),
            'huisnummer_toevoeging': es.String(index='not_analyzed'),
            'postcode': es.String(index='not_analyzed')
        }
    )
    class Meta(object):
        index = settings.ELASTIC_INDEX


def doc_from_organisatie(n: models.Model) -> Organisatie:
    """
    Create an elastic Organisate doc
    """
    doc = Organisatie(_id=n.guid)
    for key in ('naam', 'beschrijving', 'afdeling'):
        setattr(doc, key, getattr(n, key))
    doc.ext_id = n.id
    return doc


def doc_from_locatie(n: models.Model) -> Locatie:
    """
    Create an elastic Locatie doc
    """
    doc = Locatie(_id=n.guid)
    for key in ('naam', 'openbare_ruimte_naam', 'huisnummer', 'huisnummer_toevoeging', 'postcode'):
        setattr(doc, key, getattr(n, key))
    # Adding geometrie
    try:
        doc.centroid = n.geometrie.transform('wgs84', clone=True).coords
    except AttributeError:
        doc.centroid
    doc.ext_id = n.id
    return doc


def doc_from_activiteit(n: models.Model) -> Activiteit:
    """
    Create an elastic Activiteit doc
    """
    doc = Activiteit(_id=n.guid)
    for key in ('naam', 'beschrijving', 'bron_link', 'tags'):
        setattr(doc, key, getattr(n, key))
    doc.ext_id = n.id
    # Loading locatie
    try:
        locatie_doc = doc_from_locatie(n.locatie)
        doc.locatie = locatie_doc
    except Exception as e:
        print(e)
    return doc
