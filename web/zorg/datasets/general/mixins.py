from django.db import models


class EventLogMixin(models.Model):
    EVENT_TYPES = (
        ('C', 'CREATE'),
        ('U', 'UPDATE'),
        ('D', 'DELETE'),
    )

    guid = models.CharField(max_length=255)
    sequence = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)  # This makes the field un-editable.
    event_type = models.CharField(max_length=1, choices=EVENT_TYPES)
    data = models.JsonField()

    # @TODO write global part, call local part
    def create(self):
        pass

    def update(self, data):
        pass

    class Meta(object):
        abstract = True
        unique_together = ['guid', 'sequence']