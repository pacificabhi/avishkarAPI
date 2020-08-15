from django.urls import path
from .import views

from rest_framework.authtoken.views import obtain_auth_token  # <-- Here


urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='registeruser'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('hello/', views.HelloView.as_view(), name='hello'),
]