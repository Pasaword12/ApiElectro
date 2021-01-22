from typing import Type
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class CustomManager(BaseUserManager):
    def create_user(self, email, nombre, apellidos, password=None, **extra_fields):
        if email is None:
            raise TypeError("El Usuario debe tener un email")
        if nombre is None:
            raise TypeError("El Usuario debe tener un nombre")
        if apellidos is None:
            raise TypeError("El Usuario debe tener apellidos")

        user= self.model(email = self.normalize_email(email), nombre = nombre, apellidos = apellidos)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, nombre, apellidos, password=None, **extra_fields):
        if password is None:
            raise TypeError("La contraseña no puede estar vacia")

        user= self.create_user(email, nombre, apellidos, password)
        user.is_superuser=True
        user.is_staff=True
        user.is_verified=True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=86, unique=True)
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    is_verified = models.BooleanField(default= False)
    is_active = models.BooleanField(default= True)
    is_staff = models.BooleanField(default= False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellidos']

    objects= CustomManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }