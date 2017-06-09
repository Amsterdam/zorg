import functools
import json
import logging
import sys

from django.conf import settings
from elasticsearch import Elasticsearch

_logger = logging.getLogger(__name__)


class SearchError(Exception):
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


def search(q='', doctype=None, lonlat=None):
    """Generate and fire an Elastic query"""
    fields = ['naam^1.5', 'beschrijving']
    should = [
        {'multi_match': {'query': t, 'fields': fields}} for t in q.split()
    ]
    searchfilter = (doctype and {'type': {'value': doctype}}) or {}
    sort = ['_score']
    if lonlat:
        sort.insert(0, {
            '_geo_distance': {
                'pin.location': lonlat,
                'order': 'asc',
                'unit': 'km'
            }
        })
    query = {
        'query': {
            'should': should,
            'filter': searchfilter
        },
        'sort': sort,
        'size': 1000
    }

    try:
        response = _elasticsearch().search(
            index=settings.ELASTIC_INDEX,
            body=query
        )
    except Exception as e:
        _logger.critical('Exception while searching', exc_info=sys.exc_info())
        raise SearchError() from e

    return json.dumps(response)
