# Packages
from django.conf.urls import url
# Project
from api import views

urlpatterns = [
    url(r'^zorg/zoek/(activiteit|locatie|organisatie)/$', views.search),
    url(r'^zorg/zoek/$', views.search),
    url(r'^zorg/typeahead/$', views.typeahead),
    url(r'^zorg/openapi.yml', views.openapi)
]
