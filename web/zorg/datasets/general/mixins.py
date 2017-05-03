# Python
import logging
# Packages
from django.contrib.postgres.fields import JSONField
from django.db import DatabaseError, models, transaction
# Project
from django.conf import settings
from elasticsearch_dsl.connections import connections
from datetime import datetime


LOG = logging.getLogger(__name__)


class ReadOptimizedModel(models.Model):
    create_doc = None

    def save(self, *args, **kwargs):
        # Saving the model
        item = super(ReadOptimizedModel, self).save(args, kwargs)
        # Adding to elastic
        try:
            connections.create_connection(
                hosts=settings.ELASTIC_SEARCH_HOSTS,
                retry_on_timeout=True,
            )
            doc = self.create_doc()
            doc.save()
        except Exception as exp:
            LOG.error(f'Failed to send to elastic: {exp}')
        return item

    class Meta(object):
        abstract = True


class EventLogMixin(models.Model):
    read_model = None  # This must be overwritten

    EVENT_TYPES = (
        ('C', 'CREATE'),
        ('U', 'UPDATE'),
        ('D', 'DELETE'),
    )

    guid = models.CharField(max_length=255)
    sequence = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)  # This makes the field un-editable.
    event_type = models.CharField(max_length=1, choices=EVENT_TYPES)
    data = JSONField()

    def save(self, *args, **kwargs):
        # Making sure that Saving event and model is atomic

        # prevent circular import
        from datasets.general import events

        if 'locatie_id' in self.data.keys():
            if not isinstance(self.data['locatie_id'], str):
                self.data['locatie_id'] = self.data['locatie_id'].guid

        # make sure datetime fields are serialized to strings
        for k, v in self.data.items():
            if isinstance(v, datetime):
                self.data[k] = str(self.data[k])
        print(self.data)
        try:
            # @TODO atomic does not seem to work as expected
            # The event log is created even if procssing fails
            with transaction.atomic(savepoint=False):
                # Saving the event
                super(EventLogMixin, self).save()
                # Updating the Read optimized model
                # -----------------------------------
                self.data.update(kwargs)  # Adding kwargs data
                success = events.handle_event(self, self.read_model)
        except DatabaseError as e:
            LOG.error(f'Database error, rolling back: {e}')
            return False
        return success

    def __str__(self):
        return f'<{self.guid} {self.sequence} {self.get_event_type_display()}>'

    def __repr__(self):
        return f'<{self.guid} {self.sequence} {self.get_event_type_display()}>'

    class Meta(object):
        abstract = True
        unique_together = ['guid', 'sequence']
