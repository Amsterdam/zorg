# Packages
from rest_framework import serializers
# Projects
from . import models
from datasets.general import events


class OrganisatieSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = models.Organisatie
        exclude = ('guid',)

    def create(self, validated_data):
        print(validated_data)
        # Creating the guid
        guid = events.guid_from_id('CODE', validated_data['id'])

        # There can bew two cases in which create can be made:
        # 1. There is no previous entry
        # 2. The laatste event was een delete
        prev_events = models.OrganisatieEventLog.objects.filter(
                      guid=guid).order_by('sequence')
        if len(prev_events) == 0:
            sequence = 0
        elif prev_events[-1].action == 'D':
            sequence = prev_events[-1].sequence + 1
        else:
            # Does not math creation rule
            return False  # @TODO is this enough?

        event = models.OrganisatieEventLog(
            guid=guid,
            sequence=sequence,
            event_type='C',
            data=validated_data
        )
        if event.save():
            return event
        return False

    def update(self, instance, validated_data):
        pass

