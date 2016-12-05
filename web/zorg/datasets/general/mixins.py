from django.contrib.postgres.fields import JSONField
from django.db import IntegrityError, models, transaction
from datasets.general import events

from django.conf import settings
from elasticsearch_dsl.connections import connections


class ReadOptimizedModel(models.Model):

    create_doc = None

    def save(self, *args, **kwargs):
        # Saving the model
        super(ReadOptimizedModel, self).save(args, kwargs)
        # Adding to elastic
        try:
            connections.create_connection(
                hosts=settings.ELASTIC_SEARCH_HOSTS,
                retry_on_timeout=True,
            )
            doc = self.create_doc()
            doc.save()
        except Exception as exp:
            print('Failed to send to elastic:', repr(exp))

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
        success = False
        with transaction.atomic():
            # Saving the event
            super(EventLogMixin, self).save(args, kwargs)
            # Updating the Read optimized model
            success = events.handle_event(self, self.read_model)
            print('Transaction succesful')
        print(success)
        return success

    class Meta(object):
        abstract = True
        unique_together = ['guid', 'sequence']
