from .models import Cliente
from .serializers import ClienteSerializer
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from django_auto_prefetching import AutoPrefetchViewSetMixin
# Create your views here.

class ClienteList(AutoPrefetchViewSetMixin, ListCreateAPIView):
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()
    permission_classes= (permissions.IsAuthenticated,)




class ClienteDetalle(AutoPrefetchViewSetMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()
    permission_classes= (permissions.IsAuthenticated,)
    lookup_field = "id"