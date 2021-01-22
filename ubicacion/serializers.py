from rest_framework import serializers
from .models import Ciudad, Comuna, Direccion

class CiudadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  Ciudad
        fields = ['id', 'nombre']

class ComunaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  Comuna
        fields = ['id', 'nombre']

class DireccionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  Direccion
        fields = ['id', 'nombre']