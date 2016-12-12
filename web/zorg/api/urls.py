# Packages
from django.conf.urls import include, url
from django.contrib import admin
# Project
from api.views import ZoekApiView

urlpatterns = [
    url(r'^zorg/zoek/activiteit/', ZoekApiView.as_view(), {'search_for': 'activiteit'}),
]

