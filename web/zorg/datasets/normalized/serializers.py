# Packages
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from datasets.general import events
# Projects
from . import models


class ZorgModelSerializer(serializers.ModelSerializer):
    event_model = None

    def get_extra_kwargs(self):
        # On create guid should be empty
        extra_kwargs = super(ZorgModelSerializer, self).get_extra_kwargs()
        action = self.context['view'].action
        if action == 'create':
            guid = extra_kwargs.get('guid', {})
            guid['required'] = False
            extra_kwargs['guid'] = guid
        return extra_kwargs

    def create(self, validated_data):
        # Creating the guid
        if isinstance(self, OrganisatieSerializer):
            # organisatie `guid` == user `id`
            guid = events.guid_from_id(self.context['request'].user, '')
        else:
            guid = events.guid_from_id(self.context['request'].user, validated_data['id'])
        # If a guid is given, remove it from the data
        if 'guid' in validated_data:
            del (validated_data['guid'])
        # There can be two cases in which create can be made:
        # 1. There is no previous entry
        # 2. The last event was  delete
        prev_events = list(self.event_model.objects.filter(guid=guid).order_by('sequence'))
        if len(prev_events) == 0:
            sequence = 0
        elif prev_events[-1].event_type == 'D':
            sequence = prev_events[-1].sequence + 1
        else:
            # Does not match creation rule
            # @TODO convert to self.fail call
            raise ValidationError('Object already exists')

        event = self.event_model(
            guid=guid,
            sequence=sequence,
            event_type='C',
            data=validated_data
        )
        new_item = event.save()
        return new_item

    def update(self, instance, validated_data):
        # Creating the guid
        if isinstance(self, OrganisatieSerializer):
            # organisatie `guid` == user `id`
            guid = events.guid_from_id(self.context['request'].user, '')
        else:
            guid = events.guid_from_id(self.context['request'].user, validated_data['id'])

        # Checking for authorized access
        if guid != instance.guid:
            raise ValidationError('Access not allowed')
        # There can bew two cases in which create can be made:
        # 1. There is no previous entry
        # 2. The laatste event was een delete
        prev_events = list(self.event_model.objects.filter(
            guid=guid).order_by('sequence'))
        if len(prev_events) == 0 or prev_events[-1].event_type == 'D':
            # @TODO convert to self.fail call
            raise ValidationError('Object not found')
        else:
            sequence = prev_events[-1].sequence + 1

        event = self.event_model(
            guid=guid,
            sequence=sequence,
            event_type='U',
            data=validated_data
        )
        item = event.save()
        return item


class OrganisatieSerializer(ZorgModelSerializer):
    locatie_id = serializers.PrimaryKeyRelatedField(queryset=models.Locatie.objects, allow_null=True, required=False)
    event_model = models.OrganisatieEventLog

    class Meta(object):
        exclude = ('locatie',)
        model = models.Organisatie
        extra_kwargs = {'client': {'required': 'False'}}


class LocatieSerializer(ZorgModelSerializer):
    event_model = models.LocatieEventLog

    class Meta(object):
        fields = '__all__'
        model = models.Locatie


class ActiviteitSerializer(ZorgModelSerializer):
    locatie_id = serializers.PrimaryKeyRelatedField(queryset=models.Locatie.objects, allow_null=True, required=False)
    organisatie_id = serializers.PrimaryKeyRelatedField(queryset=models.Organisatie.objects, allow_null=True,
                                                        required=False)
    event_model = models.ActiviteitEventLog
    start_time = serializers.DateTimeField(allow_null=True, required=False)
    end_time = serializers.DateTimeField(allow_null=True, required=False)

    class Meta(object):
        exclude = ('locatie', 'organisatie',)
        model = models.Activiteit

class TagDefinitionSerializer(serializers.ModelSerializer):

    class Meta(object):
        fields = ['category', 'naam']
        model = models.TagDefinition
