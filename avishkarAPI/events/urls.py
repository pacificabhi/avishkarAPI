from django.urls import path
from .import views

urlpatterns = [
    path('createteam/', views.CreateTeam.as_view(), name='createteam'),
]
