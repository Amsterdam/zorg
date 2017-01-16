# Python
import logging
# Packages
from elasticsearch_dsl import Q


log = logging.getLogger(__name__)


def zorg_Q(doc_type, query_string):
    if doc_type:
        q = {
            "bool": {
                "multi_match": {
                    "query":  query_string,
                    "fields": ["naam^1.5", "beschrijving"]
                },
                "filter": {
                    {"type": {"value": doc_type}}
                }
            }
        }
    else:
        q = {
            "multi_match": {
                "query":  query_string,
                "fields": ["naam^1.5", "beschrijving"]
            }
        }
    print(q)
    return q


def location_Q():
    return Q(
        'prefix_match_phase',
        naam=query_string,
        sort_fields=['naam']
    )


def activiteit_Q(query_string):
    return Q(
        'prefix_match_phase',
        naam=query_string,
        sort_fields=['naam']
    )


def organisatie_Q(query_string):
    return Q(
        'prefix_match_phase',
        naam=query_string,
        sort_fields=['naam']
    )
