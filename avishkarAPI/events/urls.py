from django.urls import path
from .import views

urlpatterns = [
    path('createteam/', views.CreateTeam.as_view(), name='createteam'),
    path('addteammember/', views.AddTeamMember.as_view(), name='addteammember'),
    path('removeteammember/', views.RemoveTeamMember.as_view(), name='removeteammember'),
    path('joinrequestdecision/', views.JoinRequestDecision.as_view(), name='joinrequestdecision'),
    path('registertoevent/', views.RegisterToEvent.as_view(), name='registertoevent'),
    path('geteventdetails/', views.GetEventDetails.as_view(), name='geteventdetails'),
    path('getallevents/', views.GetAllEvents.as_view(), name='getallevents'),
    path('getregistereduserslistofevent/', views.GetRegisteredUsersListOfEvent.as_view(), name='getregistereduserslistofevent'),
]
