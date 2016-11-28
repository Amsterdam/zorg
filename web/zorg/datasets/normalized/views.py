# Packages
from rest_framework import viewsets
# Project
from .models import Organisatie
from .serializers import OrganisatieSerializer


class OrganisatieViewSet(viewsets.ModelViewSet):

    serializer_class = OrganisatieSerializer
    queryset = Organisatie.objects.all()

