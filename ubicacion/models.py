from django.db import models

# Create your models here.
class Ciudad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)

class Comuna(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)


class Direccion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)