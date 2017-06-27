import json

import elasticsearch_dsl as es
from django.conf import settings
from django.db import models
from elasticsearch_dsl import analyzer, tokenizer

base_analyzer = analyzer('zorg_base_txt',
                         tokenizer=tokenizer('trigram', 'nGram', min_gram=2, max_gram=20),
                         filter=['lowercase']
                         )

_index = es.Index(settings.ELASTIC_INDEX)

@_index.doc_type
class Term(es.DocType):
    term = es.Text()
    gewicht = es.Integer()


@_index.doc_type
class Organisatie(es.DocType):
    ext_id = es.String(index='not_analyzed')
    naam = es.String(analyzer=base_analyzer)  # ngram
    beschrijving = es.String(analyzer=base_analyzer)
    afdeling = es.String(index='not_analyzed')


@_index.doc_type
class Locatie(es.DocType):
    ext_id = es.String(index='not_analyzed')
    naam = es.String(analyzer=base_analyzer)
    centroid = es.GeoPoint()
    openbare_ruimte_naam = es.String(index='not_analyzed')
    huisnummer = es.String(index='not_analyzed')
    huisnummer_toevoeging = es.String(index='not_analyzed')
    postcode = es.String(index='not_analyzed')


@_index.doc_type
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

    try:
        lat, lon = n.geometrie.transform('wgs84', clone=True).coords
        doc.centroid = {'lat': lat, 'lon': lon}
    except AttributeError:
        doc.centroid
    doc.ext_id = n.id
    return doc


def doc_from_activiteit(n: models.Model) -> Activiteit:
    """
    Create an elastic Activiteit doc
    """
    doc = Activiteit(_id=n.guid)
    for key in ('naam', 'beschrijving', 'bron_link'):
        setattr(doc, key, getattr(n, key))

    # add tags
    if n.es_tags:
        setattr(doc, 'tags', n.es_tags)

    doc.ext_id = n.id
    # Loading locatie
    if n.locatie:
        try:
            locatie_doc = doc_from_locatie(n.locatie)
            doc.locatie = locatie_doc
        except Exception:
            raise
    return doc
