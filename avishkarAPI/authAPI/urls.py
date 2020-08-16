from django.urls import path
from .import views

from rest_framework.authtoken.views import obtain_auth_token  # <-- Here


urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='registeruser'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('updatenameandemail/', views.UpdateUserNameAndEmail.as_view(), name='updatenameandemail'),
    path('updatecontact/', views.UpdateUserDetails.as_view() , name='updatecontact'),
    path('updatefees/', views.UpdateFeesStatus.as_view(), name='updatefees'),
    path('getuserdetails/', views.GetUserDetails.as_view(), name='getuserdetails'),
    path('getuserdetailsbyusername/', views.GetUserDetailsByUsername.as_view(), name='getuserdetailsbyusername'),
    path('hello/', views.HelloView.as_view(), name='hello'),
]