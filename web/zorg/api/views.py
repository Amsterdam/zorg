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

    def __init__(self, *args, **kwargs):
        super(ZoekApiView, self).__init__(*args, **kwargs)
        self.elastic = Elasticsearch(
            hosts=settings.ELASTIC_SEARCH_HOSTS, retry_on_timeout=True,
            refresh=True
        )

    def search_elastic(self, search_for, query_string):
        query = {
            'query': queries.zorg_Q(search_for, query_string)
        }
        print(f'query for elastic {query!s}')
        # Perform search
        try:
            response = self.elastic.search(
                index=settings.ELASTIC_INDEX,
                body=query
            )
        except Exception as exp:
            print(f'{exp!r}')
            log.error(f'{exp!r}')
        # Format resuts
        # return
        return HttpResponse(json.dumps(response))

    def get(self, *args, **kwargs):
        print('get call to search')
        return self.search_elastic(kwargs.get('search_for', None), self.request.GET.get('query', ''))

    def post(self, *args, **kwargs):
        return self.search_elastic(kwargs.get('search_for', None), self.request.GET.get('query', ''))
