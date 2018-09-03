import elasticsearch_dsl as es
from django.conf import settings
from elasticsearch_dsl import analyzer, tokenizer

dutch_analyzer = es.analyzer(
    'dutchanalyzer', type='standard', stopwords='_dutch_')

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
    naam = es.String(analyzer=dutch_analyzer)  # ngram
    beschrijving = es.String(analyzer=dutch_analyzer)
    afdeling = es.String(index='not_analyzed')


@_index.doc_type
class Locatie(es.DocType):
    ext_id = es.String(index='not_analyzed')
    naam = es.String(analyzer=dutch_analyzer)
    centroid = es.GeoPoint()
    openbare_ruimte_naam = es.String(index='not_analyzed')
    huisnummer = es.String(index='not_analyzed')
    huisnummer_toevoeging = es.String(index='not_analyzed')
    postcode = es.String(index='not_analyzed')


@_index.doc_type
class Activiteit(es.DocType):
    ext_id = es.String(index='not_analyzed')
    naam = es.String(analyzer=dutch_analyzer)
    beschrijving = es.String(analyzer=dutch_analyzer)
    bron_link = es.String(index='not_analyzed')
    tijdstip = es.String(index='not_analyzed')
    tags = es.String(index='not_analyzed')
    centroid = es.GeoPoint()
    locatie = es.Object(
        doc_class=Locatie,
        properties={
            'ext_id': es.String(index='not_analyzed'),
            'naam': es.String(analyzer=dutch_analyzer),
            'centroid': es.GeoPoint(),
            'openbare_ruimte_naam': es.String(index='not_analyzed'),
            'huisnummer': es.String(index='not_analyzed'),
            'huisnummer_toevoeging': es.String(index='not_analyzed'),
            'postcode': es.String(index='not_analyzed')
        }
    )
