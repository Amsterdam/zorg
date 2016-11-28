# Packages
from rest_framework import mixins, generics
# Project
from .models import Organisatie
from .serializers import OrganisatieSerialiser


#class OrganisatieViewSet(generics.RetrieveUpdateDestroyAPIView):
class OrganisatieViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):
    serializer_class = OrganisatieSerialiser

    def get_queryset(self):
        return Organisatie.objects.all()

    def perform_create(self, serializer):
        print('perform_create')
        serializer.save(self.request.data)

    def perform_update(self, serializer):
        pass

    def perform_destroy(self, instance):
        pass

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
