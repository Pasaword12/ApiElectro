from rest_framework import fields, serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.exceptions import TokenError
from .models import CustomUser
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken
 

class UserSerializerConId(serializers.ModelSerializer):
    id = serializers.IntegerField()
    email = serializers.EmailField(max_length=255, min_length=4)
    nombre = serializers.CharField(max_length=255, min_length= 2)
    apellidos = serializers.CharField(max_length=255, min_length= 2)
    password = serializers.CharField(max_length=65, min_length=8, write_only = True)
    is_staff = serializers.BooleanField()
    class Meta:
        model = CustomUser
        fields=['id','email', 'nombre', 'apellidos', 'password', 'is_staff']

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=4)
    nombre = serializers.CharField(max_length=255, min_length= 2)
    apellidos = serializers.CharField(max_length=255, min_length= 2)
    password = serializers.CharField(max_length=65, min_length=8, write_only = True)
    is_staff = serializers.BooleanField()
    class Meta:
        model = CustomUser
        fields=['email', 'nombre', 'apellidos', 'password', 'is_staff']

    
    def validate(self, attrs):
        email =attrs.get('email', '')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('Email ya esta en uso')})
        return super().validate(attrs)

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = {'token'}
    
class LoginSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(max_length=255, min_length=4)
    nombre = serializers.CharField(max_length=255, min_length=2, read_only = True)
    apellidos = serializers.CharField(max_length=255, min_length=2, read_only = True)
    password = serializers.CharField(max_length=68, min_length=6, write_only = True)
    is_staff = serializers.BooleanField(read_only=True)
    tokens = serializers.SerializerMethodField()


    def get_tokens(self, obj):

        user = CustomUser.objects.get(email=obj['email'])

        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }

    class Meta:
        model=CustomUser
        fields=['email', 'nombre', 'apellidos', 'password', 'is_staff', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Datos Ingresados incorrectamente, intenta nuevamente')

        if not user.is_active:
            raise AuthenticationFailed('Cuenta desabilitada, contacta al administrador')

        if not user.is_verified:
            raise AuthenticationFailed('Su correo no ha sido verificado')
        
        return {
            'email': user.email,
            'nombre': user.nombre,
            'apellidos': user.apellidos,
            'is_staff': user.is_staff,
            'tokens': user.tokens()
        }

        return super().validate(attrs)


class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

class SetNewPasswordAPIViewSerializer(serializers.Serializer):
    password=serializers.CharField(min_length=6, max_length=68, write_only= True)
    token=serializers.CharField(min_length=1, write_only= True)
    uidb64=serializers.CharField(min_length=1, write_only= True)


    class Meta:
        fields=['password', 'token', 'uidb64']


    def validate(self, attrs):
        try:
            password=attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id=force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('El enlace de reinicio es invalido', 401)

            user.set_password(password)
            user.save()
            return (user)
        except Exception as e:
            raise AuthenticationFailed('El enlace de reinicio es invalido', 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


    default_error_messages = {
        'token_invalido': 'Token expirado o invalido'
    }
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()
        except TokenError as identifier:
            self.fail('token_invalido')
