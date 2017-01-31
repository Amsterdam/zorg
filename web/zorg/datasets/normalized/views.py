# Packages
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from rest_framework import viewsets
# Project
from .models import Organisatie, Activiteit, Locatie
from .serializers import OrganisatieSerializer, ActiviteitSerializer, LocatieSerializer
from datasets.general import events


class ZorgViewSet(viewsets.ModelViewSet):

    def get_object(self):
        queryset = self.get_queryset()
        filter = {
            self.lookup_field: self.kwargs[self.lookup_field]
        }
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, pk=None):
        prev_events = list(self.serializer_class.event_model.objects.filter(
                      guid=pk).order_by('sequence'))
        if len(prev_events) == 0 or prev_events[-1].event_type == 'D':
            raise ValidationError('Object not found')
        else:
            sequence = prev_events[-1].sequence + 1

        event = self.serializer_class.event_model(
            guid=pk,
            sequence=sequence,
            event_type='D',
            data={}
        )
        item = event.save()
        data = {
            'success': True,
            'guid': pk,
        }
        return JsonResponse(data, status=200, safe=False)

    def update(self, request, pk=None):
        return super(ZorgViewSet, self).update(request, pk, partial=True)


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


class TagsApiView(ListView):
    """
    Read only api endpoint for tags
    Works for listing all tags and for specific tag name
    """
    def get_queryset(self):
        try:
            return Activiteit.objects.filter(tags__icontains=self.args[0])
        except IndexError:
            return Activiteit.objects.all()

    def render_to_response(self, context, **response_kwargs):
        resp = ActiviteitSerializer(list(context['object_list']), many=True)
        return JsonResponse(resp.data, status=200, safe=False)
