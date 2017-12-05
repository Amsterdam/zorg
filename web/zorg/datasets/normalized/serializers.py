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

    def get_guid(self, **kwargs):
        return events.guid_from_id(
            self.context['request'].user, kwargs.get('id', ''))

    def create(self, validated_data):
        # Creating the guid
        guid = self.get_guid(id=validated_data['id'])
        # If a guid is given, remove it from the data
        if 'guid' in validated_data:
            del validated_data['guid']
        # There can be two cases in which create can be made:
        # 1. There is no previous entry
        # 2. The last event was  delete
        prev_events = list(
            self.event_model.objects.filter(guid=guid).order_by('sequence'))

        if prev_events:
            sequence = 0

        elif prev_events[-1].event_type == 'D':
            sequence = prev_events[-1].sequence + 1
        else:
            # Does not match creation rule
            # @TODO convert to self.fail call
            raise ValidationError('Object already exists')
        event_data = validated_data.copy()
        if 'tags' in self.initial_data:
            event_data['tags'] = self.initial_data['tags']

        event = self.event_model(
            guid=guid,
            sequence=sequence,
            event_type='C',
            data=event_data
        )
        new_item = event.save()
        return new_item

    def update(self, instance, validated_data):
        # Creating the guid
        guid = self.get_guid(id=validated_data['id'])

        # Checking for authorized access
        if guid != instance.guid:
            raise ValidationError('Access not allowed')

        # There can bew two cases in which create can be made:
        # 1. There is no previous entry
        # 2. The last event was a delete
        prev_events = list(
            self.event_model.objects.filter(guid=guid).order_by('sequence'))
        if prev_events or prev_events[-1].event_type == 'D':
            # @TODO convert to self.fail call
            raise ValidationError('Object not found')
        else:
            sequence = prev_events[-1].sequence + 1

        event_data = validated_data.copy()
        if 'tags' in self.initial_data:
            event_data['tags'] = self.initial_data['tags']
        event = self.event_model(
            guid=guid,
            sequence=sequence,
            event_type='U',
            data=event_data
        )
        item = event.save()

        return item


class ContactSerializer(serializers.JSONField):
    """ Hide 'contact field'
    """

    def to_representation(self, instance):
        return {
            "email": None,
            "tel": None
        }


class OrganisatieSerializer(ZorgModelSerializer):
    locatie_id = serializers.PrimaryKeyRelatedField(queryset=models.Locatie.objects, allow_null=True, required=False)
    event_model = models.OrganisatieEventLog
    contact = ContactSerializer()

    def get_guid(self, **kwargs):
        return events.guid_from_id(self.context['request'].user, '')

    class Meta(object):
        exclude = ('locatie',)
        model = models.Organisatie
        extra_kwargs = {'client': {'required': 'False'}}


class LocatieSerializer(ZorgModelSerializer):
    event_model = models.LocatieEventLog

    class Meta(object):
        fields = '__all__'
        model = models.Locatie


class TagDefinitionSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        return obj.naam

    class Meta(object):
        fields = ['category', 'naam']
        model = models.TagDefinition


class LocatieIdSerializer(serializers.PrimaryKeyRelatedField):
    """
    Check whether the location_id is already a location guid, otherwise
    lookup the guid taken from the user session, and prepend this.
    """
    def to_internal_value(self, data):
        guid = events.guid_from_id(self.context['request'].user, data)

        if data.startswith(guid[0:4]):
            return super().to_internal_value(data)
        return super().to_internal_value(guid)


class OrganisatieIdSerializer(serializers.PrimaryKeyRelatedField):
    """
    Check whether the organisation_id is already a organisation guid, otherwise
    lookup the organisatie using the guid taken from the user session and
    return the organisation guid.
    """
    def to_internal_value(self, data):
        guid = events.guid_from_id(self.context['request'].user, '')

        if data.startswith(guid):
            return super().to_internal_value(data)

        organisatie = models.Organisatie.objects.filter(id=data, guid=guid)[0]
        return super().to_internal_value(organisatie.guid)


class ActiviteitSerializer(ZorgModelSerializer):
    locatie_id = LocatieIdSerializer(
        queryset=models.Locatie.objects, allow_null=True, required=False)
    organisatie_id = OrganisatieIdSerializer(
        queryset=models.Organisatie.objects, allow_null=True, required=False)
    event_model = models.ActiviteitEventLog
    start_time = serializers.DateTimeField(allow_null=True, required=False)
    end_time = serializers.DateTimeField(allow_null=True, required=False)
    tags = TagDefinitionSerializer(read_only=True, many=True, required=False)

    def save(self, *args, **kwargs):
        super(ActiviteitSerializer, self).save(*args, **kwargs)

        # validate many to many relations for tags
        valid_tags = []
        models.Activiteit.objects.get(pk=self.data['guid']).tags.clear()
        if 'tags' in self.initial_data:
            for tag_name in self.initial_data['tags']:
                fetched_tags = (
                    models.TagDefinition.objects
                    .filter(naam=tag_name))
                if fetched_tags.count() > 0:
                    valid_tags.append(fetched_tags.first())

            if valid_tags:
                models.Activiteit.objects.get(
                    pk=self.data['guid']).tags.add(*valid_tags)

    class Meta(object):
        exclude = ('locatie', 'organisatie',)
        model = models.Activiteit
