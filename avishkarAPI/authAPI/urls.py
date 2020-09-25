from django.urls import path
from .import views

from rest_framework.authtoken.views import obtain_auth_token  # <-- Here


urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='registeruser'),
    path('changepassword/', views.ChangePassword.as_view(), name='changepassword'),
    path('reset-password/', views.ResetPassword.as_view(), name='resetpassword'),
    path('lock/', views.LockUser.as_view(), name='LockUser'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('updatenameandemail/', views.UpdateUserNameAndEmail.as_view(), name='updatenameandemail'),
    path('updatecontact/', views.UpdateUserDetails.as_view() , name='updatecontact'),
    path('updatefees/', views.UpdateFeesStatus.as_view(), name='updatefees'),
    path('getuserdetails/', views.GetUserDetails.as_view(), name='getuserdetails'),
    path('getuserdetailsbyusername/', views.GetUserDetailsByUsername.as_view(), name='getuserdetailsbyusername'),
    path('hello/', views.HelloView.as_view(), name='hello'),
]