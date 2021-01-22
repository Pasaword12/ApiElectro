from django.urls import path
from django.urls.resolvers import URLPattern
from .views import AuthUsersAPIView, LogoutAPIView, RegisterView, RequestPasswordResetEmail, SetNewPasswordAPIView, VerifyEmail, LoginView, PasswordTokenCheckAPI,AuthUserAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)




urlpatterns=[
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='reset_confirm'),
    path('reset-email', RequestPasswordResetEmail.as_view(), name='reset-email'),
    path('reset-complete', SetNewPasswordAPIView.as_view(), name='reset_complete'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', AuthUserAPIView.as_view(), name='user'),
    path('users/', AuthUsersAPIView.as_view(), name='users')
]