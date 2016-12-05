# Packages
from django.conf.urls import include, url
from rest_framework import routers
# Project
from .views import OrganisatieViewSet, ActiviteitViewSet, LocatieViewSet, TagsApiView

nrouter = routers.SimpleRouter()
nrouter.register(r'organisatie', OrganisatieViewSet, base_name='organisatie')
nrouter.register(r'activiteit', ActiviteitViewSet, base_name='activiteit')
nrouter.register(r'locatie', LocatieViewSet, base_name='locatie')

urlpatterns = [
    url(r'^data/', include(nrouter.urls)),
    url(r'^tags/$', TagsApiView.as_view()),
    url(r'^tags/([\w-]+)/$', TagsApiView.as_view()),
]