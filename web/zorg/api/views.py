"""Views for search endpoints and for the OpenAPI defintition.

.. todo::
    Reorganize this code and implement content negotiation.
"""
import functools
import logging
import os
import sys

from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.http import require_GET

# Project
from datasets.normalized import elastic

_logger = logging.getLogger(__name__)


@require_GET
def search(request, doctype=None):
    """Perform a search"""
    queryparams = request.GET
    # this is ugly!! is it lazy? because in that case I would rather create a
    # QueryDict instance from META['query_string']
    q = queryparams.get('query')
    tags = queryparams.getlist('tag')
    lon, lat = queryparams.get('lon'), queryparams.get('lat')
    lonlat = lon and lat and (float(lon), float(lat))
    try:
        return HttpResponse(
            elastic.search(q, doctype, lonlat, tags),
            content_type='application/json')
    except elastic.SearchError:
        _logger.critical('Exception while searching', exc_info=sys.exc_info())
        return HttpResponseServerError()
    except:
        _logger.fatal(
            'Unexpected exception while searching', exc_info=sys.exc_info())
        return HttpResponseServerError()


@require_GET
def typeahead(request):
    """Perform a search"""
    queryparams = request.GET
    # this is ugly!! is it lazy? because in that case I would rather create a
    # QueryDict instance from META['query_string']
    q = queryparams.get('query')
    try:
        return HttpResponse(
            elastic.typeahead(q),
            content_type='application/json')
    except elastic.SearchError:
        _logger.critical('Exception while searching', exc_info=sys.exc_info())
        return HttpResponseServerError()
    except:
        _logger.fatal(
            'Unexpected exception while searching', exc_info=sys.exc_info())
        return HttpResponseServerError()


@require_GET
def openapi(request):
    """Server the OpenAPI spec.

    Currently only supports yml output and doesn't do any content negotiation.
    """
    return HttpResponse(_swagger_yml(), content_type='application/yaml')


@functools.lru_cache(maxsize=1)
def _swagger_yml():
    """Swagger yaml file.

    Uses lru_cache so it can act as a singleton.
    """
    path = '{}/openapi.yml'.format(os.path.dirname(os.path.abspath(__file__)))
    with open(path) as file:
        return file.read()
