from django.urls import path
from .views import ContactoDetalle, ContactoList

urlpatterns=[
    path('/', ContactoList.as_view(), name='contacto'),
    path('/<int:id>', ContactoDetalle.as_view(), name='contactoDetalle')
]