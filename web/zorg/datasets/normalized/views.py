# Packages
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from rest_framework import viewsets

# Project
from .models import Organisatie, Activiteit, Locatie, TagDefinition
from .serializers import OrganisatieSerializer, ActiviteitSerializer, LocatieSerializer, TagDefinitionSerializer


class ZorgViewSet(viewsets.ModelViewSet):
    def get_object(self):
        queryset = self.get_queryset()
        filter = {
            self.lookup_field: self.kwargs[self.lookup_field]
        }
        return get_object_or_404(queryset, **filter)


class OrganisatieViewSet(ZorgViewSet):
    serializer_class = OrganisatieSerializer

    def get_queryset(self):
        return Organisatie.objects.all()


class ActiviteitViewSet(ZorgViewSet):
    serializer_class = ActiviteitSerializer

    def get_queryset(self):
        return Activiteit.objects.all()


class LocatieViewSet(ZorgViewSet):
    serializer_class = LocatieSerializer

    def get_queryset(self):
        return Locatie.objects.all()


class TagDefinitionViewSet(viewsets.ModelViewSet):
    serializer_class = TagDefinitionSerializer

    def get_queryset(self):
        return TagDefinition.objects.filter(category='BETAALD')


class TagsApiView(ListView):
    """
    Read only api endpoint for tags
    Works for listing all tags and for specific tag name
    """

    def get_queryset(self):
        try:
            return TagDefinition.objects.filter(category=self.args[0])
        except IndexError:
            return TagDefinition.objects.all()

    def render_to_response(self, context, **response_kwargs):
        resp = TagDefinitionSerializer(list(context['object_list']), many=True)
        return JsonResponse(resp.data, status=200, safe=False)
