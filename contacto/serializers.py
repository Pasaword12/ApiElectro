from django.db.models import fields
from rest_framework import serializers
from .models import Contacto


class ContactoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  Contacto
        fields = ['id', 'correo', 'nombrecompleto', 'telefono', 'observaciones']
        