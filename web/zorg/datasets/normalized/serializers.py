# Packages
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
# Projects
from . import models
from datasets.general import events


class ZorgModelSerializer(serializers.ModelSerializer):

    event_model = None

    def create(self, validated_data):
        print('Serilaizer create')
        # Creating the guid
        guid = events.guid_from_id('CODE', validated_data['id'])

        # There can bew two cases in which create can be made:
        # 1. There is no previous entry
        # 2. The laatste event was een delete
        prev_events = list(self.event_model.objects.filter(
                      guid=guid).order_by('sequence'))
        if len(prev_events) == 0:
            sequence = 0
        elif prev_events[-1].event_type == 'D':
            sequence = prev_events[-1].sequence + 1
        else:
            # Does not match creation rule
            raise ValidationError('Object already exists')

        event = self.event_model(
            guid=guid,
            sequence=sequence,
            event_type='C',
            data=validated_data
        )
        new_item = event.save()
        print ('new_item', new_item)
        return new_item

    def update(self, instance, validated_data):
        print('Serialzier update')

    def retrieve(self, request, pk=None):
        # Reading the model
        model = self.event_model

class OrganisatieSerializer(ZorgModelSerializer):

    ref_model = models.OrganisatieEventLog

    class Meta(object):
        exclude = ('guid',)
        model = models.Organisatie


class ActiviteitSerializer(ZorgModelSerializer):

    event_model = models.ActiviteitEventLog

    class Meta(object):
        exclude = ('guid',)
        model = models.Activiteit


class LocatieSerializer(ZorgModelSerializer):

    event_model = models.LocatieEventLog

    class Meta(object):
        exclude = ('guid',)
        model = models.Locatie
