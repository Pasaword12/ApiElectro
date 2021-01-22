from ubicacion.models import Ciudad, Comuna
from django.db import models
from authentication.models import CustomUser
from django.db.models.fields.related import ForeignKey

class EstadoFactura(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

class Reparacion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)


class OrdenTrabajo(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    rut = models.CharField(max_length=30, db_index=True)
    nombre = models.CharField(max_length=200)
    telefono = models.IntegerField()
    ciudad = ForeignKey(Ciudad, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    recepcion = models.DateTimeField(auto_now_add=True)
    comuna = ForeignKey(Comuna, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True) #Opcional
    marca = models.CharField(max_length=255, null=True, blank=True)
    reparacion = models.ForeignKey(Reparacion, on_delete=models.CASCADE)
    tecnico = models.ManyToManyField(CustomUser, related_name='tecnicosAsignados') #Mas de un tecnico puede encargarse
    factura = models.FileField(upload_to='facturas/', null=True, blank=True) #Opcional se llenara cuando la factura se genere en la otra plataforma
    modelo = models.CharField(max_length=255, null=True, blank=True) #Opcional
    falla = models.TextField()
    observacion = models.TextField()
    nombre_cliente = models.CharField(max_length=255)
    factura_estado = models.ForeignKey(EstadoFactura, on_delete=models.CASCADE)
    firma_tecnico = models.ImageField(upload_to='firma/', null=False, blank=False)  #La firma no puede estar vacia
    firma_cliente = models.ImageField(upload_to='firma/', null=False, blank=False)  #La firma no puede estar vacia
    autor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='autorAsignado', db_index=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']


