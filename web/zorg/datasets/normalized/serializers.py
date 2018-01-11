# Packages
from django.contrib.auth.models import User
from rest_framework import serializers

# Projects
from . import models


# For now, using a simple implemetation of concatinating the
# user identifier with the external id, using a dash to
# connect the two. Since we have control over the user identifier
# its possible to guarantee that a dash wont be in it.
def guid_from_id(user_identifier: User, ext_id: str) -> str:
    """
    Generating the systems own guid from the external id
    and the user identifier. The GUID needs to be associated with
    the user and not easily representable. This allows us to know
    which user did what, and prevent users from overwriting each
    others data, while mainting a reversible reference to the own
    user's id
    """
    profile = models.Profile.objects.get(auth_user=user_identifier)
    if ext_id != '':
        return f"{profile.guid}-{ext_id}"
    else:
        return profile.guid


class ZorgModelSerializer(serializers.ModelSerializer):

    def get_guid(self, **kwargs):
        return guid_from_id(
            self.context['request'].user, kwargs.get('id', ''))


class ContactSerializer(serializers.JSONField):

    def to_representation(self, instance):
        return {
            "email": None,
            "tel": None
        }


class OrganisatieSerializer(ZorgModelSerializer):
    locatie_id = serializers.PrimaryKeyRelatedField(queryset=models.Locatie.objects, allow_null=True, required=False)
    contact = ContactSerializer()

    def get_guid(self, **kwargs):
        return guid_from_id(self.context['request'].user, '')

    class Meta(object):
        exclude = ('locatie',)
        model = models.Organisatie
        extra_kwargs = {'client': {'required': 'False'}}


class LocatieSerializer(ZorgModelSerializer):

    class Meta(object):
        fields = '__all__'
        model = models.Locatie


class TagDefinitionSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        return obj.naam

    class Meta(object):
        fields = ['category', 'naam']
        model = models.TagDefinition


class ActiviteitSerializer(ZorgModelSerializer):
    start_time = serializers.DateTimeField(allow_null=True, required=False)
    end_time = serializers.DateTimeField(allow_null=True, required=False)
    tags = TagDefinitionSerializer(read_only=True, many=True, required=False)

    class Meta(object):
        exclude = ('locatie', 'organisatie',)
        model = models.Activiteit
