# Packages
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from rest_framework import viewsets
from datasets.normalized.batch import process_updates

import django_rq
from rq import Queue
from redis import Redis

# Project
from .models import Organisatie, Activiteit, Locatie, TagDefinition
from .serializers import OrganisatieSerializer, ActiviteitSerializer, LocatieSerializer, TagDefinitionSerializer


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

class TagDefinitionViewSet(viewsets.ModelViewSet):
    serializer_class = TagDefinitionSerializer

    def get_queryset(self):
        return TagDefinition.objects.filter(category='BETAALD')


class TagsApiView(ListView):
    """
    Read only api endpoint for tags
    Works for listing all tags and for specific tag name
    """

    def get_queryset(self):
        try:
            return TagDefinition.objects.filter(category=self.args[0])
        except IndexError:
            return TagDefinition.objects.all()

    def render_to_response(self, context, **response_kwargs):
        resp = TagDefinitionSerializer(list(context['object_list']), many=True)
        return JsonResponse(resp.data, status=200, safe=False)


class BatchUpdateView(viewsets.ViewSet):
    """
    Add new events and locations in batch
    [
        {'add': {'ts': <timestamp>, 'location': <location-rec>, 'event': <event-rec>'},
        {'patch': {'ts': <timestamp>, 'location': <location-changes>, 'event': <event-changes>'},
        {'delete': {'ts': <timestamp>, 'location': <location-guid>, 'event': <event-guid>'},
    ]
    """

    def create(self, request):
        """

        :param request:
        :return:
        """
        queue = django_rq.get_queue('low')
        res = queue.enqueue(process_updates, request.data)
        return_value = {
            "jobid": res.id,
            "status": res.status,
            "result": {
                "added": 0,
                "updated": 0,
                "deleted": 0,
                "messages": ""
            }
        }
        return JsonResponse(return_value, status=202)

    def get_job(self, request, job_id):
        """
        Get the job status from the queues
        :param request:
        :param job_id:
        :return:
        """
        q = Queue(name='low', connection=Redis())
        res = q.fetch_job(job_id)
        if res:
            return_value = {
                "jobid": job_id,
                "status": res.status,
                "result": {
                    "added": 0,
                    "updated": 0,
                    "deleted": 0,
                    "messages": ""
                }
            }
        else:
            return_value = {}
        return JsonResponse(return_value, status=200)
