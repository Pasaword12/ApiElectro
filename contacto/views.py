from .models import Contacto
from .serializers import ContactoSerializer
from django.shortcuts import render
from rest_framework import permissions
from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

# Create your views here.
class ContactoList(AutoPrefetchViewSetMixin, ListCreateAPIView):
    serializer_class = ContactoSerializer
    queryset = Contacto.objects.all()


class ContactoDetalle(AutoPrefetchViewSetMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = ContactoSerializer
    queryset= Contacto.objects.all()
    pagination_class = None
    lookup_field="id"
