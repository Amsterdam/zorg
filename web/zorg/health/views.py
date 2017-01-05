# Python
import logging

from django.conf import settings
from django.db import connection
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


log = logging.getLogger(__name__)


def health(request):
    # check database
    message = ''
    status = 200
    try:
        with connection.cursor() as cursor:
            cursor.execute("select 1")
            assert cursor.fetchone()
    except:
        log.exception("Database connectivity failed")
        message += "\nDatabase connectivity failed."
        status = 500
    # check elasticsearch
    try:
        client = Elasticsearch(settings.ELASTIC_SEARCH_HOSTS)
        assert client.info()
    except:
        log.exception("Elasticsearch connectivity failed")
        message += "\nElasticsearch connectivity failed."
        status = 500

    if not message:
        message = "Connectivity OK"

    return HttpResponse(
        message, content_type='text/plain', status=status)


def check_data(request):
    # For now alway happy
    return HttpResponse('No data yet in the system', content_type='text/plain', status=200)
    # check bag
    message = ''
    status = 200
    try:
        assert Nummeraanduiding.objects.count() > 0
    except:
        log.exception("No BAG data found")
        message += "\nNo BAG data found."
        status = 500

    # check elastic
    try:
        client = Elasticsearch(settings.ELASTIC_SEARCH_HOSTS)
        assert Search().using(client)\
                       .index(settings.ELASTIC_INDICES['DS_BAG'])\
                       .query("match_all", size=0)
    except:
        log.exception("Autocomplete failed")
        message += "\nAutocomplete failed."
        status = 500

    if not message:
        message = "Data Ok"

    return HttpResponse(message, content_type='text/plain', status=status)
