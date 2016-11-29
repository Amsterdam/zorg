# Packages
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
# Project
from .models import Organisatie, Activiteit, Locatie
from .serializers import OrganisatieSerializer, ActiviteitSerializer, LocatieSerializer


class ZorgViewSet(viewsets.ModelViewSet):

    def get_object(self):
        print(self.kwargs)

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
