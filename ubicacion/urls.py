from django.urls import path
from .views import CiudadList, ComunaList, DireccionList

urlpatterns=[
    path('ciudad/', CiudadList.as_view(), name='ciudad'),
    path('comuna/', ComunaList.as_view(), name='comuna'),
]