from ubicacion.serializers import CiudadSerializer, ComunaSerializer
from ubicacion.models import Ciudad, Comuna
from authentication.serializers import UserSerializer, UserSerializerConId
from authentication.models import CustomUser
from django.db.models import fields
from rest_framework import serializers
from .models import EstadoFactura, OrdenTrabajo, Reparacion

class FacturaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  EstadoFactura
        fields = ['id', 'nombre']

class ReparacionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  Reparacion
        fields = ['id', 'nombre']

class OrdenTrabajoListSerializer(serializers.ModelSerializer):
    factura_estado = FacturaSerializer(read_only=True)
    factura_estado_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=EstadoFactura.objects.all().select_related('factura_estado'), source='factura_estado')
    autor = UserSerializerConId(read_only=True)
    autor_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=CustomUser.objects.all().select_related('autor'), source='autor')



    class Meta:
        model=OrdenTrabajo
        fields=['id','nombre', 'recepcion', 'factura','factura_estado', 'factura_estado_id', 'autor', 'autor_id']    

class OrdenTrabajoSerializer(serializers.ModelSerializer):

    factura_estado = FacturaSerializer(read_only=True)
    factura_estado_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=EstadoFactura.objects.all(), source='factura_estado')
    ciudad = CiudadSerializer(read_only=True)
    ciudad_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Ciudad.objects.all(), source='ciudad')
    comuna = ComunaSerializer(read_only=True)
    comuna_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Comuna.objects.all(), source='comuna')
    tecnico = UserSerializerConId(read_only=True, many=True)
    tecnico_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=CustomUser.objects.all(), source='tecnico', many=True)
    reparacion = ReparacionSerializer(read_only=True)
    reparacion_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Reparacion.objects.all(), source='reparacion')
    autor = UserSerializer(read_only=True)
    autor_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=CustomUser.objects.all(), source='autor')



    class Meta:
        model=OrdenTrabajo
        fields=['id', 'rut','nombre','telefono', 'ciudad', 'ciudad_id', 'direccion', 'recepcion', 'comuna', 'comuna_id' , 'email', 'marca', 'reparacion', 'reparacion_id' , 'tecnico', 'tecnico_id' ,  'factura', 'modelo', 'falla', 'observacion', 'nombre_cliente', 'factura_estado', 'factura_estado_id', 'firma_tecnico', 'firma_cliente', 'autor', 'autor_id']