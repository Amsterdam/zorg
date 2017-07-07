import functools
import json
import logging

from django.conf import settings
from elasticsearch import Elasticsearch

_logger = logging.getLogger(__name__)


class SearchError(Exception):
    """Error that indicates to the user of this module that something went
    wrong while searching."""


@functools.lru_cache(maxsize=1)
def _elasticsearch():
    """Elasticsearch Instance.

    lru_cache makes this a singleton. I think / hope we don't need to worry
    about the connection. The docs indicate that the Elasticsearch library
    takes care of this itself.

    :see: https://elasticsearch-py.readthedocs.io/en/master/#persistent-connections
    """
    return Elasticsearch(
        hosts=settings.ELASTIC_SEARCH_HOSTS, retry_on_timeout=True,
        refresh=True
    )


def typeahead(q=''):
    """Get a list of JSON encoded search suggestions based on the given query.

    :param q: query
    """
    query = {
        'size': 100,
        'query': {
            'bool': {
                'must': [
                    {
                        'type': {
                            'value': 'term'
                        }
                    },
                    {
                        'prefix': {
                            'term': q,
                        }

                    }

                ]}

        },
        'sort': [
            {
                'gewicht': {
                    'order': 'desc'
                }
            }
        ]
    }
    try:
        results = _elasticsearch().search(
            index=settings.ELASTIC_INDEX,
            body=query
        )
    except Exception as e:
        raise SearchError() from e
    suggestions = []
    for suggestion in results['hits']['hits']:
        suggestions.append(suggestion['_source']['term'])
    return json.dumps(suggestions)


def query(q='', doctype=None, lonlat=None, tags=None):
    """Generate and fire an Elastic query."""
    query = {
        'sort': '_score',
        'size': '50',
        'query': {
            'function_score': {
                'query': {
                    'bool': {
                        'must_not': [
                            {'type': {'value': 'term'}}
                        ]
                    }
                }
            }
        }
    }
    bools = {}
    functions = []

    if q:
        bools['should'] = {
            'multi_match': {
                'query': q, 'fields': ['naam^1.5', 'beschrijving']
            }
        }

    if tags or doctype:
        bools['must'] = []
        if doctype:
            bools['must'].append({'type': {'value': doctype}})
        if tags:
            bools['must'].extend({'term': {'tags': tag}} for tag in tags)

    if lonlat:
        lon, lat = lonlat
        functions.append({
            'gauss': {
                'centroid': {
                    'scale': '100m',
                    'offset': '200m',
                    'origin': {'lon': lon, 'lat': lat},
                    'decay': 0.9
                }
            }
        })

    if bools:
        query['query']['function_score']['query']['bool'].update(bools)
    if functions:
        query['query']['function_score']['functions'] = functions

    return query


def search(q='', doctype=None, lonlat=None, tags=None):
    try:
        response = _elasticsearch().search(
            index=settings.ELASTIC_INDEX,
            body=query(q, doctype, lonlat, tags)
        )
    except Exception as e:
        raise SearchError() from e

    return json.dumps(response)
