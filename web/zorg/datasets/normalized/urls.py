# Packages
from rest_framework import routers
# Project
from .views import OrganisatieViewSet, ActiviteitViewSet, LocatieViewSet

nrouter = routers.SimpleRouter()
nrouter.register(r'organisatie', OrganisatieViewSet, base_name='organisatie')
nrouter.register(r'activiteit', ActiviteitViewSet, base_name='activiteit')
nrouter.register(r'locatie', LocatieViewSet, base_name='locatie')
