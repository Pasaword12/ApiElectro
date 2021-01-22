from django.db.models import query
from django.shortcuts import render
from drf_yasg import openapi
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.serializers import Serializer
from .serializers import EmailVerificationSerializer, RequestPasswordResetEmailSerializer, UserSerializer, LoginSerializer, SetNewPasswordAPIViewSerializer, LogoutSerializer, UserSerializerConId
from rest_framework.response import Response
from rest_framework import status, views
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import get_serializer_class, swagger_auto_schema
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from rest_framework import permissions
from django_auto_prefetching import AutoPrefetchViewSetMixin

# Create your views here.
class RegisterView(AutoPrefetchViewSetMixin, GenericAPIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            datax = request.data
            user = CustomUser.objects.get(email=datax['email'])
            token = RefreshToken.for_user(user).access_token

            sitio_actual =  get_current_site(request).domain


            
            relativeLink = reverse('email-verify')
            absurl = 'http://' + sitio_actual + relativeLink + '?token=' + str(token)
            email_body = 'Hola '+ user.nombre + ' Usa este enlace para verificar tu correo \n'+ absurl
            data={'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verifica tu correo'}
            Util.send_email(data)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(AutoPrefetchViewSetMixin, views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Descripcion', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256' )
            user = CustomUser.objects.get(id= payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email':'Activacion Exitosa'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as ex:
            return Response({'error':'Activacion Expirada'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as ex:
            return Response({'error':'Token Invalido'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(AutoPrefetchViewSetMixin, generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer= self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception= True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(AutoPrefetchViewSetMixin, generics.GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer
    def post(self,request):
        data = {'request': request, 'data': request.data }
        serializer = self.serializer_class(data=data)

        email=request.data['email']

        if CustomUser.objects.filter(email = email).exists():
            user = CustomUser.objects.get(email = email)
            uidb64= urlsafe_base64_encode(smart_bytes(user.id))
            token= PasswordResetTokenGenerator().make_token(user)

            sitio_actual =  get_current_site(request = request).domain


            relativeLink = reverse('reset_confirm', kwargs={'uidb64': uidb64, 'token':token})
            absurl = 'http://' + sitio_actual + relativeLink 
            email_body = 'Hola, \n  Usa este enlace para reiniciar tu contraseña \n'+ absurl
            data={'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reiniciar tu Contraseña'}
            Util.send_email(data)
        return Response({'sucess': 'ha sido enviado un correo con un enlace para reiniciar su contraseña'}, status = status.HTTP_200_OK)

class PasswordTokenCheckAPI(AutoPrefetchViewSetMixin, generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token no valido, por favor solicite uno nuevamente'}, status= status.HTTP_401_UNAUTHORIZED)

            return Response({'sucess': True, 'mensaje': 'Credenciales validas', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)


        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'Token no valido, por favor solicite uno nuevamente'}, status= status.HTTP_401_UNAUTHORIZED)

class SetNewPasswordAPIView(AutoPrefetchViewSetMixin, generics.GenericAPIView):
    serializer_class = SetNewPasswordAPIViewSerializer

    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'sucess': True, 'mensaje': 'reinicio de contraseña exitoso'}, status=status.HTTP_200_OK)


class LogoutAPIView(AutoPrefetchViewSetMixin, generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def post(self, request):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthUserAPIView(AutoPrefetchViewSetMixin, GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer()
    def get(self, request):
        user = CustomUser.objects.get(pk=request.user.pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class AuthUsersAPIView(AutoPrefetchViewSetMixin, generics.ListAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializerConId

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        iduser = self.request.query_params.get('id', None)
        if iduser is not None:
            queryset = queryset.filter(pk=iduser)
        return queryset
