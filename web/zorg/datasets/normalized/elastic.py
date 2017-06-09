# Python
import functools
import json
import logging
# Packages
from django.conf import settings
from elasticsearch import Elasticsearch, RequestError

log = logging.getLogger(__name__)


class QueryError(Exception):
    """Error that indicates to the user of this module that something went
    wrong while searching."""


@functools.lru_cache(maxsize=1)
def _elasticsearch():
    """Elasticsearch Instance.

    lru_cache makes this a singleton. I don't think / hope we need to worry
    about the connection. The docs indicate that the Elasticsearch library
    takes care of this itself.

    :see: https://elasticsearch-py.readthedocs.io/en/master/#persistent-connections
    """
    return Elasticsearch(
        hosts=settings.ELASTIC_SEARCH_HOSTS, retry_on_timeout=True,
        refresh=True
    )


def _search(query):
    """Fire queries at Elasticsearch.
    """
    query['size'] = 1000

    response = _elasticsearch().search(
        index=settings.ELASTIC_INDEX,
        body=query
    )
    return json.dumps(response)


def search(q='', doctype=None, latlong=None):
    fields = ["naam^1.5", "beschrijving"]
    should = [{"multi_match": {"query": t, "fields": fields}} for t in q.split()]
    filter = (doctype and {"type": {"value": doctype}}) or None
    if latlong:
        lat, long = latlong


def zorg_Q(query_string: dict, doc_type: str) -> dict:
    if doc_type:
        q = {
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": query_string,
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
                    "query": query_string,
                    "fields": ["naam^1.5", "beschrijving"]
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
        match = {
            "multi_match": {
                "query": query['text'],
                "fields": ["naam^1.5", "beschrijving"]
            }
        }
    except KeyError:
        match = {'match_all': {}}

    geo_distance = {
        "geo_distance": {
            "distance": default_distance,
            "locatie.centroid": {
                "lat": query['lat'],
                "lon": query['lon']
            }
        }
    }

    # Sorting by geo-distance add it to the results
    # Since sorting by _score is the intention, sorting first
    # by score and then by distance
    q = {
        "query": {
            "bool": {
                "must": [
                    match,
                    {
                        "geo_distance": {
                            "distance": default_distance,
                            "locatie.centroid": {
                                "lat": query['lat'],
                                "lon": query['lon']
                            }
                        }
                    }
                ]
            }
        },
        "sort": [
            "_score",
            {
                "_geo_distance": {
                    "locatie.centroid": {
                        "lat": query['lat'],
                        "lon": query['lon']
                    },
                    "order": "asc",
                    "unit": "km",
                    "mode": "min",
                    "distance_type": "plane"
                }
            }
        ]
    }

    return q
