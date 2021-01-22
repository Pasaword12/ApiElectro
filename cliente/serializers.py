from .models import Cliente
from ubicacion.serializers import ComunaSerializer, CiudadSerializer
from ubicacion.models import Comuna, Ciudad
from rest_framework import serializers



class ClienteSerializer(serializers.ModelSerializer):
    ciudad = CiudadSerializer(read_only=True)
    ciudad_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Ciudad.objects.all(), source='ciudad')
    comuna = ComunaSerializer(read_only=True)
    comuna_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Comuna.objects.all(), source='comuna')
    
    class Meta:
        model = Cliente
        fields=['id', 'rut', 'nombre', 'email', 'direccion', 'telefono', 'comuna', 'comuna_id', 'ciudad', 'ciudad_id']