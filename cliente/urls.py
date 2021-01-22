from django.urls import path
from .views import ClienteList, ClienteDetalle

urlpatterns=[
    path('/', ClienteList.as_view(), name='cliente'),
    path('/<int:id>', ClienteDetalle.as_view(), name='clienteDetalle'),
]