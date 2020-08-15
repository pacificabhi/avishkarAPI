from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *

class CreateTeam(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


    def post(self, request):
        u = request.user

        if u.is_staff:
            context = {"success": False, "errors": ["You are an event staff member, You can not create teams"]}
            return Response(context)

        team_name = request.POST.get("teamname").strip()
        team = EventTeam.objects.create(team_name=team_name, team_admin=u)

        team_id = "TEAM" + str(team.pk)
        team.team_id = team_id

        team.add_team_member(u)
        team.save()

        context = {"success": True, "team_id": team_id}

        return Response(context)


