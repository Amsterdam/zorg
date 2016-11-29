# Packages
from rest_framework import viewsets
# Project
from .models import Organisatie, Activiteit, Locatie
from .serializers import OrganisatieSerializer, ActiviteitSerializer, LocatieSerializer


class OrganisatieViewSet(viewsets.ModelViewSet):

    serializer_class = OrganisatieSerializer
    queryset = Organisatie.objects.all()


class ActiviteitViewSet(viewsets.ModelViewSet):

    serializer_class = ActiviteitSerializer
    queryset = Activiteit.objects.all()


class LocatieViewSet(viewsets.ModelViewSet):

    serializer_class = LocatieSerializer
    queryset = Locatie.objects.all()
