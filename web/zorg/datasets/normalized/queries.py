# Python
import logging
# Packages
from elasticsearch_dsl import Q


log = logging.getLogger(__name__)


def zorg_Q(doc_type, query_string):
    return {
        "bool": {
            "must": {
                "match_phrase_prefix": {
                    "naam": {
                        "query": "query_string"
                    }
                }
            },
            "filter": {
                "type": {
                    "value": doc_type
                }
            }
        }
    }


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
