from django.db import models
from ubicacion.models import Comuna, Ciudad
# Create your models here.

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=30)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    direccion = models.CharField(max_length=255)
    telefono = models.IntegerField()
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)