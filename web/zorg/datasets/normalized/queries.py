# Python
import logging
# Packages
from elasticsearch_dsl import Q


log = logging.getLogger(__name__)


def zorg_Q(doc_type, query_string):
    if doc_type:
        q = {
            "bool": {
                "must": {
                    "multi_match": {
                        "query":  query_string,
                        "fields": ["naam^1.5", "beschrijving"]
                    }
                },
                "filter": {
                    "type": {"value": doc_type}
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
    return q


def tterms_Q(doc_type, query_string):
    terms = query_string.split(' ')
    q = {
        "terms": {
            "beschrijving": terms
        }
    }

    return q
# 127.0.0.1:8000/zorg/zoek/thema/?query=Zorg%20Hulp%20Huishouden%20Verpleging%20Wmo%20Vervoer%20Jeugdzorg%20Medisch%20Medicijnen%20Terminaal%20Dagopvang%20Zorghotel%20zorg%20hulp%20huishouden%20verpleging%20wmo%20vervoer%20jeugdzorg%20medisch%20medicijnen%20terminaal%20dagopvang%20zorghotel


def terms_Q(doc_type, query_string):
    terms = query_string.split(' ')
    q = {
        "bool": {
            "should": [
                {
                    "terms": {
                        "naam": terms
                    }
                },
                {
                    "terms": {
                        "beschrijving": terms
                    }
                }
            ],
            "minimum_should_match": 1
        },
    }

    return q
