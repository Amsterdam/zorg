# Packages
from django.conf.urls import include, url
from rest_framework import routers
# Project
from .views import OrganisatieViewSet, ActiviteitViewSet, LocatieViewSet, TagsApiView, \
    TagDefinitionViewSet, BatchUpdateView

nrouter = routers.SimpleRouter()
nrouter.register(r'organisatie', OrganisatieViewSet, base_name='organisatie')
nrouter.register(r'activiteit', ActiviteitViewSet, base_name='activiteit')
nrouter.register(r'locatie', LocatieViewSet, base_name='locatie')

urlpatterns = [
    # url(r'^zorg/tags/(BETAALD|DAG|TIJD)/$', TagsApiView.as_view()),
    url(r'^zorg/tags/([\w-]+)/$', TagsApiView.as_view()),
    url(r'^zorg/batch_update/$', BatchUpdateView.as_view({'post': 'create'})),
    url(r'^zorg/batch_job/(?P<job_id>[0-9a-f-]+)/$', BatchUpdateView.as_view({'get': 'get_job'})),
    url(r'^zorg/', include(nrouter.urls)),
]
