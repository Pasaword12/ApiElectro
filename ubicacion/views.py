from django.db.models import query
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import CiudadSerializer, ComunaSerializer, DireccionSerializer
from .models import Ciudad, Comuna, Direccion
from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

# Create your views here.


class CiudadList(AutoPrefetchViewSetMixin, ListCreateAPIView):
    serializer_class = CiudadSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Ciudad.objects.all()
    pagination_class = LargeResultsSetPagination



class ComunaList(AutoPrefetchViewSetMixin, ListCreateAPIView):
    serializer_class = ComunaSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Comuna.objects.all()
    pagination_class = LargeResultsSetPagination


    def get_queryset(self):
        return super().get_queryset()

class DireccionList(AutoPrefetchViewSetMixin, ListCreateAPIView):
    serializer_class = DireccionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Direccion.objects.all()
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return super().get_queryset()
