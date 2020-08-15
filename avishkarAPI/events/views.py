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


class AddTeamMember(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    def post(self, request):

        team_id = request.POST.get("teamid").strip()
        team = EventTeam.objects.filter(team_id=team_id).first()

        if not team:
            context = {"success": False, "errors" : ["Team with team id {} is not found".format(team_id)]}
            return Response(context)

        member_username = request.POST.get("memberusername").strip()
        member = User.objects.filter(username=member_username).first()

        if not member:
            context = {"success": False, "errors" : ["User with username {} is not found".format(member_username)]}
            return Response(context)

        if member.is_staff:
            context = {"success": False, "errors" : ["User with username {} is staff member".format(member_username)]}
            return Response(context)

        if not member.userdetails.is_fees_paid():
            context = {"success": False, "errors" : ["User with username {} is not eligible because of not paying registration fees".format(member_username)]}
            return Response(context)

        if member in team.team_members.all():
            context = {"success": False, "errors" : ["User with username {} is already a team member".format(member_username)]}
            return Response(context)

        if member in team.pending_members.all():
            context = {"success": False, "errors" : ["Join Team request has been already sent to {}".format(member_username)]}
            return Response(context)

        is_mnnit = False
        if team.team_admin.userdetails.college == "MNNIT":
            is_mnnit = True

        if is_mnnit and not member.userdetails.college =="MNNIT":
            context = {"success": False, "errors" : ["You can add only users from MNNIT"]}
            return Response(context)

        team.pending_members.add(member)

        context = {"success": True, "message" : "Join Team request has been sent to {}".format(member_username)}
        return Response(context)