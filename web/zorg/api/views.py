"""Views for search endpoints and for the OpenAPI defintition.

.. todo::
    Reorganize this code and implement content negotiation.
"""
# Python
import functools
import json
import logging
import os

# Packages
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.views.decorators.http import require_GET
from elasticsearch import Elasticsearch, RequestError

# Project
from datasets.normalized import elastic

log = logging.getLogger(__name__)


@require_GET
def search(request, doctype=None):
    pass


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


class ZoekApiView(View):
    zoek_functie = queries.zorg_Q

    def __init__(self, *args, **kwargs):
        super(ZoekApiView, self).__init__(*args, **kwargs)
        self.elastic = Elasticsearch(
            hosts=settings.ELASTIC_SEARCH_HOSTS, retry_on_timeout=True,
            refresh=True
        )

    def get_query(self):
        """
        Returns the information needed by the query
        Naive implementation expects a query parameter in GET or POST
        and returns that as a string. This can be overwritten to provide
        more complex query needs.

        If nothing is found returns an emptuy string. This is in line with
        elastic behavior of suppling all the items in case of search with
        no given query
        """
        request_dict = getattr(self.request, self.request.method)
        return request_dict.get('query', '')

    def search_elastic(self, search_for: str, query: str) -> HttpResponse:
        query = self.__class__.zoek_functie(self.get_query(), search_for)
        query['size'] = 1000
        # Perform search
        try:
            response = self.elastic.search(
                index=settings.ELASTIC_INDEX,
                body=query
            )
        except RequestError as exp:
            log.error(f'{exp!r}')
            return HttpResponse(f"Search encounterd an error in the request, {exp}")
        except Exception as exp:
            log.error(f'{exp!r}')
            return HttpResponse("Error processing request")
        return HttpResponse(json.dumps(response))

    def get(self, *args, **kwargs):
        return self.search_elastic(kwargs.get('search_for', None), self.request.GET.get('query', ''))

    def post(self, *args, **kwargs):
        return self.search_elastic(kwargs.get('search_for', None), self.request.POST.get('query', ''))


class TermsZoekView(ZoekApiView):
    zoek_functie = queries.terms_Q


class GeoZoekView(ZoekApiView):
    zoek_functie = queries.geo_Q

    def get_query(self):
        """
        Overwriting to support lat / lon / text
        @TODO do some cleanup, maybe?
        """
        request_dict = getattr(self.request, self.request.method)
        return request_dict


class OpenApiView(View):
    def get(self, *args, **kwargs):
        return HttpResponse(open(f'{os.path.dirname(os.path.abspath(__file__))}/openapi.yml').read(),
                            content_type='application/yaml')
