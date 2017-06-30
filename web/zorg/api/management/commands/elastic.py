# Python
import logging
import time
import re

import elasticsearch_dsl as es
import requests
import json
from django.conf import settings
# Packages
from django.core.management import BaseCommand
from elasticsearch_dsl.connections import connections

# Project
from datasets.normalized import models
from datasets.normalized.documents import Activiteit, Locatie, Organisatie, Term

log = logging.getLogger(__name__)


class Command(BaseCommand):
    doc_types = [Activiteit, Locatie, Organisatie, Term]
    index = settings.ELASTIC_INDEX
    index_backup = index + '_backup'

    def add_arguments(self, parser):
        parser.add_argument(
            '--build',
            action='store_true',
            dest='build_index',
            default=False,
            help='Build elastic index from postgres')

        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete_indexes',
            default=False,
            help='Delete elastic indexes from elastic')

        parser.add_argument(
            '--reindex',
            action='store_true',
            dest='reindex_data',
            default=False,
            help='Reindex all the data to elastic')

        parser.add_argument(
            '--backup_index',
            action='store_true',
            dest='backup_index',
            default=False,
            help='Create backup index data to elastic')

        parser.add_argument(
            '--delete_backup_index',
            action='store_true',
            dest='delete_backup_index',
            default=False,
            help='Delete backup index from elastic')

        parser.add_argument(
            '--restore_index',
            action='store_true',
            dest='restore_index',
            default=False,
            help='Restore backup index data to elastic')

    def handle(self, *args, **options):
        start = time.time()

        if options['delete_indexes']:
            self.delete_index()
        elif options['build_index']:
            self.create_index()
        elif options['reindex_data']:
            self.reindex_data()
            self.reindex_typeahead()
        elif options['backup_index']:
            self.backup_index()
        elif options['delete_backup_index']:
            self.delete_backup_index()
        elif options['restore_index']:
            self.restore_index()
        else:
            self.stdout.write("Unkown command")

        self.stdout.write(
            "Total Duration: %.2f seconds" % (time.time() - start))

    def __connect_to_elastic(self):
        # Creates a connection to elastic
        connections.create_connection(
            hosts=settings.ELASTIC_SEARCH_HOSTS,
            retry_on_timeout=True,
        )
        return es.Index(self.index)

    def delete_index(self):
        # Deleteing the index
        requests.delete('http://{}/{}'.format(settings.ELASTIC_SEARCH_HOSTS[0], self.index))

    def create_index(self):
        # Creating a a new index and adding
        # mapping to the doc_types
        idx = self.__connect_to_elastic()
        for dt in self.doc_types:
            idx.doc_type(dt)
        idx.create()

    def reindex_data(self):
        """
        This will work for now but needs to replace with a better system after the poc
        with a 'replay' mechanism
        """
        connections.create_connection(
            hosts=settings.ELASTIC_SEARCH_HOSTS,
            retry_on_timeout=True,
        )
        locations = models.Locatie.objects.all()
        actions = models.Activiteit.objects.all()
        organisations = models.Organisatie.objects.all()

        for dataset in [locations, organisations]:
            for item in dataset:
                doc = item.create_doc()
                doc.save()
        for action in actions:
            tags = []
            for t in action.tags.all():
                tags.append(t.naam)
            if tags:
                action.es_tags = tags
            doc = action.create_doc()
            doc.save()

    def reindex_typeahead(self):
        """reindex the autocomplete terms

        """
        connections.create_connection(
            hosts=settings.ELASTIC_SEARCH_HOSTS,
            retry_on_timeout=True,
        )
        locations = models.Locatie.objects.all()
        actions = models.Activiteit.objects.all()
        organisations = models.Organisatie.objects.all()

        all_terms = {}
        for dataset in [locations, actions, organisations]:
            for item in dataset:
                for attr in ('naam', 'beschrijving'):
                    if hasattr(item, attr):
                        terms = getattr(item, attr).lower().split()
                        for term in terms:
                            term_cleaned = self.clean_term(term)
                            if term_cleaned:
                                all_terms[term_cleaned] = all_terms.get(term_cleaned, 0) + 1

        for (term, gewicht) in all_terms.items():
            doc = Term(term=term, gewicht=gewicht)
            doc.save()

    def delete_backup_index(self):
        requests.delete('http://{}/{}'.format(settings.ELASTIC_SEARCH_HOSTS[0], self.index_backup))

    def backup_index(self):
        self.delete_backup_index()
        response = requests.post('http://{}/_reindex'.format(settings.ELASTIC_SEARCH_HOSTS[0]),
                      data=json.dumps({
                          'source': {
                              'index': self.index
                          },
                          'dest': {
                              'index': self.index_backup
                          }
                      }))

        if response.status_code != 200:
            raise Exception("Error! ", response.text)

    def restore_index(self):
        response = requests.post('http://{}/_reindex'.format(settings.ELASTIC_SEARCH_HOSTS[0]),
                      data=json.dumps({
                          'source': {
                              'index': self.index_backup
                          },
                          'dest': {
                              'index': self.index
                          }
                      }))
        if response.status_code != 200:
            raise Exception("Error! ", response.text)

    def clean_term(self, term):
        result = term
        for c in ['<br', '&gt;', '&lt;']:
            result = result.replace(c, '')
        # result = re.sub('\W+', '', result)
        return result
