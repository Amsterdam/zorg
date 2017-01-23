# Python
import json
import logging
# Packages
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
# Project
from datasets.normalized import queries


log = logging.getLogger(__name__)


class ZoekApiView(View):

    zoek_functie = queries.zorg_Q

    def __init__(self, *args, **kwargs):
        super(ZoekApiView, self).__init__(*args, **kwargs)
        self.elastic = Elasticsearch(
            hosts=settings.ELASTIC_SEARCH_HOSTS, retry_on_timeout=True,
            refresh=True
        )

    def search_elastic(self, search_for, query_string):
        query = {
            'query': self.__class__.zoek_functie(search_for, query_string),
            'size': 1000
        }
        # Perform search
        try:
            response = self.elastic.search(
                index=settings.ELASTIC_INDEX,
                body=query
            )
        except Elasticsearch.RequestError:
            log.error(f'Request error: {response!r}')
            return HttpResponse("Search encounterd an error in the request")
        except Exception as exp:
            log.error(f'{exp!r}')
            return HttpResponse("Error processing request")
        return HttpResponse(json.dumps(response))

    def get(self, *args, **kwargs):
        return self.search_elastic(kwargs.get('search_for', None), self.request.GET.get('query', ''))

    def post(self, *args, **kwargs):
        return self.search_elastic(kwargs.get('search_for', None), self.request.GET.get('query', ''))


# Voor na de poc moet beter
class TermsZoekView(ZoekApiView):

    zoek_functie = queries.terms_Q
