# Python
import logging
import time
import elasticsearch_dsl as es
from django.conf import settings
# Packages
from django.core.management import BaseCommand
from elasticsearch_dsl.connections import connections

# Project
from datasets.normalized.documents import Activiteit, Locatie, Organisatie, Term

log = logging.getLogger(__name__)


class Command(BaseCommand):
    doc_types = [Activiteit, Locatie, Organisatie, Term]
    index = settings.ELASTIC_INDEX

    def handle(self, *args, **options):
        start = time.time()
        self.create_index()
        self.stdout.write("Total Duration: %.2f seconds" % (time.time() - start))

    def __connect_to_elastic(self):
        # Creates a connection to elastic
        connections.create_connection(
            hosts=settings.ELASTIC_SEARCH_HOSTS,
            retry_on_timeout=True,
        )
        return es.Index(self.index)

    def create_index(self):
        # Creating a a new index and adding
        # mapping to the doc_types
        idx = self.__connect_to_elastic()
        for dt in self.doc_types:
            idx.doc_type(dt)
        idx.create()
