# Packages
from django.conf.urls import include, url
from django.contrib import admin
# Project
from api.views import ZoekApiView, TermsZoekView


urlpatterns = [
    url(r'^zorg/zoek/activiteit/$', ZoekApiView.as_view(), {'search_for': 'activiteit'}),
    url(r'^zorg/zoek/locatie/$', ZoekApiView.as_view(), {'search_for': 'locatie'}),
    url(r'^zorg/zoek/organisatie/$', ZoekApiView.as_view(), {'search_for': 'organisatie'}),
    url(r'zorg/zoek/thema/$', TermsZoekView.as_view()),
    url(r'zorg/zoek/$', ZoekApiView.as_view()),
]
