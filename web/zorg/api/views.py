# Python
import json
# Packages
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
# Project
from datasets.normalized import queries


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

        # if search_for == 'organisatie':
        #     query = queries.organisatie_Q(query_string)
        # elif search_for == 'activiteit':
        #     query = queries.activiteit_Q(query_string)
        # elif search_for == 'locatie':
        #     query = queries.location_Q(query_string)
        # else:
        #     return None
        # Perform search
        response = self.elastic.search(
            index=settings.ELASTIC_INDEX,
            body=query
        )
        # Format resuts
        # return
        return HttpResponse(json.dumps(response))

    def get(self, *args, **kwargs):
        return self.search_elastic(kwargs.get('search_for', None), self.request.GET.get('query', ''))

    def post(self, *args, **kwargs):
        return self.search_elastic(kwargs.get('search_for', None), self.request.GET.get('query', ''))
