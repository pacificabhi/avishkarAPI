from django.urls import path
from .import views

urlpatterns = [
    path('createteam/', views.CreateTeam.as_view(), name='createteam'),
    path('addteammember/', views.AddTeamMember.as_view(), name='addteammember'),
    path('removeteammember/', views.RemoveTeamMember.as_view(), name='removeteammember'),
    path('joinrequestdecision/', views.JoinRequestDecision.as_view(), name='joinrequestdecision'),
]
