# Python
import logging
# Packages
from elasticsearch_dsl import Q


log = logging.getLogger(__name__)


def zorg_Q(query_string: dict, doc_type: str) -> dict:
    if doc_type:
        q = {
            "query": {
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
        }
    else:
        q = {
            "query": {
                "multi_match": {
                    "query":  query_string,
                    "fields": ["naam^1.5", "beschrijving"]
                }
            }
        }
    return q


def tterms_Q(doc_type, query_string):
    terms = query_string.split(' ')
    q = {
        "query": {
            "terms": {
                "beschrijving": terms
            }
        }
    }

    return q

def terms_Q(query_string: str, doc_type: str) -> dict:
    terms = query_string.split(' ')
    q = {
        "query": {
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
    }

    return q

def geo_Q(query: dict, doc_type=None) -> dict:
    """
    Perform a geospatial search.
    The query parameter contains the needed information for the query.
    There are two required keys: 'lat' and 'lon'
    An optional 'text' key can given to also
    query name and/or description
    """
    default_distance = '2km'
    # Allowing for text filtering in query, if needed
    try:
        match =  {
            "multi_match": {
                "query":  query['text'],
                "fields": ["naam^1.5", "beschrijving"]
            }
        }
    except KeyError:
        match = {"match_all" : {}}

    # Creating query dict
    q = {
        "query": {
            "bool" : {
                "must" : match,
                "filter" : {
                    "geo_distance" : {
                        "distance" : default_distance,
                        "centroid" : {
                            "lat" : query['lat'],
                            "lon" : query['lon']
                        }
                    },
                    "type": {"value": 'activiteit'}
                }
            }
        },
         "sort" : [
            {
                "_geo_distance" : {
                    "centroid" :{
                        "lat" : query['lat'],
                        "lon" : query['lon']
                    },
                    "order" : "asc",
                    "unit" : "m",
                    "mode" : "min",
                    "distance_type" : "sloppy_arc"
                }
            }
        ],
    }

    return q
