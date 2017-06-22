# Python
import logging

from django.conf import settings
from django.db import connection
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from datasets.normalized.models import Activiteit, Organisatie, Locatie
from zorg import  settings as zorg_settings


log = logging.getLogger(__name__)


def health(request):
    # check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("select 1")
            assert cursor.fetchone()
    except:
        log.exception("Database connectivity failed")
        return HttpResponse(
            "Database connectivity failed",
            content_type="text/plain", status=500)

    # check elasticsearch
    try:
        client = Elasticsearch(zorg_settings.ELASTIC_SEARCH_HOSTS)
        assert client.info()
    except:
        log.exception("Elasticsearch connectivity failed")
        return HttpResponse(
            "Elasticsearch connectivity failed",
            content_type="text/plain", status=500)

    # check debug
    if settings.DEBUG:
        log.exception("Debug mode not allowed in production")
        return HttpResponse(
            "Debug mode not allowed in production",
            content_type="text/plain", status=500)

    return HttpResponse(
        "Health OK", content_type='text/plain', status=200)


def check_data(request):
    # check database
    message = ''

    try:
        if Activiteit.objects.count() < 10:
            message = "Activities should contain a minimum of 10 records."
        elif Organisatie.objects.count() < 1:
            message = "Organisatie should contain a minimum of 1 records."
        elif Locatie.objects.count() < 1:
            message = "Locatie should contain a minimum of 1 records."
    except Exception as e:
        log.error(e)
        message = "Error connecting to database."

    # check elastic
    try:
        print(zorg_settings.ELASTIC_SEARCH_HOSTS)
        client = Elasticsearch(zorg_settings.ELASTIC_SEARCH_HOSTS)
        v = client.search(index = 'zorg',body='', size=0)
    except Exception as e:
        log.error(e)
        message = "Error connecting to elastic"

    if not message:
        message = "Data Ok"
        status = 200
    else:
        status = 500

    return HttpResponse(message, content_type='text/plain', status=status)
