# Packages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from rest_framework import viewsets
from rest_framework.response import Response
# Project
from .models import Organisatie, Activiteit, Locatie
from .serializers import OrganisatieSerializer, ActiviteitSerializer, LocatieSerializer


class ZorgViewSet(viewsets.ModelViewSet):

    def get_object(self):
        queryset = self.get_queryset()
        filter = {
            self.lookup_field: 'CODE-' + self.kwargs[self.lookup_field]
        }
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


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


class TagsApiView(ListView):
    """
    Read only api endpoint for tags
    Works for listing all tags and for specific tag name
    """
    def get_queryset(self):
        try:
            return Activiteit.objects.filter(tags__icontains=self.args[0])
        except IndexError:
            return Activiteit.objects.all()

    def render_to_response(self, context, **response_kwargs):
        resp = ActiviteitSerializer(list(context['object_list']), many=True)
        return JsonResponse(resp.data, status=200, safe=False)
