from django.db import models


# Create your models here.
class Contacto(models.Model):
    id = models.AutoField(primary_key=True)
    correo = models.EmailField(max_length=255)
    nombrecompleto = models.CharField(max_length=255)
    telefono = models.IntegerField()
    observaciones = models.TextField()

    class Meta:
        ordering = ['-id']