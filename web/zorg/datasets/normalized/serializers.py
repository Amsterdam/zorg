# Packages
from rest_framework import serializers
# Projects
from . import events, models


class OrganisatieSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # Creating the guid
        guid = events.guid_from_id(validated_data['id'])

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
            action='C',
            data=validated_data
        )
        return event.save()

    def update(self, instance, validated_data):
        pass

    class Meta(object):
        model = models.Organisatie
