from ubicacion.models import Ciudad, Comuna
from authentication.models import CustomUser
from authentication.serializers import UserSerializer
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from .serializers import FacturaSerializer, OrdenTrabajoListSerializer, OrdenTrabajoSerializer, ReparacionSerializer
from .models import EstadoFactura, OrdenTrabajo, Reparacion
from rest_framework import permissions
from .utils import docCreate
from rest_framework import serializers
import os
from django_auto_prefetching import AutoPrefetchViewSetMixin


class OrdenTrabajoList(AutoPrefetchViewSetMixin,ListCreateAPIView):

    queryset= OrdenTrabajo.objects.all()
    permission_classes= (permissions.IsAuthenticated,)
    serializer_class= OrdenTrabajoSerializer

    def create(self, request, *args, **kwargs):
        request.data['autor_id'] = request.user.pk
        
        return super().create(request, *args, **kwargs)

class OrdenTrabajoListado(AutoPrefetchViewSetMixin,ListAPIView):
    serializer_class = OrdenTrabajoSerializer
    queryset= OrdenTrabajo.objects.filter()
    permission_classes= (permissions.IsAuthenticated,)




class OrdenTrabajoDetalle(AutoPrefetchViewSetMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = OrdenTrabajoSerializer
    queryset= OrdenTrabajo.objects.all()
    pagination_class = None
    permission_classes= (permissions.IsAuthenticated,)
    lookup_field="id"


class FacturaList(AutoPrefetchViewSetMixin, ListCreateAPIView):
    serializer_class = FacturaSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = EstadoFactura.objects.all()

class ReparacionList(ListCreateAPIView):
    serializer_class = ReparacionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Reparacion.objects.all()
# Create your views here.
