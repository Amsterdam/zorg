import functools
import itertools
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


def search(q='', doctype=None, lonlat=None, tags=None):
    """Generate and fire an Elastic query"""
    bools = q and list(
        itertools.chain.from_iterable(
            (
                {'term': {'naam': {'value': t, 'boost': 1.5}}},
                {'term': {'beschrijving': t}}
            ) for t in q.split()
        )
    )
    searchfilter = (doctype and [{'type': {'value': doctype}}]) or []
    if tags:
        searchfilter.extend({'term': {'tags': tag}} for tag in tags)
    sort = ['_score']
    if lonlat:
        sort.insert(0, {
            '_geo_distance': {
                'locatie.centroid': lonlat,
                'order': 'asc',
                'unit': 'km'
            }
        })
    query = {
        'sort': sort,
        'size': 1000
    }
    if bools or searchfilter:
        query['query'] = {'bool': {}}
        boolquery = query['query']['bool']
        if bools:
            # if we have terms and we're sorting on geo, then we must filter
            # the terms with "must" rather than "should"
            booltype = (lonlat and 'must') or 'should'
            boolquery[booltype] = bools
        if searchfilter:
            boolquery['filter'] = searchfilter

    try:
        response = _elasticsearch().search(
            index=settings.ELASTIC_INDEX,
            body=query
        )
    except Exception as e:
        raise SearchError() from e

    return json.dumps(response)
