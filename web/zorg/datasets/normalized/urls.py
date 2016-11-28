# Packages
from rest_framework import routers
# Project
from .views import OrganisatieViewSet

nrouter = routers.SimpleRouter()
nrouter.register(r'organisatie', OrganisatieViewSet, base_name='organisatie')

